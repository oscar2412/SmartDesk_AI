import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.core.jira_tools import (
    create_ticket,
    get_ticket_status,
    format_tickets,
    TICKET_CREATED,
    TICKET_FAILED,
    TICKETS_FOUND,
)

print("=" * 60)
print("SmartDesk AI — Manual Ticket Creation Test")
print("=" * 60)
print()
print("This test creates 3 real tickets in your Jira project.")
print("After running check your Jira board to verify them.")
print()

created_tickets = []
passed = 0
failed = 0

print("Creating Ticket 1 — IT Support category...")
print()
result1 = create_ticket(
    employee_email = "jane.doe@roadmapconsulting.com",
    summary        = "Monitor flickering on laptop screen",
    description    = (
        "Employee reports that their laptop monitor has been "
        "flickering intermittently for the past two days. "
        "The issue occurs both on battery and when plugged in. "
        "Restarting the laptop did not resolve the issue."
    ),
    category       = "IT Support"
)
print(f"  Status     : {result1['status']}")
print(f"  Ticket ID  : {result1['ticket_id']}")
print(f"  Ticket URL : {result1['ticket_url']}")
print(f"  Reason     : {result1['reason']}")
print()
if result1["status"] == TICKET_CREATED:
    print("  Ticket 1   : PASS ✅")
    created_tickets.append(result1["ticket_id"])
    passed += 1
else:
    print("  Ticket 1   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("Creating Ticket 2 — HR Support category...")
print()
result2 = create_ticket(
    employee_email = "john.smith@roadmapconsulting.com",
    summary        = "Question about maternity leave entitlement",
    description    = (
        "Employee is requesting clarification on the maternity "
        "leave policy — duration, paid/unpaid, and application process."
    ),
    category       = "HR Support"
)
print(f"  Status     : {result2['status']}")
print(f"  Ticket ID  : {result2['ticket_id']}")
print(f"  Ticket URL : {result2['ticket_url']}")
print(f"  Reason     : {result2['reason']}")
print()
if result2["status"] == TICKET_CREATED:
    print("  Ticket 2   : PASS ✅")
    created_tickets.append(result2["ticket_id"])
    passed += 1
else:
    print("  Ticket 2   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("Creating Ticket 3 — General Support category...")
print()
result3 = create_ticket(
    employee_email = "jane.doe@roadmapconsulting.com",
    summary        = "Office printer on floor 3 is jammed",
    description    = (
        "The shared office printer on the 3rd floor has a "
        "persistent paper jam. Error code E-05 on display. "
        "Approximately 12 employees are affected."
    ),
    category       = "General Support"
)
print(f"  Status     : {result3['status']}")
print(f"  Ticket ID  : {result3['ticket_id']}")
print(f"  Ticket URL : {result3['ticket_url']}")
print(f"  Reason     : {result3['reason']}")
print()
if result3["status"] == TICKET_CREATED:
    print("  Ticket 3   : PASS ✅")
    created_tickets.append(result3["ticket_id"])
    passed += 1
else:
    print("  Ticket 3   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("Verifying tickets via email lookup...")
print()

jane_result = get_ticket_status("jane.doe@roadmapconsulting.com")
print(f"  jane.doe — Status: {jane_result['status']} | Count: {jane_result['count']}")
if jane_result["status"] == TICKETS_FOUND:
    print(format_tickets(jane_result["tickets"]))

john_result = get_ticket_status("john.smith@roadmapconsulting.com")
print(f"  john.smith — Status: {john_result['status']} | Count: {john_result['count']}")
if john_result["status"] == TICKETS_FOUND:
    print(format_tickets(john_result["tickets"]))

print("-" * 60)
print()

print("=" * 60)
print("MANUAL TICKET CREATION TEST SUMMARY")
print("=" * 60)
print()
print(f"  Tickets created  : {passed} of 3")
print(f"  Tickets failed   : {failed} of 3")
print()
if created_tickets:
    print("  Created ticket IDs:")
    for tid in created_tickets:
        print(f"    {tid}")
    print()
if failed == 0:
    print("All tickets created successfully! ✅")
else:
    print("Some tickets failed to create.")
    print("Check your Jira credentials and project settings.")
print()
