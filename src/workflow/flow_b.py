from src.core.jira_tools import create_ticket, TICKET_CREATED
from src.utils.helpers import (
    ask_for_email,
    build_ticket_summary,
    categorise_query,
    build_api_error_response,
)


def handle_ticket_creation_start(session: dict) -> str:
    """
    Flow B entry — starts ticket creation.
    Asks for email if not known, then shows confirmation summary.
    """
    if not session["employee_email"]:
        session["awaiting_email"] = True
        return (
            "I am sorry I could not find information about that "
            "in my knowledge base.\n\n"
            "I can create a support ticket for the team to "
            "look into this for you.\n\n"
            + ask_for_email()
        )

    query    = session.get("original_query", "Support request")
    email    = session["employee_email"]
    category = categorise_query(query)

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
    Flow B confirmation — called when employee says YES.
    Creates the Jira ticket and returns the result.
    """
    session["awaiting_confirmation"] = False
    ticket_data = session["pending_ticket"]

    if not ticket_data:
        return "Something went wrong. Please try again."

    try:
        result = create_ticket(
            employee_email = ticket_data["email"],
            summary        = ticket_data["summary"],
            description    = ticket_data["description"],
            category       = ticket_data["category"]
        )

        session["pending_ticket"] = None

        if result["status"] == TICKET_CREATED:
            return (
                f"Your support ticket has been created "
                f"successfully!\n\n"
                f"  Ticket ID  : {result['ticket_id']}\n"
                f"  Title      : {result['summary']}\n"
                f"  URL        : {result['ticket_url']}\n\n"
                f"The support team will review your ticket and "
                f"get back to you shortly.\n\n"
                f"Is there anything else I can help you with?"
            )
        else:
            return (
                f"I was unable to create the ticket right now.\n\n"
                f"Error: {result['reason']}\n\n"
                f"Please try again or contact IT directly at\n"
                f"it-support@roadmapconsulting.com or ext. 2020."
            )

    except Exception as e:
        session["pending_ticket"] = None
        print(f"  [Agent] Jira ticket creation error: {str(e)}")
        return build_api_error_response("Jira")
