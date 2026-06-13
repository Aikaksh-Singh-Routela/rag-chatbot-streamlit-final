import streamlit as st
import os
import tempfile
from PyPDF2 import PdfReader
import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq

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
if "collection_name" not in st.session_state:
    st.session_state.collection_name = "documents"

# Initialize Groq client using Streamlit Cloud Secrets
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    groq_client = None
    st.error(f"Please add GROQ_API_KEY to your Streamlit Cloud secrets. Error: {str(e)}")

# Initialize embedding model
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def load_chroma_client():
    return chromadb.PersistentClient(path="./chroma_db")

def extract_text_from_pdf(file):
    """Extract text from uploaded PDF file"""
    text = ""
    try:
        # Save uploaded file to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_path = tmp_file.name
        
        # Try pdfplumber first (better for complex PDFs)
        try:
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except:
            # Fallback to PyPDF2
            with open(tmp_path, 'rb') as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        # Clean up temp file
        os.unlink(tmp_path)
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
    
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def create_vector_store(chunks, embedding_model, collection_name="documents"):
    """Create ChromaDB collection from text chunks"""
    chroma_client = load_chroma_client()
    
    # Delete existing collection if it exists
    try:
        chroma_client.delete_collection(collection_name)
    except:
        pass
    
    # Create new collection
    collection = chroma_client.create_collection(name=collection_name)
    
    # Generate embeddings and add to collection
    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[f"chunk_{i}"]
        )
    
    return collection

def search_documents(query, collection, embedding_model, top_k=5):
    """Search for relevant chunks"""
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results['documents'][0] if results['documents'] else []

def generate_answer(query, context_chunks, groq_client):
    """Generate answer using Groq LLM"""
    context = "\n\n---\n\n".join(context_chunks)
    
    prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided context.

Context:
{context}

Question: {query}

Instructions:
1. Answer based ONLY on the context above
2. If the answer is not in the context, say "I cannot find this information in the uploaded documents"
3. Be concise and accurate
4. Use the same language as the question

Answer:"""
    
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# Sidebar for file upload
with st.sidebar:
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("📚 Process Documents", type="primary"):
        with st.spinner("Processing documents..."):
            all_text = ""
            progress_bar = st.progress(0)
            
            for i, file in enumerate(uploaded_files):
                text = extract_text_from_pdf(file)
                if text:
                    all_text += text + "\n\n"
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            if all_text.strip():
                chunks = chunk_text(all_text)
                embedding_model = load_embedding_model()
                collection = create_vector_store(chunks, embedding_model, st.session_state.collection_name)
                st.session_state.vector_store = collection
                st.session_state.documents_loaded = True
                st.success(f"✅ Processed {len(uploaded_files)} file(s) - {len(chunks)} chunks created")
            else:
                st.error("Could not extract text from PDFs. Make sure they contain selectable text.")
    
    if st.session_state.documents_loaded:
        st.success("📚 Documents ready for questions!")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    st.markdown("### 📝 Example Questions")
    st.markdown("- What is this document about?")
    st.markdown("- Summarize the main points")
    st.markdown("- What are the key findings?")
    st.markdown("- Who is the target audience?")

# Main chat interface
st.subheader("💬 Ask Questions About Your Documents")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        if not st.session_state.documents_loaded:
            response = "📄 Please upload documents first using the sidebar on the left."
        elif groq_client is None:
            response = "🔑 Please add your GROQ_API_KEY to the Streamlit Cloud secrets in Settings."
        else:
            with st.spinner("🔍 Searching documents and generating answer..."):
                embedding_model = load_embedding_model()
                relevant_chunks = search_documents(prompt, st.session_state.vector_store, embedding_model)
                if relevant_chunks:
                    response = generate_answer(prompt, relevant_chunks, groq_client)
                else:
                    response = "No relevant information found in the uploaded documents. Try rephrasing your question."
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})