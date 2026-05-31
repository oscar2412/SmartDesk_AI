# ── test_edge_cases.py ───────────────────────────────────────────
# Edge case testing for SmartDesk AI agent.
# Tests that the agent handles unusual unexpected and
# boundary condition inputs without crashing.
#
# The most important rule: NO CRASHES ALLOWED.
# The agent must always return a string response.
# ────────────────────────────────────────────────────────────────

from agent import process_message, create_session

print("=" * 60)
print("SmartDesk AI — Edge Case Testing")
print("=" * 60)
print()
print("Rule: Agent must NEVER crash.")
print("Rule: Agent must ALWAYS return a string response.")
print("Rule: Agent must ALWAYS be polite.")
print()

passed  = 0
failed  = 0
crashed = 0


def run_edge_test(test_num, label, message, check_fn=None, session=None):
    """
    Runs a single edge case test.
    Always checks that the agent does not crash first.
    Then applies an optional content check.
    """
    global passed, failed, crashed

    if session is None:
        session = create_session()

    print(f"TEST {test_num:2d} — {label}")

    # Show input safely
    display_msg = str(message)[:60]
    if len(str(message)) > 60:
        display_msg += "..."
    print(f"  Input    : '{display_msg}'")

    # ── Critical check: agent must not crash ─────────────────────
    try:
        response = process_message(message, session)

        # Response must be a non-empty string
        if not isinstance(response, str) or len(response) == 0:
            print(f"  Response : [EMPTY OR NON-STRING]")
            print(f"  TEST {test_num:2d}   : FAIL ❌ — Empty response")
            failed += 1
            print("-" * 60)
            print()
            return

        # Show preview
        preview = response[:80].replace("\n", " ")
        print(f"  Response : {preview}...")
        print()

        # Apply optional content check
        if check_fn is not None:
            if check_fn(response):
                print(f"  No crash         : PASS ✅")
                print(f"  Content check    : PASS ✅")
                print(f"  TEST {test_num:2d}   : PASS ✅")
                passed += 1
            else:
                print(f"  No crash         : PASS ✅")
                print(f"  Content check    : FAIL ❌")
                print(f"  TEST {test_num:2d}   : FAIL ❌")
                failed += 1
        else:
            # No content check — just passing without crash is enough
            print(f"  No crash         : PASS ✅")
            print(f"  TEST {test_num:2d}   : PASS ✅")
            passed += 1

    except Exception as e:
        print(f"  CRASH ❌ : {str(e)}")
        print(f"  TEST {test_num:2d}   : CRASH ❌")
        crashed += 1
        failed  += 1

    print("-" * 60)
    print()


# ════════════════════════════════════════════════════════════════
# CATEGORY 1 — INPUT BOUNDARY TESTS
# ════════════════════════════════════════════════════════════════
print("CATEGORY 1 — Input Boundary Tests")
print()

run_edge_test(
    1, "Empty string",
    "",
    lambda r: len(r) > 5
)

run_edge_test(
    2, "Single space",
    " ",
    lambda r: len(r) > 5
)

run_edge_test(
    3, "Single character",
    "x",
    lambda r: len(r) > 5
)

run_edge_test(
    4, "Very long message — 2000 characters",
    "Tell me about the IT policy. " * 70,
    lambda r: len(r) > 5
)

run_edge_test(
    5, "Message with only numbers",
    "12345678901234567890",
    lambda r: len(r) > 5
)

run_edge_test(
    6, "Message with only special characters",
    "!@#$%^&*()_+-=[]{}|;:',.<>?/",
    lambda r: len(r) > 5
)

# ════════════════════════════════════════════════════════════════
# CATEGORY 2 — CONTENT EDGE CASES
# ════════════════════════════════════════════════════════════════
print("CATEGORY 2 — Content Edge Cases")
print()

run_edge_test(
    7, "Question in all capitals",
    "HOW DO I RESET MY PASSWORD?",
    lambda r: len(r) > 10
)

run_edge_test(
    8, "Question in all lowercase",
    "how do i reset my password",
    lambda r: len(r) > 10
)

run_edge_test(
    9, "Question with extra whitespace",
    "  How   do   I   reset   my   password?  ",
    lambda r: len(r) > 10
)

run_edge_test(
    10, "Repeated question marks",
    "How do I reset my password???",
    lambda r: len(r) > 10
)

run_edge_test(
    11, "Question with emoji",
    "How do I reset my password 🔑?",
    lambda r: len(r) > 10
)

run_edge_test(
    12, "Sensitive looking input — fake password",
    "My password is SuperSecret123!",
    lambda r: len(r) > 10
)

# ════════════════════════════════════════════════════════════════
# CATEGORY 3 — SOCIAL EDGE CASES
# ════════════════════════════════════════════════════════════════
print("CATEGORY 3 — Social Edge Cases")
print()

run_edge_test(
    13, "Rude frustrated message",
    "This system is useless and nothing ever works!",
    lambda r: len(r) > 10
)

run_edge_test(
    14, "Very polite formal message",
    "Good afternoon. I would be most grateful if you could "
    "kindly assist me with resetting my password please.",
    lambda r: len(r) > 10
)

run_edge_test(
    15, "Completely off topic — weather",
    "What is the weather like today in San Antonio?",
    lambda r: len(r) > 10
)

run_edge_test(
    16, "Completely off topic — personal",
    "Can you recommend a good restaurant near the office?",
    lambda r: len(r) > 10
)

run_edge_test(
    17, "Asking agent its name",
    "What is your name?",
    lambda r: len(r) > 10
)

run_edge_test(
    18, "Asking agent if it is AI",
    "Are you a real person or a chatbot?",
    lambda r: len(r) > 10
)

# ════════════════════════════════════════════════════════════════
# CATEGORY 4 — SESSION STATE EDGE CASES
# ════════════════════════════════════════════════════════════════
print("CATEGORY 4 — Session State Edge Cases")
print()

# Test: Invalid email format during awaiting_email state
session_email = create_session()
session_email["awaiting_email"]  = True
session_email["last_intent"]     = "KB_QUERY"
session_email["original_query"]  = "My printer is broken"

run_edge_test(
    19, "Invalid email format when email expected",
    "notanemail",
    lambda r: "email" in r.lower() or "valid" in r.lower(),
    session=session_email
)

# Test: Random text during awaiting_confirmation state
session_confirm = create_session()
session_confirm["awaiting_confirmation"] = True
session_confirm["employee_email"]        = "test@roadmapconsulting.com"
session_confirm["pending_ticket"] = {
    "summary"    : "Test ticket",
    "description": "Test",
    "category"   : "IT Support",
    "email"      : "test@roadmapconsulting.com"
}

run_edge_test(
    20, "Random text when yes/no expected",
    "purple elephant",
    lambda r: "yes" in r.lower() or "no" in r.lower(),
    session=session_confirm
)

# ════════════════════════════════════════════════════════════════
# CATEGORY 5 — REPETITION TESTS
# ════════════════════════════════════════════════════════════════
print("CATEGORY 5 — Repetition Tests")
print()

# Test: Same question asked multiple times in same session
session_repeat = create_session()
print("TEST 21 — Same question asked 3 times in same session")
print()

repeat_question = "How do I reset my password?"
all_responded   = True

for attempt in range(1, 4):
    try:
        response = process_message(repeat_question, session_repeat)
        if not response or len(response) < 5:
            all_responded = False
        print(f"  Attempt {attempt} : {response[:60].replace(chr(10), ' ')}...")
    except Exception as e:
        print(f"  Attempt {attempt} : CRASH ❌ — {str(e)}")
        all_responded = False

print()
if all_responded:
    print("  All 3 attempts responded : PASS ✅")
    print("  TEST 21   : PASS ✅")
    passed += 1
else:
    print("  TEST 21   : FAIL ❌")
    failed += 1

print("-" * 60)
print()

# ── FINAL SUMMARY ────────────────────────────────────────────────
total_tests = passed + failed
print("=" * 60)
print("EDGE CASE TEST SUMMARY")
print("=" * 60)
print(f"  Total tests  : {total_tests}")
print(f"  Tests passed : {passed}")
print(f"  Tests failed : {failed}")
print(f"  Crashes      : {crashed}")
print()

if crashed == 0:
    print("Zero crashes! ✅")
    print("Your agent never crashed on any edge case input.")
    print()

if failed == 0:
    print("All edge case tests passed! ✅")
    print()
    print("Your agent is robust and production ready.")
    print("Ready to move on to Task 53.")
elif failed <= 3 and crashed == 0:
    print("Agent is robust with minor wording differences. ✅")
    print()
    print(f"  {failed} test(s) failed on wording checks.")
    print("  Zero crashes is the most important result.")
    print("  Ready to move on to Task 53.")
else:
    print("Some edge cases need attention.")
    print()
    if crashed > 0:
        print(f"  CRITICAL: {crashed} crash(es) detected!")
        print("  Crashes must be fixed before submission.")
    print("  Review FAIL results above.")
print()