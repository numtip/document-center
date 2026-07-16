# ADR-007: Migration Strategy

**Status**: Accepted  
**Date**: 2026-07-15 (retroactive)  
**Phase**: EA-6 through EA-10

---

## Context

627 READY documents needed migration from WTMS staging to SharePoint with metadata and Registry sync. Risk of data loss, duplicates, and untested scale required a phased approach with evidence at each gate.

## Decision

**Phased controlled migration** with idempotent resume:

| Phase | Count | Purpose |
|-------|------:|---------|
| EA-6A pilot | 6 | Prove upload + metadata + Registry |
| EA-7A expanded | 25 | Prove batch orchestration |
| EA-9 scale | 100 | Prove sustained throughput |
| EA-10 remaining | 496 | Complete corpus |

**Technical approach**:

- Method: `playwright-rest` (persistent browser profile + REST API)
- Preflight: SHA-256, source file, library assignment
- Resume: skip documents in results CSV
- Registry: AUTO_UPSERT after each batch
- Evidence: per-phase results CSV, state JSON/JSONL

**Forbidden**: `--force` re-upload, WTMS recrawl, architecture redesign.

## Consequences

**Positive**:

- 496/496 EA-10 docs migrated; 627 total; 0 failures
- Resume proven (Wave 1 Batch 1: 10 skipped)
- Reconciliation artifacts enable audit
- Fast mode reduced orchestration overhead (~4.3 sec/doc)

**Negative**:

- Browser profile lock requires single worker
- REST pagination bug discovered at scale (fixed)
- Long runtime for full corpus (~45 min fast mode)
- Migration tools remain in `.migration/` (not production runtime)

## Alternatives Considered

| Alternative | Rejected because |
|-------------|------------------|
| Big-bang 627 upload | No resume; high failure blast radius |
| SharePoint Migration Tool | No custom metadata mapping; WTMS source unavailable |
| Manual upload | Not scalable; no audit trail |
| Graph API app-only | Tenant app registration not available in timeframe |
| Power Automate upload | File size limits; complex error handling |
