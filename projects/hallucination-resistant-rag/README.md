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

### 3. Add Documents

Place PDF or text files inside:

```
data/documents/
```

---


---

## Running the System

### Option 1: Command Line Interface (CLI)

```bash
python src/main.py "Your question here"
```

### Option 2: Beautiful Web Interface 🌟

1. **Start the API Backend:**

   ```bash
   uvicorn src.api:app --reload
   ```

2. **Open the App:**

   Open `web/index.html` in your browser.

   *Features: Dark mode, real-time typing indicators, and formatted source citations.*


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
