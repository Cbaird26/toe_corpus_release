#!/usr/bin/env python3
"""
Split normalized text into 10-page chunks.
Pages approximated as LINES_PER_PAGE lines (configurable).
Output: 02_chunks/{doc_id}/chunk_{NNN}_pages_{XXX}-{YYY}.txt
"""
import csv
from pathlib import Path

LINES_PER_PAGE = 60
PAGES_PER_CHUNK = 10


def main():
    repo = Path(__file__).resolve().parent.parent
    manifest_path = repo / "00_manifest" / "corpus_manifest.csv"
    in_dir = repo / "01_ingest" / "normalized_txt"
    out_base = repo / "02_chunks"

    with open(manifest_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        doc_id = row["doc_id"]
        in_file = in_dir / f"{doc_id}.txt"
        if not in_file.exists():
            print(f"Skip {doc_id}: no normalized text")
            continue

        lines = in_file.read_text(encoding="utf-8", errors="replace").splitlines()
        total_lines = len(lines)
        total_pages = max(1, (total_lines + LINES_PER_PAGE - 1) // LINES_PER_PAGE)

        doc_dir = out_base / doc_id
        doc_dir.mkdir(parents=True, exist_ok=True)

        chunk_num = 0
        for start_page in range(1, total_pages + 1, PAGES_PER_CHUNK):
            end_page = min(start_page + PAGES_PER_CHUNK - 1, total_pages)
            start_line = (start_page - 1) * LINES_PER_PAGE
            end_line = min(end_page * LINES_PER_PAGE, total_lines)
            chunk_lines = lines[start_line:end_line]
            chunk_text = "\n".join(chunk_lines)

            chunk_num += 1
            out_name = f"chunk_{chunk_num:03d}_pages_{start_page:03d}-{end_page:03d}.txt"
            out_file = doc_dir / out_name
            out_file.write_text(chunk_text, encoding="utf-8")
            print(f"Chunk {doc_id}: {out_name}")

    print("Done. Run Cursor Cloud agents for chunk analysis (chunk_XXX_analysis.json).")


if __name__ == "__main__":
    main()
