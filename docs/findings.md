# Dashboard Finding and Recommendation

**Data:** 35 incidents linked to Whitetop Hall CIs: 30 generated through the REST API, plus 5 created by hand while testing. All ticket data is generated for demonstration.

## Finding
**Wi-Fi is the biggest problem.**
- WH Network handled **18 of 35 incidents (51%)**.
- One access point, **WH-AP-2F**, generated **9 incidents (26%)**, more than any other CI.
- Together, the floor 2 and floor 3 access points account for **16 of 35 (46%)**.

**Account lockouts come second:** 7 incidents (20%), all on WH-SRV-AUTH01.

## Recommendation
1. **Hardware:** Run a Wi-Fi site survey on floors 2–3, and replace or reposition WH-AP-2F.
   - **Measure:** Wi-Fi incidents per week for that AP before and after the change.
2. **Self-service:** Link the knowledge articles from the portal home page, specifically KB0010006 (password reset) and KB0010003 (gaming console Wi-Fi), so residents can fix common issues without a ticket.
   - **Measure:** fewer "Locked out" tickets, and more views on those articles.

## Dashboard
`Whitetop Hall Service Desk`, with 4 reports filtered to `Configuration item starts with WH-`:
- Incidents by Category (bar)
- Incidents by Priority (donut)
- Incidents by CI (horizontal bar)
- Incidents by Assignment Group (bar)
