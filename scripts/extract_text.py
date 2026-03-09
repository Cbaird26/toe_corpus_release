#!/usr/bin/env python3
"""
Extract text from PDF, DOCX, TEX, MD into 01_ingest/extracted_txt/{doc_id}.txt
Preserves page breaks where possible.
"""
import csv
import re
import subprocess
import sys
from pathlib import Path

try:
    import fitz  # pymupdf
except ImportError:
    fitz = None

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None


def extract_pdf_pymupdf(path: Path) -> str:
    if not fitz:
        raise ImportError("pymupdf required: pip install pymupdf")
    doc = fitz.open(path)
    parts = []
    for i, page in enumerate(doc):
        text = page.get_text()
        parts.append(f"\n\n--- PAGE {i + 1} ---\n\n{text}")
    doc.close()
    return "".join(parts)


def extract_pdf_pdftotext(path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {result.stderr}")
    return result.stdout or ""


def extract_pdf(path: Path) -> str:
    if fitz:
        return extract_pdf_pymupdf(path)
    try:
        return extract_pdf_pdftotext(path)
    except FileNotFoundError:
        raise RuntimeError("Need pymupdf (pip install pymupdf) or pdftotext (poppler-utils)")


def extract_docx(path: Path) -> str:
    if not DocxDocument:
        try:
            result = subprocess.run(
                ["pandoc", str(path), "-t", "plain", "--wrap=none"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                return result.stdout
        except FileNotFoundError:
            pass
        raise ImportError("python-docx required: pip install python-docx")
    doc = DocxDocument(path)
    parts = []
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def extract_tex(path: Path) -> str:
    """Strip comments and extract content between \\begin{document} and \\end{document}."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"%.*$", "", raw, flags=re.MULTILINE)
    m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", raw, re.DOTALL)
    if m:
        content = m.group(1)
    else:
        content = raw
    content = re.sub(r"\\[a-zA-Z]+\*?(\{[^}]*\})*(\[[^\]]*\])*", " ", content)
    content = re.sub(r"\s+", " ", content).strip()
    return content


def extract_md(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def main():
    repo = Path(__file__).resolve().parent.parent
    manifest_path = repo / "00_manifest" / "corpus_manifest.csv"
    out_dir = repo / "01_ingest" / "extracted_txt"
    out_dir.mkdir(parents=True, exist_ok=True)
    log = []

    with open(manifest_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    log.append(f"Loaded {len(rows)} rows from manifest")

    for row in rows:
        doc_id = row["doc_id"]
        path = Path(row["source_path"])
        if not path.is_absolute():
            path = (repo.parent / path).resolve()
        if not path.exists():
            print(f"Skip {doc_id}: {path} not found")
            continue

        out_file = out_dir / f"{doc_id}.txt"
        try:
            ext = path.suffix.lower()
            if ext == ".pdf":
                text = extract_pdf(path)
            elif ext in (".docx", ".doc"):
                text = extract_docx(path)
            elif ext == ".tex":
                text = extract_tex(path)
            elif ext == ".md":
                text = extract_md(path)
            else:
                text = path.read_text(encoding="utf-8", errors="replace")

            out_file.write_text(text, encoding="utf-8")
            log.append(f"Extracted {doc_id}")
            print(f"Extracted {doc_id}")
        except Exception as e:
            log.append(f"Error {doc_id}: {e}")
            print(f"Error {doc_id}: {e}", file=sys.stderr)

    (repo / "00_manifest" / "extract_log.txt").write_text("\n".join(log), encoding="utf-8")


if __name__ == "__main__":
    main()
