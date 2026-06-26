# Category Audit Report — Phase 5A.7

**Project:** RAE Document Center  
**Phase:** 5A.7 — Category Validation  
**Date:** 2026-06-18  
**Taxonomy version:** 1.0.0

---

## Summary

Validated all 40 registry candidate documents against the locked taxonomy (`taxonomy.json`). All documents use valid category IDs, but all are concentrated in a single category — raising a classification quality concern.

| Metric | Value |
|--------|-------|
| Total documents audited | 40 |
| Valid category IDs | 40 (100%) |
| Invalid category IDs | 0 |
| Categories with documents | 1 of 6 |
| Orphan categories | 5 of 6 |
| Potential misclassifications | 8 |

---

## Category Distribution

| Category ID | Category Name (TH) | Folder | Documents | Percentage |
|-------------|--------------------|--------|-----------|------------|
| `admin` | งานบริหารและธุรการ | `01-งานบริหารและธุรการ` | 40 | 100% |
| `finance-procurement` | งานคลังและพัสดุ | `02-งานคลังและพัสดุ` | 0 | 0% |
| `research` | งานวิจัย | `03-งานวิจัย` | 0 | 0% |
| `academic-service` | งานบริการวิชาการ | `04-งานบริการวิชาการ` | 0 | 0% |
| `policy-planning` | งานนโยบายและแผน | `05-งานนโยบายและแผน` | 0 | 0% |
| `manuals` | คู่มือปฏิบัติงาน | `06-คู่มือปฏิบัติงาน` | 0 | 0% |

---

## Why All Admin?

This is **expected at this stage** because:

1. The only legacy source processed is `dlw1.MD` — which is the **admin tab** of the original website.
2. The original website had 3 tabs: แบบฟอร์ม (forms), คู่มือ-ตัวอย่าง (manuals-samples), งานยานพาหนะ (vehicles).
3. All 3 tabs were under the same admin page (`wtms_webpageDetail.aspx?wID=1909`).
4. Documents from `finance-procurement`, `research`, `academic-service`, `policy-planning` categories have not yet been inventoried from other legacy sources.

**This is NOT a taxonomy problem — it's an inventory completeness issue.**

---

## Orphan Categories (Unused)

| Category ID | Category Name | Description | Impact |
|-------------|---------------|-------------|--------|
| `finance-procurement` | งานคลังและพัสดุ | เอกสารด้านพัสดุ คลัง จัดซื้อจัดจ้าง | No documents yet — need to inventory procurement forms |
| `research` | งานวิจัย | เอกสารด้านการวิจัย รายงานผล | No documents yet — need to inventory research docs |
| `academic-service` | งานบริการวิชาการ | เอกสารด้านบริการวิชาการ การอบรม | No documents yet — need to inventory academic service docs |
| `policy-planning` | งานนโยบายและแผน | เอกสารด้านนโยบาย แผนยุทธศาสตร์ | No documents yet — need to inventory policy docs |
| `manuals` | คู่มือปฏิบัติงาน | คู่มือปฏิบัติงาน ขั้นตอนการทำงาน | No documents yet — need to inventory manuals |

---

## Potential Misclassifications

The following documents currently in `admin` may belong in other categories based on their content:

| Document | Title | Current | Suggested | Reason |
|----------|-------|---------|-----------|--------|
| RAE-DC-0025 | ระเบียบงานสารบรรณว่าด้วย ระบบสารบรรณอิเล็กทรอนิกส์ | admin | manuals | Standing regulation / operational manual |
| RAE-DC-0026 | การใช้ตรามหาวิทยาลัยและข้อความต่างๆ ในหนังสือ | admin | manuals | Brand usage guideline / reference manual |
| RAE-DC-0027 | ตัวอย่างหนังสือราชการ หนังสือภายใน | admin | manuals | Sample letter reference / operational guide |
| RAE-DC-0028 | ตัวอย่างหนังสือราชการ หนังสือภายนอก | admin | manuals | Sample letter reference / operational guide |
| RAE-DC-0029 | ตัวอย่างหนังสือราชการ คำสั่ง | admin | manuals | Sample letter reference / operational guide |
| RAE-DC-0030 | ตัวอย่างหนังสือราชการ ประกาศ | admin | manuals | Sample letter reference / operational guide |
| RAE-DC-0031 | ตัวอย่างหนังสือราชการ หนังสือประทับตรา | admin | manuals | Sample letter reference / operational guide |
| RAE-DC-0033 | หลักเกณฑ์วิธีการประเภทการลาฯ พ.ศ.2561 | admin | policy-planning | Leave policy regulation |

### Decision: Keep as Admin?

The original website placed all these under "งานบริหารและธุรการ" (Administration). For consistency with the legacy site and to avoid confusion during initial migration, **it is acceptable to keep all 40 documents in `admin`** for now.

Reclassification can happen in a future governance phase once the full inventory across all categories is complete.

---

## Category Quality Assessment

| Criterion | Score | Notes |
|-----------|-------|-------|
| All categories exist in taxonomy | ✅ Pass | All 6 category IDs are valid |
| No empty categories on active docs | ✅ Pass | All 40 docs have `admin` |
| No invalid category IDs | ✅ Pass | No misspellings or unknown IDs |
| Category diversity | ⚠️ Concern | 100% in one category — expected but needs future attention |
| Misclassification risk | ⚠️ Medium | 8 documents may belong in other categories |
| Orphan categories | ⚠️ 5 unused | Expected — other legacy sources not yet inventoried |

---

## Recommendations

1. **Keep `admin` as-is for initial migration** — Avoid reclassifying during OneDrive move to reduce complexity.
2. **Plan Phase 5B.5+ for other categories** — Inventory documents from `finance-procurement`, `research`, `academic-service`, `policy-planning`, and `manuals` from additional legacy sources.
3. **Reclassify after full inventory** — Once all categories have documents, review the 8 potential misclassifications above.
4. **Add category source tracking** — Future migration matrices should note which legacy page/source each document came from to validate category assignment.
