# RAE Document Registry — Microsoft Lists Schema

**Phase:** M365-4 — Microsoft Lists Registry Design  
**Blueprint ref:** `docs/document-center/M365 FoundationBlueprint.MD` §Phase M365-4  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-14  
**Applies to:** `RAE Document Registry` Microsoft List on RAE Document Center site  
**Predecessor:** `docs/m365/library-schema.md` (EA-3), `docs/document-center/REGISTRY_DATA_MODEL.md` (Phase 3.7)

---

## 1. Design Principles

1. **Microsoft Lists is the authoritative operational metadata registry** — not JSON, not the website.
2. **Single schema** — One List schema for all 772 legacy records + future documents.
3. **SharePoint is the source of truth for files** — Registry references documents; it does not store files.
4. **Minimum enterprise fields** — Every record must satisfy the mandatory enterprise minimum (9 fields).
5. **Build Less. Govern More.** — Prefer Microsoft Lists native capabilities over custom code.
6. **Lean schema** — Only fields with clear governance or discovery purpose. Avoid SharePoint-only traceability fields.

---

## 2. Registry Identity Strategy — DocumentID

### 2.1 Format

```
RAE-NNNNN
```

| Part | Rule | Example |
|------|------|---------|
| Prefix | Fixed `RAE-` | `RAE-` |
| Number | Five-digit zero-padded sequence | `00001`, `00420`, `05761` |

### 2.2 Uniqueness Boundary

- **Globally unique** across all 6 document libraries and the registry.
- No DocumentID may be reused for a different logical document — ever.
- The registry enforces uniqueness natively via Microsoft Lists column unique constraint.

### 2.3 Assignment Authority

- **Assigned by Category Owner** at the point of metadata classification (when a document leaves `_Inbox`).
- Migration records inherit DocumentID from the migration manifest (already pre-assigned).
- Future new documents: the upload workflow (Power Automate, Phase M365-5) reserves the next available ID.

### 2.4 Immutability Rule

- **DocumentID is immutable.**
- After a DocumentID is assigned and the record exists in the registry, the ID must never change.
- If a record was created in error, mark it `DocumentStatus = Obsolete` with a `Notes` explanation. Do not delete or reassign.

### 2.5 Behavior When a File Is Renamed

- DocumentID **remains unchanged**.
- The filename changes independently. The registry's `StorageURL` is updated to point to the renamed file.
- The DocumentID is NOT derived from the filename.

### 2.6 Behavior When a File Is Moved Between SharePoint Folders

- DocumentID **remains unchanged**.
- Category and Subcategory fields are updated in the registry.
- The registry records the current folder location; it does not track history (that is SharePoint's versioning job).

### 2.7 Behavior When a File Moves Between Libraries

- DocumentID **remains unchanged**.
- Category field is updated to reflect the new taxonomy slug.
- Owner is re-assigned if the document moves to a different category's library.

### 2.8 Duplicate Handling

- Duplicate files (45 rows with `MigrationStatus = Duplicate (linked)`) **share the same DocumentID** as the primary file.
- The duplicate legacy URL is recorded in `RelatedDocuments` or `LegacySourceURL`.
- No separate registry record for duplicates — the registry tracks one record per logical document.

### 2.9 Migration Legacy ID Handling

- Legacy migration records from Phase 5A used format `RAE-DC-NNNN`. These **must be re-mapped** to `RAE-NNNNN` format for registry consistency.
- A mapping table should be maintained in `migration/sharepoint-migration-manifest.csv` (existing) with cross-reference columns.
- Migration immediate priority: preserve the mapping between legacy `RAE-DC-NNNN` and canonical `RAE-NNNNN`.

---

## 3. Registry Column Definitions

### Classification Legend

| Tag | Meaning |
|-----|---------|
| **CORE** | Mandatory enterprise minimum field — record is invalid without it |
| **GOVERNANCE** | Lifecycle, compliance, and operational management |
| **DISCOVERY** | Search, filtering, and categorization |
| **INTEGRATION** | Cross-system linking and synchronization |
| **OPTIONAL** | Useful but not mandatory — may be empty |
| **DEFERRED** | Recognised as needed but deferred to a later phase |

### 3.1 Core Identity Fields

#### DocumentID

| Property | Value |
|----------|-------|
| **Display Name** | Document ID |
| **Recommended Internal Name** | RAE_DocumentID |
| **Purpose** | Globally unique canonical identifier for the document record |
| **Microsoft Lists Column Type** | Single line of text |
| **Required** | Yes |
| **Unique** | Yes |
| **Indexed** | Yes |
| **Default Value** | _(auto-assigned)_ |
| **Allowed Values / Source** | Pattern: `RAE-NNNNN` |
| **Source of Truth** | Registry — assigned at classification |
| **Synchronization Direction** | Registry → SharePoint (write-back) |
| **Public Export** | Yes |
| **Validation Rule** | Must match `RAE-\d{5}` |
| **Notes** | Immutable once assigned |
| **Classification** | **CORE** |

#### Title

| Property | Value |
|----------|-------|
| **Display Name** | Title |
| **Recommended Internal Name** | RAE_Title |
| **Purpose** | Human-readable document title |
| **Microsoft Lists Column Type** | Single line of text |
| **Required** | Yes |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | _(from manifest or filename stem)_ |
| **Allowed Values / Source** | Free text; max 255 characters |
| **Source of Truth** | Registry — updated by Owner |
| **Synchronization Direction** | Bidirectional: SharePoint ↔ Registry |
| **Public Export** | Yes |
| **Validation Rule** | Must not be empty; max 255 chars |
| **Notes** | Derivation priority: manifest Title → link_text → original_filename → path stem |
| **Classification** | **CORE** |

#### Description

| Property | Value |
|----------|-------|
| **Display Name** | Description |
| **Recommended Internal Name** | RAE_Description |
| **Purpose** | Brief summary of document content and purpose |
| **Microsoft Lists Column Type** | Multiple lines of text (plain text) |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(empty)_ |
| **Allowed Values / Source** | Free text; max 500 characters |
| **Source of Truth** | Registry — entered by Owner |
| **Synchronization Direction** | Registry → SharePoint |
| **Public Export** | Yes (if Visibility = public) |
| **Validation Rule** | Max 500 chars |
| **Notes** | Not in EA-3 schema; added for registry discovery quality |
| **Classification** | **DISCOVERY** |

### 3.2 Taxonomy Fields

#### Category

| Property | Value |
|----------|-------|
| **Display Name** | Category |
| **Recommended Internal Name** | RAE_Category |
| **Purpose** | Taxonomy category slug for classification and filtering |
| **Microsoft Lists Column Type** | Choice |
| **Required** | Yes |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | _(inherited from library at creation; none for direct List entries)_ |
| **Allowed Values / Source** | `admin`, `finance-procurement`, `policy-planning`, `academic-service`, `research`, `manuals` |
| **Source of Truth** | Taxonomy — defined in `taxonomy.json` |
| **Synchronization Direction** | Bidirectional: SharePoint ↔ Registry |
| **Public Export** | Yes |
| **Validation Rule** | Must match enabled taxonomy category id |
| **Notes** | Choice column; updates to taxonomy require column update |
| **Classification** | **CORE** |

#### Subcategory

| Property | Value |
|----------|-------|
| **Display Name** | Subcategory |
| **Recommended Internal Name** | RAE_Subcategory |
| **Purpose** | Thai subcategory name from legacy hierarchy; maps to SharePoint folder |
| **Microsoft Lists Column Type** | Single line of text |
| **Required** | No |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | _(from manifest or folder name)_ |
| **Allowed Values / Source** | Free text; Thai subcategory name |
| **Source of Truth** | Registry — derived from folder at classification |
| **Synchronization Direction** | Registry → SharePoint |
| **Public Export** | Yes |
| **Validation Rule** | Max 255 chars |
| **Notes** | Not a controlled vocabulary; free text for flexibility |
| **Classification** | **DISCOVERY** |

#### Tags

| Property | Value |
|----------|-------|
| **Display Name** | Tags |
| **Recommended Internal Name** | RAE_Tags |
| **Purpose** | Keywords for search and filtering |
| **Microsoft Lists Column Type** | Single line of text (semicolon-separated) |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(empty)_ |
| **Allowed Values / Source** | Lowercase terms; semicolon-separated |
| **Source of Truth** | Registry — entered by Owner |
| **Synchronization Direction** | Registry → SharePoint |
| **Public Export** | Yes |
| **Validation Rule** | Lowercase; semicolons as delimiters; max 500 chars total |
| **Notes** | Microsoft Lists does not support Managed Metadata natively. Use text column with semicolon delimiters. SharePoint Tags column (Managed Metadata) is separate. |
| **Classification** | **DISCOVERY** |

#### Audience

| Property | Value |
|----------|-------|
| **Display Name** | Audience |
| **Recommended Internal Name** | RAE_Audience |
| **Purpose** | Target audience for the document |
| **Microsoft Lists Column Type** | Choice (multi-select) |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(empty — not selected)_ |
| **Allowed Values / Source** | `internal-staff`, `researchers`, `students`, `public`, `academic-services`, `administration` |
| **Source of Truth** | Registry — entered by Owner |
| **Synchronization Direction** | Registry → SharePoint |
| **Public Export** | Yes (if Visibility = public; mapped to audience categories) |
| **Validation Rule** | Must be from allowed values if populated |
| **Notes** | Supports multi-select for documents targeting multiple audiences |
| **Classification** | **OPTIONAL** |

### 3.3 Ownership and Lifecycle Fields

#### Owner

| Property | Value |
|----------|-------|
| **Display Name** | Owner |
| **Recommended Internal Name** | RAE_Owner |
| **Purpose** | Responsible person or group for the document |
| **Microsoft Lists Column Type** | Person or Group |
| **Required** | Yes |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | _(none — must be assigned)_ |
| **Allowed Values / Source** | M365 user or M365 group |
| **Source of Truth** | Registry — confirmed at classification |
| **Synchronization Direction** | Bidirectional: SharePoint ↔ Registry |
| **Public Export** | Yes (display name/email only; no internal identifiers) |
| **Validation Rule** | Must be a valid M365 user or group; `TBD` is NOT valid in the registry (only in SharePoint during migration) |
| **Notes** | **TBD is NOT a valid registry Owner.** Registry is the authoritative operational registry; owner must be a real person or group. The SharePoint library may temporarily show `TBD` during migration import. |
| **Classification** | **CORE** |

#### Department

| Property | Value |
|----------|-------|
| **Display Name** | Department |
| **Recommended Internal Name** | RAE_Department |
| **Purpose** | Department or unit responsible for the document |
| **Microsoft Lists Column Type** | Single line of text |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(empty)_ |
| **Allowed Values / Source** | Free text (e.g. `งานบริหารและธุรการ`, `งานวิจัย`) |
| **Source of Truth** | Registry — derived from Owner or Category |
| **Synchronization Direction** | Registry → SharePoint |
| **Public Export** | Yes |
| **Validation Rule** | Max 255 chars |
| **Notes** | Populated via DERIVED rule from Category owner_group in taxonomy |
| **Classification** | **OPTIONAL** |

### 3.4 Status and Visibility Fields

#### Status

| Property | Value |
|----------|-------|
| **Display Name** | Status |
| **Recommended Internal Name** | RAE_Status |
| **Purpose** | Document lifecycle state |
| **Microsoft Lists Column Type** | Choice |
| **Required** | Yes |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | `draft` |
| **Allowed Values / Source** | `draft`, `review`, `approved`, `published`, `current`, `obsolete`, `archived` |
| **Source of Truth** | Registry — updated by Owner or workflow |
| **Synchronization Direction** | Bidirectional: SharePoint ↔ Registry |
| **Public Export** | Yes |
| **Validation Rule** | Must be from allowed values |
| **Notes** | Seven-value enterprise lifecycle vocabulary. Legacy migration conditions (`LegacyImported`, `MetadataOnly`) are NOT lifecycle statuses — they are represented via `SourceSystem` and `MigrationStatus` fields. See `registry-lifecycle-model.md` for legal transitions. |
| **Classification** | **CORE** |

#### Visibility

| Property | Value |
|----------|-------|
| **Display Name** | Visibility |
| **Recommended Internal Name** | RAE_Visibility |
| **Purpose** | Information exposure classification |
| **Microsoft Lists Column Type** | Choice |
| **Required** | Yes |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | `internal` |
| **Allowed Values / Source** | `public`, `internal`, `restricted`, `private` |
| **Source of Truth** | Registry — updated by Owner after review |
| **Synchronization Direction** | Bidirectional: SharePoint ↔ Registry |
| **Public Export** | Only `public` is exported |
| **Validation Rule** | Must be from allowed values |
| **Notes** | Four-value enterprise visibility vocabulary. `public` = accessible to all. `internal` = M365 org users. `restricted` = access by exception. `private` = owning group only. A document awaiting review is represented by `Status = review` not by a visibility value. See `registry-lifecycle-model.md` for valid combinations. |
| **Classification** | **CORE** |

### 3.5 Date Fields

#### UpdatedDate

| Property | Value |
|----------|-------|
| **Display Name** | Updated Date |
| **Recommended Internal Name** | RAE_UpdatedDate |
| **Purpose** | Last content modification date |
| **Microsoft Lists Column Type** | Date and Time (date only) |
| **Required** | Yes |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | _(current date at record creation)_ |
| **Allowed Values / Source** | `YYYY-MM-DD` |
| **Source of Truth** | Registry — updated by Owner or workflow |
| **Synchronization Direction** | Bidirectional: SharePoint ↔ Registry |
| **Public Export** | Yes |
| **Validation Rule** | Must not be a future date; must be valid ISO 8601 date |
| **Notes** | For legacy imports, initially set to migration/upload date. Owner updates to actual document date during review. |
| **Classification** | **CORE** |

#### ReviewDate

| Property | Value |
|----------|-------|
| **Display Name** | Review Date |
| **Recommended Internal Name** | RAE_ReviewDate |
| **Purpose** | Scheduled or completed governance review date |
| **Microsoft Lists Column Type** | Date and Time (date only) |
| **Required** | No |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | _(empty)_ |
| **Allowed Values / Source** | Valid ISO 8601 date |
| **Source of Truth** | Registry — entered by Owner |
| **Synchronization Direction** | Registry → SharePoint |
| **Public Export** | No (governance metadata) |
| **Validation Rule** | Must not be future if review is completed |
| **Notes** | Used by "Expiring Review" view to flag documents needing re-review |
| **Classification** | **GOVERNANCE** |

#### PublishedDate

| Property | Value |
|----------|-------|
| **Display Name** | Published Date |
| **Recommended Internal Name** | RAE_PublishedDate |
| **Purpose** | Date the document was published (made available to audience) |
| **Microsoft Lists Column Type** | Date and Time (date only) |
| **Required** | No |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | _(empty)_ |
| **Allowed Values / Source** | Valid ISO 8601 date |
| **Source of Truth** | Registry — set when Status transitions to `Published` or `Current` |
| **Synchronization Direction** | Registry → SharePoint |
| **Public Export** | Yes |
| **Validation Rule** | Must not be future |
| **Notes** | Populated by Power Automate on status change (Phase M365-5) |
| **Classification** | **GOVERNANCE** |

### 3.6 Storage and Access Fields

#### StorageURL

| Property | Value |
|----------|-------|
| **Display Name** | Storage URL |
| **Recommended Internal Name** | RAE_StorageURL |
| **Purpose** | SharePoint view-only link to the physical document |
| **Microsoft Lists Column Type** | Hyperlink |
| **Required** | Yes (conditional — see validation rules) |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(empty — must be assigned after file upload)_ |
| **Allowed Values / Source** | Valid HTTPS SharePoint view-only link |
| **Source of Truth** | SharePoint — created by Owner after file upload |
| **Synchronization Direction** | SharePoint → Registry |
| **Public Export** | Yes |
| **Validation Rule** | Required when Status is `current`, `published`, or `approved`. Must be HTTPS. Broken links are release blockers. |
| **Notes** | For records where `SourceSystem = WTMS Migration` and the original file was inaccessible (metadata-only condition), this may remain empty with `LegacySourceURL` providing the original legacy URL reference. |
| **Classification** | **CORE** |

#### LegacySourceURL

| Property | Value |
|----------|-------|
| **Display Name** | Legacy Source URL |
| **Recommended Internal Name** | RAE_LegacySourceURL |
| **Purpose** | Original WTMS legacy URL for traceability |
| **Microsoft Lists Column Type** | Hyperlink |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(from manifest)_ |
| **Allowed Values / Source** | URL string; may be dead link |
| **Source of Truth** | Migration manifest |
| **Synchronization Direction** | One-time import (manifest → Registry) |
| **Public Export** | No (dead/internal URL; no value to public) |
| **Validation Rule** | Must be valid URL format if populated |
| **Notes** | Preserved for traceability; not validated during normal operation |
| **Classification** | **INTEGRATION** |

### 3.7 Relationship Fields

#### RelatedDocuments

| Property | Value |
|----------|-------|
| **Display Name** | Related Documents |
| **Recommended Internal Name** | RAE_RelatedDocuments |
| **Purpose** | DocumentIDs of related or superseding documents |
| **Microsoft Lists Column Type** | Single line of text |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(empty)_ |
| **Allowed Values / Source** | Comma-separated `RAE-NNNNN` values |
| **Source of Truth** | Registry — entered by Owner |
| **Synchronization Direction** | Registry → SharePoint |
| **Public Export** | Yes (DocumentIDs only) |
| **Validation Rule** | Each reference must be a valid DocumentID format |
| **Notes** | Used for merge groups, supersession chains, and related document clusters |
| **Classification** | **DISCOVERY** |

#### DuplicateOf

| Property | Value |
|----------|-------|
| **Display Name** | Duplicate Of |
| **Recommended Internal Name** | RAE_DuplicateOf |
| **Purpose** | References the primary DocumentID when this record is a duplicate/alias |
| **Microsoft Lists Column Type** | Single line of text |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(empty — not a duplicate)_ |
| **Allowed Values / Source** | Valid DocumentID `RAE-NNNNN` |
| **Source of Truth** | Migration manifest |
| **Synchronization Direction** | One-time import (manifest → Registry) |
| **Public Export** | No |
| **Validation Rule** | If populated, must reference an existing DocumentID in the registry |
| **Notes** | Only populated for the 45 duplicate-linked migration records |
| **Classification** | **INTEGRATION** |

### 3.8 Source and Version Fields

#### SourceSystem

| Property | Value |
|----------|-------|
| **Display Name** | Source System |
| **Recommended Internal Name** | RAE_SourceSystem |
| **Purpose** | Originating system or process that created this registry record |
| **Microsoft Lists Column Type** | Choice |
| **Required** | Yes |
| **Unique** | No |
| **Indexed** | Yes |
| **Default Value** | `WTMS Migration` |
| **Allowed Values / Source** | `WTMS Migration`, `Manual Entry`, `Power Automate`, `Bulk Import`, `Direct Upload` |
| **Source of Truth** | Registry — set at record creation |
| **Synchronization Direction** | Record creation only (manual or automated) |
| **Public Export** | No |
| **Validation Rule** | Must be from allowed values |
| **Notes** | Distinguishes migration records from post-migration new documents |
| **Classification** | **GOVERNANCE** |

#### Version

| Property | Value |
|----------|-------|
| **Display Name** | Version |
| **Recommended Internal Name** | RAE_Version |
| **Purpose** | Semantic version of the document |
| **Microsoft Lists Column Type** | Single line of text |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | `1.0` |
| **Allowed Values / Source** | `{major}.{minor}` pattern |
| **Source of Truth** | Registry — updated by Owner on content change |
| **Synchronization Direction** | Bidirectional: SharePoint ↔ Registry |
| **Public Export** | Yes |
| **Validation Rule** | Must match `\d+\.\d+` |
| **Notes** | Semantic versioning: major.minor |
| **Classification** | **OPTIONAL** |

### 3.9 Governance and Notes Fields

#### Notes

| Property | Value |
|----------|-------|
| **Display Name** | Notes |
| **Recommended Internal Name** | RAE_Notes |
| **Purpose** | Free-text notes: supersession, restrictions, migration notes |
| **Microsoft Lists Column Type** | Multiple lines of text (plain text) |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | _(empty)_ |
| **Allowed Values / Source** | Free text; max 1000 characters |
| **Source of Truth** | Registry — entered by Owner or workflow |
| **Synchronization Direction** | Bidirectional: SharePoint ↔ Registry |
| **Public Export** | No (internal governance notes) |
| **Validation Rule** | Max 1000 chars |
| **Notes** | Do NOT use for public notes visible on portal. Use Description for public-facing summaries. |
| **Classification** | **GOVERNANCE** |

#### RecordVersion

| Property | Value |
|----------|-------|
| **Display Name** | Record Version |
| **Recommended Internal Name** | RAE_RecordVersion |
| **Purpose** | Internal registry record version for synchronization tracking |
| **Microsoft Lists Column Type** | Number |
| **Required** | No |
| **Unique** | No |
| **Indexed** | No |
| **Default Value** | `1` |
| **Allowed Values / Source** | Integer; auto-incremented |
| **Source of Truth** | Registry — system-managed |
| **Synchronization Direction** | Registry → Export (for change detection) |
| **Public Export** | No |
| **Validation Rule** | Integer ≥ 1 |
| **Notes** | **DEFERRED** — Phase M365-7 (Migration Pilot). Used for incremental export change detection in scheduled exports. |
| **Classification** | **DEFERRED** |

---

## 4. Column Summary Table

| # | Column | Type | Required | Indexed | Classification |
|---|--------|------|----------|---------|----------------|
| 1 | DocumentID | Text | Yes | Yes | **CORE** |
| 2 | Title | Text | Yes | Yes | **CORE** |
| 3 | Description | Multi-text | No | No | DISCOVERY |
| 4 | Category | Choice | Yes | Yes | **CORE** |
| 5 | Subcategory | Text | No | Yes | DISCOVERY |
| 6 | Tags | Text | No | No | DISCOVERY |
| 7 | Audience | Choice (multi) | No | No | OPTIONAL |
| 8 | Owner | Person/Group | Yes | Yes | **CORE** |
| 9 | Department | Text | No | No | OPTIONAL |
| 10 | Status | Choice | Yes | Yes | **CORE** |
| 11 | Visibility | Choice | Yes | Yes | **CORE** |
| 12 | UpdatedDate | Date | Yes | Yes | **CORE** |
| 13 | ReviewDate | Date | No | Yes | GOVERNANCE |
| 14 | PublishedDate | Date | No | Yes | GOVERNANCE |
| 15 | StorageURL | Hyperlink | Yes* | No | **CORE** |
| 16 | LegacySourceURL | Hyperlink | No | No | INTEGRATION |
| 17 | RelatedDocuments | Text | No | No | DISCOVERY |
| 18 | DuplicateOf | Text | No | No | INTEGRATION |
| 19 | SourceSystem | Choice | Yes | Yes | GOVERNANCE |
| 20 | Version | Text | No | No | OPTIONAL |
| 21 | Notes | Multi-text | No | No | GOVERNANCE |
| 22 | RecordVersion | Number | No | No | DEFERRED |

### Totals

| Metric | Count |
|--------|-------|
| **Total Columns** | **22** |
| **CORE (Required)** | **9** (DocumentID, Title, Category, Owner, Status, Visibility, UpdatedDate, StorageURL, SourceSystem) |
| **Required** | 10 (9 CORE + Owner - StorageURL* conditional) |
| **Indexed Recommended** | **11** (DocumentID, Title, Category, Subcategory, Owner, Status, Visibility, UpdatedDate, ReviewDate, PublishedDate, SourceSystem) |
| **GOVERNANCE** | 4 |
| **DISCOVERY** | 4 |
| **INTEGRATION** | 2 |
| **OPTIONAL** | 2 |
| **DEFERRED** | 1 |

> *StorageURL is conditionally required. See `registry-validation-rules.md` for conditions.

---

## 5. Index Strategy

| Column | Index Reason |
|--------|-------------|
| DocumentID | Primary lookup; unique constraint |
| Title | Search performance |
| Category | Primary navigation filter |
| Subcategory | Folder-level grouping |
| Owner | Owner assignment views and governance |
| Status | Lifecycle filtering |
| Visibility | Portal export filtering |
| UpdatedDate | Default sort in views |
| ReviewDate | Expiring review governance |
| PublishedDate | Publication tracking |
| SourceSystem | Migration vs post-migration filtering |

> Microsoft Lists supports indexing on up to 20 columns. The 11 recommended indexes stay well within the threshold, even as the registry grows beyond 5,000 items.

---

## 6. SharePoint Internal Field Mapping Notes

The following EA-3 SharePoint fields have registry-appropriate mappings:

| SharePoint Field (EA-3) | Registry Field (EA-4) | Mapping Notes |
|-------------------------|----------------------|---------------|
| RAE_DocumentID | DocumentID (same) | DIRECT — canonical identity |
| Title | Title (same) | DIRECT — human-readable title |
| RAE_Category | Category | DIRECT — but registry uses Choice, SharePoint uses free text |
| RAE_Subcategory | Subcategory | DIRECT |
| RAE_Owner | Owner | Lists supports Person/Group column natively |
| RAE_DocumentStatus | Status | TRANSFORM — SharePoint values (LegacyImported, Draft, Current, Obsolete, Archived, MetadataOnly) map to the canonical seven-value registry vocabulary (draft, review, approved, published, current, obsolete, archived). Migration conditions are represented via SourceSystem and MigrationStatus, not lifecycle Status. |
| RAE_Version | Version | DIRECT |
| RAE_UpdatedDate | UpdatedDate | DIRECT |
| RAE_PublicVisibility | Visibility | TRANSFORM — SharePoint values (PendingReview, Public, Internal, Restricted) map to canonical four-value registry vocabulary (public, internal, restricted, private). PendingReview is not a visibility classification; documents awaiting review use Status=review + Visibility=internal. |
| RAE_Tags | Tags | TRANSFORM — SharePoint uses Managed Metadata; registry uses semicolon text |
| RAE_LegacySourceURL | LegacySourceURL | DIRECT |
| RAE_SHA256 | _(not in registry)_ | **SHAREPOINT_ONLY** — file integrity check; no registry purpose |
| RAE_MigrationStatus | _(not in registry)_ | **SHAREPOINT_ONLY** — migration tracking only |
| RAE_DuplicateOf | DuplicateOf | DIRECT |
| RAE_Notes | Notes | DIRECT |

Fields deliberately excluded from registry (SharePoint-only): `SHA256`, `MigrationStatus`. These are migration/integrity fields with no registry governance purpose.

---

## 7. Implementation Notes

- Create as a **custom Microsoft List** (not from template)
- Apply the **RAE Metadata Record** Content Type from EA-3 (`content-types.md` §7) to the List for migration records. Future documents may use a different content type assignment.
- Person/Group columns require the List to be connected to a Microsoft 365 Group or SharePoint site with user profiles
- Choice columns must be manually maintained if taxonomy changes
- The `RAE-NNNNN` format differs from the Phase 5A `RAE-DC-NNNN` format — migration re-mapping is required
- No Power Automate flows are created in this phase (EA-4 is design only)
- No public JSON export is configured in this phase (EA-7 is the export implementation phase)

---

## Related Documents

| Document | Path |
|----------|------|
| SharePoint Site Design | `docs/m365/sharepoint-site-design.md` |
| Library Schema | `docs/m365/library-schema.md` |
| Content Types | `docs/m365/content-types.md` |
| Permissions Matrix | `docs/m365/permissions-matrix.md` |
| Migration Field Map | `docs/m365/migration-field-map.csv` |
| Registry Data Model (Phase 3.7) | `docs/document-center/REGISTRY_DATA_MODEL.md` |
| Taxonomy | `docs/document-center/taxonomy.json` |
| Validation Rules | `docs/m365/registry-validation-rules.md` |
| Lifecycle Model | `docs/m365/registry-lifecycle-model.md` |
| Owner Rules | `docs/m365/registry-owner-rules.md` |
| Views | `docs/m365/registry-views.md` |
| Export Contract | `docs/m365/registry-export-contract.md` |
| SharePoint → Registry Mapping | `docs/m365/sharepoint-registry-field-map.csv` |
