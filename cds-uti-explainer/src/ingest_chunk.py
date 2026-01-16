import json
import hashlib
from pathlib import Path
from typing import Dict, List

PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

MAX_CHARS = 2400   # simple chunking; good enough for PDF text
OVERLAP = 250

def load_jsonl(path: Path) -> List[Dict]:
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            out.append(json.loads(line))
    return out

def write_jsonl(path: Path, rows: List[Dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def stable_id(*parts: str) -> str:
    h = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:16]
    return h

def chunk_text(text: str) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + MAX_CHARS)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - OVERLAP
        if start < 0:
            start = 0
        if end == len(text):
            break
    return chunks

def main():
    raw_docs = load_jsonl(PROCESSED / "raw_docs.jsonl")
    chunks = []
    for d in raw_docs:
        for idx, ch in enumerate(chunk_text(d["text"])):
            cid = stable_id(d["doc_id"], d["section"], str(idx), ch[:40])
            chunks.append({
                "chunk_id": cid,
                "doc_id": d["doc_id"],
                "source": d["source"],
                "url": d["url"],
                "jurisdiction": d["jurisdiction"],
                "topic": d["topic"],
                "section": d["section"],
                "text": ch
            })

    out = PROCESSED / "chunks.jsonl"
    write_jsonl(out, chunks)
    print("Wrote:", out, "chunks:", len(chunks))

if __name__ == "__main__":
    main()
