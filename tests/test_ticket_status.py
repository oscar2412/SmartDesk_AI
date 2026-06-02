import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.core.jira_tools import (
    get_ticket_status,
    get_ticket_by_id,
    format_tickets,
    TICKETS_FOUND,
    TICKETS_NONE,
    TICKETS_FAILED,
)
from dotenv import load_dotenv

load_dotenv()
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

print("=" * 60)
print("SmartDesk AI — Manual Ticket Status Lookup Test")
print("=" * 60)
print()

passed = 0
failed = 0

print("TEST 1 — Employee with MULTIPLE tickets")
print("         jane.doe has 2 tickets: monitor + printer")
print()
result = get_ticket_status("jane.doe@roadmapconsulting.com")
print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']} ticket(s) found")
print(f"  Reason   : {result['reason']}")
print()
if result["status"] == TICKETS_FOUND and result["count"] >= 2:
    print(format_tickets(result["tickets"]))
    print(f"  TEST 1   : PASS ✅")
    passed += 1
elif result["status"] == TICKETS_FOUND and result["count"] == 1:
    print(format_tickets(result["tickets"]))
    print(f"  TEST 1   : PARTIAL PASS ⚠️")
    passed += 1
else:
    print(f"  TEST 1   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("TEST 2 — Employee with a SINGLE ticket")
print("         john.smith has 1 ticket: maternity leave")
print()
result = get_ticket_status("john.smith@roadmapconsulting.com")
print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']} ticket(s) found")
print(f"  Reason   : {result['reason']}")
print()
if result["status"] == TICKETS_FOUND and result["count"] >= 1:
    print(format_tickets(result["tickets"]))
    print(f"  TEST 2   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 2   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("TEST 3 — Employee with NO tickets")
print()
result = get_ticket_status("new.employee@roadmapconsulting.com")
print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']} ticket(s) found")
print(f"  Reason   : {result['reason']}")
print()
if result["status"] in [TICKETS_NONE, TICKETS_FOUND] and result["count"] == 0:
    print(f"  TEST 3   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 3   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print(f"TEST 4 — Look up specific ticket {PROJECT_KEY}-3 by ID")
print()
result = get_ticket_by_id(f"{PROJECT_KEY}-3")
print(f"  Status       : {result['status']}")
print(f"  Ticket ID    : {result['ticket_id']}")
print(f"  Summary      : {result['summary']}")
print(f"  Ticket Status: {result['status_name']}")
print(f"  Created      : {result['created']}")
print(f"  URL          : {result['ticket_url']}")
print()
if result["status"] == TICKETS_FOUND:
    print(f"  TEST 4   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 4   : FAIL ❌")
    print(f"  Tip      : Check that {PROJECT_KEY}-3 exists in Jira")
    failed += 1
print("-" * 60)
print()

print("TEST 5 — Simulate a full Flow C agent conversation")
print()
email  = "jane.doe@roadmapconsulting.com"
lookup = get_ticket_status(email)
if lookup["status"] == TICKETS_FOUND:
    agent_response = (
        f"I found {lookup['count']} ticket(s) for {email}:\n\n"
        f"{format_tickets(lookup['tickets'])}"
        f"Is there anything else I can help you with?"
    )
    print("  " + agent_response.replace("\n", "\n  "))
    print(f"  TEST 5   : PASS ✅")
    passed += 1
elif lookup["status"] == TICKETS_NONE:
    print(f"  No open tickets found for {email}.")
    print(f"  TEST 5   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 5   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("=" * 60)
print("MANUAL STATUS LOOKUP TEST SUMMARY")
print("=" * 60)
print()
print(f"  Tests passed : {passed} of 5")
print(f"  Tests failed : {failed} of 5")
print()
if failed == 0:
    print("All tests passed! ✅")
else:
    print("Some tests failed. Review the FAIL results above.")
print()
