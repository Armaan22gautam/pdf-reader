import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PDF Chatbot (RAG)", page_icon="📄", layout="centered")

API_BASE_URL = "http://127.0.0.1:8001"

st.title("📄 PDF Chatbot (RAG)")
st.markdown("Upload your PDF and ask questions based on its content.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for PDF Upload
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if st.button("Process Document"):
        if uploaded_file is not None:
            with st.spinner("Processing PDF... (Extracting text, chunking, and embedding)"):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_BASE_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success(f"Successfully processed! Created {response.json().get('chunks_count')} chunks.")
                    else:
                        st.error(f"Error processing file: {response.text}")
                except Exception as e:
                    st.error(f"Could not connect to backend server. Is it running? Error: {e}")
        else:
            st.warning("Please upload a PDF file first.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is this document about?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Query backend API
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat", 
                json={"question": prompt}
            )
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found.")
                # Show assistant response
                with st.chat_message("assistant"):
                    st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Error querying API: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to backend server. Is it running? Error: {e}")
