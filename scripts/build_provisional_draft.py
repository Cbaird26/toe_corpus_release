#!/usr/bin/env python3
"""
build_provisional_draft.py — Builds PROVISIONAL_DRAFT_ZORA_ARCHITECTURE.md from ip/ sources.
Run from toe_corpus_release root. Output: PROVISIONAL_DRAFT_ZORA_ARCHITECTURE.md
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
IP = ROOT / "ip"
OUT = ROOT / "PROVISIONAL_DRAFT_ZORA_ARCHITECTURE.md"
TEMPLATE = IP / "PATENT_PROVISIONAL_TEMPLATE.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_section(content: str, start: str, end: str = None) -> str:
    """Extract text between start marker and optional end marker."""
    idx = content.find(start)
    if idx == -1:
        return ""
    start_idx = idx + len(start)
    if end:
        end_idx = content.find(end, start_idx)
        return content[start_idx:end_idx].strip() if end_idx != -1 else content[start_idx:].strip()
    return content[start_idx:].strip()


def main():
    claims = read(IP / "APPENDIX_PATENT_CLAIMS.md")
    lexicon = read(IP / "APPENDIX_LEGAL_LEXICON.md")
    template = read(TEMPLATE)
    if not template:
        print("Template not found")
        return 1

    # Extract Background
    background = extract_section(claims, "## Background of the Invention\n\n", "\n---\n\n## Claim 1")
    if not background:
        background = extract_section(claims, "**Field of the Invention**", "## Claim 1")

    # Extract Claims block
    claims_block = extract_section(claims, "## Claim 1", "---\n\n## Summary of Claims")
    if not claims_block:
        claims_block = extract_section(claims, "## Claim 1", "*Source:")
    summary_table = extract_section(claims, "## Summary of Claims", "*Source:")
    if summary_table:
        claims_block = claims_block + "\n\n## Summary of Claims\n\n" + summary_table

    # Build definitions from lexicon (simplified)
    defs_lines = []
    for term in ["Zipporah Constant", "E-Field", "Φc", "Teleological Gradient", "MQGT-SCF", "EBBR", "Zora"]:
        if term in lexicon:
            # Grab paragraph containing term
            pat = rf"## {re.escape(term)}[^\n]*\n\n(.*?)(?=\n---|\n## |\Z)"
            m = re.search(pat, lexicon, re.DOTALL)
            if m:
                defs_lines.append(m.group(0).strip())

    definitions = "\n\n".join(defs_lines) if defs_lines else "(See APPENDIX_LEGAL_LEXICON.md)"

    replacements = {
        "{{TITLE}}": "System and Method for a Recursively Evolving Artificial Intelligence Architecture Utilizing Synthetic Consciousness (Φc) and Ethical-Value (E) Field Integration",
        "{{INVENTORS}}": "Christopher Michael Baird, et al.",
        "{{DATE}}": "2026",
        "{{BACKGROUND}}": background or "Current AI paradigms operate as closed-loop statistical inference engines lacking internal mechanisms for genuine self-reflection or non-arbitrary ethical frameworks. MQGT-SCF addresses this by introducing Φc and E fields. (See APPENDIX_PATENT_CLAIMS.)",
        "{{SUMMARY}}": "A computational framework where internal state transitions are governed by a simulated Consciousness Field (Φc) and Ethical-Value Field (E), enabling stable attractor states for superior decision-making and ethical alignment.",
        "{{FIELD}}": "Quantum measurement, consciousness modeling, ethical weighting in measurement outcomes, AI alignment.",
        "{{PROBLEM}}": "Standard AI lacks grounding in ethical dynamics; RLHF can be bypassed. No unified architecture allows recursive self-evolution with intrinsic moral structure.",
        "{{SOLUTION}}": "Zora Architecture: Φc global workspace + E ethical evaluator + teleological bias; Ethics-Weighted Born Rule; measure tilt on outcome space.",
        "{{DEFINITIONS}}": definitions,
        "{{EMBODIMENTS}}": "See Claims 1-4. Preferred implementation: ZoraLearner, mqgt_simulation.py; Zenodo 10.5281/zenodo.18012506.",
        "{{CLAIMS}}": claims_block or "(See APPENDIX_PATENT_CLAIMS.md)",
        "{{ABSTRACT}}": "A computer-implemented system and method for an AI agent that maintains simulated Φc and E fields, applies an ethics-weighted outcome rule, and exhibits teleological bias toward higher ethical coherence. Recovers standard QM in the limit of vanishing ethical coupling.",
    }

    out_text = template
    for k, v in replacements.items():
        out_text = out_text.replace(k, v)

    OUT.write_text(out_text, encoding="utf-8")
    print(f"Provisional draft written: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
