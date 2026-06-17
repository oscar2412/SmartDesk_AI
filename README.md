# SmartDesk AI

An intelligent IT and HR operations agent for Roadmap Consulting.
SmartDesk AI answers employee support questions, creates Jira support
tickets for issues it cannot resolve, and retrieves ticket status —
all through a conversational terminal interface.

---

## Quick Start

```bash
# 1. Activate your virtual environment
venv\Scripts\Activate.ps1          # Windows
source venv/bin/activate           # Mac / Linux

# 2. Start the agent
python -m src.agents.agent
```

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

### Session commands

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
Searches the indexed ChromaDB vector store and returns a grounded answer
using GPT-4o-mini. The agent will not fabricate information — if the
confidence score falls below the threshold it escalates to Flow B.

**Flow B — Ticket Creation**
When the agent cannot find an answer it offers to raise a Jira support
ticket. The employee reviews a summary and must type `YES` before any
ticket is created (human-in-the-loop confirmation).

**Flow C — Ticket Status Check**
Retrieves all open Jira tickets linked to a given employee email address
and displays their current status and latest comments.

---

## Project Structure

```
SmartDesk_AI/
│
├── src/                            # All application source code
│   ├── agents/
│   │   └── agent.py                # Main orchestrator — intent detection,
│   │                               # session management, message routing
│   ├── core/
│   │   └── jira_tools.py           # Jira Cloud REST API integration
│   ├── data/
│   │   ├── index_knowledge_base.py # Indexes KB documents into ChromaDB
│   │   └── knowledge_base/
│   │       ├── it_support_guide.md
│   │       ├── hr_leave_policy.md
│   │       ├── it_qa.json
│   │       ├── hr_qa.json
│   │       ├── hr-policies-qa-dataset.jsonl
│   │       └── out_of_scope_topics.txt
│   ├── rag/
│   │   ├── rag_chain.py            # RAG answer generation via LangChain
│   │   ├── rag_config.py           # Centralised RAG settings
│   │   └── retrieval_with_threshold.py  # ChromaDB retrieval + confidence filter
│   ├── utils/
│   │   ├── helpers.py              # Validation, greeting builders, formatters
│   │   └── company_profile.txt
│   ├── web_app/
│   │   └── app.py                  # Experimental Streamlit web interface
│   └── workflow/
│       ├── flow_a.py               # Knowledge base query flow
│       ├── flow_b.py               # Ticket creation flow
│       └── flow_c.py               # Ticket status check flow
│
├── tests/                          # 17 test files
│   ├── test_confirmation.py
│   ├── test_create_ticket.py
│   ├── test_edge_cases.py
│   ├── test_error_handling.py
│   ├── test_flow_a.py
│   ├── test_flow_b.py
│   ├── test_flow_c.py
│   ├── test_get_status.py
│   ├── test_graceful_handling.py
│   ├── test_jira_connection.py
│   ├── test_langgraph.py
│   ├── test_rag_chain.py
│   ├── test_retrieval.py
│   ├── test_security.py
│   ├── test_threshold.py
│   ├── test_ticket_status.py
│   └── test_upoise_checks.py       # Evaluator confidence rubric check
│
├── docs/                           # Project documentation and diagrams
│   ├── agent_design.md
│   ├── agent_flowchart.md
│   ├── agent_flowchart.png
│   ├── agent_flowchart.jpg
│   ├── architecture.md
│   └── architecture_diagram.drawio.png
│
├── chroma_db/                      # Vector database (auto-generated, git-ignored)
├── .env                            # Secret keys — never commit this file
├── .env.example                    # Environment variable template
├── .gitignore
├── .dockerignore
├── config.yaml                     # RAG pipeline configuration
├── conftest.py                     # pytest shared fixtures                
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Prerequisites

- Python 3.11
- Git
- An OpenAI account with API access
- A Jira Cloud account (free tier is sufficient)
- A Jira API token from Atlassian account settings

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

**4. Set up environment variables**

```bash
copy .env.example .env        # Windows
cp .env.example .env          # Mac / Linux
```

Open `.env` and fill in all placeholder values. See [Configuration](#configuration) below.

**5. Index the knowledge base**

Run this once before starting the agent for the first time. It reads all
documents, chunks them, generates embeddings, and stores everything in ChromaDB.

```bash
python src/data/index_knowledge_base.py
```

A `chroma_db/` folder is created when indexing completes. Re-run this command
any time you add or update documents in `knowledge_base/`.

**6. Start the agent**

```bash
python -m src.agents.agent
```

---

## Configuration

### Environment variables

Create a `.env` file from `.env.example`. Never commit `.env` to version control.

| Variable | Description | Example |
|---|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` |
| `JIRA_EMAIL` | Email for your Jira account | `you@email.com` |
| `JIRA_API_TOKEN` | Token from Atlassian account settings | `ATATT3x...` |
| `JIRA_SERVER` | Your Atlassian domain | `https://name.atlassian.net` |
| `JIRA_PROJECT_KEY` | Short key for your Jira project | `SSDAI` |

To create a Jira API token, visit:
`https://id.atlassian.com/manage-profile/security/api-tokens`

### RAG Pipeline Settings (`config.yaml`)

| Setting | Default | Description |
|---|---|---|
| `chunk_size` | `800` | Characters per document chunk |
| `chunk_overlap` | `150` | Overlap between adjacent chunks |
| `top_k_results` | `3` | Number of chunks retrieved per query |
| `confidence_threshold` | `0.15` | Minimum score to return an answer |
| `embedding_model` | `text-embedding-3-small` | OpenAI embedding model |
| `llm_model` | `gpt-4o-mini` | OpenAI chat model |

---

## Example Conversations

**Flow A — Knowledge base answer**

```
You        : How do I reset my password?

SmartDesk  : To reset your password at Roadmap Consulting, follow these steps:
             1. Go to https://passwords.roadmapconsulting.com
             2. Click Forgot Password
             3. Enter your employee ID
             4. Follow the instructions in the email sent to you
             If you are still locked out, contact IT at ext. 2020.

             Is there anything else I can help you with?
```

**Flow B — Ticket creation**

```
You        : My monitor keeps flickering

SmartDesk  : I could not find information about that in my knowledge base.
             I can create a support ticket for the IT team.

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

**Run all tests:**

```bash
pytest tests/ -v
```

**Run a specific flow's tests:**

```bash
pytest tests/test_flow_a.py -v
pytest tests/test_flow_b.py -v
pytest tests/test_flow_c.py -v
```

**Run the evaluator confidence check:**

```bash
python poise_check.py
```

**Test file reference:**

| File | What It Tests |
|---|---|
| `test_flow_a.py` | Flow A — knowledge base answers |
| `test_flow_b.py` | Flow B — ticket creation end to end |
| `test_flow_c.py` | Flow C — ticket status retrieval |
| `test_confirmation.py` | Human-in-the-loop YES/NO confirmation |
| `test_create_ticket.py` | Jira ticket creation |
| `test_edge_cases.py` | 21 edge case scenarios |
| `test_error_handling.py` | API failure and graceful degradation |
| `test_get_status.py` | Ticket status lookup |
| `test_graceful_handling.py` | Unexpected and malformed input |
| `test_jira_connection.py` | Live Jira connection |
| `test_langgraph.py` | LangGraph installation check |
| `test_rag_chain.py` | RAG answer generation |
| `test_retrieval.py` | ChromaDB retrieval pipeline |
| `test_security.py` | No hardcoded secrets scan |
| `test_threshold.py` | Confidence threshold filtering |
| `test_ticket_status.py` | Full status lookup scenarios |
| `test_poise_checks.py`  | # Evaluator confidence rubric check | Only to run on-demand |
---

## Architecture

```
Employee Input (Terminal / Web)
         │
         ▼
   src/agents/agent.py
   Intent Detection (GPT-4o-mini)
         │
         ├── KB_QUERY ──────────► src/workflow/flow_a.py
         │                               │
         │                        src/rag/rag_chain.py
         │                               │
         │                 src/rag/retrieval_with_threshold.py
         │                               │
         │                         chroma_db/  (local disk)
         │                               │
         │                        OpenAI API  (embeddings + LLM)
         │                               │
         │               Answer returned ◄── or NOT_FOUND ──┐
         │                                                   │
         ├── NOT_FOUND / TICKET ────────────────────────────►│
         │                        src/workflow/flow_b.py     │
         │                               │                   │
         │                        src/core/jira_tools.py     │
         │                               │                   │
         │                        Jira Cloud API             │
         │                               │                   │
         │                   Ticket created — ID returned    │
         │                                                   │
         └── CHECK_STATUS ─────────────────────────────────►│
                                  src/workflow/flow_c.py
                                         │
                                  src/core/jira_tools.py
                                         │
                                   Jira Cloud API
                                         │
                             Open tickets retrieved and displayed
```

All secrets load from `.env` at runtime.
ChromaDB runs entirely on local disk — no external vector database required.
OpenAI and Jira Cloud are the only external service dependencies.

---

## Running with Docker

```bash
# Build and run
docker-compose up --build

# Stop
docker-compose down
```

The container mounts `./chroma_db` so the vector database persists between runs.
Ensure your `.env` file is present in the project root before starting.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Store | ChromaDB |
| RAG Framework | LangChain + LangGraph |
| Ticketing | Jira Cloud REST API |
| Web Interface | Streamlit (experimental) |
| Secret Management | python-dotenv |
| Testing | pytest |
| Containerisation | Docker |

---

## Known Limitations

- **CLI first.** The primary interface is the terminal. The `web_app/` Streamlit
  module is experimental and not production-ready.
- **No session persistence.** Each new session starts fresh with no memory of
  previous conversations.
- **Internet required for Jira.** If the Jira API is unreachable the agent
  returns a polite error and suggests trying again later.
- **Re-index after KB changes.** Run `python src/data/index_knowledge_base.py`
  any time documents in `knowledge_base/` are added or updated.
- **Scope limited to knowledge base content.** Answers are grounded strictly in
  indexed documents. Questions outside that scope are escalated to a ticket.

---

## Author

Oscar — AI Generalist in Training
First AI Capstone Project
Interview Kickstart · Applied Agentic AI Program
GitHub: https://github.com/oscar2412/SmartDesk_AI

---

> **Disclaimer:** This project is for educational and entertainmane purposes 
> and demonstrates a self-service support assistant on a small, controlled 
> knowledge base. For actual IT or HR resolutions, contact your company's 
> support team directly.