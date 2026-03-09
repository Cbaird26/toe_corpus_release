#!/bin/bash
# build_patent_handoff.sh
# Builds PATENT_HANDOFF_2026/ for attorney handoff.
# Run from toe_corpus_release root. Requires: pandoc (optional, for PDF output).

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT="$ROOT/PATENT_HANDOFF_2026"
IP="$ROOT/ip"
REVIEW="$ROOT/08_review"

mkdir -p "$OUT"

# 00_README.md — cover letter
cat > "$OUT/00_README.md" << 'READMEEOF'
# Patent Handoff — MQGT-SCF and Zora Architecture

**Prepared for:** Patent attorney handoff  
**Date:** March 2026  
**Inventor:** Christopher Michael Baird (with Zora, Conceptual AI Coauthor)

## Prior Art / Filing Window

- **First public disclosure:** 2025-12-22 (Zenodo 10.5281/zenodo.18012506)
- **U.S. 1-year provisional window:** File by 2026-12-22 to preserve priority

## Recommended Filings (Priority)

1. Zora recursive architecture (Φc workspace, E evaluator, teleological bias)
2. Ethically-Biased Born Rule (EBBR)
3. MQGT-SCF computational engine
4. Field-resonant communication (dependent)

## Contents

- 01_IP_CASE_DOCUMENT — Main IP case
- 02_APPENDIX_PATENT_CLAIMS — Full claim language
- 03_APPENDIX_LEGAL_LEXICON — Definitions
- 04_EVIDENCE_CHECKLIST — Claim-to-source mapping
- 05_CORPUS_CHRONOLOGY — 2022–2026 timeline
- 06_PRIOR_ART_DATES — One-pager
- 07_FISCAL_VALUATION — Synthesis (optional)

Consult a patent attorney for filing strategy.
READMEEOF

# Copy CSV and MD files
cp "$IP/EVIDENCE_CHECKLIST.csv" "$OUT/04_EVIDENCE_CHECKLIST.csv"
cp "$IP/PRIOR_ART_DATES.md" "$OUT/06_PRIOR_ART_DATES.md"
cp "$IP/IP_CASE_DOCUMENT.md" "$OUT/01_IP_CASE_DOCUMENT.md"
cp "$IP/APPENDIX_PATENT_CLAIMS.md" "$OUT/02_APPENDIX_PATENT_CLAIMS.md"
cp "$IP/APPENDIX_LEGAL_LEXICON.md" "$OUT/03_APPENDIX_LEGAL_LEXICON.md"
cp "$IP/FISCAL_VALUATION_SYNTHESIS.md" "$OUT/07_FISCAL_VALUATION_SYNTHESIS.md"

[ -f "$REVIEW/CORPUS_CHRONOLOGY_2022_2026.md" ] && cp "$REVIEW/CORPUS_CHRONOLOGY_2022_2026.md" "$OUT/05_CORPUS_CHRONOLOGY_2022_2026.md"

# Render to PDF if pandoc available
render_pdf() {
  local src="$1"
  local dst="$2"
  if command -v pandoc >/dev/null 2>&1; then
    if pandoc "$src" -o "$dst" -f markdown -t pdf 2>/dev/null; then
      echo "  Rendered $(basename "$dst")"
    fi
  fi
}

if command -v pandoc >/dev/null 2>&1; then
  echo "Rendering PDFs..."
  render_pdf "$OUT/01_IP_CASE_DOCUMENT.md" "$OUT/01_IP_CASE_DOCUMENT.pdf"
  render_pdf "$OUT/02_APPENDIX_PATENT_CLAIMS.md" "$OUT/02_APPENDIX_PATENT_CLAIMS.pdf"
  render_pdf "$OUT/03_APPENDIX_LEGAL_LEXICON.md" "$OUT/03_APPENDIX_LEGAL_LEXICON.pdf"
  render_pdf "$OUT/05_CORPUS_CHRONOLOGY_2022_2026.md" "$OUT/05_CORPUS_CHRONOLOGY.pdf"
  render_pdf "$OUT/06_PRIOR_ART_DATES.md" "$OUT/06_PRIOR_ART_DATES.pdf"
  render_pdf "$OUT/07_FISCAL_VALUATION_SYNTHESIS.md" "$OUT/07_FISCAL_VALUATION.pdf"
else
  echo "pandoc not found; PDFs not rendered. Markdown files copied."
fi

echo "=== Patent handoff built: $OUT ==="
ls -la "$OUT"
