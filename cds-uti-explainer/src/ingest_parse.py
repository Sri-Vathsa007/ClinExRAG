import json
from pathlib import Path
from pypdf import PdfReader

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

def write_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def parse_pdf(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    docs = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = "\n".join([ln.strip() for ln in text.splitlines() if ln.strip()])
        if not text:
            continue

        docs.append({
            "doc_id": "nice_ng109_visual_summary",
            "source": "NICE",
            "url": "https://www.nice.org.uk/guidance/ng109/resources/visual-summary-pdf-6544021069",
            "jurisdiction": "UK",
            "topic": "lower_uti_antimicrobial",
            "section": f"page_{i+1}",
            "text": text
        })
    return docs

def main():
    pdf_path = RAW / "nice_ng109_visual_summary.pdf"
    docs = parse_pdf(pdf_path)
    out = PROCESSED / "raw_docs.jsonl"
    write_jsonl(out, docs)
    print("Wrote:", out, "docs:", len(docs))

if __name__ == "__main__":
    main()
