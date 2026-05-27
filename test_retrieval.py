# ── test_retrieval.py ────────────────────────────────────────────
# Tests that ChromaDB can retrieve the correct chunks
# for a given query. Run this after index_knowledge_base.py
# ────────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from rag_config import (
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K_RESULTS
)

# Load API keys
load_dotenv()

print("=" * 60)
print("SmartDesk AI — Retrieval Pipeline Test")
print("=" * 60)
print()

# ── Connect to ChromaDB ──────────────────────────────────────────
print("Connecting to ChromaDB...")
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

db = Chroma(
    persist_directory=CHROMA_DB_PATH,
    embedding_function=embeddings,
    collection_name=CHROMA_COLLECTION_NAME
)

total_chunks = db._collection.count()
print(f"Connected! Total chunks in database: {total_chunks}")
print()

# ── Test Queries ─────────────────────────────────────────────────
test_queries = [
    {
        "query"    : "How do I reset my password?",
        "category" : "IT Support",
        "expect"   : "password reset portal or steps"
    },
    {
        "query"    : "How do I set up VPN on Windows?",
        "category" : "IT Support",
        "expect"   : "VPN installation steps"
    },
    {
        "query"    : "How many casual leave days do I get?",
        "category" : "HR Policy",
        "expect"   : "number of casual leave days"
    },
    {
        "query"    : "What is the work from home policy?",
        "category" : "HR Policy",
        "expect"   : "work from home eligibility or rules"
    },
    {
        "query"    : "How do I set up MFA on my phone?",
        "category" : "IT Support",
        "expect"   : "MFA setup steps"
    }
]

# ── Run Each Test ────────────────────────────────────────────────
for i, test in enumerate(test_queries, 1):
    print(f"TEST {i} — {test['category']}")
    print(f"Query   : {test['query']}")
    print(f"Expects : {test['expect']}")
    print()

    # Search ChromaDB for top matching chunks
    results = db.similarity_search_with_score(
        test["query"],
        k=TOP_K_RESULTS
    )

    if results:
        print(f"  Found {len(results)} matching chunks:")
        for j, (doc, score) in enumerate(results, 1):
            # Convert distance to similarity percentage
            similarity = round((1 - score) * 100, 1)
            source = doc.metadata.get("source", "unknown")
            # Show first 200 characters of chunk
            preview = doc.page_content[:200].replace("\n", " ")
            print(f"  Match {j}:")
            print(f"    Score   : {similarity}% similar")
            print(f"    Source  : {source}")
            print(f"    Preview : {preview}...")
            print()
    else:
        print("  WARNING: No results found for this query!")
        print()

    print("-" * 60)
    print()

print("=" * 60)
print("RETRIEVAL TEST COMPLETE")
print("=" * 60)
print()
print("What to look for in the results above:")
print("  Good score   : 40% or higher similarity")
print("  Good source  : Points to the right KB file")
print("  Good preview : Shows relevant content for the query")
print()