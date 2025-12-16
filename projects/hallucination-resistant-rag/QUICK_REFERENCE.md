# Quick Reference Guide

## 🚀 Start the System

```bash
# Navigate to project
cd projects/hallucination-resistant-rag

# Install dependencies (first time only)
pip install -r requirements.txt

# Start backend server
uvicorn src.api:app --reload

# Open web/index.html in your browser
```

## 📤 Upload PDF Workflow

```
1. Choose File → Select PDF
2. Upload PDF → Wait for processing
3. Ask questions → Get answers with sources
4. (Optional) Upload more PDFs to same session
5. (Optional) Click "New Session" to start fresh
```

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/upload` | POST | Upload a PDF file |
| `/api/upload?session_id=<id>` | POST | Add PDF to existing session |
| `/api/chat` | POST | Ask a question |
| `/api/session/{id}/files` | GET | List files in session |
| `/api/session/{id}` | DELETE | Delete session |

## 💬 Ask Questions

**Good Questions:**
- ✅ "What is X mentioned in the document?"
- ✅ "When did Y happen according to the report?"
- ✅ "Who is responsible for Z?"
- ✅ "What are the main points about topic A?"

**System Will Refuse:**
- ❌ Questions about info not in the document
- ❌ Opinions or subjective matters
- ❌ Future predictions (unless document specifies)
- ❌ General knowledge unrelated to documents

## 📁 File Structure

```
data/sessions/<session-id>/
├── uploads/       # Your PDFs
├── chunks/        # Text chunks
├── embeddings/    # Vector embeddings
└── index/         # FAISS search index
```

## 🎨 UI Elements

- **Blue Upload Button**: Upload first or additional PDF
- **Red New Session Button**: Clear session and start fresh
- **Purple File List**: Shows all uploaded PDFs
- **Chat Input**: Type questions here
- **Send Button (➤)**: Submit your question

## ⚙️ Configuration

Edit in code if needed:

| Setting | File | Default | Purpose |
|---------|------|---------|---------|
| Chunk Size | `src/chunk.py` | 300 words | Text chunk length |
| Chunk Overlap | `src/chunk.py` | 50 words | Overlap between chunks |
| Confidence Threshold | `src/main.py` | 0.25 | Min similarity score |
| Top K Results | `src/main.py` | 3 | Number of chunks retrieved |
| Max File Size | `src/upload.py` | 50 MB | Upload limit |

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend not responding | Restart: `uvicorn src.api:app --reload` |
| Upload fails | Check file is PDF, <50MB, backend running |
| No answers found | Rephrase question, check if text-based PDF |
| Slow processing | Large PDFs take time, be patient |
| CORS errors | Use same origin or configure CORS properly |

## 📊 Response Format

### Successful Answer:
```
📚 Retrieved Evidence:
Source 1
[Text from your PDF]

Answer based on retrieved context:
[AI-generated answer]
```

### Refusal:
```
⚠️ Cannot Answer:
I'm unable to answer this question because the provided 
documents do not contain sufficient information.
```

## 🔒 Security Notes

- ⚠️ Local use only (no authentication)
- ⚠️ Files stored unencrypted on server
- ⚠️ Session IDs are UUIDs (not guessable)
- ⚠️ Delete sensitive documents after use
- ✅ For production: Add auth, encryption, rate limiting

## 📚 Documentation

- **Full Guide**: [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Demo Questions**: [DEMO_QUESTIONS.md](DEMO_QUESTIONS.md)
- **Project Overview**: [README.md](README.md)
- **API Docs**: http://localhost:8000/docs (when server running)

## ✨ Quick Tips

1. **Test with sample PDF first**
2. **Ask specific questions**
3. **Check source citations**
4. **Start new session for unrelated docs**
5. **Refusals are a feature, not a bug**

## 📞 Need Help?

1. Check [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed instructions
2. Try [DEMO_QUESTIONS.md](DEMO_QUESTIONS.md) for question examples
3. Run `python test_upload_qa.py` to test system
4. Check browser console (F12) for frontend errors
5. Check terminal for backend errors

---

**Remember**: This system only answers from YOUR documents. It will NOT make up information. Refusals mean it's working correctly! 🛡️
