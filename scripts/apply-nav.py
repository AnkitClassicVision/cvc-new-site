#!/usr/bin/env python3
"""
Apply standardized navigation and footer to all CVC HTML pages.
Uses partial templates from the partials/ directory.
"""

import os
import re
from pathlib import Path

# Directory setup
BASE_DIR = Path(__file__).parent.parent
PARTIALS_DIR = BASE_DIR / "partials"

# Load partial templates
with open(PARTIALS_DIR / "nav-header.html", "r", encoding="utf-8") as f:
    NAV_TEMPLATE = f.read()

with open(PARTIALS_DIR / "footer.html", "r", encoding="utf-8") as f:
    FOOTER_TEMPLATE = f.read()

# Files to process (exclude node_modules and partials)
HTML_FILES = [
    f for f in BASE_DIR.glob("*.html")
    if "node_modules" not in str(f) and "partials" not in str(f)
]

# Skip index.html as it has custom structure
SKIP_FILES = {"index.html"}


def extract_main_content(html):
    """Extract the <main>...</main> content from HTML."""
    main_match = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
    if main_match:
        return main_match.group(0)
    return None


def extract_head(html):
    """Extract the <head>...</head> content from HTML."""
    head_match = re.search(r"<head[^>]*>(.*?)</head>", html, re.DOTALL)
    if head_match:
        return head_match.group(0)
    return None


def process_file(filepath):
    """Process a single HTML file."""
    filename = filepath.name
    print(f"Processing: {filename}")

    if filename in SKIP_FILES:
        print(f"  Skipping (in skip list)")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract key parts
    head = extract_head(content)
    main_content = extract_main_content(content)

    if not head:
        print(f"  ERROR: Could not extract <head>")
        return False

    if not main_content:
        print(f"  ERROR: Could not extract <main>")
        return False

    # Reconstruct the page with standardized nav/footer
    new_content = f'''<!DOCTYPE html>
<html lang="en">
{head}
<body class="cvc-editorial font-body text-cvc-charcoal bg-white">
{NAV_TEMPLATE}

  {main_content}

{FOOTER_TEMPLATE}
</body>
</html>
'''

    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  Updated: {filename}")
    return True


def main():
    print(f"Found {len(HTML_FILES)} HTML files")
    print(f"Skipping: {SKIP_FILES}")
    print("-" * 50)

    updated = 0
    errors = 0

    for filepath in sorted(HTML_FILES):
        try:
            if process_file(filepath):
                updated += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1

    print("-" * 50)
    print(f"Updated: {updated}")
    print(f"Errors: {errors}")
    print(f"Skipped: {len(SKIP_FILES)}")


if __name__ == "__main__":
    main()
