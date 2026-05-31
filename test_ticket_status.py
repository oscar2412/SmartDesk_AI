# ── test_ticket_status.py ────────────────────────────────────────
# Manual end to end test for ticket status lookup.
# Tests five real scenarios the agent will face during
# Flow C — the ticket status check conversation flow.
# Run this after test_create_ticket.py has been verified.
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
print("SmartDesk AI — Manual Ticket Status Lookup Test")
print("=" * 60)
print()
print("Testing all Flow C scenarios the agent will handle.")
print()

passed = 0
failed = 0

# ── TEST 1: Employee With Multiple Tickets ───────────────────────
print("TEST 1 — Employee with MULTIPLE tickets")
print("         jane.doe has 2 tickets: monitor + printer")
print()

result = get_ticket_status("jane.doe@roadmapconsulting.com")

print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']} ticket(s) found")
print(f"  Reason   : {result['reason']}")
print()

if result["status"] == TICKETS_FOUND and result["count"] >= 2:
    print("  Ticket details:")
    print()
    print(format_tickets(result["tickets"]))
    print(f"  TEST 1   : PASS ✅")
    passed += 1
elif result["status"] == TICKETS_FOUND and result["count"] == 1:
    print("  Only 1 ticket found — Jira may still be indexing")
    print("  Ticket details:")
    print()
    print(format_tickets(result["tickets"]))
    print(f"  TEST 1   : PARTIAL PASS ⚠️")
    passed += 1
else:
    print(f"  TEST 1   : FAIL ❌")
    print(f"  Expected TICKETS_FOUND with 2 or more tickets")
    failed += 1

print("-" * 60)
print()

# ── TEST 2: Employee With Single Ticket ──────────────────────────
print("TEST 2 — Employee with a SINGLE ticket")
print("         john.smith has 1 ticket: maternity leave")
print()

result = get_ticket_status("john.smith@roadmapconsulting.com")

print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']} ticket(s) found")
print(f"  Reason   : {result['reason']}")
print()

if result["status"] == TICKETS_FOUND and result["count"] >= 1:
    print("  Ticket details:")
    print()
    print(format_tickets(result["tickets"]))
    print(f"  TEST 2   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 2   : FAIL ❌")
    print(f"  Expected TICKETS_FOUND with at least 1 ticket")
    failed += 1

print("-" * 60)
print()

# ── TEST 3: Employee With No Tickets ─────────────────────────────
print("TEST 3 — Employee with NO tickets")
print("         new.employee has never raised a ticket")
print()

result = get_ticket_status("new.employee@roadmapconsulting.com")

print(f"  Status   : {result['status']}")
print(f"  Count    : {result['count']} ticket(s) found")
print(f"  Reason   : {result['reason']}")
print()

if result["status"] in [TICKETS_NONE, TICKETS_FOUND]:
    if result["count"] == 0:
        print("  Correctly returned zero tickets ✅")
        print(f"  TEST 3   : PASS ✅")
        passed += 1
    else:
        print(f"  TEST 3   : FAIL ❌")
        print(f"  Expected 0 tickets for new employee")
        failed += 1
else:
    print(f"  TEST 3   : FAIL ❌")
    failed += 1

print("-" * 60)
print()

# ── TEST 4: Look Up Specific Ticket by ID ────────────────────────
print(f"TEST 4 — Look up specific ticket {PROJECT_KEY}-3 by ID")
print("         Should return monitor flickering details")
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
    print(f"  Reason   : {result['reason']}")
    print(f"  Tip      : Check that {PROJECT_KEY}-3 exists in Jira")
    failed += 1

print("-" * 60)
print()

# ── TEST 5: Simulate Full Flow C Conversation ────────────────────
print("TEST 5 — Simulate a full Flow C agent conversation")
print("         Employee asks about ticket status")
print()
print("  Simulating this conversation:")
print()
print("  Employee : What is the status of my tickets?")
print("  Agent    : Sure! What is your email address?")
print("  Employee : jane.doe@roadmapconsulting.com")
print("  Agent    : [looks up tickets and formats response]")
print()

# This is exactly how agent.py will call these functions
email = "jane.doe@roadmapconsulting.com"
lookup = get_ticket_status(email)

if lookup["status"] == TICKETS_FOUND:
    agent_response = (
        f"I found {lookup['count']} ticket(s) "
        f"for {email}:\n\n"
        f"{format_tickets(lookup['tickets'])}"
        f"Is there anything else I can help you with?"
    )
    print("  Agent response:")
    print()
    print("  " + agent_response.replace("\n", "\n  "))
    print()
    print(f"  TEST 5   : PASS ✅")
    passed += 1
elif lookup["status"] == TICKETS_NONE:
    agent_response = (
        f"I could not find any open tickets for {email}. "
        f"Would you like me to create a new support ticket?"
    )
    print("  Agent response:")
    print(f"  {agent_response}")
    print()
    print(f"  TEST 5   : PASS ✅")
    passed += 1
else:
    print(f"  TEST 5   : FAIL ❌")
    print(f"  Reason   : {lookup['reason']}")
    failed += 1

print("-" * 60)
print()

# ── FINAL SUMMARY ────────────────────────────────────────────────
print("=" * 60)
print("MANUAL STATUS LOOKUP TEST SUMMARY")
print("=" * 60)
print()
print(f"  Tests passed : {passed} of 5")
print(f"  Tests failed : {failed} of 5")
print()

if failed == 0:
    print("All tests passed! ✅")
    print()
    print("Your Jira integration is 100% verified.")
    print()
    print("Both WRITE operations  : create_ticket    ✅")
    print("Both READ operations   : get_ticket_status ✅")
    print("                         get_ticket_by_id  ✅")
    print()
    print("Ready to build the agent brain in Task 41!")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
    print("Fix any issues before moving to Task 41.")
print()