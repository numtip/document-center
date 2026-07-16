# Operation Runbook v1.0

**Version**: 1.0.0  
**Effective**: 2026-07-16  
**Site**: `https://maejo365.sharepoint.com/sites/msteams_54adc4`

---

## 1. Daily Operation

| Task | Action |
|------|--------|
| Verify portal access | Open Document Center page; confirm Registry list loads |
| Check for failed uploads | Review latest migration results CSV (no new uploads expected post v1.0) |
| User support | Direct users to SharePoint Document Center URL |

**Production URL**:

```text
https://maejo365.sharepoint.com/sites/msteams_54adc4/SitePages/RAE-Document-Center.aspx
```

---

## 2. Monthly QA

| Check | Command / Method | Pass criteria |
|-------|------------------|---------------|
| Registry duplicate scan | `rtk python .migration/rae-wtms/tools/_ea8_registry_sync.py --count-duplicates` | duplicates = 0 |
| Registry sync | `rtk python .migration/rae-wtms/tools/_ea8_registry_sync.py --sync-all` | FAILED = 0 |
| Corpus reconcile | `rtk python .migration/rae-wtms/tools/_ea11_corpus_artifacts.py` | 627/627/627 |
| Spot URL check | Sample 10 Storage URLs from Registry | HTTP 200 (authenticated) |
| Portal smoke test | Open Document Center + one library per category | Pages load |

---

## 3. Registry Maintenance

**Sync all library items to Registry**:

```powershell
rtk python .migration/rae-wtms/tools/_ea8_registry_sync.py --sync-all
```

**Sync single document**:

```powershell
rtk python .migration/rae-wtms/tools/_ea8_registry_sync.py --doc RAE-00009
```

**Rules**:

- Idempotency key = DocumentID
- Never delete Registry rows without change control
- Never use `--force` on migration scripts

---

## 4. Backup

| Asset | Backup method |
|-------|---------------|
| SharePoint files | Microsoft 365 tenant backup / retention policies |
| Registry List | Included in SharePoint site backup |
| Migration evidence | Git repository + `.migration/rae-wtms/ea-*/` artifacts |
| Canonical manifest | `migration/sharepoint-migration-manifest.csv` |

---

## 5. Recovery

| Scenario | Procedure |
|----------|-----------|
| Missing Registry row, file exists | Run `--sync-all` or `--doc {DocumentID}` |
| Missing file, Registry exists | Investigate library; do not fabricate files |
| Broken Storage URL | Run `_ea7b_fix_registry_urls.py` pattern; verify URL format |
| Duplicate DocumentID | Stop; escalate — do not auto-delete |
| Auth profile expired | Re-authenticate `.browser-profile/m365` once; retry |

---

## 6. Monitoring

| Signal | Threshold | Action |
|--------|-----------|--------|
| Registry count drift | ≠ 627 | Run corpus reconcile; investigate |
| Duplicate DocumentIDs | > 0 | Stop uploads; escalate |
| Broken URLs | > 0 | Patch Registry; verify library item |
| SharePoint search lag | PENDING_INDEX | Accept if direct URL resolves |

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Document Center page empty | Registry web part disconnected | Re-bind List web part to RAE Document Registry |
| File 404 | Wrong library or deleted item | Verify manifest + library item ID |
| Registry count 594 in scan | REST pagination ($top=500) | Use paginated scan scripts |
| Browser profile lock | Stale Chromium | `_ea10_release_profile.py` |
| GitHub Pages shows 3 docs | Expected — preview mode | Do not treat as production issue |

---

## 8. Future Migration Procedure (Frozen — Requires Change Control)

Post v1.0, **no additional migration** is authorized without:

1. Architecture baseline amendment
2. New EA phase approval
3. Updated acceptance certificate

If authorized in future:

1. Reconcile baseline (manifest + SharePoint + Registry)
2. Select from READY manifest only
3. Preflight → batch migrate → Registry sync
4. QA gate before next batch
5. Update runbook and release notes

---

## 9. Contacts & Escalation

| Level | Contact |
|-------|---------|
| L1 | Document Center portal owner |
| L2 | SharePoint site admin (`researchmju@mju.ac.th`) |
| L3 | Migration engineering (repository maintainers) |

---

## 10. Related Documents

- `docs/release/ARCHITECTURE_BASELINE_v1.0.md`
- `docs/release/DOCUMENT_CENTER_v1.0_PRODUCTION_FREEZE.md`
- `docs/m365/ea-11-production-hardening-backlog.md`
