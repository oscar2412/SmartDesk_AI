import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tokenizers.normalizers import Replace

from src.rag.rag_config_v0 import LLM_MODEL
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

print("SmartDesk AI agent.py loaded successfully.")


# ── Intent Categories ────────────────────────────────────────────

INTENT_KB_QUERY     = "KB_QUERY"
INTENT_CHECK_STATUS = "CHECK_STATUS"
INTENT_UNCLEAR      = "UNCLEAR"


# ── Intent System Prompt ─────────────────────────────────────────

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


# ── Session Factory ──────────────────────────────────────────────

def create_session() -> dict:
    """Creates and returns a fresh session state dictionary."""
    return {
        "employee_email"      : None,
        "pending_ticket"      : None,
        "chat_history"        : [],
        "last_intent"         : None,
        "awaiting_email"      : False,
        "awaiting_confirmation": False,
        "original_query"      : None,
    }


# ── Intent Detection ─────────────────────────────────────────────

def detect_intent(message: str) -> str:
    """Classifies employee message into KB_QUERY or CHECK_STATUS."""
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

        valid_intents = [INTENT_KB_QUERY, INTENT_CHECK_STATUS, INTENT_UNCLEAR]
        if intent in valid_intents:
            return intent

        print(f"  [Intent] Unexpected response: {intent} — defaulting to KB_QUERY")
        return INTENT_KB_QUERY

    except Exception as e:
        print(f"  [Intent] Error calling GPT: {str(e)} — defaulting to KB_QUERY")
        return INTENT_KB_QUERY


# ── Core Orchestrator ────────────────────────────────────────────

def process_message(user_message: str, session: dict) -> str:
    """Routes employee message to correct flow handler."""
    message = user_message.strip()

    if not message:
        return "I did not catch that. Could you please type your question?"

    session["chat_history"].append(HumanMessage(content=message))

    validation = validate_message(user_message)
    if not validation["valid"]:
        return get_validation_response(validation["reason"])

    message = validation["cleaned"]

    if is_greeting(message):
        return build_greeting_response()

    if is_thanks(message):
        return build_thanks_response()

    session["chat_history"].append(HumanMessage(content=message))

    # ── State: waiting for email address ────────────────────────
    if session["awaiting_email"]:
        email = message.strip().lower()

        if "@" not in email or "." not in email:
            return (
                "That does not look like a valid email address. "
                "Please enter your work email address "
                "(for example: yourname@roadmapconsulting.com)"
            )

        session["employee_email"] = email
        session["awaiting_email"] = False

        if session["last_intent"] == INTENT_CHECK_STATUS:
            return handle_check_status(session)
        elif session["last_intent"] == INTENT_KB_QUERY:
            return handle_ticket_creation_start(session)
        else:
            return handle_check_status(session)

    # ── State: waiting for yes/no confirmation ───────────────────
    if session["awaiting_confirmation"]:
        response_lower = message.lower().strip()
        response_words = response_lower.split()

        if any(word in response_words for word in [
            "yes", "sure", "ok", "okay", "yep", "yeah",
            "please", "confirm", "confirmed"
        ]) or any(phrase in response_lower for phrase in [
            "go ahead", "do it", "create it",
            "sounds good", "correct"
        ]):
            return handle_ticket_confirmed(session)

        elif any(word in response_words for word in [
            "no", "cancel", "stop", "nope", "nah",
            "dont", "skip", "discard"
        ]) or any(phrase in response_lower for phrase in [
            "don't", "nevermind", "never mind",
            "forget it", "not now"
        ]):
            session["awaiting_confirmation"] = False
            session["pending_ticket"]        = None
            return (
                "No problem! The ticket has not been created.\n\n"
                "Is there anything else I can help you with?"
            )

        elif response_lower.startswith("change title"):
            new_title = message[len("change title"):].strip()
            if new_title and session["pending_ticket"]:
                session["pending_ticket"]["summary"] = new_title[:80]
                email    = session["employee_email"]
                category = session["pending_ticket"]["category"]
                return (
                    f"Title updated! Here is the revised ticket:\n\n"
                    + build_ticket_summary(new_title, email, category)
                )
            else:
                return (
                    "Please type the new title after 'change title'.\n"
                    "For example: change title My laptop screen is broken"
                )

        else:
            return (
                "I did not quite catch that.\n\n"
                "Please type:\n"
                "  YES to create the ticket\n"
                "  NO to cancel\n"
                "  CHANGE TITLE new title here — to update the title"
            )

    # ── Normal flow: detect intent and route ─────────────────────
    try:
        intent = detect_intent(message)
    except Exception as e:
        print(f"  [Agent] Intent detection error: {str(e)}")
        intent = INTENT_KB_QUERY

    session["last_intent"] = intent

    try:
        if intent == INTENT_CHECK_STATUS:
            return handle_check_status_intent(message, session)
        elif intent == INTENT_KB_QUERY:
            return handle_kb_query(message, session)
        else:
            return build_unclear_response()

    except Exception as e:
        print(f"  [Agent] Flow handler error: {str(e)}")
        return build_api_error_response("the service")


# ── Main Runner ──────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    print("=" * 60)
    print("  SmartDesk AI — Intelligent IT & HR Operations Agent")
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
            print(f"SmartDesk : I encountered an unexpected error.")
            print(f"           Please try again in a moment.")
            print(f"           Error: {str(e)}")
            print()
