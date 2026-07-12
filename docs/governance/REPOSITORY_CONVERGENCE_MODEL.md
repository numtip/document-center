# Repository Convergence Model — RAE Document Center

**Version:** 1.0  
**Status:** Approved  
**Authority:** Sonnet-5 Co-Work Command, 2026-07-12  
**Canonical Repository:** https://github.com/numtip/document-center

---

## 1. Model

The RAE Document Center project operates under a **single canonical repository model**:

```
GitHub main
    = canonical integrated version

Feature/work branch
    = isolated active work

HOME workstation
    = Git-backed checkout of canonical repository

WORK workstation
    = Git-backed checkout of canonical repository

G:\ProjectAI\RAE-M365-Platform
    = one-time historical recovery source (retired after import)
```

After historical recovery completes, **no active project development occurs outside Git**.

---

## 2. Repository Hierarchy

| Layer | Role | Authority |
|-------|------|-----------|
| `https://github.com/numtip/document-center` — `main` | Canonical integrated baseline | Single source of truth |
| `https://github.com/numtip/document-center` — feature branches | Isolated development work | Temporary, merged via PR |
| `F:\projectAi\document-center` (HOME) | Git checkout of canonical repository | Pulls from GitHub |
| `G:\ProjectAI\document-center` (WORK, after recovery) | Git checkout of canonical repository | Pulls from GitHub |
| `G:\ProjectAI\RAE-M365-Platform` (WORK) | One-time recovery source | **Not** a canonical project. Retired after import. |

---

## 3. Divergence Handling

| State | Local | Remote | Action |
|-------|-------|--------|--------|
| **LOCAL CLEAN + REMOTE NEWER** | clean | ahead | `rtk git pull origin main` — update from canonical remote |
| **LOCAL COMMITTED + REMOTE NEWER** | has commits | ahead | Create feature branch from local, push feature branch, reconcile through Git PR |
| **LOCAL UNCOMMITTED** | dirty | any | **STOP.** Inspect changes. Do not pull or push. |
| **DIVERGED HISTORY** | diverged | diverged | Create recovery branch. No force push. Review and reconcile via PR. |
| **UNKNOWN FILE SOURCE** | untracked | — | Quarantine files. Inventory before import. Apply secret scan. |

### Commands

```bash
# Behind: clean update
rtk git pull origin main

# Ahead: preserve local work
rtk git checkout -b feature/my-work
rtk git push -u origin feature/my-work
# Then create PR targeting main

# Diverged: preserve both histories
rtk git branch recovery/diverged-$(date +%Y%m%d)
rtk git reset --hard origin/main
# Review recovery/diverged branch, reconcile via PR
```

---

## 4. Frozen Rules

From [GIT_CANONICAL_VERSION_POLICY.md](./GIT_CANONICAL_VERSION_POLICY.md):

| # | Rule |
|---|------|
| 1 | GitHub is canonical |
| 2 | main must not be force-pushed |
| 3 | Architecture changes require ADR |
| 4 | Architecture artifacts belong in Git |
| 5 | IaC belongs in Git |
| 6 | Schemas belong in Git |
| 7 | Memory OS belongs in Git |
| 8 | Validated exports belong in Git |
| 9 | Secrets never belong in Git |
| 10 | M365 authentication artifacts never belong in Git |
| 11 | Real master documents never belong in Git |
| 12 | GitHub Pages remains preview/demo only |

---

## 5. Workstation Commitment

Every workstation used for RAE Document Center development MUST:

1. Be a Git checkout of `https://github.com/numtip/document-center`
2. Run `rtk git fetch origin` as the first step of every session
3. Validate before commit: `rtk npm run validate:all`
4. Secret-scan before commit
5. Never force-push to `main`
6. Never commit secrets, M365 credentials, or master documents

---

## 6. Recovery Source Status

`G:\ProjectAI\RAE-M365-Platform` is a **one-time historical recovery source**.

After its contents have been inspected, classified, and selectively imported into the canonical repository via the `recovery/ea-m365-baseline` branch process, it must be **retired**:

```bash
rtk mv G:\ProjectAI\RAE-M365-Platform G:\ProjectAI\RAE-M365-Platform.RECOVERED.<YYYY-MM-DD>
```

After retirement, all development resumes through the canonical GitHub repository only.

---

## 7. All Commands Use `rtk` Prefix

Every Git, npm, and shell operation in all runbooks, policies, and workflows uses the `rtk` command prefix. Examples:

```bash
rtk git status
rtk git fetch origin
rtk git pull origin main
rtk git push origin <branch>
rtk npm run validate:all
rtk rg -i "secret|password|token" . --glob '!.git'
```

No naked git, npm, gh, or shell commands are used in documented procedures.
