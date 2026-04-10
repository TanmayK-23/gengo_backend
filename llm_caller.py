import os
import requests
from dotenv import load_dotenv
load_dotenv()
# =========================
# Gemini (Primary)
# =========================
def call_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

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
# Groq (High Performance Alternative)
# =========================
def call_groq(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a professional SQL generator for legacy databases. Output raw SQL only."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Groq Error: {response.text}")

    return response.json()["choices"][0]["message"]["content"].strip()


# =========================
# Main LLM Caller
# =========================
def call_llm(prompt, use_fallback=False):
    try:
        # 1. Use Groq if key is present
        if os.getenv("GROQ_API_KEY"):
            return call_groq(prompt), "Groq (Llama 3)"

        # 2. Otherwise use Gemini
        if os.getenv("GEMINI_API_KEY") and not use_fallback:
            return call_gemini(prompt), "Gemini 2.0 Flash"

        # 3. Last resort: Ollama (Only works locally)
        return call_ollama(prompt), "Ollama (Local Llama 3)"

    except Exception as e:
        return f"ERROR: {str(e)}", "Error"