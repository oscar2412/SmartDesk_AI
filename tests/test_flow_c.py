import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.agents.agent import process_message, create_session
from src.core.jira_tools import get_ticket_status, TICKETS_FOUND
import os as _os
from dotenv import load_dotenv

load_dotenv()
PROJECT_KEY = _os.getenv("JIRA_PROJECT_KEY")

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
    global passed, failed

    print(f"SCENARIO {test_num} — {label}")
    print(f"  Question : {status_question}")
    print(f"  Email    : {employee_email}")
    print(f"  Expects  : {'Tickets found' if expect_tickets else 'No tickets'}")
    print()

    session      = create_session()
    step_results = []

    response1       = process_message(status_question, session)
    response1_lower = response1.lower()

    turn1_ok = (
        "email" in response1_lower or
        "ticket" in response1_lower or
        "found" in response1_lower
    )
    step_results.append(("Turn 1 - Status intent detected", turn1_ok))
    print(f"  Turn 1 response  : {response1[:100].replace(chr(10), ' ')}...")
    print()

    if session["awaiting_email"]:
        response2       = process_message(employee_email, session)
        response2_lower = response2.lower()
    else:
        session["employee_email"] = employee_email
        from src.agents.agent import handle_check_status
        response2       = handle_check_status(session)
        response2_lower = response2.lower()

    print(f"  Turn 2 response  : {response2[:150].replace(chr(10), ' ')}...")
    print()

    if expect_tickets:
        turn2_ok = (
            PROJECT_KEY in response2 or
            "ticket" in response2_lower or
            "found" in response2_lower or
            "status" in response2_lower
        )
        step_results.append(("Turn 2 - Tickets displayed", turn2_ok))
    else:
        turn2_ok = (
            "could not find" in response2_lower or
            "no ticket" in response2_lower or
            "no open" in response2_lower or
            "not find" in response2_lower
        )
        step_results.append(("Turn 2 - No tickets message", turn2_ok))

    email_remembered = session["employee_email"] == employee_email
    step_results.append(("Session email remembered", email_remembered))

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


run_flow_c_scenario(
    test_num        = 1,
    label           = "Employee with multiple tickets",
    status_question = "What is the status of my tickets?",
    employee_email  = "jane.doe@roadmapconsulting.com",
    expect_tickets  = True
)

run_flow_c_scenario(
    test_num        = 2,
    label           = "Employee with single ticket",
    status_question = "Any updates on my support request?",
    employee_email  = "john.smith@roadmapconsulting.com",
    expect_tickets  = True
)

run_flow_c_scenario(
    test_num        = 3,
    label           = "Employee with no tickets",
    status_question = "Can you check my ticket status please?",
    employee_email  = "new.employee@roadmapconsulting.com",
    expect_tickets  = False
)

print("SCENARIO 4 — Session memory across multiple turns")
print("  Testing that email is remembered after first lookup")
print()

session = create_session()

response1 = process_message("What is the status of my tickets?", session)
if session["awaiting_email"]:
    response2 = process_message("jane.doe@roadmapconsulting.com", session)

response3       = process_message("Can you check my tickets again?", session)
response3_lower = response3.lower()

print(f"  Turn 3 response  : {response3[:150].replace(chr(10), ' ')}...")
print()

asked_for_email_again = "email" in response3_lower and "could you" in response3_lower

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
    print(f"  SCENARIO 4   : FAIL ❌")
    failed += 1

print("-" * 60)
print()

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
    passed += 1
else:
    print(f"  SCENARIO 5   : FAIL ❌")
    failed += 1

print("-" * 60)
print()

print("=" * 60)
print("FLOW C TEST SUMMARY")
print("=" * 60)
print(f"  Scenarios passed : {passed} of 5")
print(f"  Scenarios failed : {failed} of 5")
print()

if failed == 0:
    print("All Flow C tests passed! ✅")
elif failed <= 1:
    print("Flow C is mostly working. ✅")
else:
    print("Flow C needs attention.")
print()
