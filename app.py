import streamlit as st
import pandas as pd
import time
import requests

st.set_page_config(page_title="Gengo", layout="wide")

# Ensure your correct Heroku URL is here
API_URL = "https://gengo-backend-api-b89286ea64a6.herokuapp.com/query"

# 🎨 GLOBAL STYLE
st.markdown("""
<style>
/* Remove default Streamlit padding */
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}

header {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: #f5f1eb;
    font-family: 'Segoe UI', sans-serif;
}

/* NAVBAR */
.navbar {
    background: #0f172a;
    padding: 24px 60px;
    width: 100%;
    margin-bottom: 40px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.logo {
    font-size: 30px;
    font-weight: 700;
    color: white;
    letter-spacing: 2px;
}

/* HERO SECTION */
.hero-wrapper {
    padding: 60px;
    max-width: 900px;
}

.hero-title {
    font-size: 64px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 10px;
}

.hero-sub {
    font-size: 24px;
    font-weight: 500;
    color: #374151;
    margin-bottom: 20px;
}

.hero-desc {
    font-size: 18px;
    color: #4b5563;
    line-height: 1.6;
    margin-bottom: 40px;
}

/* BUTTONS */
div.stButton > button {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 30px;
    padding: 12px 30px;
    font-weight: 600;
    border: none;
    transition: 0.3s all ease;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.3);
}

/* CUSTOM BOXES */
.box {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    color: #111827;
}

.sql-box {
    background: #0d1117;
    color: #c9d1d9;
    padding: 20px;
    border-radius: 12px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 16px;
    margin-bottom: 20px;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 15px;
}

/* REMOVE WHITE HEADINGS FROM STREAMLIT */
h1, h2, h3, p {
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)

# 1. NAVBAR
st.markdown('<div class="navbar"><div class="logo">GENGO</div></div>', unsafe_allow_html=True)

# 2. HERO
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-title">Welcome</div>
    <div class="hero-sub">Query your database in plain English</div>
    <div class="hero-desc">
        Gengo is an AI-powered system that converts natural language into SQL queries, executes them, and returns results instantly.
    </div>
</div>
""", unsafe_allow_html=True)

# 3. INTERACTIVE SECTION
with st.container():
    st.markdown('<div style="padding: 0 60px;">', unsafe_allow_html=True)
    
    # WHAT/WHY INFO
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">What Gengo Does</div>', unsafe_allow_html=True)
        st.write("Converts plain English into SQL and executes it instantly on your legacy database.")
    
    with col2:
        st.markdown('<div class="section-title">Why It Matters</div>', unsafe_allow_html=True)
        st.write("Ensures non-technical users can access data without waiting for SQL experts.")

    st.divider()

    # THE CORE APP
    st.markdown("## Try it now", help="Type a question below to query the database")
    
    # QUICK SUGGESTIONS
    c1, c2, c3 = st.columns(3)
    if c1.button("Customers from New York"):
        st.session_state.prefill = "Show customers from New York"
    if c2.button("Top customers"):
        st.session_state.prefill = "Show top 5 customers by balance"
    if c3.button("All customers"):
        st.session_state.prefill = "List all customers"

    # THE FORM (CORE INTERACTION)
    with st.form("query_form", clear_on_submit=False):
        user_input = st.text_input("Ask a question about your data...", value=st.session_state.get("prefill", ""))
        use_fallback = st.checkbox("Use Fallback AI (Ollama)", value=False)
        submitted = st.form_submit_button("Generate SQL")

    # RESULTS LOGIC
    if submitted and user_input:
        with st.spinner("🤖 Generating SQL and fetching results..."):
            try:
                # Call Heroku Backend
                response = requests.post(API_URL, json={
                    "question": user_input,
                    "use_fallback": use_fallback
                }, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("error"):
                        st.error(f"Logic Error: {data['error']}")
                    else:
                        st.success("Query executed successfully!")
                        
                        st.markdown("### ⚙️ Generated SQL")
                        st.markdown(f'<div class="sql-box">{data["sql"]}</div>', unsafe_allow_html=True)

                        if data.get("results"):
                            st.markdown(f"### 📊 Results ({len(data['results'])} rows)")
                            st.dataframe(pd.DataFrame(data["results"]), use_container_width=True)
                        else:
                            st.info("No matching records found in the database.")

                        if data.get("suggestion"):
                            st.info(data["suggestion"])
                        
                        st.caption(f"Execution Time: {data['execution_time_ms']}ms")
                else:
                    st.error(f"Backend Server Error ({response.status_code})")
            
            except Exception as e:
                st.error(f"Connection Failed: Ensure your Heroku backend is up and awake. Error: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)