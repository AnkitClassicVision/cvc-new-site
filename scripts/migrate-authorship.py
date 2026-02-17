#!/usr/bin/env python3
"""
One-time migration: apply proper E-E-A-T authorship to all article pages.

What this script does:
1. Assigns each post to the correct author (Dr. Mital Patel for medical,
   Ankit Patel for community/lifestyle).
2. Replaces Yoast JSON-LD schema with clean author-attributed schema.
3. Replaces plain-text bylines with rich author bylines (photo + link).
4. Adds "Medically reviewed by" footer on medical posts.
5. Generates Ankit Patel's author page (/author/ankit-patel/).
6. Adds Physician schema + articles section to Dr. Mital Patel's page.
7. Updates wp_blog_posts.json manifest with author_slug and content_type.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
ORIGIN = "https://classicvisioncare.com"


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_authors() -> tuple[dict[str, Any], set[str]]:
    path = BASE_DIR / "content" / "authors.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    community_slugs = set(data.pop("_community_slugs", []))
    return data, community_slugs


def load_manifest() -> list[dict[str, Any]]:
    path = BASE_DIR / "content" / "wp_blog_posts.json"
    return json.loads(path.read_text(encoding="utf-8"))


def read_layout_blocks() -> tuple[str, str]:
    index_text = (BASE_DIR / "index.html").read_text(encoding="utf-8")

    header_match = re.search(
        r"(<!-- Top Phone Bar -->.*?</header>)", index_text, flags=re.DOTALL
    )
    if not header_match:
        raise RuntimeError("Could not extract header from index.html")

    footer_match = re.search(
        r'(<!-- Footer -->.*?<script src="/scripts/editorial-forest\.js"></script>)',
        index_text,
        flags=re.DOTALL,
    )
    if not footer_match:
        raise RuntimeError("Could not extract footer from index.html")

    return header_match.group(1), footer_match.group(1)


# ---------------------------------------------------------------------------
# Author assignment
# ---------------------------------------------------------------------------

def assign_author(slug: str, community_slugs: set[str]) -> str:
    """Return author key: 'dr-mital-patel' or 'ankit-patel'."""
    if slug in community_slugs:
        return "ankit-patel"
    return "dr-mital-patel"


# ---------------------------------------------------------------------------
# Schema builders
# ---------------------------------------------------------------------------

def _clean_title(raw: str) -> str:
    """Strip site-name suffixes like ' | Classic Vision Care'."""
    for sep in (" | ", " - Classic Vision Care"):
        if sep in raw:
            raw = raw.split(sep)[0]
    return raw.strip()


def build_article_schema(
    post: dict[str, Any], author_slug: str, authors: dict[str, Any]
) -> str:
    author = authors[author_slug]
    canonical = f"{ORIGIN}{post['path']}"
    is_medical = author_slug == "dr-mital-patel"
    headline = _clean_title(post.get("title") or "")

    graph: list[dict[str, Any]] = []

    # -- Article / MedicalWebPage --
    article: dict[str, Any] = {
        "@type": "MedicalWebPage" if is_medical else ["Article", "BlogPosting"],
        "@id": f"{canonical}#article",
        "headline": headline,
        "author": {"@id": author["schema_id"]},
        "publisher": {"@id": f"{ORIGIN}/#organization"},
        "mainEntityOfPage": {"@id": canonical},
        "inLanguage": "en-US",
    }
    if post.get("date_published"):
        article["datePublished"] = post["date_published"]
    if post.get("date_modified"):
        article["dateModified"] = post["date_modified"]
    if post.get("description"):
        article["description"] = post["description"]
    if post.get("featured_image"):
        img = post["featured_image"]
        article["image"] = img if img.startswith("http") else f"{ORIGIN}{img}"
    graph.append(article)

    # -- WebPage --
    webpage: dict[str, Any] = {
        "@type": "WebPage",
        "@id": canonical,
        "url": canonical,
        "name": post.get("title") or headline,
        "isPartOf": {"@id": f"{ORIGIN}/#website"},
        "author": {"@id": author["schema_id"]},
        "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
        "inLanguage": "en-US",
    }
    if post.get("date_published"):
        webpage["datePublished"] = post["date_published"]
    if post.get("date_modified"):
        webpage["dateModified"] = post["date_modified"]
    if post.get("description"):
        webpage["description"] = post["description"]
    graph.append(webpage)

    # -- Author (Person or Physician) --
    author_node: dict[str, Any] = {
        "@type": author["schema_type"],
        "@id": author["schema_id"],
        "name": author["name"],
        "url": f"{ORIGIN}{author['author_page']}",
        "image": f"{ORIGIN}{author['image']}",
        "sameAs": author.get("sameAs", []),
        "worksFor": {"@id": f"{ORIGIN}/#organization"},
    }
    if author.get("credentials"):
        author_node["jobTitle"] = author["title"]
        if author["credentials"].get("specialties"):
            author_node["knowsAbout"] = author["credentials"]["specialties"]
    else:
        author_node["jobTitle"] = author["title"]
    graph.append(author_node)

    # -- BreadcrumbList --
    graph.append(
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumb",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": f"{ORIGIN}/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Resources",
                    "item": f"{ORIGIN}/blog/",
                },
                {"@type": "ListItem", "position": 3, "name": headline},
            ],
        }
    )

    # -- Organization --
    graph.append(
        {
            "@type": "Organization",
            "@id": f"{ORIGIN}/#organization",
            "name": "Classic Vision Care",
            "url": f"{ORIGIN}/",
            "logo": f"{ORIGIN}/images/logos/EOP1600_Classic_Logo_FN.png",
        }
    )

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Byline + review footer builders
# ---------------------------------------------------------------------------

def _fmt_date(date_str: str | None) -> str:
    if not date_str:
        return ""
    try:
        parsed = dt.datetime.fromisoformat(str(date_str).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        parsed = parsed.astimezone(dt.timezone.utc)
        return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}"
    except Exception:
        return ""


def build_rich_byline(
    post: dict[str, Any], author_slug: str, authors: dict[str, Any]
) -> str:
    author = authors[author_slug]
    date_text = _fmt_date(post.get("date_published"))

    safe_name = html.escape(author["name"])
    safe_img = html.escape(author["image"], quote=True)
    safe_alt = html.escape(author["image_alt"], quote=True)
    safe_page = html.escape(author["author_page"], quote=True)

    date_line = ""
    if date_text:
        date_line = f'<p class="text-xs text-gray-500">{html.escape(date_text)}</p>'

    return (
        f'<div class="mt-4 flex items-center gap-3">\n'
        f'        <img src="{safe_img}" alt="{safe_alt}" '
        f'class="w-10 h-10 rounded-full object-cover" width="40" height="40" loading="lazy">\n'
        f"        <div>\n"
        f'          <p class="text-sm font-medium text-cvc-charcoal">'
        f'<a href="{safe_page}" class="hover:underline">{safe_name}</a></p>\n'
        f"          {date_line}\n"
        f"        </div>\n"
        f"      </div>"
    )


def build_medical_review_footer(authors: dict[str, Any]) -> str:
    a = authors["dr-mital-patel"]
    return (
        f'<div class="mt-8 flex items-center gap-3 border-t border-gray-100 pt-6">\n'
        f'        <img src="{a["image"]}" alt="{html.escape(a["image_alt"], quote=True)}" '
        f'class="w-12 h-12 rounded-full object-cover" width="48" height="48" loading="lazy">\n'
        f"        <div>\n"
        f'          <p class="text-sm text-gray-500">Medically reviewed by</p>\n'
        f'          <p class="text-sm font-medium text-cvc-charcoal">'
        f'<a href="{a["author_page"]}" class="hover:underline">{html.escape(a["name"])}</a>'
        f" &middot; Optometrist</p>\n"
        f"        </div>\n"
        f"      </div>"
    )


# ---------------------------------------------------------------------------
# Article migration
# ---------------------------------------------------------------------------

JSONLD_RE = re.compile(
    r'\s*<script type="application/ld\+json">.*?</script>', re.DOTALL
)
FAQPAGE_RE = re.compile(
    r'(<script type="application/ld\+json">\s*\{[^<]*?"@type"\s*:\s*"FAQPage"[^<]*?</script>)',
    re.DOTALL,
)
BYLINE_RE = re.compile(
    r'<p class="mt-4 text-sm text-gray-500">[^<]*</p>'
)
RICH_BYLINE_RE = re.compile(
    r'<div class="mt-4 flex items-center gap-3">\s*'
    r'<img src="[^"]*"[^>]*>\s*'
    r'<div>\s*'
    r'<p class="text-sm font-medium text-cvc-charcoal">[^<]*<a[^>]*>[^<]*</a></p>\s*'
    r'(?:<p class="text-xs text-gray-500">[^<]*</p>\s*)?'
    r'</div>\s*'
    r'</div>',
    re.DOTALL,
)


def migrate_article(
    file_path: Path,
    post: dict[str, Any],
    author_slug: str,
    authors: dict[str, Any],
) -> bool:
    """Migrate a single article HTML file. Returns True if modified."""
    if not file_path.exists():
        print(f"  [MISS] {file_path.relative_to(BASE_DIR)}")
        return False

    text = file_path.read_text(encoding="utf-8")
    original = text
    is_medical = author_slug == "dr-mital-patel"

    # ---- 1. Replace JSON-LD schema ----
    new_schema = build_article_schema(post, author_slug, authors)
    new_schema_escaped = new_schema.replace("</", "<\\/")
    new_schema_tag = f'  <script type="application/ld+json">{new_schema_escaped}</script>'

    # Preserve FAQPage schema if present (punctal plugs, etc.)
    faq_match = FAQPAGE_RE.search(text)
    faq_tag = faq_match.group(1) if faq_match else ""

    # Remove ALL existing JSON-LD blocks
    text = JSONLD_RE.sub("", text)

    # Insert new schema before </head>
    insert = new_schema_tag
    if faq_tag:
        insert += f"\n{faq_tag}"
    text = text.replace("</head>", f"{insert}\n</head>")

    # ---- 2. Replace byline ----
    new_byline = build_rich_byline(post, author_slug, authors)

    if RICH_BYLINE_RE.search(text):
        text = RICH_BYLINE_RE.sub(new_byline, text, count=1)
    elif BYLINE_RE.search(text):
        text = BYLINE_RE.sub(new_byline, text, count=1)
    else:
        # Try to insert after description <p> in hero
        desc_m = re.search(
            r'(<p class="text-lg text-gray-600 max-w-2xl">[^<]*</p>)', text
        )
        if desc_m:
            text = text[: desc_m.end()] + f"\n      {new_byline}" + text[desc_m.end() :]
        else:
            # Fallback: insert after </h1>
            h1_m = re.search(r"(</h1>)", text)
            if h1_m:
                text = text[: h1_m.end()] + f"\n      {new_byline}" + text[h1_m.end() :]

    # ---- 3. Add or update medical review footer ----
    if is_medical:
        new_footer = build_medical_review_footer(authors)
        # Replace existing footer if present
        existing_footer_re = re.compile(
            r'<div class="mt-8 flex items-center gap-3 border-t border-gray-100 pt-6">\s*'
            r'<img src="[^"]*"[^>]*>\s*'
            r'<div>\s*'
            r'<p class="text-sm text-gray-500">Medically reviewed by</p>\s*'
            r'<p class="text-sm font-medium text-cvc-charcoal">[^<]*<a[^>]*>[^<]*</a>[^<]*</p>\s*'
            r'</div>\s*'
            r'</div>',
            re.DOTALL,
        )
        if existing_footer_re.search(text):
            text = existing_footer_re.sub(new_footer, text, count=1)
        elif "Medically reviewed by" not in text:
            anchor = '<div class="mt-12 bg-cvc-cream rounded-2xl p-8">'
            if anchor in text:
                text = text.replace(anchor, f"{new_footer}\n      {anchor}", 1)

    if text != original:
        file_path.write_text(text, encoding="utf-8")
        return True
    return False


# ---------------------------------------------------------------------------
# Author page generation (Ankit Patel)
# ---------------------------------------------------------------------------

def generate_ankit_author_page(
    authors: dict[str, Any],
    manifest: list[dict[str, Any]],
    community_slugs: set[str],
    header: str,
    footer: str,
) -> None:
    a = authors["ankit-patel"]

    # Collect community posts
    posts = [p for p in manifest if p["slug"] in community_slugs]
    posts.sort(key=lambda p: str(p.get("date_published") or ""), reverse=True)

    post_cards = ""
    for p in posts:
        safe_path = html.escape(p["path"], quote=True)
        safe_title = html.escape(_clean_title(p.get("title") or ""))
        safe_desc = html.escape(p.get("description") or "")
        date_text = _fmt_date(p.get("date_published"))
        post_cards += f"""
          <a href="{safe_path}" class="block rounded-2xl border border-gray-100 bg-white p-6 hover:shadow-md transition-shadow">
            {f'<p class="text-xs text-gray-500 mb-2">{html.escape(date_text)}</p>' if date_text else ''}
            <h3 class="font-semibold text-cvc-charcoal mb-2">{safe_title}</h3>
            {f'<p class="text-gray-600 text-sm leading-relaxed">{safe_desc}</p>' if safe_desc else ''}
          </a>
"""

    # Book section
    book = a.get("book")
    book_section = ""
    if book:
        safe_book_title = html.escape(book["title"])
        safe_book_url = html.escape(book["url"], quote=True)
        book_section = f"""
  <section class="py-16 lg:py-20 bg-cvc-cream">
    <div class="max-w-4xl mx-auto px-6">
      <h2 class="font-display text-2xl md:text-3xl text-cvc-charcoal mb-6">Book</h2>
      <div class="flex flex-col sm:flex-row items-start gap-6 bg-white rounded-2xl p-8 shadow-sm">
        <div class="shrink-0">
          <svg class="w-16 h-20 text-cvc-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <div>
          <h3 class="font-display text-xl text-cvc-charcoal mb-2">{safe_book_title}</h3>
          <p class="text-gray-600 text-sm leading-relaxed mb-4">A guide for optometry practice owners on mastering resourcing, performance, and building a thriving practice.</p>
          <a href="{safe_book_url}" target="_blank" rel="noopener" class="inline-flex items-center gap-2 text-cvc-teal-600 font-medium hover:underline text-sm">
            View on Amazon
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
          </a>
        </div>
      </div>
    </div>
  </section>
"""

    # Schema: Person + ProfilePage
    person_node: dict[str, Any] = {
        "@type": "Person",
        "@id": a["schema_id"],
        "name": a["name"],
        "url": f"{ORIGIN}/author/ankit-patel/",
        "image": f"{ORIGIN}{a['image']}",
        "jobTitle": a["title"],
        "description": a["bio"],
        "sameAs": a.get("sameAs", []),
        "worksFor": {
            "@type": "Organization",
            "@id": f"{ORIGIN}/#organization",
            "name": "Classic Vision Care",
        },
    }
    if book:
        person_node["author"] = {
            "@type": "Book",
            "name": book["title"],
            "url": book["url"],
        }

    schema_obj = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfilePage",
                "@id": f"{ORIGIN}/author/ankit-patel/",
                "url": f"{ORIGIN}/author/ankit-patel/",
                "name": f"{a['name']} — Author at Classic Vision Care",
                "mainEntity": {"@id": a["schema_id"]},
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "inLanguage": "en-US",
            },
            person_node,
        ],
    }
    schema_json = json.dumps(schema_obj, ensure_ascii=False).replace("</", "<\\/")

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(a['name'])} — Author | Classic Vision Care</title>
  <meta name="description" content="{html.escape(a['bio'], quote=True)}">
  <link rel="canonical" href="{ORIGIN}/author/ankit-patel/">
  <meta property="og:title" content="{html.escape(a['name'])} — Author | Classic Vision Care">
  <meta property="og:description" content="{html.escape(a['bio'], quote=True)}">
  <meta property="og:url" content="{ORIGIN}/author/ankit-patel/">
  <meta property="og:image" content="{ORIGIN}/images/logos/cropped-EOP1600_Classic_Logo_FN.png">
  <meta property="og:site_name" content="Classic Vision Care">
  <meta property="og:locale" content="en_US">
  <meta property="og:type" content="profile">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/styles/tailwind.css">
  <link rel="stylesheet" href="/styles/editorial-forest.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="/fonts/TT_Norms_Pro_Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/TT_Norms_Pro_Bold.woff2" as="font" type="font/woff2" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet"></noscript>
  <script type="application/ld+json">{schema_json}</script>
</head>
<body class="cvc-editorial font-body text-cvc-charcoal bg-white">
  <!-- Skip Link for Accessibility -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

{header}

<main id="main-content">
  <section class="py-16 lg:py-24 bg-gradient-to-br from-cvc-teal-50 to-cvc-cream">
    <div class="max-w-4xl mx-auto px-6">
      <nav class="text-sm text-gray-600 mb-6" aria-label="Breadcrumb">
        <ol class="flex flex-wrap gap-2">
          <li><a href="/" class="hover:underline">Home</a></li>
          <li aria-hidden="true">/</li>
          <li><a href="/blog/" class="hover:underline">Resources</a></li>
          <li aria-hidden="true">/</li>
          <li class="text-cvc-charcoal">{html.escape(a['name'])}</li>
        </ol>
      </nav>
      <div class="flex flex-col md:flex-row items-start gap-8">
        <img src="{a['image']}" alt="{html.escape(a['image_alt'], quote=True)}"
             class="w-32 h-32 rounded-2xl object-cover shadow-md" width="128" height="128">
        <div>
          <h1 class="font-display text-3xl md:text-4xl text-cvc-charcoal leading-tight mb-2">{html.escape(a['name'])}</h1>
          <p class="text-cvc-teal-500 font-medium mb-4">{html.escape(a['role'])}</p>
          <p class="text-gray-600 leading-relaxed max-w-2xl">{html.escape(a['bio'])}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="py-16 lg:py-20 bg-white">
    <div class="max-w-4xl mx-auto px-6">
      <h2 class="font-display text-2xl md:text-3xl text-cvc-charcoal mb-8">Articles by {html.escape(a['name'])}</h2>
      <div class="grid md:grid-cols-2 gap-6">
{post_cards}
      </div>
    </div>
  </section>

{book_section}
  <section class="py-16 bg-cvc-cream">
    <div class="max-w-4xl mx-auto px-6 text-center">
      <h2 class="font-display text-2xl md:text-3xl text-cvc-charcoal mb-4">Want a personalized plan?</h2>
      <p class="text-gray-600 mb-6 max-w-2xl mx-auto">Our doctors take time to listen, explain, and recommend options that fit your goals. Book an appointment at the location closest to you.</p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <a href="/book-now/" class="btn-primary">Book an appointment</a>
        <a href="/eye-doctor-kennesaw-ga/" class="btn-secondary">Kennesaw</a>
        <a href="/eye-doctor-marietta/" class="btn-secondary">East Cobb</a>
      </div>
    </div>
  </section>
</main>

{footer}
</body>
</html>
"""

    dest = BASE_DIR / "author" / "ankit-patel" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page_html, encoding="utf-8")
    print(f"  [OK] Generated {dest.relative_to(BASE_DIR)}")


# ---------------------------------------------------------------------------
# Author page generation (Dr. Mital Patel)
# ---------------------------------------------------------------------------

def generate_dr_mital_author_page(
    authors: dict[str, Any],
    manifest: list[dict[str, Any]],
    community_slugs: set[str],
    header: str,
    footer: str,
) -> None:
    a = authors["dr-mital-patel"]

    # Collect medical posts
    posts = [p for p in manifest if p["slug"] not in community_slugs]
    posts.sort(key=lambda p: str(p.get("date_published") or ""), reverse=True)

    post_cards = ""
    for p in posts[:12]:
        safe_path = html.escape(p["path"], quote=True)
        safe_title = html.escape(_clean_title(p.get("title") or ""))
        safe_desc = html.escape(p.get("description") or "")
        date_text = _fmt_date(p.get("date_published"))
        post_cards += f"""
          <a href="{safe_path}" class="block rounded-2xl border border-gray-100 bg-white p-6 hover:shadow-md transition-shadow">
            {f'<p class="text-xs text-gray-500 mb-2">{html.escape(date_text)}</p>' if date_text else ''}
            <h3 class="font-semibold text-cvc-charcoal mb-2">{safe_title}</h3>
            {f'<p class="text-gray-600 text-sm leading-relaxed">{safe_desc}</p>' if safe_desc else ''}
          </a>
"""

    # Schema: Physician + ProfilePage
    schema_obj = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "ProfilePage",
                "@id": f"{ORIGIN}/author/dr-mital-patel/",
                "url": f"{ORIGIN}/author/dr-mital-patel/",
                "name": f"{a['name']} — Author at Classic Vision Care",
                "mainEntity": {"@id": a["schema_id"]},
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "inLanguage": "en-US",
            },
            {
                "@type": "Physician",
                "@id": a["schema_id"],
                "name": a["name"],
                "url": f"{ORIGIN}/author/dr-mital-patel/",
                "image": f"{ORIGIN}{a['image']}",
                "jobTitle": a["title"],
                "description": a["bio"],
                "sameAs": a.get("sameAs", []),
                "medicalSpecialty": "Optometry",
                "knowsAbout": a["credentials"]["specialties"],
                "alumniOf": {
                    "@type": "EducationalOrganization",
                    "name": a["credentials"]["school"],
                },
                "worksFor": {
                    "@type": "Organization",
                    "@id": f"{ORIGIN}/#organization",
                    "name": "Classic Vision Care",
                    "url": f"{ORIGIN}/",
                },
            },
        ],
    }
    schema_json = json.dumps(schema_obj, ensure_ascii=False).replace("</", "<\\/")

    # Build credentials HTML
    creds = a.get("credentials", {})
    cert_items = ""
    for cert in creds.get("certifications", []):
        cert_items += f'<li class="text-gray-600 text-sm">{html.escape(cert)}</li>\n'
    spec_items = ""
    for spec in creds.get("specialties", []):
        spec_items += f'<li class="text-gray-600 text-sm">{html.escape(spec)}</li>\n'

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(a['name'])} — Author | Classic Vision Care</title>
  <meta name="description" content="{html.escape(a['bio'], quote=True)}">
  <link rel="canonical" href="{ORIGIN}/author/dr-mital-patel/">
  <meta property="og:title" content="{html.escape(a['name'])} — Author | Classic Vision Care">
  <meta property="og:description" content="{html.escape(a['bio'], quote=True)}">
  <meta property="og:url" content="{ORIGIN}/author/dr-mital-patel/">
  <meta property="og:image" content="{ORIGIN}{a['image']}">
  <meta property="og:site_name" content="Classic Vision Care">
  <meta property="og:locale" content="en_US">
  <meta property="og:type" content="profile">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/styles/tailwind.css">
  <link rel="stylesheet" href="/styles/editorial-forest.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="/fonts/TT_Norms_Pro_Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/TT_Norms_Pro_Bold.woff2" as="font" type="font/woff2" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet"></noscript>
  <script type="application/ld+json">{schema_json}</script>
</head>
<body class="cvc-editorial font-body text-cvc-charcoal bg-white">
  <!-- Skip Link for Accessibility -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

{header}

<main id="main-content">
  <section class="py-16 lg:py-24 bg-gradient-to-br from-cvc-teal-50 to-cvc-cream">
    <div class="max-w-4xl mx-auto px-6">
      <nav class="text-sm text-gray-600 mb-6" aria-label="Breadcrumb">
        <ol class="flex flex-wrap gap-2">
          <li><a href="/" class="hover:underline">Home</a></li>
          <li aria-hidden="true">/</li>
          <li><a href="/blog/" class="hover:underline">Resources</a></li>
          <li aria-hidden="true">/</li>
          <li class="text-cvc-charcoal">{html.escape(a['name'])}</li>
        </ol>
      </nav>
      <div class="flex flex-col md:flex-row items-start gap-8">
        <img src="{a['image']}" alt="{html.escape(a['image_alt'], quote=True)}"
             class="w-32 h-32 rounded-2xl object-cover shadow-md" width="128" height="128">
        <div>
          <h1 class="font-display text-3xl md:text-4xl text-cvc-charcoal leading-tight mb-2">{html.escape(a['name'])}</h1>
          <p class="text-cvc-teal-500 font-medium mb-4">{html.escape(a['role'])}</p>
          <p class="text-gray-600 leading-relaxed max-w-2xl mb-4">{html.escape(a['bio'])}</p>
          <a href="{a.get('doctor_page', '/dr-mital-patel-od/')}" class="text-cvc-teal-600 font-medium hover:underline text-sm">View full doctor profile &rarr;</a>
        </div>
      </div>
    </div>
  </section>

  <section class="py-12 bg-white">
    <div class="max-w-4xl mx-auto px-6">
      <div class="grid sm:grid-cols-3 gap-6">
        <div class="bg-cvc-cream rounded-2xl p-6">
          <h3 class="font-semibold text-cvc-charcoal mb-3 text-sm uppercase tracking-wider">Education</h3>
          <p class="text-gray-600 text-sm">{html.escape(creds.get('degree', 'OD'))}, {html.escape(creds.get('school', ''))}</p>
        </div>
        <div class="bg-cvc-cream rounded-2xl p-6">
          <h3 class="font-semibold text-cvc-charcoal mb-3 text-sm uppercase tracking-wider">Certifications</h3>
          <ul class="space-y-1">
{cert_items}          </ul>
        </div>
        <div class="bg-cvc-cream rounded-2xl p-6">
          <h3 class="font-semibold text-cvc-charcoal mb-3 text-sm uppercase tracking-wider">Specialties</h3>
          <ul class="space-y-1">
{spec_items}          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="py-16 lg:py-20 bg-white">
    <div class="max-w-4xl mx-auto px-6">
      <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-8">
        <h2 class="font-display text-2xl md:text-3xl text-cvc-charcoal">Articles by {html.escape(a['short_name'])}</h2>
        <a href="/blog/" class="text-cvc-teal-600 font-medium hover:underline text-sm">View all articles &rarr;</a>
      </div>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{post_cards}
      </div>
    </div>
  </section>

  <section class="py-16 bg-cvc-cream">
    <div class="max-w-4xl mx-auto px-6 text-center">
      <h2 class="font-display text-2xl md:text-3xl text-cvc-charcoal mb-4">Want a personalized plan?</h2>
      <p class="text-gray-600 mb-6 max-w-2xl mx-auto">Dr. Patel takes time to listen, explain, and recommend options that fit your goals. Book an appointment at the location closest to you.</p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <a href="/book-now/" class="btn-primary">Book an appointment</a>
        <a href="/eye-doctor-kennesaw-ga/" class="btn-secondary">Kennesaw</a>
        <a href="/eye-doctor-marietta/" class="btn-secondary">East Cobb</a>
      </div>
    </div>
  </section>
</main>

{footer}
</body>
</html>
"""

    dest = BASE_DIR / "author" / "dr-mital-patel" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page_html, encoding="utf-8")
    print(f"  [OK] Generated {dest.relative_to(BASE_DIR)}")


# ---------------------------------------------------------------------------
# Dr. Mital Patel page enhancement
# ---------------------------------------------------------------------------

def enhance_dr_mital_page(
    authors: dict[str, Any],
    manifest: list[dict[str, Any]],
    community_slugs: set[str],
) -> None:
    a = authors["dr-mital-patel"]
    page_path = BASE_DIR / "dr-mital-patel-od" / "index.html"
    if not page_path.exists():
        print(f"  [MISS] {page_path.relative_to(BASE_DIR)}")
        return

    text = page_path.read_text(encoding="utf-8")

    # Collect medical posts for her articles section
    posts = [p for p in manifest if p["slug"] not in community_slugs]
    posts.sort(key=lambda p: str(p.get("date_published") or ""), reverse=True)

    # ---- 1. Update Physician schema (replace if present, add if not) ----
    schema_obj = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Physician",
                "@id": a["schema_id"],
                "name": a["name"],
                "url": f"{ORIGIN}{a['author_page']}",
                "image": f"{ORIGIN}{a['image']}",
                "jobTitle": a["title"],
                "description": a["bio"],
                "sameAs": a.get("sameAs", []),
                "medicalSpecialty": "Optometry",
                "knowsAbout": a["credentials"]["specialties"],
                "alumniOf": {
                    "@type": "EducationalOrganization",
                    "name": a["credentials"]["school"],
                },
                "worksFor": {
                    "@type": "Organization",
                    "@id": f"{ORIGIN}/#organization",
                    "name": "Classic Vision Care",
                    "url": f"{ORIGIN}/",
                },
            },
            {
                "@type": "ProfilePage",
                "@id": f"{ORIGIN}/dr-mital-patel-od/",
                "url": f"{ORIGIN}/dr-mital-patel-od/",
                "name": f"{a['name']} — Eye Doctor at Classic Vision Care",
                "mainEntity": {"@id": a["schema_id"]},
                "isPartOf": {"@id": f"{ORIGIN}/#website"},
                "inLanguage": "en-US",
            },
        ],
    }
    schema_json = json.dumps(schema_obj, ensure_ascii=False).replace("</", "<\\/")
    schema_tag = f'  <script type="application/ld+json">{schema_json}</script>\n'

    # Remove existing JSON-LD, then insert fresh
    text = JSONLD_RE.sub("", text)
    text = text.replace("</head>", f"{schema_tag}</head>")

    # ---- 2. Add articles section if not present ----
    if "Articles by Dr." not in text:
        # Build post cards (show latest 8)
        shown = posts[:8]
        cards_html = ""
        for p in shown:
            safe_path = html.escape(p["path"], quote=True)
            safe_title = html.escape(_clean_title(p.get("title") or ""))
            safe_desc = html.escape(p.get("description") or "")
            date_text = _fmt_date(p.get("date_published"))
            cards_html += f"""
            <a href="{safe_path}" class="block rounded-2xl border border-gray-100 bg-white p-6 hover:shadow-md transition-shadow">
              {f'<p class="text-xs text-gray-500 mb-2">{html.escape(date_text)}</p>' if date_text else ''}
              <h3 class="font-semibold text-cvc-charcoal mb-2">{safe_title}</h3>
              {f'<p class="text-gray-600 text-sm leading-relaxed line-clamp-2">{safe_desc}</p>' if safe_desc else ''}
            </a>
"""

        articles_section = f"""
  <!-- Articles by Dr. Mital Patel -->
  <section class="py-16 lg:py-20 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-10">
        <div>
          <h2 class="font-display text-3xl md:text-4xl text-cvc-charcoal mb-2">Articles by Dr. Mital Patel</h2>
          <p class="text-gray-600 max-w-2xl">Eye care insights and clinical guidance from Dr. Patel.</p>
        </div>
        <a href="/blog/" class="text-cvc-teal-600 font-medium hover:underline">View all articles &rarr;</a>
      </div>
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
{cards_html}
      </div>
    </div>
  </section>
"""
        # Insert before the CTA section (look for the teal bg CTA)
        cta_pattern = re.compile(
            r'(\s*<section[^>]*class="[^"]*bg-cvc-teal-500[^"]*"[^>]*>)',
            re.DOTALL,
        )
        m = cta_pattern.search(text)
        if m:
            text = text[: m.start()] + articles_section + text[m.start() :]
        else:
            # Fallback: insert before </main>
            text = text.replace("</main>", f"{articles_section}\n</main>")

    page_path.write_text(text, encoding="utf-8")
    print(f"  [OK] Enhanced {page_path.relative_to(BASE_DIR)}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=== E-E-A-T Authorship Migration ===\n")

    authors, community_slugs = load_authors()
    manifest = load_manifest()
    header, footer = read_layout_blocks()

    print(f"Loaded {len(manifest)} posts from manifest")
    print(f"Community slugs: {len(community_slugs)}")
    print(f"Authors: {', '.join(authors.keys())}\n")

    # ---- Step 1: Migrate all article pages ----
    print("--- Migrating article pages ---")
    migrated = 0
    skipped = 0
    missing = 0

    for post in manifest:
        slug = post.get("slug", "")
        path = post.get("path", "")
        if not path:
            continue

        author_slug = assign_author(slug, community_slugs)
        file_path = BASE_DIR / path.strip("/") / "index.html"

        if migrate_article(file_path, post, author_slug, authors):
            migrated += 1
            print(f"  [OK] {path} → {authors[author_slug]['short_name']}")
        elif file_path.exists():
            skipped += 1
        else:
            missing += 1

        # Update manifest entry
        post["author_slug"] = author_slug
        post["content_type"] = "community" if author_slug == "ankit-patel" else "medical"
        post["author"] = authors[author_slug]["name"]

    print(f"\nArticles: migrated={migrated}, unchanged={skipped}, missing={missing}\n")

    # ---- Step 2: Generate author pages ----
    print("--- Generating author pages ---")
    generate_ankit_author_page(authors, manifest, community_slugs, header, footer)
    generate_dr_mital_author_page(authors, manifest, community_slugs, header, footer)

    # ---- Step 3: Enhance Dr. Mital Patel's doctor page ----
    print("\n--- Enhancing Dr. Mital Patel doctor page ---")
    enhance_dr_mital_page(authors, manifest, community_slugs)

    # ---- Step 4: Write updated manifest ----
    manifest_path = BASE_DIR / "content" / "wp_blog_posts.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\n--- Updated {manifest_path.relative_to(BASE_DIR)} ---")

    print("\n=== Migration complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
