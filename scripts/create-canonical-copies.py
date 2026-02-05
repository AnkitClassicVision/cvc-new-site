#!/usr/bin/env python3
"""
Create "clean URL" directory routes (e.g. /eye-doctor-kennesaw-ga/) by copying
existing HTML files from ./pages into /<route>/index.html.

This is a first-pass scaffold to support the SEO transition plan:
- Keep high-performing legacy slugs live (200) at launch.
- Avoid relying on /pages/... and *.html URLs publicly.

Notes:
- This script only copies files; it does not yet rewrite navigation links.
- Idempotent by default (won't overwrite existing dest files unless --overwrite).
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


COPY_ROUTES: dict[str, str] = {
    "/about-us/": "pages/about/index.html",
    "/why-choose-us/": "pages/about/why-choose-us.html",
    "/testimonials/": "pages/about/testimonials.html",
    "/community-involvement/": "pages/about/community.html",
    "/careers/": "pages/about/careers.html",
    "/contact-us/": "pages/patients/contact.html",
    "/new-patients/": "pages/patients/new.html",
    "/book-now/": "pages/patients/book.html",
    "/insurance/": "pages/patients/insurance.html",
    "/accessibility/": "pages/legal/accessibility.html",
    "/privacy-policy-2/": "pages/legal/privacy.html",
    "/our-doctors/": "pages/about/doctors/index.html",
    "/dr-mital-patel-od/": "pages/about/doctors/mital-patel.html",
    "/dr-bhumi-patel-od/": "pages/about/doctors/bhumi-patel.html",
    "/our-locations/": "pages/locations/index.html",
    "/eye-doctor-kennesaw-ga/": "pages/locations/kennesaw.html",
    "/eye-doctor-marietta/": "pages/locations/east-cobb.html",
    "/eye-care-services/": "pages/services/index.html",
    "/comprehensive-eye-exams/": "pages/services/exams/comprehensive.html",
    "/contact-lens-exams/": "pages/services/exams/contact-lens.html",
    "/diabetic-eye-exam/": "pages/services/exams/diabetic.html",
    "/pediatric-eye-exams/": "pages/services/pediatric/eye-exams.html",
    "/pediatric-eye-care/": "pages/services/pediatric/eye-care.html",
    "/childrens-eye-exam/": "pages/services/pediatric/childrens-exam.html",
    "/school-vision-screening/": "pages/services/pediatric/school-screening.html",
    "/dry-eye-treatment/": "pages/dry-eye/treatments.html",
    "/dry-eye-treatment-blephex/": "pages/dry-eye/treatments/blephex.html",
    "/dry-eye-treatment-eye-drops/": "pages/dry-eye/treatments/eye-drops.html",
    "/dry-eye-treatment-intense-pulsed-light/": "pages/dry-eye/treatments/ipl.html",
    "/dry-eye-treatment-miboflo/": "pages/dry-eye/treatments/miboflo.html",
    "/dry-eye-treatment-punctal-plugs/": "pages/dry-eye/treatments/punctal-plugs.html",
    "/dry-eye-treatment-eye-supplements/": "pages/dry-eye/treatments/supplements.html",
    "/scleral-lenses-for-dry-eyes/": "pages/dry-eye/treatments/scleral-lenses.html",
    "/myopia-control/": "pages/myopia/index.html",
    "/misight-lenses-for-myopia-control/": "pages/myopia/treatments/misight.html",
    "/ortho-k-lenses-for-myopia-control/": "pages/myopia/treatments/ortho-k.html",
    "/myopia-control-atropine-eye-drops/": "pages/myopia/treatments/atropine.html",
    "/myopia-control-multifocal-lenses/": "pages/myopia/treatments/multifocal.html",
    "/myopia-in-children/": "pages/myopia/children.html",
    "/specialty-contact-lenses/": "pages/eyewear/specialty/index.html",
    "/scleral-lenses-atlanta/": "pages/eyewear/specialty/scleral.html",
    "/keratoconus-contacts/": "pages/eyewear/specialty/keratoconus.html",
    "/post-lasik-contacts/": "pages/eyewear/specialty/post-lasik.html",
    "/contact-lenses/": "pages/eyewear/contact-lenses.html",
    "/eyewear/": "pages/eyewear/index.html",
    "/eyeglasses/": "pages/eyewear/eyeglasses.html",
    "/sunglasses/": "pages/eyewear/sunglasses.html",
    "/allergies/": "pages/services/conditions/allergies.html",
    "/astigmatism/": "pages/services/conditions/astigmatism.html",
    "/glaucoma/": "pages/services/conditions/glaucoma.html",
    "/macular-degeneration/": "pages/services/conditions/macular-degeneration.html",
    # Blog hub placeholder (will be replaced with real listing later)
    "/blog/": "pages/about/blog.html",
}


def ensure_trailing_slash(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path


def route_to_dest(route: str) -> Path:
    route = ensure_trailing_slash(route)
    if route == "/":
        raise ValueError("Homepage (/) is not a directory route.")
    return BASE_DIR / route.strip("/") / "index.html"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing destination files.")
    args = parser.parse_args()

    copied = 0
    skipped = 0
    missing = 0

    for route, source_rel in sorted(COPY_ROUTES.items()):
        source_path = (BASE_DIR / source_rel).resolve()
        dest_path = route_to_dest(route)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if not source_path.exists():
            print(f"[MISSING] {route} ← {source_rel}")
            missing += 1
            continue

        if dest_path.exists() and not args.overwrite:
            print(f"[SKIP]    {route} (already exists)")
            skipped += 1
            continue

        shutil.copyfile(source_path, dest_path)
        print(f"[COPY]    {route} ← {source_rel}")
        copied += 1

    print(f"\nDone. Copied: {copied}, Skipped: {skipped}, Missing: {missing}")
    return 0 if missing == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
