import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.agents.agent import (
    process_message,
    create_session,
    build_api_error_response,
)
from src.workflow.flow_b import handle_ticket_confirmed
from src.workflow.flow_c import handle_check_status
from unittest.mock import patch

print("=" * 60)
print("SmartDesk AI — Error Handling Test")
print("=" * 60)
print()

passed = 0
failed = 0


print("TEST 1 — API error response builder")
print()
response = build_api_error_response("OpenAI")
print(f"  Response preview : {response[:80]}...")
print()
if "trouble connecting" in response.lower() and "openai" in response.lower():
    print("  TEST 1   : PASS ✅")
    passed += 1
else:
    print("  TEST 1   : FAIL ❌")
    failed += 1
print("-" * 60)
print()


print("TEST 2 — Jira ticket creation API failure")
print()
session = create_session()
session["employee_email"]        = "test@roadmapconsulting.com"
session["awaiting_confirmation"] = True
session["pending_ticket"] = {
    "summary"    : "Test ticket",
    "description": "Test description",
    "category"   : "IT Support",
    "email"      : "test@roadmapconsulting.com"
}

with patch("src.workflow.flow_b.create_ticket") as mock_create:
    mock_create.side_effect = Exception("Simulated Jira connection timeout")
    response = handle_ticket_confirmed(session)

print(f"  Response preview : {response[:80]}...")
print()
if "trouble connecting" in response.lower() or "unable" in response.lower() or "error" in response.lower():
    print("  TEST 2   : PASS ✅")
    passed += 1
else:
    print("  TEST 2   : FAIL ❌")
    failed += 1
print("-" * 60)
print()


print("TEST 3 — Jira ticket status API failure")
print()
session = create_session()
session["employee_email"] = "test@roadmapconsulting.com"

with patch("src.workflow.flow_c.get_ticket_status") as mock_status:
    mock_status.side_effect = Exception("Simulated Jira authentication failure")
    response = handle_check_status(session)

print(f"  Response preview : {response[:80]}...")
print()
if "trouble connecting" in response.lower() or "error" in response.lower():
    print("  TEST 3   : PASS ✅")
    passed += 1
else:
    print("  TEST 3   : FAIL ❌")
    failed += 1
print("-" * 60)
print()


print("TEST 4 — RAG pipeline OpenAI API failure")
print()
session = create_session()

with patch("src.workflow.flow_a.get_rag_answer") as mock_rag:
    mock_rag.side_effect = Exception("Simulated OpenAI rate limit exceeded")
    response = process_message("How do I reset my password?", session)

print(f"  Response preview : {response[:80]}...")
print()
if "trouble connecting" in response.lower() or "error" in response.lower() or "moment" in response.lower():
    print("  TEST 4   : PASS ✅")
    passed += 1
else:
    print("  TEST 4   : FAIL ❌")
    failed += 1
print("-" * 60)
print()


print("TEST 5 — Agent never crashes on unexpected exception")
print()
session = create_session()

try:
    with patch("src.agents.agent.detect_intent") as mock_intent:
        mock_intent.side_effect = Exception("Simulated catastrophic failure")
        response = process_message("What is my ticket status?", session)

    print(f"  Response preview : {response[:80]}...")
    print()
    print("  TEST 5   : PASS ✅")
    passed += 1

except Exception as e:
    print(f"  TEST 5   : FAIL ❌")
    print(f"  Agent crashed with: {str(e)}")
    failed += 1
print("-" * 60)
print()


print("=" * 60)
print("ERROR HANDLING TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of 5")
print(f"  Tests failed : {failed} of 5")
print()
if failed == 0:
    print("All tests passed! ✅")
    print("Your agent handles all API failures gracefully.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
print()
