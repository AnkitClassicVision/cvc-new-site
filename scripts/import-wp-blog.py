#!/usr/bin/env python3
"""
Import WordPress blog posts into the static site.

Workflow:
1) Use the WP REST API to enumerate published posts + Yoast metadata.
2) For posts where `content.rendered` contains Divi shortcodes, scrape the
   rendered front-end HTML (because REST output is not usable).
3) Write each post to its existing permalink path (no redirects needed).
4) Optionally copy referenced `/wp-content/uploads/...` assets from a local
   export directory into `./wp-content/uploads/` so images keep working after
   cutover.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Authorship helpers
# ---------------------------------------------------------------------------

def _load_authors() -> tuple[dict[str, Any], set[str]]:
    path = BASE_DIR / "content" / "authors.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    community_slugs = set(data.pop("_community_slugs", []))
    return data, community_slugs


def _assign_author(slug: str, community_slugs: set[str]) -> str:
    return "ankit-patel" if slug in community_slugs else "dr-mital-patel"


def _clean_headline(raw: str) -> str:
    for sep in (" | ", " - Classic Vision Care"):
        if sep in raw:
            raw = raw.split(sep)[0]
    return raw.strip()


def _build_article_schema(
    canonical_url: str,
    meta: "PostMeta",
    author_slug: str,
    authors: dict[str, Any],
) -> str:
    origin = DEFAULT_ORIGIN
    author = authors[author_slug]
    is_medical = author_slug == "dr-mital-patel"
    headline = _clean_headline(meta.title)

    graph: list[dict[str, Any]] = []

    article: dict[str, Any] = {
        "@type": "MedicalWebPage" if is_medical else ["Article", "BlogPosting"],
        "@id": f"{canonical_url}#article",
        "headline": headline,
        "author": {"@id": author["schema_id"]},
        "publisher": {"@id": f"{origin}/#organization"},
        "mainEntityOfPage": {"@id": canonical_url},
        "inLanguage": "en-US",
    }
    if meta.date_published:
        article["datePublished"] = meta.date_published
    if meta.date_modified:
        article["dateModified"] = meta.date_modified
    if meta.description:
        article["description"] = meta.description
    if meta.featured_image:
        img = meta.featured_image
        article["image"] = img if img.startswith("http") else f"{origin}{img}"
    graph.append(article)

    webpage: dict[str, Any] = {
        "@type": "WebPage",
        "@id": canonical_url,
        "url": canonical_url,
        "name": meta.title,
        "isPartOf": {"@id": f"{origin}/#website"},
        "author": {"@id": author["schema_id"]},
        "breadcrumb": {"@id": f"{canonical_url}#breadcrumb"},
        "inLanguage": "en-US",
    }
    if meta.date_published:
        webpage["datePublished"] = meta.date_published
    if meta.date_modified:
        webpage["dateModified"] = meta.date_modified
    if meta.description:
        webpage["description"] = meta.description
    graph.append(webpage)

    author_node: dict[str, Any] = {
        "@type": author["schema_type"],
        "@id": author["schema_id"],
        "name": author["name"],
        "url": f"{origin}{author['author_page']}",
        "image": f"{origin}{author['image']}",
        "jobTitle": author["title"],
        "sameAs": author.get("sameAs", []),
        "worksFor": {"@id": f"{origin}/#organization"},
    }
    graph.append(author_node)

    graph.append({
        "@type": "BreadcrumbList",
        "@id": f"{canonical_url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{origin}/"},
            {"@type": "ListItem", "position": 2, "name": "Resources", "item": f"{origin}/blog/"},
            {"@type": "ListItem", "position": 3, "name": headline},
        ],
    })

    graph.append({
        "@type": "Organization",
        "@id": f"{origin}/#organization",
        "name": "Classic Vision Care",
        "url": f"{origin}/",
        "logo": f"{origin}/images/logos/EOP1600_Classic_Logo_FN.png",
    })

    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def _build_rich_byline(meta: "PostMeta", author_slug: str, authors: dict[str, Any]) -> str:
    author = authors[author_slug]
    date_text = ""
    if meta.date_published:
        try:
            parsed = dt.datetime.fromisoformat(meta.date_published.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=dt.timezone.utc)
            parsed = parsed.astimezone(dt.timezone.utc)
            date_text = f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}"
        except Exception:
            pass

    safe_name = html.escape(author["name"])
    safe_img = html.escape(author["image"], quote=True)
    safe_alt = html.escape(author["image_alt"], quote=True)
    safe_page = html.escape(author["author_page"], quote=True)
    date_line = f'<p class="text-xs text-gray-500">{html.escape(date_text)}</p>' if date_text else ""

    return (
        f'<div class="mt-4 flex items-center gap-3">\n'
        f'        <img src="{safe_img}" alt="{safe_alt}" '
        f'class="w-10 h-10 rounded-full object-cover" width="40" height="40" loading="lazy">\n'
        f'        <div>\n'
        f'          <p class="text-sm font-medium text-cvc-charcoal">'
        f'<a href="{safe_page}" class="hover:underline">{safe_name}</a></p>\n'
        f'          {date_line}\n'
        f'        </div>\n'
        f'      </div>'
    )


def _build_medical_review_footer(authors: dict[str, Any]) -> str:
    a = authors["dr-mital-patel"]
    return (
        f'<div class="mt-8 flex items-center gap-3 border-t border-gray-100 pt-6">\n'
        f'        <img src="{a["image"]}" alt="{html.escape(a["image_alt"], quote=True)}" '
        f'class="w-12 h-12 rounded-full object-cover" width="48" height="48" loading="lazy">\n'
        f'        <div>\n'
        f'          <p class="text-sm text-gray-500">Medically reviewed by</p>\n'
        f'          <p class="text-sm font-medium text-cvc-charcoal">'
        f'<a href="{a["author_page"]}" class="hover:underline">{html.escape(a["name"])}</a>'
        f' &middot; Optometrist</p>\n'
        f'        </div>\n'
        f'      </div>'
    )

DEFAULT_ORIGIN = "https://classicvisioncare.com"

DIVI_SHORTCODE_RE = re.compile(r"\[(?:/?et_pb|et_pb_section|et_pb_row|et_pb_text)\b", re.IGNORECASE)

DEFAULT_EXTRA_ORIGIN_HOSTS = {
    "classicvisioncare.com",
    "www.classicvisioncare.com",
    # Observed on older/staging content links.
    "classicvisioncare.us23.cdn-alpha.com",
}


@dataclass(frozen=True)
class PostMeta:
    id: int
    slug: str
    url: str
    path: str
    title: str
    description: str | None
    date_published: str | None
    date_modified: str | None
    author: str | None
    featured_image: str | None
    featured_image_alt: str | None


def normalize_slash_path(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path


def dest_for_path(path: str) -> Path:
    path = normalize_slash_path(path)
    return BASE_DIR / path.strip("/") / "index.html"


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


def wp_api_get(session: requests.Session, url: str, *, params: dict[str, Any]) -> requests.Response:
    resp = session.get(
        url,
        params=params,
        timeout=60,
        headers={
            "User-Agent": "cvc-static-blog-import/1.0",
            "Accept": "application/json",
        },
    )
    resp.raise_for_status()
    return resp


def fetch_posts(origin: str) -> list[dict[str, Any]]:
    api_url = f"{origin.rstrip('/')}/wp-json/wp/v2/posts"
    session = requests.Session()

    posts: list[dict[str, Any]] = []
    page = 1
    per_page = 100
    total_pages = None

    while True:
        resp = wp_api_get(
            session,
            api_url,
            params={
                "per_page": per_page,
                "page": page,
                "_embed": 1,
                "orderby": "date",
                "order": "desc",
            },
        )
        batch = resp.json()
        if not isinstance(batch, list):
            raise RuntimeError(f"Unexpected WP API response (page {page})")
        posts.extend(batch)

        if total_pages is None:
            try:
                total_pages = int(resp.headers.get("X-WP-TotalPages", "1"))
            except ValueError:
                total_pages = 1

        if page >= (total_pages or 1):
            break
        page += 1

    return posts


def to_root_relative(url: str, origin_hosts: set[str]) -> str | None:
    url = url.strip()
    if not url:
        return None

    lower = url.lower()
    if lower.startswith(("mailto:", "tel:", "javascript:", "data:", "#")):
        return None

    # Protocol-relative URLs.
    if url.startswith("//"):
        parsed = urlparse("https:" + url)
    else:
        parsed = urlparse(url)

    if parsed.scheme in ("http", "https"):
        if parsed.netloc and parsed.netloc.lower() not in origin_hosts:
            return None
        path = parsed.path or "/"
        rebuilt = urlunparse(("", "", path, "", parsed.query, parsed.fragment))
        return rebuilt if rebuilt.startswith("/") else "/" + rebuilt

    return None


def rewrite_fragment_urls(html_fragment: str, origin_hosts: set[str]) -> str:
    # Parse as fragment by wrapping in a root container.
    soup = BeautifulSoup(f"<div id=\"__cvc_root__\">{html_fragment}</div>", "lxml")
    root = soup.select_one("#__cvc_root__")
    if not root:
        return html_fragment

    attrs_to_rewrite = ("href", "src", "data-src", "data-lazy-src")
    for el in root.find_all(True):
        for attr in attrs_to_rewrite:
            if not el.has_attr(attr):
                continue
            value = str(el.get(attr))
            rewritten = to_root_relative(value, origin_hosts=origin_hosts)
            if rewritten:
                el[attr] = rewritten

        if el.has_attr("srcset"):
            srcset = str(el.get("srcset") or "")
            if not srcset.strip():
                continue
            parts_out: list[str] = []
            for part in [p.strip() for p in srcset.split(",") if p.strip()]:
                tokens = part.split()
                if not tokens:
                    continue
                url_token = tokens[0]
                rewritten = to_root_relative(url_token, origin_hosts=origin_hosts)
                if rewritten:
                    tokens[0] = rewritten
                parts_out.append(" ".join(tokens))
            el["srcset"] = ", ".join(parts_out)

    return root.decode_contents().strip()


def scrape_rendered_entry_content(url: str) -> str:
    resp = requests.get(url, timeout=60, headers={"User-Agent": "cvc-static-blog-import/1.0", "Accept": "text/html"})
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    entry = soup.select_one(".entry-content")
    article = soup.find("article")
    if not entry and article:
        entry = article
    if not entry:
        raise RuntimeError(f"Could not find entry content for {url}")

    divi_text_blocks = entry.select(".et_pb_text_inner")
    if divi_text_blocks:
        parts = []
        for block in divi_text_blocks:
            inner = block.decode_contents().strip()
            if inner:
                parts.append(inner)
        return "\n".join(parts).strip()

    return entry.decode_contents().strip()


def looks_like_divi_shortcodes(html_fragment: str) -> bool:
    return bool(DIVI_SHORTCODE_RE.search(html_fragment or ""))


def strip_html_tags(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    return soup.get_text(" ", strip=True)


def yoast_title(post: dict[str, Any]) -> str | None:
    y = post.get("yoast_head_json") or {}
    title = y.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return None


def yoast_description(post: dict[str, Any]) -> str | None:
    y = post.get("yoast_head_json") or {}
    desc = y.get("description")
    if isinstance(desc, str) and desc.strip():
        return desc.strip()
    return None


def yoast_schema(post: dict[str, Any]) -> dict[str, Any] | None:
    y = post.get("yoast_head_json") or {}
    schema = y.get("schema")
    return schema if isinstance(schema, dict) else None


def yoast_article_times(post: dict[str, Any]) -> tuple[str | None, str | None]:
    y = post.get("yoast_head_json") or {}
    published = y.get("article_published_time")
    modified = y.get("article_modified_time")
    return (
        published if isinstance(published, str) and published.strip() else None,
        modified if isinstance(modified, str) and modified.strip() else None,
    )


def get_author_name(post: dict[str, Any]) -> str | None:
    y = post.get("yoast_head_json") or {}
    author = y.get("author")
    if isinstance(author, str) and author.strip():
        return author.strip()

    embedded = post.get("_embedded") or {}
    authors = embedded.get("author") or []
    if isinstance(authors, list) and authors:
        name = authors[0].get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    return None


def get_featured_media(post: dict[str, Any]) -> tuple[str | None, str | None]:
    y = post.get("yoast_head_json") or {}
    og_images = y.get("og_image") or []
    if isinstance(og_images, list) and og_images:
        url = og_images[0].get("url")
        if isinstance(url, str) and url.strip():
            return url.strip(), None

    embedded = post.get("_embedded") or {}
    media = embedded.get("wp:featuredmedia") or []
    if isinstance(media, list) and media:
        item = media[0]
        source = item.get("source_url")
        alt = item.get("alt_text")
        return (
            source.strip() if isinstance(source, str) and source.strip() else None,
            alt.strip() if isinstance(alt, str) and alt.strip() else None,
        )
    return None, None


def build_post_meta(origin: str, post: dict[str, Any]) -> PostMeta:
    link = post.get("link")
    if not isinstance(link, str) or not link.strip():
        raise RuntimeError(f"Missing link for post id={post.get('id')}")

    parsed = urlparse(link)
    path = normalize_slash_path(parsed.path or "/")

    title = yoast_title(post) or strip_html_tags(post.get("title", {}).get("rendered", "")) or path
    description = yoast_description(post)
    published, modified = yoast_article_times(post)

    featured, featured_alt = get_featured_media(post)

    return PostMeta(
        id=int(post.get("id") or 0),
        slug=str(post.get("slug") or ""),
        url=link.strip(),
        path=path,
        title=title,
        description=description,
        date_published=published or (post.get("date") if isinstance(post.get("date"), str) else None),
        date_modified=modified or (post.get("modified") if isinstance(post.get("modified"), str) else None),
        author=get_author_name(post),
        featured_image=featured,
        featured_image_alt=featured_alt,
    )


def render_post_page(
    origin: str,
    meta: PostMeta,
    *,
    content_html: str,
    header: str,
    footer: str,
    author_slug: str,
    authors: dict[str, Any],
) -> str:
    canonical_url = f"{origin.rstrip('/')}{meta.path}"
    is_medical = author_slug == "dr-mital-patel"

    def build_faq_jsonld(faq_items: list[tuple[str, str]]) -> str:
        payload = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "@id": f"{canonical_url}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faq_items
            ],
        }
        return json.dumps(payload, ensure_ascii=False)

    schema_blocks: list[str] = []
    schema_blocks.append(_build_article_schema(canonical_url, meta, author_slug, authors))

    extra_section_blocks: list[str] = []

    # P0 requirement: add punctal plug "fell out" FAQ + FAQPage schema.
    if meta.path == "/dry-eyes/punctal-plugs-for-dry-eyes-guide/":
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
        schema_blocks.append(build_faq_jsonld(faq_items))

        extra_section_blocks.append(
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

    schema_block = ""
    if schema_blocks:
        lines = []
        for block in schema_blocks:
            block = block.replace("</", "<\\/")
            lines.append(f'  <script type="application/ld+json">{block}</script>')
        schema_block = "\n".join(lines) + "\n"

    byline_html = _build_rich_byline(meta, author_slug, authors)

    description = meta.description or ""
    safe_title = html.escape(meta.title)
    safe_description_attr = html.escape(description, quote=True)
    safe_description_text = html.escape(description)

    featured_block = ""
    if meta.featured_image:
        alt = meta.featured_image_alt or meta.title
        safe_alt = html.escape(alt, quote=True)
        safe_src = html.escape(meta.featured_image, quote=True)
        featured_block = f"""
      <figure class="mt-8">
        <img src="{safe_src}" alt="{safe_alt}" class="w-full rounded-2xl border border-gray-100 shadow-sm">
      </figure>
        """.rstrip()

    hero = f"""
  <section class="py-16 lg:py-20 bg-gradient-to-br from-cvc-teal-50 to-cvc-cream">
    <div class="max-w-4xl mx-auto px-6">
      <nav class="text-sm text-gray-600 mb-4" aria-label="Breadcrumb">
        <ol class="flex flex-wrap gap-2">
          <li><a href="/" class="hover:underline">Home</a></li>
          <li aria-hidden="true">/</li>
          <li><a href="/blog/" class="hover:underline">Resources</a></li>
        </ol>
      </nav>
      <h1 class="font-display text-3xl md:text-5xl text-cvc-charcoal leading-tight mb-4">{safe_title}</h1>
      {f'<p class="text-lg text-gray-600 max-w-2xl">{safe_description_text}</p>' if description else ''}
      {byline_html}
{featured_block}
      <div class="mt-8 flex flex-col sm:flex-row gap-3">
        <a href="/book-now/" class="btn-primary">Book an appointment</a>
        <a href="/dry-eye-treatment/" class="btn-secondary">Dry Eye Spa</a>
        <a href="/our-locations/" class="btn-secondary">Locations</a>
      </div>
    </div>
  </section>
    """.strip()

    disclaimer_block = ""
    if meta.path.startswith("/eye-treatment/"):
        disclaimer_block = """
      <div class="bg-cvc-cream rounded-xl p-6 mb-10 border border-cvc-teal-100">
        <p class="text-sm text-gray-700 leading-relaxed"><strong>Medical note:</strong> This page is for educational purposes and does not replace medical advice. If you have severe eye pain, sudden vision changes, new flashes/floaters, or symptoms after an injury, seek urgent care.</p>
      </div>
        """.strip()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  {f'<meta name="description" content="{safe_description_attr}">' if description else ''}
  <link rel="canonical" href="{canonical_url}">
  <link rel="stylesheet" href="/styles/tailwind.css">
  <link rel="stylesheet" href="/styles/editorial-forest.css?v=2">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="/fonts/TT_Norms_Pro_Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/TT_Norms_Pro_Bold.woff2" as="font" type="font/woff2" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
{schema_block}</head>
<body class="cvc-editorial font-body text-cvc-charcoal bg-white">
{header}

<main id="main-content">
{hero}
  <section class="py-14 lg:py-16 bg-white">
    <div class="max-w-3xl mx-auto px-6">
{disclaimer_block}
      <article class="space-y-6">
{content_html}
      </article>
{'' if not extra_section_blocks else ('\\n'.join(extra_section_blocks))}
{_build_medical_review_footer(authors) if is_medical else ''}
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


def collect_upload_paths_from_fragment(html_fragment: str) -> set[str]:
    soup = BeautifulSoup(f"<div id=\"__cvc_root__\">{html_fragment}</div>", "lxml")
    root = soup.select_one("#__cvc_root__")
    if not root:
        return set()

    uploads: set[str] = set()
    attrs = ("src", "href", "data-src", "data-lazy-src", "srcset")
    for el in root.find_all(True):
        for attr in attrs:
            if not el.has_attr(attr):
                continue
            value = str(el.get(attr) or "")
            if not value:
                continue
            if attr == "srcset":
                for part in [p.strip() for p in value.split(",") if p.strip()]:
                    url_token = part.split()[0]
                    if "/wp-content/uploads/" in url_token:
                        uploads.add(url_token.split("/wp-content/uploads/", 1)[1].split("?", 1)[0].split("#", 1)[0])
                continue
            if "/wp-content/uploads/" in value:
                uploads.add(value.split("/wp-content/uploads/", 1)[1].split("?", 1)[0].split("#", 1)[0])
    return uploads


def copy_uploads(
    upload_relpaths: set[str],
    *,
    uploads_source: Path,
    uploads_dest: Path,
    download_missing: bool,
    origin: str,
) -> tuple[int, int]:
    copied = 0
    missing = 0

    uploads_dest.mkdir(parents=True, exist_ok=True)
    session = requests.Session()

    for rel in sorted(upload_relpaths):
        src = uploads_source / rel
        dest = uploads_dest / rel
        if dest.exists():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            shutil.copy2(src, dest)
            copied += 1
            continue

        if not download_missing:
            missing += 1
            continue

        url = f"{origin.rstrip('/')}/wp-content/uploads/{rel}"
        try:
            resp = session.get(url, timeout=60, headers={"User-Agent": "cvc-static-blog-import/1.0"})
            if resp.status_code != 200:
                missing += 1
                continue
            dest.write_bytes(resp.content)
            copied += 1
        except Exception:
            missing += 1

    return copied, missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", default=DEFAULT_ORIGIN, help="WordPress origin (default: classicvisioncare.com)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing generated blog pages.")
    parser.add_argument(
        "--uploads-source",
        default=str((BASE_DIR.parent / "wp_export" / "public_html" / "wp-content" / "uploads").resolve()),
        help="Local wp-content/uploads directory to copy from.",
    )
    parser.add_argument(
        "--copy-uploads",
        action="store_true",
        help="Copy referenced /wp-content/uploads assets into the static site.",
    )
    parser.add_argument(
        "--download-missing",
        action="store_true",
        help="If an upload asset is missing locally, download it from the WP origin.",
    )
    parser.add_argument(
        "--manifest-out",
        default=str((BASE_DIR / "content" / "wp_blog_posts.json").resolve()),
        help="Where to write a JSON manifest of imported posts.",
    )
    args = parser.parse_args()

    origin = args.origin.rstrip("/")
    origin_host = urlparse(origin).netloc.lower() or "classicvisioncare.com"
    origin_hosts = set(DEFAULT_EXTRA_ORIGIN_HOSTS) | {origin_host}

    header, footer = read_layout_blocks()
    authors, community_slugs = _load_authors()

    posts = fetch_posts(origin)
    print(f"Found {len(posts)} published posts via WP API")

    uploads_source = Path(args.uploads_source)
    uploads_dest = BASE_DIR / "wp-content" / "uploads"

    manifest: list[dict[str, Any]] = []

    written = 0
    skipped = 0
    upload_paths: set[str] = set()

    for post in posts:
        meta = build_post_meta(origin, post)

        rendered = post.get("content", {}).get("rendered", "")
        if not isinstance(rendered, str):
            rendered = ""

        if looks_like_divi_shortcodes(rendered):
            try:
                content_html = scrape_rendered_entry_content(meta.url)
            except Exception as exc:
                print(f"[WARN] scrape failed for {meta.url}: {exc}. Falling back to REST content.")
                content_html = rendered
        else:
            content_html = rendered

        content_html = rewrite_fragment_urls(content_html, origin_hosts=origin_hosts)
        # Content cleanup: fix a known corrupted token in the WP HTML export.
        content_html = content_html.replace(
            "rehttps://classicvisioncare.us23.cdn-alpha.com/blog/are-glasses-better-than-contacts/placement",
            "replacement",
        )

        # Featured image URL should be root-relative as well, for preview parity.
        if meta.featured_image:
            rewritten = to_root_relative(meta.featured_image, origin_hosts=origin_hosts)
            if rewritten:
                meta = PostMeta(**{**meta.__dict__, "featured_image": rewritten})

        upload_paths |= collect_upload_paths_from_fragment(content_html)
        if meta.featured_image and "/wp-content/uploads/" in meta.featured_image:
            upload_paths.add(meta.featured_image.split("/wp-content/uploads/", 1)[1].split("?", 1)[0].split("#", 1)[0])

        author_slug = _assign_author(meta.slug, community_slugs)

        dest = dest_for_path(meta.path)
        if dest.exists() and not args.overwrite:
            skipped += 1
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            page_html = render_post_page(
                origin,
                meta,
                content_html=content_html,
                header=header,
                footer=footer,
                author_slug=author_slug,
                authors=authors,
            )
            dest.write_text(page_html, encoding="utf-8")
            written += 1

        manifest.append(
            {
                "id": meta.id,
                "slug": meta.slug,
                "path": meta.path,
                "title": meta.title,
                "description": meta.description,
                "date_published": meta.date_published,
                "date_modified": meta.date_modified,
                "author": authors[author_slug]["name"],
                "author_slug": author_slug,
                "content_type": "community" if author_slug == "ankit-patel" else "medical",
                "featured_image": meta.featured_image,
            }
        )

    manifest_out = Path(args.manifest_out)
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    copied = missing = 0
    if args.copy_uploads:
        copied, missing = copy_uploads(
            upload_paths,
            uploads_source=uploads_source,
            uploads_dest=uploads_dest,
            download_missing=args.download_missing,
            origin=origin,
        )

    print(f"Pages written: {written}, skipped: {skipped}")
    print(f"Manifest: {manifest_out.relative_to(BASE_DIR)} ({len(manifest)} posts)")
    if args.copy_uploads:
        print(f"Uploads copied: {copied}, missing: {missing} (dest: {uploads_dest.relative_to(BASE_DIR)}/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
