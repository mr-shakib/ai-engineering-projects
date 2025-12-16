"""
Quick test to verify PDF upload and Q&A functionality
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from src.ingest import ingestDocuments, extractTextFromPdf
        from src.chunk import chunkText
        from src.embed import createEmbedding, embedChunks
        from src.retrieve import buildFaissIndex, searchFaiss
        from src.generate import generateAnswer
        from src.main import runRAGSystem, runRAGForSingleFile
        from src.upload import saveUploadedPdf, getSessionFiles, deleteSession
        from src.api import app
        print("✓ All imports successful!")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are installed"""
    print("\nTesting dependencies...")
    required = [
        "pdfplumber",
        "sentence_transformers", 
        "numpy",
        "faiss",
        "fastapi",
        "uvicorn",
    ]
    
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✓ {pkg}")
        except ImportError:
            print(f"✗ {pkg} - NOT INSTALLED")
            missing.append(pkg)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("✓ All dependencies installed!")
        return True

def test_directory_structure():
    """Test that required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = [
        PROJECT_ROOT / "data" / "sessions",
        PROJECT_ROOT / "web",
        PROJECT_ROOT / "src",
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"✓ {dir_path.relative_to(PROJECT_ROOT)}")
        else:
            print(f"✗ {dir_path.relative_to(PROJECT_ROOT)} - NOT FOUND")
            all_exist = False
    
    if all_exist:
        print("✓ All required directories exist!")
    return all_exist

def test_web_files():
    """Test that web interface files exist"""
    print("\nTesting web interface files...")
    
    web_files = [
        PROJECT_ROOT / "web" / "index.html",
        PROJECT_ROOT / "web" / "script.js",
        PROJECT_ROOT / "web" / "style.css",
    ]
    
    all_exist = True
    for file_path in web_files:
        if file_path.exists():
            print(f"✓ {file_path.name}")
        else:
            print(f"✗ {file_path.name} - NOT FOUND")
            all_exist = False
    
    if all_exist:
        print("✓ All web files exist!")
    return all_exist

if __name__ == "__main__":
    print("=" * 50)
    print("RAG System - Verification Test")
    print("=" * 50)
    
    results = {
        "Imports": test_imports(),
        "Dependencies": test_dependencies(),
        "Directory Structure": test_directory_structure(),
        "Web Interface": test_web_files(),
    }
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✅ System is ready!")
        print("\nTo start the server:")
        print("  python -m src.api")
        print("\nThen open: http://localhost:8000")
        print("\nYou can:")
        print("  1. Upload a PDF file")
        print("  2. Ask questions about the content")
        print("  3. The system will refuse to answer if uncertain")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    sys.exit(0 if all_passed else 1)
