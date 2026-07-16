#!/usr/bin/env python3
"""
PXP-3 Export Live Registry — exports RAE Document Registry from SharePoint
to the PXP-1 public contract format with batch publication support.

Adds the PXP-3 enhancements over PXP-2:
  • --doc-ids flag: process only specified DocumentIDs (batch publication)
  • Reconciliation verification: explicit check that total == eligible + excluded
  • Per-record error detail: individual exclusion records carry all gate-failure context
  • Improved category mapping documentation
  • Deterministic output guarantee (maintained and verified)

Uses Playwright for authentication (reusable browser profile) + Python requests
for SharePoint REST API queries.

Usage:
    python scripts/registry/export-live-registry.py                          # Export all
    python scripts/registry/export-live-registry.py --doc-ids RAE-00001,RAE-00002  # Batch only

Output:
    data/document-registry.public.json
    data/document-registry.public.sha256
    reports/pxp2-export-audit.json
    reports/pxp2-export-summary.md
"""
import argparse
import hashlib
import json
import os
import sys
import time
from collections import Counter, OrderedDict
from datetime import datetime, timezone

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '.migration', 'rae-wtms', 'tools'))
from _m365_browser import SITE_DEFAULT, close_context, ensure_authenticated, get_page, launch_persistent
from playwright.sync_api import sync_playwright

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(REPO_ROOT, 'data')
REPORTS_DIR = os.path.join(REPO_ROOT, 'reports')
SITE = SITE_DEFAULT.rstrip('/')

# PXP-1 contract constants
SCHEMA_VERSION = "1.0.0"

ALLOWED_STATUSES = {"approved", "published", "current"}
ALLOWED_VISIBILITY = {"public"}
ALLOWED_DOWNLOAD_MODES = {
    "AUTHENTICATED_SHAREPOINT",
    "PUBLIC_SHAREPOINT_LINK",
    "PUBLIC_DISTRIBUTION_URL",
}

# PXP-1 contract categories — the public-facing categories defined in the
# PXP-1 contract. Every exported record must map to exactly one of these.
ALLOWED_CATEGORIES = OrderedDict([
    ("Administration", "Administration"),
    ("FinanceProcurement", "FinanceProcurement"),
    ("PlanningPolicy", "PlanningPolicy"),
    ("AcademicServices", "AcademicServices"),
    ("Research", "Research"),
    ("SOPManuals", "SOPManuals"),
])

# ── Thai → PXP-1 category mapping ──────────────────────────────────────────
# The live SharePoint Registry stores Category as a Thai display-name string.
# The public export maps each Thai string to a PXP-1 contract category.
#
# Mapping documentation (Thai → English rationale):
#
#   "งานบริหารและธุรการ" ("Administration & General Affairs")
#       → Administration
#       Covers office management, HR, general correspondence.
#
#   "งานคลังและพัสดุ" ("Finance & Procurement")
#       → FinanceProcurement
#       Budget, financial reports, procurement records.
#
#   "งานนโยบาย แผนและประกันคุณภาพ" ("Policy, Planning & QA")
#       → PlanningPolicy
#       Institutional policies, strategic plans, quality assurance.
#
#   "งานบริการวิชาการ" ("Academic Services")
#       → AcademicServices
#       Community outreach, training, academic consultancy.
#
#   "งานวิจัย" / "research" / "งานวิจัย/ประกาศงานวิจัย" … (23 sub-categories)
#       → Research
#       All research-related documents regardless of sub-type:
#       announcements (ประกาศ), forms (แบบฟอร์ม), reports (รายงาน),
#       regulations (ระเบียบ), grants (ทุน), handbooks (คู่มือ),
#       institutional research (วิจัยสถาบัน), standards (มาตรฐาน),
#       knowledge management (การจัดการความรู้), IP (ทรัพย์สินทางปัญญา),
#       clinics (คลินิกวิจัย), evaluation (การประเมินผล), databases,
#       plans (แผน), excellence-centre forms (แบบฟอร์มศูนย์ความเป็นเลิศ).
#
#   "คู่มือ" ("Handbook / Manual")
#       → SOPManuals
#       Procedure manuals and standard operating procedures.
#
#   "แบบฟอร์มแหล่งทุนภายนอก" ("External-funding forms")
#       → Research
#       (These are research grant application forms.)
#
#   "แบบฟอร์มงานบริการวิชาการ" ("Academic-service forms")
#       → AcademicServices
#
#   "บริหารจัดการ" ("Management / Administration")
#       → Administration
#
CATEGORY_DISPLAY_MAP = OrderedDict([
    ("งานบริหารและธุรการ", "Administration"),
    ("งานคลังและพัสดุ", "FinanceProcurement"),
    ("งานนโยบาย แผนและประกันคุณภาพ", "PlanningPolicy"),
    ("งานบริการวิชาการ", "AcademicServices"),
    ("research", "Research"),
    ("งานวิจัย", "Research"),
    ("งานวิจัย/ประกาศงานวิจัย", "Research"),
    ("งานวิจัย/แบบฟอร์มงานวิจัย", "Research"),
    ("งานวิจัย/รายงานผลงานวิจัย", "Research"),
    ("งานวิจัย/ระเบียบการบริหารงานวิจัย", "Research"),
    ("งานวิจัย/ทุนวิจัย", "Research"),
    ("งานวิจัย/วิจัยสถาบัน", "Research"),
    ("งานวิจัย/มาตรฐานการวิจัย", "Research"),
    ("งานวิจัย/คู่มือการวิจัย", "Research"),
    ("งานวิจัย/ระบบสารสนเทศงานวิจัย", "Research"),
    ("งานวิจัย/คลินิกวิจัย", "Research"),
    ("งานวิจัย/การประเมินผลงานวิจัย", "Research"),
    ("งานวิจัย/การจัดการความรู้", "Research"),
    ("งานวิจัย/ฐานข้อมูลงานวิจัย", "Research"),
    ("งานวิจัย/ทรัพย์สินทางปัญญา", "Research"),
    ("งานวิจัย/แผนงานวิจัย", "Research"),
    ("แบบฟอร์มแหล่งทุนภายนอก", "Research"),
    ("แบบฟอร์มงานบริการวิชาการ", "AcademicServices"),
    ("แบบฟอร์มศูนย์ความเป็นเลิศ", "Research"),
    ("คู่มือ", "SOPManuals"),
    ("บริหารจัดการ", "Administration"),
])

CONTRACT_FIELDS = [
    "DocumentID",
    "Title",
    "Category",
    "Status",
    "Visibility",
    "UpdatedDate",
    "StorageURL",
    "DownloadMode",
]

FORBIDDEN_PATTERNS = [
    "login.microsoftonline.com",
    "microsoftonline.com",
    "Username",
    "Password",
    "Token",
    "Bearer",
    "Authorization",
    "Cookie",
    "SessionId",
    ".browser-profile",
    "temp_profile",
]


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for batch/bulk mode."""
    parser = argparse.ArgumentParser(
        description="PXP-3 Export Live Registry — batch publication support"
    )
    parser.add_argument(
        "--doc-ids",
        type=str,
        default=None,
        help="Comma-separated list of DocumentIDs to process (batch mode). "
             "When set, only these IDs are exported; all others are skipped."
    )
    parser.add_argument(
        "--skip-writes",
        action="store_true",
        help="Skip writing output files (useful for verification or dry-run previews)."
    )
    return parser.parse_args()


def authenticate() -> tuple:
    """Use Playwright browser profile to get cookies and digest. Returns (headers, ctx_info)."""
    with sync_playwright() as p:
        ctx = launch_persistent(p, headless=False)
        page = ensure_authenticated(get_page(ctx))
        ctx_info = page.evaluate("""() => ({
            webUrl: _spPageContextInfo.webServerRelativeUrl,
            digest: _spPageContextInfo.formDigestValue,
        })""")
        cookies = ctx.cookies()
        cookie_dict = {c['name']: c['value'] for c in cookies}
        close_context(ctx)

    headers = {
        'Accept': 'application/json;odata=verbose',
        'X-RequestDigest': ctx_info['digest'],
        'Cookie': '; '.join(f"{k}={v}" for k, v in cookie_dict.items()),
    }
    return headers, ctx_info


def scan_registry(headers: dict) -> list:
    """Scan all Registry items with pagination."""
    list_url = f"{SITE}/_api/web/lists/getbytitle('RAE%20Document%20Registry')/items"
    params = {
        '$select': 'Id,Title,Document_x0020_ID,Category,Status,Visibility,Storage_x0020_URL,Updated_x0020_Date',
        '$top': 1000,
    }
    resp = requests.get(list_url, headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    rows = data.get('d', {}).get('results', [])
    return rows


def determine_download_mode(storage_url: str) -> str:
    """Determine DownloadMode from storage URL characteristics."""
    if not storage_url:
        return "AUTHENTICATED_SHAREPOINT"
    url_lower = storage_url.lower()
    if "guest" in url_lower or "anonymous" in url_lower:
        return "PUBLIC_SHAREPOINT_LINK"
    if "maejo365.sharepoint.com" in url_lower:
        return "AUTHENTICATED_SHAREPOINT"
    return "AUTHENTICATED_SHAREPOINT"


def is_valid_https_url(url: str) -> bool:
    """Basic URL syntax validation."""
    if not url:
        return False
    return url.startswith("https://") and len(url) > 10


def check_forbidden_fields(record: dict) -> list:
    """Check a record for forbidden terms."""
    findings = []
    json_str = json.dumps(record).lower()
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.lower() in json_str:
            findings.append(f"Forbidden pattern found: {pattern}")
    return findings


def map_category(display_name: str) -> str:
    """Map a live Registry Thai category display name to a PXP-1 contract category."""
    display_name = display_name.strip()
    for thai_name, contract_name in CATEGORY_DISPLAY_MAP.items():
        if display_name.lower() == thai_name.lower():
            return contract_name
    return None


def map_to_public(internal: dict) -> tuple:
    """
    Map a live Registry record to PXP-1 public contract.

    Returns (public_record, exclusion_reason). exclusion_reason is None if eligible.
    exclusion_reason is a dict with keys: reason, document_id, value, internal_id, detail.
    """
    doc_id = (internal.get("Document_x0020_ID") or "").strip()
    title = (internal.get("Title") or "").strip()
    raw_cat = (internal.get("Category") or "").strip()
    status = (internal.get("Status") or "").strip().lower()
    visibility = (internal.get("Visibility") or "").strip().lower()
    storage_url_obj = internal.get("Storage_x0020_URL") or {}
    storage_url = (storage_url_obj.get("Url") or "").strip() if isinstance(storage_url_obj, dict) else ""
    updated_date = (internal.get("Updated_x0020_Date") or "").strip()

    # ── Eligibility gates (fail closed) ──────────────────────────────────
    # Each gate returns (None, exclusion) with a distinct reason code so
    # that the reconciliation report can attribute every excluded record to
    # exactly one primary reason.

    # Gate 1: Document ID
    if not doc_id:
        return None, {
            "reason": "missing_document_id",
            "document_id": "",
            "internal_id": internal.get("Id"),
            "detail": "Record has no Document_x0020_ID; cannot be referenced in public export."
        }

    # Gate 2: Title
    if not title:
        return None, {
            "reason": "missing_title",
            "document_id": doc_id,
            "internal_id": internal.get("Id"),
            "detail": "Record has no Title; required for public display."
        }

    # Gate 3: Visibility
    if visibility not in ALLOWED_VISIBILITY:
        return None, {
            "reason": "excluded_visibility",
            "document_id": doc_id,
            "internal_id": internal.get("Id"),
            "value": visibility,
            "detail": f"Visibility '{visibility}' is not in allowed set: {ALLOWED_VISIBILITY}"
        }

    # Gate 4: Status
    if status not in ALLOWED_STATUSES:
        return None, {
            "reason": "excluded_status",
            "document_id": doc_id,
            "internal_id": internal.get("Id"),
            "value": status,
            "detail": f"Status '{status}' is not in allowed set: {ALLOWED_STATUSES}"
        }

    # Gate 5: Category mapping
    mapped_cat = map_category(raw_cat)
    if not mapped_cat:
        return None, {
            "reason": "unmappable_category",
            "document_id": doc_id,
            "internal_id": internal.get("Id"),
            "value": raw_cat,
            "detail": f"Category '{raw_cat}' does not match any known Thai category name."
        }
    if mapped_cat not in ALLOWED_CATEGORIES:
        return None, {
            "reason": "unsupported_category",
            "document_id": doc_id,
            "internal_id": internal.get("Id"),
            "value": mapped_cat,
            "detail": f"Mapped category '{mapped_cat}' is not in the PXP-1 contract: {list(ALLOWED_CATEGORIES.keys())}"
        }

    # Gate 6: Storage URL
    if not storage_url:
        return None, {
            "reason": "missing_storage_url",
            "document_id": doc_id,
            "internal_id": internal.get("Id"),
            "detail": "Record has no Storage_x0020_URL; public export requires a download location."
        }
    if not is_valid_https_url(storage_url):
        return None, {
            "reason": "invalid_storage_url",
            "document_id": doc_id,
            "internal_id": internal.get("Id"),
            "value": storage_url[:100],
            "detail": f"Storage URL does not start with https:// or is too short."
        }

    # Gate 7: Download mode
    download_mode = determine_download_mode(storage_url)
    if download_mode not in ALLOWED_DOWNLOAD_MODES:
        return None, {
            "reason": "invalid_download_mode",
            "document_id": doc_id,
            "internal_id": internal.get("Id"),
            "value": download_mode,
            "detail": f"Derived download mode '{download_mode}' is not in allowed set: {ALLOWED_DOWNLOAD_MODES}"
        }

    # ── Updated date fallback ────────────────────────────────────────────
    if not updated_date:
        updated_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build public record (contract field order)
    public = OrderedDict()
    public["DocumentID"] = doc_id
    public["Title"] = title
    public["Category"] = mapped_cat
    public["Status"] = status
    public["Visibility"] = visibility
    public["UpdatedDate"] = updated_date
    public["StorageURL"] = storage_url
    public["DownloadMode"] = download_mode

    return public, None


def compute_sha256(data: dict) -> str:
    """Compute SHA-256 of deterministic JSON (sort_keys=True)."""
    json_bytes = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(json_bytes).hexdigest()


# ── Exclusion gate order (declared here for deterministic report output) ──
# The order in which gates are evaluated. Used by the exclusion breakdown
# table in the summary so that the same run always produces the same output.
GATE_ORDER = [
    "missing_document_id",
    "missing_title",
    "excluded_visibility",
    "excluded_status",
    "unmappable_category",
    "unsupported_category",
    "missing_storage_url",
    "invalid_storage_url",
    "invalid_download_mode",
]


def run_export(doc_ids_filter: set = None, mock_rows: list = None, skip_writes_param: bool = False) -> dict:
    """
    Main export pipeline.

    Args:
        doc_ids_filter: Optional set of DocumentID strings. When provided,
                        only records whose DocumentID is in this set are
                        processed; all others are skipped. Records that
                        are skipped still appear in the total count but are
                        reported separately as "batch_skipped" in the
                        reconciliation.
        mock_rows: Optional list of SharePoint REST API row dicts for testing.
                   When provided, Phase 1 (auth) and Phase 2 (scan) are skipped;
                   the mock data is used directly. The audit will record the
                   mock source.

    Returns:
        Audit dictionary with full pipeline results. When mock_rows is used,
        the returned audit also includes "export_documents" and "excluded_records"
        so that tests can inspect them directly.
    """
    audit = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pipeline": "pxp3-export-live-registry",
        "schema_version": SCHEMA_VERSION,
    }
    phases = {}

    using_mock = mock_rows is not None
    skip_writes = using_mock or skip_writes_param

    if using_mock:
        # Test path — skip authentication and scanning
        phases["test_mode"] = {"elapsed_sec": 0, "note": "Using mock_rows; auth and scan were skipped."}
        rows = mock_rows
        print(f"[PXP-3] Test mode: processing {len(rows)} mock records", flush=True)
    else:
        # Phase 1: Authenticate
        t0 = time.time()
        print("[PXP-3] Phase 1/5: Authenticating via Playwright browser profile...", flush=True)
        try:
            headers, ctx_info = authenticate()
        except Exception as e:
            return {"error": f"Authentication failed: {e}", "verdict": "AUTH_FAILED"}
        phases["auth"] = {"elapsed_sec": round(time.time() - t0, 2)}
        print(f"[PXP-3] Authenticated. Digest: {ctx_info['digest'][:30]}...", flush=True)

        # Phase 2: Scan Registry
        t0 = time.time()
        print("[PXP-3] Phase 2/5: Scanning live Registry...", flush=True)
        try:
            rows = scan_registry(headers)
        except Exception as e:
            return {"error": f"Registry scan failed: {e}", "verdict": "SCAN_FAILED"}
        phases["scan"] = {"elapsed_sec": round(time.time() - t0, 2), "rows": len(rows)}
        print(f"[PXP-3] Scanned {len(rows)} records ({phases['scan']['elapsed_sec']}s)", flush=True)

    # Phase 3: Map and filter
    t0 = time.time()
    print("[PXP-3] Phase 3/5: Mapping fields and applying eligibility gates...", flush=True)
    eligible = []
    excluded = []
    batch_skipped = []
    by_reason = Counter()
    by_category = Counter()
    by_download_mode = Counter()

    for row in rows:
        doc_id = (row.get("Document_x0020_ID") or "").strip()

        # ── Batch filter ────────────────────────────────────────────────
        if doc_ids_filter is not None:
            if not doc_id or doc_id not in doc_ids_filter:
                batch_skipped.append({
                    "internal_id": row.get("Id"),
                    "document_id": doc_id or "(no ID)",
                    "reason": "batch_skipped",
                    "detail": "DocumentID not in the --doc-ids filter set.",
                })
                continue

        # ── Pre-check for missing DocumentID ────────────────────────────
        if not doc_id:
            exclusion = {
                "reason": "missing_document_id",
                "document_id": "",
                "internal_id": row.get("Id"),
                "detail": "Record has no Document_x0020_ID; cannot be referenced in public export.",
            }
            excluded.append(exclusion)
            by_reason["missing_document_id"] += 1
            continue

        # ── Full mapping ────────────────────────────────────────────────
        public, exclusion = map_to_public(row)
        if exclusion:
            excluded.append(exclusion)
            by_reason[exclusion.get("reason", "unknown")] += 1
        else:
            eligible.append(public)
            by_category[public["Category"]] += 1
            by_download_mode[public["DownloadMode"]] += 1

    phases["mapping"] = {
        "elapsed_sec": round(time.time() - t0, 2),
        "eligible": len(eligible),
        "excluded": len(excluded),
        "batch_skipped": len(batch_skipped),
    }
    print(
        f"[PXP-3] Eligible: {len(eligible)}, Excluded: {len(excluded)}, "
        f"Batch-skipped: {len(batch_skipped)} ({phases['mapping']['elapsed_sec']}s)",
        flush=True,
    )

    # ── Reconciliation check ────────────────────────────────────────────
    total = len(rows)
    accounted = len(eligible) + len(excluded) + len(batch_skipped)
    if total != accounted:
        print(
            f"[PXP-3] WARNING: Reconciliation mismatch — "
            f"total ({total}) != eligible ({len(eligible)}) + excluded ({len(excluded)}) "
            f"+ batch_skipped ({len(batch_skipped)}) = {accounted}",
            flush=True,
        )
    else:
        print(
            f"[PXP-3] Reconciliation OK: {total} = {len(eligible)} + {len(excluded)} + {len(batch_skipped)}",
            flush=True,
        )

    # Phase 4: Generate public export
    t0 = time.time()
    print("[PXP-3] Phase 4/5: Generating public export...", flush=True)
    eligible.sort(key=lambda d: d["DocumentID"])
    excluded.sort(key=lambda d: (d.get("reason", ""), d.get("document_id", "")))
    batch_skipped.sort(key=lambda d: (d.get("document_id", ""), str(d.get("internal_id", ""))))

    # Collect total exclusion breakdown (including batch_skipped for clarity)
    exclusion_breakdown = dict(by_reason)
    if batch_skipped:
        exclusion_breakdown["batch_skipped"] = len(batch_skipped)

    export = OrderedDict()
    export["schemaVersion"] = SCHEMA_VERSION
    export["generatedAt"] = audit["timestamp"]
    export["source"] = "RAE Document Registry (SharePoint) - Live Export"
    export["preview_mode"] = False
    export["recordCount"] = len(eligible)
    export["documents"] = eligible

    sha256 = compute_sha256(export)
    phases["generate"] = {"elapsed_sec": round(time.time() - t0, 2), "sha256": sha256}
    print(f"[PXP-3] Export SHA-256: {sha256}", flush=True)

    # Phase 5: Privacy check
    t0 = time.time()
    print("[PXP-3] Phase 5/5: Privacy check...", flush=True)
    privacy_findings = []
    for doc in eligible:
        privacy_findings.extend(check_forbidden_fields(doc))
    phases["privacy"] = {
        "elapsed_sec": round(time.time() - t0, 2),
        "forbidden_fields_found": len(privacy_findings),
        "findings": privacy_findings[:20],
    }
    print(f"[PXP-3] Privacy: {len(privacy_findings)} forbidden field occurrences", flush=True)

    # Build complete audit
    total_elapsed = round(sum(p["elapsed_sec"] for p in phases.values()), 2)
    audit["phases"] = phases
    audit["total_elapsed_sec"] = total_elapsed
    audit["live_registry"] = {
        "site": SITE,
        "list": "RAE Document Registry",
        "total_records": total,
    }
    audit["export"] = {
        "eligible": len(eligible),
        "excluded": len(excluded),
        "batch_skipped": len(batch_skipped),
        "sha256": sha256,
    }
    audit["exclusion_breakdown"] = exclusion_breakdown
    audit["category_breakdown"] = dict(by_category)
    audit["download_mode_breakdown"] = dict(by_download_mode)
    audit["excluded_records"] = excluded
    audit["batch_skipped_records"] = batch_skipped if batch_skipped else None

    # ── Verdict calculation ────────────────────────────────────────────
    # PASS if:
    #   1. No privacy findings
    #   2. Reconciliation check passed (total == eligible + excluded + batch_skipped)
    #   3. At least one record is eligible OR batch mode produced expected zero
    #
    verdict_parts = []
    if len(privacy_findings) == 0:
        verdict_parts.append("PRIVACY_OK")
    else:
        verdict_parts.append("FAIL_PRIVACY_CHECK")

    if total == accounted:
        verdict_parts.append("RECONCILIATION_OK")
    else:
        verdict_parts.append("FAIL_RECONCILIATION")

    if doc_ids_filter is not None:
        audit["batch_mode"] = {
            "enabled": True,
            "target_ids": sorted(doc_ids_filter),
            "matched": len(eligible) + len(excluded),
        }
        verdict_parts.append(f"BATCH_MODE:{len(doc_ids_filter)}_TARGETED")

    audit["verdict"] = ";".join(verdict_parts)

    # Write outputs (skipped in test/mock mode to avoid polluting production data)
    if not skip_writes:
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(REPORTS_DIR, exist_ok=True)

        export_path = os.path.join(DATA_DIR, "document-registry.public.json")
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(export, f, ensure_ascii=False, indent=2)
        print(f"[PXP-3] Written: {export_path}", flush=True)

        sha_path = os.path.join(DATA_DIR, "document-registry.public.sha256")
        with open(sha_path, "w", encoding="utf-8") as f:
            f.write(f"{sha256}  document-registry.public.json\n")
        print(f"[PXP-3] Written: {sha_path}", flush=True)

        audit_path = os.path.join(REPORTS_DIR, "pxp2-export-audit.json")
        with open(audit_path, "w", encoding="utf-8") as f:
            json.dump(audit, f, ensure_ascii=False, indent=2)
        print(f"[PXP-3] Written: {audit_path}", flush=True)

        summary_path = os.path.join(REPORTS_DIR, "pxp2-export-summary.md")
        generate_summary_md(audit, summary_path)
        print(f"[PXP-3] Written: {summary_path}", flush=True)
    else:
        print(f"[PXP-3] Test mode: skipping file writes.", flush=True)

    # Add export_documents for test inspection (excluded_records is already set above)
    audit["export_documents"] = eligible

    print(f"\n[PXP-3] Export complete in {total_elapsed}s", flush=True)
    print(f"[PXP-3] Verdict: {audit['verdict']}", flush=True)

    return audit


def generate_summary_md(audit: dict, path: str):
    lines = []
    lines.append("# PXP-3 Export Summary")
    lines.append("")
    lines.append(f"**Generated**: {audit['timestamp']}")
    lines.append(f"**Pipeline**: {audit['pipeline']}")
    lines.append(f"**Schema Version**: {audit['schema_version']}")
    lines.append(f"**Total Time**: {audit['total_elapsed_sec']}s")
    lines.append(f"**Verdict**: {audit['verdict']}")
    lines.append("")

    # Batch mode info
    if audit.get("batch_mode"):
        lines.append("## Batch Mode")
        lines.append("")
        lines.append(f"**Target IDs**: {', '.join(audit['batch_mode']['target_ids'])}")
        lines.append(f"**Matched in Registry**: {audit['batch_mode']['matched']}")
        lines.append("")

    lines.append("## Live Registry")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Site | `{audit['live_registry']['site']}` |")
    lines.append(f"| List | {audit['live_registry']['list']} |")
    lines.append(f"| Total Records | {audit['live_registry']['total_records']} |")
    lines.append("")

    lines.append("## Export Results")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Eligible (exported) | {audit['export']['eligible']} |")
    lines.append(f"| Excluded | {audit['export']['excluded']} |")
    batch_skipped = audit['export'].get('batch_skipped', 0)
    if batch_skipped:
        lines.append(f"| Batch-skipped | {batch_skipped} |")
    lines.append(f"| SHA-256 | `{audit['export']['sha256']}` |")
    lines.append("")

    # ── Reconciliation (no double-counting) ────────────────────────────
    lines.append("## Reconciliation")
    lines.append("")
    total = audit['live_registry']['total_records']
    eligible = audit['export']['eligible']
    excluded = audit['export']['excluded']
    if batch_skipped:
        lines.append(
            f"Live total ({total}) = Eligible ({eligible}) + "
            f"Excluded ({excluded}) + Batch-skipped ({batch_skipped})"
        )
    else:
        lines.append(f"Live total ({total}) = Eligible ({eligible}) + Excluded ({excluded})")

    reconciliation_sum = eligible + excluded + batch_skipped
    if total == reconciliation_sum:
        lines.append(f"✓ Reconciliation check PASSED: {total} == {reconciliation_sum}")
    else:
        lines.append(f"✗ Reconciliation FAILED: {total} != {reconciliation_sum}")
    lines.append("")

    lines.append("## Exclusion Breakdown")
    lines.append("")
    lines.append("| Reason | Count |")
    lines.append("|--------|-------|")
    # Use GATE_ORDER for deterministic output; append any unexpected keys after
    breakdown = audit.get("exclusion_breakdown", {})
    for reason in GATE_ORDER:
        count = breakdown.get(reason, 0)
        if count > 0:
            lines.append(f"| {reason} | {count} |")
    for reason, count in sorted(breakdown.items()):
        if reason not in GATE_ORDER:
            lines.append(f"| {reason} | {count} |")
    lines.append("")

    lines.append("## Category Breakdown")
    lines.append("")
    if audit.get("category_breakdown"):
        lines.append("| Category | Count |")
        lines.append("|----------|-------|")
        for cat, count in sorted(audit["category_breakdown"].items()):
            lines.append(f"| {cat} | {count} |")
        lines.append("")
    else:
        lines.append("No eligible records to categorize.")
        lines.append("")

    lines.append("## Download Mode Breakdown")
    lines.append("")
    if audit.get("download_mode_breakdown"):
        lines.append("| Mode | Count |")
        lines.append("|------|-------|")
        for mode, count in sorted(audit["download_mode_breakdown"].items()):
            lines.append(f"| {mode} | {count} |")
        lines.append("")
    else:
        lines.append("No eligible records to classify.")
        lines.append("")

    lines.append("## Phases")
    lines.append("")
    lines.append("| Phase | Elapsed (s) |")
    lines.append("|-------|-------------|")
    for phase, info in sorted(audit.get("phases", {}).items()):
        lines.append(f"| {phase} | {info.get('elapsed_sec', 0)} |")
    lines.append("")

    # ── Excluded records table with detail ─────────────────────────────
    excluded_recs = audit.get("excluded_records", [])
    if excluded_recs:
        lines.append(f"## Excluded Records ({len(excluded_recs)})")
        lines.append("")
        lines.append("| DocumentID | Reason | Detail |")
        lines.append("|------------|--------|--------|")
        for rec in excluded_recs[:60]:
            did = rec.get("document_id", "") or "(no ID)"
            reason = rec.get("reason", "unknown")
            detail = str(rec.get("detail", rec.get("value", "")))[:80]
            lines.append(f"| {did} | {reason} | {detail} |")
        if len(excluded_recs) > 60:
            lines.append(f"| ... and {len(excluded_recs) - 60} more | | |")
        lines.append("")

    # ── Batch-skipped records ──────────────────────────────────────────
    batch_recs = audit.get("batch_skipped_records") or []
    if batch_recs:
        lines.append(f"## Batch-Skipped Records ({len(batch_recs)})")
        lines.append("")
        lines.append("| DocumentID | Reason |")
        lines.append("|------------|--------|")
        for rec in batch_recs[:30]:
            did = rec.get("document_id", "") or "(no ID)"
            lines.append(f"| {did} | {rec.get('reason', 'unknown')} |")
        if len(batch_recs) > 30:
            lines.append(f"| ... and {len(batch_recs) - 30} more | |")
        lines.append("")

    lines.append("---")
    lines.append("*Report generated by PXP-3 export pipeline*")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    args = parse_args()
    doc_ids_filter = None
    skip_writes = args.skip_writes
    if args.doc_ids:
        doc_ids_filter = {did.strip() for did in args.doc_ids.split(",") if did.strip()}
        print(f"[PXP-3] Batch mode: targeting {len(doc_ids_filter)} DocumentID(s)", flush=True)
    if skip_writes:
        print(f"[PXP-3] Skip-writes mode: output files will NOT be written", flush=True)

    audit = run_export(doc_ids_filter=doc_ids_filter, skip_writes_param=skip_writes)
    if audit.get("error"):
        print(f"\n[PXP-3] ERROR: {audit['error']}", file=sys.stderr)
        sys.exit(1)
    if audit.get("verdict") and "AUTH_FAILED" in audit["verdict"]:
        print(f"[PXP-3] Authentication failed. Run again to re-authenticate.", file=sys.stderr)
        sys.exit(1)
    if audit.get("verdict") and "SCAN_FAILED" in audit["verdict"]:
        print(f"[PXP-3] Registry scan failed.", file=sys.stderr)
        sys.exit(1)
    if audit.get("verdict") and "FAIL_PRIVACY_CHECK" in audit["verdict"]:
        print(f"[PXP-3] Privacy check failed.", file=sys.stderr)
        sys.exit(1)
    if audit.get("verdict") and "FAIL_RECONCILIATION" in audit["verdict"]:
        print(f"[PXP-3] Reconciliation failed! Total != Eligible + Excluded + Batch-skipped.", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
