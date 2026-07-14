# Implementation Exception — Existing RAE Site Deployment Boundary

**Phase:** EA-3S — Existing Site Boundary Exception & Reuse Readiness Closure  
**Tenant:** Maejo University (MJU) — maejo365.sharepoint.com  
**Date:** 2026-07-14  
**Status:** `APPROVED_FOR_EXISTING_SITE_IMPLEMENTATION`

---

## Decision

```
REUSE_EXISTING_SITE_WITH_CONDITIONS
```

After successful resolution of all five EA-3R reuse conditions:

| Condition | Result |
|-----------|--------|
| C1 — Permission Group Creation | ✅ GROUP_CREATION_CONFIRMED |
| C2 — Content Type Enablement | ✅ CONTENT_TYPE_CAPABILITY_CONFIRMED |
| C3 — Navigation Impact | ✅ MEDIUM_MANAGEABLE |
| C4 — Site Ownership | ✅ OWNERSHIP_CLEAR |
| C5 — External Sharing | ✅ EXTERNAL_SHARING_CONFIRMED |

## Exception

| Field | Value |
|-------|-------|
| **Exception Type** | `ARCHITECTURE_IMPLEMENTATION_EXCEPTION` |
| **Exception Scope** | SharePoint site boundary / deployment topology |
| **Original Deployment Assumption** | Dedicated RAE Document Center Team Site at `/sites/RAEDocumentCenter` |
| **Implemented Deployment Boundary** | Existing RAE Team Site `https://maejo365.sharepoint.com/sites/msteams_54adc4` |

## Rationale

1. **Existing official RAE site** — the site `สำนักวิจัยฯ` (`/sites/msteams_54adc4`) is the verified organizational SharePoint site for สำนักวิจัยและส่งเสริมวิชาการการเกษตร
2. **Private Team Site with M365 Group** — aligns with approved privacy model; 23 members already managed through directory
3. **Current account is Site Admin** — `researchmju@mju.ac.th` has `IsSiteAdmin = true`, enabling self-service provisioning without MJU tenant admin
4. **No naming collisions** — all 6 canonical library names (Administration, FinanceProcurement, PlanningPolicy, AcademicServices, Research, SOPManuals) are available; no conflicting resources exist
5. **Microsoft Lists creation confirmed** — Lists can be created within the existing site; `RAE Document Registry` name has no collision
6. **Site Pages capability confirmed** — New > Page available; Site Page content type exists
7. **Library-level permission isolation proven** — Documents library already demonstrates unique permissions (`HasUniqueRoleAssignments = true`)
8. **Permission group creation confirmed** — Site Admin successfully created and deleted a test group via REST API
9. **Content type management confirmed** — Advanced settings expose "Allow management of content types" with Yes/No toggle
10. **Lower MJU Admin dependency** — provisioning can proceed without tenant admin site creation request
11. **Faster implementation** — no waiting for admin site provisioning

## Canonical Primitives NOT Affected

This exception explicitly does NOT alter:

| Primitive | Status |
|-----------|--------|
| `DocumentID` — `RAE-NNNNN` | ✅ Unchanged |
| `Status` — 7 values (draft, review, approved, published, current, obsolete, archived) | ✅ Unchanged |
| `Visibility` — 4 values (public, internal, restricted, private) | ✅ Unchanged |
| Six-library model | ✅ Unchanged |
| Registry schema (22 columns) | ✅ Unchanged |
| Content types (5 site content types) | ✅ Unchanged |
| Lifecycle model | ✅ Unchanged |
| Export contract (JSON) | ✅ Unchanged |
| Migration semantics | ✅ Unchanged |
| Permission groups design (RAE-DC-*) | ✅ Unchanged |
| Public eligibility rules (Visibility=public AND Status IN approved, published, current) | ✅ Unchanged |

---

## Risks and Compensating Controls

| Risk | Severity | Compensating Control |
|------|----------|---------------------|
| Navigation clutter from 6 new libraries + 1 list + 1 page | MEDIUM | Libraries hidden from navigation; single "RAE Document Center" top-level entry pointing to landing page |
| Permission complexity with M365 Group + unique library groups | MEDIUM | Clear documentation of group hierarchy; separate RAE-DC-* groups with explicit permission levels |
| Existing user confusion from new restricted resources | MEDIUM | Communication plan for 23 existing members; welcome message on landing page |
| Ownership continuity if researchmju leaves | MEDIUM | Formal owner assignment during EA-5 provisioning; document fallback path |
| External sharing governance — Anonymous links | MEDIUM | Public delivery controlled by Registry metadata + workflow validation; not by default |
| Site lifecycle tied to existing RAE site | LOW | Existing site is the official RAE site; no planned deprecation |

---

## Rollback Boundary

| Action | Rollback Method | Reversibility |
|--------|----------------|---------------|
| Library creation | Delete library (30-day retention) | ✅ Reversible |
| Site columns | Delete or deactivate column | ✅ Reversible |
| Content types | Delete content type | ✅ Reversible |
| Permission groups | Delete SharePoint group | ✅ Reversible |
| Registry List | Delete Microsoft List | ✅ Reversible |
| Site Page | Delete page | ✅ Reversible |
| Site permissions | Remove unique permissions, inherit from parent | ✅ Reversible |

If existing-site reuse fails critically, the dedicated-site fallback path (`/sites/RAEDocumentCenter`) in the Admin Provisioning Request Package remains fully viable.

---

## Governance Implications

- **Library-level governance** remains intact — versioning, content types, columns, indexing all configurable per library
- **Permission governance** uses dedicated RAE-DC-* groups with explicit permission levels — no M365 Group member automatically gains Document Center access
- **Public document delivery** uses the same link-creation workflow as the dedicated-site model
- **Power Automate governance** operates at library/list scope — no cross-site-automation concerns
- **Managed Metadata** (Term Store) dependency is unchanged — remains ADMIN_REQUIRED; "Single line of text" fallback continues

---

## Approval Status

| Stage | Status | Date |
|-------|--------|------|
| EA-3R Audit | REUSE_EXISTING_SITE_WITH_CONDITIONS | 2026-07-14 |
| EA-3S Condition 1 — Group Creation | GROUP_CREATION_CONFIRMED | 2026-07-14 |
| EA-3S Condition 2 — Content Type | CONTENT_TYPE_CAPABILITY_CONFIRMED | 2026-07-14 |
| EA-3S Condition 3 — Navigation | MEDIUM_MANAGEABLE | 2026-07-14 |
| EA-3S Condition 4 — Ownership | OWNERSHIP_CLEAR | 2026-07-14 |
| EA-3S Condition 5 — External Sharing | EXTERNAL_SHARING_CONFIRMED | 2026-07-14 |
| **Final Implementation Readiness** | **APPROVED_FOR_EXISTING_SITE_IMPLEMENTATION** | **2026-07-14** |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `docs/m365/m365-existing-rae-site-reuse-audit.md` | EA-3R reuse capability audit |
| `docs/m365/m365-existing-site-capability-matrix.csv` | EA-3R capability evidence matrix |
| `docs/m365/m365-existing-site-reuse-readiness-closure.md` | EA-3S readiness closure report |
| `docs/m365/m365-sharepoint-registry-provisioning-plan.md` | Provisioning plan (updated for existing site) |
| `docs/m365/m365-provisioning-manifest.csv` | Resource manifest (updated for existing site) |
| `docs/m365/m365-provisioning-authorization-gate.md` | Authorization gate (updated for existing site) |
