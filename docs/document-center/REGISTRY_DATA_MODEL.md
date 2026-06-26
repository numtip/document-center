# Registry Data Model — RAE Document Center

**Project:** RAE Document Center  
**Phase:** 3.7 — Taxonomy + Registry Data Model Lock  
**Status:** Locked for Phase 4 implementation  
**Last updated:** 2026-06-17

---

## Purpose

Lock the **taxonomy** and **document registry** schemas before building the Next.js static Document Center UI. This document is the canonical reference for field definitions, allowed values, validation rules, and CSV-to-JSON mapping.

---

## Architecture

```
OneDrive (file storage — not in Git)
        ↓
storage-map.xlsx / STORAGE_MAP_TEMPLATE.csv (authoring / inventory)
        ↓
document-registry.json (canonical metadata in Git)
        ↓
Next.js static Document Center
        ↓
Search + Category + Download
```

| Artifact | Location | Role |
|----------|----------|------|
| `taxonomy.json` | Git | Locked category definitions |
| `STORAGE_MAP_TEMPLATE.csv` | Git | Authoring template for inventory |
| `document-registry.json` | Git | Production registry (Phase 4) |
| `document-registry.example.json` | Git | Sample records for development |
| Document files | OneDrive only | Never committed to Git |

---

## Taxonomy Schema (`taxonomy.json`)

### Root structure

```json
{
  "version": "1.0.0",
  "updated": "YYYY-MM-DD",
  "categories": [ /* Category[] */ ]
}
```

### Category object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Stable slug used as `category` in document records |
| `name_th` | string | Yes | Thai display name |
| `name_en` | string | Yes | English display name |
| `folder` | string | Yes | OneDrive folder name under `RAE-Document-Center/` |
| `owner_group` | string | Yes | AD / M365 group responsible for the category |
| `description_th` | string | Yes | Short Thai description for UI and governance |
| `sort_order` | integer | Yes | Display order in category navigation (ascending) |
| `enabled` | boolean | Yes | `false` hides category from UI without deleting history |

### Locked categories (v1.0.0)

| `id` | `folder` | `sort_order` |
|------|----------|--------------|
| `admin` | `01-งานบริหารและธุรการ` | 1 |
| `finance-procurement` | `02-งานคลังและพัสดุ` | 2 |
| `research` | `03-งานวิจัย` | 3 |
| `academic-service` | `04-งานบริการวิชาการ` | 4 |
| `policy-planning` | `05-งานนโยบายและแผน` | 5 |
| `manuals` | `06-คู่มือปฏิบัติงาน` | 6 |

Special OneDrive folders (`00-Inbox`, `90-Archive`, `99-Governance`) are **not** taxonomy categories. Documents in those folders still use a taxonomy `category` id reflecting their subject area.

---

## Document Registry Schema

### Root structure (`document-registry.json`)

```json
{
  "version": "1.0.0",
  "updated": "YYYY-MM-DD",
  "source": "optional provenance string",
  "documents": [ /* Document[] */ ]
}
```

### Document object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique ID: `RAE-DC-NNNN` (four-digit zero-padded) |
| `title` | string | Yes | Human-readable document title |
| `category` | string | Yes | Taxonomy `id` (e.g. `research`, not folder name) |
| `owner` | string | Yes | Email or role of responsible person/unit |
| `file_type` | string | Yes | Lowercase extension without dot (`pdf`, `docx`, `xlsx`) |
| `status` | string | Yes | Lifecycle state (see allowed values) |
| `updated_date` | string | Yes | Last content change date: `YYYY-MM-DD` |
| `onedrive_path` | string | Yes | Path relative to `RAE-Document-Center/` root |
| `storage_url` | string | Conditional | OneDrive share link; see rules below |
| `tags` | string[] | Yes | Lowercase keywords for search/filter |
| `version` | string | Yes | Semantic version string (`1.0`, `1.1`, `2.0`) |
| `visibility` | string | Yes | Access tier for UI listing (see allowed values) |
| `note` | string | No | Free-text: supersession, restrictions, migration notes |

---

## Allowed Values

### `status`

| Value | Meaning | Listed in UI search |
|-------|---------|---------------------|
| `current` | Active, published document | Yes |
| `obsolete` | Superseded but retained | Optional / de-emphasized |
| `archived` | Moved to `90-Archive/` | No (default) |
| `draft` | Work in progress | No (default) |

### `visibility`

| Value | Meaning |
|-------|---------|
| `public` | Visible to all site visitors; link may allow external access |
| `internal` | Visible on site to org users; OneDrive link scoped to organization |
| `restricted` | Hidden from default search; access by exception only |

### `file_type`

Lowercase extension without leading dot. Common values: `pdf`, `docx`, `xlsx`, `pptx`, `png`, `jpg`.

---

## Conditional Rules

### `storage_url` requirement

| Condition | `storage_url` required? |
|-----------|-------------------------|
| `status = current` AND `visibility = public` | **Yes** |
| `status = current` AND `visibility = internal` | **Yes** |
| `status = current` AND `visibility = restricted` | Recommended; may omit if access is manual |
| `status = draft` | No |
| `status = obsolete` | No (optional if archive link retained) |
| `status = archived` | No |

All non-empty `storage_url` values must resolve before release. **Broken links are release blockers.**

---

## Validation Rules

Apply to CSV inventory, example JSON, and production `document-registry.json`:

1. **Duplicate IDs forbidden** — Each `id` unique across the registry.
2. **Category must exist in `taxonomy.json`** — `category` must match an enabled category `id`.
3. **Owner required** — Non-empty `owner` on every record.
4. **Updated date format** — `updated_date` must be `YYYY-MM-DD`; must not be in the future.
5. **File type format** — Lowercase extension only (e.g. `pdf`, not `.pdf` or `PDF`).
6. **Status enum** — One of: `current`, `obsolete`, `archived`, `draft`.
7. **Visibility enum** — One of: `public`, `internal`, `restricted`.
8. **`storage_url` for published documents** — Required when `status = current` and `visibility` is `public` or `internal`.
9. **Tags format** — Array of lowercase strings in JSON; semicolon-separated in CSV.
10. **Version format** — Semantic style: `{major}.{minor}` (e.g. `1.0`, `1.1`, `2.0`).
11. **Broken links are release blockers** — All required URLs must be reachable.
12. **No primary files in Git** — Binaries live in OneDrive only.
13. **Metadata only in repository** — Registry and taxonomy JSON/CSV only.

### Recommended additional checks

- `onedrive_path` folder prefix should align with taxonomy `folder` for `current` documents (except `00-Inbox`, `90-Archive`).
- Filename prefix should match `id` per [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md).
- `tags` should contain at least one entry per document.

---

## CSV to JSON Mapping

Source: [STORAGE_MAP_TEMPLATE.csv](./STORAGE_MAP_TEMPLATE.csv)  
Target: `document-registry.json`

### Column order (CSV)

```
id,title,category,owner,file_type,status,updated_date,onedrive_path,storage_url,tags,version,visibility,note
```

### Field mapping

| CSV column | JSON field | Transform |
|------------|------------|-----------|
| `id` | `id` | As-is |
| `title` | `title` | As-is |
| `category` | `category` | Taxonomy `id` slug |
| `owner` | `owner` | As-is |
| `file_type` | `file_type` | Lowercase |
| `status` | `status` | As-is |
| `updated_date` | `updated_date` | As-is (`YYYY-MM-DD`) |
| `onedrive_path` | `onedrive_path` | As-is |
| `storage_url` | `storage_url` | As-is; omit key if empty |
| `tags` | `tags` | Split on `;`, trim, lowercase → array |
| `version` | `version` | As-is |
| `visibility` | `visibility` | As-is |
| `note` | `note` | As-is; omit key if empty |

### CSV `tags` encoding

Use semicolon-separated lowercase keywords:

```csv
"manual;operations;document-management"
```

Empty tags cell → empty array `[]` (flag in validation if tags are required).

### Example conversion

**CSV row:**

```csv
RAE-DC-0001,คู่มือปฏิบัติงาน,manuals,ops@example.org,pdf,current,2026-06-17,06-คู่มือปฏิบัติงาน/RAE-DC-0001_คู่มือ_v1.0.pdf,https://...,manual;operations,1.0,public,Example note
```

**JSON object:**

```json
{
  "id": "RAE-DC-0001",
  "title": "คู่มือปฏิบัติงาน",
  "category": "manuals",
  "owner": "ops@example.org",
  "file_type": "pdf",
  "status": "current",
  "updated_date": "2026-06-17",
  "onedrive_path": "06-คู่มือปฏิบัติงาน/RAE-DC-0001_คู่มือ_v1.0.pdf",
  "storage_url": "https://...",
  "tags": ["manual", "operations"],
  "version": "1.0",
  "visibility": "public",
  "note": "Example note"
}
```

---

## Phase 3 → Phase 3.7 Deviation

Phase 3 used OneDrive **folder names** as the `category` value (e.g. `06-คู่มือปฏิบัติงาน`). Phase 3.7 **locks** `category` to taxonomy **slug ids** (e.g. `manuals`).

| Phase 3 `category` | Phase 3.7 `category` | OneDrive `folder` |
|--------------------|----------------------|-------------------|
| `01-งานบริหารและธุรการ` | `admin` | unchanged |
| `02-งานคลังและพัสดุ` | `finance-procurement` | unchanged |
| `03-งานวิจัย` | `research` | unchanged |
| `04-งานบริการวิชาการ` | `academic-service` | unchanged |
| `05-งานนโยบายและแผน` | `policy-planning` | unchanged |
| `06-คู่มือปฏิบัติงาน` | `manuals` | unchanged |

Phase 4 UI resolves display names via `taxonomy.json`. OneDrive folder structure is unchanged.

---

## Phase 4 Handoff

Phase 4 should:

1. Load `taxonomy.json` for category navigation and labels.
2. Load `document-registry.json` (generated from validated CSV) as the document index.
3. Use `document-registry.example.json` for local development and UI fixtures.
4. Implement a CSV → JSON build step applying validation rules above.
5. Filter UI listings by `status`, `visibility`, and `enabled` taxonomy categories.
6. Link downloads via `storage_url` only — never serve files from the static site.

### Phase 4 inputs (ready when validated)

- [x] `taxonomy.json` — locked v1.0.0
- [x] `document-registry.example.json` — sample fixtures
- [x] `STORAGE_MAP_TEMPLATE.csv` — updated column schema
- [ ] `document-registry.json` — production data (populate from real inventory)
- [ ] Link validation report — all required URLs verified

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [taxonomy.json](./taxonomy.json) | Locked category definitions |
| [document-registry.example.json](./document-registry.example.json) | Sample registry records |
| [STORAGE_MAP_TEMPLATE.csv](./STORAGE_MAP_TEMPLATE.csv) | CSV authoring template |
| [PHASE3_ONEDRIVE_STORAGE_GUIDE.md](./PHASE3_ONEDRIVE_STORAGE_GUIDE.md) | OneDrive storage foundation |
| [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md) | File and ID naming |
| [ONEDRIVE_PERMISSION_POLICY.md](./ONEDRIVE_PERMISSION_POLICY.md) | Access control |
