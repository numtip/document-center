# RAE Document Center — SharePoint Execution Checklist

**Plan:** `docs/m365/rae-document-center-sharepoint-implementation-plan.md`  
**Target:** Single-worker tenant execution session  
**Date:** 2026-07-15

---

## Preflight

- [ ] Authenticated as `researchmju@mju.ac.th` (site admin)
- [ ] Existing RAE site accessible at `/sites/msteams_54adc4`
- [ ] `RAE-Document-Center.aspx` located in Site Pages library
- [ ] Frozen Stitch reference files available locally: `screen.png`, `DESIGN.md`, `code.html`
- [ ] Web part mapping document open for reference

## Before Page Change

- [ ] Current page version noted (for rollback)
- [ ] Baseline full-page screenshot taken
- [ ] Page version history checked (rollback capability confirmed)

## Page Build

- [ ] Seven one-column sections added in correct order (Identity → Hero → Quick Access → Domains → Recent → Governance → Support)
- [ ] Section colors applied (green hero background; white/ivory for others)
- [ ] Section 1: Title Area web part configured (page title + description)
- [ ] Section 2: Text + Search Box + Quick Links (hero headline, search, chips)
- [ ] Section 3: Quick Links Button layout — four links with icons
- [ ] Section 4: Quick Links Grid layout — six domain links with icons and display names
- [ ] Section 5: Highlighted Content web part — scoped to six RAE libraries, sorted by modified date
- [ ] Section 6: Text web part — three trust items with inline icons
- [ ] Section 7: Text + optionally Quick Links — support text, links, copyright
- [ ] Page saved as draft after each section group

## Search

- [ ] Search Box web part renders in hero section
- [ ] Search results scope targets RAE libraries (configure result source if needed)
- [ ] Thai keyword search returns relevant results
- [ ] No unrelated portal content in search results

## Permission

- [ ] Quick Links targets resolve correctly for authenticated user
- [ ] Recent documents respect user permissions (restricted docs hidden)
- [ ] Registry list link respects list permissions
- [ ] "Documents to Review" shows empty state gracefully for non-reviewers

## Visual QA

- [ ] Compared against frozen `screen.png`
- [ ] RAE green identity visible (hero background, accents)
- [ ] No duplicate SharePoint site header within page
- [ ] Section order matches frozen design
- [ ] Mobile preview: layout is readable, no broken overlap
- [ ] Quick Links Grid shows six domains in acceptable layout

## Functional QA

- [ ] All Quick Links targets resolve (no broken URLs)
- [ ] Search Box returns results for known document titles
- [ ] Recent documents list populates with accessible content
- [ ] Governance trust section renders legibly

## Rollback Readiness

- [ ] Previous published page version documented
- [ ] Baseline screenshot saved
- [ ] Rollback procedure understood: restore via version history

## Evidence Capture

- [ ] Pre-change screenshot saved
- [ ] Draft page screenshot taken
- [ ] Post-publish screenshot taken
- [ ] Any visual gaps documented with notes

## Final Handoff

- [ ] Page published
- [ ] Checklist completed and returned with screenshots
- [ ] Visual gap notes recorded for future iteration (if any)
- [ ] Implementation plan referenced in session handoff

---

*End of checklist — complete each item during the tenant execution session.*
