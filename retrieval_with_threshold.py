# ── retrieval_with_threshold.py ──────────────────────────────────
# Retrieval function with confidence threshold logic.
# Returns chunks if score is above threshold.
# Returns escalation flag if score is below threshold.
# This module is imported by rag_chain.py in Task 34.
# ────────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from rag_config import (
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K_RESULTS,
    CONFIDENCE_THRESHOLD
)

# Load environment variables
load_dotenv()

# ── Result Types ─────────────────────────────────────────────────
RESULT_FOUND     = "FOUND"
RESULT_NOT_FOUND = "NOT_FOUND"

# ── Connect to ChromaDB Once at Module Load ───────────────────────
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

db = Chroma(
    persist_directory=CHROMA_DB_PATH,
    embedding_function=embeddings,
    collection_name=CHROMA_COLLECTION_NAME
)


def retrieve_with_threshold(query: str) -> dict:
    """
    Search ChromaDB for chunks relevant to the query.
    Apply confidence threshold to decide if answer is possible.

    Returns a dictionary with:
        status  : FOUND or NOT_FOUND
        chunks  : list of relevant document chunks if FOUND
        scores  : list of similarity scores
        query   : the original query
        reason  : explanation of the result
    """

    try:
        # Search ChromaDB for top K results with scores
        results = db.similarity_search_with_score(
            query,
            k=TOP_K_RESULTS
        )

        if not results:
            return {
                "status" : RESULT_NOT_FOUND,
                "chunks" : [],
                "scores" : [],
                "query"  : query,
                "reason" : "ChromaDB returned no results at all."
            }

        # Get the best score from the top result
        best_score = 1 - results[0][1]

        # Apply the confidence threshold check
        if best_score < CONFIDENCE_THRESHOLD:
            return {
                "status" : RESULT_NOT_FOUND,
                "chunks" : [],
                "scores" : [round((1 - r[1]) * 100, 1) for r in results],
                "query"  : query,
                "reason" : (
                    f"Best match score {round(best_score * 100, 1)}% "
                    f"is below threshold of "
                    f"{round(CONFIDENCE_THRESHOLD * 100, 1)}%."
                )
            }

        # Threshold passed — return the relevant chunks
        chunks = [doc for doc, score in results]
        scores = [round((1 - score) * 100, 1) for doc, score in results]

        return {
            "status" : RESULT_FOUND,
            "chunks" : chunks,
            "scores" : scores,
            "query"  : query,
            "reason" : (
                f"Best match score {round(best_score * 100, 1)}% "
                f"is above threshold of "
                f"{round(CONFIDENCE_THRESHOLD * 100, 1)}%."
            )
        }

    except Exception as e:
        # ChromaDB connection error or embedding failure
        return {
            "status" : RESULT_NOT_FOUND,
            "chunks" : [],
            "scores" : [],
            "query"  : query,
            "reason" : f"ChromaDB error: {str(e)}"
        }