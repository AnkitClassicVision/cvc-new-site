/**
 * FOREST EDITORIAL INTERACTIVE EFFECTS
 * Classic Vision Care - Enhanced User Experience
 *
 * Features:
 * - Scroll progress bar
 * - Magnetic buttons
 * - 3D tilt cards
 * - Parallax effects
 * - Scroll reveal animations
 * - Line reveal animations
 * - Sticky header state
 */

(function() {
  'use strict';

  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  // Easing function for smooth animations
  const easeOutExpo = (t) => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

  /**
   * Initialize all effects when DOM is ready
   */
  document.addEventListener('DOMContentLoaded', () => {
    initScrollProgress();
    initScrollReveal();
    initStickyHeader();
    initLineReveal();

    // Only init motion effects if user hasn't requested reduced motion
    if (!prefersReducedMotion) {
      if (!isTouch) {
        initMagneticButtons();
        initTiltCards();
      }
      initParallax();
    }
  });

  /**
   * SCROLL PROGRESS BAR
   * Shows reading progress at top of page
   */
  function initScrollProgress() {
    // Create progress bar if it doesn't exist
    let progressBar = document.getElementById('scroll-progress');
    if (!progressBar) {
      progressBar = document.createElement('div');
      progressBar.id = 'scroll-progress';
      document.body.prepend(progressBar);
    }

    function updateProgress() {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      progressBar.style.width = `${Math.min(progress, 100)}%`;
    }

    // Throttled scroll handler
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          updateProgress();
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    // Initial call
    updateProgress();
  }

  /**
   * SCROLL REVEAL
   * Fade in elements as they enter viewport
   */
  function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal');

    if (!revealElements.length) return;

    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -80px 0px',
      threshold: 0.1
    };

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          // Optionally unobserve after reveal
          // revealObserver.unobserve(entry.target);
        }
      });
    }, observerOptions);

    revealElements.forEach(el => {
      revealObserver.observe(el);
    });
  }

  /**
   * STICKY HEADER
   * Add scrolled class when page is scrolled
   */
  function initStickyHeader() {
    const header = document.getElementById('header') || document.querySelector('.ef-header');
    if (!header) return;

    let lastScroll = 0;
    const scrollThreshold = 50;

    function updateHeader() {
      const currentScroll = window.pageYOffset;

      if (currentScroll > scrollThreshold) {
        header.classList.add('scrolled', 'header-scrolled');
      } else {
        header.classList.remove('scrolled', 'header-scrolled');
      }

      lastScroll = currentScroll;
    }

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          updateHeader();
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    // Initial check
    updateHeader();
  }

  /**
   * LINE REVEAL
   * Animate divider lines on scroll
   */
  function initLineReveal() {
    const lines = document.querySelectorAll('.ef-divider.animated, .line-reveal');

    if (!lines.length) return;

    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.5
    };

    const lineObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    }, observerOptions);

    lines.forEach(line => {
      lineObserver.observe(line);
    });
  }

  /**
   * MAGNETIC BUTTONS
   * Buttons follow cursor on hover
   */
  function initMagneticButtons() {
    const magneticElements = document.querySelectorAll('.magnetic, [data-magnetic]');

    magneticElements.forEach(element => {
      const strength = parseFloat(element.dataset.magneticStrength) || 0.3;

      element.addEventListener('mousemove', (e) => {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const deltaX = (e.clientX - centerX) * strength;
        const deltaY = (e.clientY - centerY) * strength;

        element.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
      });

      element.addEventListener('mouseleave', () => {
        element.style.transform = 'translate(0, 0)';
      });
    });
  }

  /**
   * 3D TILT CARDS
   * Cards tilt based on mouse position
   */
  function initTiltCards() {
    const tiltCards = document.querySelectorAll('.tilt-card, [data-tilt]');

    tiltCards.forEach(card => {
      const maxTilt = parseFloat(card.dataset.tiltMax) || 10;
      const perspective = parseFloat(card.dataset.tiltPerspective) || 1000;
      const scale = parseFloat(card.dataset.tiltScale) || 1.02;

      // Set perspective on parent or card itself
      card.style.perspective = `${perspective}px`;

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        // Calculate rotation based on cursor position
        const rotateX = ((e.clientY - centerY) / (rect.height / 2)) * -maxTilt;
        const rotateY = ((e.clientX - centerX) / (rect.width / 2)) * maxTilt;

        card.style.transform = `
          rotateX(${rotateX}deg)
          rotateY(${rotateY}deg)
          scale3d(${scale}, ${scale}, ${scale})
        `;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      });

      // Reset on scroll to prevent sticking
      card.addEventListener('wheel', () => {
        card.style.transform = 'rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      }, { passive: true });
    });
  }

  /**
   * PARALLAX EFFECTS
   * Elements move at different speeds on scroll
   */
  function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax, [data-parallax]');

    if (!parallaxElements.length) return;

    function updateParallax() {
      const scrollTop = window.pageYOffset;

      parallaxElements.forEach(element => {
        const speed = parseFloat(element.dataset.parallaxSpeed) || 0.1;
        const direction = element.dataset.parallaxDirection || 'vertical';
        const rect = element.getBoundingClientRect();

        // Only animate if element is in view
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          const yPos = scrollTop * speed;

          if (direction === 'horizontal') {
            element.style.transform = `translateX(${yPos}px)`;
          } else {
            element.style.transform = `translateY(${yPos}px)`;
          }
        }
      });
    }

    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          updateParallax();
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    // Initial call
    updateParallax();
  }

  /**
   * SPLIT TEXT ANIMATION
   * Animate text character by character
   */
  function splitText(element) {
    const text = element.textContent;
    element.innerHTML = '';

    text.split('').forEach((char, i) => {
      const span = document.createElement('span');
      span.textContent = char === ' ' ? '\u00A0' : char;
      span.style.display = 'inline-block';
      span.style.animationDelay = `${i * 0.03}s`;
      element.appendChild(span);
    });
  }

  // Expose utility functions globally if needed
  window.ForestEditorial = {
    splitText,
    initScrollReveal,
    initMagneticButtons,
    initTiltCards,
    initParallax
  };

})();

/**
 * MOBILE MENU HANDLER
 * Handles mobile navigation toggle
 */
document.addEventListener('DOMContentLoaded', () => {
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.contains('hidden');

      if (isOpen) {
        mobileMenu.classList.remove('hidden');
        mobileMenuBtn.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
      } else {
        mobileMenu.classList.add('hidden');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!mobileMenu.classList.contains('hidden') &&
          !mobileMenu.contains(e.target) &&
          !mobileMenuBtn.contains(e.target)) {
        mobileMenu.classList.add('hidden');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });

    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }

  // Mobile accordion for dropdowns
  const accordionToggles = document.querySelectorAll('[data-accordion-toggle]');

  accordionToggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
      const targetId = toggle.getAttribute('data-target');
      const content = document.getElementById(targetId);
      const icon = toggle.querySelector('.accordion-icon');

      if (content) {
        const isOpen = !content.classList.contains('hidden');

        // Close all other accordions
        accordionToggles.forEach(otherToggle => {
          if (otherToggle !== toggle) {
            const otherId = otherToggle.getAttribute('data-target');
            const otherContent = document.getElementById(otherId);
            const otherIcon = otherToggle.querySelector('.accordion-icon');

            if (otherContent && !otherContent.classList.contains('hidden')) {
              otherContent.classList.add('hidden');
              if (otherIcon) otherIcon.classList.remove('rotate-180');
            }
          }
        });

        // Toggle current accordion
        if (isOpen) {
          content.classList.add('hidden');
          if (icon) icon.classList.remove('rotate-180');
        } else {
          content.classList.remove('hidden');
          if (icon) icon.classList.add('rotate-180');
        }
      }
    });
  });
});

/**
 * DROPDOWN HOVER BEHAVIOR
 * Handles desktop dropdown menus
 */
document.addEventListener('DOMContentLoaded', () => {
  const dropdowns = document.querySelectorAll('.nav-dropdown');

  dropdowns.forEach(dropdown => {
    let timeout;

    dropdown.addEventListener('mouseenter', () => {
      clearTimeout(timeout);
      dropdown.querySelector('.dropdown-menu')?.classList.remove('invisible', 'opacity-0');
      dropdown.querySelector('.dropdown-menu')?.classList.add('visible', 'opacity-100');
    });

    dropdown.addEventListener('mouseleave', () => {
      timeout = setTimeout(() => {
        dropdown.querySelector('.dropdown-menu')?.classList.add('invisible', 'opacity-0');
        dropdown.querySelector('.dropdown-menu')?.classList.remove('visible', 'opacity-100');
      }, 150);
    });
  });
});

/**
 * SMOOTH ANCHOR SCROLLING
 * Smooth scroll to anchor links
 */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const headerOffset = 100;
        const elementPosition = target.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
});

/**
 * IMAGE ERROR HANDLER
 * Replaces broken images with elegant placeholders
 */
document.addEventListener('DOMContentLoaded', () => {
  const images = document.querySelectorAll('img');

  images.forEach(img => {
    img.addEventListener('error', function() {
      // Create placeholder container
      const placeholder = document.createElement('div');
      placeholder.className = 'img-placeholder';

      // Match the image's dimensions
      if (this.width) placeholder.style.width = this.width + 'px';
      if (this.height) placeholder.style.height = this.height + 'px';
      placeholder.style.minHeight = '200px';
      placeholder.style.aspectRatio = '4/3';
      placeholder.style.borderRadius = '0.75rem';

      // Determine placeholder type based on path
      const src = this.src.toLowerCase();
      if (src.includes('doctor') || src.includes('dr-')) {
        placeholder.classList.add('doctor-placeholder');
      } else if (src.includes('hero')) {
        placeholder.classList.add('hero-placeholder');
      } else if (src.includes('location')) {
        placeholder.classList.add('location-placeholder');
      } else {
        placeholder.classList.add('service-placeholder');
      }

      // Copy classes from original image
      const imgClasses = this.className.split(' ').filter(c => !c.includes('w-') && !c.includes('h-'));
      placeholder.classList.add(...imgClasses);

      // Replace the broken image
      this.parentNode.replaceChild(placeholder, this);
    });

    // Force check for already failed images
    if (img.complete && img.naturalHeight === 0) {
      img.dispatchEvent(new Event('error'));
    }
  });
});
