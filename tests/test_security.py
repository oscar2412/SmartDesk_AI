import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import glob
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("SmartDesk AI — Security Scan")
print("No Hard-Coded Secrets Verification")
print("=" * 60)
print()

passed   = 0
failed   = 0
warnings = 0

openai_key  = os.getenv("OPENAI_API_KEY",   "")
jira_token  = os.getenv("JIRA_API_TOKEN",   "")
jira_email  = os.getenv("JIRA_EMAIL",       "")
jira_server = os.getenv("JIRA_SERVER",      "")

secrets_to_check = []

if len(openai_key) > 8:
    secrets_to_check.append({"name": "OpenAI API Key", "pattern": openai_key[:12],  "critical": True})
if len(jira_token) > 8:
    secrets_to_check.append({"name": "Jira API Token", "pattern": jira_token[:12],  "critical": True})
if jira_email:
    secrets_to_check.append({"name": "Jira Email",     "pattern": jira_email,       "critical": False})

# Run scan from project root (parent of tests/)
project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
original_dir = os.getcwd()
os.chdir(project_root)

py_files = glob.glob("**/*.py", recursive=True)
py_files = [f for f in py_files if "venv" not in f and "__pycache__" not in f]

md_files  = glob.glob("**/*.md",  recursive=True)
all_files = py_files + md_files

print(f"Scanning {len(all_files)} files...")
print(f"  Python files  : {len(py_files)}")
print(f"  Markdown files: {len(md_files)}")
print()

for secret in secrets_to_check:
    print(f"Checking: {secret['name']}")
    print(f"  Pattern: {secret['pattern'][:4]}****")
    print()

    found_in = []
    for filepath in all_files:
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if secret["pattern"] in content:
                    found_in.append(filepath)
        except Exception:
            pass

    if not found_in:
        print(f"  Not found in any file : PASS ✅")
        passed += 1
    else:
        for filepath in found_in:
            if secret["critical"]:
                print(f"  FOUND IN: {filepath} ❌ CRITICAL")
                failed += 1
            else:
                print(f"  FOUND IN: {filepath} ⚠️  WARNING")
                warnings += 1
    print()

print("Checking: .env is in .gitignore")
print()
try:
    with open(".gitignore", "r") as f:
        gitignore_content = f.read()
    if ".env" in gitignore_content:
        print("  .env in .gitignore    : PASS ✅")
        passed += 1
    else:
        print("  .env in .gitignore    : FAIL ❌ CRITICAL")
        failed += 1
except FileNotFoundError:
    print("  .gitignore not found  : FAIL ❌ CRITICAL")
    failed += 1
print()

print("Checking: .env file is not tracked by git")
print()
import subprocess
try:
    result = subprocess.run(["git", "ls-files", ".env"], capture_output=True, text=True)
    if result.stdout.strip():
        print("  .env tracked by git   : FAIL ❌ CRITICAL")
        failed += 1
    else:
        print("  .env not tracked      : PASS ✅")
        passed += 1
except Exception as e:
    print(f"  Git check error       : WARNING ⚠️ - {str(e)}")
    warnings += 1
print()

print("Checking: chroma_db is in .gitignore")
print()
try:
    with open(".gitignore", "r") as f:
        gitignore_content = f.read()
    if "chroma_db" in gitignore_content:
        print("  chroma_db in .gitignore: PASS ✅")
        passed += 1
    else:
        print("  chroma_db in .gitignore: WARNING ⚠️")
        warnings += 1
except Exception:
    pass
print()

print("Checking: venv is in .gitignore")
print()
try:
    with open(".gitignore", "r") as f:
        gitignore_content = f.read()
    if "venv" in gitignore_content:
        print("  venv in .gitignore    : PASS ✅")
        passed += 1
    else:
        print("  venv in .gitignore    : WARNING ⚠️")
        warnings += 1
except Exception:
    pass
print()

print("Checking: Python files use os.getenv for secrets")
print()
env_usage_ok = True
for filepath in py_files:
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        sk_prefix   = "sk" + "-"
        bad_patterns = [
            'OPENAI_API_KEY = "' + sk_prefix,
            "OPENAI_API_KEY = '" + sk_prefix,
            'api_key = "'        + sk_prefix,
            "api_key = '"        + sk_prefix,
        ]
        for pattern in bad_patterns:
            if pattern in content:
                print(f"  Suspicious pattern in {filepath} ❌")
                env_usage_ok = False
                failed += 1
    except Exception:
        pass

if env_usage_ok:
    print("  No suspicious patterns : PASS ✅")
    passed += 1
print()

os.chdir(original_dir)

print("=" * 60)
print("SECURITY SCAN SUMMARY")
print("=" * 60)
print(f"  Checks passed   : {passed}")
print(f"  Checks failed   : {failed}")
print(f"  Warnings        : {warnings}")
print()

if failed == 0 and warnings == 0:
    print("All security checks passed! ✅")
    print("No secrets found. Your project is safe to submit.")
elif failed == 0 and warnings > 0:
    print("Security checks passed with warnings. ✅")
    print(f"  {warnings} warning(s) — review above.")
else:
    print("CRITICAL SECURITY ISSUES FOUND! ❌")
    print("Fix these before submitting to GitHub.")
print()
