# SmartDesk AI

An intelligent IT and HR operations agent for Roadmap Consulting.
SmartDesk AI answers employee support questions, creates Jira support
tickets for issues it cannot resolve, and retrieves ticket status —
all through a conversational terminal interface.

---

## Quick Start — Running the Agent

```bash
# 1. Activate your virtual environment
venv\Scripts\Activate.ps1

# 2. Start the agent
python src/agents/agent.py
```

The agent starts and waits for your input. Type your question
and press Enter.

```
============================================================
  SmartDesk AI — Intelligent IT & HR Operations Agent
  Roadmap Consulting Internal Support
============================================================

SmartDesk : Hello! I am SmartDesk AI, your IT and HR support
            assistant at Roadmap Consulting.
            How can I help you today?

You        :
```

**Session commands:**

| Command | What It Does |
|---|---|
| Type any question | Sends your message to the agent |
| `new` or `restart` | Clears the session and starts fresh |
| `quit` or `exit` | Ends the session |
| `Ctrl + C` | Force quits |

---

## Table of Contents

1. [What It Does](#what-it-does)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Example Conversations](#example-conversations)
7. [Running the Tests](#running-the-tests)
8. [Architecture](#architecture)
9. [Technology Stack](#technology-stack)
10. [Known Limitations](#known-limitations)

---

## What It Does

SmartDesk AI handles three conversation flows:

**Flow A — Knowledge Base Answer**
Searches the indexed knowledge base and returns a grounded answer
using GPT. Will not make up information that is not in the documents.

**Flow B — Ticket Creation**
When the agent cannot find an answer it offers to create a Jira
support ticket. The employee reviews a summary and must confirm
before any ticket is created.

**Flow C — Ticket Status Check**
Retrieves all open Jira tickets for a given employee email address
and displays their current status and latest comments.

---

## Project Structure

```
SmartDesk_AI/
│
├── src/                            # All application source code
│   ├── agents/
│   │   └── agent.py                # Main agent orchestrator
│   ├── core/
│   │   └── jira_tools.py           # Jira API integration
│   ├── data/
│   │   ├── index_knowledge_base.py # Indexes KB into ChromaDB
│   │   └── knowledge_base/
│   │       ├── it_support_guide.md
│   │       ├── hr_leave_policy.md
│   │       ├── it_qa.json
│   │       ├── hr_qa.json
│   │       ├── hr-policies-qa-dataset.jsonl
│   │       └── out_of_scope_topics.txt
│   ├── rag/
│   │   ├── rag_chain.py            # RAG answer generation
│   │   ├── rag_config.py           # Centralised RAG settings
│   │   └── retrieval_with_threshold.py
│   ├── utils/
│   │   ├── helpers.py
│   │   └── company_profile.txt
│   ├── web_app/
│   │   └── app.py                  # Web interface (optional)
│   └── workflow/
│       ├── flow_a.py               # Knowledge base flow
│       ├── flow_b.py               # Ticket creation flow
│       └── flow_c.py               # Ticket status flow
│
├── tests/                          # All test files (15 total)
│   ├── test_flow_a.py
│   ├── test_flow_b.py
│   ├── test_flow_c.py
│   ├── test_confirmation.py
│   ├── test_create_ticket.py
│   ├── test_edge_cases.py
│   ├── test_error_handling.py
│   ├── test_get_status.py
│   ├── test_graceful_handling.py
│   ├── test_jira_connection.py
│   ├── test_langgraph.py
│   ├── test_rag_chain.py
│   ├── test_retrieval.py
│   ├── test_security.py
│   ├── test_threshold.py
│   └── test_ticket_status.py
│
├── chroma_db/                      # Vector database (auto-generated)
├── .env                            # Secret keys — never committed
├── .env.example                    # Environment variable template
├── .gitignore
├── config.yaml                     # Application configuration
├── conftest.py                     # pytest configuration
├── confidence_check.py             # Evaluator rubric check
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python 3.11
- Git
- An OpenAI account with API access
- A Jira Cloud account (free tier is sufficient)
- A Jira API token from your Atlassian account settings

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/oscar2412/SmartDesk_AI.git
cd SmartDesk_AI
```

**2. Create and activate a virtual environment**

```bash
# Windows
py -3.11 -m venv venv
venv\Scripts\Activate.ps1

# Mac / Linux
python3.11 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up your environment variables**

```bash
copy .env.example .env
```

Open `.env` and replace all placeholder values.
See the [Configuration](#configuration) section below.

**5. Index the knowledge base**

Run this once before starting the agent for the first time.
It reads all documents, chunks them, creates embeddings, and
stores everything in ChromaDB.

```bash
python src/data/index_knowledge_base.py
```

A `chroma_db/` folder appears when indexing is complete.
Re-run this command any time you add or change documents
in the `knowledge_base/` folder.

**6. Start the agent**

```bash
python src/agents/agent.py
```

---

## Configuration

Create a `.env` file in the project root using `.env.example`
as a template. Never commit `.env` to version control.

| Variable | Description | Example |
|---|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` |
| `JIRA_EMAIL` | Email for your Jira account | `you@email.com` |
| `JIRA_API_TOKEN` | Token from Atlassian account settings | `ATATT3x...` |
| `JIRA_SERVER` | Your Atlassian domain | `https://name.atlassian.net` |
| `JIRA_PROJECT_KEY` | Short key for your Jira project | `SSDAI` |

To create a Jira API token visit:
`https://id.atlassian.com/manage-profile/security/api-tokens`

RAG pipeline settings including chunk size, chunk overlap,
confidence threshold, embedding model, and LLM model are
all controlled in `src/rag/rag_config.py`.

---

## Example Conversations

**Flow A — Knowledge base answer**

```
You        : How do I reset my password?

SmartDesk  : To reset your password at Roadmap Consulting
             follow these steps:
             1. Go to https://passwords.roadmapconsulting.com
             2. Click Forgot Password
             3. Enter your employee ID
             4. Follow the instructions in the email sent to you
             If you are still locked out contact IT at ext. 2020.

             Is there anything else I can help you with?
```

**Flow B — Ticket creation**

```
You        : My monitor keeps flickering

SmartDesk  : I could not find information about that in my
             knowledge base. I can create a support ticket
             for the IT team.

             What is your work email address?

You        : jane@roadmapconsulting.com

SmartDesk  : Please review the ticket I will create:
             ----------------------------------------
               Title    : My monitor keeps flickering
               Category : IT Support
               Email    : jane@roadmapconsulting.com
             ----------------------------------------
             Shall I go ahead? Type YES to confirm or NO to cancel.

You        : yes

SmartDesk  : Your support ticket has been created successfully.
               Ticket ID : SSDAI-12
               URL       : https://oe7051.atlassian.net/browse/SSDAI-12
             The support team will get back to you shortly.
```

**Flow C — Ticket status check**

```
You        : What is the status of my tickets?

SmartDesk  : Could you share your work email address?

You        : jane@roadmapconsulting.com

SmartDesk  : I found 2 ticket(s) for jane@roadmapconsulting.com:

             SSDAI-12 : My monitor keeps flickering
               Status  : In Progress
               Update  : Replacement monitor ordered.

             SSDAI-8  : Printer jam on floor 3
               Status  : Done

             Is there anything else I can help you with?
```

---

## Running the Tests

All test files are in the `tests/` folder.

**Run all tests:**

```bash
pytest tests/ -v
```

**Run a specific test file:**

```bash
pytest tests/test_flow_a.py -v
pytest tests/test_flow_b.py -v
pytest tests/test_flow_c.py -v
```

**Run an individual test script directly:**

```bash
python tests/test_security.py
python tests/test_edge_cases.py
python tests/test_error_handling.py
```

**Run the evaluator confidence check:**

```bash
python confidence_check.py
```

**Test file reference:**

| File | What It Tests |
|---|---|
| `test_flow_a.py` | Flow A — knowledge base answers |
| `test_flow_b.py` | Flow B — ticket creation end to end |
| `test_flow_c.py` | Flow C — ticket status retrieval |
| `test_confirmation.py` | Human-in-the-loop confirmation |
| `test_create_ticket.py` | Jira ticket creation |
| `test_edge_cases.py` | 21 edge case scenarios |
| `test_error_handling.py` | API failure degradation |
| `test_get_status.py` | Ticket status lookup |
| `test_graceful_handling.py` | Unexpected input handling |
| `test_jira_connection.py` | Live Jira connection |
| `test_langgraph.py` | LangGraph installation |
| `test_rag_chain.py` | RAG answer generation |
| `test_retrieval.py` | ChromaDB retrieval pipeline |
| `test_security.py` | No hardcoded secrets scan |
| `test_threshold.py` | Confidence threshold logic |
| `test_ticket_status.py` | Full status lookup scenarios |

---

## Architecture

```
Employee Input (Terminal)
         |
         v
    src/agents/agent.py
    Intent Detection
         |
         |-- KB_QUERY ---------> src/rag/rag_chain.py
         |                              |
         |                 src/rag/retrieval_with_threshold.py
         |                              |
         |                        chroma_db/ (local)
         |                              |
         |                        OpenAI API (embeddings + LLM)
         |                              |
         |                       Answer returned to employee
         |
         |-- NOT_FOUND ---------> src/workflow/flow_b.py
         |                              |
         |                    src/core/jira_tools.py
         |                              |
         |                       Jira Cloud API
         |                              |
         |                       Ticket created — ID returned
         |
         |-- CHECK_STATUS ------> src/workflow/flow_c.py
                                        |
                               src/core/jira_tools.py
                                        |
                                  Jira Cloud API
                                        |
                                  Tickets retrieved and displayed
```

All secrets load from `.env` at runtime.
ChromaDB runs locally on disk.
OpenAI and Jira are the only external service dependencies.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Store | ChromaDB |
| RAG Framework | LangChain |
| Ticketing | Jira Cloud REST API |
| Secret Management | python-dotenv |
| Testing | pytest |
| Containerisation | Docker |

---

## Known Limitations

- The agent runs as a command-line interface. The `web_app/` module
  contains an experimental web interface that is not production ready.
- Session memory does not persist between runs. Each new session
  starts fresh with no memory of previous conversations.
- The Jira integration requires an active internet connection.
  If the API is unreachable the agent returns a polite error message
  and suggests trying again.
- Re-run `src/data/index_knowledge_base.py` any time documents
  in `knowledge_base/` are added or updated.

---

## Author

Oscar — AI Generalist in Training
Interview Kickstart · Applied Agentic AI Program · Capstone Project
GitHub: https://github.com/oscar2412/SmartDesk_AI