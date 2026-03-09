#!/usr/bin/env python3
"""
Build corpus manifest and source hashes.
Enumerates Tier 1 sources from TOE and mqgt_scf_reissue.
Run from repo root.
"""
import csv
import hashlib
import os
import re
from datetime import datetime
from pathlib import Path

# Tier 1 glob patterns relative to each source root
TOE_PATTERNS = [
    "papers_sources/*.tex",
    "papers_sources/*.pdf",
    "papers_sources/*.docx",
    "docs/*.md",
]
MQGT_PATTERNS = [
    "paper/main.tex",
    "docs/papers/*.pdf",
    "docs/papers/*.docx",
    "docs/*.md",
]

# Exclude large non-ToE PDFs (e.g. Srimad Bhagvatam)
EXCLUDE_PATTERNS = [
    r"Srimad_Bhagvatam",
    r"bible_",
    r"quran",
    r"urantia",
    r"zohar",
    r"shobogenzo",
    r"vigyana_bhairava",
    r"brahma_sutra",
    r"buddhist_compendium",
    r"acim\.pdf",
    r"nlp_",
    r"kama_sutra",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def slug(name: str) -> str:
    """Safe doc_id from filename."""
    base = Path(name).stem
    base = re.sub(r"[^\w\-.]", "_", base)
    return base[:80]


def extract_date_from_path(path: Path) -> str:
    """Extract YYYY or YYYY-MM from filename if present."""
    m = re.search(r"20\d{2}(?:[-_]?\d{2})?", path.name)
    return m.group(0).replace("_", "-") if m else ""


def should_exclude(name: str) -> bool:
    return any(re.search(p, name, re.I) for p in EXCLUDE_PATTERNS)


def collect_files(base: Path, patterns: list[str]) -> list[tuple[Path, str]]:
    out = []
    for pat in patterns:
        for p in base.glob(pat):
            if p.is_file() and not should_exclude(p.name):
                rel = str(p.relative_to(base))
                out.append((p, rel))
    return out


def main():
    repo = Path(__file__).resolve().parent.parent
    log_path = repo / "00_manifest" / "build_log.txt"
    log_lines = []
    raw = repo / "01_ingest" / "raw"
    manifest_path = repo / "00_manifest" / "corpus_manifest.csv"
    hashes_path = repo / "00_manifest" / "source_hashes.csv"

    rows = []
    hash_rows = []
    computed = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    doc_ids_seen = set()

    # Source roots: env override, then raw symlinks, then sibling paths
    import os
    toe_root = os.environ.get("SOURCE_TOE")
    mqgt_root = os.environ.get("SOURCE_MQGT")

    for repo_name, patterns in [("TOE", TOE_PATTERNS), ("mqgt_scf_reissue", MQGT_PATTERNS)]:
        base = None
        if repo_name == "TOE" and toe_root:
            base = Path(toe_root)
        elif repo_name == "mqgt_scf_reissue" and mqgt_root:
            base = Path(mqgt_root)
        if base is None or not base.exists():
            base = raw / repo_name
        if not base.exists():
            sibling = repo.parent / repo_name
            if repo_name == "mqgt_scf_reissue" and not sibling.exists():
                sibling = repo.parent / "mqgt_scf_reissue_2026-01-20_010939UTC"
            base = sibling if sibling.exists() else base
        if not base.exists() and repo_name == "TOE":
            base = Path.home() / "Downloads" / "TOE" if (Path.home() / "Downloads" / "TOE").exists() else base
        if not base.exists() and repo_name == "mqgt_scf_reissue":
            alt = Path.home() / "Downloads" / "mqgt_scf_reissue_2026-01-20_010939UTC"
            base = alt if alt.exists() else base

        if not base.exists():
            print(f"Skip {repo_name}: not found. Set SOURCE_TOE/SOURCE_MQGT or run setup_raw_sources.sh.")
            continue

        collected = collect_files(base, patterns)
        log_lines.append(f"{repo_name}: base={base} exists={base.exists()} files={len(collected)}")
        for path, rel in collected:
            try:
                size = path.stat().st_size
                h = sha256_file(path)
            except (OSError, IOError) as e:
                print(f"Skip {path}: {e}")
                continue

            doc_id = slug(path.name)
            if doc_id in doc_ids_seen:
                doc_id = f"{slug(rel)}"
            doc_ids_seen.add(doc_id)

            ext = path.suffix.lower()
            page_count = ""  # Filled by extract script if needed
            date = extract_date_from_path(path) or "2026"

            rows.append({
                "doc_id": doc_id,
                "title": path.stem,
                "source_path": str(path),
                "source_repo": repo_name,
                "file_type": ext.lstrip("."),
                "page_count": page_count,
                "date": date,
                "version": "",
                "notes": rel,
            })
            hash_rows.append({
                "doc_id": doc_id,
                "source_path": str(path),
                "sha256_hash": h,
                "computed_at": computed,
                "notes": "",
            })

    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "doc_id", "title", "source_path", "source_repo", "file_type",
            "page_count", "date", "version", "notes"
        ])
        w.writeheader()
        w.writerows(rows)

    with open(hashes_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["doc_id", "source_path", "sha256_hash", "computed_at", "notes"])
        w.writeheader()
        w.writerows(hash_rows)

    log_lines.append(f"Total rows: {len(rows)}")
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    print(f"Wrote {len(rows)} entries to {manifest_path}")
    print(f"Wrote {len(hash_rows)} hashes to {hashes_path}")


if __name__ == "__main__":
    main()
