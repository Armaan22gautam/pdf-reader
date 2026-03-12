import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Look for .env in the parent directory if not in the current directory
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

# We will store the vectorstore in memory for this session, but it can be persisted using doc search
VECTOR_STORE_PATH = "faiss_index"
embedding_model = None
vector_store = None
llm = None

def init_models():
    """Initialize models lazily or upfront."""
    global embedding_model, llm, vector_store
    
    if embedding_model is None:
        print("Loading embedding model...")
        embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if llm is None:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            print("CRITICAL: GOOGLE_API_KEY not found in environment variables!")
        else:
            print(f"Loading LLM with API key starting with: {google_api_key[:8]}...")
            
        # Default to 'gemini-1.5-flash' but allow override via .env
        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
        
        llm = ChatGoogleGenerativeAI(
            model=model_name, 
            google_api_key=google_api_key,
            temperature=0
        )
        
    # Try to load existing FAISS index if it exists
    if os.path.exists(VECTOR_STORE_PATH) and vector_store is None:
        print("Loading FAISS index...")
        try:
            vector_store = FAISS.load_local(VECTOR_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"Failed to load FAISS index: {e}")

def process_document(file_path: str):
    """
    Extract text from PDF, chunk it, create embeddings, and store in FAISS.
    """
    global vector_store, embedding_model
    init_models()
    
    print(f"Processing document: {file_path}")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split document into {len(chunks)} chunks.")
    
    if vector_store is None:
        vector_store = FAISS.from_documents(chunks, embedding_model)
    else:
        vector_store.add_documents(chunks)
        
    vector_store.save_local(VECTOR_STORE_PATH)
    return {"message": "Document processed and stored successfully", "chunks_count": len(chunks)}

def answer_question(question: str):
    """
    Perform similarity search and ask LLM using LangChain.
    """
    global vector_store
    init_models()
    
    if vector_store is None:
        return {"answer": "No documents have been uploaded yet. Please upload a PDF first."}
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    
    system_prompt = (
        "Use the following pieces of context to answer the question.\n"
        "If you don't know the answer based on the context, just say that you don't know.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    try:
        response = rag_chain.invoke({"input": question})
        return {
            "answer": response["answer"],
            "context": [doc.page_content for doc in response["context"]]
        }
    except Exception as e:
        print(f"Error generating answer: {e}")
        return {"answer": f"I encountered an error while trying to generate an answer: {str(e)}", "context": []}
