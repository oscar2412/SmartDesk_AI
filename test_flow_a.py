# ── test_flow_a.py ───────────────────────────────────────────────
# Official Flow A test scenario from the capstone document.
# Tests that the agent correctly answers IT and HR questions
# from the knowledge base without hallucinating or creating
# unnecessary tickets.
#
# This is the test your evaluator will run to verify Flow A.
# ────────────────────────────────────────────────────────────────

from agent import process_message, create_session, INTENT_KB_QUERY
from rag_chain import get_rag_answer, ANSWER_FOUND

print("=" * 60)
print("SmartDesk AI — Flow A Official Test")
print("Knowledge Base Answer Verification")
print("=" * 60)
print()
print("Testing that the agent correctly answers questions")
print("from the knowledge base without hallucinating.")
print()

passed = 0
failed = 0

# ── Flow A Test Questions ────────────────────────────────────────
# These are real questions an employee would ask.
# All of them should be answerable from your knowledge base.

test_questions = [
    {
        "question" : "How do I reset my password?",
        "topic"    : "IT — Password Reset",
        "must_contain" : ["password", "reset"],
        "must_not_contain" : ["ticket", "sorry", "don't have"]
    },
    {
        "question" : "How do I set up VPN on my Windows laptop?",
        "topic"    : "IT — VPN Setup",
        "must_contain" : ["vpn"],
        "must_not_contain" : ["ticket", "sorry"]
    },
    {
        "question" : "How do I set up MFA on my phone?",
        "topic"    : "IT — MFA Setup",
        "must_contain" : ["mfa", "authenticat"],
        "must_not_contain" : ["ticket", "sorry"]
    },
    {
        "question" : "How many casual leave days do I get per year?",
        "topic"    : "HR — Casual Leave",
        "must_contain" : ["leave", "casual"],
        "must_not_contain" : ["ticket", "sorry"]
    },
   {
        "question" : "What is the work from home policy?",
        "topic"    : "HR — Work From Home",
        "must_contain" : ["work from home"],
        "must_not_contain" : ["ticket", "sorry"]
    },
]

# ── Run Each Test ────────────────────────────────────────────────
for i, test in enumerate(test_questions, 1):
    print(f"TEST {i} — {test['topic']}")
    print(f"  Question : {test['question']}")
    print()

    # Use a fresh session for each test
    session = create_session()

    # Get the agent response
    response = process_message(test["question"], session)
    response_lower = response.lower()

    # Check must_contain words
    contains_required = all(
        word in response_lower
        for word in test["must_contain"]
    )

    # Check must_not_contain words
    no_bad_words = all(
        word not in response_lower
        for word in test["must_not_contain"]
    )

    # Show response preview
    preview = response[:200].replace("\n", " ")
    print(f"  Response : {preview}...")
    print()

    # Evaluate
    if contains_required and no_bad_words:
        print(f"  Contains required words : PASS ✅")
        print(f"  No escalation words     : PASS ✅")
        print(f"  TEST {i}                : PASS ✅")
        passed += 1
    else:
        if not contains_required:
            missing = [
                w for w in test["must_contain"]
                if w not in response_lower
            ]
            print(f"  Contains required words : FAIL ❌")
            print(f"  Missing words           : {missing}")
        if not no_bad_words:
            found_bad = [
                w for w in test["must_not_contain"]
                if w in response_lower
            ]
            print(f"  No escalation words     : FAIL ❌")
            print(f"  Found unwanted words    : {found_bad}")
        print(f"  TEST {i}                : FAIL ❌")
        failed += 1

    print("-" * 60)
    print()

# ── Direct RAG Chain Check ───────────────────────────────────────
print("BONUS CHECK — Direct RAG chain verification")
print("Confirming RAG returns ANSWER_FOUND for KB questions")
print()

rag_checks = [
    "How do I reset my password?",
    "How many sick leave days do I get?",
    "How do I set up MFA?"
]

rag_passed = 0
for question in rag_checks:
    result = get_rag_answer(question)
    status = result["status"]
    if status == ANSWER_FOUND:
        print(f"  '{question[:45]}' → ANSWER_FOUND ✅")
        rag_passed += 1
    else:
        print(f"  '{question[:45]}' → {status} ❌")

print()
print(f"  RAG direct checks : {rag_passed} of {len(rag_checks)} passed")
print()

# ── Final Summary ────────────────────────────────────────────────
print("=" * 60)
print("FLOW A TEST SUMMARY")
print("=" * 60)
print(f"  Agent tests passed : {passed} of {len(test_questions)}")
print(f"  Agent tests failed : {failed} of {len(test_questions)}")
print(f"  RAG direct checks  : {rag_passed} of {len(rag_checks)}")
print()

if failed == 0 and rag_passed == len(rag_checks):
    print("All Flow A tests passed! ✅")
    print()
    print("Your agent correctly answers knowledge base")
    print("questions without hallucinating or escalating.")
    print()
    print("Flow A is verified and ready for your evaluator.")
    print("Ready to move on to Task 50 — Flow B testing.")
elif failed <= 1:
    print("Flow A is mostly working. ✅")
    print()
    print("Minor wording differences are acceptable.")
    print("Check any FAIL results above to understand why.")
    print("Ready to move on to Task 50.")
else:
    print("Flow A needs attention.")
    print()
    print("Review the FAIL results above.")
    print("Common fixes:")
    print("  1. Re-run index_knowledge_base.py")
    print("  2. Lower CONFIDENCE_THRESHOLD in rag_config.py")
    print("  3. Check your knowledge base document content")
print()