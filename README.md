# 📚 StudyWise — AI Study Companion

> Upload any PDF. Walk out with mastery.

StudyWise transforms static study material (textbook chapters, lecture slides, past papers) into a **fully interactive study session** using Retrieval-Augmented Generation, HuggingFace embeddings, and an LLM backbone.

---

## ✨ Features

### 💬 Ask — RAG-Powered Q&A
Ask natural language questions, get answers grounded directly in your document with page-level source citations. Uses MMR retrieval to surface diverse, relevant chunks rather than repetitive context.

### 🧠 Quiz Me — AI-Generated MCQs
Configure topic focus, question count (3–10), and difficulty. The LLM generates contextually accurate multiple-choice questions from the document. Answer interactively, submit, and get instant feedback with explanations for every question.

### 📝 Summarise — Structured Overview
Generates a hierarchical summary (Quick / Standard / Detailed) with:
- High-level overview paragraph
- Section-by-section breakdown
- Key concepts extracted as visual tags
- Likely exam points flagged explicitly

### 🃏 Flashcards — Active Recall Review
Choose card type (Term→Definition, Concept→Explanation, Question→Answer), generate a deck, flip through cards, shuffle, and track progress. Designed around spaced repetition principles.

---

## 🏗️ Architecture

```
PDF / TXT Upload
      │
      ▼
[PyPDF Loader]  →  raw document pages
      │
      ▼
[RecursiveCharacterTextSplitter]
  chunk_size=600, overlap=80
      │  N chunks
      ▼
[HuggingFace sentence-transformers/all-MiniLM-L6-v2]
  384-dim dense embeddings
      │
      ▼
[FAISS Vector Index]
  cosine similarity, in-memory
      │
  ┌───┴────────────────────────────────────┐
  │  MMR Retrieval (k=4, fetch_k=10)       │
  │  "maximum marginal relevance"          │
  │  balances relevance + diversity        │
  └───┬────────────────────────────────────┘
      │  top-k chunks
      ▼
[LangChain RetrievalQA Chain]             [Direct LLM Calls]
  grounded Q&A with citations       ←→    quiz / summary / flashcards
      │
      ▼
[Groq LLaMA-3 8B]  ·  free API  ·  fast inference
      │
      ▼
[Streamlit UI]  ·  4 study tools  ·  responsive dark theme
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Document loading | LangChain PyPDFLoader | Parse PDFs page-by-page |
| Chunking | RecursiveCharacterTextSplitter | Semantic boundary-aware splitting |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` | Local 384-dim dense embeddings |
| Vector store | FAISS (CPU) | Sub-millisecond similarity search |
| Retrieval | LangChain MMR Retriever | Diverse, relevant context selection |
| LLM | LLaMA-3 8B via Groq | Fast, free text generation |
| Orchestration | LangChain | Composable pipeline architecture |
| UI | Streamlit | Reactive Python web app |

---

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone https://github.com/yourusername/studywise
cd studywise
pip install -r requirements.txt

# 2. Get a free Groq API key
#    → https://console.groq.com  (free tier, no credit card)

# 3. Run
streamlit run app.py
```

Open http://localhost:8501, enter your Groq key in the sidebar, upload a PDF, and start studying.

---

## 📂 Project Structure

```
# 📚 StudyWise — AI Study Companion

> Upload any PDF. Walk out with mastery.

StudyWise transforms static study material (textbook chapters, lecture slides, past papers) into a **fully interactive study session** using Retrieval-Augmented Generation, HuggingFace embeddings, and an LLM backbone.

---

## ✨ Features

### 💬 Ask — RAG-Powered Q&A
Ask natural language questions, get answers grounded directly in your document with page-level source citations. Uses MMR retrieval to surface diverse, relevant chunks rather than repetitive context.

### 🧠 Quiz Me — AI-Generated MCQs
Configure topic focus, question count (3–10), and difficulty. The LLM generates contextually accurate multiple-choice questions from the document. Answer interactively, submit, and get instant feedback with explanations for every question.

### 📝 Summarise — Structured Overview
Generates a hierarchical summary (Quick / Standard / Detailed) with:
- High-level overview paragraph
- Section-by-section breakdown
- Key concepts extracted as visual tags
- Likely exam points flagged explicitly

### 🃏 Flashcards — Active Recall Review
Choose card type (Term→Definition, Concept→Explanation, Question→Answer), generate a deck, flip through cards, shuffle, and track progress. Designed around spaced repetition principles.

---

## 🏗️ Architecture

```
PDF / TXT Upload
      │
      ▼
[PyPDF Loader]  →  raw document pages
      │
      ▼
[RecursiveCharacterTextSplitter]
  chunk_size=600, overlap=80
      │  N chunks
      ▼
[HuggingFace sentence-transformers/all-MiniLM-L6-v2]
  384-dim dense embeddings
      │
      ▼
[FAISS Vector Index]
  cosine similarity, in-memory
      │
  ┌───┴────────────────────────────────────┐
  │  MMR Retrieval (k=4, fetch_k=10)       │
  │  "maximum marginal relevance"          │
  │  balances relevance + diversity        │
  └───┬────────────────────────────────────┘
      │  top-k chunks
      ▼
[LangChain RetrievalQA Chain]             [Direct LLM Calls]
  grounded Q&A with citations       ←→    quiz / summary / flashcards
      │
      ▼
[Groq LLaMA-3 8B]  ·  free API  ·  fast inference
      │
      ▼
[Streamlit UI]  ·  4 study tools  ·  responsive dark theme
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Document loading | LangChain PyPDFLoader | Parse PDFs page-by-page |
| Chunking | RecursiveCharacterTextSplitter | Semantic boundary-aware splitting |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` | Local 384-dim dense embeddings |
| Vector store | FAISS (CPU) | Sub-millisecond similarity search |
| Retrieval | LangChain MMR Retriever | Diverse, relevant context selection |
| LLM | LLaMA-3 8B via Groq | Fast, free text generation |
| Orchestration | LangChain | Composable pipeline architecture |
| UI | Streamlit | Reactive Python web app |

---

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone https://github.com/yourusername/studywise
cd studywise
pip install -r requirements.txt

# 2. Get a free Groq API key
#    → https://console.groq.com  (free tier, no credit card)

# 3. Run
streamlit run app.py
```

Open http://localhost:8501, enter your Groq key in the sidebar, upload a PDF, and start studying.

---

## 📂 Project Structure

```
studywise/
├── app.py                  ← entry point  →  streamlit run app.py
├── requirements.txt
├── core/
│   └── document.py         ← indexing, embeddings, QA chain, LLM utils
├── ui/
│   ├── styles.py           ← all CSS (inject_css)
│   ├── sidebar.py          ← API key, file upload, stats
│   └── landing.py          ← onboarding screen
└── tools/
    ├── ask.py              ← Tab 1: RAG Q&A
    ├── quiz.py             ← Tab 2: MCQ quiz
    ├── summarise.py        ← Tab 3: structured summary
    └── flashcards.py       ← Tab 4: flip-card review
<<<<<<< HEAD
=======
```

---

## 📸 Screenshots

| Tool | Description |
|---|---|
| Landing | Feature overview before document upload |
| Ask | Chat interface with source pill citations |
| Quiz Me | Interactive MCQ with live scoring |
| Summarise | Structured summary + key concept tags |
| Flashcards | Flip-card review with progress bar |

---

## 🔑 Key AI/ML Concepts Demonstrated

**RAG (Retrieval-Augmented Generation)**
Combining retrieval (FAISS + embeddings) with generation (LLM) to produce factual, grounded answers — solving the hallucination problem inherent to pure LLM generation.

**Dense Retrieval**
Using transformer-based embeddings (`sentence-transformers`) to encode semantic meaning, enabling similarity search that understands intent rather than just keyword overlap.

**MMR (Maximal Marginal Relevance)**
A retrieval strategy that penalizes redundancy — selects chunks that are both relevant to the query AND diverse from each other, giving the LLM richer context.

**Prompt Engineering**
Structured prompts with role definition, strict grounding instructions, and JSON output schemas for quiz/flashcard/summary generation — controlling LLM behavior precisely.

**LangChain Orchestration**
Modular pipeline: loader → splitter → embedder → vector store → retriever → LLM chain. Each component is swappable (e.g. swap FAISS for Pinecone, Groq for OpenAI).

---

## 🔧 Extending the Project

- **Persistent vector stores** — swap FAISS for ChromaDB or Pinecone for cross-session memory
- **Multi-document support** — merge multiple PDFs into one index for comprehensive study sets
- **Spaced repetition** — track flashcard performance, surface weak cards more often (SM-2 algorithm)
- **Exam simulation** — timed quiz mode with past-paper style questions
- **Voice input** — integrate Whisper for spoken questions
- **Export** — generate a printable PDF of the summary + flashcards

---

## 🎯 Use Cases

- University students revising lecture slides and textbook chapters
- Exam preparation from past papers
- Professionals onboarding with dense documentation
- Researchers getting quick answers from papers

>>>>>>> ca008f602fd1999f32951df718cdced789eaeba0
```

---

## 📸 Screenshots

| Tool | Description |
|---|---|
| Landing | Feature overview before document upload |
| Ask | Chat interface with source pill citations |
| Quiz Me | Interactive MCQ with live scoring |
| Summarise | Structured summary + key concept tags |
| Flashcards | Flip-card review with progress bar |

---

## 🔑 Key AI/ML Concepts Demonstrated

**RAG (Retrieval-Augmented Generation)**
Combining retrieval (FAISS + embeddings) with generation (LLM) to produce factual, grounded answers — solving the hallucination problem inherent to pure LLM generation.

**Dense Retrieval**
Using transformer-based embeddings (`sentence-transformers`) to encode semantic meaning, enabling similarity search that understands intent rather than just keyword overlap.

**MMR (Maximal Marginal Relevance)**
A retrieval strategy that penalizes redundancy — selects chunks that are both relevant to the query AND diverse from each other, giving the LLM richer context.

**Prompt Engineering**
Structured prompts with role definition, strict grounding instructions, and JSON output schemas for quiz/flashcard/summary generation — controlling LLM behavior precisely.

**LangChain Orchestration**
Modular pipeline: loader → splitter → embedder → vector store → retriever → LLM chain. Each component is swappable (e.g. swap FAISS for Pinecone, Groq for OpenAI).

---

## 🔧 Extending the Project

- **Persistent vector stores** — swap FAISS for ChromaDB or Pinecone for cross-session memory
- **Multi-document support** — merge multiple PDFs into one index for comprehensive study sets
- **Spaced repetition** — track flashcard performance, surface weak cards more often (SM-2 algorithm)
- **Exam simulation** — timed quiz mode with past-paper style questions
- **Voice input** — integrate Whisper for spoken questions
- **Export** — generate a printable PDF of the summary + flashcards

---

## 🎯 Use Cases

- University students revising lecture slides and textbook chapters
- Exam preparation from past papers
- Professionals onboarding with dense documentation
- Researchers getting quick answers from papers
