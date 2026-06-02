import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

print("=" * 60)
print("SmartDesk AI — LangGraph Installation Test")
print("=" * 60)
print()

passed = 0
failed = 0

print("Test 1: Importing core LangGraph...")
try:
    from langgraph.graph import StateGraph, END
    print("  StateGraph         : OK ✅")
    print("  END                : OK ✅")
    passed += 1
except ImportError as e:
    print(f"  LangGraph core     : FAILED ❌ - {e}")
    failed += 1
print()

print("Test 2: Importing TypedDict for state management...")
try:
    from typing import TypedDict, Annotated, List
    import operator
    print("  TypedDict          : OK ✅")
    print("  Annotated          : OK ✅")
    print("  List               : OK ✅")
    passed += 1
except ImportError as e:
    print(f"  typing imports     : FAILED ❌ - {e}")
    failed += 1
print()

print("Test 3: Importing LangChain message types...")
try:
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    print("  HumanMessage       : OK ✅")
    print("  AIMessage          : OK ✅")
    print("  SystemMessage      : OK ✅")
    passed += 1
except ImportError as e:
    print(f"  LangChain messages : FAILED ❌ - {e}")
    failed += 1
print()

print("Test 4: Building a minimal test graph...")
try:
    from langgraph.graph import StateGraph, END
    from typing import TypedDict

    class TestState(TypedDict):
        message: str
        processed: bool

    def process_node(state: TestState) -> TestState:
        return {"message": state["message"].upper(), "processed": True}

    graph_builder = StateGraph(TestState)
    graph_builder.add_node("process", process_node)
    graph_builder.set_entry_point("process")
    graph_builder.add_edge("process", END)
    test_graph = graph_builder.compile()

    result = test_graph.invoke({"message": "hello smartdesk", "processed": False})

    if result["processed"] and result["message"] == "HELLO SMARTDESK":
        print("  Graph built        : OK ✅")
        print("  Graph compiled     : OK ✅")
        print("  Graph ran          : OK ✅")
        print(f"  Test output        : {result['message']} ✅")
        passed += 1
    else:
        print("  Graph test         : FAIL ❌")
        failed += 1
except Exception as e:
    print(f"  Graph test         : FAILED ❌ - {e}")
    failed += 1
print()

print("Test 5: Confirming all agent dependencies are ready...")
try:
    from src.rag.rag_chain import get_rag_answer, format_sources
    print("  rag_chain          : OK ✅")
except ImportError as e:
    print(f"  rag_chain          : FAILED ❌ - {e}")
    failed += 1

try:
    from src.core.jira_tools import create_ticket, get_ticket_status, get_ticket_by_id, format_tickets
    print("  jira_tools         : OK ✅")
except ImportError as e:
    print(f"  jira_tools         : FAILED ❌ - {e}")
    failed += 1

try:
    from src.rag.rag_config import LLM_MODEL
    print("  rag_config         : OK ✅")
    passed += 1
except ImportError as e:
    print(f"  rag_config         : FAILED ❌ - {e}")
    failed += 1
print()

print("=" * 60)
print("LANGGRAPH INSTALLATION TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of 5")
print(f"  Tests failed : {failed} of 5")
print()
if failed == 0:
    print("All tests passed! ✅")
    print("LangGraph is installed and all agent dependencies are ready.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
print()
