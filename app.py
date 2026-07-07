import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from claude_analyzer import analyze_with_claude

# Page config
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 AI Data Analyst")
st.markdown("Upload a CSV and ask questions. Llama AI will analyze and suggest visualizations.")

# Sidebar info
with st.sidebar:
    st.header("How it works")
    st.markdown("""
    1. **Upload** a CSV file
    2. **Ask** questions about your data
    3. **Get** AI analysis + visualization suggestion
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
    st.subheader("💬 Ask AI About Your Data")
    
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
        
        # Get AI analysis
        with st.spinner("🤖 AI is analyzing..."):
            try:
                analysis, st.session_state.conversation_history = analyze_with_claude(
                    st.session_state.df,
                    user_question,
                    st.session_state.conversation_history
                )
                
                # Show AI's response
                with st.chat_message("assistant"):
                    st.write(analysis)
            
            except Exception as e:
                st.error(f"Error: {e}")

    # VISUALIZATION SECTION (always visible once data is loaded and at least one question asked)
    if st.session_state.conversation_history:
        st.markdown("---")
        st.markdown("### 📊 Generate a Chart")
        
        numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_col = st.selectbox(
                    "Choose a column to visualize:",
                    numeric_cols,
                    key="col_select"
                )
            with col2:
                chart_type = st.selectbox(
                    "Chart type:",
                    ["Histogram", "Box Plot"],
                    key="chart_type"
                )
            
            if st.button("Generate Chart", key="gen_chart"):
                fig, ax = plt.subplots(figsize=(8, 4))
                if chart_type == "Histogram":
                    ax.hist(st.session_state.df[selected_col], bins=10, color='#4C9AFF', edgecolor='white')
                    ax.set_xlabel(selected_col)
                    ax.set_ylabel("Frequency")
                    ax.set_title(f"Distribution of {selected_col}")
                else:
                    ax.boxplot(st.session_state.df[selected_col].dropna())
                    ax.set_ylabel(selected_col)
                    ax.set_title(f"Box Plot of {selected_col}")
                
                st.pyplot(fig)
        else:
            st.info("No numeric columns available to visualize.")

else:
    st.info("👈 Upload a CSV to get started!")

# Footer
st.markdown("---")
st.markdown("<small style='color:gray'>Made with Streamlit + Groq AI</small>", unsafe_allow_html=True)