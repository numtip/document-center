# RAE Document Center — Admin Request Package

**Entry point for Maejo University Microsoft 365 administrators.**

---

## Purpose

This package formally requests MJU M365 tenant administration to provision the foundation infrastructure for the **RAE Document Center** — a governed document platform for the Office of Agricultural Research and Extension (สำนักวิจัยและส่งเสริมวิชาการการเกษตร).

**Architecture principle:** *Build Less. Govern More.* — Microsoft 365 is the platform.

---

## Current Status

| Item | Status |
|------|--------|
| Tenant verification | ✅ Complete |
| Architecture design (EA-3/EA-4) | ✅ Complete |
| Provisioning preflight | ✅ Complete |
| Admin provisioning request | ➞ **PENDING — AWAITING ADMIN ACTION** (FALLBACK PATH) — see EA-3S readiness closure |
| User authorization | ❌ NOT YET AUTHORIZED |

|| Existing-site reuse (EA-3S) | ✅ COMPLETE — `EXISTING_SITE_READY_FOR_PROVISIONING` (see `docs/m365/m365-existing-site-reuse-readiness-closure.md`) |

All tenant capability checks (SharePoint, Lists, Power Automate) have been verified using the operational account `researchmju@mju.ac.th`. Site creation and Term Store access require MJU admin privileges.

---

## What MJU Admin Must Do

1. **Create the SharePoint Team Site** — RAE Document Center at `/sites/RAEDocumentCenter`
2. **Create/associate the Microsoft 365 Group** — RAE Document Center (Private)
3. **Set site privacy** — Private
4. **Assign initial RAE site owner** — designated individual from RAE
5. **Confirm site URL and Group creation**
6. **Advise on Term Store request process** — for future Managed Metadata (RAE-Tags term set)
7. **Return the handoff checklist** with confirmed values

**Estimated admin effort:** < 1 hour for site creation and group setup.

Detailed request: [`RAE_DOCUMENT_CENTER_SITE_PROVISIONING_REQUEST.md`](./RAE_DOCUMENT_CENTER_SITE_PROVISIONING_REQUEST.md)

---

## What RAE Will Do Afterwards

Once the site foundation is confirmed, the RAE implementation team will:

| Activity | Estimated Effort | Dependency |
|----------|-----------------|------------|
| Create 6 document libraries | Est. 30 min | Site created |
| Create 17 site columns + 5 content types | Est. 1 hour | Site created |
| Create RAE Document Registry Microsoft List with 22 columns | Est. 30 min | Site created |
| Configure permissions (9 SharePoint groups) | Est. 1 hour | Category Owners confirmed |
| Configure versioning on all libraries | Est. 15 min | Libraries created |
| Configure public sharing per approved policy | Est. 15 min | External sharing confirmed |
| Implement Power Automate workflows (EA-5) | Future phase | All above complete |

RAE does NOT require MJU admin to perform any of these activities.

---

## Files in This Package

| File | Purpose |
|------|---------|
| `README.md` | Entry point (this file) |
| `RAE_DOCUMENT_CENTER_SITE_PROVISIONING_REQUEST.md` | Formal technical admin request |
| `RAE_DOCUMENT_CENTER_BUSINESS_JUSTIFICATION.md` | Institutional context and rationale |
| `RAE_DOCUMENT_CENTER_SECURITY_SCOPE.md` | Security and governance documentation |
| `RAE_DOCUMENT_CENTER_ADMIN_HANDOFF_CHECKLIST.md` | Info to return after site creation |
| `EA_ARCHITECTURE_FREEZE_AND_COMMIT_SCOPE.md` | Architecture baseline and freeze scope |

---

## Required Admin Response

After completing provisioning, please return:

1. **Confirmed Site URL** — e.g., `https://maejo365.sharepoint.com/sites/RAEDocumentCenter`
2. **Confirmed Site ID** — if readily available (GUID)
3. **Confirmed M365 Group name and email alias**
4. **Assigned Initial Owner** — name and email
5. **Term Store contact/process** — who to contact for future Managed Metadata setup
6. **Site-level external sharing setting** — any restrictions specific to this site

Use the handoff checklist: [`RAE_DOCUMENT_CENTER_ADMIN_HANDOFF_CHECKLIST.md`](./RAE_DOCUMENT_CENTER_ADMIN_HANDOFF_CHECKLIST.md)

---

## Next Architecture Phase

After site foundation is confirmed and handoff checklist is returned:

| Phase | Description | Trigger |
|-------|-------------|---------|
| **EA-3 Implementation** | Provision libraries, columns, content types | Site confirmed + user authorization |
| **EA-4 Implementation** | Provision RAE Document Registry List | Site confirmed + user authorization |
| **EA-5 Implementation** | Power Automate workflows | EA-3/EA-4 complete + user authorization |

---

## Contact

**Department:** สำนักวิจัยและส่งเสริมวิชาการการเกษตร (RAE) — Office of Agricultural Research and Extension  
**Operational Account:** researchmju@mju.ac.th  
**Designated Site Owner:** [TBD — to be confirmed by RAE and assigned by MJU admin]

---

*End of Package Entry Point — Generated 2026-07-14*
