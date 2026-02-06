#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class PageInfo:
    new_path: str
    old_path: str


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "content" / "page_manifest.json"
RUNS_DIR = ROOT / "content" / "blog_writer_runs"


IMG_SRC_RE = re.compile(r"<img[^>]+src=\"(?P<src>[^\"]+)\"", flags=re.I)
TITLE_RE = re.compile(r"<title>(?P<t>.*?)</title>", flags=re.I | re.S)
META_DESC_RE = re.compile(
    r"<meta[^>]+name=\"description\"[^>]+content=\"(?P<c>[^\"]+)\"[^>]*>",
    flags=re.I,
)
H1_RE = re.compile(r"<h1[^>]*>", flags=re.I)

BANNED_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("em/en dashes", re.compile(r"[—–]")),
    ("today world filler", re.compile(r"In today[’']s world", flags=re.I)),
    ("important-to-note filler", re.compile(r"it[’']s important to note", flags=re.I)),
    ("seamless", re.compile(r"\bseamless\b", flags=re.I)),
    ("streamline", re.compile(r"\bstreamline\b", flags=re.I)),
    ("leverage", re.compile(r"\bleverage\b", flags=re.I)),
    ("robust", re.compile(r"\brobust\b", flags=re.I)),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def load_pages() -> list[PageInfo]:
    raw = json.loads(read_text(MANIFEST_PATH))
    pages: list[PageInfo] = []
    for new_path, info in raw.items():
        pages.append(
            PageInfo(
                new_path=new_path,
                old_path=info.get("old_path", new_path),
            )
        )
    pages.sort(key=lambda p: p.new_path)
    return pages


def slugify(old_path: str) -> str:
    name = old_path.strip().lower()
    if name == "index.html":
        return "index"
    name = re.sub(r"\.html$", "", name)
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")


def local_image_issues(page_path: Path, html: str) -> list[str]:
    issues: list[str] = []
    for m in IMG_SRC_RE.finditer(html):
        src = m.group("src").strip()
        if not src or src.startswith(("http://", "https://", "//", "data:")):
            continue
        src = src.split("#", 1)[0].split("?", 1)[0]
        img_path = (page_path.parent / src).resolve()
        if not img_path.exists():
            issues.append(f"Missing image: {src}")
    return issues


def qa_for_page(page_path: Path, html: str) -> dict[str, object]:
    issues: list[str] = []

    # Core structure
    title = TITLE_RE.search(html)
    meta_desc = META_DESC_RE.search(html)
    has_h1 = bool(H1_RE.search(html))
    has_hero_points = "Hero value points" in html
    has_cta = ("pages/patients/book.html" in html) or ("href=\"tel:" in html)

    if not title or not title.group("t").strip():
        issues.append("Missing <title>")
    if not meta_desc or not meta_desc.group("c").strip():
        issues.append("Missing meta description")
    if not has_h1:
        issues.append("Missing <h1>")
    if not has_hero_points:
        issues.append("Missing hero value points block")
    if not has_cta:
        issues.append("Missing clear CTA (book or call)")

    # Banned content patterns
    for label, pattern in BANNED_PATTERNS:
        if pattern.search(html):
            issues.append(f"Banned: {label}")

    # Local images
    issues.extend(local_image_issues(page_path, html))

    return {
        "ok": len(issues) == 0,
        "issues": issues,
        "checks": {
            "hero_points": has_hero_points,
            "cta": has_cta,
            "title": bool(title and title.group("t").strip()),
            "meta_description": bool(meta_desc and meta_desc.group("c").strip()),
            "h1": has_h1,
        },
    }


def update_run_file(page: PageInfo, result: dict[str, object]) -> None:
    run_path = RUNS_DIR / f"{slugify(page.old_path)}.md"
    if not run_path.exists():
        return

    text = read_text(run_path)
    text = re.sub(r"\n## QA Results \\(.*\\)\\n[\\s\\S]*\\Z", "", text, flags=re.S)

    ok = bool(result["ok"])
    issues = result["issues"]
    checks = result["checks"]

    lines: list[str] = []
    lines.append(f"## QA Results ({date.today().isoformat()})")
    lines.append(f"- Status: {'PASS' if ok else 'FAIL'}")
    lines.append(f"- Hero value points: {'PASS' if checks['hero_points'] else 'FAIL'}")
    lines.append(f"- CTA present: {'PASS' if checks['cta'] else 'FAIL'}")
    lines.append(
        f"- Title/meta description: {'PASS' if (checks['title'] and checks['meta_description']) else 'FAIL'}"
    )
    lines.append(f"- H1 present: {'PASS' if checks['h1'] else 'FAIL'}")
    if ok:
        lines.append("- Notes: Automated checks passed for banned phrases, local images, and structure.")
    else:
        lines.append("- Issues:")
        for item in issues:
            lines.append(f"  - {item}")

    write_text(run_path, text.rstrip() + "\n\n" + "\n".join(lines) + "\n")


def write_summary(results: list[tuple[str, dict[str, object]]]) -> Path:
    out_path = RUNS_DIR / "QA_SUMMARY.md"
    total = len(results)
    failures = [(p, r) for p, r in results if not r["ok"]]
    lines: list[str] = []
    lines.append("# Blog Writer QA Summary")
    lines.append("")
    lines.append(f"Date: {date.today().isoformat()}")
    lines.append(f"Pages checked: {total}")
    lines.append(f"Pass: {total - len(failures)}")
    lines.append(f"Fail: {len(failures)}")
    lines.append("")
    if failures:
        lines.append("## Failures")
        for page_path, r in failures:
            lines.append(f"- {page_path}")
            for issue in r["issues"]:
                lines.append(f"  - {issue}")
    else:
        lines.append("All pages passed automated checks.")
    write_text(out_path, "\n".join(lines) + "\n")
    return out_path


def main() -> int:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Missing manifest: {MANIFEST_PATH}")
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    results: list[tuple[str, dict[str, object]]] = []
    for page in load_pages():
        page_path = ROOT / page.new_path
        html = read_text(page_path)
        r = qa_for_page(page_path, html)
        results.append((page.new_path, r))
        update_run_file(page, r)

    summary_path = write_summary(results)
    failures = [p for p, r in results if not r["ok"]]
    print(f"Wrote {summary_path.relative_to(ROOT)}")
    if failures:
        print(f"FAIL: {len(failures)} pages have issues")
        return 2
    print("PASS: all pages clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
