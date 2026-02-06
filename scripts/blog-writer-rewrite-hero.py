#!/usr/bin/env python3
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PageInfo:
    new_path: str
    old_path: str
    page_type: str
    primary_keyword: str


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "content" / "page_manifest.json"


HERO_P_TAG_RE = re.compile(
    r"(?P<open><p[^>]*class=\"[^\"]*text-lg[^\"]*text-gray-600[^\"]*\"[^>]*>)"
    r"(?P<content>.*?)"
    r"(?P<close></p>)",
    flags=re.I | re.S,
)

VALUE_POINTS_RE = re.compile(
    r"^\s*<!--\s*Hero value points\s*-->\s*<ul[^>]*>.*?</ul>\s*",
    flags=re.I | re.S,
)


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
                page_type=info.get("type", ""),
                primary_keyword=info.get("primary_keyword", ""),
            )
        )
    pages.sort(key=lambda p: p.new_path)
    return pages


def hero_value_points(page: PageInfo) -> list[str]:
    p = page.new_path
    t = page.page_type.lower()

    if p == "index.html":
        return [
            "Two convenient locations in Kennesaw and East Cobb/Marietta",
            "Thorough exams with clear explanations",
            "Free glasses repairs and adjustments (even if you did not buy them here)",
        ]

    if "/locations/" in p or t == "location":
        return [
            "Easy booking for this location",
            "Friendly team and a relaxed pace",
            "Help choosing the right appointment type",
        ]

    if "/dry-eye/" in p:
        return [
            "Find the root cause of your symptoms",
            "Advanced options like MiBoFlo, IPL, BlephEx, and more",
            "A clear plan that fits your day",
        ]

    if "/myopia/" in p:
        return [
            "Myopia management options for real family routines",
            "Clear milestones and follow-ups you can track",
            "Support for kids, teens, and parents",
        ]

    if "/services/pediatric/" in p:
        return [
            "A calm, kid-friendly exam experience",
            "Answers for school, screens, and sports",
            "Next steps explained in plain language",
        ]

    if "/services/exams/" in p:
        return [
            "Modern testing with a focus on eye health",
            "Time to ask questions and understand results",
            "Clear next steps, not guesswork",
        ]

    if "/services/conditions/" in p:
        return [
            "Understand symptoms and when to schedule",
            "Early detection and careful monitoring when needed",
            "A plan tailored to your eyes and health history",
        ]

    if "/eyewear/" in p and "/specialty/" in p:
        return [
            "Specialty lens options for hard-to-fit eyes",
            "Step-by-step training and follow-up support",
            "Comfort and vision refined over time",
        ]

    if "/eyewear/" in p:
        return [
            "Frame styling and fit help from experienced opticians",
            "Lens options matched to work and hobbies",
            "Free adjustments and repairs when you need them",
        ]

    if "/about/" in p:
        return [
            "Family-owned practice with 25+ years in the community",
            "4.7 stars with 756+ reviews",
            "Care that feels personal, not rushed",
        ]

    if "/patients/" in p:
        return [
            "Clear steps for booking and preparing",
            "Help understanding insurance and benefits",
            "Two locations to fit your schedule",
        ]

    if "/legal/" in p:
        return [
            "Plain-language policies you can skim",
            "How to reach us with questions",
            "Updated regularly as needed",
        ]

    return [
        "Clear next steps and a simple booking path",
        "Friendly support from our team",
        "Care built around your goals",
    ]


def hero_intro(page: PageInfo) -> str:
    kw_raw = (page.primary_keyword or "").strip()
    kw = keyword_phrase(kw_raw)
    mentions_atlanta = "atlanta" in (kw_raw or "").lower()
    p = page.new_path
    t = page.page_type.lower()

    if t == "bio":
        if "mital-patel" in p:
            return (
                "Meet Dr. Mital Patel, OD. She focuses on thorough eye care and clear explanations, with a calm approach that helps patients feel comfortable asking questions."
            )
        if "bhumi-patel" in p:
            return (
                "Meet Dr. Bhumi Patel, OD. She provides thoughtful, detail-oriented care and takes time to explain what she sees and what it means for your daily life."
            )
        return "Meet your doctor at Classic Vision Care. Expect a thorough visit and clear, plain-language next steps."

    if t == "careers":
        return (
            "Interested in joining a friendly, patient-first eye care team? This page shares current openings, what we value, and how to apply at Classic Vision Care."
        )

    if t == "blog hub":
        return (
            "Looking for practical eye care tips you can actually use? Browse our blog for clear answers about exams, eyewear, dry eye, myopia, and more."
        )

    if p.endswith("/patients/book.html"):
        return (
            "Ready to book an appointment? Choose your preferred location below to schedule online or call our team and we will help you pick the right appointment type."
        )

    if p.endswith("/patients/contact.html"):
        return (
            "Need to contact Classic Vision Care? Use the options on this page to call, request an appointment, or send us a message. We are here to help."
        )

    if p.endswith("/patients/insurance.html"):
        return (
            "Questions about eye care insurance and payment options? We can verify benefits, explain what is covered, and help you plan for exams, contacts, and eyewear."
        )

    if p.endswith("/patients/new.html"):
        return (
            "New to Classic Vision Care? This page walks you through what to bring, how to prepare, and what to expect at your first visit at either location."
        )

    if p == "pages/about/index.html":
        return (
            "Get to know Classic Vision Care. We are a family-owned practice serving Kennesaw and East Cobb/Marietta with thorough exams, friendly service, and clear explanations."
        )

    if p == "pages/about/why-choose-us.html":
        return (
            "Choosing an eye doctor is personal. Here is what patients mention most about Classic Vision Care and what you can expect during your visit."
        )

    if p == "pages/about/testimonials.html":
        return (
            "See what patients say about their experience at Classic Vision Care, from thorough exams to friendly service and quick help with glasses adjustments."
        )

    if p == "pages/about/community.html":
        return (
            "We are proud to serve the communities around Kennesaw and East Cobb/Marietta. This page highlights the local partners, events, and programs we support."
        )

    if p == "pages/about/doctors/index.html":
        return "Meet the Classic Vision Care team. We take time to listen, explain results clearly, and help you feel confident about the next step."

    # Keep the exact keyword phrase early when it reads naturally.
    if p == "index.html":
        return (
            "If you are looking for an eye doctor in Kennesaw, GA, you are in the right place. "
            "Classic Vision Care also serves East Cobb and Marietta with thorough exams, a warm team, and clear explanations."
        )

    if "/locations/" in p or t == "location":
        return (
            f"Looking for {kw}? Visit Classic Vision Care for attentive eye care, clear answers, and easy scheduling. "
            "Choose the location that fits your day and book online or call our team."
        )

    if "/dry-eye/" in p:
        metro = " Serving the metro Atlanta area from Kennesaw and East Cobb/Marietta." if mentions_atlanta else ""
        return (
            f"Need {kw}? Our Dry Eye Spa helps you get to the cause of your symptoms and build a plan that lasts. "
            "We take time to explain your options and recommend what fits your eyes and your routine."
            f"{metro}"
        )

    if "/myopia/" in p:
        return (
            f"Looking for {kw}? We help families protect long-term eye health with proven myopia management options. "
            "You will leave with a clear plan, follow-ups that make sense, and support along the way."
        )

    if "/services/pediatric/" in p:
        return (
            f"Looking for {kw}? Our team makes pediatric visits comfortable and easy for kids and parents. "
            "We explain what we find in plain language and share practical next steps."
        )

    if "/services/exams/" in p:
        return (
            f"If you need {kw}, our doctors are here to help you see clearly and protect your eye health. "
            "Expect a thorough visit, time for questions, and a plan you understand."
        )

    if "/services/conditions/" in p:
        return (
            f"Concerned about {kw}? We help you understand symptoms, risk factors, and the right timing for care. "
            "Our goal is clear answers and a plan that protects your vision."
        )

    if "/eyewear/" in p and "/specialty/" in p:
        metro = " We serve metro Atlanta from our Kennesaw and East Cobb/Marietta locations." if mentions_atlanta else ""
        return (
            f"Searching for {kw}? Specialty contact lenses can be life-changing for comfort and clarity in hard-to-fit eyes. "
            "We guide you through fitting, training, and follow-ups so the lenses feel right in real life."
            f"{metro}"
        )

    if "/eyewear/" in p:
        return (
            f"Need {kw}? Our optical team helps you choose frames and lenses that match your lifestyle and budget. "
            "You will get honest guidance and support after you pick up your glasses."
        )

    if "/about/" in p:
        return (
            "Want to learn more about Classic Vision Care? We are a family-owned practice known for thorough care, friendly service, and clear explanations."
        )

    if "/patients/" in p:
        return (
            f"Need {kw}? Here is what to expect, how to prepare, and how to take the next step with Classic Vision Care. "
            "If you prefer, call and our team will help you choose the right appointment."
        )

    if "/legal/" in p:
        return "These policies explain how we handle information and how to reach us with questions. We aim to keep this page clear and easy to skim."

    return f"Looking for {kw}? Classic Vision Care is here to help with clear answers and an easy next step."


def keyword_phrase(keyword: str) -> str:
    kw = (keyword or "").strip()
    if not kw or kw == "-":
        return "this"

    normalized = kw.lower()
    suffixes: list[tuple[str, str]] = [
        ("kennesaw ga", "Kennesaw, GA"),
        ("east cobb marietta", "East Cobb and Marietta"),
        ("east cobb", "East Cobb"),
        ("marietta", "Marietta"),
        ("kennesaw", "Kennesaw"),
        ("atlanta", "Atlanta"),
        ("georgia", "Georgia"),
    ]

    for suffix, location in suffixes:
        if normalized.endswith(suffix):
            base = kw[: -len(suffix)].strip()
            if not base:
                return f"in {location}"
            return f"{base} in {location}"

    return kw


def build_value_points_html(points: list[str]) -> str:
    items = []
    for p in points[:3]:
        items.append(
            "\n".join(
                [
                    '              <li class="flex items-start gap-3">',
                    '                <svg class="w-5 h-5 text-cvc-teal-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">',
                    '                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>',
                    "                </svg>",
                    f'                <span class="text-gray-600 text-sm leading-relaxed">{p}</span>',
                    "              </li>",
                ]
            )
        )
    return "\n".join(
        [
            "            <!-- Hero value points -->",
            '            <ul class="space-y-3 mb-8 inline-block text-left">',
            "\n".join(items),
            "            </ul>",
        ]
    )


def rewrite_hero(html: str, page: PageInfo) -> str:
    # Replace only the first qualifying hero paragraph.
    main_idx = html.lower().find("<main")
    haystack = html[main_idx:] if main_idx != -1 else html
    m = HERO_P_TAG_RE.search(haystack)
    if not m:
        return html

    open_tag = m.group("open")
    close_tag = m.group("close")

    # Reduce spacing if paragraph has mb-8 and we are inserting a list below it.
    open_tag = re.sub(r"\bmb-8\b", "mb-4", open_tag)
    if "mb-" not in open_tag:
        open_tag = open_tag.replace("text-gray-600", "text-gray-600 mb-4", 1)

    new_p = hero_intro(page)
    vp = hero_value_points(page)
    vp_html = build_value_points_html(vp)

    p_tag = f"{open_tag}{new_p}{close_tag}"

    offset = main_idx if main_idx != -1 else 0
    start = offset + m.start()
    end = offset + m.end()
    tail = html[end:]

    existing = VALUE_POINTS_RE.match(tail)
    if existing:
        tail = tail[existing.end() :]

    insertion = f"\n\n{vp_html}\n"
    return html[:start] + p_tag + insertion + tail


def main() -> int:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Missing manifest: {MANIFEST_PATH}")

    pages = load_pages()
    updated = 0
    for page in pages:
        path = ROOT / page.new_path
        html = read_text(path)
        new_html = rewrite_hero(html, page)
        if new_html != html:
            write_text(path, new_html)
            updated += 1

    print(f"Updated hero copy on {updated} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
