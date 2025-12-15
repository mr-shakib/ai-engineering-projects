import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

# =========================
# Gemini Configuration
# =========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in your .env file.")

# Must EXACTLY match ListModels output
GEMINI_MODEL = "models/gemini-2.5-flash"

GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"{GEMINI_MODEL}:generateContent"
)

# =========================
# Dynamic Refusal Handling
# =========================

REFUSAL_TEMPLATES = [
    "I checked the available documents, but I couldn’t find an answer to that.",
    "The provided sources don’t include this information.",
    "I reviewed the context, but this detail isn’t mentioned in the documents.",
    "Based on the information I have, this question can’t be answered from the provided sources.",
    "I couldn’t find relevant information about this in the current context."
]

def get_dynamic_refusal(question=None):
    base = random.choice(REFUSAL_TEMPLATES)
    return f"{base} (Question: “{question}”)" if question else base

# =========================
# Main Answer Generator
# =========================

def generateAnswer(contextChunks, question):
    """
    Gemini-compatible, chat-friendly, hallucination-safe answer generator
    """

    # ---- HARD SAFETY GATE ----
    if not contextChunks:
        return get_dynamic_refusal(question)

    # ---- Prepare Context ----
    context_text = ""
    for chunk in contextChunks:
        context_text += f"\n[{chunk['id']}]\n{chunk['text'].strip()}\n"

    # ---- Combined Instruction + User Prompt (Gemini style) ----
    prompt = f"""
You are a helpful, professional assistant.

STRICT RULES:
- Use ONLY the information provided in the context below.
- Do NOT guess, assume, or use outside knowledge.
- If the answer is not explicitly stated, politely say it is not available.
- Keep the tone natural and conversational.
- Cite relevant source IDs (e.g., [chunk_1]) when answering.

Context:
{context_text}

User question:
{question}

Answer:
"""

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 512
        }
    }

    response = requests.post(
        GEMINI_URL,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        },
        json=payload
    )

    if response.status_code != 200:
        raise Exception(
            f"Gemini API error {response.status_code}: {response.text}"
        )

    data = response.json()

    try:
        answer_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return get_dynamic_refusal(question)

    # ---- Final Safety Net ----
    if not answer_text:
        return get_dynamic_refusal(question)

    return answer_text
