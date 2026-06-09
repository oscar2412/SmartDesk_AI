"""
SmartDesk AI — RAG Configuration Settings.

Central configuration file for all RAG pipeline settings
including chunking strategy, embedding model, and ChromaDB
connection details. Change values here to tune performance.
"""

# ── Chunking Settings ────────────────────────────────────────────
CHUNK_SIZE    = 800    # Number of characters per chunk
CHUNK_OVERLAP = 150    # Characters shared between chunks

# ── Retrieval Settings ───────────────────────────────────────────
TOP_K_RESULTS = 3      # Number of chunks to retrieve per query

# ── Confidence Threshold ─────────────────────────────────────────
# If the best match scores below this value the agent will
# escalate to ticket creation instead of attempting an answer
CONFIDENCE_THRESHOLD = 0.15

# ── Embedding Model ──────────────────────────────────────────────
EMBEDDING_MODEL = "text-embedding-3-small"

# ── LLM Model ────────────────────────────────────────────────────
LLM_MODEL = "gpt-4o-mini"

# ── ChromaDB Settings ────────────────────────────────────────────
CHROMA_DB_PATH         = "./chroma_db"
CHROMA_COLLECTION_NAME = "smartdesk_knowledge"
