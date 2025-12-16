"""
Test script to verify the UI functionality:
1. Upload a PDF file
2. Ask a question based on the uploaded file
3. Verify the response
"""

import requests
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"
PROJECT_ROOT = Path(__file__).parent

def test_upload_pdf():
    """Test PDF upload functionality"""
    print("\n=== Testing PDF Upload ===")
    
    # Use the sample PDF
    pdf_path = PROJECT_ROOT / "data" / "documents" / "Resume_Shakib.pdf"
    
    if not pdf_path.exists():
        print(f"❌ Sample PDF not found at {pdf_path}")
        return None
    
    print(f"📄 Uploading: {pdf_path.name}")
    
    with open(pdf_path, 'rb') as f:
        files = {'file': (pdf_path.name, f, 'application/pdf')}
        response = requests.post(f"{BASE_URL}/api/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        session_id = data.get('session_id')
        print(f"✅ Upload successful!")
        print(f"   Session ID: {session_id}")
        print(f"   Files in session: {data.get('files_in_session', [])}")
        return session_id
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def test_ask_question(session_id, question):
    """Test asking a question"""
    print(f"\n=== Testing Question: '{question}' ===")
    
    payload = {
        "question": question,
        "session_id": session_id
    }
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        data = response.json()
        answer = data.get('response', '')
        print(f"✅ Response received:")
        print(f"\n{answer}\n")
        return answer
    else:
        print(f"❌ Question failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return None

def main():
    print("=" * 60)
    print("Testing Hallucination-Resistant RAG System UI")
    print("=" * 60)
    
    # Test 1: Upload PDF
    session_id = test_upload_pdf()
    if not session_id:
        print("\n❌ Cannot proceed without a valid session")
        return
    
    # Wait a moment for processing
    print("\n⏳ Waiting for processing to complete...")
    time.sleep(2)
    
    # Test 2: Ask a question that should be answerable
    test_ask_question(
        session_id,
        "What skills does Shakib have?"
    )
    
    # Test 3: Ask a question that should trigger refusal
    test_ask_question(
        session_id,
        "What is Shakib's favorite color?"
    )
    
    # Test 4: Ask another relevant question
    test_ask_question(
        session_id,
        "What programming languages does the candidate know?"
    )
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print(f"\n🌐 You can now open http://localhost:8000 in your browser")
    print("   to interact with the UI directly!")

if __name__ == "__main__":
    main()
