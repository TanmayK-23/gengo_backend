# GENGO: AI-Powered Natural Language Database Analyst 🤖📊

**GENGO** is a production-grade full-stack application that translates plain English questions into highly optimized PostgreSQL queries instantly. It features a robust FastAPI backend for LLM query orchestration and a beautiful, glassmorphic Streamlit frontend for data consumption, visualization, and dynamic schema navigation.

---

## ✨ Features

- **No SQL Required:** Natural language to SQL translation using blazing-fast LLMs (prioritizing **Groq/Llama-3**, with **Gemini 2.0 Flash** and **Ollama** fallbacks).
- **Read-Only Safety System:** Hardcoded validation rules prevent any `DROP`, `UPDATE`, `INSERT`, or `DELETE` commands from executing, ensuring zero risk to your legacy databases.
- **Dynamic Schema Awareness:** Automatically maps current tables, columns, and foreign keys via PostgreSQL `information_schema` directly into the LLM context.
- **Auto-Charting:** Intelligent frontend logic auto-detects categorical/numeric columns and generates interactive visualizations out of the box.
- **Instant Export:** Download generated queries as CSVs in a single click.
- **Self-Healing AI:** If the database throws a SQL exception, Gengo intercepts the error, feeds it back to the LLM, and self-corrects the query autonomously.

## 🏗️ Architecture Stack

- **Frontend:** [Streamlit](https://streamlit.io/) (Designed with custom CSS, completely responsive).
- **Backend API:** [FastAPI](https://fastapi.tiangolo.com/) hosted on Heroku.
- **Database:** PostgreSQL (Hosted on [Supabase](https://supabase.com/)).
- **LLM Engine:** Groq API (Primary), Google Gemini API (Secondary), Ollama (Local Fallback).
- **Deployment:** Streamlit Cloud (Frontend) & Heroku (Backend).

---

## 🚀 Quick Start (Local Development)

Follow these instructions to run the entire backend and frontend suite locally.

### 1. Prerequisites
- Python 3.9+
- A PostgreSQL database string (e.g., Supabase, Neon, or local).
- An API key from [Groq](https://console.groq.com/keys) or [Google AI Studio](https://aistudio.google.com/).

### 2. Environment Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/TanmayK-23/gengo_backend.git
cd gengo_backend
pip install -r requirements.txt
```

Create a `.env` file in the root directory and add your keys:

```env
# Your postgres connection string (session pooler recommended)
DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@host:6543/postgres"

# Preferred LLM API Key (Groq is highly recommended for speed)
GROQ_API_KEY="gsk_..."
GEMINI_API_KEY="AIza..."
```

### 3. Run the Backend API

Start the FastAPI server via Uvicorn.

```bash
uvicorn api:app --reload
```
*The backend will boot up at `http://localhost:8000`. You can view the Auto-Docs at `http://localhost:8000/docs`.*

### 4. Run the Streamlit Frontend

In a separate terminal window, launch the UI:

```bash
streamlit run app.py
```
*(Note: If running locally, you must update `API_URL` inside `app.py` to point to `http://localhost:8000/query` instead of the Heroku endpoint).*

---

## ☁️ Deployment Guides

### Backend (Heroku)
1. Install the Heroku CLI and login.
2. Create an app: `heroku create gengo-backend-api`
3. Add environment variables:
   ```bash
   heroku config:set DATABASE_URL="..." GROQ_API_KEY="..." 
   ```
4. Deploy the code:
   ```bash
   git push heroku main
   ```

### Frontend (Streamlit Cloud)
1. Push `app.py` and `requirements.txt` to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/), click "New App", and point it to your repository.
3. Ensure the `API_URL` inside `app.py` points to your live Heroku backend URL.

---

## 🔒 Security Notes
Gengo is built heavily on the premise of Database Agnostic connection. However, **never grant the database connection user write-privileges if it is connected to a production application.** The backend employs string-matching to prevent malicious queries, but enforcing real DB-level read-only role permissions is essential for production security.
