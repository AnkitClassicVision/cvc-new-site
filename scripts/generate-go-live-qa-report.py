#!/usr/bin/env python3
"""
Generate a go-live QA report for the static Classic Vision Care site.

Checks:
- Top GSC URLs exist as local files
- Redirect destinations exist
- Canonical tag present on public pages
- No lingering /pages/... internal links on public pages
- robots + sitemap + favicon present
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

SITE_DIR = Path(__file__).resolve().parent.parent
COMPARISONS_DIR = Path("/mnt/d_drive/repos/cvc_site_comparisons")
DATA_DIR = COMPARISONS_DIR / "cvc_analysis" / "data"
REPORTS_DIR = COMPARISONS_DIR / "cvc_analysis" / "reports"

TOP60_CSV = DATA_DIR / "launch_url_plan_gsc12m_top60.csv"
REDIRECTS_CSV = DATA_DIR / "redirects_minimal.csv"
VERCEL_JSON = SITE_DIR / "vercel.json"
SITEMAP_XML = SITE_DIR / "sitemap.xml"
ROBOTS_API = SITE_DIR / "api" / "robots.js"
CONTACT_API = SITE_DIR / "api" / "contact.js"

EXCLUDE_DIRS = {
    ".git",
    ".superdesign",
    "api",
    "content",
    "dev",
    "node_modules",
    "pages",
    "partials",
    "scripts",
    "styles",
}


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    details: list[str]


def path_to_file(site_path: str) -> Path:
    if not site_path.startswith("/"):
        site_path = "/" + site_path
    if site_path == "/":
        return SITE_DIR / "index.html"
    return SITE_DIR / site_path.lstrip("/") / "index.html"


def iter_public_html_files() -> Iterable[Path]:
    for fp in sorted(SITE_DIR.rglob("*.html")):
        rel = fp.relative_to(SITE_DIR)
        if not rel.parts:
            continue
        if rel.parts[0] in EXCLUDE_DIRS:
            continue
        yield fp


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_vercel_redirect_sources() -> set[str]:
    if not VERCEL_JSON.exists():
        return set()
    cfg = json.loads(VERCEL_JSON.read_text(encoding="utf-8"))
    redirects = cfg.get("redirects", [])
    sources: set[str] = set()
    for r in redirects:
        if not isinstance(r, dict):
            continue
        src = r.get("source")
        if isinstance(src, str) and src.startswith("/"):
            sources.add(src)
    return sources


def check_top60_urls_exist() -> CheckResult:
    missing: list[str] = []
    redirect_sources = load_vercel_redirect_sources()
    rows = read_csv_rows(TOP60_CSV)
    for row in rows:
        p = row.get("current_path") or ""
        if not p:
            continue
        fp = path_to_file(p)
        if fp.exists():
            continue
        # Acceptable if this path is a 301 source in vercel.json
        if p in redirect_sources:
            continue
        missing.append(p)
    ok = len(missing) == 0
    details = missing[:50]
    if len(missing) > 50:
        details.append(f"...and {len(missing) - 50} more")
    return CheckResult("Top60 URLs exist", ok, details)


def check_redirect_destinations_exist() -> CheckResult:
    missing: list[str] = []
    rows = read_csv_rows(REDIRECTS_CSV)
    for row in rows:
        dest = row.get("to_path") or ""
        if not dest.startswith("/"):
            continue
        fp = path_to_file(dest)
        if not fp.exists():
            missing.append(dest)
    ok = len(missing) == 0
    return CheckResult("Redirect destinations exist", ok, missing)


def check_vercel_redirects_present() -> CheckResult:
    if not VERCEL_JSON.exists():
        return CheckResult("vercel.json present", False, ["Missing vercel.json"])
    cfg = json.loads(VERCEL_JSON.read_text(encoding="utf-8"))
    redirects = cfg.get("redirects", [])
    redirect_pairs = {(r.get("source"), r.get("destination")) for r in redirects if isinstance(r, dict)}

    missing: list[str] = []
    rows = read_csv_rows(REDIRECTS_CSV)
    for row in rows:
        src = row.get("from_path") or ""
        dest = row.get("to_path") or ""
        if (src, dest) not in redirect_pairs:
            missing.append(f"{src} -> {dest}")
    ok = len(missing) == 0
    details = missing[:50]
    if len(missing) > 50:
        details.append(f"...and {len(missing) - 50} more")
    return CheckResult("Minimal redirects implemented", ok, details)


def check_canonicals_present() -> CheckResult:
    missing: list[str] = []
    pattern = re.compile(r'<link\s+[^>]*rel=["\']canonical["\']', re.IGNORECASE)
    for fp in iter_public_html_files():
        text = fp.read_text(encoding="utf-8", errors="replace")
        if not pattern.search(text):
            missing.append(str(fp.relative_to(SITE_DIR)))
    ok = len(missing) == 0
    return CheckResult("Canonical tag on public pages", ok, missing[:100])


def check_no_pages_links() -> CheckResult:
    offenders: list[str] = []
    pattern = re.compile(r'href=["\'](?:\./|\.\./)*pages/', re.IGNORECASE)
    for fp in iter_public_html_files():
        text = fp.read_text(encoding="utf-8", errors="replace")
        if pattern.search(text):
            offenders.append(str(fp.relative_to(SITE_DIR)))
    ok = len(offenders) == 0
    return CheckResult("No /pages links on public pages", ok, offenders[:100])


def check_core_files() -> list[CheckResult]:
    results: list[CheckResult] = []
    results.append(CheckResult("sitemap.xml present", SITEMAP_XML.exists(), [] if SITEMAP_XML.exists() else ["Missing sitemap.xml"]))
    results.append(CheckResult("robots API present", ROBOTS_API.exists(), [] if ROBOTS_API.exists() else ["Missing api/robots.js"]))
    results.append(CheckResult("contact API present", CONTACT_API.exists(), [] if CONTACT_API.exists() else ["Missing api/contact.js"]))

    favicon = SITE_DIR / "favicon.ico"
    results.append(CheckResult("favicon.ico present", favicon.exists(), [] if favicon.exists() else ["Missing favicon.ico"]))
    return results


def write_report(results: list[CheckResult], output_path: Path) -> None:
    ok_all = all(r.ok for r in results)
    lines: list[str] = []
    lines.append("# Go‑Live QA Report — Classic Vision Care (Static Site)")
    lines.append("")
    lines.append(f"**Report Date:** {date.today().isoformat()}")
    lines.append(f"**Site Folder:** `{SITE_DIR}`")
    lines.append(f"**Overall Status:** {'PASS' if ok_all else 'FAIL'}")
    lines.append("")
    lines.append("## Checklist Results")
    lines.append("")
    for r in results:
        lines.append(f"- {'✅' if r.ok else '❌'} **{r.name}**")
        if r.details:
            for d in r.details[:25]:
                lines.append(f"  - {d}")
            if len(r.details) > 25:
                lines.append(f"  - ...and {len(r.details) - 25} more")
    lines.append("")
    lines.append("## Go‑Live Notes (Action Items)")
    lines.append("")
    lines.append("- Set Vercel env vars for form delivery:")
    lines.append("  - `CONTACT_WEBHOOK_URL` (recommended) **or** `RESEND_API_KEY` + `CONTACT_EMAIL_TO`")
    lines.append("- Confirm GTM container `GTM-TT6JRB7` has triggers for:")
    lines.append("  - `cvc_phone_click`, `cvc_book_click`, and `cvc_form_submit` events (dataLayer)")
    lines.append("- After launch: submit `https://classicvisioncare.com/sitemap.xml` in Google Search Console and monitor Coverage + Rankings for 7–14 days.")
    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    results: list[CheckResult] = []
    results.extend(check_core_files())
    results.append(check_top60_urls_exist())
    results.append(check_redirect_destinations_exist())
    results.append(check_vercel_redirects_present())
    results.append(check_canonicals_present())
    results.append(check_no_pages_links())

    output_path = REPORTS_DIR / "01_GO_LIVE_QA_REPORT.md"
    write_report(results, output_path)
    print(f"Wrote report: {output_path}")

    # Exit non-zero if fail to make it CI-friendly if desired
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
