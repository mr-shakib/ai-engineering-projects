# Hallucination-Resistant Retrieval-Augmented AI Assistant

## Overview

Large Language Models (LLMs) are powerful but unreliable when used without constraints. A major failure mode is **hallucination** — confidently generating incorrect or unsupported information.

This project implements a **hallucination-resistant Retrieval-Augmented Generation (RAG) system** that answers **only when sufficient evidence exists** in the provided documents and **explicitly refuses** otherwise.

This is **not a chatbot**. It is a **trust-aware AI system** designed with real-world reliability in mind.

---

## Problem Statement

Most AI demos:

* Answer every question, even when evidence is missing
* Sound confident while being wrong
* Provide no traceability to source data

In production environments (enterprise AI, healthcare, legal, finance), this behavior is unacceptable.

**Goal:** Build an AI assistant that:

* Uses retrieved documents as the *only* source of truth
* Measures retrieval confidence before answering
* Refuses to answer when confidence is low
* Always provides source-backed responses

---

## Key Features

* 📄 PDF & text document ingestion
* ✂️ Intelligent document chunking with overlap
* 🔢 Sentence-transformer embeddings
* ⚡ FAISS-based vector similarity search
* 🧠 Confidence-based decision gate
* 🚫 Explicit refusal when evidence is insufficient
* 📚 Evidence-grounded answer generation
* 🖥️ **Modern Web Interface**: Glassmorphism UI with Dark Mode

---

## System Architecture

```
User Question
      ↓
Question Embedding
      ↓
FAISS Vector Search (Top-K)
      ↓
Confidence Scoring
      ↓
Decision Gate
   ┌───────────────┐
   │ Enough Context?│
   └──────┬────────┘
          │
   Yes ───┘        No
    ↓               ↓
LLM Answer     Refusal Response
(with sources)
```

The **decision gate** is the core innovation of this system.

---

## Tech Stack

* **Language:** Python 3.10+
* **Embeddings:** SentenceTransformers (`all-MiniLM-L6-v2`)
* **Backend:** FastAPI + Uvicorn
* **Frontend:** Vanilla HTML/CSS/JS (Glassmorphism Design)
* **Vector Database:** FAISS (CPU)
* **Document Parsing:** pdfplumber
* **Numerical Computing:** NumPy
* **Environment:** Conda / virtualenv
* **Version Control:** Git + GitHub

---

## Project Structure

```
hallucination-resistant-rag/
│
├── data/
│   └── documents/        # Input PDFs / text files
│
├── embeddings/            # Stored vector embeddings
│
├── src/
│   ├── ingest.py          # Document ingestion
│   ├── chunk.py           # Text chunking logic
│   ├── embed.py           # Embedding generation
│   ├── retrieve.py        # FAISS indexing & search
│   ├── decision.py        # Confidence scoring & refusal
│   ├── generate.py        # Answer generation
│   ├── api.py             # FastAPI backend
│   └── main.py            # End-to-end pipeline
│
├── web/                   # Frontend UI
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── README.md
└── .env
```

This modular structure reflects production-ready engineering practices.

---

## How Hallucinations Are Prevented

This system **does not rely on prompt instructions alone**.

Hallucination prevention is enforced at the **system level**:

1. All answers must originate from retrieved document chunks
2. Retrieval similarity scores are evaluated
3. A confidence threshold is applied
4. If confidence is below threshold → the system refuses to answer

Refusal is treated as a **feature**, not a failure.

---

## Setup Instructions

### 1. Create Environment

```bash
conda create -n hallucination-rag python=3.10
conda activate hallucination-rag
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
conda install -c conda-forge faiss-cpu
```

### 3. Configure LLM Access

This system requires access to an LLM API (e.g., OpenAI, Anthropic, or local models).
Configure your API keys in environment variables or `.env` file.

---

## Running the System

### Option 1: Command Line Interface (CLI)

```bash
python src/main.py "Your question here"
```

### Option 2: Beautiful Web Interface with PDF Upload 🌟

The web interface allows users to upload their own PDFs and ask questions based on those documents in real-time.

#### Features:
- 📤 **PDF Upload**: Upload single or multiple PDF files
- 💬 **Interactive Q&A**: Ask questions about your uploaded documents
- 🔄 **Session Management**: Add more PDFs to the same session or start fresh
- 📁 **File Tracking**: View all uploaded files in the current session
- 🎨 **Modern UI**: Glassmorphism design with dark mode
- ⚡ **Real-time**: Instant processing with typing indicators
- 🚫 **Hallucination-Resistant**: Explicit refusal when evidence is insufficient

#### How to Use:

1. **Start the API Backend:**

   ```bash
   cd projects/hallucination-resistant-rag
   uvicorn src.api:app --reload
   ```

   The API will be available at `http://localhost:8000`

2. **Open the Web Interface:**

   Open `web/index.html` in your browser, or visit via a local server.

3. **Upload Your PDF:**

   - Click "Choose File" and select a PDF document
   - Click "Upload PDF" to process the document
   - Wait for confirmation that the file is ready

4. **Ask Questions:**

   - Type your question in the input field
   - Press Enter or click the send button
   - The AI will answer based ONLY on your uploaded PDF
   - If the answer isn't found in your document, it will explicitly refuse

5. **Upload Additional PDFs (Optional):**

   - You can upload more PDFs to the same session
   - All documents will be searchable together
   - Click "New Session" to start fresh with different documents

#### Example Workflow:

```
1. Upload: "company_report_2024.pdf"
   → System processes and indexes the document

2. Ask: "What was the revenue in Q3?"
   → System retrieves relevant sections and answers

3. Ask: "What is the CEO's favorite food?"
   → System refuses (information not in document)

4. Upload: "ceo_interview.pdf" (adds to same session)
   → Now both documents are searchable

5. Ask previous question again
   → May now answer if info is in new document
```

#### API Endpoints:

- `POST /api/upload` - Upload a PDF file
  - Optional: `?session_id=<id>` to add to existing session
  - Returns: `session_id`, `file_path`, `file_name`, `files_in_session`

- `POST /api/chat` - Ask a question
  - Body: `{"question": "...", "session_id": "..."}`
  - Returns: `{"response": "..."}`

- `GET /api/session/{session_id}/files` - List files in a session
  - Returns: List of uploaded file names

- `DELETE /api/session/{session_id}` - Delete a session
  - Removes all files and embeddings for that session


---

## Example: Successful Answer

**Question:**

```
What skills does the candidate have?
```

**Response:**

```
Answer based on retrieved context:
[Extracted content from document]

Sources: [chunk_0, chunk_1]
```

---

## Example: Refusal Case

**Question:**

```
What is the candidate's favorite programming language?
```

**Response:**

```
I'm unable to answer this question because the provided documents do not contain sufficient information.
```

This behavior is intentional and correct.

---

## What This Project Demonstrates

### Technical Skills

* Vector embeddings & similarity search
* Retrieval-Augmented Generation (RAG)
* FAISS indexing
* Confidence-based decision systems
* Modular Python architecture

### Professional Engineering Mindset

* Reliability-first AI design
* Explicit handling of uncertainty
* Trust-aware system behavior
* Production-oriented thinking

---

## Why This Project Matters

Many AI systems fail silently by producing confident but incorrect answers.

This project shows an alternative approach:

> **If the AI does not know, it does not speak.**

This principle is critical in real-world AI applications.

---

## Future Enhancements (Optional)

* Persistent FAISS index (save/load)
* Advanced confidence metrics
* Real LLM integration (OpenAI / HF)
* REST API using FastAPI
* Automated evaluation metrics

---

## Final Note

This project intentionally prioritizes **correctness and trust** over fluency.

In environments where reliability matters, refusal is a strength.

---

**Author:** Shakib Howlader
