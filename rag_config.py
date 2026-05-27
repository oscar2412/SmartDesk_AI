# ── SmartDesk AI — RAG Configuration Settings ──────────────────
#
# These settings control how documents are chunked and searched.
# Change these values carefully — they affect answer quality.

# ── Chunking Settings ───────────────────────────────────────────
CHUNK_SIZE    = 1000   # Number of characters per chunk
CHUNK_OVERLAP = 200    # Characters shared between chunks

# ── Retrieval Settings ──────────────────────────────────────────
TOP_K_RESULTS = 3      # Number of chunks to retrieve per query

# ── Confidence Threshold ────────────────────────────────────────
# If the best match scores below this value the agent will
# escalate to ticket creation instead of attempting an answer
CONFIDENCE_THRESHOLD = 0.75

# ── Embedding Model ─────────────────────────────────────────────
EMBEDDING_MODEL = "text-embedding-3-small"

# ── LLM Model ───────────────────────────────────────────────────
LLM_MODEL = "gpt-4o-mini"

# ── ChromaDB Settings ───────────────────────────────────────────
CHROMA_DB_PATH        = "./chroma_db"
CHROMA_COLLECTION_NAME = "smartdesk_knowledge"