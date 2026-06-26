# UI Blueprint — RAE Document Center

**Project:** RAE Document Center  
**Phase:** 4A — UI Blueprint Only  
**Status:** Blueprint locked for Phase 4B implementation  
**Last updated:** 2026-06-17

---

## 1. Design Goal

The RAE Document Center is a **static document registry** — not file storage. Users discover metadata here and download files from OneDrive via share links.

| Goal | Requirement |
|------|-------------|
| **Fast** | Static HTML/CSS; minimal JS; no server round-trips for browse/search |
| **Mobile-first** | Layout and touch targets designed for phone first, enhanced for tablet/desktop |
| **Beautiful institutional UI** | Premium Maejo/RAE look: trustworthy, clean, professional |
| **3-click discovery** | Any published document reachable in ≤ 3 clicks from `/documents` |
| **Static export compatible** | All routes pre-renderable; no database, CMS, upload, or admin panel |

### 3-click paths (examples)

```
/documents → category card → document card → detail/download     (3 clicks)
/documents → search results → document detail                    (2 clicks)
/documents → featured doc → download                             (2 clicks)
```

### Explicit non-goals (Phase 4A–4B)

- No file upload
- No admin panel or inline editing
- No authentication layer in v1 (visibility badges are informational; OneDrive enforces access)
- No serving binaries from the static site

---

## 2. Route Plan

All routes live under `/documents` to allow co-existence with other Maejo/RAE site pages.

| Route | Purpose | Render strategy |
|-------|---------|-----------------|
| `/documents` | Home hub: search entry, KPIs, categories, featured/recent list | SSG — static at build time |
| `/documents/category/[slug]` | Category-scoped browse (`slug` = taxonomy `id`) | SSG — one page per enabled category |
| `/documents/search` | Full search + filter UI with client-side query | SSG shell + client-side filter |
| `/documents/document/[id]` | Single document detail, metadata, download CTA | SSG — one page per listable document |

### Route decisions

1. **`/documents` as hub** — Single entry point linked from main site nav; avoids scattering document UX across root routes.
2. **`[slug]` matches taxonomy `id`** — e.g. `/documents/category/research`, not folder names. Display `name_th` from `taxonomy.json`.
3. **`/documents/search` separate from hub** — Keeps home page lightweight; search page loads filter state from URL query params (`?q=&category=&file_type=&status=&visibility=`).
4. **`[id]` uses registry id** — e.g. `/documents/document/RAE-DC-0001`. Stable, shareable URLs.
5. **No `/documents/[...catchAll]`** — Fixed route set keeps static export predictable.

### Redirect / error behavior

| Case | Behavior |
|------|----------|
| Unknown category slug | 404 page with link back to `/documents` |
| Unknown document id | 404 page with search prompt |
| Disabled taxonomy category | 404 or “ไม่เปิดใช้งาน” message |
| Draft / archived / restricted (default listing rules) | Not linked from hub; direct URL shows detail with appropriate warning (see §6) |

---

## 3. Page Structure: `/documents`

Vertical single-column on mobile; two-column sections on `lg+` where noted.

```
┌─────────────────────────────────────────────┐
│  SITE HEADER (existing Maejo/RAE chrome)    │
├─────────────────────────────────────────────┤
│  HERO                                       │
│  Title + subtitle + primary search box      │
├─────────────────────────────────────────────┤
│  KPI SUMMARY (4 stat cards, horizontal      │
│  scroll on mobile)                          │
├─────────────────────────────────────────────┤
│  CATEGORY CHIPS / CARDS (6 enabled)         │
├─────────────────────────────────────────────┤
│  FEATURED / RECENT DOCUMENTS                │
│  (6–8 cards, updated_date desc, current)    │
├─────────────────────────────────────────────┤
│  ALL DOCUMENTS LIST                         │
│  (paginated or “ดูทั้งหมด” → search)        │
├─────────────────────────────────────────────┤
│  HELP / CONTACT                             │
├─────────────────────────────────────────────┤
│  SITE FOOTER                                │
└─────────────────────────────────────────────┘
```

### Section specs

#### Hero

- **Headline (TH):** ศูนย์เอกสาร RAE  
- **Subhead (TH):** ค้นหา ดาวน์โหลด และอ้างอิงเอกสารอย่างเป็นทางการ — ไฟล์จัดเก็บบน OneDrive  
- **Search box:** Large input + submit; `action="/documents/search"` method GET, param `q`
- **Secondary link:** “ดูตามหมวดหมู่” scroll-to or anchor to category section

#### KPI summary

Computed at build time from filtered registry (default: `status=current`, `visibility=public|internal`):

| KPI | Source |
|-----|--------|
| เอกสารทั้งหมด | Count of listable documents |
| หมวดหมู่ | Count of `enabled` taxonomy categories |
| อัปเดตล่าสุด | Max `updated_date` across listable docs |
| ประเภทไฟล์ | Count of distinct `file_type` values |

#### Category chips / cards

- One card per enabled taxonomy category, sorted by `sort_order`
- Show: `name_th`, `name_en` (subtitle), document count, short `description_th` (truncated 2 lines)
- Tap → `/documents/category/[id]`
- Visual: green left border accent, white card, subtle shadow

#### Featured / recent documents

- Top 6–8 documents by `updated_date` desc
- Only `status=current`, `visibility=public|internal`
- Uses Document Card spec (§4)
- Link: “ดูเอกสารทั้งหมด” → `/documents/search`

#### Document list (compact)

- Optional below fold: simple table/list (title, category, date) for remaining listable docs
- Mobile: stack rows; desktop: table with sortable headers (static default sort only in v1)

#### Help / Contact

- **TH copy:** หากไม่พบเอกสารหรือลิงก์เสีย กรุณาติดต่อเจ้าของเอกสารหรือผู้ดูแลระบบ  
- Placeholder contact: unit email / extension (TBD — not blocking blueprint)
- Link to governance note: files are not stored on this website

---

## 4. Document Card Spec

Used on hub, category, search, related-documents sections.

### Layout (mobile card)

```
┌──────────────────────────────────────┐
│ [file_type icon]  [visibility badge] │
│ Title (2 lines max, bold)            │
│ [category pill]  [status badge]      │
│ Owner · v1.0 · 17 ม.ย. 2569          │
│ [tag] [tag] [tag]                    │
│ [  ดาวน์โหลด  ]  [ รายละเอียด → ]   │
└──────────────────────────────────────┘
```

### Field mapping

| UI element | Data source | Display rule |
|------------|-------------|--------------|
| Title | `document.title` | Line-clamp 2; link to detail page |
| Category | `taxonomy.categories[].name_th` via `document.category` | Pill/chip; links to category page |
| Owner | `document.owner` | Truncate long emails; show role if not email |
| File type | `document.file_type` | Uppercase badge or icon (`PDF`, `DOCX`) |
| Updated date | `document.updated_date` | Thai Buddhist era format: `DD MMM YYYY` (TH locale) |
| Version | `document.version` | Prefix `v` e.g. `v1.0` |
| Visibility badge | `document.visibility` | See badge table below |
| Status badge | `document.status` | See badge table below |
| Tags | `document.tags[]` | Max 3 visible + “+N”; each tag links to search `?q=tag` |
| Download button | `document.storage_url` | Primary CTA; disabled/hidden if URL missing |
| Detail link | `document.id` | Secondary → `/documents/document/[id]` |

### Badge styles

**Visibility**

| Value | Label (TH) | Color |
|-------|------------|-------|
| `public` | สาธารณะ | Green outline |
| `internal` | ภายในองค์กร | Gold/neutral outline |
| `restricted` | จำกัดสิทธิ์ | Muted gray |

**Status**

| Value | Label (TH) | Color |
|-------|------------|-------|
| `current` | ฉบับปัจจุบัน | Primary green fill |
| `obsolete` | เลิกใช้แล้ว | Amber outline |
| `archived` | เก็บถาวร | Gray outline |
| `draft` | ร่าง | Dashed neutral |

### Download button rules

- Label: `ดาวน์โหลด {file_type}` e.g. `ดาวน์โหลด PDF`
- `target="_blank"` `rel="noopener noreferrer"`
- `aria-label`: `ดาวน์โหลด {title} ฉบับ v{version} ({file_type})`
- If `storage_url` absent: show disabled button + tooltip “ลิงก์ไม่พร้อมใช้งาน”

### Card visibility in lists

Default list filter (hub, category, search):

- Include: `status=current`, `visibility=public|internal`
- Exclude: `draft`, `archived`, `restricted`, `obsolete` unless user explicitly filters

---

## 5. Search & Filter Behavior

### Search fields (client-side)

Match against (case-insensitive, Thai-aware collation preferred in Phase 4B):

| Field | Weight |
|-------|--------|
| `title` | High |
| `tags[]` | High |
| `owner` | Medium |
| `category` (resolved `name_th`, `name_en`) | Medium |
| `note` | Low |

**Phase 4B recommendation:** Use [Fuse.js](https://fusejs.io/) for fuzzy search when dataset grows (> ~100 docs). Do **not** install in Phase 4A. For small/example datasets, simple `includes()` filter is sufficient.

### Filters

| Filter | Control | Options |
|--------|---------|---------|
| Category | Dropdown / chips | Enabled taxonomy categories + “ทั้งหมด” |
| File type | Multi-select chips | Derived unique `file_type` from registry |
| Status | Multi-select | `current`, `obsolete`, `archived`, `draft` |
| Visibility | Multi-select | `public`, `internal`, `restricted` |

Default filter state on `/documents/search`: `status=current`, visibility=`public`+`internal`.

### Sorting

| Sort option | Default |
|-------------|---------|
| `updated_date` desc | **Yes (default)** |
| `updated_date` asc | Optional |
| `title` asc (Thai locale) | Optional |

### URL sync

Persist state in query string for shareable searches:

```
/documents/search?q=คู่มือ&category=manuals&file_type=pdf&status=current&visibility=public
```

### Empty state

- Icon + headline: **ไม่พบเอกสาร**
- Body: ลองเปลี่ยนคำค้นหาหรือตัวกรอง หรือเลือกจากหมวดหมู่ด้านล่าง
- Actions: Clear filters button; link to `/documents`

### No-JS fallback

Static export with client-side search means **full search requires JS**. Progressive fallback:

1. Hero search form submits GET to `/documents/search?q=...` (works without JS)
2. Build step pre-renders a **static result list** for common queries (optional Phase 4C) OR
3. No-JS `/documents/search?q=` page shows: “กรุณาเปิด JavaScript เพื่อใช้การค้นหาแบบเต็มรูปแบบ” plus links to all category pages
4. Category and document detail pages are fully usable without JS (SSG HTML)

---

## 6. Detail Page: `/documents/document/[id]`

```
┌─────────────────────────────────────────────┐
│  Breadcrumb: เอกสาร › [category] › [title]  │
├─────────────────────────────────────────────┤
│  [WARNING BANNER if obsolete/archived]      │
├─────────────────────────────────────────────┤
│  Title (h1)                                 │
│  Badges: status · visibility · file_type    │
├─────────────────────────────────────────────┤
│  PRIMARY DOWNLOAD CTA (large button)        │
├─────────────────────────────────────────────┤
│  METADATA GRID                              │
│  หมวดหมู่ · เจ้าของ · ฉบับ · อัปเดต · ID     │
├─────────────────────────────────────────────┤
│  TAGS                                       │
├─────────────────────────────────────────────┤
│  NOTE (if present)                          │
├─────────────────────────────────────────────┤
│  RELATED DOCUMENTS (same category, current) │
├─────────────────────────────────────────────┤
│  Back link → category or /documents         │
└─────────────────────────────────────────────┘
```

### Metadata grid

| Label (TH) | Field |
|------------|-------|
| รหัสเอกสาร | `id` |
| หมวดหมู่ | `taxonomy.name_th` via `category` |
| เจ้าของเอกสาร | `owner` |
| ฉบับที่ | `version` |
| สถานะ | `status` (badge) |
| การมองเห็น | `visibility` (badge) |
| ประเภทไฟล์ | `file_type` |
| วันที่ปรับปรุง | `updated_date` (formatted) |
| ที่เก็บ OneDrive | `onedrive_path` (monospace, small — path reference only) |

Do **not** expose raw `storage_url` as visible text; use download CTA only.

### Warning banners

| Condition | Banner (TH) | Style |
|-----------|-------------|-------|
| `status=obsolete` | เอกสารฉบับนี้เลิกใช้แล้ว — โปรดใช้เอกสารฉบับใหม่ตามหมายเหตุ | Amber |
| `status=archived` | เอกสารนี้ถูกเก็บถาวรและอาจไม่เป็นฉบับปัจจุบัน | Gray |
| `status=draft` | เอกสารฉบับร่าง — ยังไม่เผยแพร่อย่างเป็นทางการ | Neutral dashed |
| `visibility=restricted` | เอกสารจำกัดสิทธิ์ — การดาวน์โหลดอาจต้องใช้สิทธิ์ OneDrive | Red-neutral |
| Missing `storage_url` | ลิงก์ดาวน์โหลดไม่พร้อมใช้งาน — ติดต่อเจ้าของเอกสาร | Red outline |

### Related documents

- Same `category`, `status=current`, exclude self
- Max 4 cards, sorted by `updated_date` desc
- Section title: **เอกสารที่เกี่ยวข้อง**

---

## 7. Category Page: `/documents/category/[slug]`

```
┌─────────────────────────────────────────────┐
│  Breadcrumb: เอกสาร › [name_th]             │
├─────────────────────────────────────────────┤
│  Category title (h1): name_th               │
│  Subtitle: name_en                          │
│  description_th (full)                      │
│  Meta: N เอกสาร · owner_group               │
├─────────────────────────────────────────────┤
│  Inline search (scoped to category)         │
├─────────────────────────────────────────────┤
│  Filter bar (file_type, status, visibility) │
├─────────────────────────────────────────────┤
│  Document card grid                         │
├─────────────────────────────────────────────┤
│  RELATED CATEGORIES (adjacent sort_order)   │
└─────────────────────────────────────────────┘
```

### Data resolution

| UI element | Source |
|------------|--------|
| Title | `taxonomy.categories[].name_th` where `id === slug` |
| Subtitle | `name_en` |
| Description | `description_th` |
| Owner group | `owner_group` (display as “กลุ่มดูแล: …”) |
| Document count | Count registry docs matching `category=slug` and default list filter |
| Document list | Filtered registry docs for category |
| Related categories | ±1 `sort_order` neighbors, or all others as chips |

### Empty category

- Message: **ยังไม่มีเอกสารในหมวดหมู่นี้**
- Link back to `/documents` and sibling categories

---

## 8. Visual Direction

### Brand palette (RAE / Maejo)

| Token | Hex | Usage |
|-------|-----|-------|
| Primary Green | `#005C3B` | Headers, primary buttons, active category, links |
| Secondary Gold | `#FFDE00` | Accents, KPI highlights, focus rings (with dark outline) |
| White | `#FFFFFF` | Page background, card surface |
| Neutral 50 | `#F8F9FA` | Section alternates |
| Neutral 200 | `#E5E7EB` | Borders |
| Neutral 700 | `#374151` | Body text |
| Neutral 900 | `#111827` | Headings |

### Typography

- **Thai:** Noto Sans Thai or Sarabun (system fallback: `Sarabun, sans-serif`)
- **English:** Noto Sans or Inter for `name_en` subtitles
- Base size: 16px mobile, 18px desktop body
- Heading scale: modest (institutional, not marketing-heavy)

### Components

- **Cards:** White, `border-radius: 12px`, light shadow, green 4px left accent on hover
- **Buttons:** Primary = green fill white text; secondary = green outline
- **Chips/pills:** Rounded full, small caps for file type
- **Spacing:** Generous whitespace; 16px mobile gutter, 24px tablet, 32px desktop

### Motion

- Minimal: 150ms color/opacity transitions only
- No parallax, no auto-carousels, no heavy animation
- Respect `prefers-reduced-motion`

### Header integration

- Reuse existing Maejo/RAE site header/footer when embedded
- Document Center sub-nav highlight on `/documents/*`

---

## 9. Accessibility

| Requirement | Implementation |
|-------------|----------------|
| Keyboard search | Hero and search inputs focusable; Enter submits; Tab order logical |
| Visible focus | 2px gold (`#FFDE00`) ring + green offset; never `outline: none` without replacement |
| Semantic headings | One `h1` per page; section `h2`; card titles `h3` |
| Thai typography | `lang="th"` on document; line-height ≥ 1.6 for Thai body |
| Color contrast | WCAG AA minimum: 4.5:1 body text, 3:1 large text/UI components |
| Download labels | Descriptive `aria-label` on every download anchor (see §4) |
| Mobile touch targets | Minimum 44×44px for buttons, chips, links in card actions |
| Badges | Not color-only: always include text label |
| Skip link | “ข้ามไปเนื้อหาหลัก” to `#main-content` |
| Screen reader | Live region for search result count updates (`aria-live="polite"`) |

---

## 10. Performance

| Strategy | Detail |
|----------|--------|
| Static generation | All document and category pages pre-built at compile time |
| Client-side search | In-browser filter on JSON bundled or imported at build time; suitable for small/medium registry (< ~500 docs) |
| No database | Data from `taxonomy.json` + `document-registry.json` only |
| No server dependency | Deploy as static export (CDN, GitHub Pages, or existing static host) |
| Lighthouse target | ≥ 95 Performance, Accessibility, Best Practices, SEO |
| Avoid heavy libraries | No CMS, no chart libraries, no UI framework required beyond Tailwind (if already in stack) |
| Image budget | File-type SVG icons only; no document thumbnails in v1 |
| JS budget | Target < 50KB gzipped for search/filter bundle; defer non-critical JS |

### Build-time data flow

```
taxonomy.json ──────────┐
document-registry.json ─┼→ build script → typed data → SSG pages + search index JSON
document-registry.example.json (dev only)
```

---

## 11. Data Mapping

### Taxonomy → UI

| UI location | Taxonomy field |
|-------------|----------------|
| Category card title | `name_th` |
| Category card subtitle | `name_en` |
| Category card description | `description_th` |
| Category page URL | `/documents/category/{id}` |
| Category sort order | `sort_order` |
| Category visibility | `enabled === true` |
| Category page owner line | `owner_group` |
| Folder reference (detail path display) | `folder` (informational; matches `onedrive_path` prefix) |

### Document registry → UI

| UI location | Registry field |
|-------------|----------------|
| Card / detail title | `title` |
| Category pill | `category` → resolve via taxonomy |
| Owner line | `owner` |
| File type badge | `file_type` |
| Date display | `updated_date` |
| Version | `version` |
| Status badge | `status` |
| Visibility badge | `visibility` |
| Tag chips | `tags[]` |
| Download href | `storage_url` |
| Detail URL | `/documents/document/{id}` |
| Note block | `note` |
| Path reference | `onedrive_path` |
| Related docs query | same `category` |
| Search index | `title`, `tags`, `owner`, `category`, `note` |

### Listability matrix (default UI)

| status | visibility | Hub / category list | Search (default) | Direct URL |
|--------|------------|---------------------|------------------|------------|
| current | public | Yes | Yes | Yes |
| current | internal | Yes | Yes | Yes |
| current | restricted | No | No | Yes + warning |
| obsolete | any | No | No* | Yes + warning |
| archived | any | No | No | Yes + warning |
| draft | any | No | No | Yes + warning |

*Unless user explicitly enables status filter

### Future `document-registry.json`

Same schema as `document-registry.example.json`. Phase 4B uses example data until validation passes on production CSV-derived registry.

---

## 12. Phase 4B Handoff

Phase 4B implements the blueprint. Tasks in recommended order:

### Implementation tasks

| # | Task | Notes |
|---|------|-------|
| 1 | **Create TypeScript types** | `Category`, `Document`, `Registry`, `Taxonomy` matching locked schema |
| 2 | **Create data loader** | Import `taxonomy.json` + `document-registry.example.json`; helper to resolve category by id |
| 3 | **Create validation script** | Enforce [REGISTRY_DATA_MODEL.md](./REGISTRY_DATA_MODEL.md) rules; CI-ready |
| 4 | **Create shared UI tokens** | CSS variables for `#005C3B`, `#FFDE00`, neutrals, spacing, radii |
| 5 | **Create DocumentCard component** | Per §4 spec |
| 6 | **Create Badge components** | Status + visibility + file type |
| 7 | **Create `/documents` page** | Hub layout per §3; example data only |
| 8 | **Create `/documents/category/[slug]`** | SSG `generateStaticParams` from taxonomy |
| 9 | **Create `/documents/document/[id]`** | SSG from registry; warnings per §6 |
| 10 | **Create `/documents/search` page** | Client filter; URL query sync; Fuse.js optional later |
| 11 | **Configure static export** | `output: 'export'`; no server APIs |
| 12 | **Accessibility pass** | Focus, labels, contrast, skip link |
| 13 | **Lighthouse check** | Target ≥ 95 all categories |

### Data policy for Phase 4B

- Use **`document-registry.example.json`** for all UI development
- Do **not** switch to production `document-registry.json` until validation script passes and link check complete
- Do **not** commit document binaries

### Out of scope for Phase 4B

- Production deploy
- Fuse.js install (optional enhancement when doc count warrants)
- Authentication / restricted doc gating
- Upload, admin, CMS

---

## Related Documents

| Document | Role |
|----------|------|
| [REGISTRY_DATA_MODEL.md](./REGISTRY_DATA_MODEL.md) | Schema and validation |
| [taxonomy.json](./taxonomy.json) | Category definitions |
| [document-registry.example.json](./document-registry.example.json) | Dev fixtures |
| [PHASE3_ONEDRIVE_STORAGE_GUIDE.md](./PHASE3_ONEDRIVE_STORAGE_GUIDE.md) | Storage architecture |
| [ONEDRIVE_PERMISSION_POLICY.md](./ONEDRIVE_PERMISSION_POLICY.md) | Access governance |
| [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md) | ID and filename rules |
