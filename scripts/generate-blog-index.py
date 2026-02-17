#!/usr/bin/env python3
"""
Generate /blog/ index page that links to top resources (so /blog/ is not a
"coming soon" placeholder once key articles are migrated).
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = BASE_DIR / "content" / "wp_blog_posts.json"


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


def card(href: str, eyebrow: str, title: str, desc: str) -> str:
    return f"""
          <a href=\"{href}\" class=\"bg-cvc-cream rounded-2xl p-7 card-lift reveal\">
            <p class=\"text-xs uppercase tracking-widest text-gray-500 mb-2\">{html.escape(eyebrow)}</p>
            <h3 class=\"font-semibold text-cvc-charcoal mb-2\">{html.escape(title)}</h3>
            <p class=\"text-gray-600 text-sm leading-relaxed\">{html.escape(desc)}</p>
          </a>
    """.strip()


def load_wp_posts() -> list[dict]:
    if not MANIFEST_PATH.exists():
        return []
    try:
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data if isinstance(data, list) else []


def fmt_date(date_str: str | None) -> str | None:
    if not date_str:
        return None
    try:
        parsed = dt.datetime.fromisoformat(str(date_str).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        parsed = parsed.astimezone(dt.timezone.utc)
        return f"{parsed.strftime('%b')} {parsed.day}, {parsed.year}"
    except Exception:
        return None


def post_row(post: dict) -> str:
    path = str(post.get("path") or "").strip()
    title = str(post.get("title") or "").strip() or path
    desc = str(post.get("description") or "").strip()
    date_text = fmt_date(post.get("date_published"))
    author = str(post.get("author") or "").strip()

    safe_title = html.escape(title)
    safe_desc = html.escape(desc)
    safe_path = html.escape(path, quote=True)
    safe_meta = html.escape(date_text or "")
    safe_author = html.escape(author)

    meta_parts = []
    if date_text:
        meta_parts.append(safe_meta)
    if author:
        meta_parts.append(safe_author)
    meta_line = " &middot; ".join(meta_parts)

    return f"""
          <a href=\"{safe_path}\" class=\"block rounded-2xl border border-gray-100 bg-white p-6 hover:shadow-md transition-shadow\">
            {f'<p class=\"text-xs text-gray-500 mb-2\">{meta_line}</p>' if meta_line else ''}
            <h3 class=\"font-semibold text-cvc-charcoal mb-2\">{safe_title}</h3>
            {f'<p class=\"text-gray-600 text-sm leading-relaxed\">{safe_desc}</p>' if desc else ''}
          </a>
    """.strip()


def main() -> int:
    header, footer = read_layout_blocks()

    title = "Resources & Blog | Classic Vision Care"
    description = "Practical eye care answers and local guides from Classic Vision Care in Kennesaw and East Cobb/Marietta, GA."

    featured_cards = "\n".join(
        [
            card(
                "/ocular-rosacea/all-about-ocular-rosacea/",
                "Dry Eye • Ocular Rosacea",
                "Ocular Rosacea: symptoms, causes, treatment",
                "Understand triggers, what it feels like, and how we treat it as part of your dry eye plan.",
            ),
            card(
                "/dry-eyes/punctal-plugs-for-dry-eyes-guide/",
                "Dry Eye • Treatment",
                "Punctal plugs for dry eyes (complete guide)",
                "Benefits, what to expect, and quick answers (including “did my plug fall out?”).",
            ),
            card(
                "/dry-eyes/what-is-mibo-thermoflo/",
                "Dry Eye • MiBoFlo",
                "MiBoFlo Thermoflo: what to know",
                "How thermal expression helps MGD and why it is a core part of our Dry Eye Spa.",
            ),
            card(
                "/dry-eyes/what-is-intense-pulsed-light-treatment/",
                "Dry Eye • IPL",
                "IPL treatment for dry eye: overview",
                "Learn what IPL does, who it helps, and how it fits into long-term dry eye care.",
            ),
            card(
                "/eye-treatment/dull-pain-behind-your-eyes-heres-why/",
                "Symptoms • Eye Pain",
                "Dull pain behind your eyes: here’s why",
                "Common causes, when to worry, and what to do next.",
            ),
            card(
                "/eye-care/is-squinting-bad-for-your-eyes/",
                "Eye Care • Vision Habits",
                "Is squinting bad for your eyes?",
                "Why you squint, what it means, and how to fix the root cause.",
            ),
        ]
    )

    local_cards = "\n".join(
        [
            card(
                "/blog/top-things-to-do-and-see-in-marietta/",
                "Local Guide",
                "Top things to do and see in Marietta",
                "Ideas for weekends, family days, and local favorites.",
            ),
            card(
                "/blog/top-things-to-do-and-see-in-kennesaw-ga/",
                "Local Guide",
                "Top things to do and see in Kennesaw",
                "Highlights around town and easy ways to enjoy the area.",
            ),
        ]
    )

    more_cards = "\n".join(
        [
            card(
                "/eye-care/are-you-ruining-your-eyes-with-too-much-screen-time/",
                "Digital Eye Strain",
                "Too much screen time?",
                "What’s normal, what’s not, and how to reduce strain.",
            ),
            card(
                "/computer-eye-strain/",
                "Symptoms",
                "Computer eye strain",
                "How we evaluate and treat screen-related discomfort.",
            ),
            card(
                "/blog/dont-let-fall-allergies-ruin-your-vision/",
                "Seasonal Allergies",
                "Fall allergies and your eyes",
                "How to spot allergy symptoms and get relief.",
            ),
            card(
                "/eye-care/7-tips-for-avoiding-eye-infections/",
                "Eye Care",
                "Avoiding eye infections",
                "Simple habits that reduce risk for kids and adults.",
            ),
            card(
                "/blog/investing-in-eyewear-before-the-years-end/",
                "Eyewear",
                "Investing in eyewear before year-end",
                "How to make the most of benefits and pick frames you love.",
            ),
            card(
                "/contact-lenses/contacts-vs-glasses-the-pros-and-cons/",
                "Contact Lenses",
                "Contacts vs. glasses",
                "A clear comparison for comfort, lifestyle, and budget.",
            ),
        ]
    )

    wp_posts = load_wp_posts()
    wp_posts_sorted = sorted(
        wp_posts,
        key=lambda p: str(p.get("date_published") or ""),
        reverse=True,
    )
    all_posts_block = ""
    if wp_posts_sorted:
        rows = "\n".join(post_row(p) for p in wp_posts_sorted)
        all_posts_block = f"""
  <section class="py-16 lg:py-20 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <div class="mb-10">
        <h2 class="font-display text-3xl md:text-4xl text-cvc-charcoal mb-2">All posts</h2>
        <p class="text-gray-600 max-w-3xl">Browse our full library of eye care tips, dry eye resources, and local guides.</p>
      </div>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{rows}
      </div>
    </div>
  </section>
        """.rstrip()

    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="stylesheet" href="/styles/tailwind.css">
  <link rel="stylesheet" href="/styles/editorial-forest.css?v=3">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" href="/fonts/TT_Norms_Pro_Regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/TT_Norms_Pro_Bold.woff2" as="font" type="font/woff2" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
</head>
<body class="cvc-editorial font-body text-cvc-charcoal bg-white">
{header}

<main id="main-content">
  <section class="py-20 lg:py-28 bg-gradient-to-br from-cvc-teal-50 to-cvc-cream">
    <div class="max-w-7xl mx-auto px-6 text-center">
      <h1 class="font-display text-4xl md:text-5xl lg:text-6xl text-cvc-charcoal leading-tight mb-6">Resources &amp; <span class="text-cvc-teal-500">Blog</span></h1>
      <p class="text-lg text-gray-600 mb-8 max-w-3xl mx-auto">Practical eye care answers from Classic Vision Care. Start with the topics patients ask about most, then explore local guides and seasonal tips.</p>
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <a href="/book-now/" class="btn-primary">Book an appointment</a>
        <a href="/dry-eye-treatment/" class="btn-secondary">Dry Eye Spa</a>
        <a href="/myopia-control/" class="btn-secondary">Myopia Control</a>
      </div>
      <p class="text-xs text-gray-500 mt-4 max-w-2xl mx-auto">Educational content only; it does not replace medical advice. If you have severe eye pain or sudden vision changes, seek urgent care.</p>
    </div>
  </section>

  <section class="py-16 lg:py-20 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-10">
        <div>
          <h2 class="font-display text-3xl md:text-4xl text-cvc-charcoal mb-2">Featured resources</h2>
          <p class="text-gray-600 max-w-2xl">High-impact pages that protect rankings and help patients take the next step.</p>
        </div>
        <a href="/our-locations/" class="text-cvc-teal-600 font-medium hover:underline">Find a location →</a>
      </div>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{featured_cards}
      </div>
    </div>
  </section>

  <section class="py-16 lg:py-20 bg-cvc-cream">
    <div class="max-w-7xl mx-auto px-6">
      <div class="text-center mb-10">
        <h2 class="font-display text-3xl md:text-4xl text-cvc-charcoal mb-2">Local guides</h2>
        <p class="text-gray-600 max-w-3xl mx-auto">Classic Vision Care is proud to serve Kennesaw and East Cobb/Marietta.</p>
      </div>
      <div class="grid md:grid-cols-2 gap-6">
{local_cards}
      </div>
    </div>
  </section>

  <section class="py-16 lg:py-20 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <div class="mb-10">
        <h2 class="font-display text-3xl md:text-4xl text-cvc-charcoal mb-2">More reading</h2>
        <p class="text-gray-600 max-w-2xl">Seasonal tips and deeper dives into eye health and eyewear.</p>
      </div>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{more_cards}
      </div>

      <div class="mt-14 bg-cvc-cream rounded-2xl p-8 text-center">
        <h3 class="font-display text-2xl text-cvc-charcoal mb-3">Want a personalized plan?</h3>
        <p class="text-gray-600 mb-6 max-w-2xl mx-auto">Our doctors take time to listen, explain, and recommend options that fit your goals. Book an appointment at the location closest to you.</p>
        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <a href="/book-now/" class="btn-primary">Book an appointment</a>
          <a href="/eye-doctor-kennesaw-ga/" class="btn-secondary">Kennesaw</a>
          <a href="/eye-doctor-marietta/" class="btn-secondary">East Cobb</a>
        </div>
      </div>
    </div>
  </section>

{all_posts_block}
</main>

{footer}
</body>
</html>
"""

    dest = BASE_DIR / "blog" / "index.html"
    dest.write_text(out, encoding="utf-8")
    print(f"Wrote {dest.relative_to(BASE_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
