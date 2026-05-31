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



# ── Response Helpers ─────────────────────────────────────────────

def build_greeting() -> str:
    """Returns the agent's opening greeting message."""
    return (
        "Hello! I am SmartDesk AI, your IT and HR support "
        "assistant at Roadmap Consulting.\n\n"
        "I can help you with:\n"
        "  IT support questions (passwords, VPN, MFA, email)\n"
        "  HR policy questions (leave, WFH, reimbursement)\n"
        "  Creating support tickets for issues I cannot solve\n"
        "  Checking the status of your existing tickets\n\n"
        "How can I help you today?"
    )


def build_unclear_response() -> str:
    """Returns a polite response for unclear messages."""
    return (
        "I am not sure I understood that. Could you please "
        "rephrase your question?\n\n"
        "For example you could ask me:\n"
        "  'How do I reset my password?'\n"
        "  'How many leave days do I get?'\n"
        "  'What is the status of my ticket?'"
    )


def ask_for_email() -> str:
    """Returns the email request message."""
    return (
        "Could you please share your work email address "
        "so I can look that up for you?"
    )


def build_ticket_summary(query: str, email: str, category: str) -> str:
    """
    Builds a human readable ticket summary for confirmation.
    Called before asking the employee to confirm ticket creation.
    """
    return (
        f"I would like to create a support ticket for you.\n\n"
        f"Here are the details:\n\n"
        f"  Title    : {query[:80]}\n"
        f"  Category : {category}\n"
        f"  Email    : {email}\n\n"
        f"Shall I go ahead and create this ticket?\n"
        f"Please type yes or no."
    )


def categorise_query(query: str) -> str:
    """
    Determines the ticket category based on keywords
    in the query. Returns IT Support or HR Support.
    """
    hr_keywords = [
        "leave", "holiday", "vacation", "sick", "maternity",
        "paternity", "wfh", "work from home", "reimbursement",
        "salary", "payroll", "hr", "onboarding", "policy"
    ]
    query_lower = query.lower()
    for keyword in hr_keywords:
        if keyword in query_lower:
            return "HR Support"
    return "IT Support"


# ── Core Agent Response Function ─────────────────────────────────

def process_message(user_message: str, session: dict) -> str:
    """
    The heart of the agent. Takes a single employee message
    and the current session state. Returns the agent response.

    This function handles all three flows:
      Flow A — KB answer
      Flow B — Ticket creation with confirmation
      Flow C — Ticket status check

    Parameters:
        user_message : the raw message from the employee
        session      : the current session state dictionary

    Returns:
        A string response to send back to the employee
    """

    # Clean up the input
    message = user_message.strip()

    # ── Handle empty messages ────────────────────────────────────
    if not message:
        return "I did not catch that. Could you please type your question?"

    # ── Add message to chat history ──────────────────────────────
    session["chat_history"].append(
        HumanMessage(content=message)
    )

    # ────────────────────────────────────────────────────────────
    # SPECIAL STATE: Waiting for email address
    # ────────────────────────────────────────────────────────────
    if session["awaiting_email"]:
        # Treat this message as an email address
        email = message.strip().lower()

        # Basic email validation
        if "@" not in email or "." not in email:
            return (
                "That does not look like a valid email address. "
                "Please enter your work email address "
                "(for example: yourname@roadmapconsulting.com)"
            )

        # Save the email to session
        session["employee_email"]  = email
        session["awaiting_email"]  = False

        # Now decide what to do based on the last intent
        if session["last_intent"] == INTENT_CHECK_STATUS:
            # They were asking for ticket status
            return handle_check_status(session)

        elif session["last_intent"] == INTENT_KB_QUERY:
            # They were in the ticket creation flow
            return handle_ticket_creation_start(session)

        else:
            return handle_check_status(session)

    # ────────────────────────────────────────────────────────────
    # SPECIAL STATE: Waiting for yes/no ticket confirmation
    # ────────────────────────────────────────────────────────────
    if session["awaiting_confirmation"]:
        response_lower = message.lower().strip()

        if response_lower in ["yes", "y", "sure", "go ahead",
                               "ok", "okay", "yep", "yeah"]:
            return handle_ticket_confirmed(session)

        elif response_lower in ["no", "n", "cancel", "stop",
                                  "nope", "nah", "dont", "don't"]:
            session["awaiting_confirmation"] = False
            session["pending_ticket"]        = None
            return (
                "No problem! The ticket has not been created.\n\n"
                "Is there anything else I can help you with?"
            )
        else:
            return (
                "I did not quite catch that. "
                "Please type yes to create the ticket "
                "or no to cancel."
            )

    # ────────────────────────────────────────────────────────────
    # NORMAL FLOW: Detect intent and route
    # ────────────────────────────────────────────────────────────
    intent = detect_intent(message)
    session["last_intent"] = intent

    if intent == INTENT_CHECK_STATUS:
        return handle_check_status_intent(message, session)

    elif intent == INTENT_KB_QUERY:
        return handle_kb_query(message, session)

    else:
        # UNCLEAR intent
        return build_unclear_response()



# ── Flow Handlers ────────────────────────────────────────────────

def handle_kb_query(message: str, session: dict) -> str:
    """
    Handles Flow A — Knowledge base query.
    If RAG finds an answer returns it.
    If not found escalates to Flow B ticket creation.
    """

    # Call the RAG chain
    rag_result = get_rag_answer(
        query        = message,
        chat_history = session["chat_history"]
    )

    if rag_result["status"] == ANSWER_FOUND:
        # Flow A — return the grounded answer
        answer  = rag_result["answer"]
        sources = format_sources(rag_result["sources"])
        response = answer
        if sources:
            response += f"\n\n{sources}"
        return response

    else:
        # Flow B — escalate to ticket creation
        session["original_query"] = message
        return handle_ticket_creation_start(session)


def handle_ticket_creation_start(session: dict) -> str:
    """
    Starts the ticket creation flow.
    Asks for email if not known then shows summary.
    """

    # Do we already have the email from earlier in this session?
    if not session["employee_email"]:
        session["awaiting_email"] = True
        return (
            "I am sorry I could not find information about that "
            "in my knowledge base.\n\n"
            "I can create a support ticket for the team to "
            "look into this for you.\n\n"
            + ask_for_email()
        )

    # We have the email — build and show the ticket summary
    query    = session.get("original_query", "Support request")
    email    = session["employee_email"]
    category = categorise_query(query)

    # Store the pending ticket details
    session["pending_ticket"] = {
        "summary"    : query[:80],
        "description": (
            f"Employee submitted this request via SmartDesk AI: "
            f"{query}"
        ),
        "category"   : category,
        "email"      : email
    }

    session["awaiting_confirmation"] = True
    return build_ticket_summary(query, email, category)


def handle_ticket_confirmed(session: dict) -> str:
    """
    Called when employee confirms ticket creation with yes.
    Creates the ticket and returns the result.
    """

    session["awaiting_confirmation"] = False
    ticket_data = session["pending_ticket"]

    if not ticket_data:
        return "Something went wrong. Please try again."

    # Create the ticket in Jira
    result = create_ticket(
        employee_email = ticket_data["email"],
        summary        = ticket_data["summary"],
        description    = ticket_data["description"],
        category       = ticket_data["category"]
    )

    # Clear the pending ticket
    session["pending_ticket"] = None

    if result["status"] == TICKET_CREATED:
        return (
            f"Your support ticket has been created successfully!\n\n"
            f"  Ticket ID  : {result['ticket_id']}\n"
            f"  Title      : {result['summary']}\n"
            f"  URL        : {result['ticket_url']}\n\n"
            f"The support team will review your ticket and "
            f"get back to you shortly.\n\n"
            f"Is there anything else I can help you with?"
        )
    else:
        return (
            "I am sorry — I was unable to create the ticket "
            "right now. There may be a connection issue.\n\n"
            f"Error details: {result['reason']}\n\n"
            "Please try again in a moment or contact IT directly "
            "at it-support@roadmapconsulting.com"
        )


def handle_check_status_intent(message: str, session: dict) -> str:
    """
    Entry point for Flow C — ticket status check.
    Asks for email if not already known.
    """

    if not session["employee_email"]:
        session["awaiting_email"] = True
        return ask_for_email()

    return handle_check_status(session)


def handle_check_status(session: dict) -> str:
    """
    Performs the actual ticket status lookup
    once we have the employee email.
    """

    email  = session["employee_email"]
    result = get_ticket_status(email)

    if result["status"] == TICKETS_FOUND:
        count = result["count"]
        tickets_text = format_tickets(result["tickets"])
        return (
            f"I found {count} ticket(s) for {email}:\n\n"
            f"{tickets_text}"
            f"Is there anything else I can help you with?"
        )
    else:
        return (
            f"I could not find any open tickets for {email}.\n\n"
            "Would you like me to create a new support ticket?\n"
            "If so please describe the issue and I will get "
            "that set up for you."
        )


# ================================================================
# ================================================================

# ── Main Agent Runner ────────────────────────────────────────────
# This runs when you type: python agent.py
# It starts the interactive conversation loop.

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

    # Start a fresh session
    session = create_session()

    # Print the greeting
    print(f"SmartDesk : {build_greeting()}")
    print()

    # Main conversation loop
    while True:
        try:
            # Get employee input
            user_input = input("You        : ").strip()

            # Check for exit commands
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                print()
                print("SmartDesk : Thank you for using SmartDesk AI.")
                print("           Have a great day!")
                print()
                break

            # Check for new session command
            if user_input.lower() in ["new", "restart", "reset"]:
                session = create_session()
                print()
                print("SmartDesk : Starting a new conversation.")
                print(f"           {build_greeting()}")
                print()
                continue

            # Skip empty input
            if not user_input:
                continue

            # Process the message and get response
            print()
            response = process_message(user_input, session)

            # Print the agent response
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

