"""
core/document.py
────────────────
Document indexing, embedding, QA, and LLM utilities.

Requires ONLY what is actually installed in a standard studywise venv:
  - groq              (LLM calls)
  - huggingface_hub   (embeddings via HF Inference API — no local model needed)
  - faiss-cpu         (vector store)
  - pypdf             (PDF parsing)
  - langchain_core    (Document dataclass only)
  - numpy

NO langchain, langchain-community, langchain-text-splitters, or
sentence-transformers required.
"""

from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
import streamlit as st
from groq import Groq
from huggingface_hub import InferenceClient

# ── Try to import faiss (cpu or gpu) ─────────────────────────────────────────
try:
    import faiss
except ImportError as exc:
    raise ImportError("faiss-cpu is not installed. Run: pip install faiss-cpu") from exc

# ── Constants ─────────────────────────────────────────────────────────────────
EMBED_MODEL   = "sentence-transformers/all-MiniLM-L6-v2"   # served free on HF
GROQ_MODEL    = "llama-3.3-70b-versatile"   # llama3-8b-8192 was decommissioned June 2025
CHUNK_SIZE    = 600     # characters
CHUNK_OVERLAP = 80


def _resolve_groq_key(key: str) -> str:
    if key:
        return key
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY", "")

def _resolve_hf_token(token: str) -> str:
    if token:
        return token
    try:
        return st.secrets["HF_TOKEN"]
    except Exception:
        return os.getenv("HF_TOKEN", "")
# ═══════════════════════════════════════════════════════════════════
# Lightweight Document dataclass (replaces langchain Document)
# ═══════════════════════════════════════════════════════════════════
class Doc:
    """Minimal stand-in for langchain_core Document."""
    __slots__ = ("page_content", "metadata")

    def __init__(self, page_content: str, metadata: dict | None = None):
        self.page_content = page_content
        self.metadata = metadata or {}


# ═══════════════════════════════════════════════════════════════════
# Text splitter (replaces RecursiveCharacterTextSplitter)
# ═══════════════════════════════════════════════════════════════════
def _split_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks without any LangChain dependency."""
    separators = ["\n\n", "\n", ". ", " ", ""]
    chunks: list[str] = []

    def _split(txt: str, seps: list[str]) -> list[str]:
        if not txt:
            return []
        if len(txt) <= chunk_size:
            return [txt]
        sep = seps[0] if seps else ""
        parts = txt.split(sep) if sep else list(txt)
        result: list[str] = []
        current = ""
        for part in parts:
            candidate = (current + sep + part).lstrip() if current else part
            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    result.append(current)
                # If single part is too long, recurse with next separator
                if len(part) > chunk_size and len(seps) > 1:
                    result.extend(_split(part, seps[1:]))
                    current = ""
                else:
                    current = part
        if current:
            result.append(current)
        return result

    raw = _split(text, separators)

    # Apply overlap: each chunk starts `overlap` chars before the previous ended
    for i, chunk in enumerate(raw):
        if i == 0:
            chunks.append(chunk)
        else:
            prev = chunks[-1]
            tail = prev[-overlap:] if len(prev) >= overlap else prev
            chunks.append((tail + " " + chunk).strip())

    return [c for c in chunks if c.strip()]


# ═══════════════════════════════════════════════════════════════════
# PDF / TXT loader (replaces PyPDFLoader / TextLoader)
# ═══════════════════════════════════════════════════════════════════
def _load_file(path: str, suffix: str) -> list[Doc]:
    """Return a list of Doc objects, one per page (PDF) or one total (TXT)."""
    if suffix == ".pdf":
        import pypdf
        docs: list[Doc] = []
        reader = pypdf.PdfReader(path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                docs.append(Doc(text, {"page": i + 1, "source": path}))
        return docs
    else:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        return [Doc(text, {"page": 1, "source": path})]


# ═══════════════════════════════════════════════════════════════════
# Embeddings via HuggingFace Inference API
# ═══════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def _get_hf_client(hf_token: str) -> InferenceClient:
    """Return a cached HuggingFace InferenceClient authenticated with the user's token."""
    return InferenceClient(token=hf_token)


def embed_texts(texts: list[str], hf_token: str) -> np.ndarray:
    """
    Embed a list of strings using HuggingFace Inference API.
    Returns float32 array of shape (N, dim).
    """
    client = _get_hf_client(hf_token)
    BATCH = 32
    vectors: list[np.ndarray] = []
    for i in range(0, len(texts), BATCH):
        batch = texts[i : i + BATCH]
        result = client.feature_extraction(batch, model=EMBED_MODEL, normalize=True)
        arr = np.array(result, dtype=np.float32)
        # shape might be (N, seq_len, dim) — mean-pool if so
        if arr.ndim == 3:
            arr = arr.mean(axis=1)
        vectors.append(arr)
    return np.vstack(vectors)


# ═══════════════════════════════════════════════════════════════════
# FAISS vector store wrapper
# ═══════════════════════════════════════════════════════════════════
class VectorStore:
    """Thin FAISS wrapper that stores Doc objects alongside their vectors."""

    def __init__(self, docs: list[Doc], vectors: np.ndarray, hf_token: str):
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatIP(dim)   # inner product ≈ cosine on L2-normalised vecs
        self.index.add(vectors)
        self.docs = docs
        self.hf_token = hf_token              # kept so similarity_search can embed queries

    def similarity_search(self, query: str, k: int = 4) -> list[Doc]:
        q_vec = embed_texts([query], self.hf_token)   # (1, dim)
        faiss.normalize_L2(q_vec)
        _, idxs = self.index.search(q_vec, k)
        return [self.docs[i] for i in idxs[0] if i < len(self.docs)]


# ═══════════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════════

def index_document(file, hf_token: str) -> tuple[VectorStore, int, int]:
    """
    Load a PDF or TXT upload, chunk it, embed, and return a VectorStore.
    Returns (vectorstore, num_chunks, num_pages).
    """
    hf_token = _resolve_hf_token(hf_token)
    suffix = Path(file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.read())
        path = tmp.name

    try:
        page_docs = _load_file(path, suffix)
        n_pages = len(page_docs)
    finally:
        os.unlink(path)

    # Split each page into chunks
    chunks: list[Doc] = []
    for doc in page_docs:
        for chunk_text in _split_text(doc.page_content):
            chunks.append(Doc(chunk_text, doc.metadata.copy()))

    # Embed all chunks using the authenticated HF client
    texts = [c.page_content for c in chunks]
    vectors = embed_texts(texts, hf_token)
    faiss.normalize_L2(vectors)

    vs = VectorStore(chunks, vectors, hf_token)
    return vs, len(chunks), n_pages


def build_qa_chain(vs: VectorStore, key: str) -> dict:
    """
    Return a lightweight 'chain' dict that render_ask_tab can call.
    We store the vectorstore and key so ask() can do retrieval + LLM.
    """
    key = _resolve_groq_key(key)
    return {"vs": vs, "key": key}


def ask(chain: dict, query: str) -> dict:
    """
    Retrieve relevant chunks then answer with Groq LLM.
    Returns {"result": str, "source_documents": list[Doc]}.
    """
    vs: VectorStore = chain["vs"]
    key: str = chain["key"]

    source_docs = vs.similarity_search(query, k=4)
    context = "\n\n---\n\n".join(d.page_content for d in source_docs)

    system = (
        "You are StudyWise, a helpful study assistant. "
        "Answer ONLY using the provided context. "
        "If you cannot find the answer, say so clearly — never guess. "
        "If relevant, mention the page or section the answer comes from."
    )
    user = f"Context:\n{context}\n\nStudent's question: {query}"

    client = Groq(api_key=key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
        max_tokens=1200,
    )
    answer = response.choices[0].message.content
    return {"result": answer, "source_documents": source_docs}


def llm_call(key: str, prompt: str) -> str:
    """Direct Groq LLM call — used for quiz, summary, and flashcard generation."""
    client = Groq(api_key=key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1200,
    )
    return response.choices[0].message.content


def get_doc_sample(vs: VectorStore, n: int = 6) -> str:
    """Pull a representative text sample from the vector store."""
    docs = vs.similarity_search("main concepts topics summary overview", k=n)
    return "\n\n---\n\n".join(d.page_content for d in docs)