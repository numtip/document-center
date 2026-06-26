# Document Naming Standard — RAE Document Center

**Project:** RAE Document Center  
**Applies to:** All files under `RAE-Document-Center/` in OneDrive  
**Last updated:** 2026-06-17

---

## Purpose

Consistent file and identifier naming ensures:

- Unique, stable `id` values for `document-registry.json`
- Predictable `onedrive_path` values
- Easier search, sort, and handoff to Phase 4

---

## Document ID Format

```
RAE-DC-{NNNN}
```

| Part | Rule | Example |
|------|------|---------|
| Prefix | Fixed `RAE-DC-` | `RAE-DC-` |
| Number | Four-digit zero-padded sequence | `0001`, `0042`, `1203` |

### ID rules

1. **Globally unique** — One `id` per logical document series root (new major version may keep same `id`; see versioning).
2. **Immutable** — Once assigned and published, do not reuse an `id` for a different document.
3. **Assigned at classification** — IDs are assigned when a document leaves `00-Inbox/`, not at upload.
4. **Recorded in metadata** — `id` column in storage map must match filename prefix.

---

## File Name Format

```
{id}_{title-slug}_v{major}.{minor}.{ext}
```

### Components

| Component | Rule | Example |
|-----------|------|---------|
| `{id}` | `RAE-DC-NNNN` | `RAE-DC-0042` |
| `{title-slug}` | Short Thai or English descriptor; underscores between words; no spaces | `คู่มือการจัดเก็บเอกสาร` → `คู่มือการจัดเก็บเอกสาร` or transliterated slug |
| `v{major}.{minor}` | Version number | `v1.0`, `v2.1` |
| `{ext}` | Lowercase extension | `.pdf`, `.docx`, `.xlsx` |

### Full examples

```
RAE-DC-0001_คู่มือปฏิบัติงาน_v1.0.pdf
RAE-DC-0015_research-report-template_v2.0.docx
RAE-DC-0099_governance-policy_v1.0.pdf
```

---

## Character and Length Rules

| Rule | Requirement |
|------|-------------|
| Spaces | Not allowed in filenames; use `_` |
| Special characters | Avoid `\ / : * ? " < > \|` |
| Length | Keep total filename under 200 characters |
| Case | Use lowercase for extensions; ID prefix uppercase as shown |
| Language | Thai titles allowed in slug; prefer consistency within each category |

---

## Versioning

| Change type | Version bump | Same `id`? |
|-------------|--------------|------------|
| Typo / formatting only | Minor (`v1.0` → `v1.1`) | Yes |
| Content revision | Minor or major per owner decision | Yes |
| Complete rewrite / new purpose | Major (`v1.x` → `v2.0`) | Yes, unless superseded by new document |
| Superseded by different document | N/A — old doc → `obsolete` | New document gets new `id` |

When superseding:

1. Set old registry row `status = obsolete`.
2. Add `note` referencing new `id`.
3. Move old file to `90-Archive/` when appropriate.

---

## Folder Placement vs. File Name

- **Category** is determined by folder location, not embedded in filename.
- **`onedrive_path`** = `{category-folder}/{filename}`

Example:

```
onedrive_path: 03-งานวิจัย/RAE-DC-0020_รายงานวิจัย_v1.0.pdf
category:       03-งานวิจัย
```

---

## Draft and Inbox Naming

Documents in `00-Inbox/` before ID assignment:

```
DRAFT_{upload-date}_{short-description}.{ext}
```

Example: `DRAFT_2026-06-17_ร่างคู่มือ.docx`

Upon classification:

1. Assign `RAE-DC-NNNN`.
2. Rename to standard format.
3. Move to target category folder.
4. Update storage map row.

---

## File Types (`file_type` column)

Use lowercase extension without dot:

| Extension | `file_type` value |
|-----------|-------------------|
| PDF | `pdf` |
| Word | `docx` |
| Excel | `xlsx` |
| PowerPoint | `pptx` |
| Image | `png`, `jpg` |
| Other | Use actual extension; document in `note` |

---

## Prohibited Practices

- Storing files in Git (metadata only in repository)
- Duplicate `id` in filenames or registry
- Generic names (`document.pdf`, `final_v2_FINAL.pdf`)
- Personal or non-organizational prefixes outside `RAE-DC-`
- Changing filename `id` after publication without registry update

---

## Related Documents

- [PHASE3_ONEDRIVE_STORAGE_GUIDE.md](./PHASE3_ONEDRIVE_STORAGE_GUIDE.md)
- [STORAGE_MAP_TEMPLATE.csv](./STORAGE_MAP_TEMPLATE.csv)
- [ONEDRIVE_PERMISSION_POLICY.md](./ONEDRIVE_PERMISSION_POLICY.md)
