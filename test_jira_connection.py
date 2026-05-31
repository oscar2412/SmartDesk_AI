# ── test_jira_connection.py ──────────────────────────────────────
# Tests the live connection to your Jira Cloud account.
# Verifies credentials work and SmartDesk project exists.
# Run this before building jira_tools.py in Task 37.
# ────────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv
from jira import JIRA
from jira.exceptions import JIRAError

# Load credentials from .env file
load_dotenv()

JIRA_EMAIL       = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN   = os.getenv("JIRA_API_TOKEN")
JIRA_SERVER      = os.getenv("JIRA_SERVER")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

print("=" * 60)
print("SmartDesk AI — Jira Live Connection Test")
print("=" * 60)
print()

# ── TEST 1: Connect to Jira ───────────────────────────────────────
print("Test 1: Connecting to Jira...")
print(f"  Server : {JIRA_SERVER}")
print(f"  Email  : {JIRA_EMAIL}")
print()

try:
    jira = JIRA(
        server=JIRA_SERVER,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )
    print("  Connection       : SUCCESS ✅")

except JIRAError as e:
    print(f"  Connection       : FAILED ❌")
    print(f"  Error            : {e.status_code} - {e.text}")
    print()
    print("Troubleshooting tips:")
    print("  - Check JIRA_SERVER in your .env file")
    print("  - Check JIRA_EMAIL in your .env file")
    print("  - Check JIRA_API_TOKEN in your .env file")
    print("  - Make sure your Jira API token has not expired")
    exit()

except Exception as e:
    print(f"  Connection       : FAILED ❌")
    print(f"  Unexpected error : {str(e)}")
    exit()

print()

# ── TEST 2: Get Your Account Details ─────────────────────────────
print("Test 2: Getting your account details...")

try:
    myself = jira.myself()
    display_name  = myself.get("displayName",  "Unknown")
    account_id    = myself.get("accountId",    "Unknown")
    email_address = myself.get("emailAddress", "Unknown")

    print(f"  Display Name     : {display_name} ✅")
    print(f"  Email Address    : {email_address} ✅")
    print(f"  Account ID       : {account_id[:16]}... ✅")

except Exception as e:
    print(f"  Account details  : FAILED ❌ - {str(e)}")

print()

# ── TEST 3: Confirm SmartDesk Project Exists ──────────────────────
print(f"Test 3: Looking for project '{JIRA_PROJECT_KEY}'...")

try:
    project = jira.project(JIRA_PROJECT_KEY)
    print(f"  Project Name     : {project.name} ✅")
    print(f"  Project Key      : {project.key} ✅")
    print(f"  Project ID       : {project.id} ✅")

except JIRAError as e:
    print(f"  Project search   : FAILED ❌")
    print(f"  Error            : {e.status_code} - {e.text}")
    print()
    print("Troubleshooting tips:")
    print("  - Check JIRA_PROJECT_KEY in your .env file")
    print("  - Make sure the SmartDesk project exists in Jira")
    print("  - Log in to Jira and confirm the project key is SD")

print()

# ── TEST 4: Get Available Issue Types ────────────────────────────
print("Test 4: Getting available issue types...")

try:
    issue_types = jira.issue_types_for_project(JIRA_PROJECT_KEY)
    type_names  = [it.name for it in issue_types]
    print(f"  Issue types found: {type_names} ✅")
    print()
    print("  Note: We will use one of these when creating")
    print("  tickets in Task 37. Write down the list above.")

except Exception as e:
    print(f"  Issue types      : FAILED ❌ - {str(e)}")

print()

# ── TEST 5: Count Existing Tickets ───────────────────────────────
print(f"Test 5: Counting existing tickets in {JIRA_PROJECT_KEY}...")

try:
    jql = f"project = {JIRA_PROJECT_KEY} ORDER BY created DESC"
    issues = jira.search_issues(jql, maxResults=50)
    print(f"  Tickets found    : {len(issues)} ✅")

    if issues:
        print()
        print("  Most recent tickets:")
        for issue in issues[:3]:
            print(f"    {issue.key} : {issue.fields.summary}")

except Exception as e:
    print(f"  Ticket count     : FAILED ❌ - {str(e)}")

print()

# ── FINAL SUMMARY ────────────────────────────────────────────────
print("=" * 60)
print("JIRA CONNECTION TEST COMPLETE")
print("=" * 60)
print()
print("If all 5 tests passed your Jira connection is")
print("fully working and ready for Task 37.")
print()