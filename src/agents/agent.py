import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.rag.rag_config import LLM_MODEL
from src.utils.helpers import (
    build_greeting,
    build_greeting_response,
    build_thanks_response,
    build_unclear_response,
    build_api_error_response,
    build_ticket_summary,
    validate_message,
    get_validation_response,
    is_greeting,
    is_thanks,
)
from src.workflow.flow_a import handle_kb_query
from src.workflow.flow_b import handle_ticket_creation_start, handle_ticket_confirmed
from src.workflow.flow_c import handle_check_status_intent, handle_check_status

load_dotenv()

# ── Intent Categories ────────────────────────────────────────────

INTENT_KB_QUERY     = "KB_QUERY"
INTENT_CHECK_STATUS = "CHECK_STATUS"
INTENT_UNCLEAR      = "UNCLEAR"

# ── Words that close a conversation politely ─────────────────────

CLOSING_WORDS = [
    "no", "nope", "nah", "no thanks", "no thank you",
    "that's all", "thats all", "all good", "all set",
    "nothing else", "that's it", "thats it", "done",
    "goodbye", "bye", "take care", "have a good day",
    "ok", "okay", "k", "kk", "got it", "understood",
    "sounds good", "perfect", "great", "awesome",
    "cool", "nice", "good", "alright", "alrighty",
    "noted", "thanks", "thank you", "cheers"
]

# ── Work-related keywords ─────────────────────────────────────────
# Used to detect if a message has ANY workplace relevance

WORK_KEYWORDS = [
    "password", "vpn", "mfa", "email", "laptop", "computer",
    "printer", "monitor", "screen", "wifi", "internet",
    "software", "hardware", "phone", "mobile", "office",
    "access", "login", "account", "network", "system",
    "leave", "holiday", "vacation", "sick", "wfh",
    "work from home", "remote", "payroll", "salary",
    "reimbursement", "onboarding", "hr", "ticket",
    "broken", "not working", "issue", "problem", "error",
    "slow", "crash", "frozen", "help", "support", "fix",
    "install", "setup", "set up", "configure", "update",
    "light", "desk", "chair", "door", "key", "badge",
    "parking", "gym", "cafeteria", "floor", "building",
    "projector", "headset", "keyboard", "mouse", "cable",
    "charger", "power", "outlet", "battery", "fan",
    "camera", "webcam", "microphone", "speaker", "headphone"
]

# ── Personal/non-work question starters ──────────────────────────

PERSONAL_STARTERS = [
    "where is my", "where are my", "have you seen my",
    "what is the meaning", "who is my", "find my",
    "where the", "where is the", "where are the",
    "what is love", "who is god", "tell me a joke",
    "sing me", "write me a poem", "what is the weather",
    "book me", "order me", "what should i eat",
    "recommend a movie", "recommend a restaurant",
    "what is my horoscope", "predict my future",
    "what is 2 plus", "what is 2 times",
    "can you be my", "will you be my",
    "i lost my", "i can't find my", "where did i put"
]


# ── Intent System Prompt ─────────────────────────────────────────

INTENT_SYSTEM_PROMPT = """
You are an intent classifier for SmartDesk AI,
a helpdesk assistant for Roadmap Consulting.

Your ONLY job is to classify the employee message into
exactly ONE of these three categories:

KB_QUERY      - The employee is asking a question about
                IT support or HR policy OR reporting any
                kind of problem or issue at work.
                When in doubt ALWAYS choose KB_QUERY.
                Examples:
                "How do I reset my password?"
                "How many sick days do I get?"
                "How do I set up VPN on Windows?"
                "My monitor is broken"
                "The printer is jammed"
                "My light won't turn on"
                "My computer is slow"
                "I need help with something"
                "leave" or "leave time" or "casual leave"
                "password" or "VPN" or "MFA"

CHECK_STATUS  - The employee specifically wants to check
                the status of an existing support ticket.
                Examples:
                "What is the status of my ticket?"
                "Any updates on my issue?"
                "Did IT respond to my request?"
                "Check my ticket SSDAI-3"
                "ticket status"

UNCLEAR       - ONLY use this when the message is a pure
                greeting or farewell with no work topic.
                Examples:
                "Hello"
                "Thanks"
                "OK"
                "Bye"

RULES:
1. Respond with ONLY the category name.
2. ANY workplace problem or HR/IT topic = KB_QUERY.
3. Single topic words like "leave", "VPN", "password" = KB_QUERY.
4. If in doubt always choose KB_QUERY.
5. Never respond with anything except KB_QUERY, CHECK_STATUS, or UNCLEAR.
"""


# ── Session Factory ──────────────────────────────────────────────

def create_session() -> dict:
    """Creates and returns a fresh session state dictionary."""
    return {
        "employee_email"       : None,
        "pending_ticket"       : None,
        "chat_history"         : [],
        "last_intent"          : None,
        "awaiting_email"       : False,
        "awaiting_confirmation": False,
        "original_query"       : None,
        "last_action_complete" : False,
        "session_ended"        : False,
    }


# ── Intent Detection ─────────────────────────────────────────────

def detect_intent(message: str) -> str:
    """Classifies employee message into KB_QUERY, CHECK_STATUS, or UNCLEAR."""
    if not message or len(message.strip()) < 2:
        return INTENT_UNCLEAR

    try:
        llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        response = llm.invoke([
            SystemMessage(content=INTENT_SYSTEM_PROMPT),
            HumanMessage(content=message)
        ])
        intent = response.content.strip().upper()

        valid = [INTENT_KB_QUERY, INTENT_CHECK_STATUS, INTENT_UNCLEAR]
        if intent in valid:
            return intent

        print(f"  [Intent] Unexpected: {intent} - defaulting to KB_QUERY")
        return INTENT_KB_QUERY

    except Exception as e:
        print(f"  [Intent] Error: {str(e)} - defaulting to KB_QUERY")
        return INTENT_KB_QUERY


# ── Helper Responses ─────────────────────────────────────────────

def build_how_can_i_help() -> str:
    """Returns a prompt asking the employee what they need help with."""
    return (
        "What can I help you with?\n\n"
        "You can ask me about:\n"
        "  IT support (password reset, VPN, MFA, email)\n"
        "  HR policies (leave, WFH, reimbursement)\n"
        "  Creating a support ticket\n"
        "  Checking your ticket status"
    )


def build_farewell() -> str:
    """Returns a polite closing message."""
    return (
        "You are welcome! Have a great day.\n"
        "Feel free to come back any time you need help.\n\n"
        "Enter your question or enter exit/quit to end the session.\n"
    )


def build_standby() -> str:
    """Returns a gentle nudge when session has ended."""
    return (
        "I am here whenever you need help. Just type your question!\n\n"
        "Enter your question or enter exit/quit to end the session.\n"
    )


def is_work_related(message: str) -> bool:
    """Returns True if the message contains any work-related keyword."""
    msg_lower = message.strip().lower()
    return any(k in msg_lower for k in WORK_KEYWORDS)


def is_personal_question(message: str) -> bool:
    """Returns True if the message matches a known personal question pattern."""
    msg_lower = message.strip().lower()
    return any(p in msg_lower for p in PERSONAL_STARTERS)


# ── Core Orchestrator ────────────────────────────────────────────

def process_message(user_message: str, session: dict) -> str:
    """
    Routes employee message to the correct flow handler.

    Check order — MUST NOT change:
    1. Validate message
    2. Handle greetings and thanks
    3. Session ended standby check
    4. SPECIAL STATE: awaiting_confirmation
    5. SPECIAL STATE: awaiting_email
    6. Closing words and acknowledgements
    7. Continuation words (yes/sure when not in special state)
    8. Personal/non-work question filter
    9. Normal intent detection and routing
    """

    # ── 1. Validate ──────────────────────────────────────────────
    validation = validate_message(user_message)
    if not validation["valid"]:
        return get_validation_response(validation["reason"])

    message = validation["cleaned"]
    msg_lower = message.strip().lower()

    # ── 2. Greetings and thanks ───────────────────────────────────
    if is_greeting(message):
        session["session_ended"]        = False
        session["last_action_complete"] = False
        return build_greeting_response()

    if is_thanks(message):
        return build_thanks_response()

    # ── Add to chat history ───────────────────────────────────────
    session["chat_history"].append(HumanMessage(content=message))

    # ── 3. Session ended — gentle standby ────────────────────────
    # After farewell only re-engage on real questions (3+ words or ?)
    if session.get("session_ended"):
        if len(message.split()) >= 3 or message.strip().endswith("?") or is_work_related(message):
            session["session_ended"]        = False
            session["last_action_complete"] = False
            # Fall through to normal flow
        else:
            return build_standby()

    # ────────────────────────────────────────────────────────────
    # 4. SPECIAL STATE: Waiting for yes/no ticket confirmation
    # ────────────────────────────────────────────────────────────
    if session["awaiting_confirmation"]:
        response_words = msg_lower.split()

        # YES — create the ticket
        if any(w in response_words for w in [
            "yes", "sure", "ok", "okay", "yep", "yeah",
            "please", "confirm", "confirmed"
        ]) or any(p in msg_lower for p in [
            "go ahead", "do it", "create it", "sounds good"
        ]):
            session["last_action_complete"] = True
            return handle_ticket_confirmed(session)

        # NO — cancel
        elif any(w in response_words for w in [
            "no", "cancel", "stop", "nope", "nah",
            "dont", "skip", "discard"
        ]) or any(p in msg_lower for p in [
            "don't", "nevermind", "never mind", "forget it", "not now"
        ]):
            session["awaiting_confirmation"] = False
            session["pending_ticket"]        = None
            session["last_action_complete"]  = True
            return (
                "No problem! The ticket has not been created.\n\n"
                "Is there anything else I can help you with?"
            )

        # Change title
        elif msg_lower.startswith("change title"):
            new_title = message[len("change title"):].strip()
            if new_title and session["pending_ticket"]:
                session["pending_ticket"]["summary"] = new_title[:80]
                email    = session["employee_email"]
                category = session["pending_ticket"]["category"]
                return (
                    "Title updated! Here is the revised ticket:\n\n"
                    + build_ticket_summary(new_title, email, category)
                )
            else:
                return (
                    "Please type the new title after 'change title'.\n"
                    "For example: change title My laptop screen is broken"
                )

        # Anything else in confirmation state — treat as new input
        else:
            session["awaiting_confirmation"] = False
            session["pending_ticket"]        = None
            # Fall through to normal flow

    # ────────────────────────────────────────────────────────────
    # 5. SPECIAL STATE: Waiting for email address
    # ────────────────────────────────────────────────────────────
    if session["awaiting_email"]:
        msg_words = msg_lower.split()

        decline_words = [
            "no", "nope", "nevermind", "cancel", "stop",
            "skip", "nah", "back", "quit"
        ]
        decline_phrases = [
            "never mind", "forget it", "not now",
            "no thanks", "no thank you", "don't", "dont"
        ]
        is_declining = (
            any(w in msg_words for w in decline_words) or
            any(p in msg_lower for p in decline_phrases)
        )

        question_starters = [
            "how", "what", "where", "when", "why", "can",
            "could", "is", "are", "do", "does", "help",
            "tell", "show", "explain"
        ]
        is_new_question = (
            message.strip().endswith("?") or
            any(msg_lower.startswith(w) for w in question_starters)
        )

        if is_declining:
            session["awaiting_email"] = False
            session["pending_ticket"] = None
            session["original_query"] = None
            session["last_intent"]    = None
            return (
                "No problem at all!\n\n"
                "Is there anything else I can help you with today?"
            )

        if is_new_question:
            session["awaiting_email"] = False
            session["pending_ticket"] = None
            session["original_query"] = None
            session["last_intent"]    = None
            # Fall through to intent detection

        elif "@" in message and "." in message:
            email = message.strip().lower()
            session["employee_email"] = email
            session["awaiting_email"] = False

            if session["last_intent"] == INTENT_CHECK_STATUS:
                return handle_check_status(session)
            elif session["last_intent"] == INTENT_KB_QUERY:
                return handle_ticket_creation_start(session)
            else:
                return handle_check_status(session)

        else:
            return (
                "That does not look like a valid email address.\n\n"
                "Please enter your work email address or type "
                "NO to cancel."
            )

    # ────────────────────────────────────────────────────────────
    # 6. CLOSING WORDS and acknowledgements
    # ────────────────────────────────────────────────────────────

    # Pure acknowledgements — ok, cool, perfect, noted, bye etc.
    pure_ack = [
        "ok", "okay", "k", "kk", "got it", "understood",
        "perfect", "awesome", "cool", "nice", "alright",
        "alrighty", "noted", "cheers", "bye", "goodbye",
        "take care", "have a good day", "good", "great"
    ]
    if msg_lower in pure_ack:
        if session.get("last_action_complete"):
            session["last_action_complete"] = False
            session["session_ended"]        = True
            session["original_query"]       = None
            session["last_intent"]          = None
            return "Glad I could help! Feel free to come back any time."
        else:
            # Not after completed action — treat as asking for help
            return build_how_can_i_help()

    # Closing words AFTER a completed action
    if session.get("last_action_complete") and msg_lower in CLOSING_WORDS:
        session["last_action_complete"] = False
        session["session_ended"]        = True
        session["original_query"]       = None
        session["last_intent"]          = None
        return build_farewell()

    # Reset completed flag — employee is asking something new
    session["last_action_complete"] = False

    # ────────────────────────────────────────────────────────────
    # 7. CONTINUATION WORDS (yes/sure) when NOT in special state
    # ────────────────────────────────────────────────────────────
    continuation = ["yes", "y", "sure", "yep", "yeah", "yup"]
    if msg_lower in continuation:
        session["pending_ticket"] = None
        session["original_query"] = None
        session["last_intent"]    = None
        return build_how_can_i_help()

    # ────────────────────────────────────────────────────────────
    # 8. PERSONAL / NON-WORK QUESTION FILTER
    # Catch clearly personal questions that have no work keywords
    # ────────────────────────────────────────────────────────────
    if is_personal_question(message) and not is_work_related(message):
        return (
            "I am a workplace support assistant and can only help "
            "with IT support or HR policy questions.\n\n"
            "What IT or HR topic can I help you with today?"
        )

    # ────────────────────────────────────────────────────────────
    # 9. NORMAL FLOW: Detect intent and route
    # ────────────────────────────────────────────────────────────
    try:
        intent = detect_intent(message)
    except Exception as e:
        print(f"  [Agent] Intent detection error: {str(e)}")
        intent = INTENT_KB_QUERY

    session["last_intent"] = intent

    try:
        if intent == INTENT_CHECK_STATUS:
            result = handle_check_status_intent(message, session)
            session["last_action_complete"] = True
            return result
        elif intent == INTENT_KB_QUERY:
            return handle_kb_query(message, session)
        else:
            # UNCLEAR falls back to KB_QUERY
            session["last_intent"] = INTENT_KB_QUERY
            return handle_kb_query(message, session)

    except Exception as e:
        print(f"  [Agent] Flow handler error: {str(e)}")
        return build_api_error_response("the service")


# ── Main Runner ──────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  SmartDesk AI - Intelligent IT & HR Operations Agent")
    print("  Roadmap Consulting Internal Support")
    print("=" * 60)
    print()
    print("Type your question and press Enter.")
    print("Type 'quit' or 'exit' to end the session.")
    print("Type 'new' to start a fresh conversation.")
    print("-" * 60)
    print()

    session = create_session()
    print(f"SmartDesk : {build_greeting()}")
    print()

    while True:
        try:
            user_input = input("You        : ").strip()

            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                print()
                print("SmartDesk : Thank you for using SmartDesk AI.")
                print("           Have a great day!")
                print()
                break

            if user_input.lower() in ["new", "restart", "reset"]:
                session = create_session()
                print()
                print("SmartDesk : Starting a new conversation.")
                print(f"           {build_greeting()}")
                print()
                continue

            if not user_input:
                continue

            print()
            try:
                response = process_message(user_input, session)
            except Exception as e:
                response = (
                    "I encountered an unexpected error. "
                    "Please try again in a moment.\n"
                    f"Error details: {str(e)}"
                )
                print(f"  [Agent] Unexpected error: {str(e)}")

            print(f"SmartDesk : {response}")
            print()

        except KeyboardInterrupt:
            print()
            print()
            print("SmartDesk : Session ended. Goodbye!")
            print()
            break

        except Exception as e:
            print()
            print("SmartDesk : I encountered an unexpected error.")
            print("           Please try again in a moment.")
            print(f"           Error: {str(e)}")
            print()