# ── confidence_check.py ──────────────────────────────────────────
# Evaluator-aligned confidence check for SmartDesk AI.
# Updated for the src/ subfolder project structure.
#
# Category A — Knowledge Base & RAG Pipeline    (25 marks)
# Category B — Ticket Creation Write Operation  (20 marks)
# Category C — Ticket Status Check Read Op      (15 marks)
# Category D — Agent Orchestration & Routing    (15 marks)
# Category E — Code Quality & Documentation     (15 marks)
# Category F — Error Handling & Robustness      (10 marks)
# ────────────────────────────────────────────────────────────────

import os
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

# ── Path Configuration ───────────────────────────────────────────
# All paths mapped to your src/ subfolder structure

PATHS = {
    # Core Python files
    "agent"           : "src/agents/agent.py",
    "rag_chain"       : "src/rag/rag_chain.py",
    "rag_config"      : "src/rag/rag_config.py",
    "retrieval"       : "src/rag/retrieval_with_threshold.py",
    "jira_tools"      : "src/core/jira_tools.py",
    "index_kb"        : "src/data/index_knowledge_base.py",
    "helpers"         : "src/utils/helpers.py",
    "app"             : "src/web_app/app.py",

    # Workflow files
    "flow_a"          : "src/workflow/flow_a.py",
    "flow_b"          : "src/workflow/flow_b.py",
    "flow_c"          : "src/workflow/flow_c.py",

    # Knowledge base files
    "kb_dir"          : "src/data/knowledge_base",
    "it_guide"        : "src/data/knowledge_base/it_support_guide.md",
    "hr_policy"       : "src/data/knowledge_base/hr_leave_policy.md",
    "it_qa"           : "src/data/knowledge_base/it_qa.json",
    "hr_qa"           : "src/data/knowledge_base/hr_qa.json",
    "hr_dataset"      : "src/data/knowledge_base/hr-policies-qa-dataset.jsonl",
    "gaps"            : "src/data/knowledge_base/out_of_scope_topics.txt",

    # Test files
    "tests_dir"         : "tests",
    "test_retrieval"    : "tests/test_retrieval.py",
    "test_threshold"    : "tests/test_threshold.py",
    "test_rag_chain"    : "tests/test_rag_chain.py",
    "test_jira_conn"    : "tests/test_jira_connection.py",
    "test_get_status"   : "tests/test_get_status.py",
    "test_create"       : "tests/test_create_ticket.py",
    "test_ticket_st"    : "tests/test_ticket_status.py",
    "test_confirm"      : "tests/test_confirmation.py",
    "test_graceful"     : "tests/test_graceful_handling.py",
    "test_error"        : "tests/test_error_handling.py",
    "test_flow_a"       : "tests/test_flow_a.py",
    "test_flow_b"       : "tests/test_flow_b.py",
    "test_flow_c"       : "tests/test_flow_c.py",
    "test_edge"         : "tests/test_edge_cases.py",
    "test_security"     : "tests/test_security.py",
 #   "test_poise_checks" : "tests/test_poise_checks.py",  Never to run

    # Documentation files
    "readme"          : "README.md",
    "self_assess"     : "self_assessment.md",
    "arch_diagram"    : "docs/architecture_diagram.drawio.png",
    "arch_md"         : "architecture.md",
    "agent_design"    : "agent_design.md",
    "agent_flowchart" : "docs/agent_flowchart.png",
    "requirements"    : "requirements.txt",
    "env_example"     : ".env.example",
    "gitignore"       : ".gitignore",
    "chroma_db"       : "chroma_db",
    "config_yaml"     : "config.yaml",
}


def exists(key):
    return os.path.exists(PATHS.get(key, ""))


def read(key):
    path = PATHS.get(key, "")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""


def size(key):
    path = PATHS.get(key, "")
    return os.path.getsize(path) if os.path.exists(path) else 0


print("=" * 60)
print("SmartDesk AI — Evaluator Rubric Confidence Check")
print("(Updated for src/ subfolder structure)")
print("=" * 60)
print()

scores  = {}
passed  = 0
failed  = 0


def section(title, max_marks):
    print()
    print("─" * 60)
    print(f"  {title}  [{max_marks} marks]")
    print("─" * 60)
    print()


def check(label, condition, marks, fix=None):
    global passed, failed
    status = "✅ PASS" if condition else "❌ FAIL"
    score  = marks if condition else 0
    print(f"  {status}  [{marks}pts]  {label}")
    if fix and not condition:
        print(f"           → FIX: {fix}")
    if condition:
        passed += 1
    else:
        failed += 1
    return score


# ════════════════════════════════════════════════════════════════
# CATEGORY A — Knowledge Base & RAG Pipeline (25 marks)
# ════════════════════════════════════════════════════════════════
section("CATEGORY A — Knowledge Base & RAG Pipeline", 25)
a_score = 0

# A1: Quality and breadth of KB content (5 marks)
print("A1: Quality and breadth of KB content")

it_size = size("it_guide")
hr_size = size("hr_policy")

a_score += check("IT support guide exists and is substantial",
    exists("it_guide") and it_size > 2000,
    1, f"File at: {PATHS['it_guide']}")

a_score += check("HR leave policy exists and is substantial",
    exists("hr_policy") and hr_size > 2000,
    1, f"File at: {PATHS['hr_policy']}")

a_score += check("External HR dataset included",
    exists("hr_dataset"), 1,
    f"File at: {PATHS['hr_dataset']}")

a_score += check("Deliberate gaps documented",
    exists("gaps"), 1,
    f"File at: {PATHS['gaps']}")

# Count Q&A pairs
qa_count = 0
for key in ["it_qa", "hr_qa"]:
    content = read(key)
    if content:
        try:
            qa_count += len(json.loads(content))
        except Exception:
            pass

a_score += check(f"30+ Q&A pairs total (found {qa_count})",
    qa_count >= 30, 1,
    "Add more Q&A pairs to it_qa.json and hr_qa.json")
print()

# A2: Chunking strategy and justification (5 marks)
print("A2: Chunking strategy and justification")
rc_content = read("rag_config")

a_score += check("CHUNK_SIZE defined in rag_config.py",
    "CHUNK_SIZE" in rc_content, 1,
    f"Add CHUNK_SIZE to {PATHS['rag_config']}")

a_score += check("CHUNK_OVERLAP defined in rag_config.py",
    "CHUNK_OVERLAP" in rc_content, 1,
    f"Add CHUNK_OVERLAP to {PATHS['rag_config']}")

a_score += check("Embedding model configured",
    "EMBEDDING_MODEL" in rc_content, 1,
    "Add EMBEDDING_MODEL to rag_config.py")

a_score += check("Chunking strategy documented",
    exists("arch_md") or exists("agent_design"), 1,
    "Add chunking explanation to architecture.md")

a_score += check("rag_config.py exists and centralises settings",
    exists("rag_config"), 1,
    f"Create {PATHS['rag_config']}")
print()

# A3: Retrieval quality (5 marks)
print("A3: Retrieval quality")
a_score += check("retrieval_with_threshold.py exists",
    exists("retrieval"), 2,
    f"Create {PATHS['retrieval']}")

a_score += check("ChromaDB vector store exists locally",
    os.path.isdir(PATHS["chroma_db"]), 2,
    "Run: python src/data/index_knowledge_base.py")

a_score += check("test_retrieval.py exists",
    exists("test_retrieval"), 1,
    f"Create {PATHS['test_retrieval']}")
print()

# A4: LLM grounding — no hallucination (5 marks)
print("A4: LLM grounding — no hallucination")
rag_content = read("rag_chain")

a_score += check("SYSTEM_PROMPT in rag_chain.py",
    "SYSTEM_PROMPT" in rag_content, 2,
    f"Add SYSTEM_PROMPT to {PATHS['rag_chain']}")

a_score += check("Context injection in prompt",
    "context" in rag_content.lower(), 1,
    "Add context variable to system prompt")

a_score += check("Hallucination guard phrase present",
    "not_found_phrase" in rag_content or
    "don't have enough" in rag_content or
    "I don" in rag_content, 2,
    "Add not_found_phrase check to rag_chain.py")
print()

# A5: Confidence / escalation logic (5 marks)
print("A5: Confidence / escalation logic")
ret_content = read("retrieval")

a_score += check("Confidence threshold check implemented",
    "CONFIDENCE_THRESHOLD" in ret_content, 2,
    "Add CONFIDENCE_THRESHOLD check to retrieval_with_threshold.py")

a_score += check("RESULT_FOUND and RESULT_NOT_FOUND defined",
    "RESULT_FOUND" in ret_content and
    "RESULT_NOT_FOUND" in ret_content, 2,
    "Add RESULT_FOUND and RESULT_NOT_FOUND constants")

a_score += check("test_threshold.py exists",
    exists("test_threshold"), 1,
    f"Create {PATHS['test_threshold']}")

scores["A"] = a_score
print(f"\n  CATEGORY A SCORE: {a_score} / 25")

# ════════════════════════════════════════════════════════════════
# CATEGORY B — Ticket Creation Write Operation (20 marks)
# ════════════════════════════════════════════════════════════════
section("CATEGORY B — Ticket Creation Write Operation", 20)
b_score = 0
jt_content = read("jira_tools")

# B1: Successful external API integration (5 marks)
print("B1: Successful external API integration")
b_score += check("jira library imported",
    "from jira import" in jt_content, 2,
    f"Add jira import to {PATHS['jira_tools']}")

b_score += check("create_ticket function defined",
    "def create_ticket" in jt_content, 2,
    "Add create_ticket function to jira_tools.py")

b_score += check("Jira client connection established",
    "JIRA(" in jt_content or "get_jira_client" in jt_content, 1)
print()

# B2: All mandatory fields collected (5 marks)
print("B2: All mandatory fields collected")
b_score += check("Summary field",      "summary"     in jt_content, 1)
b_score += check("Description field",  "description" in jt_content, 1)
b_score += check("Employee email",     "email"       in jt_content, 1)
b_score += check("Category field",     "category"    in jt_content, 1)
b_score += check("Issue type",         "issuetype"   in jt_content, 1)
print()

# B3: Human-in-the-loop confirmation (5 marks)
print("B3: Human-in-the-loop confirmation")
ag_content = read("agent")
b_score += check("awaiting_confirmation in session",
    "awaiting_confirmation" in ag_content, 2)
b_score += check("Ticket summary shown before confirm",
    "build_ticket_summary" in ag_content or
    "ticket summary" in ag_content.lower(), 1)
b_score += check("YES path creates ticket",
    "yes" in ag_content.lower(), 1)
b_score += check("NO path cancels politely",
    "not been created" in ag_content.lower() or
    "cancel" in ag_content.lower(), 1)
print()

# B4: Post-creation feedback with ticket ID/link (5 marks)
print("B4: Post-creation feedback with ticket ID/link")
b_score += check("Ticket ID returned",
    "ticket_id" in jt_content or "new_issue.key" in jt_content, 2)
b_score += check("Ticket URL returned",
    "ticket_url" in jt_content or "browse" in jt_content, 2)
b_score += check("TICKET_CREATED status returned",
    "TICKET_CREATED" in jt_content, 1)

scores["B"] = b_score
print(f"\n  CATEGORY B SCORE: {b_score} / 20")

# ════════════════════════════════════════════════════════════════
# CATEGORY C — Ticket Status Check Read Operation (15 marks)
# ════════════════════════════════════════════════════════════════
section("CATEGORY C — Ticket Status Check Read Operation", 15)
c_score = 0

# C1: Status retrieval via API (5 marks)
print("C1: Status retrieval via API")
c_score += check("get_ticket_status function defined",
    "def get_ticket_status" in jt_content, 2)
c_score += check("get_ticket_by_id function defined",
    "def get_ticket_by_id" in jt_content, 1)
c_score += check("JQL search by email",
    "jql" in jt_content.lower() or
    "search_issues" in jt_content, 1)
c_score += check("Status field retrieved",
    "status" in jt_content, 1)
print()

# C2: Multiple-ticket handling (5 marks)
print("C2: Multiple-ticket handling")
c_score += check("format_tickets helper function",
    "def format_tickets" in jt_content, 2)
c_score += check("Multiple tickets returned as list",
    "ticket_list" in jt_content or
    "tickets" in jt_content, 1)
c_score += check("Ticket count returned",
    "count" in jt_content, 1)
c_score += check("maxResults limits query",
    "maxResults" in jt_content, 1)
print()

# C3: Graceful handling when no tickets found (5 marks)
print("C3: Graceful handling when no tickets found")
c_score += check("TICKETS_NONE status returned",
    "TICKETS_NONE" in jt_content, 2)
c_score += check("Empty results handled gracefully",
    "not issues" in jt_content or
    "if not" in jt_content, 2)
c_score += check("test_flow_c.py exists",
    exists("test_flow_c"), 1)

scores["C"] = c_score
print(f"\n  CATEGORY C SCORE: {c_score} / 15")

# ════════════════════════════════════════════════════════════════
# CATEGORY D — Agent Orchestration & Routing (15 marks)
# ════════════════════════════════════════════════════════════════
section("CATEGORY D — Agent Orchestration & Routing", 15)
d_score = 0

# D1: Correct intent detection and routing (5 marks)
print("D1: Correct intent detection and routing")
d_score += check("detect_intent function defined",
    "def detect_intent" in ag_content, 2)
d_score += check("KB_QUERY and CHECK_STATUS intents defined",
    "KB_QUERY" in ag_content and
    "CHECK_STATUS" in ag_content, 1)
d_score += check("Intent system prompt defined",
    "INTENT_SYSTEM_PROMPT" in ag_content, 1)
d_score += check("Routing to correct handler functions",
    "handle_kb_query" in ag_content and
    "handle_check_status" in ag_content, 1)
print()

# D2: Smooth multi-turn conversations (5 marks)
print("D2: Smooth multi-turn conversations")

# Also check workflow files for session management
flow_a_content = read("flow_a")
flow_b_content = read("flow_b")
flow_c_content = read("flow_c")
all_workflow   = ag_content + flow_a_content + \
                 flow_b_content + flow_c_content

d_score += check("create_session or session management",
    "create_session" in all_workflow or
    "session" in all_workflow, 1)
d_score += check("Employee email stored in session",
    "employee_email" in all_workflow, 1)
d_score += check("Chat history maintained",
    "chat_history" in all_workflow, 1)
d_score += check("awaiting_email state tracking",
    "awaiting_email" in all_workflow, 1)
d_score += check("Workflow files separate flows A B C",
    exists("flow_a") and exists("flow_b") and
    exists("flow_c"), 1)
print()

# D3: Out-of-scope / ambiguous query handling (5 marks)
print("D3: Out-of-scope and ambiguous query handling")
d_score += check("UNCLEAR intent handled",
    "UNCLEAR" in ag_content, 1)
d_score += check("Unclear response function",
    "unclear" in ag_content.lower() or
    "rephrase" in ag_content.lower(), 1)
d_score += check("Out of scope escalates to ticket",
    "handle_ticket_creation" in ag_content or
    "create_ticket" in all_workflow, 2)
d_score += check("validate_message or input validation",
    "validate" in ag_content.lower() or
    "validate" in all_workflow.lower(), 1)

scores["D"] = d_score
print(f"\n  CATEGORY D SCORE: {d_score} / 15")

# ════════════════════════════════════════════════════════════════
# CATEGORY E — Code Quality & Documentation (15 marks)
# ════════════════════════════════════════════════════════════════
section("CATEGORY E — Code Quality & Documentation", 15)
e_score = 0

# E1: Clean modular readable code (5 marks)
print("E1: Clean, modular, readable code")
core_files_exist = all([
    exists("agent"), exists("rag_chain"),
    exists("jira_tools"), exists("retrieval"),
    exists("index_kb"), exists("rag_config")
])
e_score += check("All 6 core modules exist in src/",
    core_files_exist, 2)

# Count docstrings across all source files
all_source = ag_content + rag_content + jt_content + \
             ret_content + rc_content
docstring_count = all_source.count('"""')
e_score += check(f"Functions have docstrings ({docstring_count} found)",
    docstring_count >= 20, 1,
    "Add docstrings to key functions")

# Count test files
test_count = sum(1 for f in os.listdir("tests")
                 if f.startswith("test_") and
                 f.endswith(".py")) \
             if os.path.isdir("tests") else 0
e_score += check(f"15+ test files in tests/ folder ({test_count} found)",
    test_count >= 15, 2,
    "Make sure all test files are in tests/ folder")
print()

# E2: README with setup instructions (5 marks)
print("E2: README with setup instructions")
rm_content = read("readme").lower()
e_score += check("README has setup/install instructions",
    "setup" in rm_content or "install" in rm_content, 1)
e_score += check("README documents environment variables",
    "openai_api_key" in rm_content or
    "environment" in rm_content, 1)
e_score += check("README shows how to run agent",
    "agent.py" in rm_content or
    "python" in rm_content, 1)
e_score += check("README mentions prerequisites",
    "prerequisite" in rm_content or
    "python 3" in rm_content, 1)
e_score += check("Demo video link in README",
    "loom" in rm_content or
    "video" in rm_content or
    "demo" in rm_content, 1,
    "Add Loom video link to README")
print()

# E3: Architecture diagram (5 marks)
print("E3: Architecture diagram")
e_score += check("architecture_diagram exists",
    exists("arch_diagram") or
    os.path.exists("docs/architecture_diagram.png"), 2,
    "Export diagram from draw.io as PNG")
e_score += check("agent_flowchart.png exists",
    exists("agent_flowchart"), 1)
e_score += check("architecture.md documentation",
    exists("arch_md"), 1)
e_score += check("Docker/deployment config present",
    os.path.exists("Dockerfile") or
    os.path.exists("docker-compose.yml"), 1)

scores["E"] = e_score
print(f"\n  CATEGORY E SCORE: {e_score} / 15")

# ════════════════════════════════════════════════════════════════
# CATEGORY F — Error Handling & Robustness (10 marks)
# ════════════════════════════════════════════════════════════════
section("CATEGORY F — Error Handling & Robustness", 10)
f_score = 0

# F1: Graceful API failure degradation (3 marks)
print("F1: Graceful API failure degradation")
all_code = ag_content + rag_content + jt_content + \
           ret_content + flow_a_content + \
           flow_b_content + flow_c_content
try_count = all_code.count("except Exception")

f_score += check(f"Multiple try/except blocks ({try_count} found)",
    try_count >= 3, 1)
f_score += check("API error response function or message",
    "api_error" in all_code.lower() or
    "trouble connecting" in all_code.lower() or
    "try again" in all_code.lower(), 1)
f_score += check("JIRAError handled in jira_tools.py",
    "JIRAError" in jt_content, 1)
print()

# F2: Retry logic / LLM fallback (3 marks)
print("F2: Retry logic / LLM fallback")
f_score += check("OpenAI call wrapped in try/except",
    "except Exception" in rag_content, 1)
f_score += check("ANSWER_NOT_FOUND fallback on LLM failure",
    "ANSWER_NOT_FOUND" in rag_content, 1)
f_score += check("User-friendly fallback message",
    "trouble connecting" in rag_content.lower() or
    "try again" in rag_content.lower() or
    "moment" in rag_content.lower(), 1,
    "Add friendly fallback message to rag_chain.py")
print()

# F3: No hard-coded secrets (2 marks)
print("F3: No hard-coded secrets")
secrets_found = False
sk_prefix = "sk" + "-"
for root, dirs, files in os.walk("src"):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for fname in files:
        if fname.endswith(".py"):
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding="utf-8",
                          errors="ignore") as fp:
                    content = fp.read()
                if sk_prefix + "proj" in content:
                    secrets_found = True
            except Exception:
                pass

f_score += check("No API keys hardcoded in src/ files",
    not secrets_found, 1,
    "Remove any hardcoded API keys from source files")
f_score += check("test_security.py exists",
    exists("test_security"), 1)
print()

# F4: Edge-case handling (2 marks)
print("F4: Edge-case handling")
f_score += check("Input validation in agent or workflow",
    "validate" in all_code.lower() or
    "is_greeting" in all_code or
    "empty" in all_code.lower(), 1)
f_score += check("test_edge_cases.py exists",
    exists("test_edge"), 1)

scores["F"] = f_score
print(f"\n  CATEGORY F SCORE: {f_score} / 10")

# ════════════════════════════════════════════════════════════════
# FINAL RESULTS
# ════════════════════════════════════════════════════════════════
print()
print("=" * 60)
print("CONFIDENCE CHECK — FINAL RESULTS")
print("=" * 60)
print()

total_score = sum(scores.values())
max_scores  = {
    "A": 25, "B": 20, "C": 15,
    "D": 15, "E": 15, "F": 10
}
labels = {
    "A": "Knowledge Base & RAG Pipeline",
    "B": "Ticket Creation (Write Operation)",
    "C": "Ticket Status Check (Read Operation)",
    "D": "Agent Orchestration & Routing",
    "E": "Code Quality & Documentation",
    "F": "Error Handling & Robustness"
}

for cat in ["A", "B", "C", "D", "E", "F"]:
    s   = scores[cat]
    mx  = max_scores[cat]
    pct = int((s / mx) * 100)
    bar = "█" * (s * 2) + "░" * ((mx - s) * 2)
    print(f"  Cat {cat}: {bar} {s}/{mx} ({pct}%)")
    print(f"         {labels[cat]}")
    print()

print(f"  TOTAL ESTIMATED SCORE: {total_score} / 100")
print()

if total_score >= 90:
    print("🏆 EXCELLENT — Strong submission!")
elif total_score >= 80:
    print("✅ GOOD — Solid submission with minor gaps.")
elif total_score >= 70:
    print("⚠️  FAIR — Some areas need attention before submitting.")
else:
    print("❌ NEEDS WORK — Fix failures above before submitting.")

print()
print(f"  Checks passed : {passed}")
print(f"  Checks failed : {failed}")
print()
print("Items marked ❌ should be fixed before submission.")
print()