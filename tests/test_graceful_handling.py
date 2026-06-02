import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.agents.agent import process_message, create_session

print("=" * 60)
print("SmartDesk AI — Graceful Handling Test")
print("=" * 60)
print()

passed = 0
failed = 0


def run_test(test_num, label, message, check_fn, session=None):
    global passed, failed
    if session is None:
        session = create_session()

    print(f"TEST {test_num} — {label}")
    print(f"  Input    : '{message[:60]}'")

    try:
        response = process_message(message, session)
        preview  = response[:100].replace("\n", " ")
        print(f"  Response : {preview}...")
        print()

        if check_fn(response):
            print(f"  TEST {test_num}   : PASS ✅")
            passed += 1
        else:
            print(f"  TEST {test_num}   : FAIL ❌")
            print(f"  Full response: {response}")
            failed += 1

    except Exception as e:
        print(f"  TEST {test_num}   : CRASH ❌")
        print(f"  Error    : {str(e)}")
        failed += 1

    print("-" * 60)
    print()


run_test(1, "Empty message",   "",  lambda r: "did not" in r.lower() or "type" in r.lower())
run_test(2, "Single character input", "x", lambda r: "more information" in r.lower() or "describe" in r.lower())
run_test(3, "Very long message over 1000 characters", "This is a very long message " * 50, lambda r: "long" in r.lower() or "summarise" in r.lower() or "summary" in r.lower())
run_test(4, "Gibberish keyboard mashing", "qwrt zxcvbnm plkjhgf", lambda r: len(r) > 10)
run_test(5, "Simple greeting", "Hello", lambda r: "hello" in r.lower() or "hi" in r.lower() or "help" in r.lower())
run_test(6, "Good morning greeting", "Good morning", lambda r: "hello" in r.lower() or "morning" in r.lower() or "help" in r.lower())
run_test(7, "Thank you message", "Thanks that helped a lot", lambda r: "welcome" in r.lower() or "glad" in r.lower() or "help" in r.lower())
run_test(8, "Completely off topic question", "What is the capital of France?", lambda r: len(r) > 10)
run_test(9, "Out of scope topic from gaps list", "My monitor keeps flickering", lambda r: "ticket" in r.lower() or "support" in r.lower() or "help" in r.lower())
run_test(10, "Frustrated employee message", "This is useless nothing works!", lambda r: len(r) > 10)

print("=" * 60)
print("GRACEFUL HANDLING TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of 10")
print(f"  Tests failed : {failed} of 10")
print()
if failed == 0:
    print("All tests passed! ✅")
    print("Your agent handles all edge cases gracefully.")
else:
    print(f"{failed} test(s) failed or crashed.")
    print("The most important thing is NO CRASHES.")
print()
