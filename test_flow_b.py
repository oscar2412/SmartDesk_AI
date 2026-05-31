# ── test_flow_b.py ───────────────────────────────────────────────
# Official Flow B test scenario from the capstone document.
# Tests that the agent correctly escalates out-of-scope
# questions to Jira ticket creation with human-in-the-loop
# confirmation.
#
# This is the test your evaluator will run to verify Flow B.
# ────────────────────────────────────────────────────────────────

from agent import (
    process_message,
    create_session,
    INTENT_KB_QUERY
)
from jira_tools import get_ticket_status, TICKETS_FOUND
import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

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
    """
    Simulates a complete Flow B conversation:
    1. Employee asks out of scope question
    2. Agent offers to create ticket
    3. Employee provides email
    4. Agent shows summary and asks yes/no
    5. Employee confirms yes or no
    6. Agent creates or cancels ticket
    """
    global passed, failed, created_tickets

    print(f"SCENARIO {test_num} — {label}")
    print(f"  Question : {out_of_scope_question}")
    print(f"  Email    : {employee_email}")
    print(f"  Confirm  : {'YES' if confirm_yes else 'NO'}")
    print()

    session      = create_session()
    step_results = []

    # ── Turn 1: Employee asks out of scope question ──────────────
    response1 = process_message(out_of_scope_question, session)
    response1_lower = response1.lower()

    # Agent should offer to create a ticket or ask for email
    turn1_ok = (
        "ticket" in response1_lower or
        "email" in response1_lower or
        "create" in response1_lower or
        "support" in response1_lower
    )
    step_results.append(("Turn 1 - Escalation offered", turn1_ok))
    print(f"  Turn 1 response  : {response1[:100].replace(chr(10), ' ')}...")
    print()

    # ── Turn 2: Employee provides email ─────────────────────────
    # Check if agent already asked for email
    if session["awaiting_email"]:
        response2 = process_message(employee_email, session)
    else:
        # Agent may have skipped email ask if it had it already
        response2 = response1
        session["employee_email"] = employee_email

    response2_lower = response2.lower()

    # Agent should now show ticket summary
    turn2_ok = (
        "title" in response2_lower or
        "summary" in response2_lower or
        "ticket" in response2_lower or
        "yes" in response2_lower
    )
    step_results.append(("Turn 2 - Ticket summary shown", turn2_ok))
    print(f"  Turn 2 response  : {response2[:100].replace(chr(10), ' ')}...")
    print()

    # ── Turn 3: Employee confirms yes or no ──────────────────────
    if session["awaiting_confirmation"]:
        confirm_word = "yes" if confirm_yes else "no"
        response3    = process_message(confirm_word, session)
        response3_lower = response3.lower()

        if confirm_yes:
            # Should show ticket created confirmation
            turn3_ok = (
                "created" in response3_lower or
                "ticket id" in response3_lower or
                PROJECT_KEY.lower() in response3_lower
            )
            step_results.append(
                ("Turn 3 - Ticket created", turn3_ok)
            )

            # Extract ticket ID from response
            if PROJECT_KEY in response3:
                import re
                ticket_ids = re.findall(
                    PROJECT_KEY + r'-\d+',
                    response3
                )
                if ticket_ids:
                    created_tickets.extend(ticket_ids)
                    print(f"  Ticket created   : {ticket_ids[0]} ✅")
        else:
            # Should show cancellation message
            turn3_ok = (
                "not been created" in response3_lower or
                "no problem" in response3_lower or
                "cancel" in response3_lower
            )
            step_results.append(
                ("Turn 3 - Ticket cancelled", turn3_ok)
            )

        print(
            f"  Turn 3 response  : "
            f"{response3[:100].replace(chr(10), ' ')}..."
        )
        print()
    else:
        step_results.append(
            ("Turn 3 - Confirmation state", False)
        )
        print("  Turn 3           : Agent not in confirmation state")
        print()

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


# ── SCENARIO 1: IT out of scope — monitor flickering ────────────
run_flow_b_scenario(
    test_num             = 1,
    label                = "IT out of scope — monitor flickering",
    out_of_scope_question= "My monitor keeps flickering all day",
    employee_email       = "jane.doe@roadmapconsulting.com",
    confirm_yes          = True
)

# ── SCENARIO 2: Facilities out of scope — parking ───────────────
run_flow_b_scenario(
    test_num             = 2,
    label                = "Facilities out of scope — office parking",
    out_of_scope_question= "How do I get an office parking permit?",
    employee_email       = "john.smith@roadmapconsulting.com",
    confirm_yes          = True
)

# ── SCENARIO 3: Employee cancels ticket creation ─────────────────
run_flow_b_scenario(
    test_num             = 3,
    label                = "Employee cancels ticket creation",
    out_of_scope_question= "The printer on floor 3 is jammed again",
    employee_email       = "jane.doe@roadmapconsulting.com",
    confirm_yes          = False
)

# ── SCENARIO 4: Verify tickets actually exist in Jira ───────────
print("SCENARIO 4 — Verify created tickets exist in Jira")
print()

if created_tickets:
    print(f"  Checking {len(created_tickets)} ticket(s) in Jira...")
    print()

    jira_verified = 0
    for ticket_id in created_tickets:
        from jira_tools import get_ticket_by_id, TICKETS_FOUND
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
        print(f"  All {jira_verified} ticket(s) verified in Jira")
        passed += 1
    else:
        print(f"  SCENARIO 4   : FAIL ❌")
        failed += 1
else:
    print("  No tickets were created in Scenarios 1 and 2.")
    print("  Check the failures above before verifying Jira.")
    print(f"  SCENARIO 4   : SKIP ⚠️")

print("-" * 60)
print()

# ── FINAL SUMMARY ────────────────────────────────────────────────
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
    print()
    print("Your agent correctly escalates out-of-scope")
    print("questions to Jira ticket creation with")
    print("human-in-the-loop confirmation.")
    print()
    print("Flow B is verified and ready for your evaluator.")
    print("Ready to move on to Task 51 — Flow C testing.")
elif failed <= 1:
    print("Flow B is mostly working. ✅")
    print()
    print("Check the failing scenario above.")
    print("Minor wording differences are acceptable.")
    print("As long as tickets are created ready to move on.")
else:
    print("Flow B needs attention.")
    print()
    print("Common fixes:")
    print("  1. Check CONFIDENCE_THRESHOLD in rag_config.py")
    print("  2. Check out_of_scope_topics.txt has these topics")
    print("  3. Run python agent.py and test manually")
print()