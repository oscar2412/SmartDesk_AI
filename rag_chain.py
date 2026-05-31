# ── rag_chain.py ─────────────────────────────────────────────────
# The RAG answer generation function.
# Takes a user query, retrieves relevant chunks from ChromaDB,
# sends them to GPT with a strict system prompt, and returns
# a grounded professional answer.
#
# This module is imported by agent.py in Task 45.
# ────────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv
from langchain_core import chat_history
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from retrieval_with_threshold import (
    retrieve_with_threshold,
    RESULT_FOUND,
    RESULT_NOT_FOUND
)
from rag_config import LLM_MODEL

# Load environment variables
load_dotenv()

# ── Result Types ─────────────────────────────────────────────────
ANSWER_FOUND     = "ANSWER_FOUND"      # Answer generated from KB
ANSWER_NOT_FOUND = "ANSWER_NOT_FOUND"  # No answer — escalate


# ── System Prompt ────────────────────────────────────────────────
# This is the instruction given to GPT before every query.
# It strictly controls GPT behavior to prevent hallucination.

SYSTEM_PROMPT = """
You are SmartDesk AI, a helpful and professional IT and HR
support assistant for Roadmap Consulting.

Your job is to answer employee questions clearly and accurately.

STRICT RULES YOU MUST FOLLOW:
1. Only use information from the CONTEXT provided below.
   Never use your own training knowledge to answer.
2. If the CONTEXT does not contain enough information to
   answer the question, respond with exactly this phrase:
   "I don't have enough information about that in my
   knowledge base."
3. Never make up URLs, phone numbers, email addresses,
   or policy details that are not in the CONTEXT.
4. Always be polite, professional, and concise.
5. If steps are involved always number them clearly.
6. End every answer by asking if there is anything else
   you can help with.

CONTEXT:
{context}
"""


# ── Main RAG Function ────────────────────────────────────────────

def get_rag_answer(query: str, chat_history: list = None) -> dict:
    """
    Main RAG function. Takes a query and returns a
    grounded answer from the knowledge base.

    Returns a dictionary with:
        status   : ANSWER_FOUND or ANSWER_NOT_FOUND
        answer   : the generated answer text
        query    : the original query
        sources  : list of source files used
        reason   : explanation of the result
    """

    # Step 1 — Retrieve relevant chunks with threshold check
    retrieval_result = retrieve_with_threshold(query)

    # Step 2 — If no good chunks found return NOT_FOUND
    if retrieval_result["status"] == RESULT_NOT_FOUND:
        return {
            "status" : ANSWER_NOT_FOUND,
            "answer" : (
                "I don't have enough information about that "
                "in my knowledge base."
            ),
            "query"  : query,
            "sources": [],
            "reason" : retrieval_result["reason"]
        }

    # Step 3 — Build context from retrieved chunks
    chunks = retrieval_result["chunks"]
    context_parts = []
    sources = []

    for chunk in chunks:
        context_parts.append(chunk.page_content)
        source = chunk.metadata.get("source", "unknown")
        if source not in sources:
            sources.append(source)

    context = "\n\n---\n\n".join(context_parts)

    # Step 4 — Build the prompt with context injected
    system_message = SystemMessage(
        content=SYSTEM_PROMPT.format(context=context)
    )
    human_message = HumanMessage(content=query)

    # Step 5 — Call GPT to generate a grounded answer
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    messages = [system_message]
    if chat_history:
        messages.extend(chat_history)
        messages.append(human_message)
        response = llm.invoke(messages)
    answer = response.content.strip()

    # Step 6 — Check if GPT admitted it did not know
    not_found_phrase = "I don't have enough information"
    if not_found_phrase in answer:
        return {
            "status" : ANSWER_NOT_FOUND,
            "answer" : answer,
            "query"  : query,
            "sources": sources,
            "reason" : "GPT could not find sufficient info in context."
        }

    # Step 7 — Return the successful answer
    return {
        "status" : ANSWER_FOUND,
        "answer" : answer,
        "query"  : query,
        "sources": sources,
        "reason" : "Answer generated from knowledge base."
    }


# ── Quick Self Test ──────────────────────────────────────────────
# Only runs when you execute this file directly.
# Does not run when imported by agent.py.

if __name__ == "__main__":
    print("=" * 60)
    print("RAG Chain Quick Test")
    print("=" * 60)
    print()

    test_query = "How do I reset my password?"
    print(f"Test query: {test_query}")
    print()

    result = get_rag_answer(test_query)

    print(f"Status  : {result['status']}")
    print(f"Sources : {result['sources']}")
    print()
    print("Answer:")
    print("-" * 40)
    print(result['answer'])
    print("-" * 40)
    print()


def format_sources(sources: list) -> str:
    """
    Formats a list of source file paths into a
    clean readable string for display.

    Example output:
        Sources: IT Support Guide, HR Leave Policy
    """
    if not sources:
        return ""

    # Convert file paths to readable names
    name_map = {
        "knowledge_base/it_support_guide.md"        : "IT Support Guide",
        "knowledge_base/hr_leave_policy.md"          : "HR Leave Policy",
        "knowledge_base/it_qa.json"                  : "IT Q&A Database",
        "knowledge_base/hr_qa.json"                  : "HR Q&A Database",
        "knowledge_base/hr-policies-qa-dataset.jsonl": "HR Policies Dataset"
    }

    readable_names = []
    for source in sources:
        name = name_map.get(source, source)
        if name not in readable_names:
            readable_names.append(name)

    return "Sources: " + ", ".join(readable_names)    