import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(page_title="RAG Chatbot - Document Q&A", page_icon="📚", layout="wide")

st.title("📚 RAG Chatbot - Ask Questions About Your Documents")
st.markdown("Upload PDF files and ask questions about their content. The AI will answer based ONLY on your documents.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

# Import libraries
from PyPDF2 import PdfReader
import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq

# Initialize Groq client (using environment variable or secrets)
try:
    groq_client = Groq(api_key=st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY")))
except:
    groq_client = None

# Rest of your working code...