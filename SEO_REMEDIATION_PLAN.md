# SEO Remediation Plan: classicvisioncare.com

**Date:** 2026-02-22
**Site:** classicvisioncare.com (static site on Vercel, Tailwind CSS + vanilla JS)
**Analysis Method:** 3-agent ensemble (Codex/GPT-5.2, Gemini, Claude Code codebase scan)

---

## Guiding Principles

### Preserve the Information Architecture
The site has a **locked IA** defined in `URL_STRUCTURE.md` and `content/page_manifest.json`. All fixes
in this plan are **redirect-only changes in `vercel.json`** and `api/robots.js`. No HTML content
pages are modified -- the IA stays intact and page content is untouched.

### Do No Harm -- Universal Regression Guard
Every item in this plan carries the following **non-negotiable regression criteria** in addition to its item-specific success criteria. If any of these fail, the change must be reverted before proceeding:

1. **Existing redirects intact:** All 137+ existing redirects in `vercel.json` still function (spot-check 10 random redirects with `curl -sI`)
2. **No new 404s:** A crawl of all 510 sitemap URLs returns zero new `404` or `5xx` responses
3. **No new redirect chains:** The redirect chain detection script returns the same or fewer chains than before the change
4. **Canonical tags preserved:** Spot-check 5 pages -- canonical URLs unchanged and still return `200`
5. **Structured data intact:** Homepage, both location pages, and both doctor pages still pass Google Rich Results Test (or manual JSON-LD validation)
6. **Core Web Vitals stable:** Lighthouse Performance score on homepage does not drop below 85
7. **Forms functional:** Contact form on `/contact-us/` and booking widget on `/book-now/` still submit successfully
8. **No HTML content pages modified:** `git diff` shows zero changes to any `index.html` file in content directories
9. **robots.txt serves correctly:** `curl -s https://classicvisioncare.com/robots.txt` returns expected content (not a 404 or error page)
10. **Sitemap accessible:** `curl -sI https://classicvisioncare.com/sitemap.xml` returns `200` with valid XML

---

## Executive Summary

Three independent AI agents analyzed the classicvisioncare.com codebase. The site is in **strong technical health** overall -- 157 redirects properly handle legacy URLs, all pages are indexable (no noindex tags), canonical tags are correctly implemented, and no broken image/asset paths were detected. However, all three agents converged on the same set of actionable issues that should be fixed.

### Consensus Findings (All 3 Agents Agree)

| Finding | Codex | Gemini | Claude | Priority |
|---------|:-----:|:------:|:------:|:--------:|
| Redirect chain: miboflo -> mibo-thermoflo -> radio-frequency | Yes | Yes | Yes | P1 |
| Missing redirect: `/services/glaucoma` -> `/glaucoma/` | -- | Yes | Yes | P0 |
| Missing redirect: `/ipl-dry-eye-treatment/` -> IPL page | -- | Yes | Yes | P0 |
| Missing redirect: `/miboflo-treatment-dry-eye/` -> RF page | -- | Yes | Yes | P0 |
| robots.txt Googlebot override allows /api/ crawling | Yes | -- | Yes | P2 |
| Sitemap redundancy (sitemap.xml + sitemap-core.xml) | -- | Yes | Yes | P3 |
| CSP in Report-Only mode (not enforced) | -- | Yes | Yes | P3 |

---

## P0: Critical -- Add Missing Redirects

### 1. Add Redirects for Uncovered Legacy URLs

Three URLs referenced in content pages currently return **404** because no redirect exists for them.
The content pages are part of the locked IA and must NOT be edited. The fix is to add redirects
in `vercel.json` so these legacy paths resolve correctly.

#### 1a. `/services/glaucoma` -> `/glaucoma/`
- **Referenced by:** `glaucoma/8-troubling-signs-of-glaucoma/index.html`
- **Problem:** `/services/glaucoma` has no redirect and no page -- returns 404
- **Action:** Add to `vercel.json` redirects array:
  ```json
  { "source": "/services/glaucoma", "destination": "/glaucoma/", "permanent": true },
  { "source": "/services/glaucoma/", "destination": "/glaucoma/", "permanent": true }
  ```
- **Success criteria:**
  - `curl -sI https://classicvisioncare.com/services/glaucoma` returns `301` with `Location: /glaucoma/`
  - `curl -sI https://classicvisioncare.com/services/glaucoma/` returns `301` with `Location: /glaucoma/`
  - Final destination `/glaucoma/` returns `200`
  - No new redirect chain created (single hop only)
  - **Regression guard passes** (see Universal Regression Guard above)

#### 1b. `/ipl-dry-eye-treatment/` -> `/dry-eye-treatment-intense-pulsed-light/`
- **Referenced by:** `radio-frequency-treatment-dry-eye/index.html`
- **Problem:** `/ipl-dry-eye-treatment/` has no redirect and no page -- returns 404
- **Action:** Add to `vercel.json` redirects array:
  ```json
  { "source": "/ipl-dry-eye-treatment/", "destination": "/dry-eye-treatment-intense-pulsed-light/", "permanent": true },
  { "source": "/ipl-dry-eye-treatment", "destination": "/dry-eye-treatment-intense-pulsed-light/", "permanent": true }
  ```
- **Success criteria:**
  - `curl -sI https://classicvisioncare.com/ipl-dry-eye-treatment/` returns `301` with `Location: /dry-eye-treatment-intense-pulsed-light/`
  - Both with-slash and without-slash variants redirect correctly
  - Final destination `/dry-eye-treatment-intense-pulsed-light/` returns `200`
  - No new redirect chain created (single hop only)
  - **Regression guard passes** (see Universal Regression Guard above)

#### 1c. `/miboflo-treatment-dry-eye/` -> `/dry-eye-treatment-radio-frequency/`
- **Referenced by:** `radio-frequency-treatment-dry-eye/index.html`
- **Problem:** `/miboflo-treatment-dry-eye/` has no redirect and no page -- returns 404
- **Action:** Add to `vercel.json` redirects array:
  ```json
  { "source": "/miboflo-treatment-dry-eye/", "destination": "/dry-eye-treatment-radio-frequency/", "permanent": true },
  { "source": "/miboflo-treatment-dry-eye", "destination": "/dry-eye-treatment-radio-frequency/", "permanent": true }
  ```
- **Success criteria:**
  - `curl -sI https://classicvisioncare.com/miboflo-treatment-dry-eye/` returns `301` with `Location: /dry-eye-treatment-radio-frequency/`
  - Both with-slash and without-slash variants redirect correctly
  - Final destination `/dry-eye-treatment-radio-frequency/` returns `200`
  - No new redirect chain created (single hop only)
  - **Regression guard passes** (see Universal Regression Guard above)

---

## P1: High -- Flatten Redirect Chain

### 2. Flatten Redirect Chain (MiBoFlo)

**Current chain (3 hops):**
```
/eye-treatment/miboflo/
  -> /dry-eyes/what-is-mibo-thermoflo/
    -> /dry-eye-treatment-radio-frequency/
```

**Action:** In `vercel.json`, update the first redirect to point directly to the final destination:

```json
// BEFORE:
{ "source": "/eye-treatment/miboflo/", "destination": "/dry-eyes/what-is-mibo-thermoflo/", "permanent": true }

// AFTER:
{ "source": "/eye-treatment/miboflo/", "destination": "/dry-eye-treatment-radio-frequency/", "permanent": true }
```

**Why:** Redirect chains waste crawl budget and add latency. Google follows up to 10 hops but penalizes deep chains. Best practice: every redirect should point directly to the final destination.

**Success criteria:**
- `curl -sI https://classicvisioncare.com/eye-treatment/miboflo/` returns `301` with `Location: /dry-eye-treatment-radio-frequency/`
- Only **one** 301 hop between source and final `200` response (no intermediate redirect)
- Running the redirect chain detection script against `vercel.json` returns **zero** exact chains
- `/dry-eyes/what-is-mibo-thermoflo/` -> `/dry-eye-treatment-radio-frequency/` redirect still works independently for direct visitors
- **Regression guard passes** (see Universal Regression Guard above)

---

## P2: Medium -- Optimization

### 3. Fix robots.txt Googlebot Override

**Issue:** The robots.txt has separate `User-agent: Googlebot` and `User-agent: *` groups. Per Google's spec, the most specific user-agent group takes precedence. The Googlebot group only has `Allow: /` but **does NOT repeat** the `Disallow: /api/` and `Disallow: /partials/` rules from the wildcard group.

**Result:** Googlebot can technically crawl `/api/contact`, `/api/clinic`, and `/api/robots` endpoints, wasting crawl budget and risking indexation of JSON/API responses.

**Action:** In `api/robots.js`, add Disallow rules to the Googlebot section:

```
User-agent: Googlebot
Allow: /
Disallow: /api/
Disallow: /partials/
```

Apply the same fix to **Bingbot** and **Applebot** sections.

**Success criteria:**
- `curl -s https://classicvisioncare.com/robots.txt` output shows `Disallow: /api/` and `Disallow: /partials/` under every bot-specific section (Googlebot, Bingbot, Applebot)
- Google Search Console "Robots.txt Tester" confirms `/api/contact` is blocked for Googlebot
- No existing allowed pages (service pages, blog, etc.) are accidentally blocked
- Wildcard `User-agent: *` section remains unchanged
- **Regression guard passes** (see Universal Regression Guard above)

### 4. Verify Sitemap lastmod Dates

**Issue:** All 510 URLs in `sitemap.xml` share the same `<lastmod>2026-02-17</lastmod>` date. Google has stated that inaccurate lastmod dates reduce their trust in the sitemap signal.

**Action:** Either:
- (a) Automate lastmod to reflect actual file modification dates, OR
- (b) Remove `<lastmod>` entirely (Google will use its own crawl timestamps)

**Success criteria:**
- If (a): Each `<lastmod>` value in `sitemap.xml` reflects the actual `git log --format=%aI -1` date for that page's `index.html`
- If (b): No `<lastmod>` elements present in `sitemap.xml`; XML still validates against the sitemaps.org schema
- Sitemap URL count remains at 510 (no pages accidentally removed)
- `xmllint --schema` validates the sitemap against sitemaps.org XSD (or manual XML structure check)
- **Regression guard passes** (see Universal Regression Guard above)

### 5. Audit wp-content Redirect Behavior

**Issue:** The redirect `"/wp-content/uploads/:path*" -> "/"` sends old WordPress image URLs to the homepage. Google may interpret this as a soft 404.

**Action:** Change the destination to return a proper 410 (Gone) status, or simply remove the redirect and let Vercel return a natural 404. If keeping it, consider:
```json
{ "source": "/wp-content/uploads/:path*", "destination": "/", "statusCode": 410 }
```
*Note: Vercel redirects don't support 410 directly. Consider removing this redirect entirely to let natural 404s occur, which Google handles correctly.*

**Success criteria:**
- `curl -sI https://classicvisioncare.com/wp-content/uploads/2023/test.jpg` returns either `404` (if redirect removed) or `301` to a non-homepage destination
- Homepage (`/`) is NOT the redirect destination for any `/wp-content/` path
- No legitimate images on the live site are broken by the change (grep HTML for `/wp-content/` references -- expect zero)
- **Regression guard passes** (see Universal Regression Guard above)

---

## P3: Low -- Maintenance / Nice-to-Have

### 6. Consolidate Sitemaps

**Issue:** Two sitemaps are listed in robots.txt: `sitemap.xml` (510 URLs) and `sitemap-core.xml` (18 URLs). The core sitemap is a complete subset of the main sitemap.

**Action:** Remove `sitemap-core.xml` reference from `api/robots.js`. Keep `sitemap-core.xml` file for internal use but don't advertise it to search engines.

**Success criteria:**
- `curl -s https://classicvisioncare.com/robots.txt | grep -i sitemap` returns exactly one line: `Sitemap: https://classicvisioncare.com/sitemap.xml`
- `sitemap-core.xml` file still exists in repo (not deleted, just de-listed)
- Main `sitemap.xml` still contains all 510 URLs including the 18 core pages
- **Regression guard passes** (see Universal Regression Guard above)

### 7. Enforce Content Security Policy

**Issue:** CSP header is `Content-Security-Policy-Report-Only`, which logs violations but doesn't block anything.

**Action:** After confirming no legitimate resources are being blocked (check Vercel logs), promote to enforced `Content-Security-Policy`.

**Success criteria:**
- Response header `Content-Security-Policy` is present (not `Content-Security-Policy-Report-Only`)
- Google Fonts, Google Tag Manager, Google Analytics, Cloudflare Turnstile, and Google Maps embed all load without CSP violations
- No console errors related to CSP on homepage, contact page, or any page with embedded maps
- Lighthouse score does not regress
- **Regression guard passes** (see Universal Regression Guard above)

### 8. Clean Up Zombie Files

**Issue:** Some directories exist for pages that are now handled by redirects (e.g., `radio-frequency-treatment-dry-eye/`, `dry-eye-treatment-miboflo/`). These could cause confusion.

**Action:** Verify these aren't being served (redirects should take precedence in Vercel), then remove the directories to keep the workspace clean. **Do this carefully** -- verify redirect order/priority first.

**Success criteria:**
- Every deleted directory has a corresponding `vercel.json` redirect that handles the URL
- `curl -sI` for each deleted directory's URL still returns `301` (served by redirect, not filesystem)
- No 404s introduced -- all URLs previously served by these directories still resolve
- `sitemap.xml` does not reference any deleted directory's URL (or if it does, the URL still redirects correctly)
- **Regression guard passes** (see Universal Regression Guard above)

### 9. Ensure Trailing Slash Consistency in Internal Links

**Issue:** With `trailingSlash: true` in `vercel.json`, any internal link without a trailing slash triggers an extra 301 redirect. For example, `href="/contact-us"` causes: `/contact-us` -> `301` -> `/contact-us/`.

**Action:** Grep all HTML files for internal `href` values missing trailing slashes and fix them to include the trailing slash. This eliminates unnecessary redirect hops for every page visit.

**Success criteria:**
- `grep -rn 'href="/' *.html **/*.html` finds zero internal links missing a trailing slash (excluding file extensions like `.css`, `.js`, `.png`, `.xml`, `.ico`)
- No functional links broken by the change (spot-check 10 pages)
- Total redirect count on a full-site crawl decreases (fewer trailing-slash normalization 301s)
- **Regression guard passes** (see Universal Regression Guard above)

---

## What's Working Well (No Action Needed)

These areas were audited and found to be in excellent shape:

- **Canonical tags**: Correctly implemented on all pages
- **Structured data**: Advanced JSON-LD (MedicalWebPage, Physician, BreadcrumbList, LocalBusiness)
- **Meta descriptions**: Present on all pages
- **Social meta (OG tags)**: Complete on all pages
- **Security headers**: HSTS, X-Frame-Options, X-Content-Type-Options all properly configured
- **AI bot management**: Thoughtful allow/disallow strategy per bot
- **Image assets**: All referenced images exist and paths are correct
- **Font loading**: Preconnect + display=swap for Google Fonts
- **Form security**: Cloudflare Turnstile, honeypot fields, rate limiting
- **External links**: Proper `rel="noopener"` on all target="_blank" links

---

## Implementation Checklist

All changes are **redirect/config only** -- no HTML content pages are touched.

| # | Priority | Task | File | Success Criteria Summary |
|---|----------|------|------|------------------------|
| 1a | P0 | Add redirect `/services/glaucoma` -> `/glaucoma/` | `vercel.json` | curl returns 301 -> /glaucoma/ -> 200 |
| 1b | P0 | Add redirect `/ipl-dry-eye-treatment/` -> IPL page | `vercel.json` | curl returns 301 -> /dry-eye-treatment-intense-pulsed-light/ -> 200 |
| 1c | P0 | Add redirect `/miboflo-treatment-dry-eye/` -> RF page | `vercel.json` | curl returns 301 -> /dry-eye-treatment-radio-frequency/ -> 200 |
| 2 | P1 | Flatten miboflo redirect chain to single hop | `vercel.json` | Chain detection script returns zero chains |
| 3 | P2 | Add Disallow /api/ to Googlebot robots section | `api/robots.js` | robots.txt shows Disallow: /api/ under Googlebot |
| 4 | P2 | Fix sitemap lastmod dates | `sitemap.xml` | Per-page dates or no lastmod; still 510 URLs; valid XML |
| 5 | P2 | Audit wp-content redirect behavior | `vercel.json` | /wp-content/ paths return 404 (not 301 to homepage) |
| 6 | P3 | Remove sitemap-core.xml from robots | `api/robots.js` | robots.txt lists exactly 1 sitemap |
| 7 | P3 | Enforce CSP (remove Report-Only) | `vercel.json` | Enforced CSP header; no console errors on key pages |
| 8 | P3 | Clean up zombie directories | Multiple dirs | Deleted dirs still resolve via redirects; no new 404s |
| 9 | P3 | Fix trailing slash consistency | Multiple HTML | Zero internal hrefs missing trailing slash (excl. file extensions) |

---

## Agent-Specific Unique Insights

### Codex (GPT-5.2) -- Unique Findings
- Identified that the `Cross-Origin-Opener-Policy: same-origin` header could potentially interfere with Google Tag Manager popup/overlay functionality
- Noted that `/wp-content/uploads/:path*` -> `/` creates **soft 404 behavior** for old WordPress image URLs
- Confirmed zero duplicate redirect sources (no conflicting rules)

### Gemini -- Unique Findings
- Identified the specific broken links in content pages (the most actionable P0 findings)
- Verified canonical tag implementation across multiple page types
- Confirmed heading hierarchy (H1 -> H2 -> H3) is semantically correct
- Noted schema.org implementation quality is above average for a local practice site

### Claude Code (Codebase Scan) -- Unique Findings
- Complete inventory: 77 page directories, 510 sitemapped URLs, 138 HTML files, 157 redirects
- Verified all 510 sitemap URLs map to existing filesystem directories
- Confirmed no `<meta name="robots" content="noindex">` tags exist anywhere
- Documented all external link targets and their `rel` attributes
- Mapped the complete API endpoint structure and security configuration

---

*Generated by 3-agent ensemble: Codex (OpenAI GPT-5.2), Gemini (Google), Claude Code (Anthropic)*
