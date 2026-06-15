# 📚 RAG Chatbot - Ask Questions About Your PDFs

**Built by Aikaksh Singh Routela**

A powerful Retrieval-Augmented Generation (RAG) chatbot that allows you to upload PDF documents and ask questions about their content. The AI answers based ONLY on your uploaded documents.

## 🚀 Live Demo
[Click here to try the live app](https://huggingface.co/spaces/Aikaksh-Singh-Routela/rag-chatbot-pdf)

## 📂 GitHub Repository
[https://github.com/Aikaksh-Singh-Routela/rag-chatbot-streamlit-final](https://github.com/Aikaksh-Singh-Routela/rag-chatbot-streamlit-final)

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **LLM**: Groq (llama-3.1-8b-instant)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB
- **PDF Processing**: PyPDF2 / pdfplumber
- **Deployment**: Hugging Face Spaces

## ✨ Features
- 📄 Upload multiple PDF files
- 💬 Ask questions in natural language
- 🎯 Answers based ONLY on your documents (no hallucinations)
- 📚 Semantic search using embeddings
- 🔗 Source citations from your documents

## 📊 How It Works

1. **Upload** your PDF documents
2. **Process** - Text is extracted and split into chunks
3. **Index** - Each chunk is converted to embeddings and stored in ChromaDB
4. **Search** - When you ask a question, relevant chunks are retrieved
5. **Generate** - Groq LLM answers based ONLY on the retrieved context

## 📝 Example Queries

| Query | Response |
|-------|----------|
| "What is this document about?" | Summary of the PDF |
| "What are the main findings?" | Key points from the document |
| "Summarize the conclusion" | Conclusion section summary |

## 🔐 Environment Variables (For local deployment)
- `GROQ_API_KEY` - Your Groq API key

## 📁 Project Structure
rag-chatbot/
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── README.md # Documentation
└── .streamlit/
└── secrets.toml # API keys (gitignored)

text

## 🚀 Local Setup

```bash
# Clone the repository
git clone https://github.com/Aikaksh-Singh-Routela/rag-chatbot-streamlit-final.git
cd rag-chatbot-streamlit-final

# Install dependencies
pip install -r requirements.txt

# Create secrets file
mkdir .streamlit
echo "GROQ_API_KEY = \"your-key-here\"" > .streamlit/secrets.toml

# Run the app
streamlit run app.py
👨‍💻 Author
Aikaksh Singh Routela

📅 Build History
Built RAG chatbot with Streamlit

Integrated Groq LLM for accurate answers

Added ChromaDB for vector search

Deployed to Hugging Face Spaces

📎 Related Projects
AI Assistant - Web Search & Math

AI Image Generator
