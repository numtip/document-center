#!/usr/bin/env python3
"""
PXP-2 Validate Public Export — validates data/document-registry.public.json
against the PXP-1 contract schema.

This validator runs WITHOUT accessing M365. It validates the static export file.
Can be used in CI/CD.

Usage:
    python scripts/registry/validate-public-export.py

Exit code:
    0: All validations pass
    1: One or more validations fail
"""
import json
import os
import sys
from collections import Counter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXPORT_PATH = os.path.join(REPO_ROOT, "data", "document-registry.public.json")

SCHEMA_VERSION = "1.0.0"

ALLOWED_STATUSES = {"approved", "published", "current"}
ALLOWED_VISIBILITY = {"public"}
ALLOWED_DOWNLOAD_MODES = {
    "AUTHENTICATED_SHAREPOINT",
    "PUBLIC_SHAREPOINT_LINK",
    "PUBLIC_DISTRIBUTION_URL",
}
ALLOWED_CATEGORIES = {
    "Administration", "FinanceProcurement", "PlanningPolicy",
    "AcademicServices", "Research", "SOPManuals",
}

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

FORBIDDEN_FIELDS = [
    "OwnerId", "LegacySourceURL", "Source_x0020_System",
    "SourceSystem", "onedrive_path", "note", "owner",
    "file_type", "fileType", "tags", "version",
]

errors = []
warnings = []


def fail(message: str):
    errors.append(message)
    print(f"  FAIL: {message}")


def warn(message: str):
    warnings.append(message)
    print(f"  WARN: {message}")


def validate():
    print("PXP-2 Public Export Validator")
    print("=" * 50)

    # 1. File exists
    if not os.path.exists(EXPORT_PATH):
        fail(f"Export file not found: {EXPORT_PATH}")
        return False
    print(f"  File: {EXPORT_PATH}")

    # 2. Parse JSON
    try:
        with open(EXPORT_PATH, "r", encoding="utf-8") as f:
            export = json.load(f)
    except json.JSONDecodeError as e:
        fail(f"JSON parse error: {e}")
        return False

    # 3. Schema version
    sv = export.get("schemaVersion", "")
    if sv != SCHEMA_VERSION:
        fail(f"Schema version mismatch: expected {SCHEMA_VERSION}, got {sv}")
    else:
        print(f"  Schema version: {sv}")

    # 4. preview_mode must be false
    if export.get("preview_mode", True):
        fail("preview_mode must be false in public export")

    # 5. Record count
    docs = export.get("documents", [])
    record_count = export.get("recordCount", -1)
    if record_count != len(docs):
        fail(f"recordCount ({record_count}) != documents length ({len(docs)})")

    print(f"  Record count: {record_count}")
    print(f"  Documents: {len(docs)}")

    # 6. Validate each document
    seen_ids = set()
    categories = Counter()
    statuses = Counter()
    visibilities = Counter()
    download_modes = Counter()

    for i, doc in enumerate(docs):
        doc_id = doc.get("DocumentID", "(missing)")
        doc_num = i + 1

        # Required fields
        for field in CONTRACT_FIELDS:
            val = doc.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                fail(f"[{doc_id}] Missing required field: {field}")

        # Status
        status = doc.get("Status", "").lower()
        if status not in ALLOWED_STATUSES:
            fail(f"[{doc_id}] Invalid status: {doc.get('Status', '')}")
        statuses[status] += 1

        # Visibility
        visibility = doc.get("Visibility", "").lower()
        if visibility not in ALLOWED_VISIBILITY:
            fail(f"[{doc_id}] Invalid visibility: {doc.get('Visibility', '')}")
        visibilities[visibility] += 1

        # Category
        cat = doc.get("Category", "")
        if cat not in ALLOWED_CATEGORIES:
            fail(f"[{doc_id}] Invalid category: {cat}")
        categories[cat] += 1

        # DownloadMode
        dm = doc.get("DownloadMode", "")
        if dm not in ALLOWED_DOWNLOAD_MODES:
            fail(f"[{doc_id}] Invalid download mode: {dm}")
        download_modes[dm] += 1

        # StorageURL
        url = doc.get("StorageURL", "")
        if not url.startswith("https://"):
            fail(f"[{doc_id}] Invalid StorageURL (must be HTTPS): {url[:60]}")

        # UpdatedDate
        ud = doc.get("UpdatedDate", "")
        if not ud or len(ud) < 10:
            fail(f"[{doc_id}] Invalid UpdatedDate: {ud}")

        # Duplicate ID
        if doc_id in seen_ids:
            fail(f"[{doc_id}] Duplicate DocumentID")
        seen_ids.add(doc_id)

        # Forbidden fields
        for ff in FORBIDDEN_FIELDS:
            if ff in doc:
                fail(f"[{doc_id}] Forbidden field present: {ff}")

    # 7. Deterministic ordering
    doc_ids = [d.get("DocumentID", "") for d in docs]
    if doc_ids != sorted(doc_ids):
        warn("Documents are not sorted by DocumentID")

    # 8. Summary
    print()
    print("Summary:")
    print(f"  Total: {len(docs)}")
    print(f"  Unique IDs: {len(seen_ids)}")
    print(f"  Categories: {dict(categories)}")
    print(f"  Statuses: {dict(statuses)}")
    print(f"  Visibilities: {dict(visibilities)}")
    print(f"  Download Modes: {dict(download_modes)}")

    print()
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"PASSED: {len(docs)} records, 0 errors, {len(warnings)} warning(s)")
        return True


if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
