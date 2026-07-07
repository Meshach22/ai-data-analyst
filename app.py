import streamlit as st
import pandas as pd
from claude_analyzer import analyze_with_claude

# Page config
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 AI Data Analyst")
st.markdown("Upload a CSV and ask questions. Claude AI will analyze and suggest visualizations.")

# Sidebar info
with st.sidebar:
    st.header("How it works")
    st.markdown("""
    1. **Upload** a CSV file
    2. **Ask** questions about your data
    3. **Get** Claude's analysis + visualization suggestion
    4. **Learn** insights from your data
    """)

# Initialize session state (memory)
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "df" not in st.session_state:
    st.session_state.df = None

# FILE UPLOAD SECTION
st.subheader("📁 Upload Your Data")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Load and display CSV
if uploaded_file:
    try:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded: {len(st.session_state.df)} rows, {len(st.session_state.df.columns)} columns")
        
        # Show data preview
        with st.expander("📊 View Data Preview"):
            st.dataframe(st.session_state.df.head())
    
    except Exception as e:
        st.error(f"Error loading file: {e}")

# CHAT SECTION
if st.session_state.df is not None:
    st.markdown("---")
    st.subheader("💬 Ask Claude About Your Data")
    
    # Display chat history
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])
    
    # Get user input
    user_question = st.chat_input("Ask a question about your data...")
    
    if user_question:
        # Show user's question
        with st.chat_message("user"):
            st.write(user_question)
        
        # Get Claude's analysis
        with st.spinner("🤖 Claude is analyzing..."):
            try:
                analysis, st.session_state.conversation_history = analyze_with_claude(
                    st.session_state.df,
                    user_question,
                    st.session_state.conversation_history
                )
                
                # Show Claude's response
                with st.chat_message("assistant"):
                    st.write(analysis)
            
            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.info("👈 Upload a CSV file to get started!")