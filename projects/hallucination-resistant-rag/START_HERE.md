# Quick Start Guide - PDF Upload & Q&A System

## ✅ System is Ready!

Your hallucination-resistant RAG system is fully configured and ready to use. Users can upload PDFs and ask questions.

## 🚀 How to Start

### 1. Install Dependencies (if not already done)
```bash
cd c:\personal\AI-engineering-projects\projects\hallucination-resistant-rag
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python -m src.api
```

### 3. Access the Web Interface
Open your browser and go to:
```
http://localhost:8000
```

## 📖 How to Use

### Step 1: Upload a PDF
1. Click "Choose File" and select a PDF document
2. Click "Upload PDF"
3. Wait for processing (chunking and embedding)
4. You'll see a success message and the uploaded file listed

### Step 2: Ask Questions
1. Once a PDF is uploaded, the chat input will appear
2. Type your question about the document
3. Press Enter or click Send
4. The AI will answer based ONLY on the PDF content

### Step 3: Upload More PDFs (Optional)
- You can upload multiple PDFs to the same session
- They will all be searchable for answering questions
- Click "New Session" to start fresh

## 🛡️ Hallucination Resistance

The system will **refuse to answer** if:
- The question cannot be answered from the uploaded documents
- The retrieved context is not similar enough to the question
- There isn't sufficient evidence in the PDFs

Example refusal message:
```
⚠️ Cannot Answer: The question cannot be confidently answered based on the provided documents.
```

## 🔧 Features

✅ **PDF Upload** - Supports single or multiple PDF files
✅ **Question Answering** - Ask questions about uploaded content
✅ **Session Management** - Keep files in a session or start fresh
✅ **Hallucination Resistance** - Refuses when uncertain
✅ **Source Citations** - Shows which parts of the document were used
✅ **Multiple PDFs** - Search across multiple documents at once

## 📁 API Endpoints

If you want to use the API directly:

**Upload PDF:**
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@document.pdf"
```

**Ask Question:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?", "session_id": "your-session-id"}'
```

**List Files in Session:**
```bash
curl "http://localhost:8000/api/session/{session_id}/files"
```

**Delete Session:**
```bash
curl -X DELETE "http://localhost:8000/api/session/{session_id}"
```

## 🔍 Testing

Run the verification test:
```bash
python test_system.py
```

This will check:
- All imports work correctly
- All dependencies are installed
- Directory structure is correct
- Web interface files exist

## ⚙️ Configuration

Key settings in the code:

- **Max file size**: 50 MB (in `upload.py`)
- **Similarity threshold**: 0.25 (in `main.py` - lower = more strict)
- **Top K results**: 3 (number of chunks retrieved)
- **Chunk size**: 500 characters (in `chunk.py`)

## 🎯 Example Use Cases

1. **Research papers**: Upload PDFs and ask about methodology, results, conclusions
2. **Legal documents**: Upload contracts and ask specific questions
3. **Technical manuals**: Upload documentation and get specific answers
4. **Reports**: Upload business reports and query specific data points

## 📝 Notes

- Only PDF files are supported
- Files are stored in `data/sessions/{session_id}/`
- Each session has its own isolated data
- The system uses FAISS for efficient vector search
- Embeddings are generated using sentence-transformers

## 🎉 That's It!

Your system is ready to go. Just run `python -m src.api` and start uploading PDFs!
