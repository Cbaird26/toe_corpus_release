#!/usr/bin/env bash
# Run full corpus pipeline (phases 2–4).
# Prerequisite: sources linked via setup_raw_sources.sh, or set SOURCE_TOE/SOURCE_MQGT.

set -e
cd "$(dirname "$0")/.."
export SOURCE_TOE="${SOURCE_TOE:-$HOME/Downloads/TOE}"
export SOURCE_MQGT="${SOURCE_MQGT:-$HOME/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC}"

echo "=== Phase 2a: Build manifest ==="
python scripts/build_manifest.py

echo "=== Phase 2b: Extract text ==="
python scripts/extract_text.py

echo "=== Phase 2c: Normalize text ==="
python scripts/normalize_text.py

echo "=== Phase 3: Chunk documents ==="
python scripts/chunk_documents.py

echo "=== Phase 4: Reconstruct papers + editions ==="
python scripts/reconstruct_papers.py

echo "=== Done ==="
