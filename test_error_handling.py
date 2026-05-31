# ── test_error_handling.py ───────────────────────────────────────
# Tests error handling for API failures.
# Simulates failures by temporarily breaking connections
# and confirms the agent responds gracefully not by crashing.
# Required by Section 4.3 of the capstone document.
# ────────────────────────────────────────────────────────────────

from agent import (
    process_message,
    create_session,
    build_api_error_response,
    handle_ticket_confirmed,
    handle_check_status
)
from unittest.mock import patch

print("=" * 60)
print("SmartDesk AI — Error Handling Test")
print("=" * 60)
print()

passed = 0
failed = 0


# ── TEST 1: build_api_error_response function ────────────────────
print("TEST 1 — API error response builder")
print()

response = build_api_error_response("OpenAI")
print(f"  Response preview : {response[:80]}...")
print()

if "trouble connecting" in response.lower() and \
   "openai" in response.lower():
    print("  TEST 1   : PASS ✅")
    passed += 1
else:
    print("  TEST 1   : FAIL ❌")
    failed += 1

print("-" * 60)
print()


# ── TEST 2: Jira ticket creation failure ─────────────────────────
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

# Simulate Jira being unavailable
with patch("agent.create_ticket") as mock_create:
    mock_create.side_effect = Exception(
        "Simulated Jira connection timeout"
    )
    response = handle_ticket_confirmed(session)

print(f"  Response preview : {response[:80]}...")
print()

if "trouble connecting" in response.lower() or \
   "unable" in response.lower() or \
   "error" in response.lower():
    print("  TEST 2   : PASS ✅")
    print("  Agent handled Jira failure gracefully")
    passed += 1
else:
    print("  TEST 2   : FAIL ❌")
    print("  Expected graceful error message")
    failed += 1

print("-" * 60)
print()


# ── TEST 3: Jira status lookup failure ──────────────────────────
print("TEST 3 — Jira ticket status API failure")
print()

session = create_session()
session["employee_email"] = "test@roadmapconsulting.com"

# Simulate Jira being unavailable
with patch("agent.get_ticket_status") as mock_status:
    mock_status.side_effect = Exception(
        "Simulated Jira authentication failure"
    )
    response = handle_check_status(session)

print(f"  Response preview : {response[:80]}...")
print()

if "trouble connecting" in response.lower() or \
   "error" in response.lower():
    print("  TEST 3   : PASS ✅")
    print("  Agent handled Jira status failure gracefully")
    passed += 1
else:
    print("  TEST 3   : FAIL ❌")
    print("  Expected graceful error message")
    failed += 1

print("-" * 60)
print()


# ── TEST 4: RAG pipeline failure ────────────────────────────────
print("TEST 4 — RAG pipeline OpenAI API failure")
print()

session = create_session()

# Simulate OpenAI being unavailable
with patch("agent.get_rag_answer") as mock_rag:
    mock_rag.side_effect = Exception(
        "Simulated OpenAI rate limit exceeded"
    )
    response = process_message(
        "How do I reset my password?",
        session
    )

print(f"  Response preview : {response[:80]}...")
print()

if "trouble connecting" in response.lower() or \
   "error" in response.lower() or \
   "moment" in response.lower():
    print("  TEST 4   : PASS ✅")
    print("  Agent handled RAG failure gracefully")
    passed += 1
else:
    print("  TEST 4   : FAIL ❌")
    print("  Expected graceful error message")
    failed += 1

print("-" * 60)
print()


# ── TEST 5: Agent never crashes on any exception ─────────────────
print("TEST 5 — Agent never crashes on unexpected exception")
print()

session = create_session()

try:
    # Simulate a catastrophic unexpected error
    with patch("agent.detect_intent") as mock_intent:
        mock_intent.side_effect = Exception(
            "Simulated catastrophic failure"
        )
        response = process_message(
            "What is my ticket status?",
            session
        )

    print(f"  Response preview : {response[:80]}...")
    print()
    print("  TEST 5   : PASS ✅")
    print("  Agent did not crash on unexpected exception")
    passed += 1

except Exception as e:
    print(f"  TEST 5   : FAIL ❌")
    print(f"  Agent crashed with: {str(e)}")
    failed += 1

print("-" * 60)
print()


# ── FINAL SUMMARY ────────────────────────────────────────────────
print("=" * 60)
print("ERROR HANDLING TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of 5")
print(f"  Tests failed : {failed} of 5")
print()

if failed == 0:
    print("All tests passed! ✅")
    print()
    print("Your agent handles all API failures gracefully.")
    print("Section 4.3 requirement is fully satisfied.")
    print()
    print("AGENT PHASE COMPLETE!")
    print("Ready to move into the Testing Phase — Task 49.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
print()