#!/usr/bin/env bash
# Run pipeline with source paths for typical macOS Downloads layout.
export SOURCE_TOE="${SOURCE_TOE:-$HOME/Downloads/TOE}"
export SOURCE_MQGT="${SOURCE_MQGT:-$HOME/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC}"
cd "$(dirname "$0")/.."
echo "SOURCE_TOE=$SOURCE_TOE"
echo "SOURCE_MQGT=$SOURCE_MQGT"
python scripts/build_manifest.py
python scripts/extract_text.py
python scripts/normalize_text.py
python scripts/chunk_documents.py
python scripts/reconstruct_papers.py
echo "Pipeline done."
