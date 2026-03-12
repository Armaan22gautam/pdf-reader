# PDF-Reader

A RAG-based PDF chatbot application with a FastAPI backend and a Streamlit frontend.

## Project Structure

- `backend/`: FastAPI server and RAG engine.
- `frontend/`: Streamlit user interface.
- `list_models.py`: Utility script for listing available models.

## Setup

1. Configure your `.env` file in the root directory.
2. Install backend dependencies: `pip install -r backend/requirements.txt`.
3. Install frontend dependencies: `pip install -r frontend/requirements.txt`.
4. Run the backend: `python backend/main.py`.
5. Run the frontend: `streamlit run frontend/app.py`.
