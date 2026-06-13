import streamlit as st

# Page config - MUST BE FIRST Streamlit command
st.set_page_config(page_title="RAG Chatbot - Document Q&A", page_icon="📚", layout="wide")

st.title("📚 RAG Chatbot - Ask Questions About Your Documents")
st.markdown("Upload PDF files and ask questions about their content.")

# Test to see if app is loading
st.write("✅ App is loading! If you see this, the basic app works.")

# Simple file uploader test
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    st.info("PDF processing will be added. For now, this confirms the UI works!")