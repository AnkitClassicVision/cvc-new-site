#!/usr/bin/env python3
"""
Rewrite internal links from the build-source paths (./pages/.../*.html) to the
canonical, clean URL structure (e.g. /eye-care-services/).

Also normalizes common asset paths to root-relative so they work at any depth.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

BASE_DIR = Path(__file__).resolve().parent.parent

EXCLUDE_DIRS = {
    ".git",
    ".superdesign",
    "api",
    "content",
    "dev",
    "node_modules",
    "partials",
    "scripts",
}


# Map "source href" (relative path inside repo) -> canonical href (root-relative).
HREF_MAP: dict[str, str] = {
    "index.html": "/",
    "pages/services/index.html": "/eye-care-services/",
    "pages/services/exams/comprehensive.html": "/comprehensive-eye-exams/",
    "pages/services/exams/contact-lens.html": "/contact-lens-exams/",
    "pages/services/exams/diabetic.html": "/diabetic-eye-exam/",
    "pages/services/pediatric/eye-care.html": "/pediatric-eye-care/",
    "pages/services/pediatric/eye-exams.html": "/pediatric-eye-exams/",
    "pages/services/pediatric/childrens-exam.html": "/childrens-eye-exam/",
    "pages/services/pediatric/school-screening.html": "/school-vision-screening/",
    "pages/services/conditions/glaucoma.html": "/glaucoma/",
    "pages/services/conditions/macular-degeneration.html": "/macular-degeneration/",
    "pages/services/conditions/allergies.html": "/allergies/",
    "pages/services/conditions/astigmatism.html": "/astigmatism/",
    "pages/dry-eye/index.html": "/dry-eye-treatment/",
    "pages/dry-eye/treatments.html": "/dry-eye-treatment/",
    "pages/dry-eye/treatments/ipl.html": "/dry-eye-treatment-intense-pulsed-light/",
    "pages/dry-eye/treatments/miboflo.html": "/dry-eye-treatment-miboflo/",
    "pages/dry-eye/treatments/blephex.html": "/dry-eye-treatment-blephex/",
    "pages/dry-eye/treatments/punctal-plugs.html": "/dry-eye-treatment-punctal-plugs/",
    "pages/dry-eye/treatments/scleral-lenses.html": "/scleral-lenses-for-dry-eyes/",
    "pages/dry-eye/treatments/eye-drops.html": "/dry-eye-treatment-eye-drops/",
    "pages/dry-eye/treatments/supplements.html": "/dry-eye-treatment-eye-supplements/",
    "pages/myopia/index.html": "/myopia-control/",
    "pages/myopia/treatments/misight.html": "/misight-lenses-for-myopia-control/",
    "pages/myopia/treatments/ortho-k.html": "/ortho-k-lenses-for-myopia-control/",
    "pages/myopia/treatments/atropine.html": "/myopia-control-atropine-eye-drops/",
    "pages/myopia/treatments/multifocal.html": "/myopia-control-multifocal-lenses/",
    "pages/myopia/children.html": "/myopia-in-children/",
    "pages/eyewear/index.html": "/eyewear/",
    "pages/eyewear/eyeglasses.html": "/eyeglasses/",
    "pages/eyewear/sunglasses.html": "/sunglasses/",
    "pages/eyewear/contact-lenses.html": "/contact-lenses/",
    "pages/eyewear/specialty/index.html": "/specialty-contact-lenses/",
    "pages/eyewear/specialty/scleral.html": "/scleral-lenses-atlanta/",
    "pages/eyewear/specialty/keratoconus.html": "/keratoconus-contacts/",
    "pages/eyewear/specialty/post-lasik.html": "/post-lasik-contacts/",
    "pages/locations/index.html": "/our-locations/",
    "pages/locations/kennesaw.html": "/eye-doctor-kennesaw-ga/",
    "pages/locations/east-cobb.html": "/eye-doctor-marietta/",
    "pages/about/index.html": "/about-us/",
    "pages/about/why-choose-us.html": "/why-choose-us/",
    "pages/about/testimonials.html": "/testimonials/",
    "pages/about/community.html": "/community-involvement/",
    "pages/about/doctors/index.html": "/our-doctors/",
    "pages/about/doctors/mital-patel.html": "/dr-mital-patel-od/",
    "pages/about/doctors/bhumi-patel.html": "/dr-bhumi-patel-od/",
    "pages/about/careers.html": "/careers/",
    "pages/about/blog.html": "/blog/",
    "pages/patients/new.html": "/new-patients/",
    "pages/patients/insurance.html": "/insurance/",
    "pages/patients/contact.html": "/contact-us/",
    "pages/patients/book.html": "/book-now/",
    "pages/legal/privacy.html": "/privacy-policy-2/",
    "pages/legal/accessibility.html": "/accessibility/",
}


ASSET_PREFIX_MAP: dict[str, str] = {
    "styles/editorial-forest.css": "/styles/editorial-forest.css",
    "scripts/editorial-forest.js": "/scripts/editorial-forest.js",
}

INTERNAL_HOSTS = {
    "classicvisioncare.us23.cdn-alpha.com",
}


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


def rewrite_attr_values(html_text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        attr = match.group("attr")
        quote = match.group("quote")
        value = match.group("value")
        absolute_internal = False

        # Anchors + special protocols
        if value.startswith(("#", "tel:", "mailto:", "javascript:", "data:")):
            return match.group(0)

        # Rewrite absolute URLs that point back to our origin(s) into root-relative paths.
        if value.startswith(("http://", "https://", "//")):
            parsed = urlsplit("https:" + value if value.startswith("//") else value)
            if parsed.netloc and parsed.netloc.lower() not in INTERNAL_HOSTS:
                return match.group(0)
            absolute_internal = True
            value = parsed.path or "/"
            if parsed.query:
                value += f"?{parsed.query}"
            if parsed.fragment:
                value += f"#{parsed.fragment}"

        # Normalize leading ./ or ../ segments for lookup, then split query/fragment
        normalized = re.sub(r"^(?:\./|\.\./)+", "", value)
        parts = urlsplit(normalized)
        normalized_path = parts.path.lstrip("/")
        suffix = ""
        if parts.query:
            suffix += f"?{parts.query}"
        if parts.fragment:
            suffix += f"#{parts.fragment}"

        # Assets first
        if normalized_path in ASSET_PREFIX_MAP:
            return f'{attr}={quote}{ASSET_PREFIX_MAP[normalized_path]}{suffix}{quote}'

        # Site images/scripts/styles referenced relatively
        for static_dir in ("images/", "styles/", "scripts/"):
            if normalized_path.startswith(static_dir):
                return f'{attr}={quote}/{normalized_path}{suffix}{quote}'

        # Canonical href remap
        if normalized_path in HREF_MAP:
            return f'{attr}={quote}{HREF_MAP[normalized_path]}{suffix}{quote}'

        # If it was an absolute internal URL and we didn't match a known mapping,
        # still normalize to a root-relative path for preview + post-cutover parity.
        if absolute_internal and parts.path:
            path_out = parts.path if parts.path.startswith("/") else "/" + parts.path
            return f'{attr}={quote}{path_out}{suffix}{quote}'

        return match.group(0)

    pattern = r'(?P<attr>href|src)=(?P<quote>["\'])(?P<value>[^"\']+)(?P=quote)'
    return re.sub(pattern, repl, html_text)


def main() -> int:
    updated = 0
    scanned = 0

    for file_path in sorted(BASE_DIR.rglob("*.html")):
        if not should_process(file_path):
            continue
        scanned += 1
        before = file_path.read_text(encoding="utf-8")
        after = rewrite_attr_values(before)
        if after != before:
            file_path.write_text(after, encoding="utf-8")
            updated += 1

    print(f"Scanned {scanned} HTML files. Rewired {updated}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
