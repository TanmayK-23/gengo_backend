import os
import requests
from dotenv import load_dotenv
load_dotenv()
# =========================
# Gemini (Primary)
# =========================
def call_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, json=data)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


# =========================
# Ollama (Fallback)
# =========================
def call_ollama(prompt):
    url = "http://localhost:11434/api/generate"

    response = requests.post(url, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        raise Exception("Ollama not running")

    return response.json()["response"].strip()


# =========================
# Main LLM Caller
# =========================
def call_llm(prompt, use_fallback=False):
    try:
        # If user explicitly wants fallback → Ollama
        if use_fallback:
            return call_ollama(prompt)

        # Otherwise use Gemini
        if os.getenv("GEMINI_API_KEY"):
            return call_gemini(prompt)

        # If Gemini key missing → fallback automatically
        return call_ollama(prompt)

    except Exception as e:
        return f"ERROR: {str(e)}"