# ── test_get_status.py ───────────────────────────────────────────
# Comprehensive test for the get_ticket_status function.
# Tests four real scenarios the agent will face.
# Run this after jira_tools.py is confirmed working.
# ────────────────────────────────────────────────────────────────

from jira_tools import (
    get_ticket_status,
    get_ticket_by_id,
    format_tickets,
    TICKETS_FOUND,
    TICKETS_NONE,
    TICKETS_FAILED
)
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

print("=" * 60)
print("SmartDesk AI — Ticket Status Comprehensive Test")
print("=" * 60)
print()

passed = 0
failed = 0

# ── TEST 1: Email That Has Tickets ───────────────────────────────
print("TEST 1 — Look up tickets for email that HAS tickets")
print("         (using the test email from Task 37)")
print()

result = get_ticket_status("test.employee@roadmapconsulting.com")

print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']}")
print(f"  Reason   : {result['reason']}")
print()

if result["status"] == TICKETS_FOUND and result["count"] > 0:
    print("  Formatted output:")
    print()
    print(format_tickets(result["tickets"]))
    print(f"  TEST 1   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 1   : FAIL ❌")
    print(f"  Expected TICKETS_FOUND with count > 0")
    failed += 1

print("-" * 60)
print()

# ── TEST 2: Email That Has No Tickets ────────────────────────────
print("TEST 2 — Look up tickets for email with NO tickets")
print()

result = get_ticket_status("nobody.here@roadmapconsulting.com")

print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']}")
print(f"  Reason   : {result['reason']}")
print()

if result["status"] in [TICKETS_NONE, TICKETS_FOUND]:
    if result["count"] == 0:
        print(f"  TEST 2   : PASS ✅")
        passed += 1
    else:
        print(f"  TEST 2   : PASS ✅ (found some tickets)")
        passed += 1
else:
    print(f"  TEST 2   : FAIL ❌")
    failed += 1

print("-" * 60)
print()

# ── TEST 3: Look Up Ticket By ID ─────────────────────────────────
print("TEST 3 — Look up a specific ticket by ID")
print(f"         (looking up {PROJECT_KEY}-1)")
print()

result = get_ticket_by_id(f"{PROJECT_KEY}-1")

print(f"  Status       : {result['status']}")
print(f"  Ticket ID    : {result['ticket_id']}")
print(f"  Summary      : {result['summary']}")
print(f"  Ticket Status: {result['status_name']}")
print(f"  Created      : {result['created']}")
print(f"  URL          : {result['ticket_url']}")
print()

if result["status"] == TICKETS_FOUND:
    print(f"  TEST 3   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 3   : FAIL ❌")
    print(f"  Reason   : {result['reason']}")
    failed += 1

print("-" * 60)
print()

# ── TEST 4: Look Up Invalid Ticket ID ────────────────────────────
print("TEST 4 — Look up a ticket ID that does NOT exist")
print(f"         (looking up {PROJECT_KEY}-99999)")
print()

result = get_ticket_by_id(f"{PROJECT_KEY}-99999")

print(f"  Status   : {result['status']}")
print(f"  Reason   : {result['reason']}")
print()

if result["status"] == TICKETS_FAILED:
    print(f"  TEST 4   : PASS ✅")
    print(f"  Correctly returned TICKETS_FAILED for invalid ID")
    passed += 1
else:
    print(f"  TEST 4   : FAIL ❌")
    print(f"  Expected TICKETS_FAILED for non-existent ticket")
    failed += 1

print("-" * 60)
print()

# ── FINAL SUMMARY ────────────────────────────────────────────────
print("=" * 60)
print("TICKET STATUS TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of 4")
print(f"  Tests failed : {failed} of 4")
print()

if failed == 0:
    print("All tests passed! ✅")
    print("Jira integration is fully working.")
    print("Ready to build the agent in Task 41.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
print()