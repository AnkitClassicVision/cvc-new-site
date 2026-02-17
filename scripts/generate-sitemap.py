#!/usr/bin/env python3
"""
Generate a static sitemap.xml for the "clean URL" site output.

Scope:
- Includes only / (root index.html) and any */index.html under repo root.
- Excludes source-only folders like ./pages, ./dev, ./partials, etc.
"""

from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CANONICAL_ORIGIN = "https://classicvisioncare.com"

EXCLUDE_DIRS = {
    ".git",
    ".superdesign",
    "api",
    "content",
    "dev",
    "images",
    "node_modules",
    "pages",
    "partials",
    "scripts",
    "styles",
}

EXCLUDE_URL_PATHS = {
    # Legacy URLs that now permanently redirect (keep out of sitemap).
    "/dry-eye-treatment-miboflo/",
    "/dry-eyes/what-is-mibo-thermoflo/",
}


def git_last_committed_date(file_path: Path) -> str | None:
    """Return the ISO date of the last git commit that touched *file_path*."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", str(file_path)],
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()[:10]  # YYYY-MM-DD
    except FileNotFoundError:
        pass
    return None


def to_iso_date(file_path: Path) -> str:
    """Git commit date if available, else file mtime."""
    git_date = git_last_committed_date(file_path)
    if git_date:
        return git_date
    return dt.datetime.fromtimestamp(
        file_path.stat().st_mtime, tz=dt.timezone.utc
    ).date().isoformat()


def path_to_url_path(file_path: Path) -> str:
    if file_path == BASE_DIR / "index.html":
        return "/"
    if file_path.name != "index.html":
        raise ValueError(f"Unexpected file: {file_path}")
    rel_dir = file_path.parent.relative_to(BASE_DIR)
    return f"/{rel_dir.as_posix().strip('/')}/"


def should_include(file_path: Path) -> bool:
    try:
        rel = file_path.relative_to(BASE_DIR)
    except ValueError:
        return False

    parts = rel.parts
    if not parts:
        return False
    if parts[0] in EXCLUDE_DIRS:
        return False
    return True


def main() -> int:
    candidates = []
    for file_path in BASE_DIR.rglob("index.html"):
        if file_path == BASE_DIR / "index.html":
            candidates.append(file_path)
            continue
        if should_include(file_path):
            candidates.append(file_path)

    url_entries = []
    for file_path in sorted(set(candidates)):
        url_path = path_to_url_path(file_path)
        if url_path in EXCLUDE_URL_PATHS:
            continue
        lastmod = to_iso_date(file_path)
        url_entries.append((url_path, lastmod))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url_path, lastmod in url_entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{CANONICAL_ORIGIN}{url_path}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    lines.append("")

    (BASE_DIR / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote sitemap.xml with {len(url_entries)} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
