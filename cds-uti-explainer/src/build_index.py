import json
from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

load_dotenv()

PROCESSED = Path("data/processed")
INDEX_DIR = Path("indexes/faiss")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

def main():
    docs = []
    for r in load_jsonl(PROCESSED / "chunks.jsonl"):
        meta = {
            "chunk_id": r["chunk_id"],
            "doc_id": r["doc_id"],
            "source": r["source"],
            "url": r["url"],
            "jurisdiction": r["jurisdiction"],
            "topic": r["topic"],
            "section": r["section"],
        }
        docs.append(Document(page_content=r["text"], metadata=meta))

    emb = OpenAIEmbeddings(model="text-embedding-3-large")  # :contentReference[oaicite:8]{index=8}
    store = FAISS.from_documents(docs, emb)
    store.save_local(str(INDEX_DIR))
    print("Saved FAISS index to:", INDEX_DIR)

if __name__ == "__main__":
    main()
