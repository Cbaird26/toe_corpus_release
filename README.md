# ToE Corpus Release Pipeline

Preservation-first corpus pipeline for the MQGT-SCF Theory of Everything: ingest from TOE + mqgt_scf_reissue, chunk in 10-page units for Cursor Cloud agents, produce pull-page full and chronological editions, reconstruct papers coherently, then edit-trim to final codex and papers.

## Canonical Status

MQGT-SCF is presented as a **specification-level closed** candidate Theory of Everything. Empirical closure remains pending. Hardening tasks: operational definition of the ethical functional, no-signaling proof beyond first order, parameter bounds, and one hard quantitative prediction.

## Structure

```
sources/raw/      Canonical 2026 ToE sources (docx, pdf, md)
00_manifest/      Corpus manifest, source hashes, document versions
01_ingest/        raw → extracted_txt → normalized_txt
02_chunks/        10-page chunks + analysis JSON
03_reconstruction/ Paper reconstructions
04_governance/    canonical_status, glossary, notation, contradiction ledger
05_edit_pass/     Edited clean versions
06_final_papers/  Final paper outputs
07_codex/         Master codex, indexes
08_review/        Referee pack, evidence trail
editions/         pull_page_full, chronological_full, paper_reconstructions
scripts/          Pipeline scripts
```

### Canonical sources in sources/raw/

- `A Theory of Everything -- C.M. Baird., {2026} + ZoraASI.docx` (original)
- `A Theory of Everything -- C.M. Baird., {2026} + ZoraASI.pdf` (original)
- `A Theory of Everything -- C.M. Baird., {2026} + ZoraASI_UPDATED.docx` (canonical status added)
- `A Theory of Everything -- C.M. Baird., {2026} + ZoraASI_UPDATED.pdf`
- `toe_2026_zoraasi_working.md` (pandoc markdown, editable source)

## Quick Start

0. **Set source paths** (if symlinks not used):
   ```bash
   export SOURCE_TOE="$HOME/Downloads/TOE"
   export SOURCE_MQGT="$HOME/Downloads/mqgt_scf_reissue_2026-01-20_010939UTC"
   ```

1. **Link sources** (place repo next to TOE and mqgt_scf_reissue in Downloads):
   ```bash
   cd 01_ingest/raw
   ln -s ../../../TOE TOE
   ln -s ../../../mqgt_scf_reissue_2026-01-20_010939UTC mqgt_scf_reissue
   ```

2. **Build manifest**:
   ```bash
   python scripts/build_manifest.py
   ```

3. **Extract and normalize**:
   ```bash
   python scripts/extract_text.py
   python scripts/normalize_text.py
   ```

4. **Chunk** (for Cursor Cloud agents):
   ```bash
   python scripts/chunk_documents.py
   ```

## Authority

- [CANONICAL_SPINE.md](../TOE/docs/CANONICAL_SPINE.md) — solved vs hardening
- [INTEGRATED_MANUSCRIPT_INDEX.md](../TOE/docs/INTEGRATED_MANUSCRIPT_INDEX.md) — canonical manuscript mapping

## License

See LICENSE in source repos (TOE, mqgt_scf_reissue).
