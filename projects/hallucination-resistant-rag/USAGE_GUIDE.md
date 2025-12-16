# PDF Upload and Q&A Usage Guide

## Quick Start

### 1. Start the Backend Server

```bash
cd projects/hallucination-resistant-rag
uvicorn src.api:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 2. Open the Web Interface

Open `web/index.html` in your web browser.

## Using the PDF Upload Feature

### First-Time Upload

1. **Click "Choose File"** button
2. **Select a PDF** from your computer
3. **Click "Upload PDF"** button
4. **Wait for processing** - you'll see "Uploading and processing..."
5. **Success!** - The chat interface will appear

### Asking Questions

1. **Type your question** in the text input at the bottom
2. **Press Enter** or click the send button (➤)
3. **Receive answer** - The AI will:
   - ✅ Provide an answer with sources if found in your PDF
   - ❌ Explicitly refuse if information is not available

### Adding More PDFs to Same Session

1. **Upload first PDF** as described above
2. **Select another file** without clicking "New Session"
3. **Upload the second PDF** - it joins the same session
4. **Ask questions** - AI can now search across all uploaded PDFs

### Starting a New Session

1. **Click "New Session"** button (red button)
2. **Confirm** the dialog
3. **Upload new PDFs** - previous session is cleared
4. **Ask fresh questions** on new documents

## Example Use Cases

### Use Case 1: Single Document Analysis
```
Upload: research_paper.pdf
Ask: "What methodology did the researchers use?"
Ask: "What were the main findings?"
Ask: "What future work is suggested?"
```

### Use Case 2: Multiple Document Search
```
Upload: contract_v1.pdf
Upload: contract_v2.pdf
Upload: amendment.pdf
Ask: "What are the payment terms?"
Ask: "How did the terms change between v1 and v2?"
```

### Use Case 3: Document Verification
```
Upload: employee_handbook.pdf
Ask: "What is the vacation policy?"  → Gets answer with page reference
Ask: "What is the CEO's salary?"     → Refuses (not in document)
```

## Understanding Responses

### ✅ Successful Answer Format
```
📚 Retrieved Evidence:
Source 1
[Relevant text from your PDF]

Answer based on retrieved context:
[AI-generated answer based on the evidence]
```

### ⚠️ Refusal Format
```
⚠️ Cannot Answer:
I'm unable to answer this question because the provided documents 
do not contain sufficient information.
```

### Why Refusals Are Good
- **Prevents hallucinations** - No made-up information
- **Builds trust** - You know when the AI doesn't know
- **Source verification** - You can verify every answer

## Features Overview

### 📤 PDF Upload
- Supports PDF files only
- Maximum file size: 50 MB
- Handles text-based PDFs (not scanned images)
- Duplicate file names are auto-renamed

### 💾 Session Management
- Each upload session gets a unique ID
- Sessions persist until explicitly deleted
- Multiple files can share one session
- "New Session" clears previous uploads

### 📁 File Tracking
- See all uploaded files in sidebar
- Files listed with 📄 icon
- Purple accent for active files
- Files are stored in `data/sessions/<session_id>/`

### 🔍 Smart Search
- Uses semantic similarity (not just keywords)
- Searches across all PDFs in session
- Ranks results by relevance
- Only returns high-confidence matches

### 🎨 UI Features
- Dark mode by default
- Glassmorphism design
- Real-time typing indicators
- Formatted source citations
- Responsive layout

## Technical Details

### How It Works

1. **Upload**: PDF → Text extraction → Chunking
2. **Embedding**: Text chunks → Vector embeddings
3. **Indexing**: Embeddings → FAISS vector index
4. **Query**: Question → Embedding → Search index
5. **Decision**: Check confidence → Answer or Refuse
6. **Generate**: LLM creates answer from retrieved text

### File Storage Structure
```
data/
└── sessions/
    └── <session-id>/
        ├── uploads/          # Your PDFs
        ├── chunks/           # Text chunks
        ├── embeddings/       # Vector embeddings
        └── index/            # FAISS index + metadata
```

### Confidence Threshold
- Default: 0.25 (similarity score)
- Lower = more strict (more refusals)
- Higher = more lenient (more answers, higher hallucination risk)

## Troubleshooting

### "Error uploading file"
- **Check file type**: Must be .pdf
- **Check file size**: Max 50 MB
- **Check backend**: Is uvicorn running?
- **Check console**: Open browser DevTools for errors

### "Backend is running" message
- Backend might be down or not responding
- Restart uvicorn: `uvicorn src.api:app --reload`
- Check if port 8000 is available

### No answer found (but you know it's there)
- PDF might be scanned (image-based, not text)
- Text extraction might have failed
- Try rephrasing your question
- Check if text is selectable in the PDF

### Upload takes too long
- Large PDFs take more time to process
- Embedding generation is CPU-intensive
- Wait for "Ready to chat" message
- Don't refresh during processing

## API Usage (Advanced)

### Upload via cURL
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@document.pdf"
```

### Add to existing session
```bash
curl -X POST "http://localhost:8000/api/upload?session_id=<id>" \
  -F "file=@another.pdf"
```

### Ask question via API
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is X?", "session_id": "<id>"}'
```

### List session files
```bash
curl "http://localhost:8000/api/session/<session_id>/files"
```

### Delete session
```bash
curl -X DELETE "http://localhost:8000/api/session/<session_id>"
```

## Best Practices

1. **Upload Quality Documents**
   - Use text-based PDFs, not scanned images
   - Ensure text is selectable in the PDF
   - Clean, well-formatted documents work best

2. **Ask Specific Questions**
   - Be clear and direct
   - Use keywords from your document
   - Break complex questions into parts

3. **Verify Answers**
   - Always check the source citations
   - The system shows where it found the answer
   - Refusals are better than wrong answers

4. **Manage Sessions**
   - Start new sessions for unrelated documents
   - Group related PDFs in one session
   - Clear old sessions to save space

5. **Understand Limitations**
   - Can only answer from uploaded content
   - Cannot reason beyond the documents
   - Cannot access external information
   - Cannot process images or charts (text only)

## Security Notes

- Files are stored locally on the server
- Session IDs are UUIDs (not guessable)
- No authentication required (local use)
- For production: Add authentication & file encryption
- Delete sensitive documents after use

## Performance Tips

- Smaller PDFs process faster
- Multiple small files > One huge file
- First query is slowest (loads index)
- Subsequent queries are fast
- Clear old sessions to free disk space

---

**Need Help?** Check the main [README.md](README.md) for architecture details and system overview.
