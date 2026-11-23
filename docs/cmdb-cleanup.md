# CMDB Data-Quality Check: Missing CI Owners

**Date:** 2026-11-23
**Scope:** The 10 Whitetop Hall configuration items in the `cmdb_ci` table

## What I checked
Every CI should have an **Owned by** value, so someone is accountable for keeping it accurate and approving changes to it.

- **Query:** `cmdb_ci` where Name starts with `WH-` AND Owned by is empty

## What I found
**3 of 10 CIs (30%) had no owner:**

| CI | Class | Support group |
| --- | --- | --- |
| WH-AP-2F | Network Gear | WH Network |
| WH-PC-DESK01 | Computer | WH Hardware |
| WH-PRN-LAB01 | Printer | WH Hardware |

These gaps were seeded on purpose when I loaded the CIs, to test that the check catches them.

## What I fixed
- Set **Owned by** to System Administrator on all 3 CIs, using inline list editing.
- Re-ran the query: **0 results**. Ownership coverage went from 70% to 100%.

## Lesson learned
My first filter used `starts with WH`. ServiceNow filters are case-insensitive, so it also matched two unrelated demo CIs, "What's This? Help Composer" and "WhatsUp Gold".

- I tightened the filter to `starts with WH-` so it matches only Whitetop Hall CIs.
- **In a real CMDB, use a consistent naming convention and precise filters.** A loose filter could lead to bulk-editing the wrong records.

## Evidence
- `screenshots/cmdb-dq-before.png`: the 3 CIs with no owner
- `screenshots/cmdb-dq-after.png`: the same query returning 0 results
