# SmartDesk_AI
SmartDesk AI - Intelligent IT and HR Operations Agent Capstone Project<div align="center">

```
███████╗███╗   ███╗ █████╗ ██████╗ ████████╗██████╗ ███████╗███████╗██╗  ██╗
██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔════╝██╔════╝██║ ██╔╝
███████╗██╔████╔██║███████║██████╔╝   ██║   ██║  ██║█████╗  ███████╗█████╔╝
╚════██║██║╚██╔╝██║██╔══██║██╔══██╗   ██║   ██║  ██║██╔══╝  ╚════██║██╔═██╗
███████║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   ██████╔╝███████╗███████║██║  ██╗
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
```

# 🤖 SmartDesk AI
### An Intelligent IT & HR Operations Agent

---

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6B35?style=for-the-badge)](https://chromadb.com)
[![Jira](https://img.shields.io/badge/Jira-Integrated-0052CC?style=for-the-badge&logo=jira&logoColor=white)](https://atlassian.com/jira)
[![LangChain](https://img.shields.io/badge/LangChain-RAG_Pipeline-1C3C3C?style=for-the-badge)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

---

> *"Stop searching through wikis. Just ask SmartDesk."*

**SmartDesk AI** is a production-style conversational agent that acts as a first-line IT and HR help desk for any organisation. It answers employee questions from a curated knowledge base, creates Jira support tickets when it cannot help, and lets employees check their ticket status — all in a single chat interface.

---

</div>

## 📋 Table of Contents

- [What SmartDesk AI Does](#-what-smartdesk-ai-does)
- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Environment Variables](#-environment-variables)
- [Setup Instructions](#-setup-instructions)
- [Building the Knowledge Base](#-building-the-knowledge-base)
- [Running the Agent](#-running-the-agent)
- [Example Conversation Flows](#-example-conversation-flows)
- [Technology Stack](#-technology-stack)
- [Marking Scheme Alignment](#-marking-scheme-alignment)
- [Known Limitations](#-known-limitations)
- [Author](#-author)

---

## 🎯 What SmartDesk AI Does

Most IT and HR support teams are buried in repetitive questions — password resets, leave policies, VPN setup, reimbursement processes. The answers already exist in internal documents. Employees just cannot find them fast enough.

**SmartDesk AI sits between the employee and the support team and handles three things:**

| Capability | What It Means | How It Works |
|---|---|---|
| 🔍 **Answer from Knowledge Base** | Instantly answers IT and HR questions | RAG pipeline searches ChromaDB vector store, GPT generates grounded answer |
| 🎫 **Create a Support Ticket** | Opens a Jira ticket when it cannot answer | Collects employee info, confirms before submitting, returns ticket ID |
| 📊 **Check Ticket Status** | Reports back on open tickets | Queries Jira API by employee email, displays status and team comments |

---

## 🏗 Architecture Overview

```
![SmartDesk AI System Architecture](architecture_diagram.png)

### Component Flow
┌─────────────────────────────────────────────────────────────────┐
│                        EMPLOYEE INPUT                           │
│                   "How do I reset my VPN?"                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTENT DETECTOR                              │
│           Classifies input as one of three flows:               │
│    KB_QUERY  │  CREATE_TICKET  │  CHECK_STATUS                  │
└──────┬───────────────┬─────────────────────┬────────────────────┘
       │               │                     │
       ▼               ▼                     ▼
┌──────────┐   ┌───────────────┐   ┌─────────────────┐
│   RAG    │   │    TICKET     │   │     TICKET      │
│ PIPELINE │   │   CREATION    │   │  STATUS CHECK   │
│          │   │               │   │                 │
│ChromaDB  │   │ Collect Info  │   │  Lookup by      │
│  Search  │   │    ↓          │   │  Employee Email │
│    ↓     │   │ Show Summary  │   │     ↓           │
│  OpenAI  │   │    ↓          │   │  Return Status  │
│  Answer  │   │ Confirm Y/N   │   │  + Comments     │
│          │   │    ↓          │   │                 │
│          │   │ Create Ticket │   │                 │
└──────────┘   └───────────────┘   └─────────────────┘
       │               │                     │
       └───────────────┴─────────────────────┘
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
├── 📄 .env                        ← Your secret API keys (NEVER on GitHub)
├── 📄 .gitignore                  ← Protects secrets from GitHub
├── 📄 README.md                   ← You are reading this right now
├── 📄 requirements.txt            ← All Python libraries needed
│
│ Test files that confirm Success or Failed app activity
├── 📄 test_confirmation.py        ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── 📄 test_.py                    ← xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
│
│
├── 📂 knowledge_base/             ← All documents the AI learns from
│   ├── it_support_guide.md        ← VPN, password reset, MFA, email setup
│   ├── hr_leave_policy.md         ← Leave types, approval process, WFH
│   ├── it_qa.json                 ← IT question-answer pairs (15+ entries)
│   ├── hr_qa.json                 ← HR question-answer pairs (15+ entries)
│   └── out_of_scope_topics.txt    ← Deliberate gaps to test escalation
│
├── 📂 chroma_db/                  ← Vector database (auto-generated, not on GitHub)
│
├── 📄 index_knowledge_base.py     ← Loads documents into ChromaDB
├── 📄 rag_chain.py                ← Retrieves context and generates answers
├── 📄 jira_tools.py               ← Creates and reads Jira tickets
├── 📄 agent.py                    ← Main orchestrator — the brain of SmartDesk
│
├── 📂 venv/                       ← Virtual environment (not on GitHub)

```

---

## ✅ Prerequisites

Before running SmartDesk AI make sure you have all of the following:

- **Python 3.11** installed — [Download here](https://python.org/downloads)
- **Git** installed — [Download here](https://git-scm.com)
- **VS Code** installed — [Download here](https://code.visualstudio.com)
- **OpenAI account** with API key — [Sign up here](https://platform.openai.com)
- **Jira Cloud account** (free tier is enough) — [Sign up here](https://atlassian.com/jira)
- **Jira API token** created in your Atlassian account settings

---

## 🔐 Environment Variables

SmartDesk AI uses a `.env` file to store all secrets. **Never hard-code these in your Python files.**

Create a file named `.env` in the root of your project folder and add the following:

```env
# ── OpenAI ──────────────────────────────────────────
OPENAI_API_KEY=sk-proj-your-openai-key-here

# ── Jira ────────────────────────────────────────────
JIRA_EMAIL=your-jira-email@example.com
JIRA_API_TOKEN=your-jira-api-token-here
JIRA_SERVER=https://yourname.atlassian.net
JIRA_PROJECT_KEY=SD
```

> ⚠️ **Security Rule:** The `.gitignore` file already blocks `.env` from being uploaded to GitHub. Never remove `.env` from `.gitignore`.

---

## 🚀 Setup Instructions

Follow these steps **in order** from a fresh clone of this repository.

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YourUsername/SmartDesk_AI.git
cd SmartDesk_AI
```

### Step 2 — Create and Activate Virtual Environment

```bash
# Create the virtual environment
py -3.11 -m venv venv

# Activate it (Windows)
venv\Scripts\Activate.ps1

# Activate it (Mac/Linux)
source venv/bin/activate
```

You should see **(venv)** appear on the left of your terminal line. ✅

### Step 3 — Install All Required Libraries

```bash
pip install -r requirements.txt
```

### Step 4 — Add Your API Keys

Create your `.env` file using the template in the [Environment Variables](#-environment-variables) section above.

### Step 5 — Build the Knowledge Base

Place your documents in the `knowledge_base/` folder then run:

```bash
python index_knowledge_base.py
```

This reads all your documents, creates embeddings, and stores them in ChromaDB. A `chroma_db/` folder will appear. ✅

### Step 6 — Run the Agent

```bash
python agent.py
```

The agent will start in your terminal and wait for your first message. Type your question and press Enter.

---

## 📚 Building the Knowledge Base

The knowledge base is the foundation of SmartDesk AI. The better your documents, the better your agent performs.

### Minimum Requirements

| Requirement | Target |
|---|---|
| Total question-answer pairs | At least 30–50 |
| IT support topics covered | Password reset, VPN, MFA, email setup |
| HR topics covered | Leave policy, WFH, onboarding, reimbursement |
| Deliberate gaps included | At least 5 unanswerable topics |

### Option A — Download Ready-Made Datasets

- **HR Policies:** [huggingface.co/datasets?search=hr+pol](https://huggingface.co/datasets?sort=trending&search=hr+pol)
- **IT Support Tickets:** [huggingface.co/datasets?search=it+tick](https://huggingface.co/datasets?sort=trending&search=it+tick)
- **Recommended starter:** `strova-ai/hr-policies-qa-dataset` on Hugging Face

### Option B — Generate With ChatGPT

Use this prompt to generate IT documents:

```
You are the IT Admin at AcmeCorp, a 300-employee company.
Write an internal guide covering: password reset steps,
VPN setup for Windows and Mac, MFA setup, and email setup
on mobile. Write in simple professional language for employees.
```

Use this prompt to generate HR documents:

```
You are the HR Manager at AcmeCorp. Write a Leave Policy
covering casual leave, sick leave, earned leave, and work
from home policy. Include how to apply and approval steps.
Keep it simple and professional.
```

### Option C — Combine Both (Recommended ⭐)

Download the Hugging Face HR dataset for breadth, then generate synthetic IT guides for depth. This is the fastest path to a high-quality knowledge base.

---

## 💬 Example Conversation Flows

### Flow A — Question Answered from Knowledge Base

```
You  : Hi, how do I reset my password?

Bot  : Hello! To reset your password, visit the Self-Service
       Password Portal at https://passwords.acmecorp.com.
       Click "Forgot Password", enter your employee ID, and
       follow the instructions sent to your registered email.
       If you're locked out, contact IT at ext. 2020.
       Is there anything else I can help you with?

You  : No, thanks!

Bot  : You're welcome! Have a great day. 😊
```

---

### Flow B — Question Escalated to Ticket Creation

```
You  : My monitor has been flickering for two days.

Bot  : I'm sorry to hear that. I don't have a troubleshooting
       guide for this specific issue. I can create a support
       ticket for the IT team. Could you share your email address?

You  : jane.doe@acmecorp.com

Bot  : Thanks Jane! Here is the ticket I will create:

       📋 Title       : Monitor Flickering Issue
       📝 Description : Employee reports monitor flickering
                        for the past two days.
       🏷  Category   : IT Hardware Support
       📧 Email       : jane.doe@acmecorp.com

       Shall I go ahead and create this? (yes / no)

You  : Yes please.

Bot  : ✅ Done! Ticket SD-2847 has been created successfully.
       You can ask me for status updates anytime.
```

---

### Flow C — Ticket Status Check

```
You  : Any updates on my monitor ticket?

Bot  : Sure! Could you share your email address so I can
       look that up?

You  : jane.doe@acmecorp.com

Bot  : I found 1 open ticket for your account:

       🎫 SD-2847 : Monitor Flickering Issue
       📊 Status  : In Progress
       💬 Update  : "Replacement monitor ordered,
                     delivery expected by Thursday."

       Is there anything else I can help you with?
```

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11 | Core programming language |
| **LLM** | OpenAI GPT-4 | Generates answers from context |
| **Embeddings** | OpenAI text-embedding-3-small | Converts text to vectors |
| **Vector Store** | ChromaDB | Stores and searches document chunks |
| **RAG Framework** | LangChain | Wires retriever to LLM |
| **Agent Orchestration** | LangGraph | Routes intents and manages flow |
| **Ticketing** | Jira Cloud REST API | Creates and reads support tickets |
| **Secret Management** | python-dotenv | Loads API keys from .env file |
| **Version Control** | Git + GitHub | Code storage and submission |

---

## 📊 Marking Scheme Alignment

| Category | Marks | What Was Built |
|---|---|---|
| Knowledge Base Quality | 20 | 30–50 Q&A pairs across IT and HR with deliberate gaps |
| RAG Pipeline | 25 | ChromaDB vector store with confidence threshold and escalation |
| Ticket Integration | 20 | Jira create and status functions with human-in-the-loop |
| Orchestration & Routing | 15 | LangGraph intent detection routing all three flows |
| Conversation Quality | 10 | Polite tone, session memory, graceful error handling |
| Code Quality & Docs | 10 | Modular code, this README, architecture diagram |
| **Total** | **100** | |

---

## ⚠️ Known Limitations

- The agent runs as a **command-line interface only**. A web UI is not included but is listed as a bonus feature.
- The agent **does not persist memory across sessions**. If you close and reopen the agent it will not remember your email from a previous conversation.
- The Jira integration requires a **live internet connection**. If the API is unreachable the agent will inform you politely and suggest trying again later.


---

## 🧪 Test Results

All tests were run against the live system before submission.
Every test file can be re-run independently to verify results.

### Test Suite Summary

| Test File | Purpose | Result |
|---|---|---|
| `test_retrieval.py` | ChromaDB retrieval pipeline | ✅ All passed |
| `test_threshold.py` | Confidence threshold logic | ✅ 6 of 6 passed |
| `test_rag_chain.py` | RAG answer generation | ✅ 3 of 3 passed |
| `test_jira_connection.py` | Live Jira connection | ✅ 5 of 5 passed |
| `test_get_status.py` | Ticket status retrieval | ✅ 4 of 4 passed |
| `test_create_ticket.py` | Ticket creation | ✅ 3 of 3 passed |
| `test_ticket_status.py` | End to end status lookup | ✅ 5 of 5 passed |
| `test_confirmation.py` | Human-in-the-loop confirmation | ✅ 6 of 6 passed |
| `test_graceful_handling.py` | Edge case graceful handling | ✅ 10 of 10 passed |
| `test_error_handling.py` | API failure error handling | ✅ 5 of 5 passed |
| `test_flow_a.py` | Flow A — KB answer verification | ✅ 5 of 5 passed |
| `test_flow_b.py` | Flow B — Ticket creation verification | ✅ 4 of 4 passed |
| `test_flow_c.py` | Flow C — Ticket status verification | ✅ 5 of 5 passed |
| `test_edge_cases.py` | 21 edge case scenarios | ✅ Zero crashes |
| `test_security.py` | No hardcoded secrets scan | ✅ 8 of 8 passed |

### How to Run All Tests

Run each test file individually from the project root
with the virtual environment activated:

```bash
# Activate virtual environment first
venv\Scripts\Activate.ps1

# Run individual test files
python test_flow_a.py
python test_flow_b.py
python test_flow_c.py
python test_edge_cases.py
python test_security.py
```

---

## 🎯 Self Assessment Against Rubric

| Category | Max Marks | Self Assessment | Evidence |
|---|---|---|---|
| Knowledge Base Quality | 20 | 18/20 | 40+ Q&A pairs across IT and HR with 7 deliberate gaps |
| RAG Pipeline | 25 | 23/25 | ChromaDB with confidence threshold escalation and error handling |
| Ticket Integration | 20 | 20/20 | Full Jira CRUD with human-in-the-loop confirmation |
| Orchestration & Routing | 15 | 14/15 | LangGraph-style intent detection routing all three flows |
| Conversation Quality | 10 | 9/10 | Polite tone session memory graceful error handling |
| Code Quality & Docs | 10 | 9/10 | Modular code comprehensive tests this README |
| **Total** | **100** | **93/100** | |

---

## 🎬 Demo Video

A demo video showing all three conversation flows is available here:

> **[Add your Loom or YouTube link here before submitting]**

The demo covers:
- Flow A — Answering an IT password reset question from the knowledge base
- Flow B — Escalating a monitor flickering issue to a Jira ticket
- Flow C — Checking the status of an existing support ticket

---

## 🏃 Running the Agent

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/oscar2412/SmartDesk_AI.git
cd SmartDesk_AI

# 2. Create and activate virtual environment
py -3.11 -m venv venv
venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Copy .env.example to .env and fill in your API keys

# 5. Index the knowledge base
python index_knowledge_base.py

# 6. Start the agent
python agent.py
```

### Sample Conversation
SmartDesk : Hello! I am SmartDesk AI your IT and HR support
assistant at Roadmap Consulting.
How can I help you today?
You       : How do I reset my password?
SmartDesk : To reset your password at Roadmap Consulting
please follow these steps:
1. Go to https://passwords.roadmapconsulting.com
2. Click Forgot Password
3. Enter your employee ID
4. Follow the email instructions
Is there anything else I can help you with?

---

## 📋 Environment Variables Reference

Create a `.env` file in the project root with these variables:

| Variable | Description | Example |
|---|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-...` |
| `JIRA_EMAIL` | Email used for Jira account | `you@email.com` |
| `JIRA_API_TOKEN` | Jira API token from Atlassian | `ATATT3x...` |
| `JIRA_SERVER` | Your Atlassian domain | `https://name.atlassian.net` |
| `JIRA_PROJECT_KEY` | Jira project key | `xxxxx` |

---
---

## 👤 Author

## 👤 Author

**Oscar** — AI Generalist in Training

| Detail | Value |
|---|---|
| Program | Interview Kickstart — Applied Agentic AI |
| Project | SmartDesk AI Capstone |
| GitHub | https://github.com/oscar2412 |
| Jira Project | https://xxxxxxxx.atlassian.net |

---

<div align="center">

*Built with 🤖 RAG · Agentic AI · Jira Integration · Python 3.11*

*Interview Kickstart — Applied Agentic AI Program*

</div>

---

<div align="center">

---

*Built with 🤖 RAG · Agentic AI · Jira Integration · Python 3.11*

*Interview Kickstart — Applied Agentic AI Program*

---

</div>
