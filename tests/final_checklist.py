# ── final_checklist.py ───────────────────────────────────────────
# Final submission checklist for SmartDesk AI.
# Verifies every required file exists and the project
# is ready for evaluator review.
# ────────────────────────────────────────────────────────────────

import os
import json
import subprocess

print("=" * 60)
print("SmartDesk AI — Final Submission Checklist")
print("=" * 60)
print()

passed   = 0
failed   = 0
warnings = 0


def check(label, condition, critical=True, fix=None):
    global passed, failed, warnings
    if condition:
        print(f"  ✅ {label}")
        passed += 1
    else:
        if critical:
            print(f"  ❌ {label}")
            if fix:
                print(f"     FIX: {fix}")
            failed += 1
        else:
            print(f"  ⚠️  {label}")
            if fix:
                print(f"     FIX: {fix}")
            warnings += 1


# ════════════════════════════════════════════════════════════════
# SECTION 1 — Core Python Files
# ════════════════════════════════════════════════════════════════
print("SECTION 1 — Core Python Files")
print()

check("agent.py exists",
      os.path.exists("src/agents/agent.py"))

check("rag_chain.py exists",
      os.path.exists("src/rag/rag_chain.py"))

check("jira_tools.py exists",
      os.path.exists("src/core/jira_tools.py"))

check("retrieval_with_threshold.py exists",
      os.path.exists("src/rag/retrieval_with_threshold.py"))

check("index_knowledge_base.py exists",
      os.path.exists("src/data/index_knowledge_base.py"))

check("rag_config.py exists",
      os.path.exists("src/rag/rag_config.py"))

print()

# ════════════════════════════════════════════════════════════════
# SECTION 2 — Configuration and Setup Files
# ════════════════════════════════════════════════════════════════
print("SECTION 2 — Configuration and Setup Files")
print()

check("requirements.txt exists",
      os.path.exists("requirements.txt"))

check("requirements.txt is not empty",
      os.path.exists("requirements.txt") and
      os.path.getsize("requirements.txt") > 100)

check(".gitignore exists",
      os.path.exists(".gitignore"))

check(".env.example exists",
      os.path.exists(".env.example"),
      critical=False,
      fix="Create .env.example with template variables")

check(".env exists locally",
      os.path.exists(".env"),
      critical=True,
      fix="Create .env file with your API keys")

print()

# ════════════════════════════════════════════════════════════════
# SECTION 3 — Documentation Files
# ════════════════════════════════════════════════════════════════
print("SECTION 3 — Documentation Files")
print()

check("README.md exists",
      os.path.exists("README.md"))

check("README.md is substantial",
      os.path.exists("README.md") and
      os.path.getsize("README.md") > 3000,
      fix="README.md seems too short — add missing sections")

check("self_assessment.md exists",
      os.path.exists("docs/self_assessment.md"),
      fix="Create self_assessment.md with rubric scores")

check("architecture_diagram.png exists",
      os.path.exists("docs/02_architecture_diagram.png"),
      fix="Export architecture diagram from draw.io as PNG")

check("agent_flowchart.png exists",
      os.path.exists("docs/05_agent_flowchart_19.png"),
      fix="Export agent flowchart from draw.io as PNG")

check("agent_design.md exists",
      os.path.exists("docs/03_agent_design.md"),
      critical=False)

check("architecture.md exists",
      os.path.exists("docs/01_architecture.md"),
      critical=False)

print()