import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.rag.retrieval_with_threshold import retrieve_with_threshold
from src.rag.rag_config import CONFIDENCE_THRESHOLD

print("=" * 60)
print("SmartDesk AI — Confidence Threshold Test")
print(f"Threshold set at: {round(CONFIDENCE_THRESHOLD * 100, 1)}%")
print("=" * 60)
print()

test_cases = [
    {"query": "How do I reset my password?",         "expected": "FOUND",     "type": "IN-SCOPE"},
    {"query": "How many sick leave days do I get?",  "expected": "FOUND",     "type": "IN-SCOPE"},
    {"query": "How do I set up MFA on my phone?",    "expected": "FOUND",     "type": "IN-SCOPE"},
    {"query": "My monitor keeps flickering",         "expected": "NOT_FOUND", "type": "OUT-OF-SCOPE"},
    {"query": "How do I get an office parking permit?", "expected": "NOT_FOUND", "type": "OUT-OF-SCOPE"},
    {"query": "The office printer is jammed",        "expected": "NOT_FOUND", "type": "OUT-OF-SCOPE"},
]

passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    result     = retrieve_with_threshold(test["query"])
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

print("=" * 60)
print("THRESHOLD TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of {len(test_cases)}")
print(f"  Tests failed : {failed} of {len(test_cases)}")
print()

if failed == 0:
    print("All tests passed!")
    print("Confidence threshold is working correctly.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
    print("You may need to adjust confidence_threshold in config.yaml.")
print()
