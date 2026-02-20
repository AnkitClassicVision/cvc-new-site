# Classic Vision Care — Site Improvement Plan

**Date:** February 20, 2026
**Source:** `Local_Optometry_site_spec_action_plan.pdf` + PageSpeed Insights (mobile, Feb 20 2026)
**Site:** https://classicvisioncare.com

---

## Current Baseline

| Metric | Score | Status |
|--------|-------|--------|
| Performance (mobile) | **67** | Needs work |
| Accessibility | **97** | Good |
| Best Practices | **92** | Good |
| SEO | **100** | Perfect |

### Core Web Vitals (Field Data — Chrome UX Report)

| Metric | Value | Assessment |
|--------|-------|------------|
| LCP | 2.2s | Passed |
| FCP | 2.0s | Good |
| INP | N/A | Not enough data |
| CLS | 0 | Passed |

### Lab Data (Simulated Moto G Power, Slow 4G)

| Metric | Value | Target |
|--------|-------|--------|
| First Contentful Paint | 3.8s | < 1.8s |
| Largest Contentful Paint | 5.7s | < 2.5s |
| Total Blocking Time | 100ms | < 200ms |
| Speed Index | 5.3s | < 3.4s |
| Cumulative Layout Shift | 0 | < 0.1 |

---

## Spec Audit Summary (PDF Action Plan vs Current Site)

| Spec Item | Status | Notes |
|-----------|--------|-------|
| 1. /llms.txt at site root | DONE | Complete with NAP, hours, services, doctors, insurance, privacy. robots.txt references it. .well-known rewrite configured. |
| 2. AI Profile page + footer link | MISSING | /ai-profile/ does not exist. Not in footer. |
| 3. FAQ-first H2s on service pages | PARTIAL | 5 of 7 service pages use question-style H2s. contact-lens-exams, dry-eye-treatment, specialty-contact-lenses use descriptive H2s. All 7 have FAQPage schema. |
| 4. TOC for pages >= 2000 words | MISSING | 6 pages exceed 2000 words with no TOC. |
| 5. YMYL safety guardrails | DONE | Medical disclaimers on 25+ health pages. |
| 6. IndexNow integration | MISSING | No key file, no code, no integration. |
| 7. Footer links (general) | DONE | All major sections linked. Only missing AI Profile (page doesn't exist). |
| 8. Monitoring / KPIs | NOT ASSESSED | No dashboards or alerting reviewed. |

---

## Work Items

### M1 — AI Discoverability (from spec)

#### Item 1.1: Create AI Profile Page [P0]

**Description:** Build a canonical `/ai-profile/` page for AI citation that covers clinic identity, clinical team, services, patient guidance, safety disclaimer, and booking.

**Deliverables:**
- `ai-profile/index.html` — Full AI Profile page following the spec's 6-section structure
- Footer link to `/ai-profile/` added in `partials/footer.html`
- Organization schema on the page referencing `#organization`

**Success Criteria:**
- [x] `/ai-profile/` returns HTTP 200
- [x] Page contains: clinic name, both addresses, phone numbers, hours
- [x] Page contains: doctor names + credentials (Dr. Mital Patel OD, Dr. Bhumi Patel OD)
- [x] Page contains: services list matching service pages
- [x] Page contains: patient guidance (what to bring, insurance basics, booking steps)
- [x] Page contains: medical disclaimer ("This page is for informational purposes only...")
- [x] Page contains: direct booking link + phone numbers
- [x] Footer includes "AI Profile" link pointing to `/ai-profile/`
- [x] NAP is consistent with Google Business Profile
- [x] `llms.txt` updated to include `/ai-profile/` link

---

#### Item 1.2: Update llms.txt with AI Profile Link [P0]

**Description:** Add the new `/ai-profile/` page to the "Start here" section of llms.txt.

**Deliverables:**
- Updated `llms.txt` with AI Profile link

**Success Criteria:**
- [x] llms.txt "Start here" section includes `[AI Profile](https://classicvisioncare.com/ai-profile/)`
- [x] File validates as UTF-8 and returns HTTP 200

---

### M2 — Patient-Intent Content (from spec)

#### Item 2.1: Convert Remaining Service Pages to Question-Style H2s [P1]

**Description:** Three service pages still use descriptive H2 headings instead of question-style. Convert them to match the pattern used on the other 5 service pages.

**Pages to update:**
1. `contact-lens-exams/index.html`
2. `dry-eye-treatment/index.html`
3. `specialty-contact-lenses/index.html`

**Deliverables:**
- Rewritten H2 headings as natural patient questions on all 3 pages
- Existing FAQPage schema preserved and updated to match new headings

**Success Criteria:**
- [x] All 7 service pages use question-style H2s (e.g., "What Happens During a Contact Lens Exam?" not "The Exam Process")
- [x] H2s feel natural and match patient search queries
- [x] FAQPage schema remains valid (Google Rich Results Test passes)
- [x] No content meaning is lost — only heading phrasing changes

---

#### Item 2.2: Add Table of Contents to Long Pages [P1]

**Description:** Pages with 2000+ words need an auto-style TOC after the intro paragraph to improve navigation and SEO.

**Pages needing TOC (6):**

| Page | Word Count |
|------|-----------|
| `blog/index.html` | 3,534 |
| `comprehensive-eye-exams/index.html` | 2,227 |
| `blog/a-parents-guide-to-myopia-progression/index.html` | 2,133 |
| `myopia-control/index.html` | 2,082 |
| `ocular-rosacea/all-about-ocular-rosacea/index.html` | 2,043 |
| `radio-frequency-treatment-dry-eye/index.html` | 2,008 |

**Deliverables:**
- TOC `<nav>` block inserted after first `<p>` on each page
- Anchor `id` attributes added to each H2 on the page
- Minimal CSS (already Tailwind-based, use utility classes)

**Success Criteria:**
- [x] All 6 pages have a visible TOC after the intro
- [x] TOC links use anchor hrefs (`#section-name`) that scroll to correct H2
- [x] TOC uses semantic `<nav aria-label="Table of contents">` with `<ol>`
- [x] Blog index page is excluded (it's a listing page, not long-form content) — adjust to 5 pages
- [x] No layout shift introduced by the TOC

---

### M3 — Safety + Trust (from spec)

#### Item 3.1: YMYL Content Review Process Documentation [P2]

**Description:** The site has medical disclaimers (DONE), but the spec calls for a documented review workflow and citations policy for new medical content.

**Deliverables:**
- `docs/ymyl-content-policy.md` — Written policy for medical content creation
- Checklist template for clinician sign-off on new health pages

**Success Criteria:**
- [x] Policy document covers: no diagnosis language, no guaranteed outcomes, clinician review loop, citation requirements (AAO/CDC/NIH preferred)
- [x] Checklist exists for content review before publishing health pages
- [x] Existing disclaimers on 25+ pages remain intact

---

### M4 — Indexing + Ops (from spec)

#### Item 4.1: Implement IndexNow Integration [P1]

**Description:** Add IndexNow support so new/updated pages are instantly submitted to Bing and participating engines.

**Deliverables:**
- IndexNow API key file at site root (e.g., `<KEY>.txt`)
- `scripts/indexnow-submit.py` — Script to submit URLs to IndexNow endpoint
- Vercel config updated to serve the key file

**Success Criteria:**
- [x] IndexNow key file returns HTTP 200 at `https://classicvisioncare.com/<KEY>.txt`
- [x] Script successfully submits a URL and gets 200/202 response from `api.indexnow.org`
- [x] `robots.txt` or sitemap references are not affected
- [x] Script can be called manually or integrated into deploy pipeline

---

### P — Performance Improvements (from PageSpeed Insights)

> **Goal:** Raise mobile Performance score from 67 to 85+ without breaking existing functionality.
> **Constraint:** All changes must be safe, reversible, and testable. No framework rewrites.

#### Item P.1: Eliminate Render-Blocking CSS [HIGH IMPACT]

**Description:** `tailwind.css` (30KB) loads synchronously in `<head>`, blocking first paint. The site also loads `editorial-forest.css` (69KB). Together these are ~99KB of render-blocking CSS.

**Deliverables:**
- Critical CSS inlined in `<style>` tag in `<head>` (above-the-fold styles only, ~5-10KB)
- Remaining CSS loaded with `media="print" onload="this.media='all'"` pattern
- Fallback `<noscript>` link for non-JS browsers

**Success Criteria:**
- [ ] FCP improves (target: < 2.5s lab, currently 3.8s)
- [ ] No visible flash of unstyled content (FOUC)
- [ ] All pages render identically before and after
- [ ] `<noscript>` fallback preserves styling for non-JS users

---

#### Item P.2: Defer Non-Critical JavaScript [HIGH IMPACT]

**Description:** `editorial-forest.js` (32KB) loads in `<head>` or early `<body>`. Moving it to `defer` or loading it after DOMContentLoaded will reduce TBT and improve FCP.

**Deliverables:**
- Add `defer` attribute to `editorial-forest.js` `<script>` tag across all pages
- Verify `forms.js` and `tracking.js` also use `defer` or load at end of body

**Success Criteria:**
- [x] All `<script>` tags in `<head>` use `defer` or `async` (except inline critical scripts)
- [x] TBT stays at or below 100ms
- [x] Mobile menu, forms, and tracking all still function correctly
- [x] No console errors introduced

---

#### Item P.3: Reduce Unused JavaScript [MEDIUM IMPACT — 117 KiB savings]

**Description:** PageSpeed flags 117 KiB of unused JS. Likely from Google Tag Manager, third-party scripts, or unused portions of editorial-forest.js.

**Deliverables:**
- Audit `editorial-forest.js` for dead code (unused functions, event listeners for elements that don't exist on most pages)
- Lazy-load GTM after user interaction (scroll/click) instead of on page load
- Split page-specific JS out of the monolithic file if savings > 20KB

**Success Criteria:**
- [ ] Unused JS reduced by at least 50 KiB
- [ ] GTM fires correctly (verify in GA4 real-time)
- [ ] No features broken (mobile menu, forms, smooth scroll, dropdowns)
- [ ] editorial-forest.js size reduced or code-split

---

#### Item P.4: Reduce Unused CSS [MEDIUM IMPACT — 14 KiB savings]

**Description:** 14 KiB of CSS is unused on any given page. Tailwind purge may not be fully configured, or editorial-forest.css contains styles for components not on every page.

**Deliverables:**
- Verify Tailwind purge/content config covers all HTML files
- Rebuild tailwind.css with proper purge to eliminate dead selectors
- Audit editorial-forest.css for unused rules

**Success Criteria:**
- [ ] tailwind.css size reduced (currently 30KB, target < 20KB)
- [ ] No visual regressions on any page
- [ ] CSS coverage in DevTools shows < 10% unused on homepage

---

#### Item P.5: Optimize Image Delivery [MEDIUM IMPACT — 133 KiB savings]

**Description:** PageSpeed flags 133 KiB of image savings. Some images may not be properly sized for mobile viewport, or could use better compression.

**Deliverables:**
- Audit hero images on homepage for mobile sizing (currently 1376x768 generated WebP served to all viewports)
- Add `<picture>` with `srcset` for hero images serving 640w/1024w/1920w variants
- Compress any images over 200KB
- Ensure all above-fold images do NOT have `loading="lazy"` (remove it)
- Ensure all below-fold images DO have `loading="lazy"`

**Success Criteria:**
- [x] Hero images use responsive `srcset` serving appropriate size per viewport
- [x] No above-fold images have `loading="lazy"`
- [x] All below-fold images have `loading="lazy"`
- [ ] Total image transfer for homepage mobile < 300KB
- [ ] LCP improves (target: < 4.0s lab, currently 5.7s)

---

#### Item P.6: Fix Forced Reflow / Long Main-Thread Tasks [LOW IMPACT]

**Description:** 2 long tasks detected. Likely from layout recalculations triggered by JS reading layout properties then writing to the DOM.

**Deliverables:**
- Profile homepage with Chrome DevTools Performance tab
- Identify and batch DOM read/write operations in editorial-forest.js
- Use `requestAnimationFrame` for layout-triggering operations

**Success Criteria:**
- [ ] No main-thread tasks > 50ms on homepage load
- [ ] TBT stays at or below 100ms
- [ ] No visual jank during page load

---

#### Item P.7: Preconnect to Third-Party Origins [LOW IMPACT]

**Description:** Third-party scripts (GTM, Google Fonts if used, analytics) require DNS + TLS handshakes that delay loading.

**Deliverables:**
- Add `<link rel="preconnect">` for all third-party origins in `<head>`
- Add `<link rel="dns-prefetch">` as fallback

**Success Criteria:**
- [x] `preconnect` tags present for: `https://www.googletagmanager.com`, `https://www.google-analytics.com`, and any other third-party origins
- [x] No duplicate preconnect tags
- [ ] FCP improves by ~100-200ms

---

### A — Accessibility Fixes (from PageSpeed)

#### Item A.1: Fix Color Contrast Ratios [P1]

**Description:** Some text/background color combinations don't meet WCAG 2.1 AA contrast ratio of 4.5:1.

**Deliverables:**
- Identify all failing elements from Lighthouse audit
- Adjust text or background colors to meet 4.5:1 ratio
- Update Tailwind color classes or custom CSS

**Success Criteria:**
- [x] Lighthouse accessibility contrast audit passes
- [x] All text meets WCAG 2.1 AA minimum contrast (4.5:1 normal text, 3:1 large text)
- [x] Visual design intent preserved (colors stay on-brand)

---

#### Item A.2: Fix ARIA Roles on Incompatible Elements [P2]

**Description:** Some elements use ARIA roles that conflict with their native HTML semantics.

**Deliverables:**
- Identify and fix all ARIA role misuse flagged by Lighthouse
- Remove redundant ARIA roles where native HTML semantics suffice

**Success Criteria:**
- [x] Lighthouse "Uses ARIA roles only on compatible elements" passes
- [x] No redundant ARIA roles on native semantic elements

---

#### Item A.3: Differentiate Identical Links [P2]

**Description:** Multiple links with identical text point to different destinations, confusing screen readers.

**Deliverables:**
- Add `aria-label` or visually hidden text to differentiate identical link text
- Example: two "Book Now" links should specify which location

**Success Criteria:**
- [x] Lighthouse "Identical links have the same purpose" passes
- [x] Screen reader users can distinguish between similarly-named links

---

### B — Best Practices Fixes (from PageSpeed)

#### Item B.1: Fix Images with Incorrect Aspect Ratio [P1]

**Description:** Some images are displayed at a different aspect ratio than their natural dimensions, causing distortion.

**Deliverables:**
- Identify all images flagged by Lighthouse
- Fix `width`/`height` attributes or CSS to match natural aspect ratio
- Use `object-fit: cover` where cropping is intentional

**Success Criteria:**
- [x] Lighthouse "Displays images with incorrect aspect ratio" passes
- [x] No visually distorted images on any page

---

#### Item B.2: Fix Console Errors [P2]

**Description:** Browser errors logged to console indicate broken functionality or missing resources.

**Deliverables:**
- Identify all console errors on homepage load
- Fix broken resource references, JS errors, or missing files

**Success Criteria:**
- [x] Zero errors in browser console on homepage load
- [x] Zero errors on service pages and booking page

---

#### Item B.3: Add Security Headers [P2]

**Description:** Missing security headers flagged: CSP, HSTS, COOP, Trusted Types. These are Vercel configuration items.

**Deliverables:**
- Add headers in `vercel.json`:
  - `Content-Security-Policy` (report-only first, then enforce)
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
  - `Cross-Origin-Opener-Policy: same-origin`

**Success Criteria:**
- [x] HSTS header present on all responses
- [x] CSP header present (at minimum report-only mode)
- [x] COOP header present
- [x] No functionality broken by new headers
- [ ] Best Practices score improves to 100

---

## Priority Matrix

| Priority | Items | Impact |
|----------|-------|--------|
| **P0 — Must Do** | 1.1 (AI Profile), 1.2 (llms.txt update) | AI discoverability, spec compliance |
| **P1 — High** | P.1 (Render-blocking CSS), P.2 (Defer JS), P.5 (Image delivery), 2.1 (Question H2s), 2.2 (TOC), 4.1 (IndexNow), A.1 (Contrast) | Performance score 67 → 85+, patient intent |
| **P2 — Medium** | P.3 (Unused JS), P.4 (Unused CSS), B.1 (Aspect ratio), B.2 (Console errors), B.3 (Security headers), A.2 (ARIA), A.3 (Identical links), 3.1 (YMYL policy) | Polish, best practices |
| **P3 — Low** | P.6 (Forced reflow), P.7 (Preconnect) | Marginal gains |

---

## Recommended Execution Order

1. **P.1 + P.2** — CSS/JS loading (biggest FCP/LCP improvement, low risk)
2. **P.5** — Image delivery optimization (LCP improvement)
3. **1.1 + 1.2** — AI Profile page + llms.txt update
4. **2.1 + 2.2** — Question H2s + TOC on long pages
5. **4.1** — IndexNow integration
6. **A.1** — Contrast fixes
7. **P.3 + P.4** — Unused JS/CSS cleanup
8. **B.1 + B.2 + B.3** — Best practices fixes
9. **A.2 + A.3** — ARIA and link accessibility
10. **3.1** — YMYL policy documentation
11. **P.6 + P.7** — Reflow and preconnect (if time permits)

---

## Verification (after all items)

- [ ] PageSpeed mobile Performance >= 85
- [ ] PageSpeed Accessibility >= 97 (maintain or improve)
- [ ] PageSpeed Best Practices >= 95
- [ ] PageSpeed SEO stays at 100
- [ ] Core Web Vitals (field data) all green
- [ ] All pages render correctly on mobile and desktop
- [ ] Forms (contact, booking, locations) still submit successfully
- [ ] GTM/GA4 tracking still fires
- [ ] Google Rich Results Test passes on homepage + 1 service page + 1 doctor page
- [ ] `curl /llms.txt` returns 200 with updated AI Profile link
- [ ] `/ai-profile/` returns 200 and is linked in footer
