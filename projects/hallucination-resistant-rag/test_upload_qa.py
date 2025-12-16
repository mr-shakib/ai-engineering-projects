"""
Test script for PDF upload and Q&A functionality
Run this after starting the backend server
"""

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_server_health():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Server is running")
            return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Start it with: uvicorn src.api:app --reload")
        return False

def test_upload(file_path):
    """Test PDF upload"""
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return None
    
    print(f"\n📤 Uploading {file_path}...")
    
    with open(file_path, 'rb') as f:
        files = {'file': (Path(file_path).name, f, 'application/pdf')}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Upload successful!")
        print(f"   Session ID: {data['session_id']}")
        print(f"   File name: {data['file_name']}")
        print(f"   Files in session: {', '.join(data['files_in_session'])}")
        return data['session_id']
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_chat(session_id, question):
    """Test asking a question"""
    print(f"\n💬 Asking: {question}")
    
    payload = {
        "question": question,
        "session_id": session_id
    }
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Response received:")
        print(f"\n{data['response']}\n")
        return True
    else:
        print(f"❌ Chat failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def test_list_files(session_id):
    """Test listing files in a session"""
    print(f"\n📁 Listing files in session...")
    
    response = requests.get(f"{BASE_URL}/api/session/{session_id}/files")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Files in session:")
        for file in data['files']:
            print(f"   - {file}")
        return True
    else:
        print(f"❌ List files failed: {response.status_code}")
        return False

def test_delete_session(session_id):
    """Test deleting a session"""
    print(f"\n🗑️  Deleting session...")
    
    response = requests.delete(f"{BASE_URL}/api/session/{session_id}")
    
    if response.status_code == 200:
        print(f"✅ Session deleted successfully")
        return True
    else:
        print(f"❌ Delete failed: {response.status_code}")
        return False

def main():
    print("=" * 60)
    print("PDF Upload & Q&A System - Test Suite")
    print("=" * 60)
    
    # Test 1: Server health
    if not test_server_health():
        return
    
    # Test 2: Upload PDF
    # You need to provide a test PDF file path
    test_pdf = "test_document.pdf"  # Change this to your test PDF
    
    print("\n" + "=" * 60)
    print("Note: This test requires a PDF file.")
    print("Create a simple test PDF or provide path to existing one.")
    print("=" * 60)
    
    pdf_path = input(f"\nEnter PDF file path (or press Enter to skip): ").strip()
    
    if not pdf_path:
        print("\n⚠️  Skipping upload tests (no PDF provided)")
        print("✅ Server health check passed!")
        return
    
    session_id = test_upload(pdf_path)
    
    if not session_id:
        return
    
    # Test 3: List files
    test_list_files(session_id)
    
    # Test 4: Ask questions
    print("\n" + "=" * 60)
    print("Testing Q&A Functionality")
    print("=" * 60)
    
    # Let user ask questions
    while True:
        question = input("\nAsk a question (or press Enter to finish): ").strip()
        if not question:
            break
        test_chat(session_id, question)
    
    # Test 5: Upload another file to same session
    print("\n" + "=" * 60)
    another_pdf = input("Upload another PDF to same session? (path or Enter to skip): ").strip()
    
    if another_pdf and Path(another_pdf).exists():
        print(f"\n📤 Adding to session {session_id}...")
        with open(another_pdf, 'rb') as f:
            files = {'file': (Path(another_pdf).name, f, 'application/pdf')}
            response = requests.post(
                f"{BASE_URL}/api/upload?session_id={session_id}",
                files=files
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Added {data['file_name']} to session")
            print(f"   Total files: {', '.join(data['files_in_session'])}")
            test_list_files(session_id)
    
    # Test 6: Cleanup
    print("\n" + "=" * 60)
    cleanup = input("Delete test session? (y/N): ").strip().lower()
    
    if cleanup == 'y':
        test_delete_session(session_id)
    else:
        print(f"\n💾 Session preserved: {session_id}")
        print(f"   Delete later with: curl -X DELETE {BASE_URL}/api/session/{session_id}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
