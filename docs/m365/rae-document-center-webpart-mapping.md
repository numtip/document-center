# RAE Document Center — SharePoint Modern Web Part Mapping

**Baseline:** RAE Document Center Visual Baseline V2 (FROZEN)  
**Target:** SharePoint Modern Page on existing RAE site (`/sites/msteams_54adc4`)  
**Date:** 2026-07-15  
**EA-3R context:** Existing site reuse — do not create new site; do not duplicate site chrome  

---

## 1. Design Principles

| Principle | Application |
|-----------|-------------|
| **Native first** | Use out-of-the-box SharePoint web parts before considering configuration or custom development |
| **No site chrome duplication** | The existing RAE site header, navigation, and footer are provided by SharePoint — the page must not replicate them |
| **Six libraries unchanged** | Content maps to the six existing canonical libraries; no library is renamed or added |
| **RAE-only scope** | No Green Office, Learning Center, or unrelated portal content |

---

## 2. Section Mapping

### 2.1 Compact RAE Page Identity

| Property | Value |
|----------|-------|
| **V2 Section** | Compact RAE Page Identity |
| **UX Purpose** | Brand the page as the RAE Document Center within the parent site chrome |
| **Preferred SharePoint Implementation** | Title Area web part (page title + description) or Text web part with image/icon |
| **Data Source** | Static page metadata |
| **Native / Approximation / Future Enhancement** | Native |
| **Key Constraint** | Existing site chrome is displayed by SharePoint; only page-level identity is added. Do not duplicate the site title. |

### 2.2 Search-first Hero

| Property | Value |
|----------|-------|
| **V2 Section** | Search-first Hero |
| **UX Purpose** | Primary document discovery entry point; prominent search with quick-link chips |
| **Preferred SharePoint Implementation** | **Candidate A:** Native Search Box web part (Microsoft Search entry point) with promoted results or search scope configuration. **Candidate B:** Text/Image web part with descriptive content plus Search Box below. |
| **Data Source** | SharePoint Search index (scoped to RAE Document Center libraries) |
| **Native / Approximation / Future Enhancement** | Approximation |
| **Key Constraint** | The Stitch search box includes custom styling, placeholder text, and quick-link chips that native Search Box cannot replicate identically. Native Search Box renders with organization search settings. See §3 (Search Decision) for details. |

### 2.3 Quick Access

| Property | Value |
|----------|-------|
| **V2 Section** | Quick Access |
| **UX Purpose** | Horizontal bar of shortcut links: Search All, Latest Updates, Documents to Review, RAE Document Registry |
| **Preferred SharePoint Implementation** | Quick Links web part (Compact or Button layout) |
| **Data Source** | Static links with icon selection |
| **Native / Approximation / Future Enhancement** | Native |
| **Key Constraint** | Quick Links supports configurable icons but limited layout flexibility. Button layout with icons is the closest match. The "Documents to Review" link targets a library view with filtered documents. |

### 2.4 Six Document Domains

| Property | Value |
|----------|-------|
| **V2 Section** | Six Document Domains |
| **UX Purpose** | Category card grid: Administration, FinanceProcurement, PlanningPolicy, AcademicServices, Research, SOPManuals |
| **Preferred SharePoint Implementation** | Quick Links web part (Grid layout) with icon, title, description per link |
| **Data Source** | Static links to library views (one per category) |
| **Native / Approximation / Future Enhancement** | Approximation |
| **Key Constraint** | Stitch uses rich cards with icon, title, description, hover state, and "view documents" CTA. Quick Links Grid provides icon + title, but description text may be limited. Visual fidelity must be assessed during implementation. See §4 (Gap Summary). |

### 2.5 Recent Documents

| Property | Value |
|----------|-------|
| **V2 Section** | Recent Documents |
| **UX Purpose** | Tabular list of recently updated documents with DocumentID, title, category, date, status |
| **Preferred SharePoint Implementation** | Highlighted Content web part (filtered by modified date, scoped to the six RAE libraries) |
| **Data Source** | SharePoint search results from the six document libraries |
| **Native / Approximation / Future Enhancement** | Native |
| **Key Constraint** | Highlighted Content renders document cards/links, not a custom table. Column layout and status badge rendering are controlled by the web part, not custom-styled. Alternatively, a List web part pointing to a consolidated view. |

### 2.6 Governance / Trust

| Property | Value |
|----------|-------|
| **V2 Section** | Governance / Trust |
| **UX Purpose** | Three trust indicators: assigned owner, version history, standardized classification |
| **Preferred SharePoint Implementation** | Text web part with inline icons, or three-column Text layout |
| **Data Source** | Static content |
| **Native / Approximation / Future Enhancement** | Native |
| **Key Constraint** | This section is purely informational. Text web part with icon characters or emoji can approximate the three trust circles. Quick Links with icon layout is an alternative if a more visually structured layout is preferred. |

### 2.7 Compact Support Area

| Property | Value |
|----------|-------|
| **V2 Section** | Compact Support Area |
| **UX Purpose** | Footer area: "Need help?" with support buttons and RAE copyright |
| **Preferred SharePoint Implementation** | Text web part + Quick Links for buttons, or a single Text web part with inline links |
| **Data Source** | Static content |
| **Native / Approximation / Future Enhancement** | Native |
| **Key Constraint** | Site footer is provided by SharePoint chrome. This section adds page-level support content above the site footer. Keep concise to avoid redundancy. |

---

## 3. Search Implementation Decision

### 3.1 The Challenge

The Stitch V2 design places a prominent, styled search box in the hero section with:
- Custom placeholder text
- Quick-link chips (Latest Documents, Forms, Manuals, Research)
- RAE green hero background

The native SharePoint Search Box web part cannot replicate this exact appearance. It renders the organization's Microsoft Search configuration.

### 3.2 Options

#### Option A: Native Search Box + Descriptive Content (Recommended)

| Aspect | Detail |
|--------|--------|
| **Approach** | Use SharePoint Search Box web part placed within a hero-like section using a Text web part above it |
| **Search scope** | Configure search to scope results to the six RAE Document Center libraries via search configuration |
| **Quick links** | Place Quick Links web part below search box for the chips |
| **Fidelity gap** | Search box styling is SharePoint-native (not custom green rounded-full). Hero background uses section formatting (solid color available). |
| **Custom code** | None required |

#### Option B: Search Results Page Scoping

| Aspect | Detail |
|--------|--------|
| **Approach** | Same as Option A. Additionally configure the search results page (`/Search/Pages/results.aspx`) to default to RAE Document Center scope with relevant refiners (category, library) |
| **Custom code** | None required. Search configuration at site or site-collection level. |

#### Option C: SPFx Custom Search (Future Only)

| Aspect | Detail |
|--------|--------|
| **Approach** | SPFx React web part replicating the exact Stitch search appearance |
| **Trigger** | Only if Options A/B prove insufficient after implementation QA |
| **Custom code** | SPFx solution development, deployment, and maintenance required |

### 3.3 Recommendation

**Proceed with Option A (Native Search Box) first.** This is the lowest-customization path. The hero section can use section background formatting for the green band. Quick-link chips are implemented via Quick Links web part below the search box. If visual fidelity is deemed insufficient after implementation, escalate to Option B (search scoping configuration) before considering Option C (SPFx).

### 3.4 Search Scope Configuration

Search results must be scoped to the six RAE Document Center libraries only:
- Administration
- FinanceProcurement
- PlanningPolicy
- AcademicServices
- Research
- SOPManuals

This ensures no unrelated content (Green Office, other portal sites) appears in Document Center search results. Exact configuration depends on SharePoint search schema and result source configuration.

---

## 4. Implementation Gaps / Decisions Before Build

### 4.1 Search Fidelity

| Item | Status |
|------|--------|
| **Gap** | Native Search Box web part does not match Stitch's custom-styled search appearance |
| **Decision needed** | Is native styling sufficient, or does the visual gap justify SPFx custom search? |
| **Principle** | Proceed with native. Re-evaluate only if QA finds the experience unsatisfactory. |

### 4.2 Quick Links Card Fidelity (Six Domains)

| Item | Status |
|------|--------|
| **Gap** | Stitch shows rich cards (icon, title, description, hover effect, CTA). Quick Links Grid supports icon + title but limited description display |
| **Decision needed** | Is the native Quick Links Grid acceptable, or does the missing description per domain card justify a custom layout? |
| **Principle** | Accept Quick Links approximation. Descriptions can be added as tooltips or via additional Text web part above the grid if needed. |

### 4.3 Recent Documents Data Source

| Item | Status |
|------|--------|
| **Gap** | Highlighted Content web part queries SharePoint search. Column rendering (DocumentID, status badge) is limited by web part capabilities |
| **Decision needed** | Use Highlighted Content (search-based) or a List web part pointing to a consolidated view? |
| **Principle** | Start with Highlighted Content. If column/badge fidelity is insufficient, consider a List web part with a SharePoint view that aggregates across libraries. |

### 4.4 Governance Shortcut Permissions

| Item | Status |
|------|--------|
| **Gap** | The Quick Access link "Documents to Review" targets a view with filtered documents. Whether the user sees any documents depends on their permissions |
| **Decision needed** | Should the link be visible to all users, or conditionally shown based on permission? |
| **Principle** | Quick Links is visible to all. The target view handles permission-based visibility automatically. No conditional web part is needed. |

### 4.5 Search Box Quick-Link Chips

| Item | Status |
|------|--------|
| **Gap** | Stitch shows inline chips (Latest Documents, Forms, Manuals, Research) below the search box. Native Search Box does not support this |
| **Decision needed** | Use a separate Quick Links web part below the Search Box for the chips |
| **Principle** | This is achievable without SPFx. Quick Links web part placed below the Search Box web part in the same section. |

### 4.6 SPFx Threshold

| Item | Status |
|------|--------|
| **Decision** | SPFx is NOT justified for any identified gap at this time |
| **Rationale** | All sections have a native or configuration-based implementation path. The visual differences are acceptable approximations. Custom development should only be pursued if post-implementation QA identifies a critical experience blocker. |
| **Revisit condition** | If user testing shows that the search experience or domain card layout causes confusion or reduced discoverability, consider SPFx for those specific components only. |

---

## 5. Related Documents

| Document | Path |
|----------|------|
| Visual Baseline V2 | `docs/design/rae-document-center/RAE_DOCUMENT_CENTER_VISUAL_BASELINE.md` |
| SharePoint Site Design | `docs/m365/sharepoint-site-design.md` |
| Existing Site Reuse Audit | `docs/m365/m365-existing-rae-site-reuse-audit.md` |
| Site Reuse Closure | `docs/m365/m365-existing-site-reuse-readiness-closure.md` |
| EA Forward Implementation Baseline | `docs/architecture/EA_FORWARD_IMPLEMENTATION_BASELINE.md` |
| Session Handoff | `docs/m365/SESSION-HANDOFF.md` |
