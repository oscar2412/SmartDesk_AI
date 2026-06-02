import os
import json
import shutil
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

from src.rag.rag_config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
)

# Resolve knowledge_base path relative to this file's location
_kb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")

print("=" * 60)
print("SmartDesk AI — Knowledge Base Indexing Script")
print("=" * 60)
print()


# ── STEP 1: Load Markdown Documents ──────────────────────────────
print("Step 1: Loading markdown documents...")

markdown_files = [
    ("it_support_guide.md", "IT Support"),
    ("hr_leave_policy.md",  "HR Policy"),
]

markdown_docs = []
for filename, _ in markdown_files:
    filepath = os.path.join(_kb_dir, filename)
    source_key = f"knowledge_base/{filename}"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        doc = Document(
            page_content=content,
            metadata={"source": source_key, "type": "markdown"}
        )
        markdown_docs.append(doc)
        print(f"  Loaded: {source_key} ({len(content)} characters)")
    else:
        print(f"  WARNING: File not found - {filepath}")

print(f"  Total markdown documents loaded: {len(markdown_docs)}")
print()


# ── STEP 2: Load JSON Q&A Files ───────────────────────────────────
print("Step 2: Loading JSON Q&A files...")

json_files = [
    ("it_qa.json", "IT Support"),
    ("hr_qa.json", "HR Policy"),
]

json_docs = []
for filename, category in json_files:
    filepath   = os.path.join(_kb_dir, filename)
    source_key = f"knowledge_base/{filename}"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            qa_pairs = json.load(f)
        for pair in qa_pairs:
            content = (
                f"Question: {pair.get('question', '')}\n"
                f"Answer: {pair.get('answer', '')}\n"
                f"Category: {pair.get('category', category)}"
            )
            json_docs.append(Document(
                page_content=content,
                metadata={
                    "source"  : source_key,
                    "type"    : "qa_pair",
                    "category": pair.get("category", category)
                }
            ))
        print(f"  Loaded: {source_key} ({len(qa_pairs)} Q&A pairs)")
    else:
        print(f"  WARNING: File not found - {filepath}")

print(f"  Total Q&A documents loaded: {len(json_docs)}")
print()


# ── STEP 3: Load JSONL Dataset ────────────────────────────────────
print("Step 3: Loading JSONL dataset...")

jsonl_filename = "hr-policies-qa-dataset.jsonl"
jsonl_filepath = os.path.join(_kb_dir, jsonl_filename)
jsonl_source   = f"knowledge_base/{jsonl_filename}"
jsonl_docs     = []

if os.path.exists(jsonl_filepath):
    with open(jsonl_filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            if line:
                try:
                    entry    = json.loads(line)
                    question = entry.get("question") or entry.get("input") or entry.get("prompt") or ""
                    answer   = entry.get("answer") or entry.get("output") or entry.get("response") or ""
                    if question and answer:
                        jsonl_docs.append(Document(
                            page_content=f"Question: {question}\nAnswer: {answer}",
                            metadata={
                                "source": jsonl_source,
                                "type"  : "jsonl_entry",
                                "line"  : line_num + 1
                            }
                        ))
                except json.JSONDecodeError:
                    print(f"  Skipping invalid line {line_num + 1}")
    print(f"  Loaded: {jsonl_source} ({len(jsonl_docs)} entries)")
else:
    print(f"  WARNING: File not found - {jsonl_filepath}")

print(f"  Total JSONL documents loaded: {len(jsonl_docs)}")
print()


# ── STEP 4 & 5: Combine and Chunk ────────────────────────────────
print("Step 4: Combining all documents...")
all_docs = markdown_docs + json_docs + jsonl_docs
print(f"  Total documents before chunking: {len(all_docs)}")
print()

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


# ── STEP 6: Create Embeddings and Store in ChromaDB ──────────────
print("Step 6: Creating embeddings and storing in ChromaDB...")
print(f"  Embedding model : {EMBEDDING_MODEL}")
print(f"  Database path   : {CHROMA_DB_PATH}")
print(f"  Collection name : {CHROMA_COLLECTION_NAME}")
print()
print("  This may take 1 to 3 minutes. Please wait...")
print()

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

if os.path.exists(CHROMA_DB_PATH):
    shutil.rmtree(CHROMA_DB_PATH)
    print("  Cleared existing ChromaDB database.")

Chroma.from_documents(
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
print("You can now run the agent.")
print()
