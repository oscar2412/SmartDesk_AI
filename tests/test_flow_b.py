import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.agents.agent import process_message, create_session, INTENT_KB_QUERY
from src.core.jira_tools import get_ticket_status, TICKETS_FOUND
import os as _os
from dotenv import load_dotenv

load_dotenv()
PROJECT_KEY = _os.getenv("JIRA_PROJECT_KEY")

print("=" * 60)
print("SmartDesk AI — Flow B Official Test")
print("Escalation to Ticket Creation Verification")
print("=" * 60)
print()
print("Testing that the agent correctly escalates")
print("out-of-scope questions to Jira ticket creation.")
print()

passed = 0
failed = 0
created_tickets = []


def run_flow_b_scenario(
    test_num,
    label,
    out_of_scope_question,
    employee_email,
    confirm_yes=True
):
    global passed, failed, created_tickets

    print(f"SCENARIO {test_num} — {label}")
    print(f"  Question : {out_of_scope_question}")
    print(f"  Email    : {employee_email}")
    print(f"  Confirm  : {'YES' if confirm_yes else 'NO'}")
    print()

    session      = create_session()
    step_results = []

    response1       = process_message(out_of_scope_question, session)
    response1_lower = response1.lower()

    turn1_ok = (
        "ticket" in response1_lower or
        "email" in response1_lower or
        "create" in response1_lower or
        "support" in response1_lower
    )
    step_results.append(("Turn 1 - Escalation offered", turn1_ok))
    print(f"  Turn 1 response  : {response1[:100].replace(chr(10), ' ')}...")
    print()

    if session["awaiting_email"]:
        response2 = process_message(employee_email, session)
    else:
        response2 = response1
        session["employee_email"] = employee_email

    response2_lower = response2.lower()

    turn2_ok = (
        "title" in response2_lower or
        "summary" in response2_lower or
        "ticket" in response2_lower or
        "yes" in response2_lower
    )
    step_results.append(("Turn 2 - Ticket summary shown", turn2_ok))
    print(f"  Turn 2 response  : {response2[:100].replace(chr(10), ' ')}...")
    print()

    if session["awaiting_confirmation"]:
        confirm_word    = "yes" if confirm_yes else "no"
        response3       = process_message(confirm_word, session)
        response3_lower = response3.lower()

        if confirm_yes:
            turn3_ok = (
                "created" in response3_lower or
                "ticket id" in response3_lower or
                PROJECT_KEY.lower() in response3_lower
            )
            step_results.append(("Turn 3 - Ticket created", turn3_ok))

            if PROJECT_KEY in response3:
                import re
                ticket_ids = re.findall(PROJECT_KEY + r'-\d+', response3)
                if ticket_ids:
                    created_tickets.extend(ticket_ids)
                    print(f"  Ticket created   : {ticket_ids[0]} ✅")
        else:
            turn3_ok = (
                "not been created" in response3_lower or
                "no problem" in response3_lower or
                "cancel" in response3_lower
            )
            step_results.append(("Turn 3 - Ticket cancelled", turn3_ok))

        print(f"  Turn 3 response  : {response3[:100].replace(chr(10), ' ')}...")
        print()
    else:
        step_results.append(("Turn 3 - Confirmation state", False))
        print("  Turn 3           : Agent not in confirmation state")
        print()

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


run_flow_b_scenario(
    test_num             = 1,
    label                = "IT out of scope — monitor flickering",
    out_of_scope_question= "My monitor keeps flickering all day",
    employee_email       = "jane.doe@roadmapconsulting.com",
    confirm_yes          = True
)

run_flow_b_scenario(
    test_num             = 2,
    label                = "Facilities out of scope — office parking",
    out_of_scope_question= "How do I get an office parking permit?",
    employee_email       = "john.smith@roadmapconsulting.com",
    confirm_yes          = True
)

run_flow_b_scenario(
    test_num             = 3,
    label                = "Employee cancels ticket creation",
    out_of_scope_question= "The printer on floor 3 is jammed again",
    employee_email       = "jane.doe@roadmapconsulting.com",
    confirm_yes          = False
)

print("SCENARIO 4 — Verify created tickets exist in Jira")
print()

if created_tickets:
    print(f"  Checking {len(created_tickets)} ticket(s) in Jira...")
    print()

    jira_verified = 0
    for ticket_id in created_tickets:
        from src.core.jira_tools import get_ticket_by_id, TICKETS_FOUND
        result = get_ticket_by_id(ticket_id)

        if result["status"] == TICKETS_FOUND:
            print(f"  {ticket_id} : FOUND in Jira ✅")
            print(f"    Summary : {result['summary']}")
            print(f"    Status  : {result['status_name']}")
            jira_verified += 1
        else:
            print(f"  {ticket_id} : NOT FOUND in Jira ❌")

    print()
    if jira_verified == len(created_tickets):
        print(f"  SCENARIO 4   : PASS ✅")
        passed += 1
    else:
        print(f"  SCENARIO 4   : FAIL ❌")
        failed += 1
else:
    print("  No tickets were created in Scenarios 1 and 2.")
    print(f"  SCENARIO 4   : SKIP ⚠️")

print("-" * 60)
print()

print("=" * 60)
print("FLOW B TEST SUMMARY")
print("=" * 60)
print(f"  Scenarios passed : {passed} of 4")
print(f"  Scenarios failed : {failed} of 4")
print()

if created_tickets:
    print(f"  Tickets created  : {created_tickets}")
    print()

if failed == 0:
    print("All Flow B tests passed! ✅")
elif failed <= 1:
    print("Flow B is mostly working. ✅")
else:
    print("Flow B needs attention.")
print()
