# ── index_knowledge_base.py ─────────────────────────────────────
# This script reads all knowledge base files, chunks them,
# creates embeddings, and stores everything in ChromaDB.
# Run this script once before starting the agent.
# ────────────────────────────────────────────────────────────────
# ----------------------------------------------------------------------------------
# SECTION 1 — Imports and Setup
# Step 8. Click inside the blank index_knowledge_base.py file. Type this first section exactly:
#
import os
import json
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Load environment variables from .env file
load_dotenv()

# Import chunking settings from rag_config
from rag_config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME
)

print("=" * 60)
print("SmartDesk AI — Knowledge Base Indexing Script")
print("=" * 60)
print()


# ----------------------------------------------------------------------------------
# SECTION 2 — Load Markdown Files
# Step 9. Press Enter twice after the last line and type this next section:
# ── STEP 1: Load Markdown Documents ─────────────────────────────
#
print("Step 1: Loading markdown documents...")

markdown_files = [
    "knowledge_base/it_support_guide.md",
    "knowledge_base/hr_leave_policy.md"
]

markdown_docs = []
for filepath in markdown_files:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            doc = Document(
                page_content=content,
                metadata={"source": filepath, "type": "markdown"}
            )
            markdown_docs.append(doc)
            print(f"  Loaded: {filepath} ({len(content)} characters)")
    else:
        print(f"  WARNING: File not found - {filepath}")

print(f"  Total markdown documents loaded: {len(markdown_docs)}")
print()


# ----------------------------------------------------------------------------------
# SECTION 3 — Load JSON Q&A Files
#Step 10. Press Enter twice and type this next section:
#
# ── STEP 2: Load JSON Q&A Files ──────────────────────────────────
print("Step 2: Loading JSON Q&A files...")

json_files = [
    ("knowledge_base/it_qa.json",  "IT Support"),
    ("knowledge_base/hr_qa.json",  "HR Policy")
]

json_docs = []
for filepath, category in json_files:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            qa_pairs = json.load(f)
            for pair in qa_pairs:
                # Combine question and answer into one chunk
                content = (
                    f"Question: {pair.get('question', '')}\n"
                    f"Answer: {pair.get('answer', '')}\n"
                    f"Category: {pair.get('category', category)}"
                )
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": filepath,
                        "type": "qa_pair",
                        "category": pair.get("category", category)
                    }
                )
                json_docs.append(doc)
        print(f"  Loaded: {filepath} ({len(qa_pairs)} Q&A pairs)")
    else:
        print(f"  WARNING: File not found - {filepath}")

print(f"  Total Q&A documents loaded: {len(json_docs)}")
print()


# ----------------------------------------------------------------------------------
# SECTION 4 — Load the JSONL Dataset
# Step 11. Press Enter twice and type this next section:
#
# ── STEP 3: Load JSONL Dataset ───────────────────────────────────
print("Step 3: Loading JSONL dataset...")

jsonl_file = "knowledge_base/hr-policies-qa-dataset.jsonl"
jsonl_docs = []

if os.path.exists(jsonl_file):
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            if line:
                try:
                    entry = json.loads(line)
                    # Handle different possible field names
                    question = (
                        entry.get("question") or
                        entry.get("input") or
                        entry.get("prompt") or
                        ""
                    )
                    answer = (
                        entry.get("answer") or
                        entry.get("output") or
                        entry.get("response") or
                        ""
                    )
                    if question and answer:
                        content = (
                            f"Question: {question}\n"
                            f"Answer: {answer}"
                        )
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": jsonl_file,
                                "type": "jsonl_entry",
                                "line": line_num + 1
                            }
                        )
                        jsonl_docs.append(doc)
                except json.JSONDecodeError:
                    print(f"  Skipping invalid line {line_num + 1}")
    print(f"  Loaded: {jsonl_file} ({len(jsonl_docs)} entries)")
else:
    print(f"  WARNING: File not found - {jsonl_file}")

print(f"  Total JSONL documents loaded: {len(jsonl_docs)}")
print()


# ----------------------------------------------------------------------------------
# SECTION 5 — Combine and Chunk All Documents
# Step 12. Press Enter twice and type this next section:
#
# ── STEP 4: Combine All Documents ───────────────────────────────
print("Step 4: Combining all documents...")

all_docs = markdown_docs + json_docs + jsonl_docs
print(f"  Total documents before chunking: {len(all_docs)}")
print()

# ── STEP 5: Chunk the Documents ──────────────────────────────────
print("Step 5: Chunking documents...")
print(f"  Chunk size    : {CHUNK_SIZE} characters")
print(f"  Chunk overlap : {CHUNK_OVERLAP} characters")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunked_docs = text_splitter.split_documents(all_docs)
print(f"  Total chunks created: {len(chunked_docs)}")
print()


# ----------------------------------------------------------------------------------
# SECTION 6 — Create Embeddings and Store in ChromaDB
# Step 13. Press Enter twice and type this final section:
#
# ── STEP 6: Create Embeddings and Store in ChromaDB ─────────────
print("Step 6: Creating embeddings and storing in ChromaDB...")
print(f"  Embedding model : {EMBEDDING_MODEL}")
print(f"  Database path   : {CHROMA_DB_PATH}")
print(f"  Collection name : {CHROMA_COLLECTION_NAME}")
print()
print("  This may take 1 to 3 minutes depending on")
print("  the number of chunks. Please wait...")
print()

# Set up the OpenAI embeddings
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Delete existing ChromaDB if it exists so we start fresh
import shutil
if os.path.exists(CHROMA_DB_PATH):
    shutil.rmtree(CHROMA_DB_PATH)
    print("  Cleared existing ChromaDB database.")

# Create ChromaDB and store all chunks
vectorstore = Chroma.from_documents(
    documents=chunked_docs,
    embedding=embeddings,
    persist_directory=CHROMA_DB_PATH,
    collection_name=CHROMA_COLLECTION_NAME
)

print()
print("=" * 60)
print("INDEXING COMPLETE!")
print("=" * 60)
print()
print(f"  Total chunks indexed : {len(chunked_docs)}")
print(f"  Database location    : {CHROMA_DB_PATH}")
print()
print("Your knowledge base is ready.")
print("You can now run the RAG pipeline.")
print()