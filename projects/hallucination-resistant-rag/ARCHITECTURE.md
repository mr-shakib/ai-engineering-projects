# System Architecture - PDF Upload & Q&A

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE (web/)                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  index.html - Modern Glassmorphism UI                            │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────┐               │  │
│  │  │ File Upload│  │ Files List   │  │ New Session │               │  │
│  │  │   Button   │  │ (with icons) │  │   Button    │               │  │
│  │  └─────┬──────┘  └──────────────┘  └─────────────┘               │  │
│  │        │                                                           │  │
│  │  ┌─────▼─────────────────────────────────────────┐                │  │
│  │  │         Chat Container                        │                │  │
│  │  │  • Bot messages (with sources)                │                │  │
│  │  │  • User messages                              │                │  │
│  │  │  • Typing indicators                          │                │  │
│  │  └───────────────────────────────────────────────┘                │  │
│  │                                                                    │  │
│  │  ┌─────────────────────────────────────────────┐                  │  │
│  │  │  Question Input Field  [Send Button ➤]     │                  │  │
│  │  └─────────────────────────────────────────────┘                  │  │
│  │                                                                    │  │
│  │  script.js - Event handling & API calls                           │  │
│  │  style.css - Glassmorphism styling                                │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ HTTP/AJAX Requests
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      BACKEND API (src/api.py)                           │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  FastAPI Application + CORS Middleware                           │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ POST /api/upload │  │ POST /api/chat   │  │ Session Mgmt API │     │
│  │                  │  │                  │  │  • GET /files    │     │
│  │ • Validate PDF   │  │ • Embed question │  │  • DELETE /{id}  │     │
│  │ • Save to disk   │  │ • Search FAISS   │  └──────────────────┘     │
│  │ • Process file   │  │ • Generate reply │                            │
│  │ • Return sess_id │  │ • Return answer  │                            │
│  └────────┬─────────┘  └────────┬─────────┘                            │
│           │                     │                                       │
│           ▼                     ▼                                       │
│  ┌────────────────────────────────────────────────────┐                │
│  │           Core Processing Modules                  │                │
│  │                                                     │                │
│  │  upload.py     ingest.py      chunk.py             │                │
│  │  • Validate    • Extract      • Split text         │                │
│  │  • Save file   • Parse PDF    • Add overlap        │                │
│  │  • Session     • Get text     • Return chunks      │                │
│  │                                                     │                │
│  │  embed.py      retrieve.py    generate.py          │                │
│  │  • Create      • Build index  • LLM call           │                │
│  │  • embeddings  • FAISS search • Format answer      │                │
│  │  • Store       • Get top-K    • Add sources        │                │
│  │                                                     │                │
│  │  decision.py   main.py                             │                │
│  │  • Confidence  • Orchestrate  • runRAGSystem()     │                │
│  │  • Threshold   • Pipeline     • runRAGForFile()    │                │
│  │  • Refusal     • Integration                       │                │
│  └────────────────────────────────────────────────────┘                │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE & INDEXES                             │
│                                                                          │
│  data/sessions/<session-id>/                                            │
│  │                                                                       │
│  ├── uploads/                    ← Original PDFs                        │
│  │   ├── document1.pdf                                                  │
│  │   ├── document2.pdf                                                  │
│  │   └── ...                                                            │
│  │                                                                       │
│  ├── chunks/                     ← Text chunks (optional cache)         │
│  │                                                                       │
│  ├── embeddings/                 ← Vector embeddings                    │
│  │   ├── document1_chunk_0.npy                                          │
│  │   ├── document1_chunk_1.npy                                          │
│  │   └── ...                                                            │
│  │                                                                       │
│  └── index/                      ← FAISS index + metadata               │
│      ├── index.faiss             (fast vector search)                   │
│      └── metadata.json           (chunk info, sources)                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘


PROCESSING PIPELINE:
═══════════════════

📤 UPLOAD FLOW:
  PDF File → Validate → Save → Extract Text → Chunk → Embed → Index → Ready

💬 Q&A FLOW:
  Question → Embed → FAISS Search → Get Top-K → Score → Decision Gate
                                                              │
                                      ┌───────────────────────┴─────────────┐
                                      │                                     │
                                   ✅ High Confidence                  ❌ Low Confidence
                                      │                                     │
                                  Generate Answer                     Return Refusal
                                  + Source Citations                  + Explanation
                                      │                                     │
                                      └─────────────┬─────────────────────┘
                                                    │
                                              Return to User


KEY COMPONENTS:
═══════════════

🔧 Backend Technologies:
   • FastAPI - REST API framework
   • Uvicorn - ASGI server
   • pdfplumber - PDF text extraction
   • Sentence Transformers - Text embeddings
   • FAISS - Vector similarity search
   • NumPy - Numerical operations

🎨 Frontend Technologies:
   • Vanilla HTML/CSS/JavaScript
   • Glassmorphism design
   • Fetch API for AJAX
   • Real-time UI updates

🧠 AI/ML Components:
   • Sentence-BERT (all-MiniLM-L6-v2) - Embeddings
   • FAISS - Approximate nearest neighbor search
   • Confidence scoring - Hallucination prevention
   • Decision gate - Answer/refusal mechanism

📊 Data Flow:
   • Session-based architecture
   • UUID session identifiers
   • Persistent file storage
   • In-memory FAISS indexes
   • Metadata tracking


HALLUCINATION PREVENTION:
═════════════════════════

The system prevents hallucinations through multiple layers:

1. RETRIEVAL-ONLY: Only uses retrieved document chunks
2. SIMILARITY SCORING: Measures relevance of retrieved text
3. CONFIDENCE THRESHOLD: Requires minimum similarity score
4. EXPLICIT REFUSAL: Says "I don't know" when confidence is low
5. SOURCE ATTRIBUTION: Always shows where answer came from

This is not just prompt engineering - it's ARCHITECTURAL hallucination prevention!


SECURITY MODEL:
══════════════

Current (Development):
  • No authentication
  • Local file storage
  • UUID session IDs
  • CORS enabled for all origins
  • Single-server deployment

Production Requirements:
  • User authentication (JWT/OAuth)
  • File encryption at rest
  • Rate limiting
  • Input sanitization
  • HTTPS only
  • Session expiration
  • File quotas per user
  • Audit logging


SCALABILITY NOTES:
═════════════════

Current: Single-server, file-based storage
         Good for: <100 users, <10GB documents

To scale:
  • Use S3/cloud storage for PDFs
  • Use vector database (Pinecone/Weaviate)
  • Add Redis for session management
  • Load balancer for multiple API servers
  • Queue system for long-running tasks
  • CDN for web interface
  • Separate embedding service
