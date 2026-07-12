# EA / M365 WORK PC Recovery Runbook — RETIRED

**RETIRED — 2026-07-12**

This runbook was based on the assumption that `G:\ProjectAI\RAE-M365-Platform` existed as a one-time historical recovery source for EA / M365 architecture artifacts.

**This assumption was investigated and confirmed FALSE.** The path does not exist on any accessible machine. There is, and has only ever been, one canonical project: `numtip/document-center` on GitHub.

### Disposition

- **Status:** STALE_ASSUMPTION
- **Reason:** The entire document's purpose was a recovery procedure for a source that was never confirmed to exist. Every step, prerequisite, and command operated against `G:\ProjectAI\RAE-M365-Platform` — without that source, the document has no actionable content.
- **Evidence:** See [`docs/architecture/CANONICAL_REPOSITORY_CAPABILITY_AUDIT.md`](../architecture/CANONICAL_REPOSITORY_CAPABILITY_AUDIT.md) (Co-Work A: factual capability audit, no second project referenced) and [`docs/architecture/INVALID_RECOVERY_ASSUMPTION_REVIEW.md`](../architecture/INVALID_RECOVERY_ASSUMPTION_REVIEW.md) (Co-Work B: complete catalog of the false assumption and its corrections).

### Replacement

The forward-implementation equivalents of the recovery steps are now governed by:

- [`docs/architecture/EA_FORWARD_IMPLEMENTATION_BASELINE.md`](../architecture/EA_FORWARD_IMPLEMENTATION_BASELINE.md) — canonical current state and forward implementation scope
- [`docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md`](../architecture/EA_LEGACY_RECOVERY_MANIFEST.md) — forward implementation manifest with BUILD_NEW / EXTEND_EXISTING / NEEDS_ADR classifications
- [`docs/architecture/EA_RECOVERY_GAP_MATRIX.md`](../architecture/EA_RECOVERY_GAP_MATRIX.md) — gap matrix with forward implementation priorities

### Original content

Preserved in Git history at commits `d9f5c37`, `729b5ad`, `64eed3f` — not deleted, only retired from active guidance.
