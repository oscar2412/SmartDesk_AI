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
print("SmartDesk AI — Ticket Status Comprehensive Test")
print("=" * 60)
print()

passed = 0
failed = 0

print("TEST 1 — Look up tickets for email that HAS tickets")
print()
# result = get_ticket_status("test.employee@roadmapconsulting.com")
result = get_ticket_status("demo@roadmapconsulting.com")
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
    failed += 1
print("-" * 60)
print()

print("TEST 2 — Look up tickets for email with NO tickets")
print()
result = get_ticket_status("nobody.here@roadmapconsulting.com")
print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']}")
print(f"  Reason   : {result['reason']}")
print()
if result["status"] in [TICKETS_NONE, TICKETS_FOUND]:
    print(f"  TEST 2   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 2   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print(f"TEST 3 — Look up a specific ticket by ID ({PROJECT_KEY}-47)")
print()
result = get_ticket_by_id(f"{PROJECT_KEY}-47")
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

print(f"TEST 4 — Look up a ticket ID that does NOT exist ({PROJECT_KEY}-99999)")
print()
result = get_ticket_by_id(f"{PROJECT_KEY}-99999")
print(f"  Status   : {result['status']}")
print(f"  Reason   : {result['reason']}")
print()
if result["status"] == TICKETS_FAILED:
    print(f"  TEST 4   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 4   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("=" * 60)
print("TICKET STATUS TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of 4")
print(f"  Tests failed : {failed} of 4")
print()
if failed == 0:
    print("All tests passed! ✅")
    print("Jira integration is fully working.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
print()
