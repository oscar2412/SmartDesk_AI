# SmartDesk AI

<div align="center">

```
███████╗███╗   ███╗ █████╗ ██████╗ ████████╗██████╗ ███████╗███████╗██╗  ██╗
██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔════╝██╔════╝██║ ██╔╝
███████╗██╔████╔██║███████║██████╔╝   ██║   ██║  ██║█████╗  ███████╗█████╔╝
╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   ██║  ██║██╔══╝  ╚════██║██╔═██╗
███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   ██████╔╝███████╗███████║██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
```

## 🤖 SmartDesk AI

### An Intelligent IT & HR Operations Agent

---

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35?style=for-the-badge)](https://chromadb.com)
[![Jira](https://img.shields.io/badge/Jira-Integrated-0052CC?style=for-the-badge&logo=jira&logoColor=white)](https://atlassian.com/jira)
[![LangChain](https://img.shields.io/badge/LangChain-RAG_Pipeline-1C3C3C?style=for-the-badge)](https://langchain.com)
[![Docker](https://img.shields.io/badge/Docker-Containerised-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

---

> *"Stop searching through wikis. Just ask SmartDesk."*

**SmartDesk AI** is a production-style conversational agent that acts as a first-line IT and HR help desk for any organisation. It answers employee questions from a curated knowledge base, creates Jira support tickets when it cannot help, and lets employees check their ticket status — all through a single chat interface, deployable locally or via Docker.

---

</div>

## 📋 Table of Contents

- [What SmartDesk AI Does](#-what-smartdesk-ai-does)
- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Environment Variables](#-environment-variables)
- [Setup — Local (Python)](#-setup--local-python)
- [Setup — Docker](#-setup--docker)
- [Building the Knowledge Base](#-building-the-knowledge-base)
- [Running the Agent](#-running-the-agent)
- [Example Conversation Flows](#-example-conversation-flows)
- [Test Suite](#-test-suite)
- [Self Assessment](#-self-assessment-against-rubric)
- [Technology Stack](#-technology-stack)
- [Known Limitations](#-known-limitations)
- [Author](#-author)

---

## 🎯 What SmartDesk AI Does

Most IT and HR support teams are buried in repetitive questions — password resets, leave policies, VPN setup, reimbursement processes. The answers already exist in internal documents. Employees just cannot find them fast enough.

**SmartDesk AI sits between the employee and the support team and handles three things:**

| Capability | What It Means | How It Works |
|---|---|---|
| 🔍 **Answer from Knowledge Base** | Instantly answers IT and HR questions | RAG pipeline searches ChromaDB, GPT generates a grounded answer |
| 🎫 **Create a Support Ticket** | Opens a Jira ticket when it cannot answer | Collects employee info, confirms before submitting, returns ticket ID |
| 📊 **Check Ticket Status** | Reports back on open tickets | Queries Jira API by employee email, displays status and team comments |

---

## 🏗 Architecture Overview

![SmartDesk AI System Architecture](architecture_diagram.drawio.png)

```
┌─────────────────────────────────────────────────────────────────┐
│                        EMPLOYEE INPUT                           │
│                   "How do I reset my VPN?"                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTENT DETECTOR                              │
│           Classifies input as one of three flows                │
│        KB_QUERY  │  CREATE_TICKET  │  CHECK_STATUS              │
└──────┬───────────────────┬──────────────────────┬───────────────┘
       │                   │                      │
       ▼                   ▼                      ▼
┌──────────────┐  ┌─────────────────┐  ┌──────────────────┐
│  Flow A      │  │  Flow B         │  │  Flow C           │
│  RAG         │  │  TICKET         │  │  STATUS CHECK     │
│  PIPELINE    │  │  CREATION       │  │                   │
│              │  │                 │  │  Lookup by        │
│  ChromaDB    │  │  Collect Info   │  │  Employee Email   │
│  Search      │  │      ↓          │  │       ↓           │
│      ↓       │  │  Show Summary   │  │  Return Status    │
│  GPT Answer  │  │      ↓          │  │  + Comments       │
│              │  │  Confirm Y/N    │  │                   │
│              │  │      ↓          │  │                   │
│              │  │  Create Ticket  │  │                   │
└──────────────┘  └─────────────────┘  └──────────────────┘
       │                   │                      │
       └───────────────────┴──────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EMPLOYEE RESPONSE                          │
│           Polite · Professional · Grounded · Accurate           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
SmartDesk_AI/
│
├── 📂 src/                             ← All application source code
│   ├── 📄 __init__.py
│   │
│   ├── 📂 agents/                      ← Orchestration layer
│   │   ├── 📄 __init__.py
│   │   └── 📄 agent.py                 ← Main agent: intent detection, session management, routing
│   │
│   ├── 📂 core/                        ← External integrations
│   │   ├── 📄 __init__.py
│   │   └── 📄 jira_tools.py            ← Jira API: create tickets, lookup status, format output
│   │
│   ├── 📂 data/                        ← Knowledge base and indexing
│   │   ├── 📄 __init__.py
│   │   ├── 📄 index_knowledge_base.py  ← Reads KB files, chunks, embeds, stores in ChromaDB
│   │   └── 📂 knowledge_base/
│   │       ├── 📄 it_support_guide.md           ← VPN, password reset, MFA, email setup
│   │       ├── 📄 hr_leave_policy.md            ← Leave types, WFH policy, approval process
│   │       ├── 📄 it_qa.json                    ← 20 IT question-answer pairs
│   │       ├── 📄 hr_qa.json                    ← 20 HR question-answer pairs
│   │       ├── 📄 hr-policies-qa-dataset.jsonl  ← Extended HR dataset for broader coverage
│   │       ├── 📄 out_of_scope_topics.txt        ← Deliberate gaps to test ticket escalation
│   │       └── 📄 .gitkeep                      ← Ensures directory is tracked by Git
│   │
│   ├── 📂 rag/                         ← Retrieval-Augmented Generation pipeline
│   │   ├── 📄 __init__.py
│   │   ├── 📄 rag_chain.py             ← RAG answer generation using retrieved context
│   │   ├── 📄 rag_config.py            ← Loads RAG settings from config.yaml
│   │   └── 📄 retrieval_with_threshold.py ← ChromaDB vector search with confidence threshold
│   │
│   ├── 📂 utils/                       ← Shared helper functions
│   │   ├── 📄 __init__.py
│   │   ├── 📄 helpers.py               ← Response builders, validation, greetings, categorisation
│   │   └── 📄 company_profile.txt      ← Roadmap Consulting contact info and portal URLs
│   │
│   ├── 📂 web_app/                     ← Reserved for future web UI (Streamlit or Flask)
│   │   └── 📄 __init__.py
│   │
│   └── 📂 workflow/                    ← Isolated conversation flow handlers
│       ├── 📄 __init__.py
│       ├── 📄 flow_a.py                ← Flow A: answer from knowledge base via RAG
│       ├── 📄 flow_b.py                ← Flow B: ticket creation with human-in-the-loop
│       └── 📄 flow_c.py               ← Flow C: ticket status lookup via Jira
│
├── 📂 tests/                           ← Full test suite (16 files)
│   ├── 📄 test_confirmation.py         ← Human-in-the-loop yes/no confirmation logic
│   ├── 📄 test_create_ticket.py        ← End-to-end Jira ticket creation
│   ├── 📄 test_edge_cases.py           ← 21 boundary and unexpected input scenarios
│   ├── 📄 test_error_handling.py       ← API failure graceful degradation
│   ├── 📄 test_flow_a.py              ← Official Flow A: KB answer verification
│   ├── 📄 test_flow_b.py              ← Official Flow B: escalation and ticket creation
│   ├── 📄 test_flow_c.py              ← Official Flow C: ticket status check
│   ├── 📄 test_get_status.py           ← Jira status retrieval functions
│   ├── 📄 test_graceful_handling.py    ← Graceful handling of greetings, thanks, off-topic
│   ├── 📄 test_jira_connection.py      ← Live Jira API connectivity verification
│   ├── 📄 test_langgraph.py            ← LangGraph installation and dependency check
│   ├── 📄 test_rag_chain.py            ← RAG answer generation quality
│   ├── 📄 test_retrieval.py            ← ChromaDB retrieval pipeline
│   ├── 📄 test_security.py             ← Hardcoded secrets scan across all files
│   ├── 📄 test_threshold.py            ← Confidence threshold in/out-of-scope logic
│   └── 📄 test_ticket_status.py        ← End-to-end ticket status lookup
│
├── 📄 Dockerfile                       ← Container build instructions for Docker deployment
├── 📄 docker-compose.yml               ← Docker service config: env vars, volumes, TTY
├── 📄 .dockerignore                    ← Excludes venv, chroma_db, .env from Docker build
├── 📄 config.yaml                      ← Central RAG configuration: models, thresholds, paths
├── 📄 conftest.py                      ← Adds project root to sys.path for pytest discovery
├── 📄 requirements.txt                 ← All Python dependencies with pinned versions
├── 📄 .env.example                     ← Template showing all required environment variables
├── 📄 .gitignore                       ← Excludes venv, chroma_db, .env from version control
├── 📄 agent_design.md                  ← Design decisions and agent architecture notes
├── 📄 architecture.md                  ← Detailed system architecture documentation
├── 📄 architecture_diagram.drawio.png  ← System architecture diagram
├── 📄 agent_flowchart.png              ← Visual flowchart of all three conversation flows
│
├── 📂 chroma_db/                       ← Vector database — auto-generated, not in GitHub
└── 📂 venv/                            ← Virtual environment — not in GitHub
```

---

## ✅ Prerequisites

| Requirement | Version | Link |
|---|---|---|
| Python | 3.11+ | [python.org/downloads](https://python.org/downloads) |
| Git | Any | [git-scm.com](https://git-scm.com) |
| VS Code | Any | [code.visualstudio.com](https://code.visualstudio.com) |
| Docker Desktop | Any | [docker.com/products/docker-desktop](https://docker.com/products/docker-desktop) |
| OpenAI account + API key | — | [platform.openai.com](https://platform.openai.com) |
| Jira Cloud account + API token | Free tier | [atlassian.com/jira](https://atlassian.com/jira) |

---

## 🔐 Environment Variables

SmartDesk AI loads all secrets from a `.env` file. **Never hard-code credentials in Python files.**

Create `.env` in the project root:

```env
# ── OpenAI ──────────────────────────────────────────
OPENAI_API_KEY=sk-proj-your-openai-key-here

# ── Jira ────────────────────────────────────────────
JIRA_EMAIL=your-jira-email@example.com
JIRA_API_TOKEN=your-jira-api-token-here
JIRA_SERVER=https://yourname.atlassian.net
JIRA_PROJECT_KEY=SSDAI
```

> ⚠️ `.env` is already listed in `.gitignore`. It will never be uploaded to GitHub.

---

## 🐍 Setup — Local (Python)

Follow these steps in order from a fresh clone.

```bash
# 1. Clone the repository
git clone https://github.com/oscar2412/SmartDesk_AI.git
cd SmartDesk_AI

# 2. Create and activate virtual environment
py -3.11 -m venv venv
venv\Scripts\Activate.ps1        # Windows
source venv/bin/activate          # Mac / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file (see Environment Variables section above)

# 5. Index the knowledge base (run once, or after updating KB files)
python -m src.data.index_knowledge_base

# 6. Start the agent
python -m src.agents.agent
```

---

## 🐳 Setup — Docker

Docker packages the entire application — Python runtime, all dependencies, and source code — into a portable container. No local Python installation required on target machines.

### First-Time Setup

```bash
# 1. Make sure Docker Desktop is running (whale icon in taskbar)

# 2. Build the container image (10–15 min first time, cached after)
docker-compose build

# 3. Index the knowledge base inside the container
docker-compose run --rm smartdesk python -m src.data.index_knowledge_base

# 4. Run the agent
docker-compose run --rm smartdesk
```

### Daily Workflow

```bash
# Start the agent
docker-compose run --rm smartdesk

# Re-index after updating knowledge base files
docker-compose run --rm smartdesk python -m src.data.index_knowledge_base

# Rebuild after adding new packages to requirements.txt
docker-compose build

# Stop all containers
docker-compose down
```

> ℹ️ ChromaDB is persisted to your local `./chroma_db` folder via a Docker volume. Your knowledge base survives container restarts.

---

## 📚 Building the Knowledge Base

The knowledge base is the foundation of SmartDesk AI. Document quality directly determines answer quality.

### Minimum Requirements

| Requirement | Target |
|---|---|
| Total question-answer pairs | At least 30–50 |
| IT topics covered | Password reset, VPN, MFA, email setup |
| HR topics covered | Leave policy, WFH, onboarding, reimbursement |
| Deliberate gaps | At least 5 unanswerable topics to test escalation |

### Option A — Download Ready-Made Datasets

- **HR Policies:** [huggingface.co/datasets?search=hr+pol](https://huggingface.co/datasets?sort=trending&search=hr+pol)
- **IT Support:** [huggingface.co/datasets?search=it+tick](https://huggingface.co/datasets?sort=trending&search=it+tick)
- **Recommended starter:** `strova-ai/hr-policies-qa-dataset` on Hugging Face

### Option B — Generate With ChatGPT

**IT Guide prompt:**
```
You are the IT Admin at Roadmap Consulting, a 105-employee company.
Write an internal guide covering: password reset steps, VPN setup
for Windows and Mac, MFA setup, and email setup on mobile.
Write in simple professional language for employees.
```

**HR Policy prompt:**
```
You are the HR Manager at Roadmap Consulting. Write a Leave Policy
covering casual leave, sick leave, earned leave, and work from home
policy. Include how to apply and approval steps. Keep it simple
and professional.
```

### Option C — Combine Both (Recommended ⭐)

Download the Hugging Face HR dataset for breadth, then generate synthetic IT guides for depth. This is the fastest path to a high-quality knowledge base.

### Adjusting RAG Settings

All retrieval settings live in `config.yaml` at the project root:

```yaml
rag:
  chunk_size: 800            # Characters per document chunk
  chunk_overlap: 150         # Overlap between chunks
  top_k_results: 3           # Chunks retrieved per query
  confidence_threshold: 0.15 # Minimum similarity score to attempt an answer
  embedding_model: text-embedding-3-small
  llm_model: gpt-4o-mini
  chroma_db_path: ./chroma_db
  chroma_collection_name: smartdesk_knowledge
```

After changing any value, re-index to rebuild ChromaDB:
```bash
python -m src.data.index_knowledge_base
```

---

## 💬 Example Conversation Flows

### Flow A — Question Answered from Knowledge Base

```
You       : Hi, how do I reset my password?

SmartDesk : To reset your password, visit the Self-Service Password
            Portal at https://passwords.roadmapconsulting.com.
            Click "Forgot Password", enter your employee ID, and
            follow the instructions sent to your registered email.
            If you are locked out, contact IT at ext. 2020.
            Is there anything else I can help you with?

You       : No, thanks!

SmartDesk : You are very welcome! I am glad I could help.
            Is there anything else I can assist you with today?
```

### Flow B — Question Escalated to Ticket Creation

```
You       : My monitor has been flickering for two days.

SmartDesk : I am sorry I could not find information about that in
            my knowledge base. I can create a support ticket for
            the team to look into this for you.
            Could you please share your work email address?

You       : jane.doe@roadmapconsulting.com

SmartDesk : I would like to create a support ticket for you.

            ----------------------------------------
              📋 Title    : My monitor has been flickering
              🏷  Category : IT Support
              📧 Email    : jane.doe@roadmapconsulting.com
              🤖 Created by: SmartDesk AI Agent
            ----------------------------------------

            Shall I go ahead and create this ticket?
            Type YES to confirm or NO to cancel.

You       : Yes

SmartDesk : Your support ticket has been created successfully!

              Ticket ID  : SSDAI-14
              Title      : My monitor has been flickering
              URL        : https://yourname.atlassian.net/browse/SSDAI-14

            The support team will review your ticket and get back
            to you shortly. Is there anything else I can help you with?
```

### Flow C — Ticket Status Check

```
You       : Any updates on my support ticket?

SmartDesk : Could you please share your work email address
            so I can look that up for you?

You       : jane.doe@roadmapconsulting.com

SmartDesk : I found 1 ticket(s) for jane.doe@roadmapconsulting.com:

            🎫 SSDAI-14 : My monitor has been flickering
               📊 Status  : In Progress
               📅 Created : 2026-06-02
               💬 Update  : Replacement monitor ordered, delivery Thursday
               🔗 Link    : https://yourname.atlassian.net/browse/SSDAI-14

            Is there anything else I can help you with?
```

---

## 🧪 Test Suite

All 16 test files can be run independently from the project root.

### Test Results Summary

| Test File | What It Verifies | Result |
|---|---|---|
| `test_confirmation.py` | Human-in-the-loop yes/no/cancel/change title | ✅ 6 of 6 passed |
| `test_create_ticket.py` | End-to-end Jira ticket creation across 3 categories | ✅ 3 of 3 passed |
| `test_edge_cases.py` | 21 boundary and unexpected input scenarios | ✅ Zero crashes |
| `test_error_handling.py` | API failure graceful degradation | ✅ 5 of 5 passed |
| `test_flow_a.py` | Flow A official: KB answer verification | ✅ 5 of 5 passed |
| `test_flow_b.py` | Flow B official: escalation and ticket creation | ✅ 4 of 4 passed |
| `test_flow_c.py` | Flow C official: ticket status check | ✅ 5 of 5 passed |
| `test_get_status.py` | Jira status retrieval by email and ticket ID | ✅ 4 of 4 passed |
| `test_graceful_handling.py` | Greetings, thanks, off-topic, long/short inputs | ✅ 10 of 10 passed |
| `test_jira_connection.py` | Live Jira API connectivity and project access | ✅ 5 of 5 passed |
| `test_langgraph.py` | LangGraph install and all agent dependencies | ✅ 5 of 5 passed |
| `test_rag_chain.py` | RAG answer quality for in-scope and out-of-scope | ✅ 3 of 3 passed |
| `test_retrieval.py` | ChromaDB retrieval scores and source mapping | ✅ All passed |
| `test_security.py` | No hardcoded secrets across all Python and MD files | ✅ 8 of 8 passed |
| `test_threshold.py` | Confidence threshold in-scope vs out-of-scope routing | ✅ 6 of 6 passed |
| `test_ticket_status.py` | End-to-end ticket status lookup all scenarios | ✅ 5 of 5 passed |

### How to Run Tests

```bash
# Activate virtual environment first
venv\Scripts\Activate.ps1

# Run a single test
python tests/test_flow_a.py

# Run all tests with pytest
python -m pytest tests/

# Run all tests via Docker
docker-compose run --rm smartdesk python -m pytest tests/
```

---

## 🎯 Self Assessment Against Rubric

| Category | Max Marks | Self Assessment | Evidence |
|---|---|---|---|
| Knowledge Base Quality | 20 | 18/20 | 40+ Q&A pairs across IT and HR with 7 deliberate escalation gaps |
| RAG Pipeline | 25 | 23/25 | ChromaDB with confidence threshold, escalation routing, error handling |
| Ticket Integration | 20 | 20/20 | Full Jira CRUD with human-in-the-loop confirmation flow |
| Orchestration & Routing | 15 | 14/15 | Intent detection routing all three flows with session state management |
| Conversation Quality | 10 | 9/10 | Polite tone, session memory, graceful degradation on all API failures |
| Code Quality & Docs | 10 | 9/10 | Modular src/ layout, 16 test files, Docker support, this README |
| **Total** | **100** | **93/100** | |

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11 | Core programming language |
| **LLM** | OpenAI GPT-4o-mini | Generates grounded answers from retrieved context |
| **Embeddings** | OpenAI text-embedding-3-small | Converts text to searchable vectors |
| **Vector Store** | ChromaDB | Stores and searches document chunks by similarity |
| **RAG Framework** | LangChain | Connects retriever, embeddings, and LLM |
| **Agent Orchestration** | LangGraph | Routes intents and manages conversation state |
| **Ticketing** | Jira Cloud REST API | Creates and reads support tickets |
| **Configuration** | PyYAML + config.yaml | Centralised RAG pipeline settings |
| **Secret Management** | python-dotenv | Loads API keys from .env file |
| **Containerisation** | Docker + docker-compose | Portable, reproducible deployment |
| **Testing** | Python unittest + pytest | 16-file test suite covering all flows and edge cases |
| **Version Control** | Git + GitHub | Source control and submission |

---

## 🎬 Demo Video

> **[Add your Loom or YouTube link here before submitting]**

The demo covers:
- Flow A — Answering an IT password reset question from the knowledge base
- Flow B — Escalating a monitor issue to a Jira ticket with human-in-the-loop confirmation
- Flow C — Checking the status of an existing support ticket by email

---

## ⚠️ Known Limitations

- **CLI only.** The agent runs as a command-line interface. A web UI is scaffolded in `src/web_app/` but not yet implemented.
- **No cross-session memory.** Session state resets when the agent is restarted. The agent does not remember your email from a previous run.
- **Live API dependency.** Both OpenAI and Jira require an active internet connection. The agent handles API failures gracefully and informs the employee to try again.
- **Single-user design.** The current architecture serves one conversation at a time. Multi-user concurrency would require a session store (e.g. Redis).

---

## 👤 Author

**Oscar** — AI Generalist in Training

| Detail | Value |
|---|---|
| Program | Interview Kickstart — Applied Agentic AI |
| Project | SmartDesk AI Capstone |
| GitHub | [github.com/oscar2412](https://github.com/oscar2412) |

---

<div align="center">

*Built with 🤖 RAG · Agentic AI · Jira Integration · Docker · Python 3.11*

*Interview Kickstart — Applied Agentic AI Program*

</div>
