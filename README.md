# PDF Chatbot with FastAPI & Streamlit

This project allows users to upload PDF files, processes them using LangChain and OpenAI embeddings, and enables interactive Q&A with the content using a conversational retrieval chain. The frontend is built with Streamlit and connects to a FastAPI backend.

---

## Features

- Upload and process one or more PDFs
- Chat interface to ask questions about PDF content
- Uses OpenAI embeddings + ChromaDB for retrieval
- Conversational memory using LangChain
- Stylish frontend with Streamlit

---

## Project Structure

```
.
├── app.py               # Streamlit frontend
├── backend.py           # FastAPI backend
├── htmlTemplates.py     # HTML + CSS templates for chat display
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not included)
├── .gitignore           # Git ignored files (not included)
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pdf-chatbot.git
cd pdf-chatbot
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add `.env` File

Create a `.env` file with your OpenAI key:

```
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the Backend

```bash
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

### 6. Run the Frontend

In another terminal:

```bash
streamlit run app.py
```

---

## Tech Stack

- **FastAPI** – Backend APIs
- **Streamlit** – Frontend UI
- **LangChain** – Text splitting, embeddings, and conversation memory
- **OpenAI** – Embeddings & LLM
- **ChromaDB** – Vector store
- **PyPDF2** – PDF parsing

---

## License

MIT License

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://platform.openai.com/)
- [ChromaDB](https://www.trychroma.com/)
