# ── test_rag_chain.py ────────────────────────────────────────────
# Comprehensive test for the RAG answer function.
# Tests three scenarios:
#   1. In-scope IT question — should return ANSWER_FOUND
#   2. In-scope HR question — should return ANSWER_FOUND
#   3. Out-of-scope question — should return ANSWER_NOT_FOUND
# ────────────────────────────────────────────────────────────────

from rag_chain import get_rag_answer, ANSWER_FOUND, ANSWER_NOT_FOUND

print("=" * 60)
print("SmartDesk AI — RAG Chain Comprehensive Test")
print("=" * 60)
print()

# ── Test Cases ───────────────────────────────────────────────────
test_cases = [
    {
        "query"    : "How do I set up VPN on my Windows laptop?",
        "expected" : ANSWER_FOUND,
        "type"     : "IN-SCOPE IT"
    },
    {
        "query"    : "How many sick leave days do I get per year?",
        "expected" : ANSWER_FOUND,
        "type"     : "IN-SCOPE HR"
    },
    {
        "query"    : "My monitor keeps flickering all day",
        "expected" : ANSWER_NOT_FOUND,
        "type"     : "OUT-OF-SCOPE"
    }
]

# ── Run Each Test ────────────────────────────────────────────────
passed = 0
failed = 0

for i, test in enumerate(test_cases, 1):
    print(f"TEST {i} — {test['type']}")
    print(f"Query    : {test['query']}")
    print()

    result = get_rag_answer(test["query"])

    is_correct = result["status"] == test["expected"]

    if is_correct:
        verdict = "PASS ✅"
        passed += 1
    else:
        verdict = "FAIL ❌"
        failed += 1

    print(f"Expected : {test['expected']}")
    print(f"Got      : {result['status']}")
    print(f"Sources  : {result['sources']}")
    print(f"Verdict  : {verdict}")
    print()
    print("Answer Preview:")
    print("-" * 40)
    # Show first 300 characters of answer
    print(result["answer"][:300] + "...")
    print("-" * 40)
    print()
    print("=" * 60)
    print()

# ── Final Summary ────────────────────────────────────────────────
print("RAG CHAIN TEST SUMMARY")
print(f"  Tests passed : {passed} of {len(test_cases)}")
print(f"  Tests failed : {failed} of {len(test_cases)}")
print()

if failed == 0:
    print("All tests passed!")
    print("RAG chain is working correctly.")
    print("Ready to build the agent in Task 41.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")