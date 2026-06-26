# OneDrive Permission Policy — RAE Document Center

**Project:** RAE Document Center  
**Applies to:** `RAE-Document-Center/` OneDrive root and all subfolders  
**Last updated:** 2026-06-17

---

## Purpose

Define who can read, upload, edit, and administer documents stored in OneDrive for the RAE Document Center. Permissions here support the registry architecture: the public website links to OneDrive; access control on OneDrive determines who can open files.

---

## Principles

1. **Least privilege** — Grant the minimum access needed for each role.
2. **Owner accountability** — Every published document has an `owner` responsible for access and accuracy.
3. **Separation of duties** — Content owners manage documents; platform admins manage folder structure and governance.
4. **No anonymous write access** — Upload and edit require authenticated organizational accounts.
5. **Links are intentional** — Share links (`storage_url`) are created deliberately for registry entries; avoid org-wide "anyone with link can edit."

---

## Roles

| Role | Description |
|------|-------------|
| **Platform Admin** | Creates root structure, manages `99-Governance/`, audits permissions |
| **Category Owner** | Owns one or more category folders (`01`–`06`); approves uploads in their area |
| **Document Owner** | Responsible for a specific document (`owner` field in metadata) |
| **Contributor** | Can upload to `00-Inbox` or assigned category folders |
| **Reader** | Can view/download via share link or read-only folder access |
| **Archive Manager** | Manages `90-Archive/` moves and retention |

---

## Folder-Level Permissions

| Folder | Platform Admin | Category Owner | Contributor | Reader |
|--------|----------------|----------------|-------------|--------|
| `RAE-Document-Center/` (root) | Full Control | Read | Read | No direct access |
| `00-Inbox/` | Full Control | Read | Contribute (upload) | No |
| `01`–`06` (category) | Full Control | Edit (own category) | Contribute (with approval) | Via share link only |
| `90-Archive/` | Full Control | Read | No | Via share link only |
| `99-Governance/` | Full Control | Read | No | Read (internal) |

### Category owner assignment (to be confirmed)

| Folder | Suggested owner role |
|--------|---------------------|
| `01-งานบริหารและธุรการ/` | Administration unit lead |
| `02-งานคลังและพัสดุ/` | Inventory & supplies lead |
| `03-งานวิจัย/` | Research unit lead |
| `04-งานบริการวิชาการ/` | Academic services lead |
| `05-งานนโยบายและแผน/` | Policy & planning lead |
| `06-คู่มือปฏิบัติงาน/` | Operations / training lead |

> **Open question:** Confirm named individuals or AD groups for each category owner before go-live.

---

## Share Link Policy (`storage_url`)

For documents with `status = current` in the registry:

| Setting | Requirement |
|---------|-------------|
| Link type | **View only** (no edit via anonymous link) |
| Scope | "People in organization" preferred; "Anyone with link" only if external access is required |
| Expiration | No expiration for stable `current` documents; review annually |
| Regeneration | If link breaks or policy changes, update `storage_url` in storage map before Phase 4 release |

For `draft`, `obsolete`, and `archived` documents:

- Share links optional unless still referenced from the registry.
- Prefer removing public links when moving to `90-Archive/`.

---

## Upload and Classification Workflow

1. **Contributor** uploads to `00-Inbox/` with draft naming (see [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md)).
2. **Category Owner** reviews, assigns `id`, renames file, moves to correct category folder.
3. **Document Owner** confirms metadata row in storage map and requests share link.
4. **Platform Admin** or Category Owner creates view-only `storage_url` for `current` documents.

Documents must not remain in `00-Inbox/` for more than **30 days** without classification or explicit `note` justification.

---

## Archive and Obsolete Handling

| Action | Permission required | Registry impact |
|--------|--------------------|-----------------|
| Mark obsolete | Document Owner + Category Owner | Set `status = obsolete`; update `note` with superseding `id` |
| Move to archive | Archive Manager | Move file to `90-Archive/`; set `status = archived` |
| Delete file | Platform Admin only | Remove registry row or set archived with `note`; never delete without registry update |

**Rule:** Do not delete files that are referenced by a `current` registry entry. Broken links block release.

---

## Security Requirements

- Use organizational OneDrive / SharePoint; do not use personal OneDrive accounts for official documents.
- Do not store credentials, private keys, or unredacted personal data in publicly linked folders.
- Audit share links quarterly; revoke unused or overly broad links.
- Report suspected unauthorized access to Platform Admin immediately.

---

## Audit Checklist (Quarterly)

- [ ] Category owners still correct for each folder
- [ ] No unexpected "Anyone with link can edit" permissions
- [ ] `00-Inbox/` cleared or justified
- [ ] Archive folder contains only `obsolete` / `archived` status documents
- [ ] Share links for all `current` documents still resolve

---

## Related Documents

- [PHASE3_ONEDRIVE_STORAGE_GUIDE.md](./PHASE3_ONEDRIVE_STORAGE_GUIDE.md)
- [DOCUMENT_NAMING_STANDARD.md](./DOCUMENT_NAMING_STANDARD.md)
- [STORAGE_MAP_TEMPLATE.csv](./STORAGE_MAP_TEMPLATE.csv)
