#!/usr/bin/env python3
"""
PXP-3 Export Pipeline Tests — validates the registry exporter logic
independently of M365 (no authentication, no live data).

Tests the pure functions of export-live-registry.py and the structure
of validate-public-export.py by constructing mock internal records.

Uses importlib to load the hyphenated Python filenames.

Run:
    python scripts/registry/test-export-pipeline.py   # uses unittest
    pytest scripts/registry/test-export-pipeline.py -v  # if pytest is available
"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from collections import OrderedDict
from datetime import datetime, timezone

# ── Import modules with hyphenated filenames using importlib ───────────────

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY_DIR = os.path.join(REPO_ROOT, "scripts", "registry")


def _load_module(name, filename):
    """Load a Python module from a file path (handles hyphenated filenames)."""
    path = os.path.join(REGISTRY_DIR, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


exporter = _load_module("export_live_registry", "export-live-registry.py")
validator = _load_module("validate_public_export", "validate-public-export.py")

# Bring all names into this module's namespace for concise test code
# (importlib-loaded modules don't support from-import, so use getattr)
ALLOWED_CATEGORIES = getattr(exporter, "ALLOWED_CATEGORIES")
ALLOWED_DOWNLOAD_MODES = getattr(exporter, "ALLOWED_DOWNLOAD_MODES")
ALLOWED_STATUSES = getattr(exporter, "ALLOWED_STATUSES")
ALLOWED_VISIBILITY = getattr(exporter, "ALLOWED_VISIBILITY")
CATEGORY_DISPLAY_MAP = getattr(exporter, "CATEGORY_DISPLAY_MAP")
CONTRACT_FIELDS = getattr(exporter, "CONTRACT_FIELDS")
FORBIDDEN_PATTERNS = getattr(exporter, "FORBIDDEN_PATTERNS")
GATE_ORDER = getattr(exporter, "GATE_ORDER")
SCHEMA_VERSION = getattr(exporter, "SCHEMA_VERSION")
check_forbidden_fields = getattr(exporter, "check_forbidden_fields")
compute_sha256 = getattr(exporter, "compute_sha256")
determine_download_mode = getattr(exporter, "determine_download_mode")
is_valid_https_url = getattr(exporter, "is_valid_https_url")
map_category = getattr(exporter, "map_category")
map_to_public = getattr(exporter, "map_to_public")
run_export = getattr(exporter, "run_export")
validate = getattr(validator, "validate")


# ── Helpers ────────────────────────────────────────────────────────────────


def make_mock_internal(
    doc_id="RAE-00001",
    title="Test Document",
    category="งานบริหารและธุรการ",
    status="current",
    visibility="public",
    storage_url="https://maejo365.sharepoint.com/sites/test/doc.docx",
    updated_date="2026-07-16T08:00:00Z",
    internal_id=1,
):
    """Build a mock SharePoint REST API record (as returned by scan_registry)."""
    return {
        "Id": internal_id,
        "Title": title,
        "Document_x0020_ID": doc_id,
        "Category": category,
        "Status": status,
        "Visibility": visibility,
        "Storage_x0020_URL": {"Url": storage_url, "__deferred": {}},
        "Updated_x0020_Date": updated_date,
    }


def make_mock_public(
    doc_id="RAE-00001",
    title="Test Document",
    category="Administration",
    status="current",
    visibility="public",
    storage_url="https://maejo365.sharepoint.com/sites/test/doc.docx",
    updated_date="2026-07-16T08:00:00Z",
    download_mode="AUTHENTICATED_SHAREPOINT",
):
    """Build an expected public contract record (OrderedDict)."""
    pub = OrderedDict()
    pub["DocumentID"] = doc_id
    pub["Title"] = title
    pub["Category"] = category
    pub["Status"] = status
    pub["Visibility"] = visibility
    pub["UpdatedDate"] = updated_date
    pub["StorageURL"] = storage_url
    pub["DownloadMode"] = download_mode
    return pub


# ── Test Cases ─────────────────────────────────────────────────────────────


class TestCategoryMapping(unittest.TestCase):
    """Verify every Thai category correctly maps to the contract."""

    def test_all_thai_categories_mapped(self):
        """Every entry in CATEGORY_DISPLAY_MAP maps to a valid contract category."""
        for thai_name, contract_name in CATEGORY_DISPLAY_MAP.items():
            with self.subTest(thai=thai_name):
                self.assertIn(contract_name, ALLOWED_CATEGORIES,
                              f"'{thai_name}' → '{contract_name}' not in contract")

    def test_research_subcategories_map(self):
        """All research sub-types collapse to a single 'Research' category."""
        research_keywords = ["งานวิจัย", "research", "แบบฟอร์มแหล่งทุนภายนอก", "แบบฟอร์มศูนย์ความเป็นเลิศ"]
        for kw in research_keywords:
            result = map_category(kw)
            self.assertEqual(result, "Research", f"'{kw}' should map to Research")

    def test_administration_maps_correctly(self):
        self.assertEqual(map_category("งานบริหารและธุรการ"), "Administration")
        self.assertEqual(map_category("บริหารจัดการ"), "Administration")

    def test_finance_maps_correctly(self):
        self.assertEqual(map_category("งานคลังและพัสดุ"), "FinanceProcurement")

    def test_planning_maps_correctly(self):
        self.assertEqual(map_category("งานนโยบาย แผนและประกันคุณภาพ"), "PlanningPolicy")

    def test_academic_services_maps_correctly(self):
        self.assertEqual(map_category("งานบริการวิชาการ"), "AcademicServices")
        self.assertEqual(map_category("แบบฟอร์มงานบริการวิชาการ"), "AcademicServices")

    def test_sop_maps_correctly(self):
        self.assertEqual(map_category("คู่มือ"), "SOPManuals")

    def test_unknown_category_returns_none(self):
        self.assertIsNone(map_category("NonExistent Category"))
        self.assertIsNone(map_category(""))
        self.assertIsNone(map_category("   "))


class TestMapToPublicBasic(unittest.TestCase):
    """Test 1: A mock record transforms correctly: internal -> public mapping."""

    def test_full_valid_record_transforms_correctly(self):
        """A fully valid internal record maps to exactly the expected public record."""
        internal = make_mock_internal()
        public, exclusion = map_to_public(internal)

        self.assertIsNone(exclusion, "Valid record should not be excluded")
        self.assertIsNotNone(public, "Valid record should produce a public record")

        expected = make_mock_public()
        self.assertEqual(dict(public), dict(expected))

    def test_contract_field_order_is_preserved(self):
        """The public record fields appear in CONTRACT_FIELDS order."""
        internal = make_mock_internal()
        public, _ = map_to_public(internal)

        keys = list(public.keys())
        self.assertEqual(keys, CONTRACT_FIELDS,
                         f"Field order mismatch: {keys} != {CONTRACT_FIELDS}")

    def test_all_required_fields_present(self):
        """Every CONTRACT_FIELDS key is present on the output record."""
        internal = make_mock_internal()
        public, _ = map_to_public(internal)

        for field in CONTRACT_FIELDS:
            self.assertIn(field, public, f"Missing contract field: {field}")
            self.assertTrue(str(public[field]).strip(), f"Empty contract field: {field}")

    def test_download_mode_determined_correctly(self):
        """A maegjo365 SharePoint URL produces AUTHENTICATED_SHAREPOINT."""
        internal = make_mock_internal(
            storage_url="https://maejo365.sharepoint.com/sites/test/doc.docx"
        )
        public, _ = map_to_public(internal)
        self.assertEqual(public["DownloadMode"], "AUTHENTICATED_SHAREPOINT")

    def test_guest_url_produces_public_sharepoint_link(self):
        """A 'guest' URL produces PUBLIC_SHAREPOINT_LINK."""
        internal = make_mock_internal(
            storage_url="https://maejo365.sharepoint.com/:v:/g/guest/abc123"
        )
        public, _ = map_to_public(internal)
        self.assertEqual(public["DownloadMode"], "PUBLIC_SHAREPOINT_LINK")

    def test_anonymous_url_produces_public_sharepoint_link(self):
        """An 'anonymous' URL produces PUBLIC_SHAREPOINT_LINK."""
        internal = make_mock_internal(
            storage_url="https://maejo365.sharepoint.com/:v:/g/anonymous/abc123"
        )
        public, _ = map_to_public(internal)
        self.assertEqual(public["DownloadMode"], "PUBLIC_SHAREPOINT_LINK")


class TestExclusionGates(unittest.TestCase):
    """Test 2: Private record excluded. Test 3: Missing URL fails."""

    def test_private_visibility_excluded(self):
        """A record with visibility=internal should be excluded."""
        internal = make_mock_internal(visibility="internal")
        public, exclusion = map_to_public(internal)

        self.assertIsNone(public, "Private record should not produce public output")
        self.assertIsNotNone(exclusion, "Private record should return exclusion reason")
        self.assertEqual(exclusion["reason"], "excluded_visibility")
        self.assertEqual(exclusion["value"], "internal")

    def test_draft_status_excluded(self):
        """A record with status=draft should be excluded."""
        internal = make_mock_internal(status="draft")
        public, exclusion = map_to_public(internal)

        self.assertIsNone(public)
        self.assertIsNotNone(exclusion)
        self.assertEqual(exclusion["reason"], "excluded_status")
        self.assertEqual(exclusion["value"], "draft")

    def test_missing_document_id_excluded(self):
        """A record with empty Document_x0020_ID should be excluded."""
        internal = make_mock_internal(doc_id="")
        public, exclusion = map_to_public(internal)

        self.assertIsNone(public)
        self.assertIsNotNone(exclusion)
        self.assertEqual(exclusion["reason"], "missing_document_id")

    def test_missing_title_excluded(self):
        """A record with empty Title should be excluded."""
        internal = make_mock_internal(title="")
        public, exclusion = map_to_public(internal)

        self.assertIsNone(public)
        self.assertIsNotNone(exclusion)
        self.assertEqual(exclusion["reason"], "missing_title")

    def test_missing_storage_url_excluded(self):
        """A record with no Storage_x0020_URL should be excluded."""
        internal = make_mock_internal(storage_url="")
        public, exclusion = map_to_public(internal)

        self.assertIsNone(public)
        self.assertIsNotNone(exclusion)
        self.assertEqual(exclusion["reason"], "missing_storage_url")

    def test_invalid_storage_url_excluded(self):
        """A record with a non-HTTPS storage URL should be excluded."""
        internal = make_mock_internal(storage_url="http://example.com/doc.docx")
        public, exclusion = map_to_public(internal)

        self.assertIsNone(public)
        self.assertIsNotNone(exclusion)
        self.assertEqual(exclusion["reason"], "invalid_storage_url")

    def test_unmappable_category_excluded(self):
        """A record with an unknown category should be excluded."""
        internal = make_mock_internal(category="UnknownCategoryXYZ")
        public, exclusion = map_to_public(internal)

        self.assertIsNone(public)
        self.assertIsNotNone(exclusion)
        self.assertEqual(exclusion["reason"], "unmappable_category")

    def test_exclusion_has_detail_field(self):
        """Every exclusion record includes a 'detail' key with human-readable context."""
        internal = make_mock_internal(visibility="internal")
        _, exclusion = map_to_public(internal)
        self.assertIn("detail", exclusion, "Exclusion missing 'detail' field")
        self.assertTrue(len(exclusion["detail"]) > 10)


class TestDeterministicOutput(unittest.TestCase):
    """Test 5: Deterministic ordering and SHA-256."""

    def test_sha256_deterministic(self):
        """Same data always produces the same SHA-256 hash."""
        data = {"a": 1, "b": [2, 3], "c": {"nested": "value"}}
        h1 = compute_sha256(data)
        h2 = compute_sha256(data)
        self.assertEqual(h1, h2)

    def test_sha256_changes_with_data(self):
        """Different data produces a different SHA-256 hash."""
        data1 = {"key": "value1"}
        data2 = {"key": "value2"}
        self.assertNotEqual(compute_sha256(data1), compute_sha256(data2))

    def test_sort_keys_guarantees_order(self):
        """json.dumps(sort_keys=True) produces byte-identical output."""
        data = {"z": 1, "a": 2, "m": 3}
        h1 = compute_sha256(data)
        # Reorder keys in the dict — sort_keys=True normalises them
        data_alt = {"a": 2, "m": 3, "z": 1}
        h2 = compute_sha256(data_alt)
        self.assertEqual(h1, h2)

    def test_output_sorting_by_document_id(self):
        """Test that run_export sorts eligible records by DocumentID."""
        mock_rows = [
            make_mock_internal(doc_id="RAE-00003", internal_id=3),
            make_mock_internal(doc_id="RAE-00001", internal_id=1),
            make_mock_internal(doc_id="RAE-00002", internal_id=2),
        ]
        audit = run_export(mock_rows=mock_rows)
        doc_ids = [d["DocumentID"] for d in audit["export_documents"]]
        self.assertEqual(doc_ids, sorted(doc_ids))

    def test_excluded_sorted_by_reason_then_id(self):
        """Excluded records should be sorted by reason, then DocumentID."""
        mock_rows = [
            make_mock_internal(doc_id="RAE-Z", category="UnknownX", internal_id=3),
            make_mock_internal(doc_id="RAE-A", category="UnknownY", internal_id=1),
        ]
        audit = run_export(mock_rows=mock_rows)
        doc_ids = [r["document_id"] for r in audit["excluded_records"]]
        self.assertEqual(doc_ids, sorted(doc_ids))


class TestValidatorDuplicateDetection(unittest.TestCase):
    """Test 4: Duplicate DocumentID detection by the validator."""

    def test_validator_detects_duplicate(self):
        """The validate-public-export validator should flag duplicate
        DocumentIDs in the exported documents list."""
        docs = [
            make_mock_public(doc_id="RAE-00001"),
            make_mock_public(doc_id="RAE-00001"),
        ]
        export = {
            "schemaVersion": SCHEMA_VERSION,
            "generatedAt": "2026-07-16T12:00:00Z",
            "source": "test",
            "preview_mode": False,
            "recordCount": len(docs),
            "documents": docs,
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(export, f, ensure_ascii=False)
            tmp_path = f.name
        try:
            success = validate(export_path=tmp_path)
            self.assertFalse(success, "Validator should reject duplicate DocumentIDs")
        finally:
            os.unlink(tmp_path)


class TestValidatorSchema(unittest.TestCase):
    """Test the static validator's schema checks."""

    def _build_export(self, docs: list) -> str:
        """Write a minimal export to a temp file and return the path."""
        export = {
            "schemaVersion": SCHEMA_VERSION,
            "generatedAt": "2026-07-16T12:00:00Z",
            "source": "test",
            "preview_mode": False,
            "recordCount": len(docs),
            "documents": docs,
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(export, f, ensure_ascii=False)
            return f.name

    def test_valid_export_passes(self):
        """A well-formed export passes all checks."""
        docs = [make_mock_public()]
        path = self._build_export(docs)
        try:
            success = validate(export_path=path)
            self.assertTrue(success)
        finally:
            os.unlink(path)

    def test_invalid_status_fails(self):
        """A record with an unrecognised status fails validation."""
        doc = make_mock_public(status="archived")
        path = self._build_export([doc])
        try:
            success = validate(export_path=path)
            self.assertFalse(success)
        finally:
            os.unlink(path)

    def test_invalid_visibility_fails(self):
        """A record with private visibility fails validation."""
        doc = make_mock_public(visibility="private")
        path = self._build_export([doc])
        try:
            success = validate(export_path=path)
            self.assertFalse(success)
        finally:
            os.unlink(path)

    def test_invalid_category_fails(self):
        """A record with a category outside the contract fails."""
        doc = make_mock_public(category="BogusCategory")
        path = self._build_export([doc])
        try:
            success = validate(export_path=path)
            self.assertFalse(success)
        finally:
            os.unlink(path)

    def test_missing_required_field_fails(self):
        """A record missing a required field (e.g. Title) fails."""
        doc = make_mock_public(title="")
        path = self._build_export([doc])
        try:
            success = validate(export_path=path)
            self.assertFalse(success)
        finally:
            os.unlink(path)

    def test_forbidden_field_fails(self):
        """A record containing a forbidden field fails."""
        doc = make_mock_public()
        doc["OwnerId"] = "some-value"  # forbidden
        path = self._build_export([doc])
        try:
            success = validate(export_path=path)
            self.assertFalse(success)
        finally:
            os.unlink(path)

    def test_preview_mode_true_fails(self):
        """preview_mode must be False for a public export."""
        path = self._build_export([make_mock_public()])
        try:
            # Inject preview_mode=true via direct write
            export = {
                "schemaVersion": SCHEMA_VERSION,
                "generatedAt": "2026-07-16T12:00:00Z",
                "source": "test",
                "preview_mode": True,
                "recordCount": 1,
                "documents": [make_mock_public()],
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(export, f, ensure_ascii=False)
            success = validate(export_path=path)
            self.assertFalse(success)
        finally:
            os.unlink(path)

    def test_missing_schema_version_fails(self):
        """Missing or wrong schemaVersion fails."""
        docs = [make_mock_public()]
        path = self._build_export(docs)
        try:
            export = {
                "schemaVersion": "0.0.0",
                "generatedAt": "2026-07-16T12:00:00Z",
                "source": "test",
                "preview_mode": False,
                "recordCount": 1,
                "documents": docs,
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(export, f, ensure_ascii=False)
            success = validate(export_path=path)
            self.assertFalse(success)
        finally:
            os.unlink(path)


class TestPrivacyCheck(unittest.TestCase):
    """Verify the privacy / forbidden-pattern check."""

    def test_no_forbidden_patterns_in_valid_record(self):
        """A valid public record should have zero forbidden-pattern hits."""
        public = make_mock_public()
        findings = check_forbidden_fields(public)
        self.assertEqual(len(findings), 0)

    def test_forbidden_patterns_detected(self):
        """If a record contains a forbidden pattern, it is flagged."""
        public = make_mock_public()
        public["StorageURL"] = public["StorageURL"] + "?Token=abc123"
        findings = check_forbidden_fields(public)
        self.assertGreater(len(findings), 0)
        pattern_found = any("Token" in f for f in findings)
        self.assertTrue(pattern_found)


class TestUtilityFunctions(unittest.TestCase):
    """Test standalone utility functions."""

    def test_is_valid_https_url(self):
        self.assertTrue(is_valid_https_url("https://example.com/doc.pdf"))
        self.assertFalse(is_valid_https_url(""))
        self.assertFalse(is_valid_https_url("http://example.com"))
        self.assertFalse(is_valid_https_url("ftp://example.com"))
        self.assertFalse(is_valid_https_url("https://a"))  # too short

    def test_determine_download_mode_empty(self):
        self.assertEqual(determine_download_mode(""), "AUTHENTICATED_SHAREPOINT")

    def test_determine_download_mode_guest(self):
        self.assertEqual(
            determine_download_mode("https://example.com/guest/abc"),
            "PUBLIC_SHAREPOINT_LINK",
        )

    def test_determine_download_mode_anonymous(self):
        self.assertEqual(
            determine_download_mode("https://example.com/anonymous/abc"),
            "PUBLIC_SHAREPOINT_LINK",
        )

    def test_determine_download_mode_sharepoint(self):
        self.assertEqual(
            determine_download_mode("https://maejo365.sharepoint.com/doc.pdf"),
            "AUTHENTICATED_SHAREPOINT",
        )


class TestBatchMode(unittest.TestCase):
    """Test the --doc-ids batch filter logic."""

    def test_batch_filter_keeps_only_targeted(self):
        """When run_export receives doc_ids_filter, only matching records are processed."""
        mock_rows = [
            make_mock_internal(doc_id="RAE-00001", internal_id=1),
            make_mock_internal(doc_id="RAE-00002", internal_id=2),
            make_mock_internal(doc_id="RAE-00003", internal_id=3),
        ]
        audit = run_export(mock_rows=mock_rows, doc_ids_filter={"RAE-00002"})
        eligible_ids = [d["DocumentID"] for d in audit["export_documents"]]
        self.assertEqual(eligible_ids, ["RAE-00002"])
        self.assertEqual(audit["export"]["batch_skipped"], 2)

    def test_batch_filter_all_skipped(self):
        """When no records match the filter, the export is empty."""
        mock_rows = [
            make_mock_internal(doc_id="RAE-00001", internal_id=1),
        ]
        audit = run_export(mock_rows=mock_rows, doc_ids_filter={"NONEXISTENT"})
        self.assertEqual(audit["export"]["eligible"], 0)
        self.assertEqual(audit["export"]["batch_skipped"], 1)

    def test_batch_filter_reconciliation(self):
        """Batch mode reconciliation accounts for batch_skipped."""
        mock_rows = [
            make_mock_internal(doc_id="RAE-00001", internal_id=1, status="current", visibility="public"),
            make_mock_internal(doc_id="RAE-00002", internal_id=2, status="draft", visibility="internal"),
            make_mock_internal(doc_id="RAE-00003", internal_id=3, status="current", visibility="public"),
        ]
        audit = run_export(mock_rows=mock_rows, doc_ids_filter={"RAE-00001", "RAE-00002"})
        total = len(mock_rows)
        accounted = (
            audit["export"]["eligible"]
            + audit["export"]["excluded"]
            + audit["export"]["batch_skipped"]
        )
        self.assertEqual(total, accounted,
                         f"Reconciliation mismatch: {total} != {accounted}")


class TestExclusionDetail(unittest.TestCase):
    """Verify that every exclusion record carries rich detail."""

    def test_exclusion_reasons_use_defined_gates(self):
        """Every exclusion reason should be one of the defined GATE_ORDER values."""
        valid_reasons = set(GATE_ORDER)
        test_cases = [
            (make_mock_internal(doc_id=""), "missing_document_id"),
            (make_mock_internal(title=""), "missing_title"),
            (make_mock_internal(visibility="internal"), "excluded_visibility"),
            (make_mock_internal(status="draft"), "excluded_status"),
            (make_mock_internal(category="BogusCat"), "unmappable_category"),
            (make_mock_internal(storage_url=""), "missing_storage_url"),
            (make_mock_internal(storage_url="http://bad"), "invalid_storage_url"),
        ]
        for internal, expected_reason in test_cases:
            with self.subTest(reason=expected_reason):
                _, exclusion = map_to_public(internal)
                self.assertIsNotNone(exclusion)
                self.assertEqual(exclusion["reason"], expected_reason)
                self.assertIn(exclusion["reason"], valid_reasons)

    def test_exclusion_detail_describes_why(self):
        """The 'detail' field on every exclusion explains the reason."""
        test_cases = [
            (make_mock_internal(doc_id=""), "missing_document_id", "Document_x0020_ID"),
            (make_mock_internal(visibility="internal"), "excluded_visibility", "Visibility"),
            (make_mock_internal(status="draft"), "excluded_status", "Status"),
        ]
        for internal, expected_reason, keyword in test_cases:
            with self.subTest(reason=expected_reason):
                _, exclusion = map_to_public(internal)
                detail = exclusion.get("detail", "")
                self.assertIn(keyword, detail,
                              f"Detail for '{expected_reason}' should mention '{keyword}'")


class TestReconciliation(unittest.TestCase):
    """Verify the reconciliation invariant."""

    def test_reconciliation_total_equals_sum(self):
        """total_records == eligible + excluded + batch_skipped."""
        mock_rows = [
            make_mock_internal(doc_id="RAE-00001", internal_id=1, status="current", visibility="public"),
            make_mock_internal(doc_id="RAE-00002", internal_id=2, status="draft", visibility="internal"),
            make_mock_internal(doc_id="", internal_id=3),  # no doc_id
            make_mock_internal(doc_id="RAE-00004", internal_id=4, category="Unknown", status="draft", visibility="internal"),
        ]
        audit = run_export(mock_rows=mock_rows)
        total = audit["live_registry"]["total_records"]
        accounted = audit["export"]["eligible"] + audit["export"]["excluded"]
        self.assertEqual(total, accounted,
                         f"Reconciliation: {total} != {accounted}")

    def test_reconciliation_all_cases(self):
        """Test with a mix of eligible, excluded, and missing doc_id records."""
        mock_rows = [
            make_mock_internal(doc_id="RAE-00001", internal_id=1, status="current", visibility="public"),
            make_mock_internal(internal_id=2, doc_id=""),  # missing doc_id
            make_mock_internal(doc_id="RAE-00003", internal_id=3, visibility="internal"),
            make_mock_internal(doc_id="RAE-00004", internal_id=4, status="draft"),
        ]
        audit = run_export(mock_rows=mock_rows)
        total = audit["live_registry"]["total_records"]
        accounted = audit["export"]["eligible"] + audit["export"]["excluded"]
        self.assertEqual(total, accounted,
                         f"Reconciliation: {total} != {accounted}")


class TestDeterministicExportFile(unittest.TestCase):
    """Verify that running the pipeline twice with the same input
    produces byte-identical output."""

    def test_repeatable_sha256(self):
        """Two runs with identical mock data produce the same SHA-256."""
        mock_rows = [
            make_mock_internal(doc_id="RAE-00002", internal_id=2),
            make_mock_internal(doc_id="RAE-00001", internal_id=1),
        ]
        audit1 = run_export(mock_rows=mock_rows)
        audit2 = run_export(mock_rows=mock_rows)
        self.assertEqual(
            audit1["export"]["sha256"],
            audit2["export"]["sha256"],
            "Two identical runs should produce the same SHA-256",
        )


# ── Entry Point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
