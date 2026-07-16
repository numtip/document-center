#!/usr/bin/env python3
"""
PXP-2 Export Live Registry — exports RAE Document Registry from SharePoint
to the PXP-1 public contract format.

Uses Playwright for authentication (reusable browser profile) + Python requests
for SharePoint REST API queries.

Usage:
    python scripts/registry/export-live-registry.py

Output:
    data/document-registry.public.json
    data/document-registry.public.sha256
    reports/pxp2-export-audit.json
    reports/pxp2-export-summary.md
"""
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

# PXP-1 contract categories
ALLOWED_CATEGORIES = OrderedDict([
    ("Administration", "Administration"),
    ("FinanceProcurement", "FinanceProcurement"),
    ("PlanningPolicy", "PlanningPolicy"),
    ("AcademicServices", "AcademicServices"),
    ("Research", "Research"),
    ("SOPManuals", "SOPManuals"),
])

# Live Registry Thai display name -> PXP-1 contract category mapping
# The Registry stores Thai category names, not internal IDs
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
    """
    doc_id = (internal.get("Document_x0020_ID") or "").strip()
    title = (internal.get("Title") or "").strip()
    raw_cat = (internal.get("Category") or "").strip()
    status = (internal.get("Status") or "").strip().lower()
    visibility = (internal.get("Visibility") or "").strip().lower()
    storage_url_obj = internal.get("Storage_x0020_URL") or {}
    storage_url = (storage_url_obj.get("Url") or "").strip() if isinstance(storage_url_obj, dict) else ""
    updated_date = (internal.get("Updated_x0020_Date") or "").strip()

    # Eligibility gates (fail closed)
    if not doc_id:
        return None, {"reason": "missing_document_id", "internal_id": internal.get("Id")}
    if not title:
        return None, {"reason": "missing_title", "document_id": doc_id}

    # Visibility gate
    if visibility not in ALLOWED_VISIBILITY:
        return None, {"reason": "excluded_visibility", "document_id": doc_id, "value": visibility}

    # Status gate
    if status not in ALLOWED_STATUSES:
        return None, {"reason": "excluded_status", "document_id": doc_id, "value": status}

    # Category mapping
    mapped_cat = map_category(raw_cat)
    if not mapped_cat:
        return None, {"reason": "unmappable_category", "document_id": doc_id, "value": raw_cat}
    if mapped_cat not in ALLOWED_CATEGORIES:
        return None, {"reason": "unsupported_category", "document_id": doc_id, "value": mapped_cat}

    # Storage URL
    if not storage_url:
        return None, {"reason": "missing_storage_url", "document_id": doc_id}
    if not is_valid_https_url(storage_url):
        return None, {"reason": "invalid_storage_url", "document_id": doc_id, "value": storage_url[:100]}

    # Download mode
    download_mode = determine_download_mode(storage_url)
    if download_mode not in ALLOWED_DOWNLOAD_MODES:
        return None, {"reason": "invalid_download_mode", "document_id": doc_id, "value": download_mode}

    # Updated date
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
    """Compute SHA-256 of deterministic JSON."""
    json_bytes = json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(json_bytes).hexdigest()


def run_export() -> dict:
    """Main export pipeline."""
    audit = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pipeline": "pxp2-export-live-registry",
        "schema_version": SCHEMA_VERSION,
    }
    phases = {}

    # Phase 1: Authenticate
    t0 = time.time()
    print("[PXP-2] Phase 1/5: Authenticating via Playwright browser profile...", flush=True)
    try:
        headers, ctx_info = authenticate()
    except Exception as e:
        return {"error": f"Authentication failed: {e}", "verdict": "AUTH_FAILED"}
    phases["auth"] = {"elapsed_sec": round(time.time() - t0, 2)}
    print(f"[PXP-2] Authenticated. Digest: {ctx_info['digest'][:30]}...", flush=True)

    # Phase 2: Scan Registry
    t0 = time.time()
    print("[PXP-2] Phase 2/5: Scanning live Registry...", flush=True)
    try:
        rows = scan_registry(headers)
    except Exception as e:
        return {"error": f"Registry scan failed: {e}", "verdict": "SCAN_FAILED"}
    phases["scan"] = {"elapsed_sec": round(time.time() - t0, 2), "rows": len(rows)}
    print(f"[PXP-2] Scanned {len(rows)} records ({phases['scan']['elapsed_sec']}s)", flush=True)

    # Phase 3: Map and filter
    t0 = time.time()
    print("[PXP-2] Phase 3/5: Mapping fields and applying eligibility gates...", flush=True)
    eligible = []
    excluded = []
    by_reason = Counter()
    by_category = Counter()
    by_download_mode = Counter()

    for row in rows:
        doc_id = (row.get("Document_x0020_ID") or "").strip()
        if not doc_id:
            excluded.append({"internal_id": row.get("Id"), "document_id": "", "reason": "missing_document_id"})
            by_reason["missing_document_id"] += 1
            continue
        public, exclusion = map_to_public(row)
        if exclusion:
            excluded.append({
                "internal_id": row.get("Id"),
                "document_id": doc_id,
                "reason": exclusion.get("reason", "unknown"),
                "value": exclusion.get("value", ""),
            })
            by_reason[exclusion.get("reason", "unknown")] += 1
        else:
            eligible.append(public)
            by_category[public["Category"]] += 1
            by_download_mode[public["DownloadMode"]] += 1

    phases["mapping"] = {"elapsed_sec": round(time.time() - t0, 2), "eligible": len(eligible), "excluded": len(excluded)}
    print(f"[PXP-2] Eligible: {len(eligible)}, Excluded: {len(excluded)} ({phases['mapping']['elapsed_sec']}s)", flush=True)

    # Phase 4: Generate public export
    t0 = time.time()
    print("[PXP-2] Phase 4/5: Generating public export...", flush=True)
    eligible.sort(key=lambda d: d["DocumentID"])
    excluded.sort(key=lambda d: (d.get("reason", ""), d.get("document_id", "")))

    export = OrderedDict()
    export["schemaVersion"] = SCHEMA_VERSION
    export["generatedAt"] = audit["timestamp"]
    export["source"] = "RAE Document Registry (SharePoint) - Live Export"
    export["preview_mode"] = False
    export["recordCount"] = len(eligible)
    export["documents"] = eligible

    sha256 = compute_sha256(export)
    phases["generate"] = {"elapsed_sec": round(time.time() - t0, 2), "sha256": sha256}
    print(f"[PXP-2] Export SHA-256: {sha256}", flush=True)

    # Phase 5: Privacy check
    t0 = time.time()
    print("[PXP-2] Phase 5/5: Privacy check...", flush=True)
    privacy_findings = []
    for doc in eligible:
        privacy_findings.extend(check_forbidden_fields(doc))
    phases["privacy"] = {
        "elapsed_sec": round(time.time() - t0, 2),
        "forbidden_fields_found": len(privacy_findings),
        "findings": privacy_findings[:20],
    }
    print(f"[PXP-2] Privacy: {len(privacy_findings)} forbidden field occurrences", flush=True)

    # Build complete audit
    total_elapsed = round(sum(p["elapsed_sec"] for p in phases.values()), 2)
    audit["phases"] = phases
    audit["total_elapsed_sec"] = total_elapsed
    audit["live_registry"] = {
        "site": SITE,
        "list": "RAE Document Registry",
        "total_records": len(rows),
    }
    audit["export"] = {
        "eligible": len(eligible),
        "excluded": len(excluded),
        "sha256": sha256,
    }
    audit["exclusion_breakdown"] = dict(by_reason)
    audit["category_breakdown"] = dict(by_category)
    audit["download_mode_breakdown"] = dict(by_download_mode)
    audit["excluded_records"] = excluded
    audit["verdict"] = "PASS" if len(privacy_findings) == 0 else "FAIL_PRIVACY_CHECK"

    # Write outputs
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    export_path = os.path.join(DATA_DIR, "document-registry.public.json")
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(export, f, ensure_ascii=False, indent=2)
    print(f"[PXP-2] Written: {export_path}", flush=True)

    sha_path = os.path.join(DATA_DIR, "document-registry.public.sha256")
    with open(sha_path, "w", encoding="utf-8") as f:
        f.write(f"{sha256}  document-registry.public.json\n")
    print(f"[PXP-2] Written: {sha_path}", flush=True)

    audit_path = os.path.join(REPORTS_DIR, "pxp2-export-audit.json")
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
    print(f"[PXP-2] Written: {audit_path}", flush=True)

    summary_path = os.path.join(REPORTS_DIR, "pxp2-export-summary.md")
    generate_summary_md(audit, summary_path)
    print(f"[PXP-2] Written: {summary_path}", flush=True)

    print(f"\n[PXP-2] Export complete in {total_elapsed}s", flush=True)
    print(f"[PXP-2] Verdict: {audit['verdict']}", flush=True)

    return audit


def generate_summary_md(audit: dict, path: str):
    lines = []
    lines.append("# PXP-2 Export Summary")
    lines.append("")
    lines.append(f"**Generated**: {audit['timestamp']}")
    lines.append(f"**Pipeline**: {audit['pipeline']}")
    lines.append(f"**Schema Version**: {audit['schema_version']}")
    lines.append(f"**Total Time**: {audit['total_elapsed_sec']}s")
    lines.append(f"**Verdict**: {audit['verdict']}")
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
    lines.append(f"| SHA-256 | `{audit['export']['sha256']}` |")
    lines.append("")
    lines.append("## Reconciliation")
    lines.append("")
    total = audit['live_registry']['total_records']
    eligible = audit['export']['eligible']
    excluded = audit['export']['excluded']
    lines.append(f"Live total ({total}) = Eligible ({eligible}) + Excluded ({excluded})")
    lines.append("")
    lines.append("## Exclusion Breakdown")
    lines.append("")
    lines.append("| Reason | Count |")
    lines.append("|--------|-------|")
    for reason, count in sorted(audit.get("exclusion_breakdown", {}).items()):
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

    excluded_recs = audit.get("excluded_records", [])
    if excluded_recs:
        lines.append(f"## Excluded Records ({len(excluded_recs)})")
        lines.append("")
        lines.append("| DocumentID | Reason | Value |")
        lines.append("|------------|--------|-------|")
        for rec in excluded_recs[:60]:
            did = rec.get("document_id", "") or "(no ID)"
            reason = rec.get("reason", "unknown")
            val = str(rec.get("value", ""))[:60]
            lines.append(f"| {did} | {reason} | {val} |")
        if len(excluded_recs) > 60:
            lines.append(f"| ... and {len(excluded_recs) - 60} more | | |")
        lines.append("")

    lines.append("---")
    lines.append("*Report generated by PXP-2 export pipeline*")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    audit = run_export()
    if audit.get("error"):
        print(f"\n[PXP-2] ERROR: {audit['error']}", file=sys.stderr)
        sys.exit(1)
    if audit.get("verdict") == "AUTH_FAILED":
        print(f"[PXP-2] Authentication failed. Run again to re-authenticate.", file=sys.stderr)
        sys.exit(1)
    if audit.get("verdict") == "SCAN_FAILED":
        print(f"[PXP-2] Registry scan failed.", file=sys.stderr)
        sys.exit(1)
    if audit.get("verdict") == "FAIL_PRIVACY_CHECK":
        print(f"[PXP-2] Privacy check failed.", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
