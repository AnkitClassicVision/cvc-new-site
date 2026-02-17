#!/usr/bin/env python3
"""
Inject Editorial Forest stylesheet and body class across all HTML pages.
"""

from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent
HTML_FILES = [f for f in BASE_DIR.glob("*.html") if "node_modules" not in str(f)]

STYLESHEET_TAG = '<link rel="stylesheet" href="styles/editorial-forest.css?v=3">'


def ensure_stylesheet(html: str) -> str:
    if "styles/editorial-forest.css?v=3" in html:
        return html
    return html.replace("</head>", f"  {STYLESHEET_TAG}\n</head>")


def ensure_body_class(html: str) -> str:
    def repl(match):
        attrs = match.group(1) or ""
        classes = match.group(2) or ""
        if "cvc-editorial" in classes:
            return match.group(0)
        new_classes = f"cvc-editorial {classes}".strip()
        return f'<body{attrs} class="{new_classes}">'

    if "<body" not in html:
        return html
    html = re.sub(r"<body([^>]*)class=\"([^\"]*)\">", repl, html, count=1)
    if "cvc-editorial" not in html:
        html = re.sub(r"<body([^>]*)>", r"<body\1 class=\"cvc-editorial\">", html, count=1)
    return html


def main():
    updated = 0
    for file in HTML_FILES:
        text = file.read_text(encoding="utf-8")
        new_text = ensure_stylesheet(ensure_body_class(text))
        if new_text != text:
            file.write_text(new_text, encoding="utf-8")
            updated += 1
    print(f"Updated {updated} files")


if __name__ == "__main__":
    main()
