# ── test_threshold.py ────────────────────────────────────────────
# Tests the confidence threshold logic.
# IN-SCOPE questions should return FOUND.
# OUT-OF-SCOPE questions should return NOT_FOUND.
# ────────────────────────────────────────────────────────────────

from retrieval_with_threshold import retrieve_with_threshold
from rag_config import CONFIDENCE_THRESHOLD

print("=" * 60)
print("SmartDesk AI — Confidence Threshold Test")
print(f"Threshold set at: {round(CONFIDENCE_THRESHOLD * 100, 1)}%")
print("=" * 60)
print()

# ── Test Cases ───────────────────────────────────────────────────
test_cases = [
    # IN-SCOPE — should return FOUND
    {
        "query"    : "How do I reset my password?",
        "expected" : "FOUND",
        "type"     : "IN-SCOPE"
    },
    {
        "query"    : "How many sick leave days do I get?",
        "expected" : "FOUND",
        "type"     : "IN-SCOPE"
    },
    {
        "query"    : "How do I set up MFA on my phone?",
        "expected" : "FOUND",
        "type"     : "IN-SCOPE"
    },
    # OUT-OF-SCOPE — should return NOT_FOUND
    {
        "query"    : "My monitor keeps flickering",
        "expected" : "NOT_FOUND",
        "type"     : "OUT-OF-SCOPE"
    },
    {
        "query"    : "How do I get an office parking permit?",
        "expected" : "NOT_FOUND",
        "type"     : "OUT-OF-SCOPE"
    },
    {
        "query"    : "The office printer is jammed",
        "expected" : "NOT_FOUND",
        "type"     : "OUT-OF-SCOPE"
    }
]

# ── Run Each Test ────────────────────────────────────────────────
passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    result = retrieve_with_threshold(test["query"])

    # Check if result matches expectation
    is_correct = result["status"] == test["expected"]

    if is_correct:
        verdict = "PASS ✅"
        passed += 1
    else:
        verdict = "FAIL ❌"
        failed += 1

    print(f"Test {i} — {test['type']}")
    print(f"  Query    : {test['query']}")
    print(f"  Expected : {test['expected']}")
    print(f"  Got      : {result['status']}")
    print(f"  Scores   : {result['scores']}")
    print(f"  Reason   : {result['reason']}")
    print(f"  Verdict  : {verdict}")
    print()
    print("-" * 60)
    print()

# ── Final Summary ────────────────────────────────────────────────
print("=" * 60)
print("THRESHOLD TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of {len(test_cases)}")
print(f"  Tests failed : {failed} of {len(test_cases)}")
print()

if failed == 0:
    print("All tests passed!")
    print("Confidence threshold is working correctly.")
    print("Ready to build the RAG chain in Task 34.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
    print("You may need to adjust CONFIDENCE_THRESHOLD")
    print("in rag_config.py and re-run this test.")
print()