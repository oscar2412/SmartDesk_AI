# ── agent.py ─────────────────────────────────────────────────────
# SmartDesk AI — Main Agent Orchestrator
#
# This is the brain of SmartDesk AI. It:
#   1. Detects the employee intent (KB_QUERY or CHECK_STATUS)
#   2. Routes the conversation to the right function
#   3. Manages session state across multiple turns
#   4. Handles human-in-the-loop ticket confirmation
#   5. Returns polite professional responses always
#
# Run this file directly to start the agent:
#   python agent.py
# ────────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from rag_chain import (
    get_rag_answer,
    format_sources,
    ANSWER_FOUND,
    ANSWER_NOT_FOUND
)
from jira_tools import (
    create_ticket,
    get_ticket_status,
    get_ticket_by_id,
    format_tickets,
    TICKET_CREATED,
    TICKET_FAILED,
    TICKETS_FOUND,
    TICKETS_NONE
)
from rag_config import LLM_MODEL

# Load environment variables
load_dotenv()

print("SmartDesk AI agent.py loaded successfully.")


# ── Intent Categories ────────────────────────────────────────────
# These are the three possible intents your agent detects.
# Every employee message maps to exactly one of these.

INTENT_KB_QUERY      = "KB_QUERY"      # Answer from knowledge base
INTENT_CHECK_STATUS  = "CHECK_STATUS"  # Look up ticket status
INTENT_UNCLEAR       = "UNCLEAR"       # Cannot determine intent

# ── Session State Template ───────────────────────────────────────
# This dictionary holds everything the agent remembers
# during a single conversation session.
# A fresh copy is created at the start of each conversation.

def create_session() -> dict:
    """
    Creates and returns a fresh session state dictionary.
    Called once at the start of every new conversation.
    """
    return {
        # Employee information
        "employee_email"     : None,

        # Ticket being built (before confirmation)
        "pending_ticket"     : None,

        # Full conversation history for GPT context
        "chat_history"       : [],

        # The last detected intent
        "last_intent"        : None,

        # Tracks if we are waiting for email input
        "awaiting_email"     : False,

        # Tracks if we are waiting for yes/no confirmation
        "awaiting_confirmation": False,

        # What triggered the current ticket creation
        "original_query"     : None,
    }


# ── Intent Detection ─────────────────────────────────────────────

# System prompt specifically for intent classification.
# This is different from the RAG system prompt.
# It only asks GPT to classify the intent — nothing else.

INTENT_SYSTEM_PROMPT = """
You are an intent classifier for SmartDesk AI,
a helpdesk assistant for Roadmap Consulting.

Your ONLY job is to classify the employee message into
exactly ONE of these three categories:

KB_QUERY      — The employee is asking a question about
                IT support or HR policy that could be
                answered from an internal knowledge base.
                Examples:
                "How do I reset my password?"
                "How many sick days do I get?"
                "How do I set up VPN on Windows?"
                "My monitor is broken"
                "The printer is jammed"

CHECK_STATUS  — The employee wants to check the status
                of an existing support ticket.
                Examples:
                "What is the status of my ticket?"
                "Any updates on my issue?"
                "Did IT respond to my request?"
                "Check my ticket SSDAI-3"
                "Has anyone looked at my problem yet?"

UNCLEAR       — The message is too vague, off topic,
                or does not fit either category above.
                Examples:
                "Hello"
                "Thanks"
                "OK"
                "What?"

RULES:
1. Respond with ONLY the category name.
   No explanation. No punctuation. No extra words.
2. If in doubt between KB_QUERY and UNCLEAR
   always choose KB_QUERY.
3. Never respond with anything except one of:
   KB_QUERY
   CHECK_STATUS
   UNCLEAR
"""


def detect_intent(message: str) -> str:
    """
    Classifies the employee message into one of three intents.

    Parameters:
        message : the raw employee message string

    Returns:
        One of: KB_QUERY, CHECK_STATUS, UNCLEAR
    """

    # Handle empty or very short messages
    if not message or len(message.strip()) < 2:
        return INTENT_UNCLEAR

    # Call GPT to classify the intent
    try:
        llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        system_msg = SystemMessage(content=INTENT_SYSTEM_PROMPT)
        human_msg  = HumanMessage(content=message)

        response = llm.invoke([system_msg, human_msg])
        intent   = response.content.strip().upper()

        # Validate the response is one of our three intents
        valid_intents = [
            INTENT_KB_QUERY,
            INTENT_CHECK_STATUS,
            INTENT_UNCLEAR
        ]

        if intent in valid_intents:
            return intent
        else:
            # If GPT returns something unexpected default to KB_QUERY
            print(f"  [Intent] Unexpected response: {intent} — defaulting to KB_QUERY")
            return INTENT_KB_QUERY

    except Exception as e:
        # If GPT call fails default to KB_QUERY
        print(f"  [Intent] Error calling GPT: {str(e)} — defaulting to KB_QUERY")
        return INTENT_KB_QUERY


# ── Quick Self Test ──────────────────────────────────────────────
# Only runs when you execute this file directly.
# Tests the detect_intent function with 10 sample messages.

if __name__ == "__main__":
    print("=" * 60)
    print("SmartDesk AI — Intent Detection Test")
    print("=" * 60)
    print()

    test_cases = [
        # KB_QUERY cases
        {
            "message"  : "How do I reset my password?",
            "expected" : INTENT_KB_QUERY,
            "label"    : "IT question"
        },
        {
            "message"  : "How many casual leave days do I get?",
            "expected" : INTENT_KB_QUERY,
            "label"    : "HR question"
        },
        {
            "message"  : "My laptop screen keeps flickering",
            "expected" : INTENT_KB_QUERY,
            "label"    : "IT problem report"
        },
        {
            "message"  : "How do I set up VPN on my Windows laptop?",
            "expected" : INTENT_KB_QUERY,
            "label"    : "IT how-to"
        },
        {
            "message"  : "The office printer on floor 3 is jammed",
            "expected" : INTENT_KB_QUERY,
            "label"    : "Out of scope escalation"
        },
        # CHECK_STATUS cases
        {
            "message"  : "What is the status of my ticket?",
            "expected" : INTENT_CHECK_STATUS,
            "label"    : "Direct status check"
        },
        {
            "message"  : "Any updates on my issue?",
            "expected" : INTENT_CHECK_STATUS,
            "label"    : "Informal status check"
        },
        {
            "message"  : "Has the IT team responded to my request yet?",
            "expected" : INTENT_CHECK_STATUS,
            "label"    : "Status check with context"
        },
        # UNCLEAR cases
        {
            "message"  : "Hello",
            "expected" : INTENT_UNCLEAR,
            "label"    : "Greeting"
        },
        {
            "message"  : "Thanks",
            "expected" : INTENT_UNCLEAR,
            "label"    : "Acknowledgement"
        },
    ]

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"Test {i:2d} — {test['label']}")
        print(f"  Message  : {test['message']}")
        print(f"  Expected : {test['expected']}")

        result = detect_intent(test["message"])
        print(f"  Got      : {result}")

        if result == test["expected"]:
            print(f"  Verdict  : PASS ✅")
            passed += 1
        else:
            print(f"  Verdict  : FAIL ❌")
            failed += 1

        print()

    print("=" * 60)
    print("INTENT DETECTION TEST SUMMARY")
    print("=" * 60)
    print(f"  Tests passed : {passed} of {len(test_cases)}")
    print(f"  Tests failed : {failed} of {len(test_cases)}")
    print()

    if failed == 0:
        print("All tests passed! ✅")
        print()
        print("Intent detection is working correctly.")
        print("Ready to build the full agent loop in Task 45.")
    else:
        print("Some tests failed.")
        print("This is normal — GPT can sometimes classify")
        print("borderline cases differently.")
        print()
        print("As long as 8 or more of 10 pass you are ready")
        print("to continue to Task 45.")
    print()
