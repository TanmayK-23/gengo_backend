import streamlit as st
import pandas as pd
import time
import requests

st.set_page_config(page_title="Gengo", layout="wide")

API_URL = "https://gengo-backend-api-b89286ea64a6.herokuapp.com/query"

# 🎨 GLOBAL STYLE
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: #f5f1eb;
    font-family: 'Segoe UI', sans-serif;
}

/* FIX WHITE HEADINGS */
h2, h3 {
    color: #111827 !important;
}

/* NAVBAR */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: #0f172a;
    padding: 18px 60px;
    z-index: 999;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.logo {
    font-size: 30px;
    font-weight: 700;
    color: white;
    letter-spacing: 2px;
}

/* MAIN */
.main {
    margin-top: 110px;
}

/* HERO */
.hero {
    max-width: 900px;
    margin-left: 60px;
}

.hero-title {
    font-size: 64px;
    font-weight: 700;
    color: #111827;
}

.hero-sub {
    font-size: 20px;
    color: #374151;
    margin-top: 15px;
}

.hero-desc {
    font-size: 18px;
    color: #4b5563;
    margin-top: 10px;
    line-height: 1.6;
}

/* CTA BUTTON */
.center-btn {
    text-align: center;
    margin-top: 50px;
}

.cta-btn {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white !important;
    padding: 14px 36px;
    border-radius: 40px;
    text-decoration: none !important;
    display: inline-block;
    font-size: 16px;
    transition: all 0.3s ease;
    cursor: pointer;
}

.cta-btn:hover {
    transform: scale(1.08);
    box-shadow: 0 0 30px rgba(15, 23, 42, 0.4);
}

/* DIVIDER */
.divider {
    border-top: 1px solid #d1d5db;
    margin: 60px 0;
}

/* SECTION */
.section-title {
    font-size: 26px;
    font-weight: 600;
    color: #111827;
}

.section-text {
    color: #374151;
    margin-top: 8px;
}

/* INPUT */
.stTextInput input {
    background-color: #ffffff !important;
    color: #111827 !important;
    border-radius: 10px;
    padding: 12px;
}

/* LABEL */
label {
    color: #2563eb !important;
}

/* BUTTON */
div.stButton > button {
    background: #0f172a !important;
    color: white !important;
    border-radius: 30px;
    padding: 12px 28px;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
}

/* CUSTOM BOX */
.box {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 12px;
    margin-top: 15px;
}

/* SQL BOX */
.sql-box {
    background: #0d1117;
    color: #c9d1d9;
    padding: 18px;
    border-radius: 12px;
    font-family: monospace;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

# NAVBAR
st.markdown('<div class="navbar"><div class="logo">GENGO</div></div>', unsafe_allow_html=True)

# MAIN
st.markdown('<div class="main">', unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
<div class="hero-title">Welcome</div>
<div class="hero-sub">Query your database in plain English</div>
<div class="hero-desc">
Gengo is an AI-powered system that converts natural language into SQL queries, executes them, and returns results instantly.
</div>
</div>
""", unsafe_allow_html=True)

# ✅ WORKING SCROLL BUTTON (JS FIX)
st.markdown("""
<div class="center-btn">
<button class="cta-btn" onclick="document.getElementById('try-section').scrollIntoView({behavior: 'smooth'});">
 Try it now
</button>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# INFO
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">What Gengo Does</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-text">Converts plain English into SQL and executes it instantly.</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-title">Why It Matters</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-text">Makes data accessible to everyone without SQL knowledge.</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 🎯 SCROLL TARGET (IMPORTANT)
st.markdown('<div id="try-section"></div>', unsafe_allow_html=True)

# TRY
st.markdown("## Try it now")

c1, c2, c3 = st.columns(3)

if c1.button("Customers from New York"):
    st.session_state.prefill = "Show customers from New York"

if c2.button("Top customers"):
    st.session_state.prefill = "Show top 5 customers by balance"

if c3.button("All customers"):
    st.session_state.prefill = "List all customers"

# INPUT
with st.form("query_form"):
    user_input = st.text_input("Ask something...", value=st.session_state.get("prefill", ""))
    use_fallback = st.checkbox("Use Fallback LLM (Ollama/Llama 3)", value=False)
    submitted = st.form_submit_button("Generate SQL")

# OUTPUT
if submitted and user_input:

    placeholder = st.empty()

    # ANIMATION
    for i in range(3):
        placeholder.markdown(f"""
        <div style="
            padding:16px;
            border-radius:10px;
            background:#f1f5f9;
            color:#111827;
            font-weight:500;
        ">
            🤖 Generating SQL{'.' * (i+1)}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.4)

    placeholder.empty()

    try:
        response = requests.post(API_URL, json={
            "question": user_input,
            "use_fallback": use_fallback
        })
        
        data = response.json()
        
        if response.status_code == 200 and not data.get("error"):
            st.markdown("""
            <div class="box" style="background:#ecfdf5; border:1px solid #a7f3d0; color:#065f46;">
            Query executed successfully
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 🔍 Your Query")
            st.markdown(f'<div class="box">{user_input}</div>', unsafe_allow_html=True)

            st.markdown("### ⚙️ Generated SQL")
            st.markdown(f'<div class="sql-box">{data["sql"]}</div>', unsafe_allow_html=True)

            if data["results"]:
                st.markdown(f"### 📊 Results ({len(data['results'])} rows)")
                df = pd.DataFrame(data["results"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No data found for this query.")

            if data.get("suggestion"):
                st.info(data["suggestion"])
                
            st.caption(f"Execution time: {data['execution_time_ms']}ms")

        else:
            error_msg = data.get("error", "Unknown error")
            st.error(f"Failed to process query: {error_msg}")

    except Exception as e:
        st.error(f"Could not connect to API: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)