# Owner Remediation Report — Phase 5A.8

**Project:** RAE Document Center  
**Phase:** 5A.8 — Owner Remediation Pack  
**Date:** 2026-06-18  
**Source:** `owner-assignment-proposal.csv` (40 proposals from Phase 5A.7)

---

## Summary

Reviewed all 40 owner proposals and created a confirmation checklist with recommended final owners. No final owners were fabricated — low-confidence proposals remain TBD.

| Metric | Count |
|--------|-------|
| Total proposals reviewed | 40 |
| High-confidence (copied to recommendedFinalOwner) | 32 |
| Medium-confidence (needs-confirmation) | 5 |
| Low-confidence (unresolved, kept TBD) | 3 |
| Owners confirmed (final) | 0 (all await human sign-off) |

---

## Owner Decision Status Distribution

| Status | Count | Description |
|--------|-------|-------------|
| proposed | 32 | High-confidence proposal copied to recommendedFinalOwner |
| needs-confirmation | 5 | Medium-confidence — needs human unit confirmation |
| unresolved | 3 | Low-confidence — kept as TBD per rules |
| **Total** | **40** | |

---

## High-Confidence Proposals (32)

All 32 high-confidence proposals recommend `rae-dc-admin-owners` as the owner group. These are standard HR/Admin responsibilities where the taxonomy-defined owner group is the clear fit.

| Document Group | Count | Recommended Owner | Reason |
|----------------|-------|-------------------|--------|
| Training forms (0001-0003, 0009-0011) | 6 | rae-dc-admin-owners | HR/Admin training coordinator |
| Attendance forms (0004, 0004A, 0013) | 3 | rae-dc-admin-owners | HR/timekeeping |
| Leave forms (0014-0017) | 4 | rae-dc-admin-owners | HR leave responsibility |
| Resignation forms (0018-0019) | 2 | rae-dc-admin-owners | HR resignation processing |
| Travel/training reports (0008, 0021) | 2 | rae-dc-admin-owners | Admin/HR travel approval |
| Contractor forms (0012) | 1 | rae-dc-admin-owners | HR contractor management |
| Correspondence/seal (0025-0026) | 2 | rae-dc-admin-owners | Admin/records/communications |
| Sample letters (0027-0031) | 5 | rae-dc-admin-owners | Admin/records management |
| Leave regulation (0033) | 1 | rae-dc-admin-owners | HR/admin policy |
| Vehicle forms (0035-0041) | 7 | rae-dc-admin-owners | Fleet/admin responsibility |

---

## Medium-Confidence Proposals (5)

These proposals need human confirmation because the owner unit is ambiguous.

| Document | Title | Issue | Question for Human |
|----------|-------|-------|-------------------|
| RAE-DC-0007 | Smart Card application | IT or HR? | Which unit owns smart card issuance? |
| RAE-DC-0020 | Contractor resignation | HR sub-unit? | Which HR sub-unit handles contractor resignations? |
| RAE-DC-0022 | Working hours policy พ.ศ.2564 | Admin or governance? | Is this admin/HR or a governance-level policy? |
| RAE-DC-0032 | International travel procedure | Admin or rewrite owner? | Does rewrite need a separate content owner? |

---

## Low-Confidence Proposals (3) — Unresolved

These proposals remain TBD per mandatory rules. No final owner was fabricated.

| Document | Title | Issue | Reason for Low Confidence |
|----------|-------|-------|---------------------------|
| RAE-DC-0023 | หลักเกณฑ์ประเมินผล ปีงบประมาณ 2565 | HR or research unit? | Assessment criteria could be owned by HR (performance) or research unit (academic assessment) |
| RAE-DC-0024 | หลักเกณฑ์ประเมินพฤติกรรม ปีงบประมาณ 2565 | HR or research unit? | Same uncertainty as RAE-DC-0023 |
| RAE-DC-0034 | สิทธิการลาของบุคลากรประเภทต่างๆ | May not be a document | Links to PHP page — may not be a downloadable document at all |

---

## Owner Proposal Methodology

Each owner proposal was based on:

1. **Document title analysis** — What function does the document serve?
2. **Taxonomy owner group** — The `admin` category maps to `rae-dc-admin-owners` group
3. **Legacy source context** — All documents came from the admin tab of the legacy website
4. **Standard organizational patterns** — HR forms → HR, vehicle forms → fleet/admin, etc.

**No owners were fabricated.** Low-confidence proposals explicitly remain TBD until human review.

---

## Impact on Registry

| Metric | Before (5A.7) | After (5A.8) |
|--------|---------------|--------------|
| Owners assigned (real) | 0 | 0 (all await confirmation) |
| Owner proposals (high confidence) | 32 | 32 (copied to recommendedFinalOwner) |
| Owner proposals (medium confidence) | 5 | 5 (flagged needs-confirmation) |
| Owner proposals (low confidence) | 3 | 3 (kept TBD — unresolved) |
| Owners fabricated | 0 | 0 |

---

## Next Steps for Human Reviewer

1. **Review 32 high-confidence proposals** — Confirm or override `rae-dc-admin-owners` for each
2. **Resolve 5 medium-confidence proposals** — Answer the specific questions in the table above
3. **Investigate 3 low-confidence proposals** — Determine if RAE-DC-0023/0024 are HR or research; confirm if RAE-DC-0034 is a real document
4. **Update `document-registry.remediated.json`** — Replace `owner: TBD` with confirmed owners

---

## Related Documents

- [OWNER_CONFIRMATION_CHECKLIST.csv](./OWNER_CONFIRMATION_CHECKLIST.csv) — Full checklist with 40 rows
- [owner-assignment-proposal.csv](./owner-assignment-proposal.csv) — Original proposals from Phase 5A.7
- [taxonomy.json](./taxonomy.json) — Category owner group definitions
