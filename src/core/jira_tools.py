import os
from datetime import datetime
from dotenv import load_dotenv
from jira import JIRA
from jira.exceptions import JIRAError

load_dotenv()

JIRA_EMAIL       = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN   = os.getenv("JIRA_API_TOKEN")
JIRA_SERVER      = os.getenv("JIRA_SERVER")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

ISSUE_TYPE = "Task"

TICKET_CREATED = "TICKET_CREATED"
TICKET_FAILED  = "TICKET_FAILED"
TICKETS_FOUND  = "TICKETS_FOUND"
TICKETS_NONE   = "TICKETS_NONE"
TICKETS_FAILED = "TICKETS_FAILED"


def get_jira_client():
    """Creates and returns a connected Jira client."""
    return JIRA(
        server=JIRA_SERVER,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )


def create_ticket(
    employee_email: str,
    summary:        str,
    description:    str,
    category:       str = "General Support"
) -> dict:
    """Creates a new support ticket in Jira."""
    try:
        jira = get_jira_client()

        full_description = (
            f"{description}\n\n"
            f"---\n"
            f"Reported by  : {employee_email}\n"
            f"Category     : {category}\n"
            f"Created by   : SmartDesk AI Agent\n"
            f"Created at   : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        )

        issue_fields = {
            "project"    : {"key": JIRA_PROJECT_KEY},
            "summary"    : summary,
            "description": full_description,
            "issuetype"  : {"name": ISSUE_TYPE},
            "labels"     : ["smartdesk-ai", category.lower().replace(" ", "-")]
        }

        new_issue  = jira.create_issue(fields=issue_fields)
        ticket_url = f"{JIRA_SERVER}/browse/{new_issue.key}"

        return {
            "status"    : TICKET_CREATED,
            "ticket_id" : new_issue.key,
            "ticket_url": ticket_url,
            "summary"   : summary,
            "reason"    : f"Ticket {new_issue.key} created successfully."
        }

    except JIRAError as e:
        return {
            "status"    : TICKET_FAILED,
            "ticket_id" : None,
            "ticket_url": None,
            "summary"   : summary,
            "reason"    : f"Jira API error: {e.status_code} - {e.text}"
        }

    except Exception as e:
        return {
            "status"    : TICKET_FAILED,
            "ticket_id" : None,
            "ticket_url": None,
            "summary"   : summary,
            "reason"    : f"Unexpected error: {str(e)}"
        }


def get_ticket_status(employee_email: str) -> dict:
    """Retrieves all open tickets for a given employee email."""
    try:
        jira = get_jira_client()

        jql = (
            f'project = {JIRA_PROJECT_KEY} '
            f'AND description ~ "{employee_email}" '
            f'ORDER BY created DESC'
        )

        issues = jira.search_issues(
            jql,
            maxResults=10,
            fields="summary,status,created,comment,description"
        )

        if not issues:
            return {
                "status" : TICKETS_NONE,
                "tickets": [],
                "count"  : 0,
                "reason" : f"No tickets found for {employee_email}"
            }

        ticket_list = []
        for issue in issues:
            latest_comment = ""
            comments = issue.fields.comment.comments
            if comments:
                latest_comment = comments[-1].body[:200]

            ticket_list.append({
                "ticket_id"     : issue.key,
                "summary"       : issue.fields.summary,
                "status"        : issue.fields.status.name,
                "created"       : str(issue.fields.created)[:10],
                "ticket_url"    : f"{JIRA_SERVER}/browse/{issue.key}",
                "latest_comment": latest_comment
            })

        return {
            "status" : TICKETS_FOUND,
            "tickets": ticket_list,
            "count"  : len(ticket_list),
            "reason" : f"Found {len(ticket_list)} ticket(s) for {employee_email}"
        }

    except JIRAError as e:
        return {
            "status" : TICKETS_FAILED,
            "tickets": [],
            "count"  : 0,
            "reason" : f"Jira API error: {e.status_code} - {e.text}"
        }

    except Exception as e:
        return {
            "status" : TICKETS_FAILED,
            "tickets": [],
            "count"  : 0,
            "reason" : f"Unexpected error: {str(e)}"
        }


def get_ticket_by_id(ticket_id: str) -> dict:
    """Retrieves a single ticket by its Jira ticket ID."""
    try:
        jira  = get_jira_client()
        issue = jira.issue(ticket_id, fields="summary,status,created,comment")

        latest_comment = ""
        comments = issue.fields.comment.comments
        if comments:
            latest_comment = comments[-1].body[:200]

        return {
            "status"        : TICKETS_FOUND,
            "ticket_id"     : issue.key,
            "summary"       : issue.fields.summary,
            "status_name"   : issue.fields.status.name,
            "created"       : str(issue.fields.created)[:10],
            "ticket_url"    : f"{JIRA_SERVER}/browse/{issue.key}",
            "latest_comment": latest_comment,
            "reason"        : f"Ticket {issue.key} found successfully."
        }

    except JIRAError as e:
        return {
            "status"        : TICKETS_FAILED,
            "ticket_id"     : ticket_id,
            "summary"       : "",
            "status_name"   : "",
            "created"       : "",
            "ticket_url"    : "",
            "latest_comment": "",
            "reason"        : f"Jira error: {e.status_code} - {e.text}"
        }

    except Exception as e:
        return {
            "status"        : TICKETS_FAILED,
            "ticket_id"     : ticket_id,
            "summary"       : "",
            "status_name"   : "",
            "created"       : "",
            "ticket_url"    : "",
            "latest_comment": "",
            "reason"        : f"Unexpected error: {str(e)}"
        }


def format_tickets(tickets: list) -> str:
    """Formats ticket list into readable string for display."""
    if not tickets:
        return "No tickets found."

    lines = []
    for ticket in tickets:
        lines.append(f"🎫 {ticket['ticket_id']} : {ticket['summary']}")
        lines.append(f"   📊 Status  : {ticket['status']}")
        lines.append(f"   📅 Created : {ticket['created']}")
        if ticket.get("latest_comment"):
            lines.append(f"   💬 Update  : {ticket['latest_comment'][:100]}")
        lines.append(f"   🔗 Link    : {ticket['ticket_url']}")
        lines.append("")

    return "\n".join(lines)
