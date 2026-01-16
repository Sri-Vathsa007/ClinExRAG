from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

INDEX_DIR = Path("indexes/faiss")

def load_store():
    emb = OpenAIEmbeddings(model="text-embedding-3-large")
    return FAISS.load_local(str(INDEX_DIR), emb, allow_dangerous_deserialization=True)

def retrieve_evidence(store, query: str, k: int = 6):
    # Similarity search only; you can add metadata filtering later
    return store.similarity_search(query, k=k)
