from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Add project root to Python path so imports work
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.main import runRAGSystem, runRAGForSingleFile
from src.upload import saveUploadedPdf, getSessionFiles, deleteSession

app = FastAPI(title="Hallucination-Resistant RAG API")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    question: str
    session_id: str


@app.post("/api/chat")
async def chat(query: Query):
    try:
        if not query.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        response = runRAGSystem(query.question, query.session_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload(file: UploadFile = File(...), session_id: str = None):
    """
    Upload a PDF file. If session_id is provided, adds to existing session.
    Otherwise creates a new session.
    """
    try:
        session_id, file_path = await saveUploadedPdf(file, session_id)
        
        # Run RAG process for all files in the session
        runRAGForSingleFile(session_id)
        
        # Get list of all files in session
        files = getSessionFiles(session_id)
        
        return {
            "session_id": session_id, 
            "file_path": file_path,
            "file_name": file.filename,
            "files_in_session": files
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/session/{session_id}/files")
async def list_session_files(session_id: str):
    """List all files uploaded in a session."""
    try:
        files = getSessionFiles(session_id)
        return {"session_id": session_id, "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/session/{session_id}")
async def delete_session_endpoint(session_id: str):
    """Delete a session and start fresh."""
    try:
        success = deleteSession(session_id)
        if success:
            return {"message": "Session deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount static files AFTER API routes to avoid conflicts
web_path = PROJECT_ROOT / "web"
if web_path.exists():
    app.mount("/", StaticFiles(directory=str(web_path), html=True), name="web")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api:app", 
        host="0.0.0.0", 
        port=8000,
        reload=False
    )
