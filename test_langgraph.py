# ── test_langgraph.py ────────────────────────────────────────────
# Quick test to confirm LangGraph is installed correctly
# and the core components needed for agent.py are available.
# ────────────────────────────────────────────────────────────────

print("=" * 60)
print("SmartDesk AI — LangGraph Installation Test")
print("=" * 60)
print()

passed = 0
failed = 0

# ── Test 1: Core LangGraph Import ────────────────────────────────
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

# ── Test 2: TypedDict for State Management ───────────────────────
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

# ── Test 3: LangChain Messages ───────────────────────────────────
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

# ── Test 4: Build a Minimal Test Graph ───────────────────────────
print("Test 4: Building a minimal test graph...")
try:
    from langgraph.graph import StateGraph, END
    from typing import TypedDict

    # Define a simple state
    class TestState(TypedDict):
        message: str
        processed: bool

    # Define a simple node function
    def process_node(state: TestState) -> TestState:
        return {
            "message"  : state["message"].upper(),
            "processed": True
        }

    # Build a simple one node graph
    graph_builder = StateGraph(TestState)
    graph_builder.add_node("process", process_node)
    graph_builder.set_entry_point("process")
    graph_builder.add_edge("process", END)

    # Compile the graph
    test_graph = graph_builder.compile()

    # Run the graph with a test input
    result = test_graph.invoke({
        "message"  : "hello smartdesk",
        "processed": False
    })

    if result["processed"] and result["message"] == "HELLO SMARTDESK":
        print("  Graph built        : OK ✅")
        print("  Graph compiled     : OK ✅")
        print("  Graph ran          : OK ✅")
        print(f"  Test output        : {result['message']} ✅")
        passed += 1
    else:
        print("  Graph test         : FAIL ❌")
        print(f"  Got result         : {result}")
        failed += 1

except Exception as e:
    print(f"  Graph test         : FAILED ❌ - {e}")
    failed += 1

print()

# ── Test 5: Confirm All Agent Dependencies Are Ready ─────────────
print("Test 5: Confirming all agent dependencies...")
try:
    from rag_chain import get_rag_answer, format_sources
    print("  rag_chain          : OK ✅")
except ImportError as e:
    print(f"  rag_chain          : FAILED ❌ - {e}")
    failed += 1

try:
    from jira_tools import (
        create_ticket,
        get_ticket_status,
        get_ticket_by_id,
        format_tickets
    )
    print("  jira_tools         : OK ✅")
except ImportError as e:
    print(f"  jira_tools         : FAILED ❌ - {e}")
    failed += 1

try:
    from rag_config import LLM_MODEL
    print("  rag_config         : OK ✅")
    passed += 1
except ImportError as e:
    print(f"  rag_config         : FAILED ❌ - {e}")
    failed += 1

print()

# ── Final Summary ────────────────────────────────────────────────
print("=" * 60)
print("LANGGRAPH INSTALLATION TEST SUMMARY")
print("=" * 60)
print(f"  Tests passed : {passed} of 5")
print(f"  Tests failed : {failed} of 5")
print()

if failed == 0:
    print("All tests passed! ✅")
    print()
    print("LangGraph is installed and working correctly.")
    print("All agent dependencies are confirmed ready.")
    print()
    print("Ready to build the agent in Tasks 44 and 45.")
else:
    print("Some tests failed.")
    print("Review the FAIL results above.")
    print("Fix any issues before moving to Task 43.")
print()