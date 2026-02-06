#!/usr/bin/env python3
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class PageInfo:
    new_path: str
    old_path: str
    page_type: str
    primary_keyword: str


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "content" / "page_manifest.json"
OUT_DIR = ROOT / "content" / "blog_writer_runs"


def slugify(old_path: str) -> str:
    name = old_path.strip().lower()
    if name == "index.html":
        return "index"
    name = re.sub(r"\.html$", "", name)
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_headings(html: str) -> tuple[str, list[str]]:
    def clean(s: str) -> str:
        s = re.sub(r"<[^>]+>", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    h1 = ""
    m1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.I | re.S)
    if m1:
        h1 = clean(m1.group(1))

    h2 = []
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, flags=re.I | re.S):
        h2.append(clean(m.group(1)))
    return h1, h2[:14]


def persona_for(page: PageInfo) -> str:
    p = page.new_path
    t = page.page_type.lower()

    if p == "index.html":
        return "Local family looking for an eye doctor they can trust"
    if "/locations/" in p or t == "location":
        return "New patient choosing the most convenient location"
    if "/dry-eye/" in p:
        return "Adult with dry eye symptoms who wants lasting relief"
    if "/myopia/" in p:
        return "Parent of a child with worsening nearsightedness"
    if "/services/pediatric/" in p:
        return "Parent booking a child’s eye exam and looking for a calm, friendly experience"
    if "/eyewear/" in p and "/specialty/" in p:
        return "Patient with hard-to-fit eyes who needs specialty contact lens expertise"
    if "/eyewear/" in p:
        return "Adult who needs glasses or contacts that feel good and look great"
    if "/services/conditions/" in p:
        return "Patient researching a diagnosis and deciding when to schedule care"
    if "/services/exams/" in p:
        return "Patient ready to book an exam and wants to know what to expect"
    if "/patients/" in p:
        return "New or returning patient who needs clear next steps"
    if "/about/" in p:
        return "Patient comparing practices and looking for trust signals"
    if "/legal/" in p:
        return "Website visitor who wants clear, plain-language policies"
    if t == "careers":
        return "Candidate evaluating a clinic culture and role fit"
    if t == "blog hub":
        return "Reader browsing eye care articles and updates"
    return "Patient exploring care options"


def pain_points_for(page: PageInfo) -> list[str]:
    p = page.new_path
    if "/dry-eye/" in p:
        return [
            "Burning, gritty, watery eyes that keep coming back",
            "Drops that only help for a short time",
            "Screen time making symptoms worse",
            "Not knowing which treatment actually fits the cause",
        ]
    if "/myopia/" in p:
        return [
            "A child’s prescription changing quickly",
            "Worry about long-term eye health risks from higher myopia",
            "Uncertainty about which option is realistic for a child",
        ]
    if "/services/pediatric/" in p:
        return [
            "Not knowing when a child should have an eye exam",
            "Concern a child will be nervous or uncooperative",
            "School screenings missing problems that affect learning",
        ]
    if "/services/conditions/" in p:
        return [
            "Confusing symptoms and unclear next steps",
            "Fear of missing a serious eye health issue",
            "Wanting clear explanation without medical jargon",
        ]
    if "/eyewear/" in p:
        return [
            "Glasses or contacts that feel uncomfortable",
            "Not understanding lens options and pricing",
            "Wanting honest guidance without pressure",
        ]
    if "/locations/" in p:
        return [
            "Unsure which location to book",
            "Need convenient scheduling and clear directions",
            "Want confidence the care will be thorough and friendly",
        ]
    if "/patients/" in p:
        return [
            "Not sure what to bring or how to prepare",
            "Confusion about insurance and costs",
            "Wanting to book quickly without back-and-forth",
        ]
    if "/about/" in p:
        return [
            "Trying to decide if the practice is the right fit",
            "Want proof the clinic is thorough and kind",
        ]
    if "/legal/" in p:
        return [
            "Wanting privacy and accessibility details in plain language",
            "Need to know how information is handled and who to contact",
        ]
    return ["Need clear, trustworthy information and an easy next step"]


def aspirations_for(page: PageInfo) -> list[str]:
    p = page.new_path
    if "/dry-eye/" in p:
        return [
            "Comfortable eyes that stay comfortable",
            "A plan that treats the root cause, not just symptoms",
            "Confidence trying the next step",
        ]
    if "/myopia/" in p:
        return [
            "Slow myopia progression while keeping daily life simple",
            "Protect long-term eye health",
            "Feel confident about the plan and follow-ups",
        ]
    if "/services/pediatric/" in p:
        return [
            "A positive first exam experience for a child",
            "Clear answers about vision and learning",
            "A plan parents can actually follow",
        ]
    if "/services/conditions/" in p:
        return [
            "Understand what the condition is and what’s next",
            "Catch issues early and protect vision",
            "Feel reassured by a clear plan",
        ]
    if "/eyewear/" in p:
        return [
            "See clearly and feel confident in frames",
            "Lens recommendations that match work and hobbies",
            "Support after purchase (repairs and adjustments)",
        ]
    if "/locations/" in p:
        return [
            "Book the right appointment at the right location",
            "Feel welcomed and cared for from the first call",
        ]
    if "/patients/" in p:
        return [
            "Know exactly what to do next",
            "Set expectations before the visit",
        ]
    if "/about/" in p:
        return [
            "Trust the doctors and team",
            "Feel confident choosing an independent practice",
        ]
    if "/legal/" in p:
        return ["Know what to expect and how to reach us"]
    return ["Clarity, confidence, and an easy way to book"]


def secondary_keywords(primary: str, page: PageInfo) -> list[str]:
    if not primary or primary == "-":
        return []
    p = page.new_path

    base: list[str] = []
    if "/locations/" in p:
        base += ["optometrist near me", "eye exam near me", "vision center"]
    elif "/dry-eye/" in p:
        base += ["dry eye specialist", "meibomian gland dysfunction", "burning eyes relief"]
    elif "/myopia/" in p:
        base += ["myopia management", "kids myopia control", "nearsightedness in children"]
    elif "/services/pediatric/" in p:
        base += ["childrens eye exam", "pediatric optometrist", "school vision screening"]
    elif "/services/conditions/" in p:
        base += ["eye symptoms", "when to see an eye doctor", "vision changes"]
    elif "/eyewear/" in p and "/specialty/" in p:
        base += ["scleral lenses", "keratoconus contacts", "contacts after lasik"]
    elif "/eyewear/" in p:
        base += ["prescription glasses", "contact lenses", "optical boutique"]
    elif "/services/exams/" in p:
        base += ["eye exam", "vision check", "eye health screening"]
    elif "/patients/" in p:
        base += ["book eye exam", "insurance", "new patient forms"]
    elif "/about/" in p:
        base += ["eye doctors", "patient reviews", "family owned optometry"]
    else:
        base += ["eye care", "optometrist", "book appointment"]

    if "kennesaw" in primary.lower() and "kennesaw" not in " ".join(base).lower():
        base.append("kennesaw ga")
    if "marietta" in primary.lower() and "marietta" not in " ".join(base).lower():
        base.append("marietta ga")

    seen = set()
    out = []
    for kw in [primary] + base:
        k = kw.strip()
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(k)
    return out[:6]


def evidence_snippets(page: PageInfo) -> list[str]:
    p = page.new_path
    ev = [
        "VoC Bank: 756 reviews, 4.7 stars; frequent mentions of thorough exams and friendly staff.",
        "Multi-location strategy: two locations with distinct scheduling needs and local markets.",
        "SEO competitor analysis: strong local pack presence, room to grow organic traffic.",
    ]
    if "/dry-eye/" in p:
        ev.insert(
            0,
            "Dry Eye Spa strategy: unique spa positioning; MiBoFlo + IPL + BlephEx + scleral lenses menu.",
        )
    return ev


def stage_text(page: PageInfo) -> str:
    html = read_text(ROOT / page.new_path)
    h1, h2s = extract_headings(html)

    sec_kws = secondary_keywords(page.primary_keyword, page)
    persona = persona_for(page)
    pains = pain_points_for(page)
    aspirations = aspirations_for(page)
    evidence = evidence_snippets(page)
    today = date.today().isoformat()

    lines: list[str] = []
    lines.append(f"# Blog Writer Run - {page.old_path} -> {page.new_path}")
    lines.append("")
    lines.append(f"Generated: {today}")
    lines.append("")

    lines.append("## STAGE 1: Validate Idea")
    lines.append(f"- Primary persona: {persona}")
    lines.append("- Pain points:")
    for x in pains:
        lines.append(f"  - {x}")
    lines.append("- Aspirations:")
    for x in aspirations:
        lines.append(f"  - {x}")
    lines.append("- Language swipe (from VoC):")
    lines.append('  - "thorough" and "explains everything clearly"')
    lines.append('  - "warm, welcoming" and "friendly"')
    lines.append('  - "free repairs and adjustments" (even if you did not buy glasses here)')
    lines.append("")

    lines.append("## STAGE 2: Competitive Landscape Scan")
    lines.append(
        "- Main competitor patterns (from internal research): corporate chains and large regional groups with volume and brand authority."
    )
    lines.append(
        "- Positioning opportunity: independent, family-owned care with a calmer experience and clear explanations."
    )
    lines.append("")

    lines.append("## STAGE 3: Keyword + Channel Blueprint")
    lines.append(f"- Primary keyword: {page.primary_keyword}")
    if sec_kws[1:]:
        lines.append("- Secondary keywords:")
        for x in sec_kws[1:]:
            lines.append(f"  - {x}")
    else:
        lines.append("- Secondary keywords: (n/a)")
    lines.append("")

    lines.append("## STAGE 4: Outcome Crystal")
    lines.append("- After reading, the visitor will: choose the right next step and book the appropriate appointment.")
    lines.append("")

    lines.append("## STAGE 5: Angle Distiller")
    lines.append(
        "- Angle: Thorough eye care meets genuine warmth, backed by strong local reviews and practical support (repairs, guidance, follow-through)."
    )
    lines.append("")

    lines.append("## STAGE 6: Evidence Hunt (Internal Sources)")
    for x in evidence:
        lines.append(f"- {x}")
    lines.append("")

    lines.append("## STAGE 7: Deep Research Notes")
    lines.append("- Use page-specific strategy docs when applicable (dry eye and multi-location).")
    lines.append("- Pull trust signals and wording from the VoC excerpts.")
    lines.append("")

    lines.append("## STAGE 8: Story Spine")
    lines.append("- Problem: visitor has a concern or goal.")
    lines.append("- Clarity: explain options in plain language.")
    lines.append("- Trust: show proof (years, reviews, local presence).")
    lines.append("- Action: simple CTA to book or call.")
    lines.append("")

    lines.append("## STAGE 9: Header Blueprint")
    lines.append(f"- Current H1: {h1 or '(missing)'}")
    lines.append("- Current H2s:")
    if h2s:
        for x in h2s:
            lines.append(f"  - {x}")
    else:
        lines.append("  - (to be refined during rewrite)")
    lines.append("")

    lines.append("## STAGE 10: Section Skeleton")
    lines.append("- Hero: keyword-forward promise + 3-bullet value summary + CTA")
    lines.append("- Main sections: what it is, who it helps, what to expect, why Classic Vision Care, FAQs")
    lines.append("- CTA: book or call, plus next-best internal links")
    lines.append("")

    lines.append("## STAGE 11: Draft Weaver")
    lines.append(f"- Draft lives in: `{page.new_path}`")
    lines.append("")

    lines.append("## STAGE 12: Voice Polish")
    lines.append("- Plain language, short sentences, skimmable sections")
    lines.append("- No AI filler phrases and no banned words")
    lines.append("")

    lines.append("## STAGE 13: Review")
    lines.append("- Run automated checks: banned phrases, em/en dashes, broken markup, missing images, readability target")
    lines.append("")

    lines.append("## STAGE 14: Final Review")
    lines.append("- Fix issues from Stage 13 and confirm intent, accuracy, and on-page SEO basics")
    lines.append("")

    lines.append("## STAGE 15: Technical SEO")
    lines.append("- Verify title, meta description, single H1, alt text, and internal links")
    lines.append("")

    lines.append("## STAGE 16: Featured Image")
    lines.append("- Confirm hero image present and has descriptive alt text")
    lines.append("")

    lines.append("## STAGE 17: CTA")
    lines.append("- Confirm at least one clear CTA (book and/or call)")

    return "\n".join(lines) + "\n"


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


def main() -> int:
    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Missing manifest: {MANIFEST_PATH}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pages = load_pages()
    for page in pages:
        out_path = OUT_DIR / f"{slugify(page.old_path)}.md"
        out_path.write_text(stage_text(page), encoding="utf-8")

    (OUT_DIR / "README.md").write_text(
        "\n".join(
            [
                "# Blog Writer Runs (Per Page)",
                "",
                "These files capture the 17-stage writing checklist for each site page.",
                "They are generated from the site manifest at `content/page_manifest.json`.",
                "",
                f"Generated on: {date.today().isoformat()}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(pages)} briefs to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

