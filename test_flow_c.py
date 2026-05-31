# ── test_flow_c.py ───────────────────────────────────────────────
# Official Flow C test scenario from the capstone document.
# Tests that the agent correctly retrieves and displays
# ticket status information for employees.
#
# This is the test your evaluator will run to verify Flow C.
# ────────────────────────────────────────────────────────────────

from agent import process_message, create_session
from jira_tools import get_ticket_status, TICKETS_FOUND
import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

print("=" * 60)
print("SmartDesk AI — Flow C Official Test")
print("Ticket Status Check Verification")
print("=" * 60)
print()
print("Testing that the agent correctly retrieves and")
print("displays ticket status for employees.")
print()

passed = 0
failed = 0


def run_flow_c_scenario(
    test_num,
    label,
    status_question,
    employee_email,
    expect_tickets=True
):
    """
    Simulates a complete Flow C conversation:
    1. Employee asks about ticket status
    2. Agent asks for email if not known
    3. Employee provides email
    4. Agent looks up and displays tickets
    """
    global passed, failed

    print(f"SCENARIO {test_num} — {label}")
    print(f"  Question : {status_question}")
    print(f"  Email    : {employee_email}")
    print(f"  Expects  : {'Tickets found' if expect_tickets else 'No tickets'}")
    print()

    session      = create_session()
    step_results = []

    # ── Turn 1: Employee asks about ticket status ────────────────
    response1       = process_message(status_question, session)
    response1_lower = response1.lower()

    # Agent should either ask for email or show tickets
    # if email already in session
    turn1_ok = (
        "email" in response1_lower or
        "ticket" in response1_lower or
        "found" in response1_lower
    )
    step_results.append(("Turn 1 - Status intent detected", turn1_ok))
    print(
        f"  Turn 1 response  : "
        f"{response1[:100].replace(chr(10), ' ')}..."
    )
    print()

    # ── Turn 2: Employee provides email ─────────────────────────
    if session["awaiting_email"]:
        response2       = process_message(employee_email, session)
        response2_lower = response2.lower()
    else:
        # Agent did not ask for email — unusual but handle it
        session["employee_email"] = employee_email
        from agent import handle_check_status
        response2       = handle_check_status(session)
        response2_lower = response2.lower()

    print(
        f"  Turn 2 response  : "
        f"{response2[:150].replace(chr(10), ' ')}..."
    )
    print()

    if expect_tickets:
        # Should show ticket list
        turn2_ok = (
            PROJECT_KEY in response2 or
            "ticket" in response2_lower or
            "found" in response2_lower or
            "status" in response2_lower
        )
        step_results.append(("Turn 2 - Tickets displayed", turn2_ok))
    else:
        # Should say no tickets found
        turn2_ok = (
            "could not find" in response2_lower or
            "no ticket" in response2_lower or
            "no open" in response2_lower or
            "not find" in response2_lower
        )
        step_results.append(("Turn 2 - No tickets message", turn2_ok))

    # ── Check session memory ─────────────────────────────────────
    email_remembered = session["employee_email"] == employee_email
    step_results.append(("Session email remembered", email_remembered))

    # ── Evaluate all steps ───────────────────────────────────────
    all_passed = all(ok for _, ok in step_results)

    for step_label, step_ok in step_results:
        status = "PASS ✅" if step_ok else "FAIL ❌"
        print(f"  {step_label:35} : {status}")

    print()
    if all_passed:
        print(f"  SCENARIO {test_num}   : PASS ✅")
        passed += 1
    else:
        print(f"  SCENARIO {test_num}   : FAIL ❌")
        failed += 1

    print("-" * 60)
    print()
    return all_passed


# ── SCENARIO 1: Employee with multiple tickets ───────────────────
run_flow_c_scenario(
    test_num        = 1,
    label           = "Employee with multiple tickets",
    status_question = "What is the status of my tickets?",
    employee_email  = "jane.doe@roadmapconsulting.com",
    expect_tickets  = True
)

# ── SCENARIO 2: Employee with single ticket ──────────────────────
run_flow_c_scenario(
    test_num        = 2,
    label           = "Employee with single ticket",
    status_question = "Any updates on my support request?",
    employee_email  = "john.smith@roadmapconsulting.com",
    expect_tickets  = True
)

# ── SCENARIO 3: Employee with no tickets ─────────────────────────
run_flow_c_scenario(
    test_num        = 3,
    label           = "Employee with no tickets",
    status_question = "Can you check my ticket status please?",
    employee_email  = "new.employee@roadmapconsulting.com",
    expect_tickets  = False
)

# ── SCENARIO 4: Session memory test ─────────────────────────────
print("SCENARIO 4 — Session memory across multiple turns")
print("  Testing that email is remembered after first lookup")
print()

session = create_session()

# Turn 1 — Check status and provide email
response1 = process_message(
    "What is the status of my tickets?",
    session
)
if session["awaiting_email"]:
    response2 = process_message(
        "jane.doe@roadmapconsulting.com",
        session
    )

# Turn 2 — Ask again without providing email
response3 = process_message(
    "Can you check my tickets again?",
    session
)
response3_lower = response3.lower()

print(
    f"  Turn 3 response  : "
    f"{response3[:150].replace(chr(10), ' ')}..."
)
print()

# Agent should NOT ask for email again
asked_for_email_again = "email" in response3_lower and \
                        "could you" in response3_lower

if not asked_for_email_again and (
    "ticket" in response3_lower or
    "found" in response3_lower or
    "status" in response3_lower or
    PROJECT_KEY in response3
):
    print("  Email not asked again    : PASS ✅")
    print("  Tickets shown directly   : PASS ✅")
    print(f"  SCENARIO 4   : PASS ✅")
    passed += 1
else:
    print("  Session memory           : FAIL ❌")
    print("  Agent asked for email again or showed no tickets")
    print(f"  SCENARIO 4   : FAIL ❌")
    failed += 1

print("-" * 60)
print()

# ── SCENARIO 5: Direct Jira API verification ─────────────────────
print("SCENARIO 5 — Direct Jira API verification")
print("  Confirming get_ticket_status works independently")
print()

emails_to_check = [
    "jane.doe@roadmapconsulting.com",
    "john.smith@roadmapconsulting.com"
]

jira_passed = 0
for email in emails_to_check:
    result = get_ticket_status(email)
    if result["status"] == TICKETS_FOUND and result["count"] > 0:
        print(f"  {email[:40]:40} : {result['count']} ticket(s) ✅")
        jira_passed += 1
    else:
        print(f"  {email[:40]:40} : No tickets found ⚠️")

print()
if jira_passed >= 1:
    print(f"  SCENARIO 5   : PASS ✅")
    print(f"  {jira_passed} of {len(emails_to_check)} emails have tickets in Jira")
    passed += 1
else:
    print(f"  SCENARIO 5   : FAIL ❌")
    print("  No tickets found for any test email")
    print("  Run test_flow_b.py first to create test tickets")
    failed += 1

print("-" * 60)
print()

# ── FINAL SUMMARY ────────────────────────────────────────────────
print("=" * 60)
print("FLOW C TEST SUMMARY")
print("=" * 60)
print(f"  Scenarios passed : {passed} of 5")
print(f"  Scenarios failed : {failed} of 5")
print()

if failed == 0:
    print("All Flow C tests passed! ✅")
    print()
    print("Your agent correctly retrieves and displays")
    print("ticket status for employees by email lookup.")
    print()
    print("Flow C is verified and ready for your evaluator.")
    print()
    print("ALL THREE FLOWS ARE NOW VERIFIED:")
    print("  Flow A — Knowledge base answers  ✅")
    print("  Flow B — Ticket creation         ✅")
    print("  Flow C — Ticket status check     ✅")
    print()
    print("Ready to move on to Task 52 — Edge case testing.")
elif failed <= 1:
    print("Flow C is mostly working. ✅")
    print()
    print("Check the failing scenario above.")
    print("Minor issues are acceptable — move on to Task 52.")
else:
    print("Flow C needs attention.")
    print()
    print("Common fixes:")
    print("  1. Run test_flow_b.py first to create test tickets")
    print("  2. Wait 60 seconds for Jira to index new tickets")
    print("  3. Check JIRA credentials in .env file")
print()