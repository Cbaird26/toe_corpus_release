#!/usr/bin/env python3
"""
Normalize extracted text: dehyphenation, header/footer cleanup, OCR junk.
Light edits only — no claim smoothing.
"""
import csv
import re
from pathlib import Path


def dehyphenate(text: str) -> str:
    """Fix end-of-line hyphenation."""
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.endswith("-") and i + 1 < len(lines) and len(line) > 2:
            next_line = lines[i + 1].lstrip()
            if next_line and not next_line.startswith("-"):
                out.append(line[:-1] + next_line.split()[0] if next_line.split() else line[:-1])
                rest = " ".join(next_line.split()[1:]) if len(next_line.split()) > 1 else ""
                if rest:
                    lines[i + 1] = rest
                else:
                    i += 1
                i += 1
                continue
        out.append(line)
        i += 1
    return "\n".join(out)


def clean_headers_footers(text: str) -> str:
    """Remove common header/footer patterns."""
    patterns = [
        r"^\s*\d+\s*$",  # page number alone
        r"^—\s*\d+\s*—\s*$",
        r"^--- PAGE \d+ ---$",  # keep our markers but could simplify
    ]
    lines = text.split("\n")
    out = []
    for line in lines:
        stripped = line.strip()
        if any(re.match(p, stripped) for p in patterns[:2]):
            continue
        out.append(line)
    return "\n".join(out)


def clean_ocr_junk(text: str) -> str:
    """Remove obvious OCR artifacts."""
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    text = re.sub(r"\f", "\n\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def normalize(text: str) -> str:
    text = clean_ocr_junk(text)
    text = dehyphenate(text)
    text = clean_headers_footers(text)
    return text


def main():
    repo = Path(__file__).resolve().parent.parent
    manifest_path = repo / "00_manifest" / "corpus_manifest.csv"
    in_dir = repo / "01_ingest" / "extracted_txt"
    out_dir = repo / "01_ingest" / "normalized_txt"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        doc_id = row["doc_id"]
        in_file = in_dir / f"{doc_id}.txt"
        if not in_file.exists():
            print(f"Skip {doc_id}: no extracted text")
            continue

        text = in_file.read_text(encoding="utf-8", errors="replace")
        normalized = normalize(text)
        out_file = out_dir / f"{doc_id}.txt"
        out_file.write_text(normalized, encoding="utf-8")
        print(f"Normalized {doc_id}")


if __name__ == "__main__":
    main()
