"""
rag_setup.py
Handles loading Param's resume, chunking, embedding, and creating the Chroma vector store.
Run this once to build the vector DB, then reuse it in the app.
"""

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

VECTOR_DB_DIR = os.path.join(os.path.dirname(__file__), "vector_db")
RESUME_PATH = os.path.join(os.path.dirname(__file__), "data", "resume.pdf")
COLLECTION_NAME = "param_resume"


def build_vector_store(gemini_api_key: str) -> Chroma:
    """Load resume PDF, split into chunks, embed and store in Chroma."""
    print("📄 Loading resume PDF...")
    loader = PyPDFLoader(RESUME_PATH)
    docs = loader.load()

    print(f"✅ Loaded {len(docs)} page(s). Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks.")

    print("🔢 Creating embeddings with Gemini...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=gemini_api_key,
    )

    print("💾 Storing in ChromaDB...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR,
        collection_name=COLLECTION_NAME,
    )
    print("✅ Vector store built and persisted!")
    return vector_store


def load_vector_store(gemini_api_key: str) -> Chroma:
    """Load an existing Chroma vector store from disk."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=gemini_api_key,
    )
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=VECTOR_DB_DIR,
        collection_name=COLLECTION_NAME,
    )
    return vector_store


def get_or_build_vector_store(gemini_api_key: str) -> Chroma:
    """Return existing vector store if available, else build it."""
    chroma_data_path = os.path.join(VECTOR_DB_DIR, "chroma.sqlite3")
    if os.path.exists(chroma_data_path):
        print("📂 Found existing vector store. Loading...")
        return load_vector_store(gemini_api_key)
    else:
        print("🔨 No vector store found. Building from resume...")
        return build_vector_store(gemini_api_key)
