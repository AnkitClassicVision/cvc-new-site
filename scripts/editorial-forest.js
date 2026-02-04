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
    initAutoEnhancements();
    initHeroMediaEnhancements();
    initScrollProgress();
    initScrollReveal();
    initStickyHeader();
    initLineReveal();
    initActiveNav();
    initPageTransitions();
    initImageFadeIn();
    initPressFeedback();

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
   * AUTO ENHANCEMENTS
   * Applies lightweight classes/attributes so pages don’t need per-file edits.
   */
  function initAutoEnhancements() {
    // Mark primary buttons as pressable (works via CSS + touch JS)
    document.querySelectorAll('.btn-primary, .ef-cta, .ef-btn-outline, .mobile-cta-btn').forEach(el => {
      el.classList.add('ef-pressable');
    });
  }

  /**
   * HERO MEDIA ENHANCEMENTS
   * Adds subtle image reveal + continuous Ken Burns motion (without changing layout).
   */
  function initHeroMediaEnhancements() {
    if (prefersReducedMotion) return;
    if (document.documentElement.hasAttribute('data-ef-no-hero-auto')) return;

    const hero = findHeroSection();
    if (!hero) return;

    const heroImage = findHeroImage(hero);
    if (heroImage) {
      // Continuous, subtle motion on the hero image.
      heroImage.classList.add('ef-hero-kenburns');

      // Add reveal mask to the image wrapper (if it exists and is safe to decorate).
      const wrapper =
        heroImage.closest('.image-reveal') ||
        heroImage.closest('.overflow-hidden') ||
        heroImage.parentElement;

      if (wrapper && wrapper !== hero && hero.contains(wrapper)) {
        wrapper.classList.add('image-reveal');

        // Match wrapper radius to the image so the reveal mask looks “native”.
        try {
          const radius = window.getComputedStyle(heroImage).borderRadius;
          if (radius && radius !== '0px') wrapper.style.borderRadius = radius;
        } catch {
          // ignore
        }

        // Gentle scroll parallax for the hero media container.
        if (!isTouch) {
          wrapper.setAttribute('data-parallax', '');
          wrapper.dataset.parallaxSpeed = wrapper.dataset.parallaxSpeed || '0.06';
        }
      }
    }

    enhanceHeroCopy(hero);
  }

  function findHeroSection() {
    const explicit = document.querySelector('.hero-gradient');
    if (explicit) return explicit;

    const main = document.querySelector('main');
    if (!main) return null;

    const sections = Array.from(main.querySelectorAll(':scope > section'));
    for (const section of sections) {
      if (section.querySelector('h1')) return section;
    }

    return null;
  }

  function findHeroImage(hero) {
    const images = Array.from(hero.querySelectorAll('img'));
    for (const img of images) {
      const src = (img.getAttribute('src') || '').toLowerCase();
      if (!src) continue;
      if (src.includes('/logos/') || src.includes('logo')) continue;
      return img;
    }
    return null;
  }

  function enhanceHeroCopy(hero) {
    if (prefersReducedMotion) return;
    if (document.documentElement.hasAttribute('data-ef-no-hero-text')) return;

    const h1 = hero.querySelector('h1');
    if (!h1) return;

    // Find the “copy column” container around the H1.
    let copyRoot = h1.parentElement;
    while (copyRoot && copyRoot !== hero) {
      if (copyRoot.tagName === 'DIV') {
        const kids = Array.from(copyRoot.children).filter(el => el.tagName !== 'SCRIPT');
        // Heuristic: the column should have multiple blocks (eyebrow, h1, paragraph, CTA).
        if (kids.length >= 3) break;
      }
      copyRoot = copyRoot.parentElement;
    }
    if (!copyRoot || copyRoot === hero) copyRoot = h1.parentElement;

    const children = Array.from(copyRoot.children).filter(el => el.tagName !== 'SCRIPT');
    if (!children.length) return;

    let delay = 0.08;
    children.forEach((child) => {
      // Skip if element already opts into reveal/stagger.
      if (child.classList.contains('reveal') ||
          child.classList.contains('reveal-up') ||
          child.classList.contains('reveal-scale') ||
          child.classList.contains('stagger-children')) {
        if (!child.style.animationDelay) child.style.animationDelay = `${delay.toFixed(2)}s`;
        delay += 0.1;
        return;
      }

      child.classList.add('reveal');
      child.style.animationDelay = `${delay.toFixed(2)}s`;
      delay += 0.1;
    });
  }

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
    const revealElements = document.querySelectorAll('.reveal, .reveal-up, .reveal-scale, .stagger-children');

    if (!revealElements.length) return;

    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -80px 0px',
      threshold: 0.1
    };

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          entry.target.classList.add('active');
          // Unobserve after reveal for performance
          revealObserver.unobserve(entry.target);
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
   * ACTIVE NAV STATE
   * Adds aria-current + active styles based on current URL
   */
  function initActiveNav() {
    const header = document.getElementById('header');
    if (!header) return;

    const currentPath = normalizePath(window.location.pathname);

    const navLinks = header.querySelectorAll('a[href]');
    navLinks.forEach(link => {
      const href = link.getAttribute('href') || '';
      if (!href || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:')) return;

      let linkPath = '';
      try {
        const url = new URL(href, window.location.href);
        if (url.origin !== window.location.origin) return;
        linkPath = normalizePath(url.pathname);
      } catch {
        return;
      }

      const exactMatch = linkPath === currentPath;
      const isTopLevelTrigger = link.classList.contains('nav-link') && !link.closest('.dropdown-menu');
      const indexPrefixMatch = isTopLevelTrigger && linkPath.endsWith('/index.html') && currentPath.startsWith(linkPath.replace(/index\.html$/, ''));

      if (exactMatch || indexPrefixMatch) {
        link.setAttribute('aria-current', 'page');
        link.classList.add('is-active');
      }
    });

    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenu) {
      mobileMenu.querySelectorAll('a[href]').forEach(link => {
        const href = link.getAttribute('href') || '';
        if (!href || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:')) return;

        let linkPath = '';
        try {
          const url = new URL(href, window.location.href);
          if (url.origin !== window.location.origin) return;
          linkPath = normalizePath(url.pathname);
        } catch {
          return;
        }

        const exactMatch = linkPath === currentPath;

        if (exactMatch) {
          link.setAttribute('aria-current', 'page');
          link.classList.add('is-active');
        }
      });
    }
  }

  function normalizePath(pathname) {
    if (!pathname) return '/index.html';

    let normalized = pathname;
    if (!normalized.startsWith('/')) normalized = `/${normalized}`;

    if (normalized === '/') normalized = '/index.html';
    if (normalized.endsWith('/')) normalized = `${normalized}index.html`;

    return normalized;
  }

  /**
   * PAGE TRANSITIONS (subtle)
   * Adds a short fade/slide on internal navigation for a “premium” feel.
   */
  function initPageTransitions() {
    if (prefersReducedMotion) return;

    // Ensure we reset state on bfcache restores.
    window.addEventListener('pageshow', () => {
      document.documentElement.classList.remove('ef-page-leave');
    });

    document.addEventListener('click', (e) => {
      const link = e.target.closest && e.target.closest('a[href]');
      if (!link) return;

      // Respect default browser behaviors
      if (e.defaultPrevented) return;
      if (e.button !== 0) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if (link.target && link.target !== '_self') return;
      if (link.hasAttribute('download')) return;
      if (link.hasAttribute('data-no-transition')) return;

      const href = link.getAttribute('href') || '';
      if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;

      let url;
      try {
        url = new URL(link.href);
      } catch {
        return;
      }

      if (url.origin !== window.location.origin) return;

      // If only hash is changing on the same page, skip transition.
      const currentNoHash = window.location.href.split('#')[0];
      const targetNoHash = url.href.split('#')[0];
      if (currentNoHash === targetNoHash && url.hash) return;

      e.preventDefault();
      document.documentElement.classList.add('ef-page-leave');

      // Slight delay so the transition can be perceived.
      window.setTimeout(() => {
        window.location.href = url.href;
      }, 170);
    }, { capture: true });
  }

  /**
   * IMAGE FADE-IN
   * Smoothly fades in images that haven’t finished loading yet.
   */
  function initImageFadeIn() {
    const images = document.querySelectorAll('img');

    images.forEach(img => {
      // If already loaded, don’t force opacity flicker.
      if (img.complete && img.naturalHeight > 0) {
        img.classList.add('ef-img-loaded');
        return;
      }

      img.classList.add('ef-img-fade');

      img.addEventListener('load', () => {
        img.classList.add('ef-img-loaded');
      }, { once: true });

      img.addEventListener('error', () => {
        img.classList.remove('ef-img-fade');
      }, { once: true });
    });
  }

  /**
   * PRESS FEEDBACK
   * Adds tactile “press” feedback on touch devices.
   */
  function initPressFeedback() {
    if (!isTouch) return;

    const pressables = document.querySelectorAll('.ef-pressable');
    if (!pressables.length) return;

    pressables.forEach(el => {
      el.addEventListener('touchstart', () => {
        el.classList.add('is-pressed');
      }, { passive: true });

      el.addEventListener('touchend', () => {
        el.classList.remove('is-pressed');
      }, { passive: true });

      el.addEventListener('touchcancel', () => {
        el.classList.remove('is-pressed');
      }, { passive: true });
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
  const accordionToggles = document.querySelectorAll('[data-accordion-toggle], .accordion-toggle');

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
              otherToggle.setAttribute('aria-expanded', 'false');
            }
          }
        });

        // Toggle current accordion
        if (isOpen) {
          content.classList.add('hidden');
          if (icon) icon.classList.remove('rotate-180');
          toggle.setAttribute('aria-expanded', 'false');
        } else {
          content.classList.remove('hidden');
          if (icon) icon.classList.add('rotate-180');
          toggle.setAttribute('aria-expanded', 'true');
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
