# Workstation Sync Runbook

Canonical source: https://github.com/numtip/document-center

Use this runbook to synchronise a HOME or WORK workstation checkout with the canonical repository.

---

## START Workflow — Pull Latest Canonical State

Run these steps in order every time you begin a session.

```bash
# 1. Navigate to the canonical checkout
cd /mnt/f/projectAi/document-center             # HOME PC
# cd G:/ProjectAI/document-center                # WORK PC (uncomment as needed)

# 2. Check working tree — must be clean
rtk git status

# 3. Confirm you are on main
rtk git branch

# 4. Confirm origin points to the canonical repository
rtk git remote -v
# Expected: origin  https://github.com/numtip/document-center.git (fetch)
# Expected: origin  https://github.com/numtip/document-center.git (push)

# 5. Fetch latest remote refs
rtk git fetch origin

# 6. Print local HEAD
rtk git rev-parse HEAD

# 7. Print remote HEAD
rtk git rev-parse origin/main

# 8. Compare — if BEHIND, pull
# BEHIND: local HEAD is ancestor of origin/main
rtk git pull origin main

# 9. If DIVERGED — STOP. Do not force push.
# Create a recovery branch and investigate the divergence.
rtk git branch recovery/$(date +%Y%m%d-%H%M%S)-diverged
```

### Behind vs Diverged

| State | Meaning | Action |
|-------|---------|--------|
| **BEHIND** | Local HEAD is ancestor of origin/main | `rtk git pull origin main` |
| **AHEAD** | Local HEAD has commits not in origin/main | `rtk git push origin main` (if safe) |
| **DIVERGED** | Local and remote have different histories | Create recovery branch. Do NOT push. Investigate. |

---

## END Workflow — Commit and Push Changes

Run these steps in order to publish work back to the canonical repository.

```bash
# 1. Review all changes
rtk git status

# 2. Review staged diff
rtk git diff --cached

# 3. Run validation (adjust to your project's validation command)
rtk npm run validate:all

# 4. Run secret scan (adjust to your project's scanner)
rtk rg -i "password|secret|token|api_key|PRIVATE_KEY|BEGIN RSA|BEGIN OPENSSH|client_secret|tenant_id" . --glob '!.git'

# 5. Stage files
rtk git add <files>

# 6. Commit with conventional commit message
rtk git commit -m "type: description"

# 7. Push branch to origin
rtk git push origin <branch>

# 8. Verify push
rtk git log --oneline -3
```

---

## Safety Rules

- **Never** use `--force` or `--force-with-lease` on `main`.
- **Never** commit secrets or authentication artifacts.
- **Never** commit real master documents — they belong in SharePoint/OneDrive.
- When in doubt, create a recovery branch instead of overwriting history.
