# Project Memory Freeze v1

**Version**: 1.0.1  
**Effective**: 2026-07-16  
**Purpose**: Preserve operational knowledge from EA-3 through EA-12 for future maintainers

---

## 1. Lessons Learned

| Topic | Lesson |
|-------|--------|
| Migration sequencing | Pilot (6) → expanded (25) → scale (100) → full corpus (496) de-risked production |
| Idempotent Registry | AUTO_UPSERT by DocumentID eliminates duplicate rows on re-sync |
| Artifact reconciliation | Faster and more reliable than live REST full-library scan |
| Portal clarity | GitHub Pages is preview; SharePoint DC is production — document explicitly |
| Governance timing | Defer owners/workflows until corpus migration complete |
| Fast mode | Wave-level QA + append-only state reduces orchestration overhead |
| Single browser worker | Only one M365 Playwright session; parallel Chromium causes profile lock |

---

## 2. Known Pitfalls

| Pitfall | Symptom | Prevention |
|---------|---------|------------|
| REST `$top=500` without pagination | Library count 594 instead of 627 | Always paginate with `$skip` |
| Browser profile lock | Script hangs on launch | Run `_ea10_release_profile.py` first |
| `git` alias via RTK | `git: '\' is not a git command` | Use `G:\Git\cmd\git.exe` directly |
| Manual state file edit | JSON corruption, resume failure | Append-only JSONL for state |
| Batch tag as int | Subprocess type error | Cast batch tags to string |
| Assuming GitHub Pages = production | Wrong portal URL communicated | Reference EA-11A production URL doc |
| `--force` re-upload | Duplicate files, broken idempotency | Never use force on migration scripts |
| `file://` for portal QA | Fetch CORS failures | Use local HTTP server |

---

## 3. Pagination Issue ($top=500)

SharePoint REST returns max 500 items per request. Research library has 530+ items.

**Fix applied (EA-10)**:

```text
GET .../items?$top=500&$skip=0
GET .../items?$top=500&$skip=500
... until empty page
```

Implemented in `_registry_upsert.py` paginated library scan. Any future scan script must use pagination.

---

## 4. Registry Synchronization

| Property | Value |
|----------|-------|
| Tool | `_ea8_registry_sync.py --sync-all` |
| Mode | AUTO_UPSERT |
| Key | DocumentID |
| Per-doc | `--doc RAE-00009` |

**Rules**:

- Sync after any library upload batch
- Idempotent — safe to re-run
- Never delete Registry rows without change control

---

## 5. SharePoint REST

| Pattern | Usage |
|---------|-------|
| ValidateUpdateListItem | Metadata apply after upload |
| List items REST | Library scan, item lookup |
| `$select` + `$filter` | Targeted queries |
| Paginated `$skip/$top` | Full library inventory |

**Avoid**: Unpaginated full-library scan on 500+ item libraries (hangs/timeouts).

---

## 6. Browser Profile Rules

| Rule | Detail |
|------|--------|
| Profile path | `.browser-profile/m365` |
| Sessions | One at a time |
| Lock recovery | `_ea10_release_profile.py` |
| Gitignore | `.browser-profile/` never committed |
| Auth | Manual login once; persistent cookies |

---

## 7. RTK Rules

| Rule | Detail |
|------|--------|
| Command prefix | `rtk python`, `rtk npm` for sandboxed execution |
| Git | PowerShell aliases `git` to RTK — use `G:\Git\cmd\git.exe` for git ops |
| Node PATH | `$env:PATH = "G:\nodejs;" + $env:PATH` if npm not found |
| PowerShell | Use `;` not `&&` for command chaining |

---

## 8. Token Reduction Strategy

| Technique | Applied in |
|-----------|------------|
| Wave-level QA (not per-doc) | EA-10 fast mode |
| Append-only state JSONL | EA-10 multi-worker |
| Artifact-based reconcile | EA-11 (skip live REST scan) |
| Resume skip-on-seen | All batch migrations |
| Minimal logging in fast mode | EA-10 fast runner |
| Co-worker model | Only Worker M365 uses browser |

---

## 9. Co-Worker Strategy

```text
Worker M365  →  Browser automation, upload, Registry sync
Worker Docs  →  Reports, reconciliation, state analysis
Worker QA    →  Portal smoke, build/lint validation
```

Only Worker M365 holds the browser profile lock. Other workers consume CSV/JSON artifacts.

---

## 10. Release History

| Version | Tag | Date | Summary |
|---------|-----|------|---------|
| 1.0.0 | `document-center-v1.0.0` | 2026-07-16 | Production freeze — 627/627/627 |
| 1.0.1 | `document-center-v1.0.1` | 2026-07-16 | Canonical repository elevation |

---

## 11. Production URLs

| Environment | URL |
|-------------|-----|
| **Production portal** | `https://maejo365.sharepoint.com/sites/msteams_54adc4/SitePages/RAE-Document-Center.aspx` |
| **Registry admin** | `…/Lists/RAE%20Document%20Registry/AllItems.aspx` |
| **Preview (demo)** | `https://numtip.github.io/document-center/` (3 records) |

---

## 12. Repository Philosophy

1. **SharePoint stores files; Registry stores metadata; Git stores standards.**
2. **Freeze production; evolve governance through ADRs.**
3. **Evidence over assumptions** — CSV/JSON artifacts are reconciliation truth.
4. **Preview ≠ Production** — always label environments explicitly.
5. **Idempotency everywhere** — DocumentID is the universal key.
6. **Defer governance until corpus is complete** — then activate via change control.

---

## Related Documents

- [docs/release/PROJECT_CLOSEOUT_REPORT.md](../release/PROJECT_CLOSEOUT_REPORT.md)
- [docs/release/OPERATION_RUNBOOK_v1.0.md](../release/OPERATION_RUNBOOK_v1.0.md)
- [docs/canonical/REFERENCE_STANDARDS.md](REFERENCE_STANDARDS.md)
