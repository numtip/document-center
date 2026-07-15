# RAE Document Center SharePoint Implementation Plan

**Version:** 1.0  
**Status:** READY FOR TENANT EXECUTION  
**Date:** 2026-07-15  
**Baseline:** RAE Document Center Visual Baseline V2 (FROZEN)  
**Web Part Mapping:** `docs/m365/rae-document-center-webpart-mapping.md`  

---

## 1. Purpose

This plan translates the frozen Stitch V2 visual baseline into a SharePoint Modern Page on the approved existing RAE SharePoint Site (`/sites/msteams_54adc4`).

| Constraint | Status |
|---|---|
| No new site creation | The existing RAE site is reused (EA-3S approved) |
| No architecture redesign | EA-3/EA-4 canonical architecture remains frozen |
| No content-scope expansion | RAE institutional documents only |
| Excluded portals | Green Office, Learning Center, and unrelated portal content are excluded |

---

## 2. Implementation Target

| Property | Value |
|---|---|
| **Existing RAE SharePoint Site** | `https://maejo365.sharepoint.com/sites/msteams_54adc4` |
| **Site type** | Private Team Site (M365 Group-connected) |
| **Site Admin** | `researchmju@mju.ac.th` |
| **Target page** | Existing `RAE-Document-Center.aspx` (already published in Site Pages) |
| **Page URL** | To be confirmed at runtime via Site Pages library |
| **Navigation** | No new navigation entry (Teams-connected site constraint — deferred) |

**Do not** create a new site. **Do not** create a new page path unless the existing page needs replacement.

---

## 3. Page Composition

The page sections appear in the following order, matching the frozen Stitch V2 layout:

### 3.1 Compact RAE Page Identity

| Aspect | Specification |
|---|---|
| **Purpose** | Brand the page as RAE Document Center within SharePoint site chrome |
| **SharePoint section** | One-column full-width section at top of page |
| **Web part type** | Title Area web part (recommended) — or Text web part as fallback |
| **Content** | Page title: "RAE Document Center" / "ศูนย์กลางเอกสาร RAE" Subtitle or description: brief Thai/English line |
| **Source data** | Static text |
| **Visual fidelity** | Native — SharePoint Title Area provides its own styling |
| **Constraint** | Do not duplicate the site header. The existing RAE site chrome already displays the site title. This section is page-level branding only. |

### 3.2 Search-first Hero

| Aspect | Specification |
|---|---|
| **Purpose** | Primary discovery entry point — prominent search with green hero background and quick-link chips below |
| **SharePoint section** | One-column full-width section; apply solid background color |
| **Web part stack** | (1) Text web part — headline + description. (2) Search Box web part. (3) Quick Links web part — for quick-link chips. |
| **Content** | Headline: "ค้นหาและเข้าถึงเอกสารสำคัญ จากศูนย์กลางเดียว" Subtitle: "เข้าถึงเอกสาร...” Quick Links: เอกสารล่าสุด, แบบฟอร์ม, คู่มือ, งานวิจัย |
| **Source data** | Static text (headline/description); SharePoint Search Box (search); static links (chips) |
| **Visual fidelity** | Approximation — SharePoint Search Box renders with organization's Microsoft Search styling, not the Stitch custom styling. Section background formatting provides the green band. |
| **Constraint** | Search Box web part is native SharePoint. Quick Link chips are a separate web part below the search box, not inline as in the Stitch design. |

### 3.3 Quick Access

| Aspect | Specification |
|---|---|
| **Purpose** | Horizontal bar of four shortcut links for rapid navigation |
| **SharePoint section** | One-column section |
| **Web part type** | Quick Links (Button or Compact layout) |
| **Content** | ค้นหาเอกสารทั้งหมด, เอกสารที่อัปเดตล่าสุด, เอกสารที่ต้องทบทวน, RAE Document Registry — each with icon |
| **Source data** | Static links to library views / registry list |
| **Visual fidelity** | Native — Quick Links Button layout is a natural fit |
| **Constraint** | "Documents to Review" target view filters by permission; empty results for users without review items is acceptable |

### 3.4 Six Document Domains

| Aspect | Specification |
|---|---|
| **Purpose** | Category card grid for the six canonical document domains |
| **SharePoint section** | One-column section |
| **Web part type** | Quick Links (Grid layout) |
| **Content** | 6 links: Administration, FinanceProcurement, PlanningPolicy, AcademicServices, Research, SOPManuals — each with icon, title, short description |
| **Source data** | Static links to library views (one per library) |
| **Visual fidelity** | Approximation — Quick Links Grid supports icon + title per card. Descriptions are limited compared to the Stitch rich cards. Native spacing and proportions differ. |
| **Constraint** | Do not change library names. Do not add or remove domains. |

### 3.5 Recent Documents

| Aspect | Specification |
|---|---|
| **Purpose** | Tabular list of recently updated documents: DocumentID, title, category, date, status |
| **SharePoint section** | One-column section |
| **Web part type** | Highlighted Content (recommended Phase 1 default) — see §7 |
| **Content** | Filter by modified date desc; scope to the 6 RAE libraries |
| **Source data** | SharePoint search index (Highlighted Content); or aggregated list view (List web part fallback) |
| **Visual fidelity** | Approximation — Highlighted Content renders document cards, not the Stitch custom table with status badges. Column layout is controlled by web part, not custom-styled. |
| **Constraint** | Cross-library aggregation is the key requirement. Highlighted Content handles this natively via search. |

### 3.6 Governance / Trust

| Aspect | Specification |
|---|---|
| **Purpose** | Three trust indicators: assigned owner, version history, standardized classification |
| **SharePoint section** | One-column section |
| **Web part type** | Text web part with inline icons or Quick Links (Icon layout) |
| **Content** | Three items: มีผู้รับผิดชอบเอกสาร (verified owner), มีประวัติเวอร์ชัน (version history), มีมาตรฐานการจัดหมวดหมู่ (standardized classification) |
| **Source data** | Static content |
| **Visual fidelity** | Native — Text web part with icons. The Stitch circular icon containers are approximated by standard SharePoint icon rendering. |
| **Constraint** | Purely informational. No dynamic data source needed. |

### 3.7 Compact Support Area

| Aspect | Specification |
|---|---|
| **Purpose** | Footer-area support: "Need help?" buttons and RAE copyright |
| **SharePoint section** | One-column section |
| **Web part type** | Text web part (description + inline links) or Text + Quick Links |
| **Content** | "ต้องการความช่วยเหลือเกี่ยวกับเอกสาร?" with ติดต่อผู้ดูแลระบบ, คู่มือการใช้งาน links; RAE copyright |
| **Source data** | Static content |
| **Visual fidelity** | Native |
| **Constraint** | Site footer is rendered by SharePoint chrome. This section adds page-level support content above the site footer. Keep concise. |

---

## 4. Exact Web Part Plan

| Section | Web Part | Layout | Native / Approximation |
|---|---|---|---|
| Compact RAE Page Identity | Title Area | — | Native |
| Search-first Hero | Text + Search Box + Quick Links | One-column | Approximation |
| Quick Access | Quick Links | Button / Compact | Native |
| Six Document Domains | Quick Links | Grid | Approximation |
| Recent Documents | Highlighted Content | List/Card | Approximation |
| Governance / Trust | Text | Inline | Native |
| Compact Support Area | Text + Quick Links | Inline | Native |

**No SPFx web parts are recommended for Phase 1.** All sections have a native or configuration-based implementation path.

---

## 5. Six Canonical Domain Mapping

| Library (English) | Display Title (TH) | Short Description | Quick Links Target |
|---|---|---|---|
| `Administration` | งานบริหารและธุรการ | เอกสารที่เกี่ยวข้องกับการบริหารงานทั่วไป ระเบียบ ประกาศ และหนังสือสั่งการ | Link to Administration library view |
| `FinanceProcurement` | งานคลังและพัสดุ | แบบฟอร์มการเบิกจ่าย งบประมาณ การจัดซื้อจัดจ้าง และเอกสารการเงินต่างๆ | Link to FinanceProcurement library view |
| `PlanningPolicy` | งานนโยบายและแผน | แผนปฏิบัติราชการ รายงานผลการดำเนินงาน และเอกสารเชิงนโยบาย | Link to PlanningPolicy library view |
| `AcademicServices` | งานบริการวิชาการ | เอกสารประกอบการจัดอบรม โครงการบริการวิชาการ และฐานข้อมูลผู้เชี่ยวชาญ | Link to AcademicServices library view |
| `Research` | งานวิจัย | คู่มือทุนวิจัย แบบฟอร์มเสนอโครงการ และรายงานผลการวิจัย | Link to Research library view |
| `SOPManuals` | คู่มือปฏิบัติงาน | มาตรฐานการปฏิบัติงาน (SOP) คู่มือการใช้ระบบ และแนวทางการทำงาน | Link to SOPManuals library view |

**Rules:**
- Library names are NOT renamed — they match the six existing canonical libraries.
- Display titles (Thai) are separate from library names; they are set via column defaults or display settings.
- Each Quick Links target links to the corresponding library's default view or a dedicated category-scoped view.
- Do not create additional libraries for Green Office, Learning Center, or any other scope.

---

## 6. Search Capability Decision

### Evaluation

The frozen Stitch V2 baseline calls for a prominent search-first hero. The search must surface only relevant RAE Document Center content and must not show results from Green Office, Learning Center, or other unrelated sites.

### Option A — Native SharePoint Search Box (Recommended Phase 1)

| Aspect | Detail |
|---|---|
| **Approach** | Place the native Search Box web part in the hero section. Uses the organization's Microsoft Search configuration. |
| **Search scope** | Configure the search results page to scope results to the six RAE libraries. |
| **Custom code** | None. |
| **Fidelity** | Approximates the Stitch search bar visually. The SharePoint Search Box is styled by the organization's search settings, not by custom CSS. |

### Option B — Scoped Search Results Experience

| Aspect | Detail |
|---|---|
| **Approach** | Same as Option A, plus configure the search results page (`/Search/Pages/results.aspx`) with a custom result source limited to the RAE Document Center libraries. Add refiners for category, library, and document status. |
| **Custom code** | None. Result sources and refiners are SharePoint configuration. |
| **Prerequisite** | Requires site collection or search service application access. |

### Option C — SPFx Custom Search (Future Only)

| Aspect | Detail |
|---|---|
| **Approach** | SPFx React web part with custom search UI matching Stitch exactly. |
| **Trigger** | Only if Options A/B fail acceptance criteria after implementation QA. |

### Recommendation: Phase 1 = Option A + prepare Option B

**Phase 1:** Deploy native Search Box web part. Accept the visual approximation. Verify search scope targets RAE libraries.

**Phase 1.5 (if scoping is insufficient):** Configure custom result source scoped to the six RAE libraries (Option B). This requires search administration access but is still zero-code.

**Phase 2 (only if proven necessary):** SPFx custom search.

### Acceptance Criteria

| Criterion | How to Verify |
|---|---|
| Searches across relevant RAE Document Center content | Search known document titles; confirm results appear |
| No unrelated portal results (Green Office, Learning Center, etc.) | Search known terms from excluded portals; confirm zero results |
| Usable Thai keyword search | Search in Thai; confirm results are relevant |
| Clear result destination | Click a result; confirm it opens the document or detail page |
| Permission-aware | Log in as a user without access to restricted documents; confirm those documents do not appear |
| No custom code | Confirm only Search Box web part + search configuration are used |

---

## 7. Recent Documents Decision

### Options Compared

| Criterion | Highlighted Content (Recommended) | List Web Part |
|---|---|---|
| **Cross-library aggregation** | Native — queries SharePoint search across the entire site. Scopes to specific libraries via search query filter. | Fallback — requires a single list or view; does not aggregate across separate libraries unless a custom rollup view exists. |
| **Metadata visibility** | Displays selected document metadata columns (title, modified date, etc.). Non-searchable metadata may be limited. | Full column-level control from the target list/view. Can show DocumentID, category, status badges if the view defines them. |
| **Filtering** | Supports date-range and search-query filters. Easy to show "most recent N documents." | Relies on list view filters (standard SharePoint filtering). |
| **Configuration complexity** | Low — add web part, configure query scope, pick template. | Low — point to an existing list or aggregated view. Buildup requires creating the aggregated view first. |
| **Visual fidelity** | Cards or list template — not a custom table. Status badges are web part-controlled. | Closer to the Stitch table layout if the target view includes all desired columns. |
| **Permission behavior** | Search-results based; user sees only what they have permission to read. | List-view based; user sees only what they have permission to read. Both are equivalent. |

### Recommendation: Start with Highlighted Content

**Phase 1 default:** Highlighted Content web part, scoped to the six RAE libraries, sorted by modified date descending. Accept the card/list layout and column limitations.

**Fallback:** If the Highlighted Content layout does not display sufficient metadata (DocumentID, category, status), switch to a List web part pointing to a SharePoint view that aggregates content across the six libraries. Note that creating an aggregated cross-library view may require a Search Results web part — which Option A already provides.

**Do not** redesign the registry architecture to create a single flat library to simplify the recent-documents display.

---

## 8. Quick Access and Permission Behavior

| Link | Thai Label | Target | Audience | Permission Behavior |
|---|---|---|---|---|
| ค้นหาเอกสารทั้งหมด | All Documents Search | Search results page scoped to RAE libraries | General staff | Available to all. Target page respects user permissions. |
| เอกสารที่อัปเดตล่าสุด | Latest Updated Documents | Highlighted Content or library view sorted by modified date desc | General staff | Available to all. Results are permission-filtered by SharePoint. |
| เอกสารที่ต้องทบทวน | Documents to Review | Library view filtered by review-required status | Governance / owner-oriented | Links display for all users. Target view may show empty results for users without review assignments. This is acceptable — the page remains clean. |
| RAE Document Registry | Registry List | RAE Document Registry Microsoft List | Governance / owner-oriented | Links display for all users. List permissions control whether the user sees data or an access-denied message. |

**Phase 1 behavior:** All four Quick Access links are visible to all page visitors. Permission control is handled at the target (library view, list, search results), not at the link level. If UX QA finds that empty results for general staff are confusing, consider hiding "Documents to Review" in a future iteration. No new role system is designed — existing SharePoint permissions handle enforcement.

---

## 9. Visual Fidelity Rules

### Must Preserve

| Element | Requirement |
|---|---|
| RAE green identity | `#005C3B` primary green used for page section backgrounds and accents where SharePoint theme permits |
| Sarabun typography | Apply via SharePoint theme if possible; otherwise accept the site default font as an approximation |
| Search-first hierarchy | Hero section with search and quick links must be the first visual element below the page title |
| Six-domain 3×2 conceptual grid | Desktop layout should present the six domains in a 3-column x 2-row arrangement via Quick Links Grid |
| Restrained gold accents | `#D8A01A` gold for subtle highlights where SharePoint theme permits |
| White / ivory surfaces | Section background formatting should use light/white theme colors |
| Calm enterprise spacing | Generous vertical spacing between sections; avoid cramped layouts |
| Recent-document list orientation | A list or card layout showing recently modified documents |
| Governance trust section | Three-column layout: assigned owner, version history, standardized classification |

### Acceptable Approximation

| Element | Rationale |
|---|---|
| Native SharePoint spacing | SharePoint section and web part spacing defaults are used; they will differ from Stitch's 4px baseline |
| Native Quick Links card proportions | Quick Links Grid renders its own icon/title layout; card proportions are controlled by the web part, not by Stitch |
| Native search styling | The native Search Box web part renders with organization search settings |
| Minor typography differences | Sarabun may not be the active SharePoint theme font; SharePoint's theme font is acceptable |

### Not Acceptable

| Element | Rationale |
|---|---|
| Architecture changes for visual parity | Do not rename or restructure the six-domain model to match Stitch pixel positions |
| Custom code for pixel-perfect matching | SPFx is not justified for visual differences alone |
| Duplicate SharePoint site/app headers | The existing site chrome must not be duplicated within the page |
| Mixed portal content | Green Office, Learning Center, or unrelated content must not appear |
| Replacing canonical six-domain structure | The six-library structure is frozen EA architecture |

---

## 10. Execution Sequence

### Phase 0 — Preflight and Evidence Capture

| Step | Action | Est. Time |
|---|---|---|
| 0.1 | Authenticate to M365 tenant as `researchmju@mju.ac.th` (or `prinya@office365.mju.ac.th`) | 5 min |
| 0.2 | Verify site access: navigate to existing RAE site (`/sites/msteams_54adc4`) | 2 min |
| 0.3 | Locate existing `RAE-Document-Center.aspx` in Site Pages library | 3 min |
| 0.4 | Take baseline screenshot of the existing page | 3 min |

### Phase 1 — Backup and Baseline Capture

| Step | Action | Est. Time |
|---|---|---|
| 1.1 | Check the existing page's version history. Note the current published version. | 3 min |
| 1.2 | If version history is available, the current version serves as the rollback point. | 1 min |
| 1.3 | Take a full-page screenshot of the existing published page. | 3 min |

### Phase 2 — Page Structure

| Step | Action | Est. Time |
|---|---|---|
| 2.1 | Edit `RAE-Document-Center.aspx` in SharePoint Page Editor. | 2 min |
| 2.2 | Add 7 one-column sections in the correct order (see §3). | 5 min |
| 2.3 | Apply section backgrounds: green to the hero section, white/ivory to others. | 5 min |
| 2.4 | Save as draft. | 1 min |

### Phase 3 — Identity and Hero

| Step | Action | Est. Time |
|---|---|---|
| 3.1 | Add Title Area web part to Section 1. Set title and description. | 3 min |
| 3.2 | In Section 2: add Text web part with hero headline and subtitle (Thai). | 3 min |
| 3.3 | Add Search Box web part below the Text web part in Section 2. | 2 min |
| 3.4 | Add Quick Links web part below Search Box for the four quick-link chips. | 3 min |
| 3.5 | Save as draft. | 1 min |

### Phase 4 — Quick Access and Six Domains

| Step | Action | Est. Time |
|---|---|---|
| 4.1 | In Section 3: add Quick Links web part. Set layout to Button or Compact. Add four links with icons. | 5 min |
| 4.2 | In Section 4: add Quick Links web part. Set layout to Grid. Add six domain links with icons and display titles. | 8 min |
| 4.3 | Configure each domain link to point to its corresponding library view. | 5 min |
| 4.4 | Save as draft. | 1 min |

### Phase 5 — Recent Documents

| Step | Action | Est. Time |
|---|---|---|
| 5.1 | In Section 5: add Highlighted Content web part. | 3 min |
| 5.2 | Configure query: scope to the six RAE libraries, sort by modified date desc. | 5 min |
| 5.3 | Select list layout. Configure visible columns. | 3 min |
| 5.4 | If Highlighted Content is insufficient, replace with List web part pointing to a SharePoint search results page or a cross-library view. | 10 min |
| 5.5 | Save as draft. | 1 min |

### Phase 6 — Governance and Support Area

| Step | Action | Est. Time |
|---|---|---|
| 6.1 | In Section 6: add Text web part. Add three trust items with inline icons (using Unicode or SharePoint icon characters). | 5 min |
| 6.2 | In Section 7: add Text web part with support text and inline links. Alternatively add Text + Quick Links combination. | 5 min |
| 6.3 | Verify no section is missing. Verify section order matches §3. | 3 min |
| 6.4 | Save as draft. | 1 min |

### Phase 7 — Responsive / Permission / Search QA

| Step | Action | Est. Time |
|---|---|---|
| 7.1 | Preview page at mobile, tablet, and desktop widths. Verify layout is acceptable. | 5 min |
| 7.2 | Verify all Quick Links targets resolve correctly. | 5 min |
| 7.3 | Verify Search Box renders and search returns results from RAE libraries. | 3 min |
| 7.4 | Verify permission-sensitive items (recent documents, registry link) behave correctly for a test user. | 5 min |
| 7.5 | Verify no SharePoint chrome duplication (page title, site header). | 2 min |
| 7.6 | Compare visual against frozen `screen.png`. Note acceptable approximations. | 5 min |

### Phase 8 — Final Evidence and Handoff

| Step | Action | Est. Time |
|---|---|---|
| 8.1 | Take full-page screenshot of the completed draft. | 3 min |
| 8.2 | Verify rollback readiness (current published version preserved). | 2 min |
| 8.3 | Publish the page. | 1 min |
| 8.4 | Take post-publish screenshot. | 3 min |
| 8.5 | Return the execution checklist with evidence. | 5 min |

---

## 11. Validation Checklist

### Architecture

- [ ] Existing site reused (no new site created)
- [ ] Six canonical libraries unchanged (not renamed, not removed, not added)
- [ ] RAE-only scope preserved (no Green Office, Learning Center, or unrelated content)
- [ ] EA-3/EA-4 frozen architecture not modified

### Visual

- [ ] Compared against frozen `screen.png`
- [ ] No duplicate SharePoint site header within the page
- [ ] Section order matches Stitch V2 (Identity → Hero → Quick Access → Domains → Recent → Governance → Support)
- [ ] Mobile layout is acceptable (no broken overlap, readable text)
- [ ] RAE green identity is present

### Functional

- [ ] All Quick Links targets are valid (no broken URLs)
- [ ] Permissions respected (restricted documents not visible to unauthorized users)
- [ ] Recent documents load correctly and show content the user can access
- [ ] Search scope is configured for RAE libraries only
- [ ] Search returns Thai keyword results

### Governance

- [ ] No restricted content exposed to unauthorized users
- [ ] No Green Office or Learning Center content visible or searchable
- [ ] Registry list link respects existing list permissions

---

## 12. Rollback Plan

| Priority | Strategy | Steps |
|---|---|---|
| **Primary** | Restore previous published version | Before editing, note the current published version number. If the new page fails, use SharePoint page version history to restore the previous published version. |
| **Secondary** | Republish the draft as unpublished | If version history is unavailable, save the original page content (screenshot + text copy) before editing. Recreate if needed. |
| **Do NOT** | Delete libraries, lists, or existing production resources | No production resources are modified by this plan. Page changes are confined to the single `RAE-Document-Center.aspx` page. |

**Rollback is simple because:**
- Only one SharePoint page is modified.
- No libraries, lists, columns, content types, permissions, or workflows are created or altered.
- SharePoint page version history provides native rollback.
- Baseline screenshots are captured before changes begin.

---

## 13. SPFx Escalation Criteria

**SPFx is NOT approved by default.** All Phase 1 sections have native or configuration-based implementation paths. SPFx may be reconsidered only if post-native implementation QA proves a **material functional gap**:

| Gap | SPFx Justified? | Condition |
|---|---|---|
| Search cannot be scoped correctly | Yes | If Result Source configuration cannot limit results to the six RAE libraries |
| Required information architecture cannot be represented | Yes | If Quick Links Grid or Highlighted Content cannot represent the six domains or recent documents in a usable way |
| Accessibility requirement cannot be met | Yes | If native web parts fail WCAG requirements and no configuration workaround exists |
| Critical UX function is impossible natively | Yes | If a defined user workflow required by the frozen baseline cannot be implemented with native web parts |
| Pixel-perfect parity with Stitch | **No** | Visual differences alone are not sufficient justification |

**Escalation process:** Document the gap with evidence (screenshot + description). If the gap is one of the four criteria above, submit an ADR proposing the specific SPFx component. SPFx development is a separate workstream — it does not block Phase 1 implementation.

---

## 14. Related Documents

| Document | Path |
|---|---|
| Visual Baseline V2 | `docs/design/rae-document-center/RAE_DOCUMENT_CENTER_VISUAL_BASELINE.md` |
| Web Part Mapping | `docs/m365/rae-document-center-webpart-mapping.md` |
| Execution Checklist | `docs/m365/rae-document-center-sharepoint-execution-checklist.md` |
| Session Handoff | `docs/m365/SESSION-HANDOFF.md` |
| SharePoint Site Design | `docs/m365/sharepoint-site-design.md` |
| Existing Site Reuse Audit | `docs/m365/m365-existing-rae-site-reuse-audit.md` |
| EA-3S Reuse Closure | `docs/m365/m365-existing-site-reuse-readiness-closure.md` |
