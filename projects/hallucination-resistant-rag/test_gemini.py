"""Quick test to check Gemini API"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {GEMINI_API_KEY[:20]}...")

# Try different model names
models_to_try = [
    "models/gemini-2.5-flash",
    "models/gemini-1.5-flash",
    "models/gemini-pro",
    "gemini-2.5-flash",
    "gemini-1.5-flash"
]

for model in models_to_try:
    print(f"\nTrying model: {model}")
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent"
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Say hello"}]}]
    }
    
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        },
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✅ SUCCESS with {model}")
        print(f"Response: {response.json()}")
        break
    else:
        print(f"❌ Failed: {response.text[:200]}")
