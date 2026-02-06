#!/usr/bin/env python3
"""
Reorganize HTML pages into a deep hierarchy structure.
Creates folders, moves files, and updates all internal links.
"""

import os
import re
import shutil
from pathlib import Path

# Mapping: old filename -> new path (relative to cvc-new/)
FILE_MAPPING = {
    # Root - stays
    'index.html': 'index.html',

    # Services
    'eye-care-services.html': 'pages/services/index.html',

    # Services > Exams
    'comprehensive-eye-exams.html': 'pages/services/exams/comprehensive.html',
    'contact-lens-exams.html': 'pages/services/exams/contact-lens.html',
    'diabetic-eye-exam.html': 'pages/services/exams/diabetic.html',

    # Services > Pediatric
    'pediatric-eye-care.html': 'pages/services/pediatric/eye-care.html',
    'pediatric-eye-exams.html': 'pages/services/pediatric/eye-exams.html',
    'childrens-eye-exam.html': 'pages/services/pediatric/childrens-exam.html',
    'school-vision-screening.html': 'pages/services/pediatric/school-screening.html',

    # Services > Conditions
    'glaucoma-treatment.html': 'pages/services/conditions/glaucoma.html',
    'macular-degeneration.html': 'pages/services/conditions/macular-degeneration.html',
    'eye-allergies.html': 'pages/services/conditions/allergies.html',
    'astigmatism-correction.html': 'pages/services/conditions/astigmatism.html',

    # Dry Eye
    'dry-eye-spa.html': 'pages/dry-eye/index.html',
    'dry-eye-treatment.html': 'pages/dry-eye/treatments.html',

    # Dry Eye > Treatments
    'dry-eye-treatment-intense-pulsed-light.html': 'pages/dry-eye/treatments/ipl.html',
    'dry-eye-treatment-miboflo.html': 'pages/dry-eye/treatments/miboflo.html',
    'dry-eye-treatment-blephex.html': 'pages/dry-eye/treatments/blephex.html',
    'dry-eye-treatment-punctal-plugs.html': 'pages/dry-eye/treatments/punctal-plugs.html',
    'scleral-lenses-for-dry-eyes.html': 'pages/dry-eye/treatments/scleral-lenses.html',

    # Myopia
    'myopia-control.html': 'pages/myopia/index.html',
    'myopia-in-children.html': 'pages/myopia/children.html',

    # Myopia > Treatments
    'misight-lenses-for-myopia-control.html': 'pages/myopia/treatments/misight.html',
    'ortho-k-lenses-for-myopia-control.html': 'pages/myopia/treatments/ortho-k.html',
    'myopia-control-atropine-eye-drops.html': 'pages/myopia/treatments/atropine.html',
    'myopia-control-multifocal-lenses.html': 'pages/myopia/treatments/multifocal.html',

    # Eyewear
    'eyewear.html': 'pages/eyewear/index.html',
    'eyeglasses.html': 'pages/eyewear/eyeglasses.html',
    'sunglasses.html': 'pages/eyewear/sunglasses.html',
    'contact-lenses.html': 'pages/eyewear/contact-lenses.html',

    # Eyewear > Specialty
    'specialty-contact-lenses.html': 'pages/eyewear/specialty/index.html',
    'scleral-lenses-atlanta.html': 'pages/eyewear/specialty/scleral.html',
    'keratoconus-contacts.html': 'pages/eyewear/specialty/keratoconus.html',
    'post-lasik-contacts.html': 'pages/eyewear/specialty/post-lasik.html',

    # Locations
    'our-locations.html': 'pages/locations/index.html',
    'eye-doctor-kennesaw-ga.html': 'pages/locations/kennesaw.html',
    'east-cobb-eye-doctors.html': 'pages/locations/east-cobb.html',

    # About
    'about-us.html': 'pages/about/index.html',
    'why-choose-us.html': 'pages/about/why-choose-us.html',
    'testimonials.html': 'pages/about/testimonials.html',
    'community-involvement.html': 'pages/about/community.html',
    'careers.html': 'pages/about/careers.html',
    'blog.html': 'pages/about/blog.html',

    # About > Doctors
    'our-doctors.html': 'pages/about/doctors/index.html',
    'dr-mital-patel-od.html': 'pages/about/doctors/mital-patel.html',
    'dr-bhumi-patel-od.html': 'pages/about/doctors/bhumi-patel.html',

    # Patients
    'new-patients.html': 'pages/patients/new.html',
    'insurance.html': 'pages/patients/insurance.html',
    'contact.html': 'pages/patients/contact.html',
    'book-now.html': 'pages/patients/book.html',

    # Legal
    'privacy-policy-2.html': 'pages/legal/privacy.html',
    'accessibility.html': 'pages/legal/accessibility.html',
}

def create_directories(base_dir):
    """Create all necessary directories"""
    dirs = set()
    for new_path in FILE_MAPPING.values():
        dir_path = os.path.dirname(new_path)
        if dir_path:
            dirs.add(dir_path)

    for d in sorted(dirs):
        full_path = base_dir / d
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {d}/")

def compute_relative_path(from_file, to_file):
    """Compute relative path from one file to another"""
    from_dir = os.path.dirname(from_file)

    # Count how many levels up we need to go
    if from_dir:
        levels_up = from_dir.count('/') + 1
        prefix = '../' * levels_up
    else:
        prefix = ''

    return prefix + to_file

def update_links_in_file(file_path, file_new_path, mapping):
    """Update all internal links in a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update href and src attributes
    def replace_link(match):
        attr = match.group(1)  # href or src
        quote = match.group(2)  # " or '
        old_link = match.group(3)

        # Skip external links, anchors, tel:, mailto:, javascript:
        if old_link.startswith(('http://', 'https://', '#', 'tel:', 'mailto:', 'javascript:', 'data:')):
            return match.group(0)

        # Skip asset paths (images, styles, scripts)
        if old_link.startswith(('images/', 'styles/', 'scripts/')):
            # Need to adjust path based on new file location
            new_file_dir = os.path.dirname(file_new_path)
            if new_file_dir:
                levels_up = new_file_dir.count('/') + 1
                prefix = '../' * levels_up
                return f'{attr}={quote}{prefix}{old_link}{quote}'
            return match.group(0)

        # Handle HTML file links
        # Extract just the filename (remove any path prefix and query/hash)
        link_parts = old_link.split('?')[0].split('#')
        base_link = link_parts[0]
        suffix = ''
        if '?' in old_link:
            suffix = '?' + old_link.split('?')[1]
        elif len(link_parts) > 1:
            suffix = '#' + link_parts[1]

        # Get just the filename
        old_filename = os.path.basename(base_link)

        if old_filename in mapping:
            new_target = mapping[old_filename]
            relative_path = compute_relative_path(file_new_path, new_target)
            return f'{attr}={quote}{relative_path}{suffix}{quote}'

        return match.group(0)

    # Match href="..." or src="..." or href='...' or src='...'
    pattern = r'(href|src)=(["\'])([^"\']*)\2'
    new_content = re.sub(pattern, replace_link, content)

    return new_content

def main():
    base_dir = Path(__file__).parent.parent

    print("Step 1: Creating directory structure...")
    create_directories(base_dir)

    print("\nStep 2: Moving and updating files...")

    # First pass: read all files and update links
    updated_files = {}
    for old_name, new_path in FILE_MAPPING.items():
        old_file = base_dir / old_name
        if old_file.exists():
            new_content = update_links_in_file(old_file, new_path, FILE_MAPPING)
            updated_files[new_path] = new_content
            print(f"  Processed: {old_name} -> {new_path}")
        else:
            print(f"  WARNING: {old_name} not found!")

    print("\nStep 3: Writing files to new locations...")
    for new_path, content in updated_files.items():
        new_file = base_dir / new_path
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)

    print("\nStep 4: Removing old files from root...")
    for old_name in FILE_MAPPING.keys():
        if old_name == 'index.html':
            continue  # Keep index.html at root
        old_file = base_dir / old_name
        if old_file.exists():
            old_file.unlink()
            print(f"  Removed: {old_name}")

    print("\nStep 5: Generating path reference...")
    ref_content = "# CVC-New URL Structure Reference\n\n"
    ref_content += "Use this as a reference for the new URL paths.\n\n"
    ref_content += "| Old Path | New Path |\n"
    ref_content += "|----------|----------|\n"
    for old_name, new_path in sorted(FILE_MAPPING.items()):
        ref_content += f"| {old_name} | {new_path} |\n"

    with open(base_dir / 'URL_STRUCTURE.md', 'w') as f:
        f.write(ref_content)
    print("  Created: URL_STRUCTURE.md")

    print("\n Done! Reorganized", len(FILE_MAPPING), "files.")

if __name__ == '__main__':
    main()
