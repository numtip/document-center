# RAE Document Center — Security & Governance Scope

**Document ID:** RAE-SEC-SCOPE-001  
**Version:** 1.0  
**Date:** July 14, 2026  
**Audience:** Maejo University IT Administration  
**Tenant:** `maejo365.sharepoint.com`

---

## 1. Purpose

This document defines the security model, governance boundaries, and operational scope for the RAE Document Center project within the Maejo University Microsoft 365 tenant (`maejo365.sharepoint.com`). It is intended for review by Maejo University IT administrators to confirm that the proposed architecture aligns with institutional security policy before deployment.

The scope covers:

- Site-level access control and permission inheritance
- Document exposure classification via metadata vocabularies
- Governance risks addressed by the RAE workflow
- Anonymous (Anyone) sharing risk and compensating controls
- A least-privilege statement for the RAE service principal

---

## 2. Site-Level Security

### 2.1 Site Privacy

The RAE Document Center is configured as a **Private** site. Access is restricted to explicitly approved members only. Unauthenticated users and tenant-wide users who are not site members cannot browse, search, or view any content within the site.

| Property | Value |
|---|---|
| Site privacy | **Private** |
| Site visibility | Hidden from search results for non-members |
| Membership approval | Controlled by site owners |

### 2.2 Permission Inheritance

The RAE Document Center operates with **default permission inheritance at the library level**. No item-level or folder-level permission breaks are employed. This ensures:

- A flat, auditable permission model
- Reduced administrative overhead
- Elimination of permission creep from nested breaks
- Consistent access behavior across all documents

### 2.3 SharePoint Groups (No Individual Permissions)

All access is managed through standard SharePoint groups:

| Group | Members | Permissions granted |
|---|---|---|
| **RAE Owners** | Document center administrators | Full Control |
| **RAE Members** | Content contributors, reviewers | Edit / Contribute |
| **RAE Visitors** | Read-only consumers | Read |

Individual user permissions are **not** assigned. Every user's effective permissions derive solely from group membership.

---

## 3. Document Exposure Model

### 3.1 Public Exposure Is Explicit and Metadata-Governed

A document becomes eligible for public visibility **only** through explicit metadata assignment. No document is publicly accessible by default. The workflow requires two metadata conditions to be satisfied before any public-facing delivery occurs:

1. `Visibility = public`
2. `Status` in (`approved`, `published`, `current`)

### 3.2 Master Files Remain in SharePoint

Original document files (the "master" copies) are stored exclusively in the RAE Document Center SharePoint library. Master files are **never** moved, copied, or transferred to any public web server, external application server, or content delivery network.

### 3.3 Public Portal Stores No Master Files

Any public-facing portal or external system that displays RAE documents consumes data via **JSON export only**. The public portal:

- Receives a read-only metadata payload and, where applicable, a **derived display copy** (e.g., a PDF rendition or HTML fragment)
- Stores **no master file** (no `.docx`, `.xlsx`, `.pdf` source files)
- Cannot mutate the source of truth in SharePoint
- Relies on periodic or event-driven export refresh

This architecture ensures that the SharePoint library remains the authoritative source and that revocation of a document's public eligibility is effective immediately upon metadata update.

---

## 4. Visibility Vocabulary

Every document in the RAE Document Center is classified with exactly one of the following visibility values:

| Value | Definition | Typical audience |
|---|---|---|
| **public** | May be published to external audiences. Eligible for public-facing portal delivery after status validation. | General public, external stakeholders |
| **internal** | Visible to all authenticated tenant users (Maejo University faculty, staff, students). | University-wide |
| **restricted** | Visible only to site members and named groups with a business need. | Specific departments or committees |
| **private** | Visible only to document owners, site owners, and explicitly authorized reviewers. | Confidential, pre-release, or personally identifiable information |

The visibility field is mandatory. A document with no assigned visibility value blocks the publishing workflow.

---

## 5. Governance Risks Addressed

### 5.1 Owner Is Mandatory

Every document record in the operational registry **must** have an assigned owner. `TBD` is **not** a valid value for the owner field. This ensures:

- Clear accountability for each document's lifecycle
- An identifiable point of contact for access reviews and status transitions
- Elimination of orphaned documents

### 5.2 Broken Public Links Are Release Blockers

The RAE workflow monitors the integrity of any public-facing links or URLs associated with a document. If a link is detected as broken (HTTP 4xx/5xx, DNS failure, or access denied):

- The document's eligibility for public delivery is automatically revoked
- A notification is raised to the document owner and site administrators
- The broken link must be resolved before the document can be re-eligible for public display

This guardrail prevents the public portal from serving dead links or exposing access errors to external audiences.

### 5.3 Approval Lifecycle via Status Transitions

Document lifecycle is governed by the `Status` field, which uses a 7-value controlled vocabulary. Transitions between statuses follow defined rules that gate public exposure:

```
draft  ──►  review  ──►  approved  ──►  published  ──►  current
                  │                        │
                  └──►  obsolete ◄─────────┘
                  │
                  └──►  archived
```

- A document with `Status = draft` or `Status = review` is not eligible for public delivery regardless of its visibility value.
- Only `Status` values `approved`, `published`, or `current` satisfy the public-delivery eligibility gate.
- `Status = obsolete` and `Status = archived` represent end-of-life states; documents in these states are excluded from public delivery.

---

## 6. Anonymous Sharing Governance Risk (CRITICAL)

### 6.1 Tenant Finding

During the tenant assessment for the RAE Document Center project, a critical configuration was observed in the Maejo University tenant (`maejo365.sharepoint.com`):

> **Anyone (anonymous) sharing links are enabled** and were confirmed as the **default sharing option** for SharePoint sites.

This means that any user with contribute or higher permissions on a SharePoint site can, by default, generate an anonymous link that grants access to **anyone** — including unauthenticated external users — without requiring sign-in.

### 6.2 Governance Risk

The default-anyone sharing configuration introduces the following risk to the RAE Document Center:

| Risk | Description |
|---|---|
| **Inadvertent exposure** | A content contributor could generate an anonymous link to a document that has not yet completed its visibility review (e.g., a `draft` document with `Visibility = restricted`). |
| **Circumvention of metadata governance** | Anonymous links grant access at the file-permission level, bypassing the RAE visibility and status metadata workflow entirely. |
| **Loss of audit trail** | Once an anonymous link is shared externally, the document owner loses the ability to track who accessed the document or to revoke access from specific individuals. |

### 6.3 RAE Compensating Controls

Because tenant-wide policy changes are outside the RAE project scope (see Section 7), the RAE Document Center implements the following **compensating controls within its own site and workflow**:

1.  **Public-delivery eligibility gate** — The RAE export pipeline explicitly validates two metadata conditions before any document is included in the public-facing output:
    - `Visibility = public` **AND**
    - `Status` in (`approved`, `published`, `current`)
    
    A document that fails this validation is excluded from the public portal regardless of any anonymous link that may exist.

2.  **Monitoring and alerting** — The RAE site includes a scheduled governance check that surfaces any document for which anonymous sharing links exist but the document metadata does not satisfy the public-delivery eligibility gate. These are flagged for owner review.

3.  **User training** — RAE content contributors and site members are trained that anonymous link sharing must only be used for documents that have completed their visibility review and whose metadata explicitly classifies them as `public`.

### 6.4 Recommendation (Within RAE Scope)

While a tenant-wide policy change is not requested (see Section 7), it is recommended that the RAE site collection be configured with a **site-level sharing policy** that restricts the default link type to "People in Maejo University" or "Specific people" rather than "Anyone." This is a site-level setting and does not affect other site collections in the tenant.

---

## 7. Least Privilege Statement

The RAE Document Center operates under a strict least-privilege model:

| Item | Status |
|---|---|
| **Global Administrator** | **Not requested.** RAE does not require any tenant-wide administrative role. |
| **Broad Graph API permissions** | **Not requested.** All SharePoint interactions use site-scoped application permissions or delegated user permissions. |
| **Tenant-wide policy changes** | **Not requested.** RAE does not ask for changes to tenant-wide sharing defaults, external identity policies, or conditional access policies. |
| **Permissions required** | **Site-level Full Control** on the RAE Document Center site collection only. This is the minimum permission needed to manage site contents, configure library settings, and operate the export workflow. |

The RAE service principal's effective permissions are scoped to a single site collection and do not extend to any other SharePoint site, OneDrive, Exchange, or Azure resource within the tenant.

---

## 8. Data Classification Notes

Documents managed in the RAE Document Center should be classified according to the following categories. The RAE workflow does not enforce these classifications programmatically but expects them to be documented in the registry metadata:

| Classification | Description | Examples |
|---|---|---|
| **Unrestricted** | No legal, regulatory, or contractual restrictions on disclosure. Suitable for public or internal visibility. | Published policies, procedural manuals, organizational charts |
| **Internal-Only** | Not sensitive but not intended for external audiences. | Draft meeting minutes, internal memos, working documents |
| **Sensitive** | Contains information that, if disclosed, could cause moderate harm to the university or individuals. | Staff performance data, procurement details, pending legal matters |
| **Confidential** | Contains information protected by law, regulation, or binding agreement. | Student records (PII), research data under NDA, financial audits |

**Note on PII:** Any document containing personally identifiable information (PII) must be assigned `Visibility = private` and should be flagged in the document registry.

---

## 9. Recommendations

The following recommendations are made for the RAE Document Center site. None of these require tenant-wide administrative changes:

1.  **Adopt a site-level default sharing link type of "People in Maejo University"** for the RAE site collection. This is configurable per site and does not alter the tenant-wide default. It reduces the risk of accidental anonymous link generation without affecting other sites.

2.  **Enable site-level access requests** so that non-members who attempt to access the site can submit a request that is routed to the RAE Owners group for approval.

3.  **Schedule quarterly access reviews** for the RAE Owners, RAE Members, and RAE Visitors groups to ensure membership remains current and appropriate.

4.  **Establish a visibility audit cadence** — a monthly automated or manual review of all documents with `Visibility = public` to confirm they still satisfy the institution's disclosure criteria.

5.  **Document the RAE status transition rules** in the operational registry so that all content contributors understand which statuses gate public delivery.

6.  **Publish this scope document** in the RAE Document Center as a reference for all site members and for future IT administration handovers.

---

*End of document*
