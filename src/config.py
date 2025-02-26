import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq


def load_config():
    """Load environment variables from .env."""
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY  # Ensure key is available globally


def load_models_and_data():
    """Initialize embedding model, document retriever and LLM."""
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    pdf_paths = [
        "data/SNBC-2_complete.pdf",
        "data/Corporate_Sustainability_Strategy.pdf",
    ]
    docs = [PyPDFLoader(path).load() for path in pdf_paths]
    docs_list = [item for sublist in docs for item in sublist]

    # Split documents into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    doc_splits = text_splitter.split_documents(docs_list)

    # Create and persist a Chroma vector store
    chroma_vector_store = Chroma.from_documents(
        documents=doc_splits,
        embedding=embedding_model,
        persist_directory="./chroma_db",
    )
    retriever = chroma_vector_store.as_retriever()

    # Initialize the LLM
    llm = ChatGroq(model_name="mixtral-8x7b-32768")

    return embedding_model, retriever, llm
