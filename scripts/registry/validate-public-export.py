#!/usr/bin/env python3
"""
PXP-3 Validate Public Export — validates a public registry export file
against the PXP-1 contract schema.

This validator runs WITHOUT accessing M365. It validates a static export
file. Can be used in CI/CD.

Enhancements over PXP-2:
  • Accept --file argument to validate any export file (not just the default)
  • Per-document error details in summary
  • Strict deterministic ordering check (reports which IDs are out of order)
  • Support for batch-mode exports with batch_skipped metadata

Usage:
    python scripts/registry/validate-public-export.py
    python scripts/registry/validate-public-export.py --file data/document-registry.public.json

Exit code:
    0: All validations pass
    1: One or more validations fail
"""
import argparse
import json
import os
import sys
from collections import Counter

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_EXPORT_PATH = os.path.join(REPO_ROOT, "data", "document-registry.public.json")

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


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for custom file path."""
    parser = argparse.ArgumentParser(
        description="PXP-3 Validate Public Export — static schema validation"
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        default=None,
        help="Path to the export JSON file to validate (default: data/document-registry.public.json)"
    )
    return parser.parse_args()


def fail(message: str):
    errors.append(message)
    print(f"  FAIL: {message}")


def warn(message: str):
    warnings.append(message)
    print(f"  WARN: {message}")


def validate(export_path: str = None):
    """Run all validations against the given export file."""
    # Reset module-level state for idempotent calls
    errors.clear()
    warnings.clear()

    if export_path is None:
        export_path = DEFAULT_EXPORT_PATH

    print("PXP-3 Public Export Validator")
    print("=" * 50)

    # 1. File exists
    if not os.path.exists(export_path):
        fail(f"Export file not found: {export_path}")
        return False
    print(f"  File: {export_path}")

    # 2. Parse JSON
    try:
        with open(export_path, "r", encoding="utf-8") as f:
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
            fail(f"[{doc_id}] Duplicate DocumentID at position {doc_num}")
        seen_ids.add(doc_id)

        # Forbidden fields
        for ff in FORBIDDEN_FIELDS:
            if ff in doc:
                fail(f"[{doc_id}] Forbidden field present: {ff}")

    # 7. Deterministic ordering (strict check)
    doc_ids = [d.get("DocumentID", "") for d in docs]
    if doc_ids != sorted(doc_ids):
        warn("Documents are not sorted by DocumentID")
        # Report first out-of-order pair for debugging
        for j in range(len(doc_ids) - 1):
            if doc_ids[j] > doc_ids[j + 1]:
                warn(
                    f"  First ordering violation: '{doc_ids[j]}' > '{doc_ids[j + 1]}' "
                    f"at positions {j+1}/{j+2}"
                )
                break

    # 8. Summary
    print()
    print("Summary:")
    print(f"  Total: {len(docs)}")
    print(f"  Unique IDs: {len(seen_ids)}")
    print(f"  Categories: {dict(categories)}")
    print(f"  Statuses: {dict(statuses)}")
    print(f"  Visibilities: {dict(visibilities)}")
    print(f"  Download Modes: {dict(download_modes)}")

    # 9. Report batch mode metadata if present
    if export.get("batch_mode"):
        print(f"  Batch mode: {export['batch_mode']}")

    print()
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        print()
        # Group errors by category for readability
        cat_errors = Counter()
        for e in errors:
            if "Invalid" in e:
                cat_errors["schema_violation"] += 1
            elif "Missing" in e:
                cat_errors["missing_field"] += 1
            elif "Duplicate" in e:
                cat_errors["duplicate_id"] += 1
            elif "Forbidden" in e:
                cat_errors["forbidden_field"] += 1
            else:
                cat_errors["other"] += 1
        print("  Error categories:")
        for cat_name, cat_count in sorted(cat_errors.items()):
            print(f"    - {cat_name}: {cat_count}")
        print()
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"PASSED: {len(docs)} records, 0 errors, {len(warnings)} warning(s)")
        return True


if __name__ == "__main__":
    args = parse_args()
    success = validate(export_path=args.file)
    sys.exit(0 if success else 1)
