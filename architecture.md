# SmartDesk AI — Architecture Documentation

## System Architecture Diagram

![Architecture Diagram](architecture_diagram.png)

## Component Descriptions

### Layer 1 — User Interface
| Component | Description |
|---|---|
| Terminal CLI | Employee interacts via `python agent.py` |
| Input handler | Validates and cleans all employee messages |

### Layer 2 — Agent Orchestrator
| Component | Description |
|---|---|
| `agent.py` | Main orchestrator — routes all conversation flows |
| Intent Detection | Classifies messages as KB_QUERY or CHECK_STATUS |
| Session Memory | Remembers employee email across conversation turns |
| Human-in-the-Loop | Confirms before creating any Jira ticket |

### Layer 3 — Core Components
| Component | Description |
|---|---|
| `rag_chain.py` | Builds GPT prompts from retrieved context |
| `retrieval_with_threshold.py` | Searches ChromaDB with confidence gating |
| `jira_tools.py` | Creates and reads Jira tickets via REST API |

### Layer 4 — Local Data Stores
| Component | Description |
|---|---|
| `ChromaDB` | Vector database storing all document embeddings |
| `knowledge_base/` | Source documents — markdown and JSON files |
| `rag_config.py` | Central configuration for all RAG settings |

### Layer 5 — External Services
| Component | Description |
|---|---|
| OpenAI API | GPT-4o-mini for answer generation |
| OpenAI Embeddings | text-embedding-3-small for vector creation |
| Jira Cloud API | REST API for ticket CRUD operations |

## Data Flow

### Flow A — Knowledge Base Answer

Employee message
→ agent.py detects KB_QUERY intent
→ rag_chain.py calls retrieve_with_threshold()
→ retrieval_with_threshold.py searches ChromaDB
→ Top 3 chunks returned if above threshold
→ rag_chain.py builds GPT prompt with context
→ OpenAI API generates grounded answer
→ Answer returned to employee

### Flow B — Ticket Creation
Employee message → RAG returns ANSWER_NOT_FOUND
→ agent.py asks for employee email
→ agent.py shows ticket summary
→ Employee confirms yes
→ jira_tools.py calls Jira Cloud API
→ New ticket created in SSDAI project
→ Ticket ID returned to employee

### Flow C — Ticket Status
Employee asks about ticket status
→ agent.py detects CHECK_STATUS intent
→ agent.py asks for employee email
→ jira_tools.py searches Jira by email
→ Matching tickets returned and formatted
→ Ticket list displayed to employee

## Security Architecture

| Security Measure | Implementation |
|---|---|
| API key storage | `.env` file — never committed to GitHub |
| .gitignore | Blocks `.env`, `venv/`, `chroma_db/` |
| No hardcoded secrets | Verified by `test_security.py` |
| Human confirmation | Required before any write operation |