# backend.py

import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import uvicorn

load_dotenv()

# --- Pydantic Models ---

class ProcessResponse(BaseModel):
    session_id: str
    message: str

class SourceDocument(BaseModel):
    page_content: str
    metadata: Dict

class ChatResponse(BaseModel):
    answer: str
    source_documents: List[SourceDocument]

# --- FastAPI Initialization ---
app = FastAPI()

# CORS for Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation state per session
conversations: Dict[str, ConversationalRetrievalChain] = {}

# --- Helper Methods ---

def get_pdf_text(pdf_files: List[UploadFile]) -> str:
    text = ""
    for pdf in pdf_files:
        try:
            pdf_reader = PdfReader(pdf.file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            print(f"Error reading {pdf.filename}: {e}")
    return text

def get_text_chunks(text: str) -> List[str]:
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)

def get_vectorstore(chunks: List[str]) -> Chroma:
    embeddings = OpenAIEmbeddings()
    return Chroma.from_texts(chunks, embedding=embeddings)

def get_conversation_chain(vectorstore: Chroma) -> ConversationalRetrievalChain:
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True, output_key="answer"
    )
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=True,
        output_key="answer"
    )

# --- API Endpoints ---

@app.post("/process-pdfs", response_model=ProcessResponse)
async def process_pdfs(files: List[UploadFile] = File(...)):
    try:
        text = get_pdf_text(files)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from PDFs.")

        chunks = get_text_chunks(text)
        vectorstore = get_vectorstore(chunks)
        chain = get_conversation_chain(vectorstore)

        session_id = str(uuid.uuid4())
        conversations[session_id] = chain

        return {"session_id": session_id, "message": "PDFs processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(session_id: str = Form(...), user_question: str = Form(...)):
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Invalid session ID.")
    try:
        chain = conversations[session_id]
        result = chain({"question": user_question})
        return {
            "answer": result["answer"],
            "source_documents": result["source_documents"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
