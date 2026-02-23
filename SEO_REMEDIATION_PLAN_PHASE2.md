# SEO Remediation Plan Phase 2: classicvisioncare.com

**Date:** 2026-02-22
**Site:** classicvisioncare.com (static HTML + Tailwind CSS site on Vercel)
**Audit Score:** 61/100 (Grade D) — Target: 85+ (Grade B)
**Analysis Method:** 3-agent ensemble (Codex/GPT-5.2, Gemini, Claude Code codebase scan)

---

## Guiding Principles

### Preserve the Information Architecture
The site has a **locked IA** defined in `URL_STRUCTURE.md` and `content/page_manifest.json`. No pages are added or removed. Content meaning is preserved. Changes are limited to HTML attributes, image markup, JSON-LD data, and asset optimization.

### Do No Harm — Universal Regression Guard
Every item in this plan carries the following **non-negotiable regression criteria**. If any fail, the change must be reverted before proceeding:

1. **No new 404s:** Spot-check 10 key pages return 200
2. **Existing redirects intact:** 10 random redirects from vercel.json still function
3. **No new redirect chains:** Redirect chain count does not increase
4. **Canonical tags preserved:** 5 pages — canonical URLs unchanged, return 200
5. **Structured data intact:** Homepage + 2 blog pages pass JSON-LD validation
6. **Core Web Vitals stable:** Lighthouse Performance on homepage ≥ 85
7. **Forms functional:** Contact form on `/contact-us/` and booking on `/book-now/` still submit
8. **robots.txt serves correctly:** `curl -s https://classicvisioncare.com/robots.txt` returns expected content
9. **Sitemap accessible:** `curl -sI https://classicvisioncare.com/sitemap.xml` returns 200
10. **Visual appearance unchanged:** Pages render identically (no layout shifts, no broken images)

---

## Item 1: Fix Trailing-Slash Internal Links (P0 — Critical)

### Problem
99 pages have internal `href` values missing trailing slashes (e.g., `href="/blog"` instead of `href="/blog/"`). Since `vercel.json` has `trailingSlash: true`, each bare link triggers a **308 redirect**, wasting crawl budget and adding latency.

### Scope
- ~210 internal links across ~199 HTML files need trailing slashes added
- Affected pattern: `href="/path"` where path is an internal page directory (NOT a file)
- Mostly in legacy WordPress blog content (blog image links) and some navigation

### Implementation Approach
**Regex search-and-replace** across all `*/index.html` files:
- Match: `href="(/[a-zA-Z0-9\-_/]+)"` where the path does NOT end in `/`, does NOT contain a `.` (file extension), and is NOT a protocol link
- Replace: add trailing slash before any `#anchor` or `?query`
- **Exclude:** external links (`http`, `//`), protocol links (`tel:`, `mailto:`, `javascript:`), file paths (`.js`, `.css`, `.jpg`, `.png`, `.webp`, `.ico`, `.pdf`, `.xml`, `.txt`, `.woff2`), root path `/`, and paths already ending in `/`

### Edge Cases (All 3 Agents Agree)
| Edge Case | Rule |
|-----------|------|
| `href="/blog"` | → `href="/blog/"` |
| `href="/blog#section"` | → `href="/blog/#section"` |
| `href="/blog?s=term"` | → `href="/blog/?s=term"` |
| `href="/book-now/?location=kennesaw"` | Leave as-is (already has slash before `?`) |
| `href="/presbyopia/#sharpvision"` | Leave as-is (already has slash before `#`) |
| `href="/"` | Leave as-is (root path) |
| `href="/styles/tailwind.css"` | Leave as-is (file extension) |
| `href="/images/hero.jpg"` | Leave as-is (file extension) |
| `href="tel:+17704992020"` | Leave as-is (protocol) |
| `href="mailto:info@..."` | Leave as-is (protocol) |
| `href="https://external.com"` | Leave as-is (external) |

### Success Criteria
1. **Zero bare internal page links:** `grep -rn 'href="/' */index.html index.html | grep -vE '\.(js|css|jpg|jpeg|png|webp|ico|svg|pdf|xml|txt|woff2|mp4)' | grep -vE 'href="/(#|$|\?)' | grep -vE 'href="(tel:|mailto:|https?:|//|javascript:)' | grep -vE 'href="/[^"]*/"' | grep -vE 'href="/[^"]*\.[^"]*"'` returns **zero results**
2. **No double slashes introduced:** `grep -rn 'href="[^"]*//[^"]*"' */index.html | grep -v 'http'` returns zero results
3. **No trailing slashes on file paths:** `grep -rn 'href="[^"]*\.\(js\|css\|jpg\|png\)/"' */index.html` returns zero results
4. **Live verification:** `curl -sI https://classicvisioncare.com/blog/ | grep HTTP` returns `200` (no redirect)
5. **Redirect chain count drops:** Re-run squirrelscan → `links/redirect-chains` warning count drops from 198 to near 0
6. **Regression guard passes** (all 10 items above)

---

## Item 2: Optimize Oversized Hero Images (P0 — Critical)

### Problem
8 images exceed 200KB, with `about-us-hero.jpg` at 629KB. These are served as raw JPEGs despite **responsive WebP variants already existing** in `images/heroes/responsive/` and `images/heroes/webp/`. The HTML uses plain `<img>` tags pointing to the heavy JPGs.

### Scope
**Images to fix (sorted by size):**

| Image | JPG Size | WebP 1920w | WebP 1024w | WebP 640w | Used On |
|-------|----------|------------|------------|-----------|---------|
| about-us-hero.jpg | 629K | 197K | 62K | 31K | /, /about-us, /our-doctors, /why-choose-us |
| main-hero.jpg | 399K | 218K | 67K | 34K | / |
| why-choose-us.jpg | 399K | 218K | 67K | 34K | /why-choose-us |
| child-eye-exam.jpg | 242K | 140K | 66K | 31K | /childrens-eye-exam |
| pediatric-hero.jpg | 242K | 140K | 66K | 31K | /myopia-control, /pediatric-eye-care |
| school-screening.jpg | 242K | 140K | 66K | 31K | /school-vision-screening |
| eye-exam-header.jpg | 231K | N/A (143K webp) | N/A | N/A | /comprehensive-eye-exams, /contact-lens-exams, /diabetic-eye-exam |
| dry-eye-hero.jpg | 185K | 86K | 33K | 18K | /dry-eye-treatment |

### Implementation Approach
**Replace `<img>` tags with `<picture>` elements** using existing responsive WebP files:

```html
<!-- BEFORE -->
<img src="/images/heroes/about-us-hero.jpg" alt="..." class="..." width="1920" height="1080">

<!-- AFTER -->
<picture>
  <source type="image/webp"
    srcset="/images/heroes/responsive/about-us-hero-640w.webp 640w,
           /images/heroes/responsive/about-us-hero-1024w.webp 1024w,
           /images/heroes/responsive/about-us-hero-1920w.webp 1920w"
    sizes="100vw">
  <img src="/images/heroes/about-us-hero.jpg" alt="..." class="..." width="1920" height="1080">
</picture>
```

**Additional steps:**
- For `eye-exam-header.jpg`: Generate responsive WebP variants (640w, 1024w, 1920w) since only a single WebP exists
- For above-fold hero images: keep `fetchpriority="high"`, remove `loading="lazy"`
- For below-fold images: keep `loading="lazy"`
- Preserve all existing `alt`, `class`, `width`, `height` attributes on the `<img>` fallback

### Edge Cases
| Edge Case | Rule |
|-----------|------|
| LCP hero image (above fold) | `fetchpriority="high"`, NO `loading="lazy"` |
| Below-fold image | Keep `loading="lazy"` on `<img>` |
| CSS background-image | Not applicable (all heroes use `<img>` tags) |
| `eye-exam-header.jpg` | Generate responsive WebP variants first |
| Multiple pages share same image | Update ALL pages referencing that image |

### Success Criteria
1. **No image >200KB served:** All hero images load as WebP in Chrome DevTools Network tab, each <200KB
2. **`<picture>` elements present:** `grep -rn '<picture>' */index.html index.html | wc -l` shows all hero locations converted
3. **JPG fallback preserved:** Every `<picture>` still contains an `<img>` with `.jpg` src for Safari/legacy
4. **srcset has 3 sizes:** `grep -rn 'srcset=.*640w.*1024w.*1920w' */index.html` matches all hero images
5. **No broken images:** Visual spot-check of homepage, /about-us, /dry-eye-treatment, /comprehensive-eye-exams — all heroes render correctly
6. **LCP improvement:** Lighthouse LCP on homepage improves (target: <2.5s)
7. **CLS stable:** No new CLS from image dimension changes (width/height preserved)
8. **File sizes verified:**
   ```bash
   ls -lh images/heroes/responsive/*-1920w.webp  # All < 220K
   ls -lh images/heroes/responsive/*-1024w.webp  # All < 70K
   ls -lh images/heroes/responsive/*-640w.webp   # All < 35K
   ```
9. **Regression guard passes** (all 10 items above)

---

## Item 3: Fix Blog Image-Link Accessibility (P1 — High)

### Problem
23 pages have `<a>` tags wrapping `<img alt="">` with empty alt text. The links have no accessible name, violating **WCAG 2.1 AA SC 1.1.1** (Non-text Content) and **SC 2.4.4** (Link Purpose). Screen readers announce these as "link, image" with no context.

### Scope
**Affected files** (legacy WordPress blog content with image thumbnails as links):
- `blog/optometry-and-covid19-what-you-should-know/index.html` (6 image-links)
- `contact-lenses/am-i-a-candidate-for-contact-lenses/index.html` (6 image-links)
- `contact-lenses/contacts-vs-glasses-the-pros-and-cons/index.html` (7 image-links)
- `contact-lenses/how-to-safely-wear-colored-contact-lenses/index.html` (6 image-links)
- `contact-lenses/the-different-kinds-of-contact-lenses-and-what-to-expect/index.html` (6 image-links)
- `contact-lenses/the-symptoms-of-eye-infections-caused-by-contacts/index.html` (6 image-links)
- Plus ~17 more pages with similar patterns

### Current Pattern
```html
<p><a href="/blog/are-glasses-better-than-contacts" rel="noopener" target="_blank">
  <img alt="" class="aligncenter wp-image-2020 size-full" decoding="async"
       height="448" loading="lazy" src="/wp-content/uploads/2023/09/2439584.jpg"
       srcset="..." width="700"/>
</a></p>
```

### Implementation Approach (All 3 Agents Agree: Fix `alt` on `<img>`)
**Add descriptive `alt` text to the `<img>` tag** that describes the link destination. When an image is the only content inside a link, its `alt` text serves as the link's accessible name (per WCAG H30 technique).

```html
<!-- AFTER -->
<p><a href="/blog/are-glasses-better-than-contacts/" rel="noopener" target="_blank">
  <img alt="Read: Are Glasses Better Than Contacts?" class="aligncenter wp-image-2020 size-full"
       decoding="async" height="448" loading="lazy"
       src="/wp-content/uploads/2023/09/2439584.jpg"
       srcset="..." width="700"/>
</a></p>
```

**Rules for alt text:**
- Derive from the blog post title in the `href` path (slugify → title case)
- Prefix with "Read: " to indicate link purpose
- Keep under 125 characters
- Also fix the trailing slash on the href (ties to Item 1)

### Edge Cases
| Edge Case | Rule |
|-----------|------|
| Image is decorative but only link content | `alt` MUST be non-empty (WCAG H30) |
| Link has visible text alongside image | `alt=""` is OK if text provides the name |
| `target="_blank"` | Note in alt: not required per WCAG but good practice |
| Multiple images in same `<a>` | Only one needs descriptive alt, others can be `alt=""` |

### Success Criteria
1. **Zero empty-alt image-links:** `grep -rn '<a[^>]*><img[^>]*alt=""' */index.html` returns **zero results** for image-only links
2. **All alt texts are meaningful:** Manual review of 5 sample pages — alt text matches blog post title
3. **Alt text length OK:** No alt text exceeds 125 characters
4. **axe-core passes:** `a11y/aria-command-name` and `a11y/link-text` errors drop to 0
5. **Screen reader test:** Navigate with tab key through a sample blog page — each image-link announces its purpose
6. **No visual changes:** Images render identically (alt text is not visible)
7. **hrefs also get trailing slashes:** All `<a href>` values in these fixes also include trailing slashes (Item 1)
8. **Regression guard passes** (all 10 items above)

---

## Item 4: Fix JSON-LD Schema Errors (P1 — High)

### Problem
6 pages have invalid JSON-LD that prevents Google Rich Results:
- `Organization.logo` is an object `{@type: "ImageObject", url: "..."}` instead of a URL string (2 pages: `/about-us`, `/new-patients`)
- `WebPage.url` is missing (older legacy pages that use `@id` but omit `url`)
- `Article.publisher.name` and `Article.publisher.logo` are missing (blog articles use `publisher: {"@id": "..."}` reference but the referenced Organization doesn't always resolve inline)

### Scope
**Pages with `logo` as object (2 files):**
- `about-us/index.html` (line ~33)
- `pages/about/index.html` (line ~30) — source template

**Pages potentially missing `WebPage.url`:** Older service pages using multi-line JSON-LD with `@graph` where `WebPage` has `@id` but no explicit `url` property.

**Blog articles with publisher reference:** Most blog articles use `"publisher": {"@id": "https://classicvisioncare.com/#organization"}`. When the Organization node is included inline in the same `@graph` with `logo` as a string, this works. But on pages where Organization has `logo` as an object, it fails validation.

### Implementation Approach

**Fix 1: Organization.logo (2 pages)**
```json
// BEFORE (about-us/index.html)
"logo": {
  "@type": "ImageObject",
  "url": "https://classicvisioncare.com/images/logos/cropped-EOP1600_Classic_Logo_FN.png"
}

// AFTER
"logo": "https://classicvisioncare.com/images/logos/cropped-EOP1600_Classic_Logo_FN.png"
```

**Fix 2: Add `url` to WebPage nodes missing it**
Search all JSON-LD for `"@type": "WebPage"` nodes missing `"url"` property. Add `"url"` matching the canonical URL.

**Fix 3: Ensure Article publisher is resolvable**
For any blog article where `publisher` is a reference (`{"@id": "...#organization"}`), verify the Organization node in the same `@graph` has `name` and `logo` as a string. The blog articles already include the Organization inline — fixing the `logo` type in Fix 1 and ensuring consistency resolves this.

### Success Criteria
1. **No logo-as-object:** `grep -rn '"logo".*{' */index.html about-us/index.html | grep -v '@type.*Organization'` — specifically check `"logo": {` pattern returns 0 results in JSON-LD context
2. **All WebPage nodes have `url`:** Parse JSON-LD from the 6 flagged pages → every `WebPage` type has a `url` property
3. **Google Rich Results Test passes:** Submit these 6 URLs to Google Rich Results Test — all return "Page is eligible for rich results" or no errors
4. **Valid JSON syntax:** `python3 -c "import json; json.loads(open('about-us/index.html').read().split('application/ld+json\">')[1].split('</script>')[0])"` succeeds with no errors
5. **Squirrelscan `schema/json-ld-valid` errors drop from 6 to 0**
6. **No other schema changes:** `git diff` shows only the targeted JSON-LD properties changed
7. **Regression guard passes** (all 10 items above)

---

## Item 5: Fix Honeypot Field Accessibility (P1 — High)

### Problem
The anti-spam honeypot field `input#company_website` on 3 form pages is inside an `aria-hidden="true"` container but is still keyboard-focusable, has no label, and has no accessible name. This violates **WCAG SC 4.1.2** (Name, Role, Value) and triggers 3 squirrelscan errors.

### Scope
**3 files:**
- `book-now/index.html` (line ~785)
- `contact-us/index.html` (line ~1201)
- `our-locations/index.html`

### Current Pattern
```html
<div style="position:absolute;left:-9999px;top:-9999px;" aria-hidden="true">
  <input type="text" name="company_website" tabindex="-1" autocomplete="off">
</div>
```

### Implementation Approach (All 3 Agents Agree)
The field already has `tabindex="-1"` and `aria-hidden="true"` on the parent. The remaining issue is the **focusable element inside `aria-hidden`**. Fix by adding `aria-hidden="true"` directly to the input and an off-screen label:

```html
<div style="position:absolute;left:-9999px;top:-9999px;" aria-hidden="true">
  <label for="company_website" class="sr-only">Do not fill this field</label>
  <input type="text" name="company_website" id="company_website"
         tabindex="-1" autocomplete="off" aria-hidden="true">
</div>
```

**Key changes:**
1. Add `aria-hidden="true"` directly to the `<input>` element
2. Add `id="company_website"` to enable label association
3. Add a `<label>` with `class="sr-only"` (already exists in Tailwind) for completeness
4. Keep `tabindex="-1"` to prevent keyboard focus
5. Keep `autocomplete="off"` to prevent autofill

**Important:** The `id="company_website"` must be unique per page. Since each page has only one form, this is safe. If multiple forms exist, use `id="hp_company_website"` instead.

### Edge Cases
| Edge Case | Rule |
|-----------|------|
| `id` uniqueness | Verify only 1 form per page has this field |
| Spam bot detection still works | Field name `company_website` unchanged; position unchanged |
| Browser autofill | `autocomplete="off"` prevents accidental fill |
| Screen readers | `aria-hidden="true"` on both container and input removes from a11y tree |

### Success Criteria
1. **No focusable-in-aria-hidden errors:** `a11y/aria-hidden-focus` squirrelscan error count drops from 3 to 0
2. **No form-labels errors:** `a11y/form-labels` error count drops from 3 to 0
3. **No aria-input-field-name errors:** `a11y/aria-input-field-name` error count drops from 3 to 0
4. **Tab test:** On `/contact-us/`, pressing Tab through the form skips the honeypot completely
5. **Spam still caught:** Submit test form with `company_website` field filled → form rejects (or honeypot detection triggers)
6. **Spam still passes:** Submit test form with `company_website` field empty → form submits normally
7. **HTML valid:** No duplicate `id` attributes on any of the 3 pages
8. **Regression guard passes** (all 10 items above)

---

## Implementation Order

| Order | Item | Priority | Files Affected | Parallelizable? |
|-------|------|----------|----------------|-----------------|
| 1 | Item 5: Honeypot a11y | P1 | 3 files | Yes (independent) |
| 2 | Item 4: JSON-LD schema | P1 | 2-6 files | Yes (independent) |
| 3 | Item 1: Trailing slashes | P0 | ~199 files | No (bulk operation) |
| 4 | Item 3: Image-link a11y | P1 | ~23 files | Yes (after Item 1) |
| 5 | Item 2: Hero images | P0 | ~15 files + assets | No (needs verification) |

**Rationale:** Items 5 and 4 are small, surgical, and independent — do them first. Item 1 (trailing slashes) is the bulk operation that also benefits Item 3 (the hrefs in image-links need slashes too). Item 2 (images) is last because it involves asset generation and `<picture>` markup changes.

---

## Agent Consensus & Divergence

### Agreement (All 3 Agents)
- Trailing slash fix: regex on internal `href` values, exclude files/protocols/external
- Image optimization: use existing responsive WebP files with `<picture>` + `srcset`
- Blog image a11y: add descriptive `alt` to `<img>` (not `aria-label` on `<a>`)
- Honeypot: `tabindex="-1"` + `aria-hidden="true"` on input is the right approach
- JSON-LD: `Organization.logo` should be a plain URL string, not an ImageObject

### Unique Insights
- **Codex:** Found that responsive WebP files already exist but are unused — the fix is markup-only, no image generation needed (except `eye-exam-header`)
- **Gemini:** Recommended also adding `fetchpriority="high"` on LCP heroes and removing `loading="lazy"` from above-fold heroes
- **Claude Code:** Identified exact line numbers and confirmed only 2 pages have `logo` as object (not 6 — the other 4 errors are `WebPage.url` and `Article.publisher` issues)

### No Conflicts
All three agents agreed on approach for all 5 items. No reconciliation needed.

---

## Verification After All Items Complete

After all 5 items are implemented and individually verified:

1. **Re-run squirrelscan:** `squirrel audit https://classicvisioncare.com --refresh --format llm`
2. **Target score:** 75+ (from 61)
3. **Expected error reduction:** 186 → <50 errors
4. **Expected warning reduction:** 1359 → <900 warnings
5. **Key metrics to verify:**
   - `links/redirect-chains` → 0 (was 198)
   - `schema/json-ld-valid` → 0 errors (was 6)
   - `a11y/aria-hidden-focus` → 0 (was 3)
   - `a11y/aria-command-name` → 0 (was 23 pages)
   - `a11y/link-text` → 0 (was 23 pages)
   - `images/image-file-size` → 0 (was 8)
