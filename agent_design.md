# SmartDesk AI — Agent Design Document

## Agent Overview

SmartDesk AI is a conversational agent that handles
three conversation flows for Roadmap Consulting employees.

## Intent Categories

| Intent | Triggered By | Handled By |
|---|---|---|
| KB_QUERY | Any IT or HR question | get_rag_answer() |
| CHECK_STATUS | Questions about ticket status | get_ticket_status() |
| CREATE_TICKET | When RAG returns ANSWER_NOT_FOUND | create_ticket() |

## Session State

The agent maintains these values during a conversation:

| Key | Type | Purpose |
|---|---|---|
| employee_email | string | Stored once asked |
| pending_ticket | dict | Holds ticket details before confirmation |
| conversation_history | list | Stores chat messages for GPT context |
| last_intent | string | Remembers the previous intent |

## Flow A — Knowledge Base Query

1. Employee asks an IT or HR question
2. Agent calls get_rag_answer()
3. If ANSWER_FOUND return the answer
4. If ANSWER_NOT_FOUND escalate to Flow B

## Flow B — Ticket Creation

1. Agent tells employee it cannot find the answer
2. Agent asks for employee email if not already known
3. Agent builds ticket summary and shows it
4. Agent asks for yes/no confirmation
5. If yes call create_ticket() and return ticket ID
6. If no cancel politely

## Flow C — Ticket Status Check

1. Employee asks about ticket status
2. Agent asks for email if not already known
3. Agent calls get_ticket_status()
4. Agent formats and displays ticket list

## Error Handling

- OpenAI API failure → polite retry message
- Jira API failure → polite retry message
- Unclear input → ask for clarification
- Empty input → ask employee to rephrase

## Files Used by Agent

| File | What Agent Imports From It |
|---|---|
| rag_chain.py | get_rag_answer() |
| jira_tools.py | create_ticket() get_ticket_status() format_tickets() |
| rag_config.py | LLM_MODEL |