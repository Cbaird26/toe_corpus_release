#!/usr/bin/env bash
# Create symlinks from 01_ingest/raw/ to TOE and mqgt_scf_reissue.
# Run from repo root. Expects TOE and mqgt_scf_reissue as siblings in Downloads/.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
RAW_DIR="$REPO_ROOT/01_ingest/raw"
DOWNLOADS="$(dirname "$REPO_ROOT")"

mkdir -p "$RAW_DIR"
cd "$RAW_DIR"

# TOE
if [ -d "$DOWNLOADS/TOE" ] && [ ! -e TOE ]; then
  ln -s "$DOWNLOADS/TOE" TOE
  echo "Linked TOE"
fi

# mqgt_scf_reissue
if [ -d "$DOWNLOADS/mqgt_scf_reissue_2026-01-20_010939UTC" ] && [ ! -e mqgt_scf_reissue ]; then
  ln -s "$DOWNLOADS/mqgt_scf_reissue_2026-01-20_010939UTC" mqgt_scf_reissue
  echo "Linked mqgt_scf_reissue"
fi

echo "Done. Run: python scripts/build_manifest.py"
