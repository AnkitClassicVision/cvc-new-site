#!/usr/bin/env python3
"""
Targeted verification for fixes requested in website_feedback.pdf (2026-02-09).

This script is intentionally narrow: it checks only the pages/strings mentioned
in the feedback email/PDF so it stays stable as the site grows.
"""

from __future__ import annotations

import re
import json
from dataclasses import dataclass
from pathlib import Path


SITE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class PageCheck:
    rel_path: str
    must_contain: tuple[str, ...] = ()
    must_not_contain: tuple[str, ...] = ()
    must_match: tuple[re.Pattern[str], ...] = ()
    must_not_match: tuple[re.Pattern[str], ...] = ()


def read_text(rel_path: str) -> str:
    fp = SITE_DIR / rel_path
    if not fp.exists():
        raise FileNotFoundError(f"Missing file: {fp}")
    return fp.read_text(encoding="utf-8", errors="replace")


def run_check(check: PageCheck) -> list[str]:
    errors: list[str] = []
    text = read_text(check.rel_path)

    for s in check.must_contain:
        if s not in text:
            errors.append(f"{check.rel_path}: missing required text: {s!r}")

    for s in check.must_not_contain:
        if s in text:
            errors.append(f"{check.rel_path}: contains forbidden text: {s!r}")

    for pat in check.must_match:
        if not pat.search(text):
            errors.append(f"{check.rel_path}: missing required pattern: {pat.pattern!r}")

    for pat in check.must_not_match:
        if pat.search(text):
            errors.append(f"{check.rel_path}: contains forbidden pattern: {pat.pattern!r}")

    return errors


def read_json(rel_path: str) -> object:
    fp = SITE_DIR / rel_path
    if not fp.exists():
        raise FileNotFoundError(f"Missing file: {fp}")
    return json.loads(fp.read_text(encoding="utf-8", errors="replace"))


def has_redirect(vercel_config: object, source: str, destination: str) -> bool:
    if not isinstance(vercel_config, dict):
        return False
    redirects = vercel_config.get("redirects")
    if not isinstance(redirects, list):
        return False
    for r in redirects:
        if not isinstance(r, dict):
            continue
        if r.get("source") == source and r.get("destination") == destination:
            return True
    return False


def main() -> int:
    checks: list[PageCheck] = []

    checks.append(
        PageCheck(
            "index.html",
            must_contain=(
                # Services -> Conditions We Treat
                'href="/presbyopia/"',
                ">Presbyopia<",
                'href="/presbyopia/#sharpvision"',
                ">SharpVision<",
                # Dry eye dropdown / resources swap
                'href="/dry-eye-treatment-radio-frequency/"',
                ">Radio Frequency<",
                # Footer social links
                'href="https://www.facebook.com/CVCGlasses/"',
                'href="https://www.instagram.com/classic_vision_care/"',
                # Map embeds (simple q= form)
                "https://www.google.com/maps?q=1615+Ridenour+Blvd+Suite+201+Kennesaw+GA+30152&output=embed",
                "https://www.google.com/maps?q=3535+Roswell+Rd+Suite+8+Marietta+GA+30062&output=embed",
            ),
            must_not_contain=(
                # Explicitly called out in feedback
                "MiBoFlo",
                "miboflo",
            ),
        )
    )

    checks.append(
        PageCheck(
            "comprehensive-eye-exams/index.html",
            must_contain=("custom prescription plan",),
        )
    )

    checks.append(
        PageCheck(
            "blepharitis/index.html",
            must_contain=("Topcon Myah",),
            must_not_contain=("LipiScan", "LipiScan®"),
        )
    )

    checks.append(
        PageCheck(
            "computer-eye-strain/index.html",
            must_not_match=(re.compile(r"vision\s+therapy", re.IGNORECASE),),
        )
    )

    checks.append(
        PageCheck(
            "our-locations/index.html",
            must_contain=(
                # Feedback: clarify Dry Eye Spa treatments location
                "Advanced Dry Eye Spa treatments are performed at our Kennesaw office.",
                # East Cobb hours should include Monday (not incorrectly closed)
                "Monday & Wednesday",
            ),
            must_match=(
                # East Cobb: Friday should be closed (unique vs Kennesaw card)
                re.compile(r"<span>\s*Friday\s*</span>\s*<span[^>]*>\s*Closed", re.IGNORECASE),
            ),
        )
    )

    checks.append(
        PageCheck(
            "eye-doctor-marietta/index.html",
            must_contain=(
                # East Cobb hours should include Monday (not incorrectly closed)
                ">Monday</span><span>8:00 AM - 5:00 PM</span>",
                ">Friday</span><span>Closed</span>",
                # Feedback: don't claim Dry Eye Spa at East Cobb
                "Advanced in-office dry eye treatments are available at our Kennesaw location.",
            ),
        )
    )

    # Fax numbers were called out as incorrect; at minimum they should not remain wrong.
    checks.append(
        PageCheck(
            "eye-doctor-kennesaw-ga/index.html",
            must_not_match=(re.compile(r"<strong>Fax:</strong>", re.IGNORECASE),),
        )
    )
    checks.append(
        PageCheck(
            "eye-doctor-marietta/index.html",
            must_not_match=(re.compile(r"<strong>Fax:</strong>", re.IGNORECASE),),
        )
    )

    errors: list[str] = []
    for c in checks:
        errors.extend(run_check(c))

    # Legacy MiBoFlo URLs should redirect to Radio Frequency.
    try:
        vercel = read_json("vercel.json")
        if not has_redirect(vercel, "/dry-eye-treatment-miboflo/", "/dry-eye-treatment-radio-frequency/"):
            errors.append("vercel.json: missing redirect /dry-eye-treatment-miboflo/ -> /dry-eye-treatment-radio-frequency/")
        if not has_redirect(vercel, "/dry-eyes/what-is-mibo-thermoflo/", "/dry-eye-treatment-radio-frequency/"):
            errors.append("vercel.json: missing redirect /dry-eyes/what-is-mibo-thermoflo/ -> /dry-eye-treatment-radio-frequency/")
    except Exception as e:
        errors.append(f"vercel.json: failed to parse/validate redirects: {e}")

    # Sitemap should not list legacy URLs that now permanently redirect.
    try:
        sitemap = read_text("sitemap.xml")
        if "/dry-eye-treatment-miboflo/" in sitemap:
            errors.append("sitemap.xml: contains legacy URL /dry-eye-treatment-miboflo/ (should be excluded)")
        if "/dry-eyes/what-is-mibo-thermoflo/" in sitemap:
            errors.append("sitemap.xml: contains legacy URL /dry-eyes/what-is-mibo-thermoflo/ (should be excluded)")
    except Exception as e:
        errors.append(f"sitemap.xml: failed to read/validate: {e}")

    if errors:
        print("Verification FAILED:")
        for e in errors:
            print(f"- {e}")
        return 1

    print("Verification PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
