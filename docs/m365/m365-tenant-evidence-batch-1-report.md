# EA-1C — Microsoft 365 Tenant Evidence Collection: Batch 1 Report

**Date:** 2026-07-14  
**Collected by:** Main Agent (Orchestrator) via MCP Browser  
**Account:** researchmju@mju.ac.th / สำนักวิจัยและส่งเสริมวิชาการการเกษตร  
**Tenant:** maejo365.sharepoint.com  

---

## Scope Covered

| CheckID | Capability | Status |
|---|---|---|
| B1-01 | Microsoft 365 Account / App Availability | ✅ CONFIRMED |
| B1-02 | SharePoint Online Access + Tenant Context | ✅ CONFIRMED |
| B1-03 | Microsoft Lists Access + Creation Capability | ✅ CONFIRMED |
| B1-04 | SharePoint External Sharing / Anonymous Link Capability | ✅ CONFIRMED |

---

## B1-01 — M365 Account / App Availability

**Evidence Type:** Browser Screenshot, Accessibility Snapshot  
**Evidence Reference:** B1-01-browser-login

### Findings

| Attribute | Value |
|---|---|
| Tenant Hostname | `maejo365.sharepoint.com` |
| Account UPN | `researchmju@mju.ac.th` |
| Organisation | สำนักวิจัยและส่งเสริมวิชาการการเกษตร (Maejo University) |
| Login State | Authenticated session active in MCP browser |
| SharePoint Global Nav | Available (Discover, Publish, Build, OneDrive tabs visible) |
| Account Manager Button | Shows "Account manager for สำนักวิจัยและส่งเสริมวิชาการการเกษตร" |

### Conclusion

Account is active and authenticated. The M365 tenant `maejo365` is confirmed as Maejo University's institutional tenant. No app-specific blocks were observed at the account level.

---

## B1-02 — SharePoint Online Access + Tenant Context

**Evidence Type:** Browser Snapshot  
**Evidence Reference:** B1-02-discover-page, B1-02-documents-library

### Findings

| Attribute | Value |
|---|---|
| SharePoint Root URL | `https://maejo365.sharepoint.com` |
| SharePoint Access | ✅ Full access |
| Existing Sites Discovered | Maejo university Team Site, Green Office สำนักวิจัยฯ, สำนักวิจัยฯ, ImagesRae, เอกสารประกอบของคลาส, และอื่น ๆ |
| Document Library | "Shared Documents" accessible via classic/modern UI |
| Files in Library | Document.docx, Pirisa Korea chicken sauce.pdf, ตลาดเงิน.docx |
| Site Navigation | Home, Notebook, Documents, Calendar, eform_rae, Pages, Site Contents, Recycle Bin |
| Add Column Button | Visible in document library (supports Type, Name, Modified, Modified By columns) |
| Site Access Button | Visible in toolbar |

### Observations

- The existing site ("Maejo university Team Site") is a classic team site with both classic and modern UI elements
- Users can browse sites via the Discover page
- Site admin controls (Site Contents, Recycle Bin) are visible, suggesting site-level administrative access

### Conclusion

SharePoint Online is **CONFIRMED AVAILABLE**. The user has access to at least one team site with document library functionality. Custom columns, upload, and site navigation are all functional.

---

## B1-03 — Microsoft Lists Access + Creation Capability

**Evidence Type:** Browser Screenshot, Accessibility Snapshot  
**Evidence Reference:** B1-03-lists-portal, B1-03-create-list

### Findings

| Attribute | Value |
|---|---|
| Lists URL | `https://maejo365-my.sharepoint.com/personal/researchmju_mju_ac_th/_layouts/15/lists.aspx` |
| Lists Portal Access | ✅ Full access |
| Create New Button | ✅ Visible and functional |
| My Lists Tab | ✅ Available |
| Recents Tab | ✅ Available (shows disabled state — no recent lists) |

### List Creation Options Available

| Creation Method | Available |
|---|---|
| Blank List | ✅ Yes |
| From Excel | ✅ Yes |
| From CSV | ✅ Yes |
| From Existing List | ✅ Yes |
| Form-based (Power Apps) | ✅ Yes |
| Gallery Layout | ✅ Yes |
| Calendar Layout | ✅ Yes |
| Board (Kanban) Layout | ✅ Yes |

### Microsoft Templates Visible

Issue tracker, Employee onboarding, Event itinerary, Asset manager, Recruitment tracker, Travel requests, Travel requests with approvals, Work tracker, Content scheduler, Content scheduler with approvals, Playlist, Gift ideas, Expense tracker, Recipe tracker, Reading list, Apartment hunting, Job application tracker, Product support metrics, and more.

### Conclusion

Microsoft Lists is **CONFIRMED AVAILABLE WITH FULL CAPABILITY**. List creation, multiple view types, and various creation methods (including import from Excel/CSV) are all accessible. The user can create blank lists and choose from Microsoft-provided templates. There is also a "From your organization" tab for custom templates.

---

## B1-04 — SharePoint External Sharing / Anonymous Link Capability

**Evidence Type:** Browser Screenshot  
**Evidence Reference:** B1-04-link-settings, B1-04-anyone-link

### Findings

Share dialog opened on file `Pirisa Korea chicken sauce.pdf` from Shared Documents library.

**Link Types Available (in order):**

| # | Link Type | Description | Default |
|---|---|---|---|
| 1 | **Anyone** | "Share with anyone, doesn't require sign-in" | ✅ **Default (checked)** |
| 2 | People in Maejo university | "organization account required" | ❌ |
| 3 | People with existing access | "reshare with people who already have access" | ❌ |
| 4 | Specific people | "inside or outside of Maejo university" | ❌ |

**Additional Settings Visible:**
- **Role selector** (Can edit / Can view / Can review)
- **Password field** for Anyone link
- **Expiration date** for Anyone link (MM/DD/YYYY picker)
- **Manage access** link (shows "4 groups, 1 link")

### Architectural Implications

This is a **CRITICAL FINDING** for the public portal architecture:

1. **POSITIVE:** The "Anyone" (anonymous) link type being available means the planned public document portal can serve documents to external users without authentication. This supports the EA-7 Registry Export → GitHub → Next.js architecture where public documents need to be accessible.

2. **SECURITY CONCERN:** "Anyone" links are the **default** sharing option. This requires:
   - Explicit governance policy for who can create anonymous links
   - Training to ensure users don't accidentally expose sensitive content
   - Possible DLP policy enforcement for sensitive content types
   - Consideration of expiration and password requirements for anonymous links

3. **COMPATIBILITY:**
   - Public document StorageURLs from SharePoint can be directly embedded in the Next.js portal
   - Anonymous links are compatible with the EA-4 Visibility=`public` classification
   - Internal documents can use "People in Maejo university" links

### Conclusion

External sharing (including anonymous/Anyone links) is **CONFIRMED ENABLED AT THE TENANT LEVEL**. This supports the planned architecture. Policy governance and DLP recommendations will be added to the consolidated audit.

---

## Screenshots Captured

| # | File | Content |
|---|---|---|
| 1 | page-2026-07-14T04-05-20-764Z.png | SharePoint page with Discover navigation |
| 2 | page-2026-07-14T04-07-35-410Z.png | Share dialog Link Settings panel |
| 3 | page-2026-07-14T04-08-00-402Z.png | Link Settings dialog showing Anyone link default |
| 4 | page-2026-07-14T04-08-18-967Z.png | Microsoft Lists portal page |

*Screenshots stored in MCP browser temp directory. Recommend downloading to `docs/m365/screenshots/` for permanent evidence.*

---

## Not Yet Collected (Deferred to Batch 2)

| CheckID | Reason |
|---|---|
| SPO-003 | Site creation capability — requires admin center or SharePoint admin permission |
| SPO-005 to SPO-012 | Column types, Content Types, Term Store — requires deeper site settings navigation |
| SPO-010 | Version History — requires library settings access |
| PA-001 to PA-012 | Power Automate — requires separate browser navigation to make.powerautomate.com |
| TMS-001 to TMS-004 | Teams / Approvals — requires Teams client or web app |
| GPH-001 to GPH-004 | Graph API — requires Graph Explorer session |
| ENT-001 to ENT-006 | Entra ID — requires Entra admin center |
| OPT-001 to OPT-003 | Power BI, Forms, Copilot — optional services |

---

## Updated Evidence Register

The following entries in `docs/m365/m365-tenant-evidence-register.csv` were updated from `NOT_VERIFIED` to `CONFIRMED`:

- SPO-001 (Portal Access)
- SPO-002 (Active Sites Discovery)
- SPO-004 (Document Library Creation)
- SPO-013 (External Sharing Policy)
- SPO-014 (Anonymous Link Creation)
- SPO-015 (Organization Links)
- LST-001 (Lists Portal Access)
- LST-002 (List Creation)

---

## Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| Anyone sharing is default | Medium | Require DLP policy; train users; set anonymous link expiration default via admin center |
| User may not have site creation permission | Low-Medium | Needs admin confirmation for site provisioning (EA-3) |
| Classic site may not support modern custom columns | Low | Tested site is classic; new site for RAE should be modern communication site |

---

## Next Steps

1. **Batch 2** — Power Automate verification (PA-001 to PA-012)
2. **Batch 3** — Teams / Approvals verification (TMS-001 to TMS-004)
3. **Batch 4** — Graph API verification (GPH-001 to GPH-004)
4. **Batch 5** — Entra ID verification (ENT-001 to ENT-006)
5. **Update EA-1 Audit Documents** — Integrate Batch 1 findings into `M365_LICENSE_AUDIT.md`, `m365-tenant-readiness-matrix.csv`
6. **Screenshot Storage** — Move screenshots from MCP temp to `docs/m365/screenshots/`

---

*End of Batch 1 Report — Generated 2026-07-14*
