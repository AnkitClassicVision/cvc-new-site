#!/usr/bin/env python3
"""
Standardize footer across all public HTML pages.

Extracts the footer block from index.html and applies it across the static site.
This repo uses root-relative paths (e.g., /book-now/), so we do NOT attempt to
rewrite links based on directory depth.

Footer block boundary:
  Start: <!-- Footer -->
  End:   <script src="/scripts/editorial-forest.js"></script>
"""

from __future__ import annotations

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


def extract_footer_from_index(index_path: Path) -> str | None:
    content = index_path.read_text(encoding="utf-8")
    pattern = r'(<!-- Footer -->.*?<script\s+src="/scripts/editorial-forest\.js"></script>)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1)
    return None


def replace_footer_in_file(file_path: Path, new_footer: str) -> bool:
    content = file_path.read_text(encoding="utf-8")

    patterns = [
        r'(<!-- Footer -->.*?<script\s+src="/scripts/editorial-forest\.js"></script>)',
        r'(<!-- Footer -->.*?<script\s+src="[^"]*editorial-forest\.js"></script>)',
    ]

    for pattern in patterns:
        if re.search(pattern, content, re.DOTALL):
            new_content = re.sub(pattern, new_footer, content, count=1, flags=re.DOTALL)
            file_path.write_text(new_content, encoding="utf-8")
            return True

    return False


def main() -> int:
    base_dir = Path(__file__).parent.parent
    index_path = base_dir / "index.html"

    footer_content = extract_footer_from_index(index_path)
    if not footer_content:
        print("ERROR: Could not extract footer block from index.html")
        return 1

    print(f"Extracted footer block ({len(footer_content)} chars)")

    updated = 0
    skipped = 0

    for html_file in sorted(base_dir.rglob("*.html")):
        rel = html_file.relative_to(base_dir)
        if rel.parts and rel.parts[0] in EXCLUDE_DIRS:
            continue
        if html_file == index_path:
            continue

        if replace_footer_in_file(html_file, footer_content):
            print(f"  Updated: {rel.as_posix()}")
            updated += 1
        else:
            print(f"  Skipped (no footer found): {rel.as_posix()}")
            skipped += 1

    print(f"\nDone! Updated {updated} files, skipped {skipped} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
