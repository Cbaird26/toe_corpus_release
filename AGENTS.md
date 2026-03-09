# Cursor Cloud Agent Instructions

## Canonical Status (preserve in every pass)

**MQGT-SCF is presented as a specification-level closed candidate Theory of Everything. Empirical closure remains pending.** Hardening tasks: (1) operational definition of the ethical functional, (2) no-signaling proof beyond first order, (3) parameter bounds, (4) one hard quantitative prediction.

Never upgrade this to "fully completed" or "100%" unless explicitly supported by canonical authority. Downgrade any overclaim (complete, final, proved) unless it matches this status.

---

## 10-Page Chunk Workflow

### Scan Pass (no editing)

1. **Input:** `02_chunks/{doc_id}/chunk_{NNN}_pages_{XXX}-{YYY}.txt`
2. **Output:** `02_chunks/{doc_id}/chunk_{NNN}_analysis.json`
3. **Fields:**
   - `document_title_guess`
   - `section_title_guess`
   - `page_range` (e.g. "001-010")
   - `equations_detected` (list)
   - `claims_detected` (list, raw text)
   - `citations_detected` (list)
   - `contradictions_or_duplicates` (list, or empty)
   - `proposed_destination_paper` (paper ID for reconstruction)
   - `confidence_score` (0–1)

4. **Rules:**
   - Do NOT edit the text.
   - Do NOT invent proofs or citations.
   - Do NOT add new physics.
   - Map only: classify and route.

### Edit Pass (after reconstruction)

1. **Input:** `03_reconstruction/paper_{XXX}/reconstruction_full.md` (10-page chunks)
2. **Output:** Edits to `05_edit_pass/paper_{XXX}/edited_clean.md`
3. **Rules:**
   - Preserve canonical status meaning.
   - Downgrade overclaims (complete → specified, etc.).
   - Flag contradictions; do not hide them.
   - Do NOT invent proof steps, citations, or experiments.
   - Log every change: `old_wording → new_wording | reason | source_of_authority`

---

## Claim Types

| Type | Meaning |
|------|---------|
| **proved** | Mathematically or empirically verified |
| **specified** | Formally defined, not yet proved |
| **conjectural** | Hypothetical, open |
| **experimental** | Requires or awaits experiment |

Use only these four. Do not invent new categories.

---

## Terminology

- **complete** / **closed** / **solved** / **100%** / **referee-proof** — not interchangeable. Prefer "specification-level closed" and "empirical closure pending" per canonical status.
- **Φc** — consciousness field
- **E** — ethical field
- **η** — ethics modulation parameter
- **ΔE** — ethical energy difference
- **C_E** — ethical coupling constant
- **P_η** — ethics-weighted Born probability

---

## Source of Authority

- [TOE/docs/CANONICAL_SPINE.md](../TOE/docs/CANONICAL_SPINE.md)
- [TOE/docs/INTEGRATED_MANUSCRIPT_INDEX.md](../TOE/docs/INTEGRATED_MANUSCRIPT_INDEX.md)
- [04_governance/canonical_status.md](04_governance/canonical_status.md)
- [04_governance/glossary.md](04_governance/glossary.md)
