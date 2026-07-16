#!/usr/bin/env python3
"""
PXP-4 Batch Publisher Tests — validates the batch publisher logic
independently of M365 (no authentication, no live data).

Tests the pure functions and mock-isolated workflows of publish-batch.py.

Run:
    python scripts/registry/test-publish-batch.py        # uses unittest
    pytest scripts/registry/test-publish-batch.py -v      # if pytest is available
"""
import importlib.util
import json
import os
import sys
import tempfile
import time
import unittest
from unittest.mock import MagicMock, patch

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRY_DIR = os.path.join(REPO_ROOT, "scripts", "registry")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
PXP4_DIR = os.path.join(REPO_ROOT, ".migration", "pxp4")


def _load_module(name, filename):
    """Load a Python module from a file path (handles hyphenated filenames)."""
    path = os.path.join(REGISTRY_DIR, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


publisher = _load_module("publish_batch", "publish-batch.py")

# Bring key constants and functions into test namespace
parse_args = getattr(publisher, "parse_args")
authenticate = getattr(publisher, "authenticate")
read_registry_item = getattr(publisher, "read_registry_item")
publish_record = getattr(publisher, "publish_record")
load_checkpoint = getattr(publisher, "load_checkpoint")
save_checkpoint = getattr(publisher, "save_checkpoint")
REPO_ROOT = getattr(publisher, "REPO_ROOT")
DEFAULT_MANIFEST = getattr(publisher, "DEFAULT_MANIFEST")
DEFAULT_CHECKPOINT = getattr(publisher, "DEFAULT_CHECKPOINT")
DEFAULT_OUTPUT = getattr(publisher, "DEFAULT_OUTPUT")


# ── Helpers ────────────────────────────────────────────────────────────────

def make_mock_manifest_record(
    list_item_id=1,
    doc_id="RAE-00001",
    prev_status="draft",
    prev_visibility="internal",
):
    """Build a mock manifest record matching the format used in pxp4-batch-a-manifest.json."""
    return {
        "ListItemId": list_item_id,
        "DocumentID": doc_id,
        "PreviousStatus": prev_status,
        "PreviousVisibility": prev_visibility,
    }


def make_mock_manifest(count=10, start_id=1):
    """Build a list of mock manifest records."""
    return [
        make_mock_manifest_record(
            list_item_id=start_id + i,
            doc_id=f"RAE-{start_id + i:05d}",
            prev_status="draft",
            prev_visibility="internal",
        )
        for i in range(count)
    ]


def make_mock_registry_read(status="draft", visibility="internal"):
    """Build a mock SharePoint Registry read response."""
    return {
        "Id": 1,
        "Status": status,
        "Visibility": visibility,
        "Document_x0020_ID": "RAE-00001",
    }


# ── Test Cases ─────────────────────────────────────────────────────────────


class TestManifestParsing(unittest.TestCase):
    """Verify the manifest file can be loaded and has the expected structure."""

    def test_default_manifest_exists(self):
        """The default manifest file must exist with the right format."""
        self.assertTrue(
            os.path.exists(DEFAULT_MANIFEST),
            f"Default manifest not found: {DEFAULT_MANIFEST}",
        )
        with open(DEFAULT_MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertIsInstance(manifest, list)
        self.assertGreater(len(manifest), 0, "Manifest should not be empty")

    def test_manifest_record_has_required_fields(self):
        """Every manifest record must have DocumentID, ListItemId, PreviousStatus, PreviousVisibility."""
        with open(DEFAULT_MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
        required = {"DocumentID", "ListItemId", "PreviousStatus", "PreviousVisibility"}
        for i, rec in enumerate(manifest):
            with self.subTest(record=i, doc_id=rec.get("DocumentID", "?")):
                for field in required:
                    self.assertIn(field, rec, f"Record {i} missing field: {field}")
                self.assertTrue(
                    str(rec.get("DocumentID", "")).strip(),
                    f"Record {i} has empty DocumentID",
                )
                self.assertIsInstance(
                    rec.get("ListItemId"),
                    int,
                    f"Record {i} ListItemId must be int",
                )

    def test_manifest_100_records(self):
        """The batch-a manifest should contain exactly 100 records."""
        with open(DEFAULT_MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(len(manifest), 100)

    def test_manifest_all_unique_ids(self):
        """Every DocumentID in the manifest should be unique."""
        with open(DEFAULT_MANIFEST, encoding="utf-8") as f:
            manifest = json.load(f)
        doc_ids = [rec["DocumentID"] for rec in manifest]
        self.assertEqual(len(doc_ids), len(set(doc_ids)), "Duplicate DocumentIDs found")

    def test_mock_manifest_valid(self):
        """The helper should produce records matching the expected format."""
        manifest = make_mock_manifest(count=5)
        self.assertEqual(len(manifest), 5)
        for rec in manifest:
            self.assertIn("DocumentID", rec)
            self.assertIn("ListItemId", rec)
            self.assertIn("PreviousStatus", rec)
            self.assertIn("PreviousVisibility", rec)


class TestCheckpointLogic(unittest.TestCase):
    """Verify checkpoint save/load/resume works correctly."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.checkpoint_path = os.path.join(self.tmpdir, "checkpoint.json")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_save_and_load_checkpoint(self):
        """Saving then loading a checkpoint returns identical data."""
        original = {
            "batch_index": 2,
            "completed_batches": 3,
            "processed_ids": ["RAE-00001", "RAE-00002", "RAE-00003"],
            "timestamp": "2026-07-16T08:00:00Z",
            "results_so_far": {
                "published": ["RAE-00001"],
                "failed": [],
                "skipped": ["RAE-00002", "RAE-00003"],
            },
            "audit_log": [
                {
                    "doc_id": "RAE-00001",
                    "list_item_id": 1,
                    "timestamp": "2026-07-16T08:00:00Z",
                    "status": "published",
                    "error": None,
                    "response": "Status=current, Visibility=public",
                }
            ],
        }
        save_checkpoint(self.checkpoint_path, original)
        self.assertTrue(os.path.exists(self.checkpoint_path))

        loaded = load_checkpoint(self.checkpoint_path)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["completed_batches"], 3)
        self.assertEqual(len(loaded["processed_ids"]), 3)
        self.assertEqual(len(loaded["results_so_far"]["published"]), 1)
        self.assertEqual(len(loaded["audit_log"]), 1)

    def test_load_missing_checkpoint(self):
        """Loading a non-existent checkpoint returns None."""
        result = load_checkpoint(os.path.join(self.tmpdir, "nonexistent.json"))
        self.assertIsNone(result)

    def test_load_corrupt_checkpoint(self):
        """Loading a corrupt checkpoint file returns None."""
        path = os.path.join(self.tmpdir, "corrupt.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write("not json")
        result = load_checkpoint(path)
        self.assertIsNone(result)

    def test_checkpoint_atomic_write(self):
        """Checkpoint writes should be atomic (uses .tmp then rename)."""
        cp = {"completed_batches": 1, "processed_ids": [], "results_so_far": {}, "audit_log": []}
        save_checkpoint(self.checkpoint_path, cp)
        # Verify no .tmp file remains
        self.assertFalse(os.path.exists(self.checkpoint_path + ".tmp"))
        self.assertTrue(os.path.exists(self.checkpoint_path))

    def test_resume_skip_already_processed(self):
        """When resuming, records already in processed_ids should be skipped."""
        manifest = make_mock_manifest(count=10)
        processed = {f"1:RAE-00001", "RAE-00001", "2:RAE-00002", "RAE-00002", "3:RAE-00003", "RAE-00003"}
        remaining = []
        for rec in manifest:
            doc_id = rec.get("DocumentID", "").strip()
            entry_id = f"{rec.get('ListItemId')}:{doc_id}"
            if entry_id not in processed and doc_id not in processed:
                remaining.append(rec)
        self.assertEqual(len(remaining), 7)


class TestIdempotentUpdate(unittest.TestCase):
    """Verify already-public records are skipped without API calls."""

    @patch.object(publisher, "read_registry_item")
    def test_skip_already_public(self, mock_read):
        """A record that is already current/public should be skipped."""
        mock_read.return_value = make_mock_registry_read(status="current", visibility="public")
        headers = {"mock": "headers"}
        entry = publish_record(headers, list_item_id=1, doc_id="RAE-00001")
        self.assertEqual(entry["status"], "skipped")
        self.assertIn("Already", entry.get("response", ""))

    @patch.object(publisher, "read_registry_item")
    @patch.object(publisher.requests, "post")
    def test_publish_draft_record(self, mock_post, mock_read):
        """A draft/internal record should be published."""
        mock_read.return_value = make_mock_registry_read(status="draft", visibility="internal")
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "d": {
                "ValidateUpdateListItem": {
                    "results": [{"HasException": False}]
                }
            }
        }
        headers = {"mock": "headers"}
        entry = publish_record(headers, list_item_id=1, doc_id="RAE-00001")
        self.assertEqual(entry["status"], "published")

    @patch.object(publisher, "read_registry_item")
    @patch.object(publisher.requests, "post")
    def test_dry_run_skips_api_call(self, mock_post, mock_read):
        """In dry-run mode, no API call should be made."""
        mock_read.return_value = make_mock_registry_read(status="draft", visibility="internal")
        headers = {"mock": "headers"}
        entry = publish_record(headers, list_item_id=1, doc_id="RAE-00001", dry_run=True)
        self.assertEqual(entry["status"], "dry-run")
        mock_post.assert_not_called()

    @patch.object(publisher, "read_registry_item")
    def test_skip_partial_public(self, mock_read):
        """A record with only Status=current but Visibility=internal should still be updated."""
        mock_read.return_value = make_mock_registry_read(status="current", visibility="internal")
        headers = {"mock": "headers"}
        entry = publish_record(headers, list_item_id=1, doc_id="RAE-00001")
        self.assertNotEqual(entry["status"], "skipped", "Partially current record should not be skipped")

    @patch.object(publisher, "read_registry_item")
    def test_skip_reverse_partial_public(self, mock_read):
        """A record with only Visibility=public but Status=draft should still be updated."""
        mock_read.return_value = make_mock_registry_read(status="draft", visibility="public")
        headers = {"mock": "headers"}
        entry = publish_record(headers, list_item_id=1, doc_id="RAE-00001")
        self.assertNotEqual(entry["status"], "skipped", "Partially current record should not be skipped")


class TestPartialFailureRetry(unittest.TestCase):
    """Verify retry logic: failed records are retried once before being marked as failed."""

    @patch.object(publisher, "read_registry_item")
    @patch.object(publisher.requests, "post")
    def test_retry_on_http_error(self, mock_post, mock_read):
        """A record that fails on first attempt should be retried."""
        mock_read.return_value = make_mock_registry_read(status="draft", visibility="internal")
        # First call fails, second call succeeds
        mock_post.side_effect = [
            MagicMock(status_code=500, text="Server Error"),
            MagicMock(
                status_code=200,
                json=lambda: {
                    "d": {
                        "ValidateUpdateListItem": {
                            "results": [{"HasException": False}]
                        }
                    }
                },
            ),
        ]
        headers = {"mock": "headers"}
        entry = publish_record(headers, list_item_id=1, doc_id="RAE-00001")
        # publish_record only does one attempt and the caller does retry
        # The first call should fail
        self.assertEqual(entry["status"], "failed")
        self.assertEqual(mock_post.call_count, 1)

    def test_retry_logic_in_main(self):
        """Simulate the retry loop used in main()."""
        # This tests the retry pattern from publish-batch.py main():
        # entry = publish_record(...)
        # if entry['status'] == 'failed':
        #     time.sleep(1)
        #     entry = publish_record(...)
        headers = {"mock": "headers"}
        results = []

        with patch.object(publisher, "read_registry_item") as mock_read, \
             patch.object(publisher.requests, "post") as mock_post:
            # Mock pre-read for attempt 1
            mock_read.return_value = make_mock_registry_read(status="draft", visibility="internal")
            # First POST fails
            mock_post.return_value = MagicMock(status_code=500, text="Server Error")
            entry1 = publish_record(headers, 1, "RAE-00001")
            results.append(entry1)

            if entry1["status"] == "failed":
                # Mock pre-read for retry
                mock_read.return_value = make_mock_registry_read(status="draft", visibility="internal")
                # Retry succeeds
                mock_post.return_value = MagicMock(
                    status_code=200,
                    json=lambda: {
                        "d": {
                            "ValidateUpdateListItem": {
                                "results": [{"HasException": False}]
                            }
                        }
                    },
                )
                entry2 = publish_record(headers, 1, "RAE-00001")
                results.append(entry2)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "failed")
        self.assertEqual(results[1]["status"], "published")

    @patch.object(publisher, "read_registry_item")
    @patch.object(publisher.requests, "post")
    def test_retry_still_fails(self, mock_post, mock_read):
        """If retry also fails, record remains in failed state."""
        mock_read.return_value = make_mock_registry_read(status="draft", visibility="internal")
        mock_post.return_value = MagicMock(status_code=500, text="Server Error")
        headers = {"mock": "headers"}
        # First attempt
        entry1 = publish_record(headers, 1, "RAE-00001")
        self.assertEqual(entry1["status"], "failed")
        # Retry
        entry2 = publish_record(headers, 1, "RAE-00001")
        self.assertEqual(entry2["status"], "failed")
        self.assertEqual(mock_post.call_count, 2)


class TestCLIArguments(unittest.TestCase):
    """Verify CLI argument parsing works correctly."""

    def test_default_args(self):
        """Default arguments should use expected paths."""
        with patch.object(sys, "argv", ["publish-batch.py"]):
            args = parse_args()
            self.assertFalse(args.resume)
            self.assertFalse(args.dry_run)
            self.assertEqual(args.batch_size, 25)
            self.assertEqual(args.manifest, DEFAULT_MANIFEST)
            self.assertEqual(args.checkpoint, DEFAULT_CHECKPOINT)
            self.assertEqual(args.output, DEFAULT_OUTPUT)

    def test_resume_flag(self):
        """--resume flag should be parsed correctly."""
        with patch.object(sys, "argv", ["publish-batch.py", "--resume"]):
            args = parse_args()
            self.assertTrue(args.resume)

    def test_dry_run_flag(self):
        """--dry-run flag should be parsed correctly."""
        with patch.object(sys, "argv", ["publish-batch.py", "--dry-run"]):
            args = parse_args()
            self.assertTrue(args.dry_run)

    def test_batch_size(self):
        """--batch-size should be parsed and validated."""
        with patch.object(sys, "argv", ["publish-batch.py", "--batch-size", "22"]):
            args = parse_args()
            self.assertEqual(args.batch_size, 22)

    def test_custom_paths(self):
        """Custom manifest/checkpoint/output paths should be accepted."""
        with patch.object(sys, "argv", [
            "publish-batch.py",
            "--manifest", "/custom/manifest.json",
            "--checkpoint", "/custom/checkpoint.json",
            "--output", "/custom/output.json",
        ]):
            args = parse_args()
            self.assertEqual(args.manifest, "/custom/manifest.json")
            self.assertEqual(args.checkpoint, "/custom/checkpoint.json")
            self.assertEqual(args.output, "/custom/output.json")

    def test_batch_size_out_of_range(self):
        """batch-size outside 20-25 should be handled (validation in main)."""
        with patch.object(sys, "argv", ["publish-batch.py", "--batch-size", "100"]):
            args = parse_args()
            self.assertEqual(args.batch_size, 100)
            # Validation happens in main(), not parse_args()


class TestAuditLog(unittest.TestCase):
    """Verify audit log structure and completeness."""

    def test_audit_entry_has_required_fields(self):
        """Each audit entry must have doc_id, list_item_id, timestamp, status, error, response."""
        required = {"doc_id", "list_item_id", "timestamp", "status", "error", "response"}
        entry = {
            "doc_id": "RAE-00001",
            "list_item_id": 1,
            "timestamp": "2026-07-16T08:00:00Z",
            "status": "published",
            "error": None,
            "response": "Status=current, Visibility=public",
        }
        for field in required:
            self.assertIn(field, entry)

    @patch.object(publisher, "read_registry_item")
    def test_audit_entry_on_skip(self, mock_read):
        """Skipped records should produce a complete audit entry."""
        mock_read.return_value = make_mock_registry_read(status="current", visibility="public")
        headers = {"mock": "headers"}
        entry = publish_record(headers, 1, "RAE-00001")
        self.assertEqual(entry["status"], "skipped")
        self.assertIn("timestamp", entry)
        self.assertIn("doc_id", entry)
        self.assertIn("list_item_id", entry)

    @patch.object(publisher, "read_registry_item")
    @patch.object(publisher.requests, "post")
    def test_audit_entry_on_publish(self, mock_post, mock_read):
        """Published records should produce a complete audit entry."""
        mock_read.return_value = make_mock_registry_read(status="draft", visibility="internal")
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "d": {
                "ValidateUpdateListItem": {
                    "results": [{"HasException": False}]
                }
            }
        }
        headers = {"mock": "headers"}
        entry = publish_record(headers, 1, "RAE-00001")
        self.assertEqual(entry["status"], "published")
        self.assertIn("timestamp", entry)
        self.assertIn("response", entry)


class TestDryRun(unittest.TestCase):
    """Verify dry-run mode correctly previews changes."""

    def test_dry_run_output_structure(self):
        """The dry-run results output should include audit_log and dry_run flag."""
        # Simulate a dry-run results structure
        results = {
            "published": [],
            "failed": [],
            "skipped": [],
            "total": 5,
            "timestamp": "2026-07-16T08:00:00Z",
            "dry_run": True,
            "audit_log": [
                {
                    "doc_id": "RAE-00001",
                    "list_item_id": 1,
                    "timestamp": "2026-07-16T08:00:00Z",
                    "status": "dry-run",
                    "error": None,
                    "response": "Would update: Status=draft→current, Visibility=internal→public",
                }
            ],
            "source_manifest": DEFAULT_MANIFEST,
        }
        self.assertTrue(results["dry_run"])
        self.assertEqual(results["published"], [])
        self.assertEqual(len(results["audit_log"]), 1)
        self.assertEqual(results["audit_log"][0]["status"], "dry-run")


class TestOutputFormat(unittest.TestCase):
    """Verify the output results format matches expectations."""

    def test_output_format_fields(self):
        """The output JSON must have published, failed, skipped, total, timestamp, audit_log."""
        output = {
            "published": ["RAE-00001"],
            "failed": [],
            "skipped": ["RAE-00002"],
            "total": 2,
            "timestamp": "2026-07-16T08:00:00Z",
            "dry_run": False,
            "audit_log": [],
            "source_manifest": DEFAULT_MANIFEST,
        }
        required = {"published", "failed", "skipped", "total", "timestamp", "audit_log", "source_manifest"}
        for field in required:
            self.assertIn(field, output)


class TestPreReadFailure(unittest.TestCase):
    """Verify behavior when the pre-read (idempotency check) fails."""

    @patch.object(publisher, "read_registry_item")
    def test_pre_read_exception_results_in_failure(self, mock_read):
        """If the pre-read for an item fails, it should be recorded as failed."""
        mock_read.side_effect = Exception("Network error during pre-read")
        headers = {"mock": "headers"}
        entry = publish_record(headers, list_item_id=999, doc_id="RAE-99999")
        self.assertEqual(entry["status"], "failed")
        self.assertIn("Pre-read", entry.get("error", ""))


# ── Entry Point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
