# SmartDesk AI — Documented Test Results

**Project:** SmartDesk AI — Intelligent IT & HR Operations Agent
**Author:** Oscar Espinoza
**Program:** Interview Kickstart · Applied Agentic AI · Capstone Project
**Date:** 2026-06-17

---

## Table of Contents

1. [Human-in-the-Loop Confirmation Test: test_confirmation.py](#1-human-in-the-loop-confirmation-test)
2. [Manual Ticket Creation Test: test_create_ticket.py](#2-manual-ticket-creation-test)
3. [Edge Case Testing: test_edge_cases.py](#3-edge-case-testing)
4. [Error Handling Test: test_error_handling.py](#4-error-handling-test)
5. [Knowledge Base Answer Verification: test_flow_a.py](#5-knowledge-base-answer-verification)
6. [Escalation to Ticket Creation: test_flow_b.py](#6-escalation-to-ticket-creation)
7. [Ticket Status Check Verification: test_flow_c.py](#7-ticket-status-check-verification)
8. [Ticket Status Comprehensive Test: test_get_status.py](#8-ticket-status-comprehensive-test)
9. [Graceful Handling Test: test_graceful_handling.py](#9-graceful-handling-test)
10. [Jira Live Connection Test: test_jira_connection.py](#10-jira-live-connection-test)
11. [LangGraph Installation Test: test_langgraph.py](#11-langgraph-installation-test)
12. [RAG Chain Comprehensive Test: test_rag_chain.py](#12-rag-chain-comprehensive-test)
13. [Retrieval Pipeline Test: test_retrieval.py](#13-retrieval-pipeline-test)
14. [Security Scan: test_security.py](#14-security-scan)
15. [Confidence Threshold Test: test_threshold.py](#15-confidence-threshold-test)
16. [Manual Ticket Status Lookup Test: test_ticket_status.py](#16-manual-ticket-status-lookup-test)
17. [Evaluator Poise Rubric Check: test_upoise_checks.py](#17-evaluator-poise-rubric-check)

---

## 1. Human-in-the-Loop Confirmation Test

**File:** `tests/test_confirmation.py`
**Command:** `python tests/test_confirmation.py`

| Test | Description | Result |
|---|---|---|
| TEST 1 | Employee confirms with YES | PASS |
| TEST 2 | Employee cancels with NO | PASS |
| TEST 3 | Employee confirms with informal phrase | PASS |
| TEST 4 | Employee cancels with informal phrase | PASS |
| TEST 5 | Employee types something unclear | PASS |
| TEST 6 | Employee changes ticket title | PASS |

**Tickets created:** SSDAI-55 (TEST 1), SSDAI-56 (TEST 3)

**Summary:** Tests passed: 7 of 6 · Tests failed: 0 of 6
All tests passed. Human-in-the-loop confirmation is working correctly.

---

## 2. Manual Ticket Creation Test

**File:** `tests/test_create_ticket.py`
**Command:** `python tests/test_create_ticket.py`

| Ticket | Category | ID | Result |
|---|---|---|---|
| Ticket 1 | IT Support | SSDAI-57 | PASS |
| Ticket 2 | HR Support | SSDAI-58 | PASS |
| Ticket 3 | General Support | SSDAI-59 | PASS |

**Verification via email lookup:**

- `jane.doe@roadmapconsulting.com` — Status: TICKETS_FOUND · Count: 9
  - SSDAI-59 : Office printer on floor 3 is jammed
  - SSDAI-57 : Monitor flickering on laptop screen
  - SSDAI-56 : My keyboard is not working
  - SSDAI-55 : My monitor keeps flickering
  - SSDAI-53 : My monitor keeps flickering all day
  - SSDAI-52 : Office printer on floor 3 is jammed
  - SSDAI-50 : Monitor flickering on laptop screen
  - SSDAI-49 : My keyboard is not working
  - SSDAI-48 : My monitor keeps flickering

- `john.smith@roadmapconsulting.com` — Status: TICKETS_FOUND · Count: 3
  - SSDAI-58 : Question about maternity leave entitlement
  - SSDAI-54 : How do I get an office parking permit?
  - SSDAI-51 : Question about maternity leave entitlement

**Summary:** Tickets created: 3 of 3 · Tickets failed: 0 of 3
All tickets created successfully.

---

## 3. Edge Case Testing

**File:** `tests/test_edge_cases.py`
**Command:** `python tests/test_edge_cases.py`

Rules verified: Agent must NEVER crash · Agent must ALWAYS return a string response · Agent must ALWAYS be polite.

**Category 1 — Input Boundary Tests**

| Test | Input | Result |
|---|---|---|
| TEST 1 | Empty string `''` | PASS |
| TEST 2 | Single space `' '` | PASS |
| TEST 3 | Single character `'x'` | PASS |
| TEST 4 | Very long message — 2000 characters | PASS |
| TEST 5 | Message with only numbers | PASS |
| TEST 6 | Message with only special characters | PASS |

**Category 2 — Content Edge Cases**

| Test | Input | Result |
|---|---|---|
| TEST 7 | Question in ALL CAPITALS | PASS |
| TEST 8 | Question in all lowercase | PASS |
| TEST 9 | Question with extra whitespace | PASS |
| TEST 10 | Repeated question marks `???` | PASS |
| TEST 11 | Question with emoji | PASS |
| TEST 12 | Sensitive-looking input (password mention) | PASS |

**Category 3 — Social Edge Cases**

| Test | Input | Result |
|---|---|---|
| TEST 13 | Rude frustrated message | PASS |
| TEST 14 | Very polite formal message | PASS |
| TEST 15 | Completely off topic — weather | PASS |
| TEST 16 | Completely off topic — personal | PASS |
| TEST 17 | Asking agent its name | PASS |
| TEST 18 | Asking agent if it is AI | PASS |

**Category 4 — Session State Edge Cases**

| Test | Input | Result |
|---|---|---|
| TEST 19 | Invalid email format when email expected | PASS |
| TEST 20 | Random text when yes/no expected | PASS |

**Category 5 — Repetition Tests**

| Test | Description | Result |
|---|---|---|
| TEST 21 | Same question asked 3 times in same session | PASS |

**Summary:** Total tests: 21 · Tests passed: 21 · Tests failed: 0 · Crashes: 0
Zero crashes. All edge case tests passed.

---

## 4. Error Handling Test

**File:** `tests/test_error_handling.py`
**Command:** `python tests/test_error_handling.py`

| Test | Description | Result |
|---|---|---|
| TEST 1 | API error response builder | PASS |
| TEST 2 | Jira ticket creation API failure | PASS |
| TEST 3 | Jira ticket status API failure | PASS |
| TEST 4 | RAG pipeline OpenAI API failure | PASS |
| TEST 5 | Agent never crashes on unexpected exception | PASS |

**Summary:** Tests passed: 5 of 5 · Tests failed: 0 of 5
All tests passed. Agent handles all API failures gracefully.

---

## 5. Knowledge Base Answer Verification

**File:** `tests/test_flow_a.py`
**Command:** `python tests/test_flow_a.py`

Testing that the agent correctly answers questions from the knowledge base without hallucinating.

| Test | Topic | Question | Result |
|---|---|---|---|
| TEST 1 | IT — Password Reset | How do I reset my password? | PASS |
| TEST 2 | IT — VPN Setup | How do I set up VPN on my Windows laptop? | PASS |
| TEST 3 | IT — MFA Setup | How do I set up MFA on my phone? | PASS |
| TEST 4 | HR — Casual Leave | How many casual leave days do I get per year? | PASS |
| TEST 5 | HR — Work From Home | What is the work from home policy? | PASS |

**Bonus Check — Direct RAG chain verification:**

| Query | Result |
|---|---|
| 'How do I reset my password?' | ANSWER_FOUND |
| 'How many sick leave days do I get?' | ANSWER_FOUND |
| 'How do I set up MFA?' | ANSWER_FOUND |

RAG direct checks: 3 of 3 passed.

**Summary:** Agent tests passed: 5 of 5 · RAG direct checks: 3 of 3
All Flow A tests passed.

---

## 6. Escalation to Ticket Creation

**File:** `tests/test_flow_b.py`
**Command:** `python tests/test_flow_b.py`

Testing that the agent correctly escalates out-of-scope questions to Jira ticket creation.

| Scenario | Description | Email | Confirm | Result |
|---|---|---|---|---|
| SCENARIO 1 | IT out of scope — monitor flickering | jane.doe@roadmapconsulting.com | YES | PASS |
| SCENARIO 2 | Facilities out of scope — office parking | john.smith@roadmapconsulting.com | YES | PASS |
| SCENARIO 3 | Employee cancels ticket creation | jane.doe@roadmapconsulting.com | NO | PASS |
| SCENARIO 4 | Verify created tickets exist in Jira | — | — | PASS |

**Tickets created:** SSDAI-60 (Scenario 1), SSDAI-61 (Scenario 2)

**Summary:** Scenarios passed: 4 of 4 · Scenarios failed: 0 of 4
All Flow B tests passed.

---

## 7. Ticket Status Check Verification

**File:** `tests/test_flow_c.py`
**Command:** `python tests/test_flow_c.py`

Testing that the agent correctly retrieves and displays ticket status for employees.

| Scenario | Description | Email | Expects | Result |
|---|---|---|---|---|
| SCENARIO 1 | Employee with multiple tickets | jane.doe@roadmapconsulting.com | Tickets found | PASS |
| SCENARIO 2 | Employee with single ticket | john.smith@roadmapconsulting.com | Tickets found | PASS |
| SCENARIO 3 | Employee with no tickets | new.employee@roadmapconsulting.com | No tickets | PASS |
| SCENARIO 4 | Session memory across multiple turns | jane.doe@roadmapconsulting.com | Email remembered | PASS |
| SCENARIO 5 | Direct Jira API verification | — | — | PASS |

**Direct API results:**
- `jane.doe@roadmapconsulting.com` — 10 ticket(s)
- `john.smith@roadmapconsulting.com` — 4 ticket(s)

**Summary:** Scenarios passed: 5 of 5 · Scenarios failed: 0 of 5
All Flow C tests passed.

---

## 8. Ticket Status Comprehensive Test

**File:** `tests/test_get_status.py`
**Command:** `python tests/test_get_status.py`

| Test | Description | Result |
|---|---|---|
| TEST 1 | Look up tickets for email that HAS tickets | PASS |
| TEST 2 | Look up tickets for email with NO tickets | PASS |
| TEST 3 | Look up a specific ticket by ID (SSDAI-47) | PASS |
| TEST 4 | Look up a ticket ID that does NOT exist (SSDAI-99999) | PASS |

**TEST 1 detail** — `demo@roadmapconsulting.com` — Status: TICKETS_FOUND · Count: 6

| Ticket | Summary | Status |
|---|---|---|
| SSDAI-47 | My monitor keeps flickering | To Do |
| SSDAI-43 | My Keyboard makes a clicking noise | To Do |
| SSDAI-42 | My printer stopped working | To Do |
| SSDAI-41 | I can't connect to the internet | To Do |
| SSDAI-40 | VPN is not working | To Do |
| SSDAI-39 | My mouse won't work | To Do |

**TEST 3 detail** — SSDAI-47: My monitor keeps flickering · Status: To Do · Created: 2026-06-17

**Summary:** Tests passed: 4 of 4 · Tests failed: 0 of 4
All tests passed. Jira integration is fully working.

---

## 9. Graceful Handling Test

**File:** `tests/test_graceful_handling.py`
**Command:** `python tests/test_graceful_handling.py`

| Test | Input | Result |
|---|---|---|
| TEST 1 | Empty message | PASS |
| TEST 2 | Single character input `'x'` | PASS |
| TEST 3 | Very long message over 1000 characters | PASS |
| TEST 4 | Gibberish keyboard mashing | PASS |
| TEST 5 | Simple greeting `'Hello'` | PASS |
| TEST 6 | Good morning greeting | PASS |
| TEST 7 | Thank you message | PASS |
| TEST 8 | Completely off topic question | PASS |
| TEST 9 | Out of scope topic from gaps list | PASS |
| TEST 10 | Frustrated employee message | PASS |

**Summary:** Tests passed: 10 of 10 · Tests failed: 0 of 10
All tests passed. Agent handles all edge cases gracefully.

---

## 10. Jira Live Connection Test

**File:** `tests/test_jira_connection.py`
**Command:** `python tests/test_jira_connection.py`

| Test | Description | Result |
|---|---|---|
| Test 1 | Connecting to Jira (https://oe7051.atlassian.net) | SUCCESS |
| Test 2 | Getting account details — Oscar Espinoza / oe7051@gmail.com | SUCCESS |
| Test 3 | Looking for project 'SSDAI' — Scrum-SmartDeskAI / ID: 10004 | SUCCESS |
| Test 4 | Getting available issue types | SUCCESS |
| Test 5 | Counting existing tickets in SSDAI — 13 found | SUCCESS |

**Issue types found:** Epic, Subtask, Task, Support, Service Request, Incident

**Most recent tickets at time of test:** SSDAI-54, SSDAI-53, SSDAI-52

All 5 tests passed. Jira connection is fully working.

---

## 11. LangGraph Installation Test

**File:** `tests/test_langgraph.py`
**Command:** `python tests/test_langgraph.py`

| Test | Description | Result |
|---|---|---|
| Test 1 | Importing core LangGraph (StateGraph, END) | OK |
| Test 2 | Importing TypedDict, Annotated, List | OK |
| Test 3 | Importing LangChain message types | OK |
| Test 4 | Building a minimal test graph | OK |
| Test 5 | Confirming all agent dependencies (rag_chain, jira_tools, rag_config) | OK |

**Summary:** Tests passed: 5 of 5 · Tests failed: 0 of 5
LangGraph is installed and all agent dependencies are ready.

---

## 12. RAG Chain Comprehensive Test

**File:** `tests/test_rag_chain.py`
**Command:** `python tests/test_rag_chain.py`

| Test | Scope | Query | Expected | Got | Result |
|---|---|---|---|---|---|
| TEST 1 | IN-SCOPE IT | How do I set up VPN on my Windows laptop? | ANSWER_FOUND | ANSWER_FOUND | PASS |
| TEST 2 | IN-SCOPE HR | How many sick leave days do I get per year? | ANSWER_FOUND | ANSWER_FOUND | PASS |
| TEST 3 | OUT-OF-SCOPE | My monitor keeps flickering all day | ANSWER_NOT_FOUND | ANSWER_NOT_FOUND | PASS |

**Sources cited:**
- TEST 1: `knowledge_base/it_qa.json`, `knowledge_base/it_support_guide.md`
- TEST 2: `knowledge_base/hr_qa.json`
- TEST 3: `[]` (correctly returned no sources)

**Summary:** Tests passed: 3 of 3 · Tests failed: 0 of 3
RAG chain is working correctly.

---

## 13. Retrieval Pipeline Test

**File:** `tests/test_retrieval.py`
**Command:** `python tests/test_retrieval.py`

ChromaDB connected successfully. Total chunks in database: **175**

| Test | Query | Top Score | Source | Result |
|---|---|---|---|---|
| TEST 1 | How do I reset my password? | 31.9% | knowledge_base/it_qa.json | PASS |
| TEST 2 | How do I set up VPN on Windows? | 35.4% | knowledge_base/it_qa.json | PASS |
| TEST 3 | How many casual leave days do I get? | 60.4% | knowledge_base/hr_qa.json | PASS |
| TEST 4 | What is the work from home policy? | 28.8% | knowledge_base/hr_leave_policy.md | PASS |
| TEST 5 | How do I set up MFA on my phone? | 56.0% | knowledge_base/it_support_guide.md | PASS |

**Retrieval scoring guide:**
- Good score: 40% or higher similarity
- Good source: Points to the right KB file
- Good preview: Shows relevant content for the query

> Note: A `LangChainDeprecationWarning` was present for the `Chroma` import — already resolved by using `langchain-chroma` package in production code.

---

## 14. Security Scan

**File:** `tests/test_security.py`
**Command:** `python tests/test_security.py`

Files scanned: **82** (Python: 37, Markdown: 45)

| Check | Description | Result |
|---|---|---|
| 1 | OpenAI API Key (`sk-p****`) not found in any file | PASS |
| 2 | Jira API Token (`ATAT****`) not found in any file | PASS |
| 3 | Jira Email (`oe70****`) not found in any file | PASS |
| 4 | `.env` is in `.gitignore` | PASS |
| 5 | `.env` file is not tracked by git | PASS |
| 6 | `chroma_db` is in `.gitignore` | PASS |
| 7 | `venv` is in `.gitignore` | PASS |
| 8 | Python files use `os.getenv` for secrets | PASS |

**Summary:** Checks passed: 8 · Checks failed: 0 · Warnings: 0
All security checks passed. No secrets found. Project is safe to submit.

---

## 15. Confidence Threshold Test

**File:** `tests/test_threshold.py`
**Command:** `python tests/test_threshold.py`

**Threshold set at: 15.0%**

| Test | Scope | Query | Expected | Got | Top Score | Result |
|---|---|---|---|---|---|---|
| Test 1 | IN-SCOPE | How do I reset my password? | FOUND | FOUND | 31.9% | PASS |
| Test 2 | IN-SCOPE | How many sick leave days do I get? | FOUND | FOUND | 41.5% | PASS |
| Test 3 | IN-SCOPE | How do I set up MFA on my phone? | FOUND | FOUND | 56.0% | PASS |
| Test 4 | OUT-OF-SCOPE | My monitor keeps flickering | NOT_FOUND | NOT_FOUND | -38.8% | PASS |
| Test 5 | OUT-OF-SCOPE | How do I get an office parking permit? | NOT_FOUND | NOT_FOUND | -33.1% | PASS |
| Test 6 | OUT-OF-SCOPE | The office printer is jammed | NOT_FOUND | NOT_FOUND | -17.3% | PASS |

**Summary:** Tests passed: 6 of 6 · Tests failed: 0 of 6
All tests passed. Confidence threshold is working correctly.

---

## 16. Manual Ticket Status Lookup Test

**File:** `tests/test_ticket_status.py`
**Command:** `python tests/test_ticket_status.py`

| Test | Description | Result |
|---|---|---|
| TEST 1 | Employee with MULTIPLE tickets (jane.doe — 5 tickets found) | PASS |
| TEST 2 | Employee with a SINGLE ticket (john.smith — 2 tickets found) | PASS |
| TEST 3 | Employee with NO tickets (new.employee — 0 found) | PASS |
| TEST 4 | Look up specific ticket SSDAI-47 by ID | PASS |
| TEST 5 | Simulate a full Flow C agent conversation | PASS |

**TEST 4 detail:**
- Status: TICKETS_FOUND
- Ticket ID: SSDAI-47
- Summary: My monitor keeps flickering
- Ticket Status: To Do
- Created: 2026-06-17

**Summary:** Tests passed: 5 of 5 · Tests failed: 0 of 5
All tests passed.

---

## 17. Evaluator Poise Rubric Check

**File:** `docs/test_upoise_checks.py`
**Command:** `python docs/test_upoise_checks.py`

### Category Scores

| Category | Description | Score |
|---|---|---|
| A | Knowledge Base & RAG Pipeline | 25 / 25 (100%) |
| B | Ticket Creation (Write Operation) | 20 / 20 (100%) |
| C | Ticket Status Check (Read Operation) | 15 / 15 (100%) |
| D | Agent Orchestration & Routing | 15 / 15 (100%) |
| E | Code Quality & Documentation | 15 / 15 (100%) |
| F | Error Handling & Robustness | 10 / 10 (100%) |
| **TOTAL** | | **100 / 100** |

### Detailed Results

**Category A — Knowledge Base & RAG Pipeline (25/25)**

| Check | Points | Result |
|---|---|---|
| IT support guide exists and is substantial | 1 | PASS |
| HR leave policy exists and is substantial | 1 | PASS |
| External HR dataset included | 1 | PASS |
| Deliberate gaps documented | 1 | PASS |
| 30+ Q&A pairs total (found 41) | 1 | PASS |
| CHUNK_SIZE defined in rag_config.py | 1 | PASS |
| CHUNK_OVERLAP defined in rag_config.py | 1 | PASS |
| Embedding model configured | 1 | PASS |
| Chunking strategy documented | 1 | PASS |
| rag_config.py exists and centralises settings | 1 | PASS |
| retrieval_with_threshold.py exists | 2 | PASS |
| ChromaDB vector store exists locally | 2 | PASS |
| test_retrieval.py exists | 1 | PASS |
| SYSTEM_PROMPT in rag_chain.py | 2 | PASS |
| Context injection in prompt | 1 | PASS |
| Hallucination guard phrase present | 2 | PASS |
| Confidence threshold check implemented | 2 | PASS |
| RESULT_FOUND and RESULT_NOT_FOUND defined | 2 | PASS |
| test_threshold.py exists | 1 | PASS |

**Category B — Ticket Creation Write Operation (20/20)**

| Check | Points | Result |
|---|---|---|
| jira library imported | 2 | PASS |
| create_ticket function defined | 2 | PASS |
| Jira client connection established | 1 | PASS |
| Summary field | 1 | PASS |
| Description field | 1 | PASS |
| Employee email | 1 | PASS |
| Category field | 1 | PASS |
| Issue type | 1 | PASS |
| awaiting_confirmation in session | 2 | PASS |
| Ticket summary shown before confirm | 1 | PASS |
| YES path creates ticket | 1 | PASS |
| NO path cancels politely | 1 | PASS |
| Ticket ID returned | 2 | PASS |
| Ticket URL returned | 2 | PASS |
| TICKET_CREATED status returned | 1 | PASS |

**Category C — Ticket Status Check Read Operation (15/15)**

| Check | Points | Result |
|---|---|---|
| get_ticket_status function defined | 2 | PASS |
| get_ticket_by_id function defined | 1 | PASS |
| JQL search by email | 1 | PASS |
| Status field retrieved | 1 | PASS |
| format_tickets helper function | 2 | PASS |
| Multiple tickets returned as list | 1 | PASS |
| Ticket count returned | 1 | PASS |
| maxResults limits query | 1 | PASS |
| TICKETS_NONE status returned | 2 | PASS |
| Empty results handled gracefully | 2 | PASS |
| test_flow_c.py exists | 1 | PASS |

**Category D — Agent Orchestration & Routing (15/15)**

| Check | Points | Result |
|---|---|---|
| detect_intent function defined | 2 | PASS |
| KB_QUERY and CHECK_STATUS intents defined | 1 | PASS |
| Intent system prompt defined | 1 | PASS |
| Routing to correct handler functions | 1 | PASS |
| create_session or session management | 1 | PASS |
| Employee email stored in session | 1 | PASS |
| Chat history maintained | 1 | PASS |
| awaiting_email state tracking | 1 | PASS |
| Workflow files separate flows A B C | 1 | PASS |
| UNCLEAR intent handled | 1 | PASS |
| Unclear response function | 1 | PASS |
| Out of scope escalates to ticket | 2 | PASS |
| validate_message or input validation | 1 | PASS |

**Category E — Code Quality & Documentation (15/15)**

| Check | Points | Result |
|---|---|---|
| All 6 core modules exist in src/ | 2 | PASS |
| Functions have docstrings (40 found) | 1 | PASS |
| 15+ test files in tests/ folder (17 found) | 2 | PASS |
| README has setup/install instructions | 1 | PASS |
| README documents environment variables | 1 | PASS |
| README shows how to run agent | 1 | PASS |
| README mentions prerequisites | 1 | PASS |
| Demo video link in README | 1 | PASS |
| architecture_diagram exists | 2 | PASS |
| agent_flowchart.png exists | 1 | PASS |
| architecture.md documentation | 1 | PASS |
| Docker/deployment config present | 1 | PASS |

**Category F — Error Handling & Robustness (10/10)**

| Check | Points | Result |
|---|---|---|
| Multiple try/except blocks (13 found) | 1 | PASS |
| API error response function or message | 1 | PASS |
| JIRAError handled in jira_tools.py | 1 | PASS |
| OpenAI call wrapped in try/except | 1 | PASS |
| ANSWER_NOT_FOUND fallback on LLM failure | 1 | PASS |
| User-friendly fallback message | 1 | PASS |
| No API keys hardcoded in src/ files | 1 | PASS |
| test_security.py exists | 1 | PASS |
| Input validation in agent or workflow | 1 | PASS |
| test_edge_cases.py exists | 1 | PASS |

**Final result:** Checks passed: 80 · Checks failed: 0
**TOTAL ESTIMATED SCORE: 100 / 100 — EXCELLENT, Strong submission.**
