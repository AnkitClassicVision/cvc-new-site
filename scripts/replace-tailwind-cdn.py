#!/usr/bin/env python3
"""
Replace Tailwind CDN usage with the precompiled /styles/tailwind.css file.

Actions per HTML file:
- Remove <script src="https://cdn.tailwindcss.com"></script>
- Remove inline tailwind.config blocks
- Remove preconnect to cdn.tailwindcss.com
- Ensure <link rel="stylesheet" href="/styles/tailwind.css"> exists before editorial-forest.css
"""

from __future__ import annotations

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".git",
    ".superdesign",
    "api",
    "content",
    "dev",
    "images",
    "node_modules",
    "partials",
    "scripts",
}

TAILWIND_CSS_LINK = '<link rel="stylesheet" href="/styles/tailwind.css">'


def should_process(file_path: Path) -> bool:
    try:
        rel = file_path.relative_to(BASE_DIR)
    except ValueError:
        return False
    if not rel.parts:
        return False
    if rel.parts[0] in EXCLUDE_DIRS:
        return False
    return True


def strip_tailwind_cdn(html_text: str) -> str:
    # Remove preconnect to tailwind CDN
    html_text = re.sub(
        r'\s*<link[^>]+rel=["\']preconnect["\'][^>]+href=["\']https://cdn\.tailwindcss\.com["\'][^>]*>\s*',
        "\n",
        html_text,
        flags=re.IGNORECASE,
    )

    # Remove Tailwind CDN script tag
    html_text = re.sub(
        r'\s*<script[^>]+src=["\']https://cdn\.tailwindcss\.com["\'][^>]*>\s*</script>\s*',
        "\n",
        html_text,
        flags=re.IGNORECASE,
    )

    # Remove inline tailwind.config blocks (common pattern)
    html_text = re.sub(
        r'\s*<script>\s*tailwind\.config\s*=\s*\{.*?\}\s*</script>\s*',
        "\n",
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    return html_text


def ensure_tailwind_css_link(html_text: str) -> str:
    if "/styles/tailwind.css" in html_text:
        return html_text

    # Insert before editorial-forest.css if present
    m = re.search(r'(<link[^>]+href=["\']/styles/editorial-forest\.css["\'][^>]*>)', html_text, flags=re.IGNORECASE)
    if m:
        insert_at = m.start(1)
        return html_text[:insert_at] + f"{TAILWIND_CSS_LINK}\n  " + html_text[insert_at:]

    # Otherwise insert before </head>
    m = re.search(r"</head>", html_text, flags=re.IGNORECASE)
    if m:
        insert_at = m.start(0)
        return html_text[:insert_at] + f"  {TAILWIND_CSS_LINK}\n" + html_text[insert_at:]
    return html_text


def main() -> int:
    updated = 0
    scanned = 0

    for file_path in sorted(BASE_DIR.rglob("*.html")):
        if not should_process(file_path):
            continue
        scanned += 1
        before = file_path.read_text(encoding="utf-8")
        after = ensure_tailwind_css_link(strip_tailwind_cdn(before))
        if after != before:
            file_path.write_text(after, encoding="utf-8")
            updated += 1

    print(f"Scanned {scanned} HTML files. Updated {updated}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

