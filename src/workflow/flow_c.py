from src.core.jira_tools import get_ticket_status, format_tickets, TICKETS_FOUND
from src.utils.helpers import ask_for_email, build_api_error_response


def handle_check_status_intent(message: str, session: dict) -> str:
    """
    Flow C entry — ticket status check.
    Asks for email if not already known.
    """
    if not session["employee_email"]:
        session["awaiting_email"] = True
        return ask_for_email()

    return handle_check_status(session)


def handle_check_status(session: dict) -> str:
    """
    Flow C lookup — performs the actual Jira status retrieval
    once the employee email is known.
    """
    email = session["employee_email"]

    try:
        result = get_ticket_status(email)

        if result["status"] == TICKETS_FOUND:
            count        = result["count"]
            tickets_text = format_tickets(result["tickets"])
            return (
                f"I found {count} ticket(s) for {email}:\n\n"
                f"{tickets_text}"
                f"Is there anything else I can help you with?"
            )
        else:
            return (
                f"I could not find any open tickets for "
                f"{email}.\n\n"
                f"Would you like me to create a new support "
                f"ticket? If so please describe the issue."
            )

    except Exception as e:
        print(f"  [Agent] Jira status lookup error: {str(e)}")
        return build_api_error_response("Jira")
