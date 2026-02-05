#!/usr/bin/env python3
"""
Standardize navigation across all public HTML pages.

Extracts the header block from index.html and applies it across the static site.
This repo uses root-relative paths (e.g., /book-now/), so we do NOT attempt to
rewrite links based on directory depth.
"""

import os
import re
from pathlib import Path

EXCLUDE_DIRS = {
    ".git",
    ".superdesign",
    "api",
    "content",
    "dev",
    "images",
    "node_modules",
    "pages",  # source-only files; not part of clean-route output
    "partials",
    "scripts",  # avoid modifying generators
    "styles",
    "wp-content",
}

def extract_nav_from_index(index_path):
    """Extract the topbar + header section from index.html"""
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match from <!-- Top Phone Bar --> through </header>
    # The nav section starts with the topbar and ends with </header>
    pattern = r'(<!-- Top Phone Bar -->.*?</header>)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1)
    return None

def replace_nav_in_file(file_path, new_nav):
    """Replace the nav section in a file with the standardized nav"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match existing topbar + header
    # Start: <!-- Top Phone Bar --> or <div class="ef-topbar
    # End: </header>
    patterns = [
        r'(<!-- Top Phone Bar -->.*?</header>)',
        r'(<div class="ef-topbar.*?</header>)',
    ]

    replaced = False
    for pattern in patterns:
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, new_nav, content, count=1, flags=re.DOTALL)
            replaced = True
            break

    if replaced:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    base_dir = Path(__file__).parent.parent
    index_path = base_dir / 'index.html'

    # Extract nav from index.html
    nav_content = extract_nav_from_index(index_path)
    if not nav_content:
        print("ERROR: Could not extract nav from index.html")
        return

    print(f"Extracted nav section ({len(nav_content)} chars)")

    # Find all HTML files recursively except index.html
    html_files = list(base_dir.rglob('*.html'))

    updated = 0
    skipped = 0
    for html_file in html_files:
        rel = html_file.relative_to(base_dir)
        if rel.parts and rel.parts[0] in EXCLUDE_DIRS:
            continue
        if html_file == index_path:
            continue

        if replace_nav_in_file(html_file, nav_content):
            print(f"  Updated: {rel.as_posix()}")
            updated += 1
        else:
            print(f"  Skipped (no nav found): {rel.as_posix()}")
            skipped += 1

    print(f"\nDone! Updated {updated} files, skipped {skipped} files.")

if __name__ == '__main__':
    main()
