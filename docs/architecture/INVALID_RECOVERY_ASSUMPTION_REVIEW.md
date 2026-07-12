# Invalid Recovery Assumption Review

**Project:** RAE Document Center
**Canonical repo:** `https://github.com/numtip/document-center`
**Analyst:** Co-Work B (Recovery Assumption Cleanup Analyst)
**Date:** 2026-07-12
**Status:** Analysis only — no source documents modified

---

## Context

A prior task committed five governance/recovery documents to `main` (commits `d9f5c37`, `729b5ad`, `64eed3f`) that assumed a second project, **RAE-M365-Platform**, existed at `G:\ProjectAI\RAE-M365-Platform` and could serve as a "one-time historical recovery source" for missing EA/M365 architecture artifacts.

**This assumption has been verified FALSE.** The path `G:\ProjectAI\RAE-M365-Platform` does not exist on any accessible machine. There is, and has only ever been, **one canonical project**: `numtip/document-center` on GitHub.

This document catalogs every statement in the affected files that depends on the nonexistent RAE-M365-Platform project, assesses the impact of leaving each statement uncorrected, specifies the required correction, and assigns a disposition to each file. **No files were modified as part of this review** — see [`docs/architecture/INVALID_RECOVERY_ASSUMPTION_REVIEW.md`](INVALID_RECOVERY_ASSUMPTION_REVIEW.md) file ownership boundary in the originating task.

### Scope confirmation

A repository-wide search confirmed the false assumption is contained to exactly the 5 files named in scope. No other files reference `RAE-M365-Platform`, `historical recovery source`, or the `recovery/ea-m365-baseline` branch name.

| Search pattern | Files matched |
|---|---|
| `RAE-M365-Platform` | `PROJECT_BASELINE.md`, `docs/governance/REPOSITORY_CONVERGENCE_MODEL.md`, `docs/architecture/EA_RECOVERY_GAP_MATRIX.md`, `docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md`, `docs/runbooks/EA_WORK_PC_RECOVERY_RUNBOOK.md` |
| `historical recovery source` | `PROJECT_BASELINE.md`, `docs/governance/REPOSITORY_CONVERGENCE_MODEL.md` |
| `recovery/ea-m365-baseline` | `docs/governance/REPOSITORY_CONVERGENCE_MODEL.md`, `docs/runbooks/EA_WORK_PC_RECOVERY_RUNBOOK.md` |

`docs/runbooks/WORKSTATION_SYNC_RUNBOOK.md` was also inspected because it matches a broader `WORK PC` search — it references a generic WORK-workstation checkout of the canonical repository (a valid, unrelated concept) and contains **no** reference to RAE-M365-Platform. No correction required for that file.

---

## Findings by File

### File: `PROJECT_BASELINE.md`

| Incorrect Assumption | Impact | Required Correction |
|---|---|---|
| "Known Archives for Recovery" table lists `G:\ProjectAI\RAE-M365-Platform` — "ONE-TIME historical recovery source" — Status: **Active** | Presents a nonexistent path as a live, "Active" recovery source in the project's top-level baseline document. Anyone onboarding or auditing the project would believe a second data source is standing by for import. | Remove the "Known Archives for Recovery" section in its entirety, or replace it with an explicit statement: "No external recovery sources exist. This repository is the sole source of project history." |
| Blockquote: "`G:\ProjectAI\RAE-M365-Platform` is NOT a second canonical project. It is a recovery source only. After historical recovery is complete, all authoritative work must flow through the canonical repository..." | Frames the retirement of a nonexistent source as a pending, actionable future step, implying recovery work is outstanding and could still block "authoritative work" from being fully centralized in Git. | Remove the blockquote. If retained for historical framing, replace with a statement that no recovery step ever existed or was required — the canonical repository has always been the sole authoritative source. |

**Disposition: REQUIRES_CORRECTION** — the canonical-repository identity, branch strategy, and governance-reference sections are valid and unaffected; only the "Known Archives for Recovery" section and its blockquote depend on the false assumption.

---

### File: `docs/governance/REPOSITORY_CONVERGENCE_MODEL.md`

| Incorrect Assumption | Impact | Required Correction |
|---|---|---|
| Model diagram (§1) includes the node `G:\ProjectAI\RAE-M365-Platform = one-time historical recovery source (retired after import)` | Embeds a nonexistent node into the project's authoritative repository model diagram, giving false structural weight to a source that was never real. | Delete the `G:\ProjectAI\RAE-M365-Platform` line from the diagram. The model should show only: GitHub main, feature/work branches, HOME checkout, WORK checkout. |
| Sentence following the diagram: "After historical recovery completes, no active project development occurs outside Git." | Implies a precondition ("historical recovery completes") that can never be satisfied because there is nothing to recover, which — read literally — could be (mis)interpreted as permanently deferring the "no development outside Git" rule. | Remove the sentence, or rewrite as an unconditional statement: "No active project development occurs outside Git" (the rule was always true and never depended on any recovery step). |
| Repository Hierarchy table (§2) row: `G:\ProjectAI\RAE-M365-Platform (WORK)` — "One-time recovery source" — "Not a canonical project. Retired after import." | Adds a nonexistent layer to the canonical hierarchy table, alongside genuinely real layers (GitHub main, HOME checkout, WORK checkout). | Delete this table row entirely. |
| §6 "Recovery Source Status" — entire section, including the retirement command `rtk mv G:\ProjectAI\RAE-M365-Platform G:\ProjectAI\RAE-M365-Platform.RECOVERED.<YYYY-MM-DD>` and the reference to the `recovery/ea-m365-baseline` branch process | Presents a concrete, copy-pasteable command against a path that does not exist. If executed, it fails; the failure could be misread as an environment/access problem rather than confirmation the assumption was false. Also implies a specific recovery branch (`recovery/ea-m365-baseline`) was a real, expected workflow artifact. | Delete §6 in its entirety. Renumber subsequent sections (§7 "All Commands Use `rtk` Prefix" becomes §6). Remove the `recovery/ea-m365-baseline` branch reference from this document. |

**Disposition: REQUIRES_CORRECTION** — the core single-canonical-repository model (GitHub main = canonical; HOME and WORK are Git-backed checkouts of it; divergence-handling rules; frozen governance rules; `rtk`-prefix convention) is valid, well-formed governance and should be retained. Only the RAE-M365-Platform-specific diagram node, hierarchy row, and §6 need removal.

---

### File: `docs/architecture/EA_RECOVERY_GAP_MATRIX.md`

| Incorrect Assumption | Impact | Required Correction |
|---|---|---|
| Header: "**WORK PC source (claimed):** `G:\ProjectAI\RAE-M365-Platform`" | Frames the entire gap analysis as validating a specific external claim rather than simply documenting what is/isn't in GitHub yet. | Remove this header row, or replace with "Comparison basis: claimed EA artifact inventory (source unverifiable / nonexistent) vs. actual GitHub content." |
| "Recovery Priority" column throughout the Summary table (values: HIGH, CRITICAL, MEDIUM) | Frames urgency in terms of *recovering from an external source*, which risks directing engineers to search for or wait on a nonexistent system instead of scoping new implementation work. | Rename column to "Implementation Priority" and confirm the underlying priority rationale (e.g., "Taxonomy v2 essential for EA-3F") is about build effort, not recovery effort. |
| "EA-3F Readiness Determination" → **Decision: RECOVERY_REQUIRED_BEFORE_EA_3F** | This decision requires an action (recovery from a nonexistent source) that is permanently impossible. Taken literally, it would block EA-3F indefinitely. | Change decision label to something like `FORWARD_IMPLEMENTATION_REQUIRED_BEFORE_EA_3F`, and reframe the supporting "Evidence" bullets (currently phrased as "duplicating work that reportedly already exists on the WORK PC," etc.) to describe gaps that must be newly designed and built. |
| "Recommended path," step 1: "**Recover WORK PC artifacts** using the runbook at `docs/runbooks/EA_WORK_PC_RECOVERY_RUNBOOK.md`" | Points to a runbook whose only stated source does not exist — a dead-end procedure that cannot succeed. | Replace step 1 with a forward-implementation step, e.g., "Design and author the missing EA-3A–3E artifacts directly against the canonical repository; there is no external source to import from." Remove the reference to the recovery runbook. |
| Scattered speculative language in Notes columns, e.g., "The WORK PC may have additional states (e.g., pending-review, approved, published)" | Implies a real, inspectable secondary system whose contents are merely unknown/unconfirmed, rather than a system that does not exist at all. | Reword such notes to describe design options to consider going forward (e.g., "Consider additional states such as pending-review, approved, published as part of forward design"), not speculation about an external system's contents. |

**Disposition: REQUIRES_CORRECTION** — the core artifact-by-artifact comparison of *claimed* EA-3A–3E scope against *actual* GitHub content (the Gap Matrix itself, the "Key Architecture Conflicts," and the "What exists that IS usable for EA-3F" section) remains a valid and useful audit of what is missing from the canonical repository. Only the recovery-sourced framing, the "Recovery Priority"/"RECOVERY_REQUIRED" language, and the pointer to the recovery runbook need correction.

---

### File: `docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md`

| Incorrect Assumption | Impact | Required Correction |
|---|---|---|
| Header: "**Recovery source:** `G:\ProjectAI\RAE-M365-Platform`" and "**Canonical target:** `G:\ProjectAI\document-center` (WORK PC checkout)" | Sets the document's stated purpose as importing from a nonexistent source into a WORK PC checkout, an objective that can never be achieved. | Remove or replace the header framing with "Comparison basis: claimed EA artifact inventory vs. actual canonical GitHub content" (no recovery source, no WORK PC target). |
| "Likely File/Path Pattern" column — 23 rows, each fabricating a plausible-looking path under `RAE-M365-Platform\EA-3X\...` (e.g., `RAE-M365-Platform\EA-3A\sharepoint-site-design.md`) | These are invented, speculative paths for a directory tree that was never confirmed to exist. Anyone acting on this manifest would search fruitlessly for files at these exact fabricated paths, or worse, could be misled into treating a coincidentally similar file elsewhere as a "match." | Remove the "Likely File/Path Pattern" column entirely from all tables (EA-3A through Memory OS). There is no recovery source to pattern-match against. |
| "Import Classification" column values (`IMPORT_AS_AUTHORITATIVE`, `MERGE_WITH_EXISTING`, `REQUIRES_ADR_REVIEW`, etc.) — premised on inspecting real files found at the recovery source | None of these classifications can ever be exercised because there is nothing to find or inspect at the source. | Rename column to "Implementation Classification" and remap values to forward-implementation actions, e.g.: `BUILD_NEW` (replaces IMPORT_AS_AUTHORITATIVE — artifact doesn't exist anywhere, must be newly authored), `EXTEND_EXISTING` (replaces MERGE_WITH_EXISTING — a partial GitHub equivalent exists and should be extended), `NEEDS_ADR` (replaces REQUIRES_ADR_REVIEW — architectural decision needed before building). Drop `RETAIN_AS_HISTORICAL` and `DO_NOT_IMPORT_DUPLICATE` (both presuppose a discoverable source). |
| "Recovery Item Count" summary table — a precise 23-item accounting across import classifications | Presents an authoritative-looking accounting of "items to be recovered" that can never be actioned as recovery, since there is nothing to recover. | Re-derive the count as an "Items requiring forward implementation" accounting once the Implementation Classification remapping above is applied. |

**Disposition: REQUIRES_CORRECTION** — the "Canonical Comparison Target" column and the underlying claimed-vs-actual-GitHub-content comparison remain valid and useful (they show precisely what already exists in GitHub for each claimed artifact). Only the recovery-source framing, the fabricated "Likely File/Path Pattern" column, and the import-classification vocabulary need correction to reflect that these are build targets, not recovery targets.

---

### File: `docs/runbooks/EA_WORK_PC_RECOVERY_RUNBOOK.md`

| Incorrect Assumption | Impact | Required Correction |
|---|---|---|
| Document purpose (Purpose section): "One-time procedure to recover missing EA/M365 architecture artifacts from the WORK PC at `G:\ProjectAI\RAE-M365-Platform` and integrate them into the canonical GitHub repository" | The entire document's reason for existing is to execute a recovery that cannot happen. | No partial correction is possible — the document's premise itself is false. |
| Prerequisites table: "Recovery source | `G:\ProjectAI\RAE-M365-Platform` must be accessible" | States as a prerequisite something that is permanently unsatisfiable. | N/A — see disposition. |
| Step 1–14 workflow, all of which manipulate/reference `G:\ProjectAI\RAE-M365-Platform` (inspect, inventory, classify, compare, import, retire) | Every single procedural step is scoped to a nonexistent directory. Following Step 3 ("Inspect recovery source" — `rtk ls G:\ProjectAI\RAE-M365-Platform`) will simply fail. An engineer unaware of this review could burn time troubleshooting "why can't I access the recovery source" rather than understanding that no source was ever confirmed to exist. | N/A — see disposition. |
| "Quick Reference" sequential command list — repeats the same `G:\ProjectAI\RAE-M365-Platform` operations as a condensed script | Same as above — a ready-to-run script against a nonexistent path, which increases the chance someone executes it without reading the full context first. | N/A — see disposition. |
| Error recovery table entry: "WORK PC source not found → Document absence. Note: `G:\ProjectAI\RAE-M365-Platform` does not exist. Recovery impossible without source." | This is the one line in the entire document that is *actually accurate* — it correctly anticipates the now-confirmed real-world state. However, it is presented as merely one contingency among several ("Validation fails," "Secrets detected," etc.), not as the actual, confirmed outcome that supersedes the rest of the document. | Elevate this fact to the top of the document (or replace the document, see disposition) rather than burying it as one row in a contingency table at the bottom. |

**Disposition: STALE_ASSUMPTION** — the entire document's purpose is a recovery procedure with no valid source to recover from. Unlike the other four files, there is no salvageable governance content once the recovery premise is removed — every step, prerequisite, and command exists solely to operate against `G:\ProjectAI\RAE-M365-Platform`. Recommend retiring the document (e.g., replacing its body with a short pointer noting the assumption was investigated and found false, with a link to this review) rather than attempting line-level correction. Per the "do not delete evidence" principle, the file should not simply be deleted without a trace — either retain it with a clear historical-record banner, or rely on Git history (commits `d9f5c37`/`729b5ad`/`64eed3f`) to preserve the original content if it is removed from the working tree.

---

## Summary

| Disposition | File count | Files |
|---|---|---|
| **REQUIRES_CORRECTION** | 4 | `PROJECT_BASELINE.md`, `docs/governance/REPOSITORY_CONVERGENCE_MODEL.md`, `docs/architecture/EA_RECOVERY_GAP_MATRIX.md`, `docs/architecture/EA_LEGACY_RECOVERY_MANIFEST.md` |
| **STALE_ASSUMPTION** | 1 | `docs/runbooks/EA_WORK_PC_RECOVERY_RUNBOOK.md` |
| **CORRECT_AS_GOVERNANCE** | 0 (whole file) | — (applies only to unaffected *portions* of the 4 REQUIRES_CORRECTION files; see per-file notes above) |
| **RETAIN_AS_HISTORICAL_NOTE** | 0 (as a distinct recommendation) | Not recommended as the primary disposition for any file; however, per the "no evidence deletion" principle, whichever file(s) are ultimately edited or retired should preserve a historical-record trace (either an in-document note or reliance on Git history), rather than being silently rewritten or deleted. |

**Total literal references to `RAE-M365-Platform` across the 5 files: 45** (line-level occurrences: `PROJECT_BASELINE.md` = 2, `REPOSITORY_CONVERGENCE_MODEL.md` = 4, `EA_RECOVERY_GAP_MATRIX.md` = 1, `EA_LEGACY_RECOVERY_MANIFEST.md` = 23, `EA_WORK_PC_RECOVERY_RUNBOOK.md` = 15).

---

## What Remains Valid — Explicit Preservation Notes

### `PROJECT_BASELINE.md` and `REPOSITORY_CONVERGENCE_MODEL.md`

The **core canonical-repository model is correct and must be preserved**:

- GitHub (`https://github.com/numtip/document-center`, branch `main`) is the single canonical, integrated source of truth.
- HOME and WORK workstations are simply Git-backed checkouts of that canonical repository — this is a valid, ordinary two-workstation Git workflow and has nothing to do with RAE-M365-Platform.
- The divergence-handling matrix, frozen governance rules (GitHub is canonical, no force-push to `main`, secrets never in Git, etc.), and the `rtk`-prefix convention for all commands are all sound governance independent of the false assumption.

**Only** the RAE-M365-Platform-specific references (the "Known Archives for Recovery" section in `PROJECT_BASELINE.md`; the diagram node, hierarchy row, and §6 in `REPOSITORY_CONVERGENCE_MODEL.md`) need to be removed. Neither document should be discarded wholesale.

### `EA_RECOVERY_GAP_MATRIX.md` and `EA_LEGACY_RECOVERY_MANIFEST.md`

The **comparison of claimed EA-3A–3E artifacts against what actually exists in GitHub remains valid and useful** — it is a legitimate audit of gaps in the canonical repository (missing SharePoint schemas, missing Taxonomy v2 structure, missing extended registry fields, missing governance policies, etc.), independent of whether a recovery source exists.

What is **no longer valid** is the recommendation to *recover* these artifacts from the WORK PC — there is no such source, so there is nothing to import. **The gaps themselves are real; only the proposed remedy is wrong.** The correct reframing is:

> The audited gaps (missing SharePoint foundation, Taxonomy v2 structure, extended metadata fields, governance policies, etc.) are confirmed real and remain open. Since no recovery source exists or ever existed, these gaps cannot be closed by importing pre-existing artifacts. The only path forward is **forward implementation**: design and author each missing artifact directly against the canonical repository, using Architecture Decision Records where the gap matrix/manifest already flagged architectural implications (e.g., Taxonomy v2 scope, extended registry schema, PnP vs. TypeScript tooling choice).

### `EA_WORK_PC_RECOVERY_RUNBOOK.md`

This document is **entirely STALE_ASSUMPTION**. It is a runbook for a recovery process for which no valid source has ever existed. There is no partial-correction path: every step depends on `G:\ProjectAI\RAE-M365-Platform` being accessible, and it is not (and never was, as far as any accessible machine is concerned). The document should be retired in favor of forward-implementation planning derived from the (corrected) Gap Matrix and Legacy Recovery Manifest, with its original content preserved in Git history as a record of the corrected assumption.

---

## Secret Scan

A secret scan (`password|secret|token|api_key|PRIVATE_KEY|BEGIN RSA|BEGIN OPENSSH|client_secret|tenant_id`) was run against this review document. No matches were found — this document contains no credentials, tokens, or other sensitive material.
