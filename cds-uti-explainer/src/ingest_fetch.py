from pathlib import Path
import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

# NICE_VISUAL_SUMMARY_PDF = "https://www.nice.org.uk/guidance/ng109/resources/visual-summary-pdf-6544021069"  # :contentReference[oaicite:5]{index=5}

# def download(url: str, out_path: Path) -> None:
#     resp = requests.get(url, timeout=60)
#     resp.raise_for_status()
#     out_path.write_bytes(resp.content)

# def main():
#     pdf_path = RAW / "nice_ng109_visual_summary.pdf"
#     download(NICE_VISUAL_SUMMARY_PDF, pdf_path)
#     print("Downloaded:", pdf_path)

# if __name__ == "__main__":
#     main()
