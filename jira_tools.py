# ── jira_tools.py ────────────────────────────────────────────────
# Jira integration tools for SmartDesk AI.
# Contains two main functions:
#   1. create_ticket()     — creates a new Jira support ticket
#   2. get_ticket_status() — retrieves ticket status by email
#
# This module is imported by agent.py in Task 45.
# ────────────────────────────────────────────────────────────────

import os
from datetime import datetime
from dotenv import load_dotenv
from jira import JIRA
from jira.exceptions import JIRAError

# Load environment variables
load_dotenv()

# ── Jira Configuration ───────────────────────────────────────────
JIRA_EMAIL       = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN   = os.getenv("JIRA_API_TOKEN")
JIRA_SERVER      = os.getenv("JIRA_SERVER")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

# ── Issue Type ───────────────────────────────────────────────────
# Use the issue type you noted from Task 36 Test 4
# Common values: "Task", "Story", "Bug", "Service Request"
ISSUE_TYPE = "Task"
#ISSUE_TYPE = "Story"

# ── Result Types ─────────────────────────────────────────────────
TICKET_CREATED = "TICKET_CREATED"
TICKET_FAILED  = "TICKET_FAILED"
TICKETS_FOUND  = "TICKETS_FOUND"
TICKETS_NONE   = "TICKETS_NONE"
TICKETS_FAILED = "TICKETS_FAILED"


# ── Connect to Jira ──────────────────────────────────────────────
def get_jira_client():
    """
    Creates and returns a connected Jira client.
    Called at the start of each function to ensure
    a fresh connection every time.
    """
    return JIRA(
        server=JIRA_SERVER,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )


# ── Function 1: Create Ticket ────────────────────────────────────

def create_ticket(
    employee_email: str,
    summary:        str,
    description:    str,
    category:       str = "General Support"
) -> dict:
    """
    Creates a new support ticket in Jira.

    Parameters:
        employee_email : email of the employee reporting the issue
        summary        : short one-line title of the ticket
        description    : detailed description of the issue
        category       : type of issue (IT Support or HR Support)

    Returns a dictionary with:
        status     : TICKET_CREATED or TICKET_FAILED
        ticket_id  : the new ticket ID e.g. SSDAI-2
        ticket_url : direct link to the ticket in Jira
        summary    : the ticket title
        reason     : explanation of the result
    """

    try:
        # Connect to Jira
        jira = get_jira_client()

        # Build the full description with metadata
        full_description = (
            f"{description}\n\n"
            f"---\n"
            f"Reported by  : {employee_email}\n"
            f"Category     : {category}\n"
            f"Created by   : SmartDesk AI Agent\n"
            f"Created at   : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        )

        # Define the ticket fields
        issue_fields = {
            "project"    : {"key": JIRA_PROJECT_KEY},
            "summary"    : summary,
            "description": full_description,
            "issuetype"  : {"name": ISSUE_TYPE},
            "labels"     : ["smartdesk-ai", category.lower().replace(" ", "-")]
        }

        # Create the ticket in Jira
        new_issue = jira.create_issue(fields=issue_fields)

        # Build the direct URL to the ticket
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


# ── Function 2: Get Ticket Status ────────────────────────────────

def get_ticket_status(employee_email: str) -> dict:
    """
    Retrieves all open tickets for a given employee email.

    Parameters:
        employee_email : email of the employee to look up

    Returns a dictionary with:
        status  : TICKETS_FOUND, TICKETS_NONE, or TICKETS_FAILED
        tickets : list of ticket details
        count   : number of tickets found
        reason  : explanation of the result
    """

    try:
        # Connect to Jira
        jira = get_jira_client()

        # Build JQL query to find tickets by this employee
        # Searches in description for their email
        jql = (
            f'project = {JIRA_PROJECT_KEY} '
            f'AND description ~ "{employee_email}" '
            f'ORDER BY created DESC'
        )

        # Search for matching tickets
        issues = jira.search_issues(
            jql,
            maxResults=10,
            fields="summary,status,created,comment,description"
        )

        # If no tickets found
        if not issues:
            return {
                "status" : TICKETS_NONE,
                "tickets": [],
                "count"  : 0,
                "reason" : f"No tickets found for {employee_email}"
            }

        # Build the ticket details list
        ticket_list = []
        for issue in issues:
            # Get the latest comment if any exist
            latest_comment = ""
            comments = issue.fields.comment.comments
            if comments:
                latest = comments[-1]
                latest_comment = latest.body[:200]

            ticket_info = {
                "ticket_id"     : issue.key,
                "summary"       : issue.fields.summary,
                "status"        : issue.fields.status.name,
                "created"       : str(issue.fields.created)[:10],
                "ticket_url"    : f"{JIRA_SERVER}/browse/{issue.key}",
                "latest_comment": latest_comment
            }
            ticket_list.append(ticket_info)

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


# ── Quick Self Test ──────────────────────────────────────────────
# Only runs when you execute this file directly.
# Does not run when imported by agent.py.

if __name__ == "__main__":
    print("=" * 60)
    print("jira_tools.py — Quick Self Test")
    print("=" * 60)
    print()
    print("Testing create_ticket function...")
    print()

    result = create_ticket(
        employee_email = "test.employee@roadmapconsulting.com",
        summary        = "Quick self test ticket from jira_tools.py",
        description    = "This is a test ticket created by the SmartDesk AI quick self test. Safe to delete.",
        category       = "IT Support"
    )

    print(f"Status     : {result['status']}")
    print(f"Ticket ID  : {result['ticket_id']}")
    print(f"Ticket URL : {result['ticket_url']}")
    print(f"Reason     : {result['reason']}")
    print()

    if result["status"] == TICKET_CREATED:
        print("create_ticket  : PASS ✅")
        print()
        print("Now testing get_ticket_status function...")
        print()

        status_result = get_ticket_status(
            "test.employee@roadmapconsulting.com"
        )

        print(f"Status  : {status_result['status']}")
        print(f"Count   : {status_result['count']}")
        print(f"Reason  : {status_result['reason']}")
        print()

        if status_result["status"] == TICKETS_FOUND:
            print("get_ticket_status : PASS ✅")
            print()
            print("Most recent ticket:")
            ticket = status_result["tickets"][0]
            print(f"  ID      : {ticket['ticket_id']}")
            print(f"  Summary : {ticket['summary']}")
            print(f"  Status  : {ticket['status']}")
            print(f"  URL     : {ticket['ticket_url']}")
        else:
            print("get_ticket_status : FAIL ❌")
            print(f"Reason  : {status_result['reason']}")
    else:
        print("create_ticket  : FAIL ❌")
        print(f"Reason  : {result['reason']}")

    print()
    print("=" * 60)
    print("Quick self test complete.")
    print("Check your Jira project to see the test ticket.")
    print("=" * 60)

