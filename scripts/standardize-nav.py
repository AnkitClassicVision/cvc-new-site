#!/usr/bin/env python3
"""
Standardize navigation across all CVC HTML pages.
This script replaces the header and footer sections with a consistent template.
"""

import os
import re
from pathlib import Path

# Directory containing HTML files
HTML_DIR = Path(__file__).parent.parent

# Files to process (exclude node_modules)
HTML_FILES = [f for f in HTML_DIR.glob("*.html") if "node_modules" not in str(f)]

# Standard navigation template (top bar + header + mobile menu)
NAV_TEMPLATE = '''  <!-- Top Phone Bar -->
  <div class="bg-cvc-charcoal text-white py-2 text-sm hidden md:block">
    <div class="max-w-7xl mx-auto px-6 flex justify-between items-center">
      <p class="text-gray-300">Serving Kennesaw & East Cobb/Marietta for 25+ Years</p>
      <div class="flex items-center gap-6">
        <a href="tel:+17704992020" class="flex items-center gap-2 hover:text-cvc-gold-light transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
          </svg>
          <span>Kennesaw: (770) 499-2020</span>
        </a>
        <span class="text-gray-600">|</span>
        <a href="tel:+17705098800" class="flex items-center gap-2 hover:text-cvc-gold-light transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
          </svg>
          <span>East Cobb: (770) 509-8800</span>
        </a>
      </div>
    </div>
  </div>

  <!-- Header -->
  <header id="header" class="sticky top-0 z-50 bg-white shadow-sm transition-all duration-300">
    <div class="max-w-7xl mx-auto px-6">
      <nav class="flex items-center justify-between h-20 lg:h-24">
        <!-- Logo -->
        <a href="index.html" class="flex items-center gap-3">
          <div class="w-12 h-12 lg:w-14 lg:h-14 bg-cvc-teal-500 rounded-full flex items-center justify-center">
            <svg class="w-8 h-8 lg:w-10 lg:h-10 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
            </svg>
          </div>
          <div>
            <span class="font-display text-xl lg:text-2xl font-semibold text-cvc-charcoal">Classic Vision Care</span>
            <span class="hidden sm:block text-xs text-gray-500 tracking-wider uppercase">Eye Care Excellence</span>
          </div>
        </a>

        <!-- Desktop Navigation with Dropdowns -->
        <div class="hidden lg:flex items-center gap-6">
          <!-- Services Dropdown -->
          <div class="nav-dropdown relative group">
            <a href="eye-care-services.html" class="nav-link flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-cvc-teal-500 transition-colors py-2">
              Services
              <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </a>
            <div class="dropdown-menu absolute top-full left-0 pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
              <div class="bg-white rounded-xl shadow-xl border border-gray-100 py-3 min-w-[240px]">
                <div class="px-5 py-2 text-xs font-semibold text-cvc-gold uppercase tracking-wider">Eye Exams</div>
                <a href="comprehensive-eye-exams.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Comprehensive Eye Exams</a>
                <a href="contact-lens-exams.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Contact Lens Exams</a>
                <a href="pediatric-eye-exams.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Pediatric Eye Exams</a>
                <a href="diabetic-eye-exam.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Diabetic Eye Exam</a>
                <div class="border-t border-gray-100 my-2"></div>
                <div class="px-5 py-2 text-xs font-semibold text-cvc-gold uppercase tracking-wider">Conditions</div>
                <a href="glaucoma-treatment.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Glaucoma</a>
                <a href="macular-degeneration.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Macular Degeneration</a>
                <a href="eye-allergies.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Eye Allergies</a>
                <a href="astigmatism-correction.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Astigmatism</a>
                <div class="border-t border-gray-100 my-2"></div>
                <a href="eye-care-services.html" class="block px-5 py-2.5 text-sm font-medium text-cvc-teal-600 hover:bg-cvc-teal-50 transition-colors">View All Services →</a>
              </div>
            </div>
          </div>

          <!-- Dry Eye Dropdown -->
          <div class="nav-dropdown relative group">
            <a href="dry-eye-treatment.html" class="nav-link flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-cvc-teal-500 transition-colors py-2">
              Dry Eye Spa
              <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </a>
            <div class="dropdown-menu absolute top-full left-0 pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
              <div class="bg-white rounded-xl shadow-xl border border-gray-100 py-3 min-w-[240px]">
                <div class="px-5 py-2 text-xs font-semibold text-cvc-gold uppercase tracking-wider">Treatments</div>
                <a href="dry-eye-treatment-intense-pulsed-light.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">IPL Therapy</a>
                <a href="dry-eye-treatment-miboflo.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">MiBoFlo</a>
                <a href="dry-eye-treatment-blephex.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">BlephEx</a>
                <a href="dry-eye-treatment-punctal-plugs.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Punctal Plugs</a>
                <a href="scleral-lenses-for-dry-eyes.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Scleral Lenses</a>
                <div class="border-t border-gray-100 my-2"></div>
                <a href="dry-eye-treatment.html" class="block px-5 py-2.5 text-sm font-medium text-cvc-teal-600 hover:bg-cvc-teal-50 transition-colors">Explore Dry Eye Spa →</a>
              </div>
            </div>
          </div>

          <!-- Myopia Control Dropdown -->
          <div class="nav-dropdown relative group">
            <a href="myopia-control.html" class="nav-link flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-cvc-teal-500 transition-colors py-2">
              Myopia Control
              <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </a>
            <div class="dropdown-menu absolute top-full left-0 pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
              <div class="bg-white rounded-xl shadow-xl border border-gray-100 py-3 min-w-[220px]">
                <a href="misight-lenses-for-myopia-control.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">MiSight® Lenses</a>
                <a href="ortho-k-lenses-for-myopia-control.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Ortho-K Lenses</a>
                <a href="myopia-control-atropine-eye-drops.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Atropine Eye Drops</a>
                <a href="myopia-control-multifocal-lenses.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Multifocal Lenses</a>
                <div class="border-t border-gray-100 my-2"></div>
                <a href="myopia-control.html" class="block px-5 py-2.5 text-sm font-medium text-cvc-teal-600 hover:bg-cvc-teal-50 transition-colors">Learn About Myopia →</a>
              </div>
            </div>
          </div>

          <!-- Eyewear Dropdown -->
          <div class="nav-dropdown relative group">
            <a href="eyewear.html" class="nav-link flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-cvc-teal-500 transition-colors py-2">
              Eyewear
              <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </a>
            <div class="dropdown-menu absolute top-full left-0 pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
              <div class="bg-white rounded-xl shadow-xl border border-gray-100 py-3 min-w-[200px]">
                <a href="eyeglasses.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Eyeglasses</a>
                <a href="sunglasses.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Sunglasses</a>
                <a href="contact-lenses.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Contact Lenses</a>
                <a href="specialty-contact-lenses.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Specialty Contacts</a>
                <div class="border-t border-gray-100 my-2"></div>
                <a href="eyewear.html" class="block px-5 py-2.5 text-sm font-medium text-cvc-teal-600 hover:bg-cvc-teal-50 transition-colors">Browse Eyewear →</a>
              </div>
            </div>
          </div>

          <!-- Locations Dropdown -->
          <div class="nav-dropdown relative group">
            <a href="our-locations.html" class="nav-link flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-cvc-teal-500 transition-colors py-2">
              Locations
              <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </a>
            <div class="dropdown-menu absolute top-full left-0 pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
              <div class="bg-white rounded-xl shadow-xl border border-gray-100 py-3 min-w-[200px]">
                <a href="eye-doctor-kennesaw-ga.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">
                  <span class="font-medium">Kennesaw</span>
                  <span class="block text-xs text-gray-500">(770) 499-2020</span>
                </a>
                <a href="east-cobb-eye-doctors.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">
                  <span class="font-medium">East Cobb / Marietta</span>
                  <span class="block text-xs text-gray-500">(770) 509-8800</span>
                </a>
              </div>
            </div>
          </div>

          <!-- About Dropdown -->
          <div class="nav-dropdown relative group">
            <a href="about-us.html" class="nav-link flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-cvc-teal-500 transition-colors py-2">
              About
              <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </a>
            <div class="dropdown-menu absolute top-full right-0 pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
              <div class="bg-white rounded-xl shadow-xl border border-gray-100 py-3 min-w-[200px]">
                <a href="our-doctors.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Our Doctors</a>
                <a href="dr-mital-patel-od.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors pl-8">Dr. Mital Patel, OD</a>
                <a href="dr-bhumi-patel-od.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors pl-8">Dr. Bhumi Patel, OD</a>
                <div class="border-t border-gray-100 my-2"></div>
                <a href="new-patients.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">New Patients</a>
                <a href="insurance.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Insurance</a>
                <a href="contact.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Contact Us</a>
                <div class="border-t border-gray-100 my-2"></div>
                <a href="careers.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Careers</a>
                <a href="blog.html" class="block px-5 py-2.5 text-sm text-gray-700 hover:bg-cvc-teal-50 hover:text-cvc-teal-600 transition-colors">Blog</a>
              </div>
            </div>
          </div>
        </div>

        <!-- CTA Button -->
        <div class="flex items-center gap-4">
          <a href="book-now.html" class="hidden sm:inline-flex items-center gap-2 bg-cvc-teal-500 text-white px-6 py-3 rounded font-medium text-sm hover:bg-cvc-teal-600 transition-colors">
            Book Appointment
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
            </svg>
          </a>

          <!-- Mobile Menu Button -->
          <button id="mobile-menu-btn" class="lg:hidden p-3 min-w-[44px] min-h-[44px] text-gray-700" aria-label="Open navigation menu">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
        </div>
      </nav>
    </div>

    <!-- Mobile Menu -->
    <div id="mobile-menu" class="hidden lg:hidden bg-white border-t max-h-[80vh] overflow-y-auto">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <!-- Services Accordion -->
        <div class="mobile-accordion border-b border-gray-100">
          <button class="accordion-toggle w-full flex items-center justify-between py-3 text-gray-700 font-medium" data-target="mobile-services">
            Services
            <svg class="accordion-icon w-5 h-5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div id="mobile-services" class="accordion-content hidden pb-3 pl-4 space-y-2">
            <span class="block pt-2 text-xs font-semibold text-cvc-gold uppercase tracking-wider">Eye Exams</span>
            <a href="comprehensive-eye-exams.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Comprehensive Eye Exams</a>
            <a href="contact-lens-exams.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Contact Lens Exams</a>
            <a href="pediatric-eye-exams.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Pediatric Eye Exams</a>
            <a href="diabetic-eye-exam.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Diabetic Eye Exam</a>
            <span class="block pt-3 text-xs font-semibold text-cvc-gold uppercase tracking-wider">Conditions</span>
            <a href="glaucoma-treatment.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Glaucoma</a>
            <a href="macular-degeneration.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Macular Degeneration</a>
            <a href="eye-allergies.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Eye Allergies</a>
            <a href="astigmatism-correction.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Astigmatism</a>
            <a href="eye-care-services.html" class="block py-2 text-sm text-cvc-teal-600 font-medium">View All Services →</a>
          </div>
        </div>

        <!-- Dry Eye Accordion -->
        <div class="mobile-accordion border-b border-gray-100">
          <button class="accordion-toggle w-full flex items-center justify-between py-3 text-gray-700 font-medium" data-target="mobile-dryeye">
            Dry Eye Spa
            <svg class="accordion-icon w-5 h-5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div id="mobile-dryeye" class="accordion-content hidden pb-3 pl-4 space-y-2">
            <a href="dry-eye-treatment-intense-pulsed-light.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">IPL Therapy</a>
            <a href="dry-eye-treatment-miboflo.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">MiBoFlo</a>
            <a href="dry-eye-treatment-blephex.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">BlephEx</a>
            <a href="dry-eye-treatment-punctal-plugs.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Punctal Plugs</a>
            <a href="scleral-lenses-for-dry-eyes.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Scleral Lenses</a>
            <a href="dry-eye-treatment.html" class="block py-2 text-sm text-cvc-teal-600 font-medium">Explore Dry Eye Spa →</a>
          </div>
        </div>

        <!-- Myopia Accordion -->
        <div class="mobile-accordion border-b border-gray-100">
          <button class="accordion-toggle w-full flex items-center justify-between py-3 text-gray-700 font-medium" data-target="mobile-myopia">
            Myopia Control
            <svg class="accordion-icon w-5 h-5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div id="mobile-myopia" class="accordion-content hidden pb-3 pl-4 space-y-2">
            <a href="misight-lenses-for-myopia-control.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">MiSight® Lenses</a>
            <a href="ortho-k-lenses-for-myopia-control.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Ortho-K Lenses</a>
            <a href="myopia-control-atropine-eye-drops.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Atropine Eye Drops</a>
            <a href="myopia-control-multifocal-lenses.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Multifocal Lenses</a>
            <a href="myopia-control.html" class="block py-2 text-sm text-cvc-teal-600 font-medium">Learn About Myopia →</a>
          </div>
        </div>

        <!-- Eyewear Accordion -->
        <div class="mobile-accordion border-b border-gray-100">
          <button class="accordion-toggle w-full flex items-center justify-between py-3 text-gray-700 font-medium" data-target="mobile-eyewear">
            Eyewear
            <svg class="accordion-icon w-5 h-5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div id="mobile-eyewear" class="accordion-content hidden pb-3 pl-4 space-y-2">
            <a href="eyeglasses.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Eyeglasses</a>
            <a href="sunglasses.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Sunglasses</a>
            <a href="contact-lenses.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Contact Lenses</a>
            <a href="specialty-contact-lenses.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Specialty Contacts</a>
            <a href="eyewear.html" class="block py-2 text-sm text-cvc-teal-600 font-medium">Browse Eyewear →</a>
          </div>
        </div>

        <!-- Locations Accordion -->
        <div class="mobile-accordion border-b border-gray-100">
          <button class="accordion-toggle w-full flex items-center justify-between py-3 text-gray-700 font-medium" data-target="mobile-locations">
            Locations
            <svg class="accordion-icon w-5 h-5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div id="mobile-locations" class="accordion-content hidden pb-3 pl-4 space-y-2">
            <a href="eye-doctor-kennesaw-ga.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Kennesaw</a>
            <a href="east-cobb-eye-doctors.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">East Cobb / Marietta</a>
            <a href="our-locations.html" class="block py-2 text-sm text-cvc-teal-600 font-medium">All Locations →</a>
          </div>
        </div>

        <!-- About Accordion -->
        <div class="mobile-accordion border-b border-gray-100">
          <button class="accordion-toggle w-full flex items-center justify-between py-3 text-gray-700 font-medium" data-target="mobile-about">
            About
            <svg class="accordion-icon w-5 h-5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>
          <div id="mobile-about" class="accordion-content hidden pb-3 pl-4 space-y-2">
            <a href="our-doctors.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Our Doctors</a>
            <a href="dr-mital-patel-od.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500 pl-3">Dr. Mital Patel, OD</a>
            <a href="dr-bhumi-patel-od.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500 pl-3">Dr. Bhumi Patel, OD</a>
            <a href="new-patients.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">New Patients</a>
            <a href="insurance.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Insurance</a>
            <a href="contact.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Contact Us</a>
            <a href="careers.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Careers</a>
            <a href="blog.html" class="block py-2 text-sm text-gray-600 hover:text-cvc-teal-500">Blog</a>
            <a href="about-us.html" class="block py-2 text-sm text-cvc-teal-600 font-medium">About Us →</a>
          </div>
        </div>

        <!-- Phone Numbers -->
        <div class="pt-4 mt-2 border-t border-gray-200 space-y-3">
          <a href="tel:+17704992020" class="flex items-center gap-3 py-2 text-cvc-teal-600 font-medium">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
            </svg>
            Kennesaw: (770) 499-2020
          </a>
          <a href="tel:+17705098800" class="flex items-center gap-3 py-2 text-cvc-teal-600 font-medium">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
            </svg>
            East Cobb: (770) 509-8800
          </a>
          <a href="book-now.html" class="block w-full text-center bg-cvc-teal-500 text-white py-3 rounded font-medium mt-3">
            Book Appointment
          </a>
        </div>
      </div>
    </div>
  </header>'''

# Standard footer template
FOOTER_TEMPLATE = '''  <!-- Footer -->
  <footer class="bg-cvc-charcoal text-white pt-16 pb-8">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
        <!-- Brand Column -->
        <div>
          <a href="index.html" class="flex items-center gap-3 mb-6">
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

        <!-- Quick Links -->
        <div>
          <h3 class="font-semibold text-lg mb-5">Quick Links</h3>
          <ul class="space-y-3">
            <li><a href="eye-care-services.html" class="text-gray-400 hover:text-white transition-colors text-sm">Services</a></li>
            <li><a href="dry-eye-treatment.html" class="text-gray-400 hover:text-white transition-colors text-sm">Dry Eye Spa</a></li>
            <li><a href="myopia-control.html" class="text-gray-400 hover:text-white transition-colors text-sm">Myopia Control</a></li>
            <li><a href="eyewear.html" class="text-gray-400 hover:text-white transition-colors text-sm">Eyewear</a></li>
            <li><a href="our-doctors.html" class="text-gray-400 hover:text-white transition-colors text-sm">Our Doctors</a></li>
            <li><a href="insurance.html" class="text-gray-400 hover:text-white transition-colors text-sm">Insurance</a></li>
            <li><a href="new-patients.html" class="text-gray-400 hover:text-white transition-colors text-sm">New Patients</a></li>
            <li><a href="book-now.html" class="text-gray-400 hover:text-white transition-colors text-sm">Book Appointment</a></li>
          </ul>
        </div>

        <!-- Kennesaw Location -->
        <div>
          <h3 class="font-semibold text-lg mb-5">Kennesaw</h3>
          <address class="not-italic text-gray-400 text-sm space-y-2">
            <p>1615 Ridenour Blvd<br>Suite 201<br>Kennesaw, GA 30152</p>
            <p><a href="tel:+17704992020" class="hover:text-white transition-colors">(770) 499-2020</a></p>
            <p class="text-xs">Tue/Thu: 9:00am - 6:00pm<br>Wed/Fri: 8:00am - 5:00pm<br>Sat: 10:00am - 2:00pm</p>
          </address>
          <a href="eye-doctor-kennesaw-ga.html" class="inline-block mt-3 text-cvc-teal-500 hover:text-cvc-teal-400 text-sm font-medium">View Location →</a>
        </div>

        <!-- East Cobb Location -->
        <div>
          <h3 class="font-semibold text-lg mb-5">East Cobb</h3>
          <address class="not-italic text-gray-400 text-sm space-y-2">
            <p>3535 Roswell Rd<br>Suite 8<br>Marietta, GA 30062</p>
            <p><a href="tel:+16785608065" class="hover:text-white transition-colors">(678) 560-8065</a></p>
            <p class="text-xs">Tue/Thu: 9:00am - 6:00pm<br>Wed/Fri: 8:00am - 5:00pm<br>Mon/Sat/Sun: Closed</p>
          </address>
          <a href="east-cobb-eye-doctors.html" class="inline-block mt-3 text-cvc-teal-500 hover:text-cvc-teal-400 text-sm font-medium">View Location →</a>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="border-t border-white/10 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-gray-400 text-sm">&copy; 2026 Classic Vision Care. All rights reserved.</p>
        <div class="flex gap-6 text-sm">
          <a href="blog.html" class="text-gray-400 hover:text-white transition-colors">Blog</a>
          <a href="careers.html" class="text-gray-400 hover:text-white transition-colors">Careers</a>
          <a href="privacy-policy-2.html" class="text-gray-400 hover:text-white transition-colors">Privacy Policy</a>
          <a href="accessibility.html" class="text-gray-400 hover:text-white transition-colors">Accessibility</a>
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
      <a href="book-now.html" class="flex-1 flex items-center justify-center gap-2 bg-cvc-gold text-cvc-charcoal py-3 rounded font-medium text-sm">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        Book
      </a>
    </div>
  </div>

  <!-- Navigation Scripts -->
  <script>
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
      mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
      });
    }

    // Mobile accordion toggles
    const accordionToggles = document.querySelectorAll('.accordion-toggle');

    accordionToggles.forEach(toggle => {
      toggle.addEventListener('click', () => {
        const targetId = toggle.getAttribute('data-target');
        const content = document.getElementById(targetId);
        const icon = toggle.querySelector('.accordion-icon');

        // Close other accordions
        accordionToggles.forEach(otherToggle => {
          if (otherToggle !== toggle) {
            const otherId = otherToggle.getAttribute('data-target');
            const otherContent = document.getElementById(otherId);
            const otherIcon = otherToggle.querySelector('.accordion-icon');
            if (otherContent && !otherContent.classList.contains('hidden')) {
              otherContent.classList.add('hidden');
              otherIcon?.classList.remove('rotate-180');
            }
          }
        });

        // Toggle current accordion
        if (content) {
          content.classList.toggle('hidden');
          icon?.classList.toggle('rotate-180');
        }
      });
    });

    // Sticky header scroll effect
    const header = document.getElementById('header');
    if (header) {
      window.addEventListener('scroll', () => {
        if (window.pageYOffset > 50) {
          header.classList.add('shadow-md');
        } else {
          header.classList.remove('shadow-md');
        }
      });
    }
  </script>'''


def process_file(filepath):
    """Process a single HTML file to standardize navigation."""
    print(f"Processing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip index.html - it has custom hero and scripts that need to be preserved
    if filepath.name == 'index.html':
        print(f"  Skipping index.html (will process separately)")
        return False

    original_content = content

    # Pattern to match everything from start of body to start of main
    # This captures: <body...> [top bar] [header with nav] ... up to <main
    body_to_main_pattern = r'(<body[^>]*>)\s*(?:<!--[^>]*-->)?\s*(?:<div[^>]*bg-cvc-charcoal[^>]*>.*?</div>\s*)?(?:<header[^>]*>.*?</header>\s*)?(?=\s*<main)'

    # Check if file has the expected structure
    if '<main' in content and '</main>' in content:
        # Replace header section
        match = re.search(body_to_main_pattern, content, re.DOTALL)
        if match:
            body_tag = match.group(1)
            content = re.sub(body_to_main_pattern, body_tag + '\n' + NAV_TEMPLATE + '\n\n', content, flags=re.DOTALL)
        else:
            # Try simpler approach - find header and replace
            header_pattern = r'(<body[^>]*>)\s*(?:<!--[^>]*-->)?\s*<div[^>]*bg-cvc-charcoal[^>]*>.*?</div>\s*<header[^>]*>.*?</header>'
            match = re.search(header_pattern, content, re.DOTALL)
            if match:
                body_tag = match.group(1)
                content = re.sub(header_pattern, body_tag + '\n' + NAV_TEMPLATE, content, flags=re.DOTALL)

    # Replace footer section
    footer_pattern = r'<!--\s*Footer\s*-->\s*<footer[^>]*>.*?</footer>(?:\s*<!--[^>]*-->)?\s*(?:<div[^>]*fixed[^>]*bottom[^>]*>.*?</div>)?\s*(?:<script>.*?</script>)?\s*(?=</body>)'

    if re.search(footer_pattern, content, re.DOTALL):
        content = re.sub(footer_pattern, FOOTER_TEMPLATE + '\n', content, flags=re.DOTALL)
    else:
        # Try simpler footer pattern
        simple_footer_pattern = r'<footer[^>]*bg-cvc-charcoal[^>]*>.*?</footer>'
        if re.search(simple_footer_pattern, content, re.DOTALL):
            # Find position of footer and replace everything from footer to </body>
            footer_match = re.search(r'<footer[^>]*bg-cvc-charcoal[^>]*>', content)
            if footer_match:
                body_end = content.rfind('</body>')
                if body_end > footer_match.start():
                    content = content[:footer_match.start()] + FOOTER_TEMPLATE + '\n' + content[body_end:]

    # Write back if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filepath.name}")
        return True
    else:
        print(f"  No changes needed: {filepath.name}")
        return False


def main():
    print(f"Found {len(HTML_FILES)} HTML files to process")
    print("-" * 50)

    updated = 0
    for filepath in sorted(HTML_FILES):
        if process_file(filepath):
            updated += 1

    print("-" * 50)
    print(f"Updated {updated} of {len(HTML_FILES)} files")


if __name__ == "__main__":
    main()
