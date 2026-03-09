# Chunks

10-page chunks of normalized text. After running `python scripts/chunk_documents.py`, each `doc_id` gets a subfolder:

```
02_chunks/{doc_id}/
  chunk_001_pages_001-010.txt
  chunk_002_pages_011-020.txt
  ...
  chunk_XXX_analysis.json   # Cursor Cloud agent output
```

## Chunk Analysis Schema (agent output)

Each `chunk_XXX_analysis.json` should contain:

```json
{
  "document_title_guess": "...",
  "section_title_guess": "...",
  "page_range": "001-010",
  "equations_detected": [],
  "claims_detected": [],
  "citations_detected": [],
  "contradictions_or_duplicates": [],
  "proposed_destination_paper": "paper_id",
  "confidence_score": 0.8
}
```

Scan only — no editing in this pass.
