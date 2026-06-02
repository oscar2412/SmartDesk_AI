import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from dotenv import load_dotenv
from jira import JIRA
from jira.exceptions import JIRAError

load_dotenv()

JIRA_EMAIL       = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN   = os.getenv("JIRA_API_TOKEN")
JIRA_SERVER      = os.getenv("JIRA_SERVER")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

print("=" * 60)
print("SmartDesk AI — Jira Live Connection Test")
print("=" * 60)
print()

print("Test 1: Connecting to Jira...")
print(f"  Server : {JIRA_SERVER}")
print(f"  Email  : {JIRA_EMAIL}")
print()

try:
    jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
    print("  Connection       : SUCCESS ✅")
except JIRAError as e:
    print(f"  Connection       : FAILED ❌")
    print(f"  Error            : {e.status_code} - {e.text}")
    exit()
except Exception as e:
    print(f"  Connection       : FAILED ❌")
    print(f"  Unexpected error : {str(e)}")
    exit()

print()

print("Test 2: Getting your account details...")
try:
    myself        = jira.myself()
    display_name  = myself.get("displayName",  "Unknown")
    account_id    = myself.get("accountId",    "Unknown")
    email_address = myself.get("emailAddress", "Unknown")
    print(f"  Display Name     : {display_name} ✅")
    print(f"  Email Address    : {email_address} ✅")
    print(f"  Account ID       : {account_id[:16]}... ✅")
except Exception as e:
    print(f"  Account details  : FAILED ❌ - {str(e)}")

print()

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

print("Test 4: Getting available issue types...")
try:
    issue_types = jira.issue_types_for_project(JIRA_PROJECT_KEY)
    type_names  = [it.name for it in issue_types]
    print(f"  Issue types found: {type_names} ✅")
except Exception as e:
    print(f"  Issue types      : FAILED ❌ - {str(e)}")

print()

print(f"Test 5: Counting existing tickets in {JIRA_PROJECT_KEY}...")
try:
    jql    = f"project = {JIRA_PROJECT_KEY} ORDER BY created DESC"
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
print("=" * 60)
print("JIRA CONNECTION TEST COMPLETE")
print("=" * 60)
print()
print("If all 5 tests passed your Jira connection is fully working.")
print()
