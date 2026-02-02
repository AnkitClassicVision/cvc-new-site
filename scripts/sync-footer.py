#!/usr/bin/env python3
"""
Sync footer across all HTML pages with proper relative paths.
"""

import os
import re
from pathlib import Path

# Footer content with placeholders for relative paths
FOOTER_TEMPLATE = '''  <!-- Footer -->
  <footer class="ef-footer bg-cvc-charcoal text-white pt-16 pb-8">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid md:grid-cols-2 lg:grid-cols-5 gap-10 mb-12">
        <!-- Brand Column -->
        <div>
          <a href="{prefix}index.html" class="flex items-center gap-3 mb-6">
            <div class="w-12 h-12 bg-cvc-teal-500 rounded-full flex items-center justify-center">
              <svg class="w-7 h-7 text-white" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
              </svg>
            </div>
            <span class="font-display text-xl font-semibold">Classic Vision Care</span>
          </a>
          <p class="text-gray-400 text-sm leading-relaxed mb-6">
            Providing comprehensive eye care with a personal touch for over 25 years.
          </p>
          <div class="flex gap-4">
            <a href="https://facebook.com/classicvisioncare" target="_blank" rel="noopener" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-cvc-teal-500 transition-colors" aria-label="Facebook">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            </a>
            <a href="https://instagram.com/classicvisioncare" target="_blank" rel="noopener" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center hover:bg-cvc-teal-500 transition-colors" aria-label="Instagram">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
            </a>
          </div>
        </div>

        <!-- Services -->
        <div>
          <h3 class="font-semibold text-lg mb-5">Services</h3>
          <ul class="space-y-3">
            <li><a href="{prefix}pages/services/index.html" class="text-gray-400 hover:text-white transition-colors text-sm">Eye Care Services</a></li>
            <li><a href="{prefix}pages/dry-eye/index.html" class="text-gray-400 hover:text-white transition-colors text-sm">Dry Eye Spa</a></li>
            <li><a href="{prefix}pages/myopia/index.html" class="text-gray-400 hover:text-white transition-colors text-sm">Myopia Control</a></li>
            <li><a href="{prefix}pages/services/pediatric/eye-care.html" class="text-gray-400 hover:text-white transition-colors text-sm">Pediatric Eye Care</a></li>
            <li><a href="{prefix}pages/eyewear/specialty/index.html" class="text-gray-400 hover:text-white transition-colors text-sm">Specialty Contacts</a></li>
            <li><a href="{prefix}pages/eyewear/index.html" class="text-gray-400 hover:text-white transition-colors text-sm">Eyewear</a></li>
          </ul>
        </div>

        <!-- Conditions & About -->
        <div>
          <h3 class="font-semibold text-lg mb-5">Conditions & About</h3>
          <ul class="space-y-3">
            <li><a href="{prefix}pages/services/conditions/glaucoma.html" class="text-gray-400 hover:text-white transition-colors text-sm">Glaucoma</a></li>
            <li><a href="{prefix}pages/services/conditions/macular-degeneration.html" class="text-gray-400 hover:text-white transition-colors text-sm">Macular Degeneration</a></li>
            <li><a href="{prefix}pages/services/conditions/astigmatism.html" class="text-gray-400 hover:text-white transition-colors text-sm">Astigmatism</a></li>
            <li><a href="{prefix}pages/services/conditions/allergies.html" class="text-gray-400 hover:text-white transition-colors text-sm">Eye Allergies</a></li>
            <li><a href="{prefix}pages/about/doctors/index.html" class="text-gray-400 hover:text-white transition-colors text-sm">Our Doctors</a></li>
            <li><a href="{prefix}pages/about/why-choose-us.html" class="text-gray-400 hover:text-white transition-colors text-sm">Why Choose Us</a></li>
            <li><a href="{prefix}pages/about/testimonials.html" class="text-gray-400 hover:text-white transition-colors text-sm">Testimonials</a></li>
            <li><a href="{prefix}pages/about/careers.html" class="text-gray-400 hover:text-white transition-colors text-sm">Careers</a></li>
            <li><a href="{prefix}pages/about/blog.html" class="text-gray-400 hover:text-white transition-colors text-sm">Blog</a></li>
            <li><a href="{prefix}pages/patients/insurance.html" class="text-gray-400 hover:text-white transition-colors text-sm">Insurance</a></li>
            <li><a href="{prefix}pages/patients/new.html" class="text-gray-400 hover:text-white transition-colors text-sm">New Patients</a></li>
            <li><a href="{prefix}pages/patients/book.html" class="text-gray-400 hover:text-white transition-colors text-sm">Book Appointment</a></li>
          </ul>
        </div>

        <!-- Kennesaw Location -->
        <div>
          <h3 class="font-semibold text-lg mb-5">Kennesaw</h3>
          <address class="not-italic text-gray-400 text-sm space-y-2">
            <p>1615 Ridenour Blvd<br>Suite 201<br>Kennesaw, GA 30152</p>
            <p><a href="tel:+17704992020" class="hover:text-white transition-colors">(770) 499-2020</a></p>
            <p class="text-xs">Tue: 9am - 6pm<br>Wed: 8am - 5pm<br>Thu: 9am - 6pm<br>Fri: 8am - 5pm<br>Sat: 10am - 2pm</p>
          </address>
          <a href="{prefix}pages/locations/kennesaw.html" class="inline-block mt-3 text-cvc-teal-500 hover:text-cvc-teal-400 text-sm font-medium">View Location →</a>
        </div>

        <!-- East Cobb Location -->
        <div>
          <h3 class="font-semibold text-lg mb-5">East Cobb</h3>
          <address class="not-italic text-gray-400 text-sm space-y-2">
            <p>3535 Roswell Rd<br>Suite 8<br>Marietta, GA 30062</p>
            <p><a href="tel:+16785608065" class="hover:text-white transition-colors">(678) 560-8065</a></p>
            <p class="text-xs">Tue: 9am - 6pm<br>Wed: 8am - 5pm<br>Thu: 9am - 6pm<br>Fri: 8am - 5pm</p>
          </address>
          <a href="{prefix}pages/locations/east-cobb.html" class="inline-block mt-3 text-cvc-teal-500 hover:text-cvc-teal-400 text-sm font-medium">View Location →</a>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-gray-400 text-sm">&copy; 2026 Classic Vision Care. All rights reserved.</p>
        <div class="flex gap-6 text-sm">
          <a href="{prefix}pages/about/blog.html" class="text-gray-400 hover:text-white transition-colors">Blog</a>
          <a href="{prefix}pages/about/careers.html" class="text-gray-400 hover:text-white transition-colors">Careers</a>
          <a href="{prefix}pages/legal/privacy.html" class="text-gray-400 hover:text-white transition-colors">Privacy Policy</a>
          <a href="{prefix}pages/legal/accessibility.html" class="text-gray-400 hover:text-white transition-colors">Accessibility</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Sticky Mobile CTA -->
  <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 md:hidden z-40">
    <div class="flex gap-3">
      <a href="tel:+17704992020" class="flex-1 flex items-center justify-center gap-2 bg-cvc-teal-500 text-white py-3 rounded font-medium text-sm">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
        </svg>
        Call Now
      </a>
      <a href="{prefix}pages/patients/book.html" class="flex-1 flex items-center justify-center gap-2 bg-cvc-gold text-cvc-charcoal py-3 rounded font-medium text-sm">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        Book
      </a>
    </div>
  </div>

  <!-- Forest Editorial Interactive Effects -->
  <script src="{prefix}scripts/editorial-forest.js"></script>'''


def get_prefix(file_path, base_dir):
    """Calculate relative prefix from file to base directory"""
    rel_path = os.path.relpath(file_path, base_dir)
    depth = rel_path.count(os.sep)
    if depth == 0:
        return ''
    return '../' * depth


def replace_footer(content, new_footer):
    """Replace footer section in content"""
    # Match from <!-- Footer --> to </script> after editorial-forest.js
    pattern = r'(  <!-- Footer -->.*?<script src="[^"]*editorial-forest\.js"></script>)'
    if re.search(pattern, content, re.DOTALL):
        return re.sub(pattern, new_footer, content, count=1, flags=re.DOTALL)
    return None


def main():
    base_dir = Path(__file__).parent.parent

    # Find all HTML files
    html_files = list(base_dir.rglob('*.html'))

    updated = 0
    skipped = 0

    for html_file in html_files:
        # Skip partials, dev, node_modules
        if 'partials' in str(html_file) or 'dev' in str(html_file) or 'node_modules' in str(html_file):
            continue

        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Calculate prefix for this file
        prefix = get_prefix(html_file, base_dir)
        footer = FOOTER_TEMPLATE.format(prefix=prefix)

        new_content = replace_footer(content, footer)
        if new_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Updated: {html_file.relative_to(base_dir)}")
            updated += 1
        else:
            print(f"  Skipped (no footer): {html_file.relative_to(base_dir)}")
            skipped += 1

    print(f"\nDone! Updated {updated} files, skipped {skipped}.")


if __name__ == '__main__':
    main()
