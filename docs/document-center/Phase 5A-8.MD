Starting **Phase 5A.8 — Registry Remediation**. Let me begin with the workspace check. 

Created 10 todos

Ran terminal command: rtk git status --short
Completed with input: rtk git status --short

Ran terminal command: rtk find docs/document-center -type f | sort

All 9 required Phase 5A.7 input files verified present. Let me read the key data files needed for remediation: 

Read [](file:///g%3A/ProjectAI/document-center/docs/document-center/audit-matrix.csv)

Read [](file:///g%3A/ProjectAI/document-center/docs/document-center/owner-assignment-proposal.csv)

Read [](file:///g%3A/ProjectAI/document-center/docs/document-center/legacy-link-audit.csv#1-1), lines 1 to 50

I have all the data needed. Now let me proceed through all phases. Starting with Phase 2 — Readiness Score Formula Audit: 

Starting: *Phase 2: Readiness score formula audit* (2/10)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/READINESS_SCORE_FORMULA.md)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/readiness-score-breakdown.csv)

Phase 2 done. Now Phase 3 — Audit findings triage: 

Starting: *Phase 3: Audit findings triage* (3/10)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/audit-remediation-plan.csv)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/AUDIT_REMEDIATION_REPORT.md)

Phase 3 done. Now Phase 4 — Owner remediation pack: 

Starting: *Phase 4: Owner remediation pack* (4/10)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/OWNER_CONFIRMATION_CHECKLIST.csv)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/OWNER_REMEDIATION_REPORT.md)

Phase 4 done. Now Phase 5 — Review document resolution: 

Starting: *Phase 5: Review document resolution* (5/10)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/review-resolution.csv)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/REVIEW_RESOLUTION_REPORT.md)

Phase 5 done. Now Phase 6 — Merge decision pack: 

Starting: *Phase 6: Merge decision pack* (6/10)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/merge-decision-pack.csv)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/MERGE_DECISION_REPORT.md)

Phase 6 done. Now Phase 7 — Legacy URL sample validation: 

Starting: *Phase 7: Legacy URL sample validation* (7/10)

Let me test a sample of URLs using safe HEAD requests only: 

Ran terminal command: cd g:\ProjectAI\document-center; $urls = @(
    @{id="RAE-DC-0001"; group="keep"; url="https://erp.mju.ac.th/openFile.aspx?id=Nzk4NTgw&method=inline"},
    @{id="RAE-DC-0007"; group="keep"; url="https://erp.mju.ac.th/openFile.aspx?id=NTMxMTM3&method=inline"},
    @{id="RAE-DC-0014"; group="keep"; url="https://erp.mju.ac.th/openFile.aspx?id=NDk4Mzky&method=inline"},
    @{id="RAE-DC-0027"; group="merge"; url="http://www.general.mju.ac.th/wtms_document_download.aspx?id=MTgyMjQ="},
    @{id="RAE-DC-0028"; group="merge"; url="https://erp.mju.ac.th/openFile.aspx?id=NDY2Mzc1&method=inline"},
    @{id="RAE-DC-0032"; group="rewrite"; url="http://personnel.mju.ac.th/edoc/forms/10789.pdf"},
    @{id="RAE-DC-0022"; group="review"; url="https://erp.mju.ac.th/openFile.aspx?id=NDgwMDg4&method=inline"},
    @{id="RAE-DC-0034"; group="review"; url="http://personnel.mju.ac.th/leave.php"},
    @{id="RAE-DC-0035"; group="random"; url="http://www.erp.mju.ac.th/openFile.aspx?id=MzI0MDcz&method=inline"},
    @{id="RAE-DC-0039"; group="random"; url="http://researchex.rae.mju.ac.th/form/05-report1.docx"}
); foreach ($u in $urls) { try { $r = Invoke-WebRequest -Uri $u.url -Method Head -TimeoutSec 10 -UseBasicParsing -ErrorAction Stop; Write-Output "$($u.id)|$($u.group)|$($r.StatusCode)|reachable" } catch { $code = $_.Exception.Response.StatusCode.value__; if ($code) { Write-Output "$($u.id)|$($u.group)|$code|$($_.Exception.Message)" } else { Write-Output "$($u.id)|$($u.group)|unknown|$($_.Exception.Message)" } } }

Excellent — got real HTTP status codes. Let me create the sample validation CSV and report: 

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/legacy-url-sample-validation.csv)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/LEGACY_URL_SAMPLE_VALIDATION_REPORT.md)

Phase 7 done. Now Phase 8 — Remediated registry candidate. Let me create the generator script: 

Starting: *Phase 8: Remediated registry candidate* (8/10)

Created [](file:///g%3A/ProjectAI/document-center/scripts/generate-remediated-registry.ts)

Ran terminal command: npx tsx scripts/generate-remediated-registry.ts docs/document-center/document-registry.draft.json docs/document-center/owner-assignment-proposal.csv docs/document-center/review-resolution.csv docs/document-center/merge-decision-pack.csv docs/document-center/taxonomy.json docs/document-center/document-registry.remediated.json 2>&1

28 documents are now `ready-for-onedrive-prep`. Now Phase 9 — create the remediated registry validator: 

Starting: *Phase 9: Validators* (9/10)

Created [](file:///g%3A/ProjectAI/document-center/scripts/validate-remediated-registry.ts)

Now run all three validators: 

Ran terminal command: Write-Host "=== 1. Matrix Validator ===" ; npx tsx scripts/validate-document-migration-matrix.ts docs/document-center/migration-matrix.v2.csv 2>&1

Ran terminal command: Write-Host "=== 2. Registry Draft Validator ===" ; npx tsx scripts/validate-document-registry.ts docs/document-center/document-registry.draft.json docs/document-center/taxonomy.json 2>&1

Ran terminal command: Write-Host "=== 3. Remediated Registry Validator ===" ; npx tsx scripts/validate-remediated-registry.ts docs/document-center/document-registry.remediated.json docs/document-center/taxonomy.json 2>&1

All 3 validators pass. Now Phase 10 — final report: 

Starting: *Phase 10: Final report* (10/10)

Created [](file:///g%3A/ProjectAI/document-center/docs/document-center/PHASE5A8_REGISTRY_REMEDIATION_REPORT.md)

Now final verification: 

Ran terminal command: rtk find docs/document-center -type f | sort

Completed: *Phase 10: Final report* (10/10)

---

## Phase 5A.8 — Final Response

### Decision: PARTIAL

Registry remediation complete. 28 documents ready for OneDrive prep; 12 need human decisions.

### Readiness Score: 43/100 → 76/100 (+33)

### Ready for OneDrive Prep: 28 documents

### Needs Human Decision: 12 documents
- 5 medium-confidence owners (needs-confirmation)
- 4 review documents (needs-human-decision)
- 3 low-confidence owners (unresolved)

### Owners
- **Proposed:** 40 (32 high + 5 medium + 3 low)
- **Unresolved:** 3 (RAE-DC-0023, 0024, 0034)

### Review Docs
- **Resolved (recommendation made):** 4
- **Unresolved (awaiting human):** 4
  - RAE-DC-0022 → recommend keep
  - RAE-DC-0023 → recommend archive
  - RAE-DC-0024 → recommend archive
  - RAE-DC-0034 → recommend drop (PHP page confirmed)

### Merge Docs
- **Canonical proposed:** 2 groups (RAE-DC-0027, RAE-DC-0004)
- **Unresolved:** 7 source documents awaiting human decision

### Files Created (15)
1. READINESS_SCORE_FORMULA.md
2. readiness-score-breakdown.csv
3. audit-remediation-plan.csv
4. AUDIT_REMEDIATION_REPORT.md
5. OWNER_CONFIRMATION_CHECKLIST.csv
6. OWNER_REMEDIATION_REPORT.md
7. review-resolution.csv
8. REVIEW_RESOLUTION_REPORT.md
9. merge-decision-pack.csv
10. MERGE_DECISION_REPORT.md
11. legacy-url-sample-validation.csv
12. LEGACY_URL_SAMPLE_VALIDATION_REPORT.md
13. document-registry.remediated.json
14. generate-remediated-registry.ts
15. validate-remediated-registry.ts

### Validation Results
- Matrix validator: ✅ PASSED
- Registry draft validator: ✅ PASSED
- Remediated registry validator: ✅ PASSED

### Sample URL Validation
- 8/10 reachable (200)
- 2/10 broken (404): RAE-DC-0027 PDF, RAE-DC-0032 PDF
- RAE-DC-0034 PHP page confirmed live (validates drop recommendation)

### Recommended Next Phase: Phase 5A.9 — Human Decision Import

Human decisions needed before Phase 5B.0:
1. Confirm 32 high-confidence owner proposals
2. Resolve 5 medium-confidence owner questions
3. Investigate 3 low-confidence owners
4. Confirm 4 review resolutions
5. Decide 2 merge groups
6. Locate 2 broken URL alternatives

**Alternative:** Phase 5B.0 can start in parallel for the 28 `ready-for-onedrive-prep` documents.

Made changes.