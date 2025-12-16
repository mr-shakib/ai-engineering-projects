import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
import os

SESSIONS_DIR = Path("data/sessions")
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

# Maximum file size: 50 MB
MAX_FILE_SIZE = 50 * 1024 * 1024


def validatePdfFile(file: UploadFile) -> None:
    """Validate the uploaded file is a proper PDF."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE // (1024*1024)}MB limit")


async def saveUploadedPdf(file: UploadFile, session_id: str = None) -> (str, str):
    """
    Save an uploaded PDF file to a session directory.
    If session_id is provided, adds file to existing session.
    Otherwise, creates a new session.
    """
    validatePdfFile(file)
    
    if not session_id:
        session_id = str(uuid.uuid4())
    
    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = session_dir / "uploads" / file.filename
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if file already exists
    if file_path.exists():
        base_name = file_path.stem
        extension = file_path.suffix
        counter = 1
        while file_path.exists():
            file_path = file_path.parent / f"{base_name}_{counter}{extension}"
            counter += 1

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    return session_id, str(file_path)


def getSessionFiles(session_id: str) -> list:
    """Get list of files uploaded in a session."""
    session_dir = SESSIONS_DIR / session_id / "uploads"
    if not session_dir.exists():
        return []
    
    return [f.name for f in session_dir.iterdir() if f.suffix.lower() == '.pdf']


def deleteSession(session_id: str) -> bool:
    """Delete a session and all its files."""
    session_dir = SESSIONS_DIR / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)
        return True
    return False
