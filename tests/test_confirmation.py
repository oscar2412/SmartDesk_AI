import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.agents.agent import process_message, create_session, INTENT_KB_QUERY

print("=" * 60)
print("SmartDesk AI — Human-in-the-Loop Confirmation Test")
print("=" * 60)
print()

passed = 0
failed = 0


def setup_confirmation_state(query: str, email: str) -> dict:
    session = create_session()
    session["employee_email"]       = email
    session["original_query"]       = query
    session["last_intent"]          = INTENT_KB_QUERY
    session["awaiting_confirmation"] = True
    session["pending_ticket"] = {
        "summary"    : query[:80],
        "description": f"Employee request: {query}",
        "category"   : "IT Support",
        "email"      : email
    }
    return session


print("TEST 1 — Employee confirms with YES")
print()
session  = setup_confirmation_state("My monitor keeps flickering", "jane.doe@roadmapconsulting.com")
response = process_message("yes", session)
print(f"  Response preview : {response[:100]}...")
print()
if "created" in response.lower() or "ticket" in response.lower():
    print("  TEST 1   : PASS ✅")
    passed += 1
else:
    print("  TEST 1   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("TEST 2 — Employee cancels with NO")
print()
session  = setup_confirmation_state("The printer on floor 3 is jammed", "john.smith@roadmapconsulting.com")
response = process_message("no", session)
print(f"  Response preview : {response[:100]}...")
print()
if "not been created" in response.lower() or "no problem" in response.lower():
    print("  TEST 2   : PASS ✅")
    passed += 1
else:
    print("  TEST 2   : FAIL ❌")
    failed += 1
if session["pending_ticket"] is None and not session["awaiting_confirmation"]:
    print("  Session cleared  : PASS ✅")
    passed += 1
else:
    print("  Session cleared  : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("TEST 3 — Employee confirms with informal phrase")
print()
session  = setup_confirmation_state("My keyboard is not working", "jane.doe@roadmapconsulting.com")
response = process_message("sure go ahead please", session)
print(f"  Response preview : {response[:100]}...")
print()
if "created" in response.lower() or "ticket" in response.lower():
    print("  TEST 3   : PASS ✅")
    passed += 1
else:
    print("  TEST 3   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("TEST 4 — Employee cancels with informal phrase")
print()
session  = setup_confirmation_state("My mouse is broken", "john.smith@roadmapconsulting.com")
response = process_message("never mind forget it", session)
print(f"  Response preview : {response[:100]}...")
print()
if "not been created" in response.lower() or "no problem" in response.lower():
    print("  TEST 4   : PASS ✅")
    passed += 1
else:
    print("  TEST 4   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("TEST 5 — Employee types something unclear")
print()
session  = setup_confirmation_state("My headphones are not working", "jane.doe@roadmapconsulting.com")
response = process_message("what do you mean?", session)
print(f"  Response preview : {response[:100]}...")
print()
if "yes" in response.lower() and "no" in response.lower():
    print("  TEST 5   : PASS ✅")
    passed += 1
else:
    print("  TEST 5   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("TEST 6 — Employee changes ticket title")
print()
session  = setup_confirmation_state("problem with computer", "jane.doe@roadmapconsulting.com")
response = process_message("change title My laptop screen is cracked", session)
print(f"  Response preview : {response[:150]}...")
print()
if "cracked" in response.lower() or "updated" in response.lower():
    print("  TEST 6   : PASS ✅")
    passed += 1
else:
    print("  TEST 6   : FAIL ❌")
    failed += 1
print("-" * 60)
print()

print("=" * 60)
print("HUMAN-IN-THE-LOOP CONFIRMATION TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of 6")
print(f"  Tests failed : {failed} of 6")
print()
if failed == 0:
    print("All tests passed! ✅")
    print("Human-in-the-loop confirmation is working correctly.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
print()
