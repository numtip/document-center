# RAE Document Center — Site Provisioning Request
## คำขอจัดตั้งไซต์ศูนย์เอกสารสำนักวิจัยฯ

**Request Reference:** RAE-PROV-001  
**Request Date:** 14 July 2026  
**Priority:** Normal  
**Status:** Draft — Pending Admin Review

---

## 1. Request Summary

This document formally requests the creation of a Microsoft 365 Team Site and associated Microsoft 365 Group to serve as the centralized document repository for the Research Administration and Evaluation (RAE) unit of Maejo University (MJU).

The site will host RAE operational documents, reports, templates, and related content. All site configuration beyond provisioning (libraries, columns, content types, lists, automation, and migration) will be performed by the RAE team after the site is created.

---

## 2. Requested Resource

| Item | Detail |
|---|---|
| **Site Name (EN)** | RAE Document Center |
| **Site Name (TH)** | ศูนย์เอกสารสำนักวิจัยฯ |
| **Recommended URL** | `https://maejo365.sharepoint.com/sites/RAEDocumentCenter` |
| **Site Type** | Team Site (connected to Microsoft 365 Group) |
| **Privacy** | Private |
| **Language** | Thai and English |

---

## 3. Tenant Context

Parameters below were verified during tenant readiness assessment (July 2026).

| Parameter | Status / Value |
|---|---|
| **Tenant Name** | Maejo University (MJU) — มหาวิทยาลัยแม่โจ้ |
| **SharePoint Hostname** | `maejo365.sharepoint.com` |
| **Verification Account** | `researchmju@mju.ac.th` |
| **SharePoint Online** | CONFIRMED |
| **Microsoft Lists** | CONFIRMED AVAILABLE |
| **Site Self-Creation (researchmju)** | NOT AVAILABLE — Admin provisioning required |
| **Managed Metadata / Term Store** | ADMIN REQUIRED — Access needs to be confirmed separately |
| **Anonymous / Anyone Links** | CONFIRMED ENABLED (tenant-level policy) |

---

## 4. Site Parameters

| Parameter | Value | หมายเหตุ |
|---|---|---|
| **Site Title (EN)** | RAE Document Center | |
| **Site Title (TH)** | ศูนย์เอกสารสำนักวิจัยฯ | ชื่อภาษาไทยสำหรับแสดงผล |
| **URL Path** | `/sites/RAEDocumentCenter` | ขอให้ใช้ URL นี้ |
| **Template / Kind** | Team Site (STS#3) | Connected to M365 Group |
| **Privacy Setting** | Private | Only members can access |
| **Description (EN)** | Central document repository for the Research Administration and Evaluation (RAE) unit, Maejo University. | |
| **Description (TH)** | ศูนย์รวมเอกสารของหน่วยงานวิจัยและประเมินผล (RAE) มหาวิทยาลัยแม่โจ้ | |
| **Hub Association** | None (standalone) | อาจเชื่อมต่อ Hub ในภายหลัง |
| **Geo Location** | Default (Thailand) | |
| **Time Zone** | (SE Asia Standard Time) UTC+07:00 | |

---

## 5. Microsoft 365 Group Parameters

| Parameter | Value |
|---|---|
| **Group Name (EN)** | RAE Document Center |
| **Group Name (TH)** | ศูนย์เอกสารสำนักวิจัยฯ |
| **Group Alias (Email)** | `RAEDocumentCenter` (suggested) |
| **Privacy** | Private |
| **Auto-create Microsoft Teams Team** | **No** — Do not create a Teams team |
| **Subscribe new members** | No |
| **Send calendar invites** | No |
| **Classification** | Internal (if available in tenant) |

---

## 6. Initial Owner Requirement

> **Owner (proposed):** _\[Name of approved RAE site owner to be filled by MJU IT/Microsoft 365 Admin\]_
>
> **ตำแหน่ง:** _\[Role / Department\]_
>
> **Email:** _\[MJU email address\]_

The RAE unit will provide the name and email of the approved site owner once administrative approval is granted. The site owner must be an active user in Maejo University's Entra ID (Azure AD).

---

## 7. Admin Actions Requested

This request is limited to the following provisioning actions. No additional configuration is requested.

| # | Action | รายละเอียด |
|---|---|---|
| 1 | **Create Team Site** | Provision a new SharePoint Team Site at `/sites/RAEDocumentCenter` |
| 2 | **Create / Associate M365 Group** | Provision a Microsoft 365 Group named "RAE Document Center" and link it to the site |
| 3 | **Set Privacy = Private** | Ensure both the site and the associated group are set to **Private** |
| 4 | **Assign Approved Site Owner** | Add the RAE-designated owner to the **Site Owners** group |
| 5 | **Confirm Site URL** | Verify the site is accessible at the requested URL |
| 6 | **Confirm Group Creation** | Verify the M365 Group is created and the alias/email is operational |
| 7 | **Confirm Term Store Process / Contact** | Provide contact or process for requesting Managed Metadata / Term Store access |

---

## 8. Actions NOT Requested (RAE Will Handle)

To keep provisioning scope minimal, the RAE team will perform the following tasks after the site is created. **No admin action is required** for these items.

| # | Item | หมายเหตุ |
|---|---|---|
| — | **Create document libraries** (6 libraries) | RAE team will create and configure all libraries post-provisioning |
| — | **Create site columns** (17 columns) | RAE team will define and publish site columns |
| — | **Create content types** | RAE team will create and associate content types |
| — | **Create Registry List** | RAE team will provision the Registry List with its 22 columns |
| — | **Create Power Automate flows** | RAE team will deploy and manage all automation flows |
| — | **Configure public / anonymous document links** | RAE team will manage sharing links on a per-document basis as needed |
| — | **Perform data migration** | RAE team handles all content migration into the site |
| — | **Hub site association** | May be requested separately at a later date if needed |

---

## 9. Post-Provision Responsibility (RAE)

Upon site creation, the RAE team will take ownership of the following:

1. **Verify site accessibility** — Confirm the site and group are reachable with correct permissions.
2. **Configure site structure** — Create libraries, columns, content types, and lists per the RAE information architecture.
3. **Set up permissions** — Manage site-level and item-level permissions as required.
4. **Deploy automation** — Create and test Power Automate flows for document workflows.
5. **Migrate content** — Transfer existing RAE documents into the new site.
6. **User onboarding** — Add members and communicate site access procedures to RAE staff.
7. **Ongoing administration** — Manage site content, users, and configuration without requiring further SharePoint Admin intervention.

---

## 10. Validation Information Required Back from Admin

After provisioning is complete, the MJU Microsoft 365 Admin team is requested to confirm the following:

| # | Item | Format |
|---|---|---|
| 1 | Site URL (confirmed) | Full HTTPS URL |
| 2 | M365 Group email alias | email@maejo365.onmicrosoft.com |
| 3 | Assigned site owner name and email | Name + @mju.ac.th email |
| 4 | Site and group privacy = Private | Yes / No confirmation |
| 5 | Term Store contact or request process | Contact name / email or link to process |

These validation items will be recorded in the RAE tenant evidence register.

---

## 11. Technical Contact / Owner

| Role | Name | Email |
|---|---|---|
| **RAE Technical Contact** | _[To be filled]_ | _[To be filled]_ |
| **RAE Site Owner (proposed)** | _[To be filled — requires admin approval]_ | _[To be filled — @mju.ac.th]_ |
| **MJU M365 Admin** | _[MJU IT / Microsoft 365 Admin Team]_ | _[Admin contact email]_ |

---

*This request was prepared by the RAE team based on verified tenant evidence collected July 2026. For questions or clarifications, please contact the RAE technical contact above.*
