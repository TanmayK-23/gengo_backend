import streamlit as st
import pandas as pd
import time
import requests

st.set_page_config(page_title="GENGO - Your AI Data Analyst", layout="wide", initial_sidebar_state="collapsed")

API_URL = "https://gengo-backend-api-b89286ea64a6.herokuapp.com/query"

st.markdown("""
<style>
/* Import a premium modern font */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;800&display=swap');

html, body, [class*="css"], p, span, div {
    font-family: 'Outfit', sans-serif;
}

/* Force dark text for readability against the light background */
p, li, span.st-emotion-cache-10trblm, markdown-text-container {
    color: #0f172a !important; 
}

/* Base App Background - Clean Light Gradient */
.stApp {
    background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
}

/* Hide Default Streamlit UI elements */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Custom padding for wide layout so it doesn't hug edges entirely */
.block-container {
    padding-left: 5% !important;
    padding-right: 5% !important;
    padding-top: 2rem !important;
}

/* Headings */
h1 {
    font-size: 4rem !important;
    font-weight: 800 !important;
    background: -webkit-linear-gradient(45deg, #0f172a, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px !important;
    padding-bottom: 5px;
}
h2 {
    font-size: 2.2rem !important;
    font-weight: 600 !important;
    color: #1e293b !important;
}
h3 {
    font-size: 1.5rem !important;
    color: #1e293b !important;
}

/* Subtext */
.subtitle {
    font-size: 1.3rem;
    color: #334155 !important;
    font-weight: 500;
    margin-bottom: 40px;
}

/* All Buttons (Force Dark Background & White Text) */
div.stButton > button, 
div.stFormSubmitButton > button, 
div.stDownloadButton > button {
    background-color: #0f172a !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.2) !important;
    width: 100%;
}

div.stButton > button:hover, 
div.stFormSubmitButton > button:hover, 
div.stDownloadButton > button:hover {
    background-color: #1e293b !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(15, 23, 42, 0.3) !important;
}

/* Explicitly force paragraph and span text inside all buttons to be white */
div.stButton > button p, div.stButton > button div, div.stButton > button span,
div.stFormSubmitButton > button p, div.stFormSubmitButton > button div, div.stFormSubmitButton > button span,
div.stDownloadButton > button p, div.stDownloadButton > button div, div.stDownloadButton > button span {
    color: #ffffff !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
}

/* Text Input Styling */
.stTextInput input {
    background: rgba(255, 255, 255, 0.8) !important;
    border: 1px solid rgba(15, 23, 42, 0.2) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
    font-size: 1.2rem !important;
    color: #0f172a !important;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.02) !important;
}

.stTextInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.3) !important;
}

/* Result Boxes */
.success-box {
    background: #d1fae5;
    border-left: 5px solid #10b981;
    padding: 15px 20px;
    border-radius: 8px;
    color: #065f46 !important;
    font-weight: 600;
    margin-bottom: 20px;
}

hr {
    border: 0;
    height: 1px;
    background: rgba(15,23,42,0.1);
    margin: 40px 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------
# UI LAYOUT
# -----------------

# Header Section
st.markdown("<h1>GENGO</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Query your legacy database in plain English. AI-powered SQL generation and execution.</p>', unsafe_allow_html=True)

# Three column highlights
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### No SQL Needed\nJust speak naturally and let AI do the work.")
with col2:
    st.markdown("### Blazing Fast\nInstant execution via Groq & Supabase.")
with col3:
    st.markdown("### Read-Only Safe\nBuilt to guarantee your data cannot be altered.")

st.markdown("<hr>", unsafe_allow_html=True)

# Main Interaction Area
st.markdown("<h2>Ask your Data</h2>", unsafe_allow_html=True)

# Suggestion Chips
st.markdown("<p style='font-weight: 500; margin-bottom: 10px;'>Try one of these to get started:</p>", unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)
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
        submitted = st.form_submit_button("Generate and Run SQL")

# Results Area
if submitted and user_input:
    with st.spinner("Analyzing your prompt and generating SQL..."):
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
                    st.error(f"Error: {data['error']}")
                else:
                    # Success
                    st.markdown('<div class="success-box">Query generated and executed successfully!</div>', unsafe_allow_html=True)
                    
                    st.markdown("### Generated SQL")
                    st.code(data["sql"], language="sql")
                    
                    if data.get("results"):
                        df = pd.DataFrame(data["results"])
                        
                        st.markdown(f"### Data Results ({len(data['results'])} rows)")
                        st.dataframe(df, use_container_width=True)
                        
                        # CSV Download Feature
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name='gengo_results.csv',
                            mime='text/csv',
                        )
                        
                        st.markdown("---")
                        st.markdown("### Visualisation")
                        
                        # Advanced auto-charting logic
                        num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                        cat_cols = df.select_dtypes(include=['object', 'string', 'datetime64']).columns.tolist()
                        
                        if len(num_cols) > 0:
                            if len(cat_cols) > 0:
                                # Best scenario: X is categorical (like a name/city), Y is numeric (like amount/count)
                                st.bar_chart(df, x=cat_cols[0], y=num_cols[0])
                            else:
                                # If pure numbers, a line chart looks better over an index
                                st.line_chart(df, y=num_cols[0])
                        else:
                            st.info("No numeric data found to visualize for this query.")
                            
                    else:
                        st.warning("No records found matching your query.")

                    if data.get("suggestion"):
                        st.info(data["suggestion"])
                    
                    st.caption(f"End-to-end processing time: {req_time}ms (DB execution: {data.get('execution_time_ms', 0)}ms)")
            
            else:
                st.error(f"Backend Server Error ({response.status_code}): Ensure your Heroku Dyno is awake.")
        
        except Exception as e:
            st.error(f"Connection Failed: Could not reach the API. Error details: `{str(e)}`")