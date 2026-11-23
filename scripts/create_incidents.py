"""Create sample Whitetop Hall incidents in ServiceNow through the REST Table API.

Usage:
    python create_incidents.py          # creates 30 incidents
    python create_incidents.py 50       # creates 50 incidents

Needs environment variables SN_INSTANCE (e.g. dev123456), SN_USER and SN_PASS.
"""
import os
import random
import sys

import requests

INSTANCE = os.environ["SN_INSTANCE"]
USER = os.environ.get("SN_USER", "admin")
PASSWORD = os.environ["SN_PASS"]

BASE = f"https://{INSTANCE}.service-now.com/api/now/table"
AUTH = (USER, PASSWORD)
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

# (short description, category, CI name, impact, urgency, how often it happens)
SCENARIOS = [
    ("Wi-Fi drops every few minutes on floor 2", "network", "WH-AP-2F", 2, 2, 6),
    ("No Wi-Fi signal in room 3014", "network", "WH-AP-3F", 2, 1, 4),
    ("Entire building lost internet", "network", "WH-CORE-SW01", 1, 1, 1),
    ("Lab printer shows offline", "hardware", "WH-PRN-LAB01", 3, 2, 5),
    ("Front desk printer jammed", "hardware", "WH-PRN-DESK01", 3, 3, 3),
    ("Front desk PC will not boot", "hardware", "WH-PC-DESK01", 2, 2, 2),
    ("Locked out of university account", "inquiry", "WH-SRV-AUTH01", 3, 2, 6),
    ("Password reset link not arriving", "inquiry", "WH-SRV-AUTH01", 3, 2, 3),
]


def get_sys_id(table, name):
    """Look up a record's sys_id by its name."""
    response = requests.get(
        f"{BASE}/{table}",
        auth=AUTH,
        headers=HEADERS,
        params={"sysparm_query": f"name={name}", "sysparm_fields": "sys_id", "sysparm_limit": 1},
        timeout=30,
    )
    response.raise_for_status()
    results = response.json()["result"]
    if not results:
        sys.exit(f"Could not find '{name}' in {table}. Check the name matches your CMDB.")
    return results[0]["sys_id"]


def main(count):
    ci_ids = {name: get_sys_id("cmdb_ci", name) for name in {s[2] for s in SCENARIOS}}
    weights = [s[5] for s in SCENARIOS]
    created = 0

    for _ in range(count):
        desc, category, ci, impact, urgency, _ = random.choices(SCENARIOS, weights=weights)[0]
        body = {
            "short_description": desc,
            "description": "Sample ticket generated for the Whitetop Hall service desk project.",
            "category": category,
            "cmdb_ci": ci_ids[ci],
            "impact": str(impact),
            "urgency": str(urgency),
        }
        response = requests.post(f"{BASE}/incident", auth=AUTH, headers=HEADERS, json=body, timeout=30)
        if response.status_code == 201:
            created += 1
            print(f"Created {response.json()['result']['number']}: {desc}")
        else:
            print(f"Failed ({response.status_code}): {response.text[:200]}")

    print(f"\nDone: {created} of {count} incidents created.")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30)
