#!/usr/bin/env python3
"""
Add Google Tag Manager snippet + lightweight tracking loader to all public HTML pages.

- Inserts GTM loader in <head>
- Inserts GTM <noscript> immediately after <body>
- Adds /scripts/tracking.js as a deferred script in <head>
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
    "node_modules",
    "partials",
    "scripts",  # avoid modifying templates/generators
}

GTM_ID = "GTM-WG6M9ZDV"

HEAD_SNIPPET = f"""<!-- Google Tag Manager -->
<script>
(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');
</script>
<!-- End Google Tag Manager -->
<script src="/scripts/tracking.js" defer></script>
"""

NOSCRIPT_SNIPPET = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
"""


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


def insert_head(html: str) -> str:
    if GTM_ID in html:
        return html
    if "</head>" not in html.lower():
        return html
    return re.sub(r"</head>", HEAD_SNIPPET + "\n</head>", html, count=1, flags=re.IGNORECASE)


def insert_noscript(html: str) -> str:
    if f"ns.html?id={GTM_ID}" in html:
        return html
    return re.sub(r"(<body\b[^>]*>)", r"\1\n" + NOSCRIPT_SNIPPET, html, count=1, flags=re.IGNORECASE)


def main() -> int:
    scanned = 0
    updated = 0

    for file_path in sorted(BASE_DIR.rglob("*.html")):
        if not should_process(file_path):
            continue
        scanned += 1
        before = file_path.read_text(encoding="utf-8")
        after = before
        after = insert_head(after)
        after = insert_noscript(after)
        if after != before:
            file_path.write_text(after, encoding="utf-8")
            updated += 1

    print(f"Scanned {scanned} HTML files. Updated {updated}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
