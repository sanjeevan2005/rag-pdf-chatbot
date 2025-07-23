# app.py

import streamlit as st
import requests
from htmlTemplates import css, bot_template, user_template  # Custom styles & templates

# URL of your FastAPI backend
BACKEND_URL = "http://127.0.0.1:8000"

# --- User-Bot Interaction Handler --- #
def handle_user_input(question: str):
    session_id = st.session_state.session_id
    data = {"session_id": session_id, "user_question": question}

    # Show user question
    st.session_state.chat_history.append({"type": "user", "content": question})
    st.write(user_template.replace("{{MSG}}", question), unsafe_allow_html=True)

    with st.spinner("Thinking..."):
        try:
            response = requests.post(f"{BACKEND_URL}/chat", data=data)
            if response.status_code == 200:
                result = response.json()
                answer = result.get("answer", "Sorry, I don't have an answer.")
                sources = result.get("source_documents", [])

                # Show bot response
                st.session_state.chat_history.append({"type": "bot", "content": answer})
                st.write(bot_template.replace("{{MSG}}", answer), unsafe_allow_html=True)

                # Show source documents if available
                if sources:
                    with st.expander("Show sources"):
                        for i, doc in enumerate(sources):
                            st.markdown(f"**Chunk {i+1}:**")
                            st.write(doc['page_content'])

            else:
                st.error(f"Request failed: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Backend error: {e}")

# --- Streamlit App Layout --- #
def main():
    st.set_page_config(page_title="PDF Chatbot", page_icon="📚")
    st.title("Chat with PDFs 📚")

    # Inject custom CSS
    st.write(css, unsafe_allow_html=True)

    # Initialize session state
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        template = user_template if msg["type"] == "user" else bot_template
        st.write(template.replace("{{MSG}}", msg["content"]), unsafe_allow_html=True)

    # User question input
    user_input = st.chat_input("Ask a question about your PDFs...")
    if user_input and st.session_state.session_id:
        handle_user_input(user_input)

    # Sidebar: PDF upload
    with st.sidebar:
        st.subheader("Upload your PDFs")
        pdfs = st.file_uploader("Select PDF files", type=["pdf"], accept_multiple_files=True)

        if st.button("Process PDFs"):
            if pdfs:
                with st.spinner("Processing..."):
                    files = [("files", (pdf.name, pdf.getvalue(), pdf.type)) for pdf in pdfs]
                    try:
                        res = requests.post(f"{BACKEND_URL}/process-pdfs", files=files)
                        if res.status_code == 200:
                            result = res.json()
                            st.session_state.session_id = result["session_id"]
                            st.session_state.chat_history = []
                            st.success("PDFs processed! Ask your questions below.")
                        else:
                            st.error(f"Failed to process PDFs: {res.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {e}")
            else:
                st.warning("Please upload at least one PDF file.")

# Run the app
if __name__ == "__main__":
    main()
