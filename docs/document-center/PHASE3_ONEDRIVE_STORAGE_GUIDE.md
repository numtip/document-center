# Phase 3 — OneDrive Storage Foundation

**Project:** RAE Document Center  
**Phase:** 3 — OneDrive Storage Foundation  
**Status:** Documentation only (no implementation)  
**Last updated:** 2026-06-17

---

## Purpose

Phase 3 establishes the **OneDrive storage layer** and **registry-ready metadata structure** for the RAE Document Center. This phase prepares physical file storage and governance so Phase 4 can build `document-registry.json` and wire it to the Next.js Document Center.

The website is a **Document Registry**, not file storage. OneDrive holds files; the repository holds metadata only.

---

## Architecture

```
OneDrive (primary file storage)
        ↓
document-registry.json (metadata bridge — Phase 4)
        ↓
Next.js Document Center (registry UI)
        ↓
Search + Category + Download (links to OneDrive)
```

| Layer | Role | In Git? |
|-------|------|---------|
| OneDrive | Authoritative file storage | No |
| `document-registry.json` | Canonical metadata index | Yes (metadata only) |
| Next.js Document Center | Search, browse, download links | Yes (app code) |

---

## Prerequisites

Before starting Phase 3 work:

1. OneDrive for Business (or designated organizational OneDrive) account with sufficient quota.
2. Agreement on document owners per category (see folder structure below).
3. Read and apply:
   - [ONEDRIVE_PERMISSION_POLICY.md](./ONEDRIVE_PERMISSION_POLICY.md)
   - [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md)
4. Use [STORAGE_MAP_TEMPLATE.csv](./STORAGE_MAP_TEMPLATE.csv) to inventory existing documents.

> **Note:** At the time this guide was written, prerequisite KB documents (`TOKEN_SAVIOR_WORKFLOW.md`, RAE Document Registry Architecture, Document Governance Policy) were not present in the repository. Align this guide with those documents when they become available.

---

## OneDrive Root Folder Structure

Create the following top-level structure under the designated OneDrive account or shared library:

```
RAE-Document-Center/
├── 00-Inbox/                      # Staging — unclassified uploads
├── 01-งานบริหารและธุรการ/          # Administration & general affairs
├── 02-งานคลังและพัสดุ/             # Inventory & supplies
├── 03-งานวิจัย/                    # Research
├── 04-งานบริการวิชาการ/            # Academic services
├── 05-งานนโยบายและแผน/             # Policy & planning
├── 06-คู่มือปฏิบัติงาน/             # Operational manuals
├── 90-Archive/                    # Obsolete / superseded documents
└── 99-Governance/                 # Policies, standards, audit artifacts
```

### Folder usage rules

| Folder | Purpose | Default `status` |
|--------|---------|-------------------|
| `00-Inbox` | Temporary holding; must be classified within 30 days | `draft` |
| `01`–`06` | Active category storage | `current` |
| `90-Archive` | Retained for reference; not primary | `archived` or `obsolete` |
| `99-Governance` | Governance docs for this system | `current` |

Category folder names map directly to the `category` field in registry metadata (use the numeric prefix + Thai label, e.g. `03-งานวิจัย`).

---

## Metadata Schema (Registry-Ready)

All documents indexed in Phase 4 must conform to this schema. Populate rows in `STORAGE_MAP_TEMPLATE.csv` during Phase 3 inventory.

| Column | Required | Description |
|--------|----------|-------------|
| `id` | Yes | Unique document identifier (see naming standard) |
| `title` | Yes | Human-readable document title |
| `category` | Yes | OneDrive category folder (e.g. `03-งานวิจัย`) |
| `owner` | Yes | Responsible person or unit (email or role) |
| `file_type` | Yes | Extension or MIME hint (`pdf`, `docx`, `xlsx`, etc.) |
| `status` | Yes | `current` \| `obsolete` \| `archived` \| `draft` |
| `updated_date` | Yes | ISO 8601 date (`YYYY-MM-DD`) of last content change |
| `onedrive_path` | Yes | Relative path from `RAE-Document-Center/` root |
| `storage_url` | Conditional | Shareable OneDrive link; **required** when `status` is `current` |
| `note` | No | Free-text (supersedes, restrictions, migration notes) |

### Status values

| Value | Meaning |
|-------|---------|
| `current` | Active, published document |
| `obsolete` | Superseded but retained; link may point to archive copy |
| `archived` | Moved to `90-Archive/`; not promoted in search |
| `draft` | Work in progress; not publicly listed |

---

## Validation Rules

These rules apply to the storage map CSV and, in Phase 4, to `document-registry.json`.

1. **`owner` required** — Every row must have a non-empty owner.
2. **`storage_url` required for published documents** — Rows with `status = current` must have a valid, shareable OneDrive URL.
3. **Duplicate IDs forbidden** — Each `id` must be unique across the entire registry.
4. **Broken links are release blockers** — All `storage_url` values must resolve before Phase 4 release.
5. **No primary files in Git** — Document binaries live in OneDrive only; the repository stores metadata and application code.
6. **Metadata only in repository** — CSV during Phase 3; JSON registry in Phase 4.

Additional checks recommended during inventory:

- `onedrive_path` must match an actual file location in OneDrive.
- `category` must match a defined folder under `RAE-Document-Center/`.
- `updated_date` must not be in the future.
- Files in `00-Inbox` longer than 30 days should be classified or flagged in `note`.

---

## Phase 3 Workflow

### Step 1 — Provision OneDrive

1. Create `RAE-Document-Center/` root folder.
2. Create all subfolders per structure above.
3. Apply permissions per [ONEDRIVE_PERMISSION_POLICY.md](./ONEDRIVE_PERMISSION_POLICY.md).

### Step 2 — Inventory existing documents

1. Copy [STORAGE_MAP_TEMPLATE.csv](./STORAGE_MAP_TEMPLATE.csv) to a working copy (e.g. `STORAGE_MAP_2026.csv`).
2. For each document, record metadata per schema.
3. Rename/move files to comply with [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md).
4. Generate share links (`storage_url`) for all `current` documents.

### Step 3 — Validate storage map

Run manual or scripted checks (Phase 4 may automate):

- [ ] No duplicate `id` values
- [ ] All rows have `owner`
- [ ] All `current` rows have `storage_url`
- [ ] Spot-check links open correctly
- [ ] Paths align with OneDrive folder structure

### Step 4 — Handoff to Phase 4

Deliver to Phase 4:

- Validated `STORAGE_MAP_*.csv` (source for `document-registry.json`)
- Confirmed OneDrive folder structure and permissions
- List of open questions (owners TBD, broken legacy links, etc.)

---

## What Phase 3 Does NOT Include

- Building or deploying the Next.js application
- Creating `document-registry.json` (Phase 4)
- Committing document files to Git
- Processing or converting document content
- Production deployment or live URL changes

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [STORAGE_MAP_TEMPLATE.csv](./STORAGE_MAP_TEMPLATE.csv) | Metadata inventory template |
| [ONEDRIVE_PERMISSION_POLICY.md](./ONEDRIVE_PERMISSION_POLICY.md) | Access control |
| [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md) | File and ID naming |

---

## Readiness Checklist for Phase 4

- [ ] OneDrive folder structure created and permissioned
- [ ] Storage map populated with all known documents
- [ ] Validation rules passed (no duplicate IDs, owners set, links verified)
- [ ] Naming standard applied to all files
- [ ] Open questions documented and assigned
