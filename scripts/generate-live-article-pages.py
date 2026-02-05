#!/usr/bin/env python3
"""
Generate clean, static article pages by scraping rendered HTML from the
current ClassicVisionCare.com site and wrapping it in the new site's layout.

Why scrape (instead of WP REST content):
- Several high-traffic posts use Divi shortcodes in REST output.
- The front-end HTML contains the fully rendered content we need to preserve.
"""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
ORIGIN = "https://classicvisioncare.com"


@dataclass(frozen=True)
class ScrapedArticle:
    title: str
    meta_description: str | None
    content_html: str
    date_published: str | None
    date_modified: str | None
    author: str | None


def read_layout_blocks() -> tuple[str, str]:
    index_text = (BASE_DIR / "index.html").read_text(encoding="utf-8")

    header_match = re.search(r"(<!-- Top Phone Bar -->.*?</header>)", index_text, flags=re.DOTALL)
    if not header_match:
        raise RuntimeError("Could not extract header from index.html")

    footer_match = re.search(
        r"(<!-- Footer -->.*?<script src=\"/scripts/editorial-forest\.js\"></script>)",
        index_text,
        flags=re.DOTALL,
    )
    if not footer_match:
        raise RuntimeError("Could not extract footer from index.html")

    return header_match.group(1), footer_match.group(1)


def scrape_article(path: str) -> ScrapedArticle:
    url = f"{ORIGIN}{path}"
    resp = requests.get(url, timeout=45)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")

    title = None
    og_title = soup.select_one('meta[property="og:title"]')
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    if not title and soup.title and soup.title.string:
        title = soup.title.string.strip()
    if not title:
        raise RuntimeError(f"Could not determine title for {url}")

    meta_description = None
    desc = soup.select_one('meta[name="description"]')
    if desc and desc.get("content"):
        meta_description = desc["content"].strip()

    article = soup.find("article")
    entry = soup.select_one(".entry-content")
    if not entry and article:
        entry = article
    if not entry:
        raise RuntimeError(f"Could not find article content for {url}")

    # Inner HTML of entry content.
    # If the post uses Divi builder markup, prefer the actual text-module bodies.
    divi_text_blocks = entry.select(".et_pb_text_inner")
    if divi_text_blocks:
        content_html = "\n".join(block.decode_contents().strip() for block in divi_text_blocks if block.decode_contents().strip())
    else:
        content_html = entry.decode_contents().strip()

    # Try common WP meta patterns
    date_published = None
    date_modified = None
    author = None

    time_published = soup.select_one("time.entry-date.published") or soup.select_one("time.published")
    if time_published and time_published.get("datetime"):
        date_published = time_published["datetime"]

    time_modified = soup.select_one("time.updated") or soup.select_one("time.entry-date.updated")
    if time_modified and time_modified.get("datetime"):
        date_modified = time_modified["datetime"]

    author_el = soup.select_one(".author.vcard a") or soup.select_one(".author a") or soup.select_one("span.author a")
    if author_el and author_el.get_text(strip=True):
        author = author_el.get_text(strip=True)

    return ScrapedArticle(
        title=title,
        meta_description=meta_description,
        content_html=content_html,
        date_published=date_published,
        date_modified=date_modified,
        author=author,
    )


def normalize_path(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path


def dest_for_path(path: str) -> Path:
    path = normalize_path(path)
    return BASE_DIR / path.strip("/") / "index.html"


def build_faq_jsonld(faq_items: list[tuple[str, str]], canonical_url: str) -> str:
    entities = []
    for q, a in faq_items:
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )

    import json

    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"{canonical_url}#faq",
        "mainEntity": entities,
    }
    return json.dumps(payload, ensure_ascii=False)


def render_page(path: str, scraped: ScrapedArticle, header: str, footer: str) -> str:
    canonical_path = normalize_path(path)
    canonical_url = f"{ORIGIN}{canonical_path}"

    title = scraped.title
    description = scraped.meta_description or ""

    extra_schema_blocks: list[str] = []
    extra_body_blocks: list[str] = []

    # P0 requirement: add punctal plug "fell out" FAQ + schema.
    if canonical_path == "/dry-eyes/punctal-plugs-for-dry-eyes-guide/":
        faq_items = [
            (
                "How do I know if my punctal plug fell out?",
                "Common signs include a return of dry eye symptoms, new irritation near the inner corner of the eyelid, or feeling like something is stuck in the eye. Some people have no symptoms at all. If you are unsure, we can check the plug position during an exam.",
            ),
            (
                "Do punctal plugs hurt?",
                "Most patients feel little to no discomfort. The procedure is quick, and you may notice mild irritation for a short time after placement.",
            ),
            (
                "Are punctal plugs covered by insurance?",
                "Coverage depends on your plan and the reason for treatment. Our team can help verify benefits and discuss options during your visit.",
            ),
            (
                "How long do punctal plugs last?",
                "Some plugs are temporary (designed to dissolve), while others are longer-lasting. Your doctor will recommend the right type based on your symptoms and goals.",
            ),
            (
                "What are possible side effects of punctal plugs?",
                "Possible side effects include temporary irritation, watering, or inflammation. Rarely, plugs can shift or cause infection. Contact our office if you have increasing pain, discharge, or vision changes.",
            ),
        ]
        extra_schema_blocks.append(build_faq_jsonld(faq_items, canonical_url))

        extra_body_blocks.append(
            """
    <section class="mt-12 bg-cvc-cream rounded-2xl p-8">
      <h2 class="font-display text-2xl md:text-3xl text-cvc-charcoal mb-4">Quick answers about punctal plugs</h2>
      <div class="grid md:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-6">
          <h3 class="font-semibold text-cvc-charcoal mb-2">Did my plug fall out?</h3>
          <p class="text-gray-600 text-sm leading-relaxed">A sudden return of dryness is common, but the only way to know for sure is a quick exam. If you are unsure, schedule a visit and we will check the plug position.</p>
        </div>
        <div class="bg-white rounded-xl p-6">
          <h3 class="font-semibold text-cvc-charcoal mb-2">Should I call right away?</h3>
          <p class="text-gray-600 text-sm leading-relaxed">Call us if you have new pain, discharge, significant redness, or any vision change. Otherwise, we can usually check and replace plugs during a routine visit.</p>
        </div>
      </div>
      <div class="mt-6 flex flex-col sm:flex-row gap-3">
        <a href="/book-now/" class="btn-primary">Book an appointment</a>
        <a href="tel:+17704992020" class="btn-secondary">Call Kennesaw</a>
        <a href="tel:+16785608065" class="btn-secondary">Call East Cobb</a>
      </div>
    </section>
            """.strip()
        )

    # Medical disclaimer block for symptom articles (P1 requirement).
    if canonical_path.startswith("/eye-treatment/"):
        extra_body_blocks.insert(
            0,
            """
    <div class="bg-cvc-cream rounded-xl p-6 mb-10 border border-cvc-teal-100">
      <p class="text-sm text-gray-700 leading-relaxed"><strong>Medical note:</strong> This page is for educational purposes and does not replace medical advice. If you have severe eye pain, sudden vision changes, new flashes/floaters, or symptoms after an injury, seek urgent care.</p>
    </div>
            """.strip()
        )

    schema_lines = "\n".join(
        f'  <script type="application/ld+json">{block.replace("</", "<\\/")}</script>' for block in extra_schema_blocks
    )

    hero = f"""
    <section class=\"py-16 lg:py-20 bg-gradient-to-br from-cvc-teal-50 to-cvc-cream\">
      <div class=\"max-w-4xl mx-auto px-6\">
        <nav class=\"text-sm text-gray-600 mb-4\" aria-label=\"Breadcrumb\">
          <ol class=\"flex flex-wrap gap-2\">
            <li><a href=\"/\" class=\"hover:underline\">Home</a></li>
            <li aria-hidden=\"true\">/</li>
            <li><a href=\"/blog/\" class=\"hover:underline\">Resources</a></li>
          </ol>
        </nav>
        <h1 class=\"font-display text-3xl md:text-5xl text-cvc-charcoal leading-tight mb-4\">{html.escape(title)}</h1>
        {f'<p class=\"text-lg text-gray-600 max-w-2xl\">{html.escape(description)}</p>' if description else ''}
        <div class=\"mt-6 flex flex-col sm:flex-row gap-3\">
          <a href=\"/book-now/\" class=\"btn-primary\">Book an appointment</a>
          <a href=\"/dry-eye-treatment/\" class=\"btn-secondary\">Dry Eye Spa</a>
          <a href=\"/our-locations/\" class=\"btn-secondary\">Locations</a>
        </div>
      </div>
    </section>
    """.strip()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  {f'<meta name="description" content="{html.escape(description, quote=True)}">' if description else ''}
  <link rel="stylesheet" href="/styles/tailwind.css">
  <link rel="stylesheet" href="/styles/editorial-forest.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400&family=Instrument+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
{schema_lines}
</head>
<body class="cvc-editorial font-body text-cvc-charcoal bg-white">
{header}

<main id="main-content">
{hero}
  <section class="py-14 lg:py-16 bg-white">
    <div class="max-w-3xl mx-auto px-6">
{extra_body_blocks[0] if extra_body_blocks and canonical_path.startswith('/eye-treatment/') else ''}
      <article class="space-y-6">
{scraped.content_html}
      </article>
{'' if not extra_body_blocks else ('\\n'.join(extra_body_blocks[1:] if canonical_path.startswith('/eye-treatment/') else extra_body_blocks))}
      <div class="mt-12 bg-cvc-cream rounded-2xl p-8">
        <h2 class="font-display text-2xl text-cvc-charcoal mb-3">Need help now?</h2>
        <p class="text-gray-600 mb-6">If you are dealing with symptoms and want a clear plan, we can help. Book an appointment or call the location closest to you.</p>
        <div class="flex flex-col sm:flex-row gap-3">
          <a href="/book-now/" class="btn-primary">Book an appointment</a>
          <a href="tel:+17704992020" class="btn-secondary">Call Kennesaw</a>
          <a href="tel:+16785608065" class="btn-secondary">Call East Cobb</a>
        </div>
      </div>
    </div>
  </section>
</main>

{footer}
</body>
</html>
"""


def iter_paths(input_paths: list[str]) -> Iterable[str]:
    for p in input_paths:
        p = p.strip()
        if not p:
            continue
        yield normalize_path(p)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        help="Canonical paths to scrape from classicvisioncare.com (e.g. /dry-eyes/what-is-mibo-thermoflo/)",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing generated pages.")
    args = parser.parse_args()

    if not args.paths:
        print("No paths provided. Example:\n  python3 scripts/generate-live-article-pages.py /ocular-rosacea/all-about-ocular-rosacea/")
        return 2

    header, footer = read_layout_blocks()

    generated = 0
    skipped = 0
    for path in iter_paths(args.paths):
        dest = dest_for_path(path)
        if dest.exists() and not args.overwrite:
            print(f"[SKIP] {path} (exists)")
            skipped += 1
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        scraped = scrape_article(path)
        page_html = render_page(path, scraped, header=header, footer=footer)
        dest.write_text(page_html, encoding="utf-8")
        print(f"[OK]   {path} → {dest.relative_to(BASE_DIR)}")
        generated += 1

    print(f"\nDone. Generated: {generated}, Skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
