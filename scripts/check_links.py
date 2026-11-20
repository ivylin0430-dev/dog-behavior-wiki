#!/usr/bin/env python3
"""
scripts/check_links.py
Deterministic programmatic linter for dog-behavior-wiki.
Validates:
1. Internal markdown links ([[link]] or [text](path)) resolve to existing files.
2. All wiki entries are registered in index.md.
3. No orphan pages (every page has inbound links).
4. All footnote tags [^src-xx] have valid definitions at page bottom.
5. Every src-xx cited points to a valid raw/src-xx-* file.
6. No forbidden/deprecated sources (e.g., VCA) are cited.
"""

import os
import re
import sys
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Deterministic Wiki Linter")
    parser.add_argument("--root-dir", type=str, default=".", help="Root directory of the repo")
    parser.add_argument("--wiki-dir", type=str, default="wiki", help="Wiki directory relative to root")
    parser.add_argument("--raw-dir", type=str, default="raw", help="Raw directory relative to root")
    return parser.parse_args()

def main():
    args = parse_args()
    root = Path(args.root_dir).resolve()
    wiki_dir = (root / args.wiki_dir).resolve()
    raw_dir = (root / args.raw_dir).resolve()

    print(f"=== Running Wiki Programmatic Linter ===")
    print(f"Root: {root}")
    print(f"Wiki: {wiki_dir}")
    print(f"Raw:  {raw_dir}\n")

    errors = []
    warnings = []

    if not wiki_dir.exists():
        print(f"ERROR: Wiki directory '{wiki_dir}' does not exist.")
        sys.exit(1)

    # 1. Discover all markdown files in wiki
    wiki_files = list(wiki_dir.glob("**/*.md"))
    content_files = [f for f in wiki_files if f.name not in ["index.md", "log.md"]]
    index_file = wiki_dir / "index.md"

    if not index_file.exists():
        errors.append("Critical: wiki/index.md does not exist.")

    # Read index content
    index_content = index_file.read_text(encoding="utf-8") if index_file.exists() else ""

    # Map of raw source files
    raw_files = list(raw_dir.glob("src-*.md")) if raw_dir.exists() else []
    valid_raw_ids = set()
    deprecated_raw_ids = set()
    for rf in raw_files:
        name = rf.name
        match = re.match(r"(src-\d+)", name)
        if match:
            src_id = match.group(1)
            content = rf.read_text(encoding="utf-8")
            if "status: \"deprecated_superseded\"" in content or "status: deprecated_superseded" in content:
                deprecated_raw_ids.add(src_id)
            else:
                valid_raw_ids.add(src_id)

    print(f"Discovered {len(content_files)} content pages in wiki.")
    print(f"Discovered {len(valid_raw_ids)} active valid raw source IDs: {sorted(list(valid_raw_ids))}")
    print(f"Discovered {len(deprecated_raw_ids)} deprecated raw source IDs: {sorted(list(deprecated_raw_ids))}\n")

    # Inbound links tracker: target_path -> set of source_paths
    inbound_links = {f.resolve(): set() for f in wiki_files}

    # 2. Iterate each file and check links, footnotes, deprecated citations
    for f in wiki_files:
        rel_path = f.relative_to(root)
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()

        # Check: Deprecated VCA citations in active wiki
        if f.name != "index.md" and f.name != "log.md":
            if "vca" in text.lower():
                # Check if it's an accidental active citation
                if re.search(r"\[\^src-03-vca\]|src-03-vca|vcahospitals", text, re.IGNORECASE):
                    errors.append(f"[{rel_path}] Contains forbidden reference to deprecated VCA source.")

        # Check: Registration in index.md
        if f in content_files:
            file_basename = f.name
            stem = f.stem
            # Check if mentioned in index.md
            if file_basename not in index_content and stem not in index_content:
                errors.append(f"[{rel_path}] Orphan catalog: Not registered in index.md.")

        # Check: Wikilinks [[target]] or [[target|text]] (support escaped pipe \| in markdown tables)
        wikilinks = re.findall(r"\[\[(.*?)\]\]", text)
        for wl in wikilinks:
            clean_wl = wl.replace(r"\|", "|")
            target = clean_wl.split("|")[0].strip()
            # If target has wiki/ prefix, strip it to resolve relative to wiki_dir
            normalized_target = target[5:] if target.startswith("wiki/") else target

            resolved_target = None
            candidate1 = wiki_dir / f"{normalized_target}.md"
            candidate2 = f.parent / f"{normalized_target}.md"
            candidate3 = wiki_dir / normalized_target
            candidate4 = f.parent / normalized_target

            if candidate1.exists():
                resolved_target = candidate1
            elif candidate2.exists():
                resolved_target = candidate2
            elif candidate3.exists():
                resolved_target = candidate3
            elif candidate4.exists():
                resolved_target = candidate4
            else:
                # Search by stem in wiki_dir
                matching = list(wiki_dir.glob(f"**/{normalized_target}.md")) + list(wiki_dir.glob(f"**/{normalized_target}"))
                if matching:
                    resolved_target = matching[0]

            if resolved_target and resolved_target.exists():
                res_key = resolved_target.resolve()
                if res_key in inbound_links:
                    inbound_links[res_key].add(f.resolve())
            else:
                errors.append(f"[{rel_path}] Broken internal wikilink: '[[{wl}]]'")

        # Check: Markdown links [text](path)
        md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
        for link_text, link_target in md_links:
            # Ignore external urls and anchor-only links
            if link_target.startswith("http://") or link_target.startswith("https://") or link_target.startswith("#") or link_target.startswith("mailto:"):
                continue
            # Strip anchor if present
            clean_target = link_target.split("#")[0]
            if not clean_target:
                continue
            resolved = (f.parent / clean_target).resolve()
            if resolved.exists():
                if resolved in inbound_links:
                    inbound_links[resolved].add(f.resolve())
            else:
                errors.append(f"[{rel_path}] Broken markdown link: '[{link_text}]({link_target})'")

        # Check: Footnote citations and definitions
        cited_tags = set(re.findall(r"\[\^(src-\d+)\]", text))
        defined_tags = set(re.findall(r"^\[\^(src-\d+)\]:\s*(.*)", text, re.MULTILINE))
        defined_tag_names = {t[0] for t in defined_tags}

        # In content files, all cited footnotes must have definitions
        if f in content_files:
            missing_defs = cited_tags - defined_tag_names
            if missing_defs:
                for md in missing_defs:
                    errors.append(f"[{rel_path}] Undefined footnote: '[^{md}]' cited without definition.")

            # Validate each cited source ID corresponds to active valid raw source
            for ct in cited_tags:
                if ct not in valid_raw_ids:
                    errors.append(f"[{rel_path}] Citation '[^{ct}]' does not match any active valid raw source file.")

            if not cited_tags:
                warnings.append(f"[{rel_path}] No substantive source footnote citations found.")

    # 3. Check for orphan pages (content pages with 0 inbound links)
    for cf in content_files:
        inbound = inbound_links.get(cf.resolve(), set())
        # Filter out self-links
        external_inbound = {src for src in inbound if src != cf.resolve()}
        if not external_inbound:
            errors.append(f"[{cf.relative_to(root)}] Orphan Page: No inbound links from index.md or other wiki pages.")

    # Output Summary
    print("--- LINT RESULTS ---")
    if warnings:
        print(f"\n[WARNINGS] ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"\n[FAIL] Found {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    else:
        print("\n[PASS] All structural, link, footnote, index, and provenance checks passed successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
