import streamlit as st
import pandas as pd
import time
import requests

st.set_page_config(page_title="Gengo - Your AI Data Analyst", layout="centered", initial_sidebar_state="collapsed")

API_URL = "https://gengo-backend-api-b89286ea64a6.herokuapp.com/query"

st.markdown("""
<style>
/* Import a premium modern font */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Base App Background - Clean Light Gradient */
.stApp {
    background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
}

/* Hide Default Streamlit UI elements */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Headings */
h1 {
    font-size: 3.5rem !important;
    font-weight: 800 !important;
    background: -webkit-linear-gradient(45deg, #0f172a, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px !important;
    padding-bottom: 10px;
}
h2 {
    font-size: 2rem !important;
    font-weight: 600 !important;
    color: #1e293b !important;
}

/* Subtext */
.subtitle {
    font-size: 1.25rem;
    color: #475569;
    font-weight: 400;
    margin-bottom: 30px;
}

/* Custom Primary Button Styling */
div.stButton > button {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.2) !important;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.3) !important;
}

div.stButton > button:active {
    transform: translateY(1px) !important;
}

/* Text Input Styling (Glassmorphism feel) */
.stTextInput input {
    background: rgba(255, 255, 255, 0.6) !important;
    border: 1px solid rgba(203, 213, 225, 0.5) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-size: 1.1rem !important;
    color: #0f172a !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
}

.stTextInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15) !important;
    background: #ffffff !important;
}

/* Result Boxes */
.success-box {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    border-left: 5px solid #10b981;
    padding: 15px 20px;
    border-radius: 8px;
    color: #065f46;
    font-weight: 600;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(16, 185, 129, 0.1);
}

.code-box {
    background-color: #1e293b;
    border-radius: 12px;
    padding: 20px;
    color: #e2e8f0;
    font-family: 'Courier New', monospace;
    font-size: 0.95rem;
    overflow-x: auto;
    margin-bottom: 20px;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);
}

/* Checkbox styling */
.stCheckbox label {
    font-weight: 500;
    color: #475569;
}

hr {
    border: 0;
    height: 1px;
    background: linear-gradient(to right, rgba(0,0,0,0), rgba(15,23,42,0.1), rgba(0,0,0,0));
    margin: 40px 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------
# UI LAYOUT
# -----------------

# Header Section
st.markdown("<h1>Gengo</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Query your legacy database in plain English. AI-powered SQL generation and execution.</p>', unsafe_allow_html=True)

# Three column highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**1. No SQL Needed**<br>Just speak naturally.", unsafe_allow_html=True)
with col2:
    st.markdown("**2. Blazing Fast**<br>Instant execution via Llama & Supabase.", unsafe_allow_html=True)
with col3:
    st.markdown("**3. Read-Only Safe**<br>Your data cannot be altered.", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Main Interaction Area
st.markdown("<h2>Ask your Data</h2>", unsafe_allow_html=True)

# Suggestion Chips
st.caption("Try one of these to get started:")
s1, s2, s3 = st.columns(3)
if s1.button("Customers in Mumbai"):
    st.session_state.prefill = "Show me all customers from Mumbai"
if s2.button("Highest orders"):
    st.session_state.prefill = "Who are the top 5 customers with the highest amount orders?"
if s3.button("Recent activity"):
    st.session_state.prefill = "List the 10 most recent orders"

st.write("") # small spacing

# Control Form
with st.form("query_form"):
    user_input = st.text_input("What would you like to know?", value=st.session_state.get("prefill", ""), placeholder="e.g., Show me the top 5 customers by order amount...")
    
    col_a, col_b = st.columns([3, 1])
    with col_a:
        use_fallback = st.checkbox("Use Fallback AI (Locally hosted Ollama)", value=False)
    with col_b:
        submitted = st.form_submit_button("Generate & Run SQL")

# Results Area
if submitted and user_input:
    with st.spinner("🤖 Analyzing your prompt and generating SQL..."):
        try:
            req_start = time.time()
            response = requests.post(API_URL, json={
                "question": user_input,
                "use_fallback": use_fallback
            }, timeout=20)
            req_time = round((time.time() - req_start) * 1000)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("error"):
                    st.error(f"⚠️ **Error:** {data['error']}")
                else:
                    # Success
                    st.markdown('<div class="success-box">✅ Query generated and executed successfully!</div>', unsafe_allow_html=True)
                    
                    st.markdown("### ⚙️ The SQL Query")
                    st.markdown(f'<div class="code-box">{data["sql"]}</div>', unsafe_allow_html=True)

                    if data.get("results"):
                        st.markdown(f"### 📊 Results ({len(data['results'])} rows)")
                        # Show interactive dataframe
                        st.dataframe(pd.DataFrame(data["results"]), use_container_width=True)
                    else:
                        st.warning("No records found matching your query.")

                    if data.get("suggestion"):
                        st.info(data["suggestion"])
                    
                    st.caption(f"⚡ End-to-end processing time: {req_time}ms (DB execution: {data.get('execution_time_ms', 0)}ms)")
            
            else:
                st.error(f"**Backend Server Error ({response.status_code}):** Ensure your Heroku Dyno is awake.")
        
        except Exception as e:
            st.error(f"**Connection Failed:** Could not reach the API. Error details: `{str(e)}`")