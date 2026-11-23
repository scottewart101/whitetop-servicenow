# Whitetop Hall IT Service Desk: Build Progress

ServiceNow ITSM portfolio project, built in a Personal Developer Instance (Brazil release).
All configuration is captured in the update set **Whitetop Hall Service Desk**.

**Overall: ~95% complete** (Steps 1–6 done; exports done; GitHub + resume left) · Last updated: 2026-11-23

| Step | Status | Est. time left |
| --- | --- | --- |
| 1. Setup | ✅ Done | — |
| 2. Service desk basics | ✅ Done | — |
| 3. CMDB | ✅ Done | — |
| 4. Automation (business rule + flow) | ✅ Done | — |
| 5. Ticket data with Python | ✅ Done | — |
| 6. Dashboard | ✅ Done | — |
| 7. Package + resume | 🟡 Exports done; GitHub + resume left | ~15 min |

---

## What's built

### Step 1: Setup ✅
- Update set `Whitetop Hall Service Desk` created and set as current.
  - So far it has captured 24 changes: SLA, catalog items, variables and question choices.

### Step 2: Service desk basics ✅

**Assignment groups** ✅

| Group | Manager | Covers |
| --- | --- | --- |
| WH Network | System Administrator | Wi-Fi, access points, core switch |
| WH Hardware | System Administrator | Printers, front desk PC, print server |
| WH Accounts | System Administrator | Lockouts, password resets, auth server |

**SLA definition** ✅
- `WH P1 Resolution (4 hours)`: Incident, Resolution target, 4 hours
  - **Start:** Priority = 1 - Critical
  - **Pause:** State = On Hold
  - **Stop:** State = Resolved
  - **Schedule:** none, so the clock runs 24/7. A P1 means the building is down, so the clock shouldn't pause overnight.

**Priority:** uses the platform's built-in impact × urgency lookup matrix.

**Service Catalog items** ✅

| Item | Category | Variables |
| --- | --- | --- |
| Guest Device Wi-Fi Access | Hardware | Device type (Select Box: Gaming console, Smart TV, Streaming stick, Other) · MAC address · Room number |
| Software Install Request | Software | Software name (required) · Reason for request (required, multi-line) · Room or computer |

- Test orders:
  - **REQ0010001 / RITM0010001** (Software Install Request)
  - **REQ0010002 / RITM0010002** (Guest Device Wi-Fi Access)

**Knowledge articles** ✅ (IT knowledge base, published through the review/approval workflow)

| Number | Title |
| --- | --- |
| KB0010003 | Connect a gaming console to residence hall Wi-Fi |
| KB0010006 | Reset your university account password |
| KB0010009 | Fix a printer that shows offline |

### Step 3: CMDB ✅

**Configuration items** ✅ (10 CIs)

| CI | Class | Support group | Owned by |
| --- | --- | --- | --- |
| Whitetop Hall Wi-Fi | Service | WH Network | System Administrator |
| WH-CORE-SW01 | IP Switch | WH Network | System Administrator |
| WH-AP-1F | Network Gear | WH Network | System Administrator |
| WH-AP-2F | Network Gear | WH Network | *(blank, seeded for data-quality check)* |
| WH-AP-3F | Network Gear | WH Network | System Administrator |
| WH-SRV-PRINT01 | Windows Server | WH Hardware | System Administrator |
| WH-PRN-LAB01 | Printer | WH Hardware | *(blank, seeded for data-quality check)* |
| WH-PRN-DESK01 | Printer | WH Hardware | System Administrator |
| WH-PC-DESK01 | Computer | WH Hardware | *(blank, seeded for data-quality check)* |
| WH-SRV-AUTH01 | Windows Server | WH Accounts | System Administrator |

- **Support group** on each CI drives incident auto-assignment (Step 4).
- I set support group and owner in bulk with list editing on `cmdb_ci.list`.

**Relationships** ✅ (7, all `Depends on::Used by`)

| Parent | Depends on |
| --- | --- |
| Whitetop Hall Wi-Fi | WH-AP-1F, WH-AP-2F, WH-AP-3F |
| WH-AP-1F / 2F / 3F | WH-CORE-SW01 |
| WH-PRN-LAB01 | WH-SRV-PRINT01 |

The dependency view shows Wi-Fi service → 3 access points → core switch, so a switch outage maps straight to service impact.

**Data-quality check** ✅
- Found 3 of 10 CIs with no owner. Fixed all 3 and re-ran the query to get 0 results.
- Full write-up in `docs/cmdb-cleanup.md`.

---

### Step 4: Automation ✅

**Business rule** ✅ `WH Auto-assign from CI support group`
- Incident · before · Insert · Order 50 · Advanced (JavaScript)
- When a new incident has a CI and no group, it sets the assignment group from the CI's support group and adds an audit work note.
- Tested:
  - **INC0010004** (CI WH-AP-3F) was assigned to WH Network with the work note *"Auto-assigned to WH Network (support group for WH-AP-3F)."*

**Flow: P1 alert** ✅ `WH P1 Incident Alert` (Flow Designer, no code)
- **Trigger:** Incident created where Priority = 1 - Critical
- **Actions:** Send Email to on-call (admin@example.com), then Update Record to add the work note "P1 alert sent to on-call."
- Tested:
  - **INC0010005** "Entire building lost internet" (CI WH-CORE-SW01, Impact 1 / Urgency 1 = P1)
    - The business rule auto-assigned it to WH Network with a work note.
    - The flow added "P1 alert sent to on-call." and queued the email "P1 incident: INC0010005" in the Outbox (developer instances don't send mail, so the email log is the proof).
  - The P1 SLA attached to the incident.

### Step 5: Ticket data with Python ✅
- `scripts/create_incidents.py` created **30 incidents (INC0010006–INC0010035)** through the REST Table API.
  - It runs as a dedicated integration account, `wh.api.integration` (Identity type: Machine; roles `itil` + `snc_basic_auth_api_access`).
  - Credentials come from environment variables and are never stored in the repo.
- Results, verified in the instance:
  - **30 of 30** auto-assigned by the business rule, each with an audit work note
  - The 1 P1 (INC0010013, "Entire building lost internet") set off the P1 flow: work note plus alert email
  - **By category:** Network 14 · Hardware 9 · Inquiry 7
  - **By group:** WH Network 14 · WH Hardware 9 · WH Accounts 7
  - **By priority:** P1 1 · P2 6 · P3 8 · P4 15
  - **Top CIs:** WH-AP-2F 7 · WH-SRV-AUTH01 7 · WH-AP-3F 6
- Output log: `docs/step5-script-output.txt`

### Step 6: Dashboard ✅
- **4 reports** on Incident, all filtered to `Configuration item starts with WH-`:
  - WH Incidents by Category (bar)
  - WH Incidents by Priority (donut)
  - WH Incidents by CI (horizontal bar)
  - WH Incidents by Assignment Group (bar)
- **Dashboard** `Whitetop Hall Service Desk` (Platform Analytics, in-line editor): 4 data visualizations on Incident in a 2×2 grid, filtered to `Configuration item starts with WH-`. Category (vertical bar), Priority (donut), Configuration item (horizontal bar), Assignment group (vertical bar).
- **Finding:** WH-AP-2F is the top problem CI (9 of 35 incidents, 26%), and Wi-Fi is 51% of all volume. Full write-up in `docs/findings.md`.

### Step 7: Package 🟡
- Update set **Whitetop Hall Service Desk** marked Complete and exported. It holds **46 changes**: 1 business rule, 1 flow, 1 SLA, 2 catalog items, 10 variables, 4 question choices, 4 reports and the dashboard. → `exports/update-set-whitetop-hall-service-desk.xml`
- **Data exports (XML):** these hold the records the update set doesn't capture.
  - `data-groups.xml`: 3 groups
  - `data-cmdb-cis.xml`: 9 hardware CIs
  - `data-cmdb-relationships.xml`: 7 relationships
  - `data-incidents.xml`: 35 incidents plus their work notes
  - `data-knowledge-articles.xml`: 3 articles
  - The *Whitetop Hall Wi-Fi* service CI isn't in the CI export because the filter was `WH-`. The relationships export still references it.
- The empty duplicate update set ("Whitetop Hall Service Desk 2", 0 changes, created by accident) was set to **Ignore**.

---

## Problems hit and how I fixed them
- **API returned 401 even with the correct admin password:** the instance began enforcing basic-auth restrictions (`glide.authenticate.basic_auth.restriction.enforce = true`), which allow API basic auth only for users with `snc_basic_auth_api_access`. Instead of granting admin more access, I created a least-privilege integration user with just `itil` and `snc_basic_auth_api_access`.
- **Business rule didn't fire:** the out-of-box rule "Populate Assignment Group based on CI/SO" (task, before, order 100) set the group first, so my rule skipped. I found it by searching active business rules whose script references `support_group`. Fixed by setting my rule to **order 50** so it runs first.
- **Support group / Owned by missing from CI forms:** the IP Switch form layout doesn't show them. Fixed by creating the CIs with a name only, then bulk-editing both fields inline from the `cmdb_ci` list.
These make good interview stories.

- **"Invalid insert" on a catalog item:** the item had already saved, and a second save tried to insert a duplicate. Fixed by reopening the saved record from the list.
  - **Lesson:** after saving, the button reads **Update**, not **Submit**.
- **Variables vs. choices:** I first created each device type as its own variable. Fixed by deleting them and adding them as **Question Choices** on one Select Box variable.
- **Knowledge article stuck in Review:** the IT knowledge base sends approvals to its knowledge manager, not to admin. Fixed by approving the `sysapproval_approver` records as admin on the manager's behalf.
- **Classic reports couldn't be added to the new dashboard:** the Platform Analytics dashboard builder has no legacy Report element, and "Add to Dashboard" only lists existing classic dashboards. Rebuilt the 4 charts as data visualizations on the same Incident table and filter.
- **Loose CMDB filter:** `starts with WH` also matched demo CIs like "WhatsUp Gold", because filters are case-insensitive. Tightened it to `WH-`.
- **SLA schedule required:** the instance had no "24 x 7" schedule. Fixed by setting **Schedule source = No schedule**, which runs the SLA 24/7.

---

## Screenshot checklist (`/screenshots`)
- [ ] Update set record
- [ ] Groups list filtered to `WH`
- [ ] Priority lookup matrix
- [ ] SLA definition form
- [ ] Guest Device Wi-Fi Access in the portal ("Try It")
- [ ] Software Install Request confirmation (REQ0010001)
- [ ] Guest Device Wi-Fi Access confirmation (REQ0010002)
- [ ] Knowledge articles
- [x] CMDB dependency view (`03-cmdb-dependency-view.png`)
- [x] CMDB data-quality before (`03-cmdb-dq-before.png`)
- [ ] CMDB data-quality after: optional retake with the `WH-` filter (0 results)
- [x] Business rule work note on INC0010004 (`04-business-rule-work-note.png`)
- [x] P1 flow + business rule work notes on INC0010005 (`04-p1-flow-work-notes.png`)
- [x] P1 alert email record in System Logs > Emails (`04-p1-alert-email.png`)
- [ ] Terminal output of the script run (or use `docs/step5-script-output.txt`)
- [x] Dashboard (`06-dashboard.png`)

## Up next
Step 7: back up the update set, export the data, write the README and update the resume.
