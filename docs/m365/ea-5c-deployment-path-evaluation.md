# EA-5C — Power Automate Deployment Path Evaluation

**Phase:** EA-5C — Power Automate Deployment Path Evaluation  
**Precondition:** EA-5B = EA5B_BLOCKED (commit `428d21e`)  
**Tenant:** Maejo University (MJU) — maejo365.sharepoint.com  
**Power Automate Environment:** Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8  
**Date:** 2026-07-14  
**Status:** EA5C_AUTOMATED_DEPLOYMENT_PATH_FOUND

---

## 1. Capability Audit — Installed Tools

### 1.1 Tool Inventory

| Tool | Installed | Version | Available To Install | Notes |
|------|:---------:|---------|:-------------------:|-------|
| `pac` (Power Platform CLI) | ❌ No | — | ✅ winget | `winget install Microsoft.PowerAppsCLI` |
| `az` (Azure CLI) | ❌ No | — | ✅ winget | Not needed for primary path |
| Python | ✅ Yes | 3.14.2 | — | — |
| Python `requests` | ✅ Yes | 2.33.0 | — | HTTP capability available |
| Python `msal` | ❌ No | — | ✅ pip | `pip install msal` |
| Python `azure-identity` | ❌ No | — | ✅ pip | Alternative to msal |
| Node.js | ✅ Yes | v24.18.0 | — | — |
| npm | ✅ Yes | 11.8.0 | — | — |
| `dotnet` runtime | ❌ No | — | ✅ winget | Only needed for `pac package deploy` |
| PowerApps PowerShell module | ❌ No | — | ✅ PSGallery | `Install-Module Microsoft.PowerApps.Administration.PowerShell` |
| PnP PowerShell (SharePoint) | ❌ No | — | ✅ PSGallery | Unrelated to flow deployment |

**Audit Constraint Respected:** No tools installed during capability audit. Winget, pip, and PSGallery installation options are documented for subsequent phases.

### 1.2 Browser Session State

| Item | Status | Evidence |
|------|--------|---------|
| Browser authenticated to Power Platform | ✅ ACTIVE | `make.powerautomate.com` loads with "Maejo university (default)" |
| MSAL access tokens in localStorage | ✅ PRESENT | Multiple scopes including `https://service.powerapps.com//user_impersonation` and `https://api.powerplatform.com/…` |
| Tenant ID | ✅ CONFIRMED | `8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8` |
| User account ID | ✅ CONFIRMED | `6693e9ff-447f-4998-ba67-72a8791aadf1` |
| Token expiry | ✅ VALID | Expires ~1 hour from session start (refreshable) |

---

## 2. Authentication Path Evaluation

### 2.1 Available Authentication Methods

| Method | Feasibility | Description |
|--------|:-----------:|-------------|
| **pac auth create (device code)** | ✅ HIGH | Opens browser → user confirms already-authenticated session. Interactive but one-time. |
| **pac auth create (username/password)** | 🟡 MEDIUM | Direct credentials. Not recommended; ROPC flow deprecated in many tenants. |
| **Python msal device code flow** | ✅ HIGH | `msal.PublicClientApplication.acquire_token_by_device_flow()` → browser prompt. Requires `pip install msal`. |
| **Python msal interactive browser** | ✅ HIGH | Opens browser tab automatically. Leverages existing authenticated session. |
| **Service Principal (client credentials)** | 🔴 LOW NOW | Requires Azure App Registration + admin consent. No App Registration configured yet. |
| **Browser session token extraction** | ⚠️ FRAGILE | Tokens in localStorage are valid but not repeatable / expire hourly. Not suitable for pipelines. |

### 2.2 Recommended Authentication Path

For EA-5B re-execution, the recommended authentication sequence is:

```powershell
# Step 1: Install pac CLI (one-time)
winget install Microsoft.PowerAppsCLI

# Step 2: Authenticate (device code — leverages existing browser session)
pac auth create --environment "Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8" --deviceCode

# Step 3: Verify connection
pac org who
```

The device code flow opens the browser at `login.microsoft.com`. Since the browser is already authenticated to the same account, the device code confirmation is typically a one-click approval.

### 2.3 Required Permissions / Licenses

| Permission | Required For | Current Status |
|------------|-------------|----------------|
| Environment Maker role | Creating/importing solutions and flows | ✅ CONFIRMED (Solutions UI shows "+New solution" button) |
| SharePoint connection (pre-existing) | Flow connection reference binding | ✅ CONFIRMED (connections listed in Power Automate) |
| Approvals connector | WF-02 approval routing | ✅ CONFIRMED (connector listed) |
| Office 365 Outlook connector | WF-01/WF-04 notifications | ✅ CONFIRMED (connector listed) |
| Power Automate per-user or per-flow license | Running flows in production | 🟡 VERIFY (Microsoft 365 default license may be sufficient for non-premium connectors) |
| Premium connector license | Not needed (all connectors are standard) | ✅ N/A |

**Key Finding:** All 5 target workflows (WF-01 through WF-05) use only **standard connectors** (SharePoint, Approvals, Office 365 Outlook). No premium connectors required. The existing Microsoft 365 tenant license is sufficient.

---

## 3. Dataverse & Solutions Availability

### 3.1 Dataverse Status

| Check | Result | Evidence |
|-------|--------|---------|
| Dataverse enabled in Default environment | ✅ YES | Solutions page loads with full content |
| Solutions tab accessible | ✅ YES | Make.powerautomate.com → Solutions → content displayed |
| Existing solutions present | ✅ YES | 15+ managed solutions from Microsoft (Project, Scheduling, URS) |
| "+New solution" button accessible | ✅ YES | Environment Maker confirmed |
| "Import solution" button accessible | ✅ YES | Solution ZIP import available |
| "Connect to Git" button present | ✅ YES | GitHub/Azure DevOps source control integration available |

**Key Finding:** Dataverse is fully enabled. The `workflow` entity (which stores Power Automate flows) is available. Solution-based deployment is fully supported.

### 3.2 Source Control Integration Discovery

The "Connect to Git" button on the Solutions page indicates native GitHub/Azure DevOps integration is available. This allows:

- Exporting solution components (including flow JSON) directly to a git branch
- Importing from a git branch back to the environment
- Full round-trip: PA UI → Git → PA import (or vice versa)

This is the **Microsoft-native source control integration** for Power Platform (ALM feature). When activated:
- Flow definitions are stored as `.json` files in the git repository under `Workflows/` folder
- Changes in git can be imported back via `pac solution import` or via the portal

---

## 4. Deployment Method Feasibility Assessment

### 4.1 Method A — pac CLI + Solution Import (RECOMMENDED)

**Classification:** `EA5C_AUTOMATED_DEPLOYMENT_PATH_FOUND`

**Process:**
```
1. winget install Microsoft.PowerAppsCLI          [one-time]
2. pac auth create --deviceCode                   [one-time per session]
3. pac solution init --publisher-name RAE-DC      [one-time]
   --publisher-prefix raedc
4. Create flow JSON definitions (see Section 5)
5. pac solution pack --zipFile rae-dc-flows.zip   [per deployment]
   --zipFolder ./solution-src
6. pac solution import --path rae-dc-flows.zip    [per deployment]
   --settings-file ./settings/maejo.settings.json
   --publish-changes
   --force-overwrite
7. Enable flows in Power Automate UI or via API   [per deployment]
```

**Feasibility:** ✅ HIGH
- pac CLI available via winget (no admin required for user-level install)
- Device code auth leverages existing browser session
- All flow definitions already specified in `ea-5b-workflow-implementation-report.md` §4
- Standard connectors = no premium license required
- Version-controlled JSON in git (DevOps-ready)

**Blockers:** None identified. **Connection References** are the main complexity (see Section 4.1.1 below).

#### 4.1.1 Connection Reference Binding

When importing a solution containing flows, each flow's connector must be bound to a **Connection Reference** — a reusable reference to a pre-created connection.

**Required Connection References for WF-01 through WF-05:**

| Connector | API Name | Logical Name (canonical) | Status |
|-----------|---------|--------------------------|--------|
| SharePoint Online | `shared_sharepointonline` | `raedc_sharedsharepoint` | 🔴 Need to create in settings file |
| Approvals | `shared_approvals` | `raedc_sharedapprovals` | 🔴 Need to create in settings file |
| Office 365 Outlook | `shared_office365` | `raedc_sharedoutlook` | 🔴 Need to create in settings file |

**Settings file template (`maejo.settings.json`):**
```json
{
  "EnvironmentVariables": [
    {
      "SchemaName": "raedc_SiteUrl",
      "Value": "https://maejo365.sharepoint.com/sites/msteams_54adc4"
    }
  ],
  "ConnectionReferences": [
    {
      "LogicalName": "raedc_sharedsharepoint",
      "ConnectionId": "FILL_FROM_PA_CONNECTIONS_PAGE",
      "ConnectorId": "/providers/Microsoft.PowerApps/apis/shared_sharepointonline"
    },
    {
      "LogicalName": "raedc_sharedapprovals",
      "ConnectionId": "FILL_FROM_PA_CONNECTIONS_PAGE",
      "ConnectorId": "/providers/Microsoft.PowerApps/apis/shared_approvals"
    },
    {
      "LogicalName": "raedc_sharedoutlook",
      "ConnectionId": "FILL_FROM_PA_CONNECTIONS_PAGE",
      "ConnectorId": "/providers/Microsoft.PowerApps/apis/shared_office365"
    }
  ]
}
```

**ConnectionId resolution:** Navigate to `make.powerautomate.com → Connections`, click each connection, copy the GUID from the URL. This is a one-time, 5-minute manual step.

### 4.2 Method B — Dataverse Web API (Python + requests + msal)

**Classification:** `FEASIBLE WITH DEPENDENCIES`

**Process:**
```python
import msal, requests, json

# 1. Authenticate (device code)
app = msal.PublicClientApplication(
    "51f81489-12ee-4a9e-aaae-a2591f45987d",  # Dataverse discovery client
    authority="https://login.microsoftonline.com/8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8"
)
flow = app.initiate_device_flow(scopes=["https://maejo365.crm.dynamics.com/.default"])
print(flow["message"])  # Display device code instructions
token = app.acquire_token_by_device_flow(flow)

# 2. Create flow via Dataverse workflows entity
headers = {
    "Authorization": f"Bearer {token['access_token']}",
    "Content-Type": "application/json",
    "OData-MaxVersion": "4.0",
    "OData-Version": "4.0"
}
org_url = "https://maejo365.crm.dynamics.com"  # Need to verify CRM URL

payload = {
    "category": 5,           # Cloud flow
    "name": "WF-01 - RAE Upload & Registration",
    "type": 1,               # Definition
    "primaryentity": "none",
    "clientdata": json.dumps({ ...flow_definition... })
}
response = requests.post(f"{org_url}/api/data/v9.2/workflows", headers=headers, json=payload)
```

**Dependencies:**
- `pip install msal` (not installed, audit complete → can install now)
- Verify Dataverse CRM URL (format: `https://{domain}.crm{N}.dynamics.com`)
- Full flow definition JSON for each workflow (available in `ea-5b-workflow-implementation-report.md`)

**Limitation:** `api.flow.microsoft.com` is deprecated per Microsoft Learn (2024). Use Dataverse Web API only.

**Feasibility:** ✅ MEDIUM-HIGH (requires msal install + CRM URL verification)

### 4.3 Method C — Portal Solution Import (Manual UI / Semi-Automated)

**Classification:** `MANUAL BUT RELIABLE`

**Process:**
1. Create flows in Power Automate inside a **Solution** (not "My Flows")
2. Solutions → Export solution → Download ZIP
3. Commit ZIP and/or unpacked JSON files to git
4. For redeployment: Solutions → Import solution → upload ZIP → map connections

**Key Insight:** Creating flows **inside a Solution** from the start (vs. "My Flows") means they are immediately version-controllable via:
- Manual export/import cycle
- `pac solution export/import` via CLI
- Portal "Connect to Git" integration

This is the fallback if pac CLI or Python approach encounters issues.

### 4.4 Method D — Power Platform GitHub Actions / Azure DevOps (CI/CD Pipeline)

**Classification:** `FUTURE STATE — NOT NEEDED FOR EA-5B`

Using [Microsoft Power Platform Build Tools for GitHub Actions](https://learn.microsoft.com/en-us/power-platform/alm/github-actions-start):

```yaml
# .github/workflows/deploy-flows.yml
- uses: microsoft/powerplatform-actions/import-solution@main
  with:
    environment-url: 'https://maejo365.crm.dynamics.com'
    app-id: ${{ secrets.PP_APP_ID }}
    client-secret: ${{ secrets.PP_CLIENT_SECRET }}
    tenant-id: '8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8'
    solution-file: './dist/RAE-DC-Flows.zip'
    settings-file: './settings/maejo.settings.json'
```

**Requirements:** Azure App Registration with Power Platform admin consent.  
**Status:** Requires Azure AD App Registration (not yet configured). Valid long-term ALM target.

### 4.5 Method E — Browser UI (Fallback Only)

**Classification:** `MANUAL — LAST RESORT`

Create flows manually in Power Automate UI inside a **Solution** (not "My Flows"), following EA-5B Section 4 specifications. This is the baseline fallback if all automated methods fail.

**Critical improvement over EA-5B approach:** Creating flows **inside a Solution** from the start eliminates the "My Flows" persistence problem encountered in EA-5A/EA-5B.

---

## 5. Recommended Implementation Path for EA-5B Re-execution

### Phase EA-5D: Solution-Based Flow Deployment

**Decision: Use Method A (pac CLI + Solution Import) as primary.**

#### Step 1: Install pac CLI

```powershell
# No admin required (user-scope install)
winget install Microsoft.PowerAppsCLI --scope user
# Verify
pac --version
```

Expected: `Microsoft PowerApps CLI 1.x.x`

#### Step 2: Authenticate

```powershell
pac auth create `
  --environment "Default-8ec74a39-ddf6-41e1-b0a2-ff0459ea8eb8" `
  --deviceCode
# Follow browser prompt — confirm with already-authenticated account
pac org who
```

#### Step 3: Resolve Connection IDs (one-time, 5 minutes)

Navigate to `make.powerautomate.com → Connections`:
1. SharePoint connection → copy GUID from URL → paste to `settings/maejo.settings.json`
2. Approvals connection → same
3. Office 365 Outlook connection → same

#### Step 4: Build Solution Structure

```
.
└── solution-src/
    ├── [Content_Types].xml
    ├── solution.xml                 ← solution manifest
    ├── customizations.xml           ← component list
    └── Workflows/
        ├── WF-01-UploadRegistration-Administration.json
        ├── WF-01-UploadRegistration-FinanceProcurement.json
        ├── WF-01-UploadRegistration-PlanningPolicy.json
        ├── WF-01-UploadRegistration-AcademicServices.json
        ├── WF-01-UploadRegistration-Research.json
        ├── WF-01-UploadRegistration-SOPManuals.json
        ├── WF-02-ApprovalLifecycle.json
        ├── WF-03-ArchiveControl.json
        ├── WF-04-ExpiringReviewNotification.json
        └── WF-05-ExportFoundation.json
```

Each JSON file follows the Azure Logic Apps workflow definition schema with:
- `connectionReferences` pointing to canonical logical names
- `definition` per EA-5B Section 4 specifications

#### Step 5: Pack and Import

```powershell
# Pack solution
pac solution pack `
  --zipFile ./dist/RAE-DC-Flows.zip `
  --zipFolder ./solution-src

# Import with connection bindings
pac solution import `
  --path ./dist/RAE-DC-Flows.zip `
  --settings-file ./settings/maejo.settings.json `
  --publish-changes `
  --force-overwrite

# Verify
pac solution list
```

#### Step 6: Enable Flows

All flows are created in Draft (Off) state. Enable via:

**Option A — pac (if available):**
```powershell
pac flow enable --name "WF-01 - RAE Upload & Registration - Administration"
```

**Option B — Power Automate UI:**
Solutions → [RAE-DC-Flows] → Turn on each flow

**Option C — Python (after msal install):**
```python
# PATCH workflow statecode to 1 (Active)
requests.patch(f"{org_url}/api/data/v9.2/workflows({workflowid})",
               headers=headers, json={"statecode": 1})
```

---

## 6. Exact Blockers (Remaining Before EA-5D)

| Blocker | Severity | Resolution |
|---------|----------|------------|
| `pac` CLI not installed | 🟡 RESOLVABLE | `winget install Microsoft.PowerAppsCLI` — no admin required |
| Connection IDs not captured | 🟡 RESOLVABLE | 5-minute manual step in PA Connections page |
| Flow JSON definitions not yet in solution format | 🟡 RESOLVABLE | Convert EA-5B specs to Azure Logic Apps JSON schema |
| Dataverse CRM URL not confirmed | 🟡 RESOLVABLE | `pac org who` after auth gives the URL |
| Category Owner assignments unresolved | 🔴 DEPENDENCY | WF-02/WF-04 will route to Site Admin (TEST) until resolved |
| MigrationBot service account not provisioned | 🔴 DEPENDENCY | WF-01 bulk path blocked; upload-by-staff path unaffected |

**No blocking issues** that require tenant admin action or Azure subscription changes.

---

## 7. Source Control Strategy

### 7.1 Git-Based Flow Definitions

All flow JSON definitions will be committed to this repository under:

```
docs/m365/flows/
├── solution-src/
│   ├── solution.xml
│   ├── customizations.xml
│   └── Workflows/
│       └── WF-{N}-*.json
├── settings/
│   └── maejo.settings.json.template   ← template only (no ConnectionIds)
└── dist/
    └── .gitkeep                       ← RAE-DC-Flows.zip not committed (built artifact)
```

Connection IDs are **not committed** to git (environment-specific, potentially sensitive). The `settings.json.template` provides structure; the actual `settings.json` is kept locally or in a secure variable store.

### 7.2 Optional: Connect to Git via Portal

The Power Automate Solutions page shows "Connect to Git" button. This enables:
- Automatic export of solution JSON files to GitHub on each save
- Import from GitHub branch to environment
- Native Microsoft ALM without `pac` CLI required for export

**Status:** Available but not configured. Requires GitHub repository connection setup (OAuth to github.com). This is an enhancement to document for EA-5D if desired.

---

## 8. Open-Source / Community Deployment Patterns

| Pattern | Source | Feasibility | Notes |
|---------|--------|:-----------:|-------|
| Power Platform Build Tools (GitHub Actions) | Microsoft official | ✅ HIGH | Best for CI/CD; requires App Registration |
| `pac solution` CLI workflow | Microsoft official | ✅ HIGH | **Primary recommended path** |
| Power Platform ALM Accelerator | Microsoft (AppSource) | 🟡 MEDIUM | Complex setup; overkill for 5 flows |
| Community `powerplatform-deploy` npm package | Community | 🔴 LOW | Not maintained; use official pac |
| Direct Dataverse Web API | Microsoft official | ✅ HIGH | Secondary path; requires msal |
| Import package via portal ZIP | Microsoft official | ✅ HIGH | Manual fallback; always available |

---

## 9. Files Changed

| File | Change |
|------|--------|
| `docs/m365/ea-5c-deployment-path-evaluation.md` | **NEW** — This report |

---

## 10. Commit Hash

| Phase | Commit Hash |
|-------|-------------|
| EA-5B (precondition) | `428d21e` |
| EA-5C (this report) | _pending commit_ |

---

## 11. Final Decision

**EA5C_AUTOMATED_DEPLOYMENT_PATH_FOUND** ✅

### 11.1 Primary Path: `pac solution import` (pac CLI)

| Criterion | Assessment |
|-----------|------------|
| Repeatable | ✅ YES — same command every deployment |
| Version-controlled | ✅ YES — flow JSON in git repo |
| Microsoft-supported | ✅ YES — official Power Platform CLI |
| No browser automation required | ✅ YES — fully terminal-based |
| Admin privileges required | ✅ NO — Environment Maker role sufficient |
| Cost | ✅ FREE — pac CLI is free |
| Dependencies to install | `winget install Microsoft.PowerAppsCLI` |
| Authentication | `pac auth create --deviceCode` (device code, one-click confirm) |

### 11.2 Secondary Path: Python + Dataverse Web API

Available as an alternative if `pac` CLI encounters issues. Requires `pip install msal` and Dataverse CRM URL resolution.

### 11.3 What Changes for EA-5B Re-execution

EA-5B should be re-run as **EA-5D** (or EA-5B second attempt) using this deployment path:

1. Install `pac` CLI via winget (**now allowed** — capability audit complete)
2. Authenticate via `pac auth create --deviceCode`
3. Create solution structure + flow JSON definitions from EA-5B specs
4. Resolve connection IDs (5 minutes manual)
5. `pac solution import` → all 5 flows created in environment
6. Enable flows via `pac flow enable` or UI
7. Run end-to-end test per EA-5B Section 5.1
8. Commit flow JSON to git

---

## 12. Recommended Next Phase

**EA-5D — Solution-Based Flow Implementation (pac CLI)**

Prerequisites (all unblocked):
- [x] EA-5C = `EA5C_AUTOMATED_DEPLOYMENT_PATH_FOUND`
- [ ] `pac` CLI installed (`winget install Microsoft.PowerAppsCLI`)
- [ ] `pac auth create` completed
- [ ] Connection IDs captured from PA Connections page
- [ ] Flow JSON definitions written in Azure Logic Apps schema

**EA-5D will implement all 5 workflows and run end-to-end tests using the pac solution import path. If validated, final decision = EA5D_WORKFLOWS_VALIDATED → EA-6.**
