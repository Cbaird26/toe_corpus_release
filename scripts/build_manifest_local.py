#!/usr/bin/env python3
"""Build manifest using hardcoded paths for standard layout. Use when env vars fail."""
import csv
import hashlib
import re
from datetime import datetime
from pathlib import Path

# Edit these if your paths differ
BASE = Path.home() / "Downloads"
TOE_ROOT = BASE / "TOE"
MQGT_ROOT = BASE / "mqgt_scf_reissue_2026-01-20_010939UTC"

TOE_PATTERNS = ["papers_sources/*.tex", "papers_sources/*.pdf", "papers_sources/*.docx", "docs/*.md"]
MQGT_PATTERNS = ["paper/main.tex", "docs/papers/*.pdf", "docs/papers/*.docx", "docs/*.md"]

EXCLUDE = [r"Srimad_Bhagvatam", r"bible_", r"quran", r"urantia", r"zohar", r"shobogenzo",
           r"vigyana_bhairava", r"brahma_sutra", r"buddhist_compendium", r"acim\.pdf", r"nlp_", r"kama_sutra"]

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def slug(n):
    return re.sub(r"[^\w\-.]", "_", Path(n).stem)[:80]

def exclude(n):
    return any(re.search(pat, n, re.I) for pat in EXCLUDE)

def collect(base, patterns):
    out = []
    for pat in patterns:
        for p in base.glob(pat):
            if p.is_file() and not exclude(p.name):
                out.append((p, str(p.relative_to(base))))
    return out

def main():
    repo = Path(__file__).resolve().parent.parent
    manifest_path = repo / "00_manifest" / "corpus_manifest.csv"
    hashes_path = repo / "00_manifest" / "source_hashes.csv"
    rows, hash_rows = [], []
    computed = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    seen = set()

    for repo_name, root, patterns in [
        ("TOE", TOE_ROOT, TOE_PATTERNS),
        ("mqgt_scf_reissue", MQGT_ROOT, MQGT_PATTERNS),
    ]:
        if not root.exists():
            continue
        for path, rel in collect(root, patterns):
            try:
                h = sha256_file(path)
            except Exception:
                continue
            doc_id = slug(path.name)
            if doc_id in seen:
                doc_id = slug(rel)
            seen.add(doc_id)
            m = re.search(r"20\d{2}(?:[-_]?\d{2})?", path.name)
            date = m.group(0).replace("_", "-") if m else "2026"
            rows.append({
                "doc_id": doc_id, "title": path.stem, "source_path": str(path),
                "source_repo": repo_name, "file_type": path.suffix.lstrip("."),
                "page_count": "", "date": date, "version": "", "notes": rel,
            })
            hash_rows.append({
                "doc_id": doc_id, "source_path": str(path), "sha256_hash": h,
                "computed_at": computed, "notes": "",
            })

    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["doc_id","title","source_path","source_repo","file_type","page_count","date","version","notes"])
        w.writeheader()
        w.writerows(rows)
    with open(hashes_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["doc_id","source_path","sha256_hash","computed_at","notes"])
        w.writeheader()
        w.writerows(hash_rows)

if __name__ == "__main__":
    main()
