import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from src.agents.agent import process_message, create_session, INTENT_KB_QUERY
from src.rag.rag_chain import get_rag_answer, ANSWER_FOUND

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

for i, test in enumerate(test_questions, 1):
    print(f"TEST {i} — {test['topic']}")
    print(f"  Question : {test['question']}")
    print()

    session = create_session()
    response = process_message(test["question"], session)
    response_lower = response.lower()

    contains_required = all(
        word in response_lower
        for word in test["must_contain"]
    )

    no_bad_words = all(
        word not in response_lower
        for word in test["must_not_contain"]
    )

    preview = response[:200].replace("\n", " ")
    print(f"  Response : {preview}...")
    print()

    if contains_required and no_bad_words:
        print(f"  Contains required words : PASS ✅")
        print(f"  No escalation words     : PASS ✅")
        print(f"  TEST {i}                : PASS ✅")
        passed += 1
    else:
        if not contains_required:
            missing = [w for w in test["must_contain"] if w not in response_lower]
            print(f"  Contains required words : FAIL ❌")
            print(f"  Missing words           : {missing}")
        if not no_bad_words:
            found_bad = [w for w in test["must_not_contain"] if w in response_lower]
            print(f"  No escalation words     : FAIL ❌")
            print(f"  Found unwanted words    : {found_bad}")
        print(f"  TEST {i}                : FAIL ❌")
        failed += 1

    print("-" * 60)
    print()

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

print("=" * 60)
print("FLOW A TEST SUMMARY")
print("=" * 60)
print(f"  Agent tests passed : {passed} of {len(test_questions)}")
print(f"  Agent tests failed : {failed} of {len(test_questions)}")
print(f"  RAG direct checks  : {rag_passed} of {len(rag_checks)}")
print()

if failed == 0 and rag_passed == len(rag_checks):
    print("All Flow A tests passed! ✅")
elif failed <= 1:
    print("Flow A is mostly working. ✅")
else:
    print("Flow A needs attention.")
print()
