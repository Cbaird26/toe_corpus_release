# Reconstruction

Per-paper reconstruction from normalized text. Each `paper_{XXX}/` contains:

- `reconstruction_full.md` — merged content
- `source_map.csv` — chunk_or_full, doc_id, source_path
- `duplicate_map.csv` — (optional, from edit pass)
- `unresolved_gaps.md` — (optional)
- `contradiction_log.md` — (optional)

Run: `python scripts/reconstruct_papers.py`
