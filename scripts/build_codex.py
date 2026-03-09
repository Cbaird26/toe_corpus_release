#!/usr/bin/env python3
"""
Build master codex from final papers and governance.
Output: 07_codex/master_codex.md, master_codex.txt, indexes.
"""
import csv
import json
from pathlib import Path
from datetime import datetime


def main():
    repo = Path(__file__).resolve().parent.parent
    final_dir = repo / "06_final_papers"
    edit_dir = repo / "05_edit_pass"
    recon_dir = repo / "03_reconstruction"
    gov_dir = repo / "04_governance"
    codex_dir = repo / "07_codex"
    codex_dir.mkdir(parents=True, exist_ok=True)

    # Use edited_clean if exists, else reconstruction
    papers = []
    for d in sorted(edit_dir.iterdir()) if edit_dir.exists() else []:
        if d.is_dir() and d.name.startswith("paper_"):
            clean = d / "edited_clean.md"
            if clean.exists():
                papers.append((d.name, clean.read_text(encoding="utf-8", errors="replace")))
    if not papers:
        for d in sorted(recon_dir.iterdir()) if recon_dir.exists() else []:
            if d.is_dir() and d.name.startswith("paper_"):
                recon = d / "reconstruction_full.md"
                if recon.exists():
                    papers.append((d.name, recon.read_text(encoding="utf-8", errors="replace")))

    md_parts = ["# Master Codex\n\n", f"Generated: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}\n\n"]
    for name, content in papers:
        md_parts.append(f"\n\n---\n\n## {name}\n\n{content}")

    master_md = codex_dir / "master_codex.md"
    master_txt = codex_dir / "master_codex.txt"
    master_md.write_text("".join(md_parts), encoding="utf-8")
    # Strip Markdown for .txt
    txt_content = "".join(md_parts)
    for sym in ["#", "**", "*", "---", "```"]:
        txt_content = txt_content.replace(sym, "")
    master_txt.write_text(txt_content, encoding="utf-8")

    # Indexes
    paper_rows = [{"paper_id": n, "title": n, "path": str(final_dir / f"{n}_final.md"), "page_count": "", "date": ""} for n, _ in papers]
    with open(codex_dir / "paper_index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["paper_id", "title", "path", "page_count", "date"])
        w.writeheader()
        w.writerows(paper_rows)

    index_data = {"version": "1.0", "created": datetime.utcnow().isoformat() + "Z", "papers": [p[0] for p in papers], "governance": "04_governance/"}
    (codex_dir / "index.json").write_text(json.dumps(index_data, indent=2), encoding="utf-8")

    print(f"Codex built: {master_md}, {master_txt}, indexes")
    print(f"Papers: {len(papers)}")


if __name__ == "__main__":
    main()
