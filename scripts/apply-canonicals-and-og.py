#!/usr/bin/env python3
"""
Add/update canonical + OpenGraph/Twitter meta tags across the static site.

Rules:
- Canonical origin is always https://classicvisioncare.com
- For clean-route pages (/<route>/index.html), canonical is /<route>/
- For root index.html, canonical is /
- For legacy source pages under ./pages, canonical is the matching clean route
  when one exists (based on scripts/create-canonical-copies.py mapping).
"""

from __future__ import annotations

from dataclasses import dataclass
import html
import re
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
    "partials",
    "scripts",
    "styles",
}


def normalize_slash_path(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path


def to_canonical_url(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if path == "/":
        return f"{CANONICAL_ORIGIN}/"
    # If it's a file-like path (e.g. /pages/foo/bar.html), do not force a trailing slash.
    if re.search(r"/[^/]+\.[^/]+$", path):
        return f"{CANONICAL_ORIGIN}{path}"
    return f"{CANONICAL_ORIGIN}{normalize_slash_path(path)}"


@dataclass(frozen=True)
class HeadMeta:
    title: str | None
    description: str | None


def get_head_meta(html_text: str) -> HeadMeta:
    title_match = re.search(r"<title>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_match.group(1).strip()) if title_match else None

    desc_match = re.search(
        r'<meta\s+name=["\']description["\']\s+content=(?P<q>["\'])(?P<desc>.*?)(?P=q)\s*/?>',
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    description = html.unescape(desc_match.group("desc").strip()) if desc_match else None
    return HeadMeta(title=title, description=description)


def upsert_canonical(html_text: str, canonical_url: str) -> str:
    canonical_tag = f'  <link rel="canonical" href="{canonical_url}">'
    if re.search(r'<link\s+rel=["\']canonical["\']', html_text, flags=re.IGNORECASE):
        return re.sub(
            r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']\s*/?>',
            canonical_tag,
            html_text,
            flags=re.IGNORECASE,
        )

    # Prefer insert after meta description
    m = re.search(r'(<meta\s+name=["\']description["\'][^>]*>\s*)', html_text, flags=re.IGNORECASE)
    if m:
        insert_at = m.end(1)
        return html_text[:insert_at] + "\n" + canonical_tag + html_text[insert_at:]

    # Fallback: insert after </title>
    m = re.search(r"(</title>\s*)", html_text, flags=re.IGNORECASE)
    if m:
        insert_at = m.end(1)
        return html_text[:insert_at] + canonical_tag + "\n" + html_text[insert_at:]

    return html_text


def remove_existing_og_and_twitter(html_text: str) -> str:
    patterns = [
        r'\s*<meta\s+property=["\']og:[^"\']+["\'][^>]*>\s*',
        r'\s*<meta\s+name=["\']twitter:[^"\']+["\'][^>]*>\s*',
    ]
    for pat in patterns:
        html_text = re.sub(pat, "\n", html_text, flags=re.IGNORECASE)
    return html_text


def insert_og_and_twitter(html_text: str, canonical_url: str, meta: HeadMeta, og_type: str) -> str:
    if not meta.title and not meta.description:
        return html_text

    meta_lines: list[str] = []
    if meta.title:
        meta_lines.append(f'  <meta property="og:title" content="{html.escape(meta.title, quote=True)}">')
    if meta.description:
        meta_lines.append(
            f'  <meta property="og:description" content="{html.escape(meta.description, quote=True)}">'
        )
    meta_lines.append(f'  <meta property="og:url" content="{canonical_url}">')
    meta_lines.append(f'  <meta property="og:type" content="{og_type}">')
    meta_lines.append('  <meta name="twitter:card" content="summary_large_image">')

    block = "\n".join(meta_lines) + "\n"

    # Insert right after canonical tag (preferred)
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']\s*/?>\s*', html_text, flags=re.IGNORECASE)
    if m:
        insert_at = m.end(0)
        return html_text[:insert_at] + block + html_text[insert_at:]

    # Else insert before </head>
    m = re.search(r"</head>", html_text, flags=re.IGNORECASE)
    if m:
        insert_at = m.start(0)
        return html_text[:insert_at] + block + html_text[insert_at:]
    return html_text


def file_to_served_path(file_path: Path) -> str:
    if file_path == BASE_DIR / "index.html":
        return "/"
    if file_path.name == "index.html" and file_path.parent != BASE_DIR:
        rel = file_path.parent.relative_to(BASE_DIR)
        return normalize_slash_path(rel.as_posix())
    # For non-index pages, treat as file path (legacy)
    rel = file_path.relative_to(BASE_DIR)
    return "/" + rel.as_posix()


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


def main() -> int:
    # Load route mapping from scripts/create-canonical-copies.py (reverse map)
    # This avoids importing code from a script file.
    source_to_route: dict[str, str] = {
        "pages/about/index.html": "/about-us/",
        "pages/about/why-choose-us.html": "/why-choose-us/",
        "pages/about/testimonials.html": "/testimonials/",
        "pages/about/community.html": "/community-involvement/",
        "pages/about/careers.html": "/careers/",
        "pages/patients/contact.html": "/contact-us/",
        "pages/patients/new.html": "/new-patients/",
        "pages/patients/book.html": "/book-now/",
        "pages/patients/insurance.html": "/insurance/",
        "pages/legal/accessibility.html": "/accessibility/",
        "pages/legal/privacy.html": "/privacy-policy-2/",
        "pages/about/doctors/index.html": "/our-doctors/",
        "pages/about/doctors/mital-patel.html": "/dr-mital-patel-od/",
        "pages/about/doctors/bhumi-patel.html": "/dr-bhumi-patel-od/",
        "pages/locations/index.html": "/our-locations/",
        "pages/locations/kennesaw.html": "/eye-doctor-kennesaw-ga/",
        "pages/locations/east-cobb.html": "/eye-doctor-marietta/",
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
        "pages/dry-eye/treatments.html": "/dry-eye-treatment/",
        "pages/dry-eye/index.html": "/dry-eye-treatment/",
        "pages/dry-eye/treatments/blephex.html": "/dry-eye-treatment-blephex/",
        "pages/dry-eye/treatments/ipl.html": "/dry-eye-treatment-intense-pulsed-light/",
        "pages/dry-eye/treatments/miboflo.html": "/dry-eye-treatment-miboflo/",
        "pages/dry-eye/treatments/punctal-plugs.html": "/dry-eye-treatment-punctal-plugs/",
        "pages/dry-eye/treatments/eye-drops.html": "/dry-eye-treatment-eye-drops/",
        "pages/dry-eye/treatments/supplements.html": "/dry-eye-treatment-eye-supplements/",
        "pages/dry-eye/treatments/scleral-lenses.html": "/scleral-lenses-for-dry-eyes/",
        "pages/myopia/index.html": "/myopia-control/",
        "pages/myopia/children.html": "/myopia-in-children/",
        "pages/myopia/treatments/ortho-k.html": "/ortho-k-lenses-for-myopia-control/",
        "pages/myopia/treatments/atropine.html": "/myopia-control-atropine-eye-drops/",
        "pages/myopia/treatments/misight.html": "/misight-lenses-for-myopia-control/",
        "pages/myopia/treatments/multifocal.html": "/myopia-control-multifocal-lenses/",
        "pages/eyewear/specialty/index.html": "/specialty-contact-lenses/",
        "pages/eyewear/contact-lenses.html": "/contact-lenses/",
        "pages/eyewear/eyeglasses.html": "/eyeglasses/",
        "pages/eyewear/index.html": "/eyewear/",
        "pages/eyewear/sunglasses.html": "/sunglasses/",
        "pages/eyewear/specialty/scleral.html": "/scleral-lenses-atlanta/",
        "pages/eyewear/specialty/keratoconus.html": "/keratoconus-contacts/",
        "pages/eyewear/specialty/post-lasik.html": "/post-lasik-contacts/",
        "pages/services/conditions/allergies.html": "/allergies/",
        "pages/services/conditions/astigmatism.html": "/astigmatism/",
        "pages/about/blog.html": "/blog/",
    }

    updated = 0
    scanned = 0

    for file_path in sorted(BASE_DIR.rglob("*.html")):
        if not should_process(file_path):
            continue

        scanned += 1
        rel_str = file_path.relative_to(BASE_DIR).as_posix()

        served_path = file_to_served_path(file_path)
        canonical_path = served_path

        # If it's a legacy source page under ./pages that has a clean route, canonicalize it.
        if rel_str in source_to_route:
            canonical_path = source_to_route[rel_str]

        canonical_url = to_canonical_url(canonical_path)
        og_type = "website" if canonical_path in ("/", "/blog/") else "website"

        text = file_path.read_text(encoding="utf-8")
        before = text

        meta = get_head_meta(text)
        text = upsert_canonical(text, canonical_url)
        text = remove_existing_og_and_twitter(text)
        text = insert_og_and_twitter(text, canonical_url, meta, og_type=og_type)

        if text != before:
            file_path.write_text(text, encoding="utf-8")
            updated += 1

    print(f"Scanned {scanned} HTML files. Updated {updated}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
