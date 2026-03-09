#!/usr/bin/env python3
"""
Reconstruct papers from chunks.
- Reads chunk analysis JSON (if present) to group by proposed_destination_paper
- Otherwise groups by doc_id
- Writes 03_reconstruction/paper_{XXX}/reconstruction_full.md
- Also produces pull-page full and chronological editions
"""
import csv
import json
from pathlib import Path
from collections import defaultdict


def main():
    repo = Path(__file__).resolve().parent.parent
    manifest_path = repo / "00_manifest" / "corpus_manifest.csv"
    chunks_base = repo / "02_chunks"
    recon_base = repo / "03_reconstruction"
    pull_page_dir = repo / "editions" / "pull_page_full"
    chrono_dir = repo / "editions" / "chronological_full"
    norm_dir = repo / "01_ingest" / "normalized_txt"

    pull_page_dir.mkdir(parents=True, exist_ok=True)
    chrono_dir.mkdir(parents=True, exist_ok=True)
    recon_base.mkdir(parents=True, exist_ok=True)

    with open(manifest_path, encoding="utf-8") as f:
        manifest = list(csv.DictReader(f))

    # paper_id -> list of (doc_id, content, row)
    paper_content = defaultdict(list)

    for row in manifest:
        doc_id = row["doc_id"]
        norm_file = norm_dir / f"{doc_id}.txt"
        if not norm_file.exists():
            continue

        content = norm_file.read_text(encoding="utf-8", errors="replace")
        doc_chunks = chunks_base / doc_id

        paper_id = doc_id
        if doc_chunks.exists():
            analyses = list(doc_chunks.glob("*_analysis.json"))
            if analyses:
                try:
                    a = json.loads(analyses[0].read_text(encoding="utf-8"))
                    paper_id = a.get("proposed_destination_paper", doc_id)
                except Exception:
                    pass

        paper_content[paper_id].append((doc_id, content, row))

    # Reconstruction: merge content per paper
    for paper_id, items in paper_content.items():
        paper_dir = recon_base / f"paper_{paper_id}"
        paper_dir.mkdir(parents=True, exist_ok=True)

        parts = []
        source_entries = []
        for doc_id, content, row in sorted(items, key=lambda x: (x[2].get("date", ""), x[0])):
            parts.append(f"\n\n<!-- Source: {doc_id} -->\n\n{content}")
            source_entries.append(f"full,{doc_id},{row.get('source_path', '')}")

        recon_file = paper_dir / "reconstruction_full.md"
        recon_file.write_text(f"# {paper_id}\n\n" + "\n".join(parts), encoding="utf-8")
        (paper_dir / "source_map.csv").write_text(
            "chunk_or_full,doc_id,source_path\n" + "\n".join(source_entries),
            encoding="utf-8",
        )
        print(f"Reconstructed paper_{paper_id}")

    # Pull-page full: one file per doc, original order
    for row in manifest:
        doc_id = row["doc_id"]
        norm_file = norm_dir / f"{doc_id}.txt"
        if norm_file.exists():
            out = pull_page_dir / f"{doc_id}_pull_page_full.txt"
            header = f"# {row['title']}\n# doc_id: {doc_id}\n# source: {row['source_path']}\n\n"
            out.write_text(header + norm_file.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
            print(f"Pull-page: {doc_id}")

    # Chronological: same material, ordered by date
    dated = [(r.get("date", ""), r["doc_id"], r) for r in manifest]
    dated.sort(key=lambda x: (x[0], x[1]))
    chrono_parts = []
    for date, doc_id, row in dated:
        norm_file = norm_dir / f"{doc_id}.txt"
        if norm_file.exists():
            chrono_parts.append(
                f"\n\n=== {row['title']} (doc_id={doc_id}, date={date}) ===\n\n"
                + norm_file.read_text(encoding="utf-8", errors="replace")
            )
    if chrono_parts:
        (chrono_dir / "chronological_full.txt").write_text(
            "# Chronological Full Edition\n\n" + "\n".join(chrono_parts),
            encoding="utf-8",
        )
        print("Chronological: chronological_full.txt")

    print("Done.")


if __name__ == "__main__":
    main()
