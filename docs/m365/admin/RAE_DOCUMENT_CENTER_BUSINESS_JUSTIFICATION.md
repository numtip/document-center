# RAE Document Center — Business Justification

**Submitted to:** Maejo University M365 Administration Team  
**Unit:** สำนักวิจัยและส่งเสริมวิชาการการเกษตร (Office of Agricultural Research and Extension)  
**Tenant:** maejo365.sharepoint.com  
**Date:** July 2026

---

## 1. Problem Statement

The Office of Agricultural Research and Extension currently relies on the legacy WTMS platform for document distribution. WTMS is being decommissioned, and no equivalent governed document platform exists to replace it. In parallel, operational files are stored across multiple VPS servers with no central registry, no version history, and no assigned ownership. This has resulted in:

- **Fragmented file storage** — documents scattered across servers with no single source of truth.
- **Broken links** — WTMS-dependent URLs that fail as the system is retired.
- **No version control** — inability to track revisions to policies, procedures, and governance documents.
- **No ownership tracking** — unclear accountability for document accuracy and currency.

## 2. Purpose

Establish a single, governed SharePoint document platform for the Office of Agricultural Research and Extension. The RAE Document Center will serve as the authoritative file repository and operational registry for all units within the office, replacing ad-hoc VPS storage and the outgoing WTMS distribution model.

## 3. Microsoft 365 Role

Microsoft 365 (SharePoint + Microsoft Lists) is the platform layer. It provides:

| Capability | Role |
|---|---|
| **Storage** | Authoritative file repository (SharePoint document libraries) |
| **Versioning** | Built-in version history for all governed documents |
| **Metadata** | Custom column schemas for classification, owner, expiry, and retention |
| **Ownership** | Assigned document owners with review cadence enforcement |
| **Lifecycle** | Retention labels, content type policies, and disposition workflows |

Microsoft Lists serves as the **authoritative operational registry** — tracking tenants, sites, provisioning status, and migration state.

## 4. Public Website Role

The public-facing RAE website serves **discovery and presentation only**:

- The website consumes a stateless JSON export generated from SharePoint.
- No master files are stored on the website server.
- All authoritative content resides in M365.
- The website is a presentation layer; M365 is the system of record.

This one-way flow (M365 → JSON → Website) ensures that decommissioning or redesigning the website never risks data loss.

## 5. Systems Served

| System | Consumption Model |
|---|---|
| **RAE Website** | Stateless JSON export from SharePoint |
| **Green Office** | Direct SharePoint access for evidence documentation |
| **Research Portal** | Document metadata via SharePoint API |
| **Learning Center** | Curated file sets published from governed libraries |

## 6. Institutional Benefits

1. **Reduce VPS dependencies** — eliminate file storage on standalone servers, lowering maintenance and security surface area.
2. **Eliminate broken links** — replace WTMS URLs with persistent M365 links governed by the university tenant.
3. **Ownership accountability** — every document has an assigned owner and review schedule.
4. **Version control** — full revision history for governance documents, policies, and operational records.
5. **Green Office evidence** — structured document repository for ISO 14001 / Green Office certification evidence.
6. **AI-ready governed sources** — clean, metadata-tagged document corpus suitable for future M365 Copilot and AI service integration.

## 7. Architecture Principle: Build Less. Govern More.

The RAE Document Center explicitly avoids custom development:

- **SharePoint** is the file platform — no custom storage code.
- **Microsoft Lists** is the operational registry — no custom database.
- **The public website** is stateless — no master files on the web server.
- **Metadata and lifecycle** are enforced by M365 platform capabilities, not custom scripts.

The university invests in **governance configuration**, not application code. This minimizes maintenance liability, reduces vendor lock-in, and aligns with Maejo University M365 standards.

---

**Prepared by:** Office of Agricultural Research and Extension  
**Approval required:** Maejo University M365 Administration
