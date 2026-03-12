# PDF-Reader

A RAG-based PDF chatbot application with a FastAPI backend and a Streamlit frontend.

## Project Structure

- `backend/`: FastAPI server and RAG engine.
- `frontend/`: Streamlit user interface.
- `list_models.py`: Utility script for listing available models.

## Features

- **PDF Processing**: Upload and process PDF documents for question answering.
- **RAG Engine**: Uses Retrieval-Augmented Generation for accurate responses.
- **Modern UI**: Built with Streamlit for a smooth user experience.
- **FastAPI Backend**: High-performance backend processing.

1. Configure your `.env` file in the root directory.
2. Install backend dependencies: `pip install -r backend/requirements.txt`.
3. Install frontend dependencies: `pip install -r frontend/requirements.txt`.
4. Run the backend: `python backend/main.py`.
5. Run the frontend: `streamlit run frontend/app.py`.
