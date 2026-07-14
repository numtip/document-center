# RAE Document Registry — Owner Assignment Rules

**Phase:** M365-4 — Microsoft Lists Registry Design  
**Status:** Design (pre-implementation)  
**Last updated:** 2026-07-14  
**Applies to:** `RAE Document Registry` Microsoft List Owner column

---

## 1. Core Principle

> **Every document must have an owner.**  
> Documents without owners are invalid and must not be publicly exported.

---

## 2. Owner Column Specification

| Property | Value |
|----------|-------|
| **Column Type** | Person or Group |
| **Required** | Yes |
| **Default** | None (must be explicitly assigned) |
| **Allow multiple selections** | No (single primary owner) |
| **Show profile** | Name only (not email by default) |
| **Allow selection from** | All site users |
| **Require that this column contains information** | Yes |

### Why Person or Group over Text?

| Criterion | Person/Group | Text |
|-----------|:------------:|:----:|
| Native M365 identity | ✅ | ❌ |
| Email/name resolved automatically | ✅ | ❌ |
| Account lifecycle events (disabled, deleted) | ✅ | ❌ |
| Can be used in Power Automate approval | ✅ | ❌ |
| Validation against real users | ✅ | ❌ |
| `TBD` placeholder allowed | ❌ | ✅ |

The registry is the authoritative operational registry. `TBD` is NOT valid here — only SharePoint libraries allow `TBD` during migration.

---

## 3. Owner Types

### 3.1 Individual Owner

The Person column selects an individual M365 user. This is the **preferred owner type** for most documents.

**Use when:**
- The document has a clear responsible individual
- The document is operational or task-specific
- Accountability needs to be assigned to a named person

### 3.2 Microsoft 365 Group as Owner

Microsoft Lists supports a single Person or Group column. An M365 Group (e.g., `RAE-DC-Admin-Owners`) can be selected as the Owner.

**Use when:**
- The document is owned by a unit, not an individual
- Individual ownership is not yet confirmed
- The document is shared responsibility across a team
- The category-level owner group is appropriate

**Constraint:** Only M365 Groups (not SharePoint groups) can be selected in a Person or Group column.

---

## 4. Primary Owner Rule

| Rule | Description |
|------|-------------|
| **One primary owner per document** | Single value in the Owner column |
| **Owner must be a valid M365 user or group** | No free-text names, no `TBD` |
| **Owner is who makes governance decisions** | Status changes, Visibility changes, Review scheduling |
| **Owner is NOT necessarily the author** | The owner may delegate content creation |
| **Owner is the point of contact for the registry** | Public inquiries about document accuracy go to the Owner |

---

## 5. Backup / Steward Concept

A backup or steward is NOT a separate column in this phase. Instead:

| Strategy | Implementation |
|----------|----------------|
| **Group ownership** | If the owner is an M365 Group, the group has multiple members who can act as backup |
| **Category Owner oversight** | The Category Owner (from `permissions-matrix.md`) has Edit permission on the registry and can re-assign owners |
| **Platform Admin override** | Platform Admin has Full Control and can assign temporary owners |

> A dedicated `BackupOwner` column is deferred. If operational experience shows single-owner risk, add in a later phase.

---

## 6. Orphaned Owner Handling

An orphaned record has an Owner who is no longer valid.

### 6.1 Owner Account Disabled

| Action | Responsibility |
|--------|----------------|
| Person/Group column automatically indicates the user is no longer active | Microsoft Lists (native — shows "user not found") |
| Category Owner is notified via the "By Owner" view | Manual review (Phase M365-4); automated in Phase M365-5 |
| Category Owner assigns a new owner within 30 days | Human action |
| Platform Admin assigns temporary owner if Category Owner does not act | Escalation |

### 6.2 Owner Account Deleted

| Action | Responsibility |
|--------|----------------|
| Person/Group column preserves the name but shows "unresolved" | Microsoft Lists (native — name persists, no active account) |
| Platform Admin runs quarterly "By Owner" review to detect unresolved owners | Quarterly governance audit |
| Records with unresolved owners > 90 days are flagged as "Missing Metadata" | Manual tracking until Phase M365-5 |

---

## 7. Migration Fallback

For the 772 migration records:

| Scenario | Owner Assignment | Timeline |
|----------|-----------------|----------|
| High-confidence owner proposal (32 documents) | Pre-populate with proposed M365 group | Before registry creation |
| Medium-confidence owner proposal (5 documents) | Pre-populate with Category Owner group; individual owner TBD | Within 90 days of migration |
| Low-confidence owner proposal (3 documents) | Assign to Category Owner group for resolution | Within 90 days of migration |
| All other migration records | Assign to Category Owner group for distribution | Within 90 days of migration |

> The EA-3 design allows `Owner = TBD` in SharePoint libraries. The **registry does not accept TBD**. Migration records must have a valid M365 group as Owner before appearing in the registry.

---

## 8. Department Responsibility

| Rule | Description |
|------|-------------|
| **Department is derived** | Department is a derived column, not manually maintained |
| **Derivation source** | The `owner_group` field in `taxonomy.json` for the record's Category |
| **Manual override** | Allowed if the document's owner group differs from the category default |
| **Governance use** | Department enables roll-up reporting by organizational unit |

### Derived Mapping

| Category | Default Owner Group | Default Department |
|----------|---------------------|-------------------|
| `admin` | RAE-DC-Admin-Owners | งานบริหารและธุรการ |
| `finance-procurement` | RAE-DC-Finance-Owners | งานคลังและพัสดุ |
| `policy-planning` | RAE-DC-Policy-Owners | งานนโยบายและแผน |
| `academic-service` | RAE-DC-Academic-Owners | งานบริการวิชาการ |
| `research` | RAE-DC-Research-Owners | งานวิจัย |
| `manuals` | RAE-DC-Manuals-Owners | คู่มือปฏิบัติงาน |

---

## 9. Review Responsibility

| Review Type | Responsible Party | Frequency |
|-------------|-------------------|-----------|
| Owner validity review | Category Owner | Quarterly |
| Unresolved owner detection | Platform Admin | Quarterly |
| Owner TBD resolution in SharePoint | Category Owner | Monthly (until all resolved) |
| Registry Owner accuracy | Owner (self-review) | Annually |

---

## 10. Design Constraints

- Do NOT implement a custom RBAC system
- Do NOT create a `BackupOwner` column in this phase
- Do NOT create a separate owner approval workflow in this phase
- Do NOT replace the Person/Group column with a free-text column to allow `TBD`
- Category Owners (from `permissions-matrix.md`) are the authority for owner disputes

---

## Related Documents

| Document | Path |
|----------|------|
| Permissions Matrix | `docs/m365/permissions-matrix.md` |
| Registry Schema | `docs/m365/registry-list-schema.md` |
| Validation Rules | `docs/m365/registry-validation-rules.md` |
| Lifecycle Model | `docs/m365/registry-lifecycle-model.md` |
| Owner Confirmation Checklist | `docs/document-center/OWNER_CONFIRMATION_CHECKLIST.csv` |
| Owner Remediation Report | `docs/document-center/OWNER_REMEDIATION_REPORT.md` |
