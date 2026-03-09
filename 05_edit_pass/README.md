# Edit Pass

Per-reconstructed-paper editorial output. Each `paper_{XXX}/` contains:

- `edited_clean.md` — trimmed, normalized text
- `redline.md` — (optional) diff-style changes
- `edit_log.md` — `old_wording → new_wording | reason | source_of_authority`
- `open_questions.md` — unresolved contradictions or gaps

## Rules

- Preserve canonical status meaning
- Downgrade overclaims
- Flag contradictions; do not hide them
- Do not invent proof steps, citations, or experiments
- Log every change

## Edit Log Format

```
old_wording → new_wording | reason | source_of_authority
```

Run Cursor Cloud agents in 10-page chunks over `03_reconstruction/paper_{XXX}/reconstruction_full.md`.
