# Google Search Console Fix Plan — classicvisioncare.com

**Generated:** 2026-02-26
**Data Range:** 2026-01-29 to 2026-02-26
**Total:** 846 clicks | 181,669 impressions | 0.5% CTR | avg position 12.6

---

## Executive Summary

The site has **846 clicks from 181K impressions** (0.5% CTR). Top issues from GSC:
1. **54 non-blog pages have WRONG breadcrumb schema** pointing to `/blog/` instead of their real parent (CRITICAL)
2. **All 8 old WordPress category URLs return 404** (indexed in Google, no redirects)
3. **Old `?page_id=` query parameters serve duplicate homepage** (200 instead of redirect)
4. **Sitemaps show 0 indexed URLs** despite being submitted
5. **Redirect error on `/ocular-rosacea`** (top page — 220 clicks/25K impressions)
6. **Massive CTR problem** on high-impression pages (many pages with 1K+ impressions and 0% CTR)
7. **6 service pages use inconsistent breadcrumb parent** ("Eye Care Services" vs "Services")
8. **`www.classicvisioncare.com` old URLs still appearing** in search results

---

## FIX 0: Breadcrumb Schema & Visible Breadcrumb Errors (CRITICAL — 54 pages)

**Problem:** 54 non-blog article pages have their BreadcrumbList schema AND visible breadcrumb HTML pointing to `/blog/` ("Resources") as the parent. These pages live under service directories (`/dry-eyes/`, `/eye-treatment/`, `/eye-care/`, `/glasses/`, `/contact-lenses/`, `/glaucoma/`, `/myopia/`, `/ocular-rosacea/`) but Google thinks they're blog posts.

This includes the **#1 traffic page** (ocular rosacea: 220 clicks, 25K impressions) and the **#2 traffic page** (eye pain: 157 clicks, 59K impressions).

**Pages affected (54 total, grouped by parent directory):**

| Parent Directory | Count | Correct Breadcrumb Parent | Current (WRONG) |
|-----------------|-------|--------------------------|-----------------|
| `contact-lenses/` | 5 | Home > Contact Lenses > [Title] | Home > Resources > [Title] |
| `dry-eyes/` | 10 | Home > Dry Eye > [Title] | Home > Resources > [Title] |
| `eye-care/` | 12 | Home > Eye Care > [Title] | Home > Resources > [Title] |
| `eye-treatment/` | 14 | Home > Eye Treatment > [Title] | Home > Resources > [Title] |
| `glasses/` | 9 | Home > Glasses > [Title] | Home > Resources > [Title] |
| `glaucoma/` | 3 | Home > Glaucoma > [Title] | Home > Resources > [Title] |
| `myopia/` | 1 | Home > Myopia Control > [Title] | Home > Resources > [Title] |
| `ocular-rosacea/` | 1 | Home > Eye Conditions > [Title] | Home > Resources > [Title] |

**What's wrong on each page (example: ocular-rosacea):**

1. **Visible breadcrumb HTML** (line ~495): Shows `Home > Resources` with link to `/blog/`
2. **Schema BreadcrumbList** (in ld+json): `position 2: "Resources" → /blog/`
3. **Both need to change** to reflect actual site hierarchy

**Fix:** For each of the 54 pages, update:
1. The `<nav aria-label="Breadcrumb">` visible HTML — change parent link from `/blog/` to the correct service parent
2. The `BreadcrumbList` in `<script type="application/ld+json">` — change position 2 name and URL

**Additional breadcrumb sub-issue — 6 pages use inconsistent parent name:**
These service pages use "Eye Care Services" instead of "Services" as the breadcrumb parent:
- `blepharitis/`, `computer-eye-strain/`, `eye-infections/`, `pediatric-eye-exams/`, `school-vision-screening/`, `specialty-contact-lenses/`

Should be standardized to match the majority pattern ("Services" linking to `/eye-care-services/`).

**Risk:** LOW — HTML content changes only, no routing or config changes. BUT this is a large number of files (54+6 = 60 files).

---

## FIX 1: Category Pages Returning 404 (CRITICAL)

**Problem:** All old WordPress `/category/*` URLs return 404. Google has them indexed and they're wasting crawl budget.

**URLs affected (from GSC data):**
| URL | Impressions | Status |
|-----|-------------|--------|
| `/category/blog/` | 18 | 404 → Indexed! |
| `/category/childrens-eye-care/` | 5 | 404 |
| `/category/contact-lenses/` | 5 | 404 |
| `/category/dry-eye/` | 1 | 404 |
| `/category/eye-care/` | 3 | 404 |
| `/category/eye-health/` | 5 | 404 |
| `/category/glasses/` | 10 | 404 |
| `/category/myopia/` | 1 | 404 |

**Fix:** Add 301 redirects in `vercel.json`:
```json
{ "source": "/category/blog/", "destination": "/blog/", "permanent": true },
{ "source": "/category/blog", "destination": "/blog/", "permanent": true },
{ "source": "/category/childrens-eye-care/", "destination": "/pediatric-eye-care/", "permanent": true },
{ "source": "/category/childrens-eye-care", "destination": "/pediatric-eye-care/", "permanent": true },
{ "source": "/category/contact-lenses/", "destination": "/contact-lenses/", "permanent": true },
{ "source": "/category/contact-lenses", "destination": "/contact-lenses/", "permanent": true },
{ "source": "/category/dry-eye/", "destination": "/dry-eye-treatment/", "permanent": true },
{ "source": "/category/dry-eye", "destination": "/dry-eye-treatment/", "permanent": true },
{ "source": "/category/eye-care/", "destination": "/eye-care-services/", "permanent": true },
{ "source": "/category/eye-care", "destination": "/eye-care-services/", "permanent": true },
{ "source": "/category/eye-health/", "destination": "/eye-care-services/", "permanent": true },
{ "source": "/category/eye-health", "destination": "/eye-care-services/", "permanent": true },
{ "source": "/category/glasses/", "destination": "/eyeglasses/", "permanent": true },
{ "source": "/category/glasses", "destination": "/eyeglasses/", "permanent": true },
{ "source": "/category/myopia/", "destination": "/myopia-control/", "permanent": true },
{ "source": "/category/myopia", "destination": "/myopia-control/", "permanent": true },
{ "source": "/category/:path*", "destination": "/blog/", "permanent": true }
```

**Risk:** LOW — Adding new redirects, no existing routes affected.

---

## FIX 2: Old WordPress Query Parameter URLs (MODERATE)

**Problem:** `https://classicvisioncare.com/?page_id=2` returns HTTP 200 (serving the homepage). This creates duplicate content. GSC shows 53 impressions.

**Fix:** Add redirect in `vercel.json` or handle via Vercel middleware/edge function to strip `?page_id=` params and redirect to `/`:
```json
{ "source": "/:path*", "has": [{ "type": "query", "key": "page_id" }], "destination": "/:path*", "permanent": true }
```

**Risk:** LOW — Only affects URLs with `?page_id=` query param, which are all legacy WP URLs.

---

## FIX 3: Sitemap 0-Indexed Issue (MODERATE)

**Problem:** Both `sitemap.xml` and `sitemap-core.xml` show **0 indexed URLs** in GSC despite being submitted on 2026-02-20. This is likely normal processing delay (only 6 days), but we should verify the sitemaps are valid.

**Fix:**
1. Verify sitemaps are well-formed XML (check for encoding issues, proper `<urlset>` namespace)
2. Re-submit sitemaps via GSC after fixing category/redirect issues
3. Monitor — GSC sitemap indexing count can lag by weeks

**Risk:** NONE — Monitoring only.

---

## FIX 4: `/ocular-rosacea` Redirect Error (HIGH PRIORITY)

**Problem:** GSC reports "Redirect error" for `https://classicvisioncare.com/ocular-rosacea` (without trailing slash). The redirect chain is:
1. `/ocular-rosacea` → Vercel adds trailing slash → `/ocular-rosacea/`
2. `/ocular-rosacea/` → vercel.json redirect → `/ocular-rosacea/all-about-ocular-rosacea/`

This is a **redirect chain** (2 hops), which Google flags as a redirect error. This affects the **top page by clicks** (220 clicks, 25K impressions).

**Fix:** Add a direct redirect for the non-trailing-slash variant:
```json
{ "source": "/ocular-rosacea", "destination": "/ocular-rosacea/all-about-ocular-rosacea/", "permanent": true }
```

**Risk:** LOW — Adds a shortcut for existing redirect chain. Does not affect any existing working URL.

---

## FIX 5: Title/Meta Description CTR Optimization (HIGH IMPACT)

**Problem:** Many pages rank well (positions 1-10) but have terrible CTR, indicating poor title tags and meta descriptions.

**Worst CTR offenders (high impressions, decent position, but near-0% CTR):**

| Page | Impressions | Position | CTR | Action Needed |
|------|-------------|----------|-----|---------------|
| `/eye-treatment/...` (eye pain) | 58,846 | 15.7 | 0.3% | Improve title + meta |
| `/dry-eyes/...` (punctal plugs) | 13,120 | 8.3 | 0.6% | Improve title + meta |
| `/dry-eyes/...` (causes) | 8,362 | 5.6 | 0.5% | Improve title + meta |
| `/glaucoma/...` | 7,047 | 4.0 | 0.3% | Improve title + meta |
| `/eye-care/...` | 6,340 | 5.5 | 0.3% | Improve title + meta |
| `/eye-treatment/...` (macular) | 6,636 | 10.4 | 0.0% | Improve title + meta |
| `/contact-lenses/...` | 5,729 | 15.8 | 0.2% | Improve title + meta |
| `/eye-care/...` (infections) | 5,941 | 4.7 | 0.1% | Improve title + meta |
| `/dry-eye-treatment-...` (IPL) | 3,644 | 38.9 | 0.0% | Long-term content fix |
| `/dry-eyes/...` (symptoms) | 3,146 | 44.2 | 0.0% | Long-term content fix |

**Fix:** This is a content/SEO task, NOT a code change. For each page:
1. Audit current `<title>` and `<meta name="description">`
2. Rewrite with target keywords + compelling CTAs
3. Ensure title is <60 chars, description is 150-160 chars

**Risk:** NONE to the codebase — content-only changes to HTML files.

---

## FIX 6: `www` to Non-`www` Canonical Consolidation (LOW)

**Problem:** GSC shows impressions/clicks for `www.classicvisioncare.com` URLs:
- `https://www.classicvisioncare.com/?utm_s...` — 2 clicks, 171 impressions
- `https://www.classicvisioncare.com/servic...` — 2 clicks, 294 impressions
- `https://www.classicvisioncare.com//servi...` — 1 click (double slash!)

The `www` → non-`www` redirect is working (GSC shows "Page with redirect"), so this is a **monitoring issue**, not a code fix. Google will eventually consolidate.

**Fix:**
1. Ensure all internal links use `https://classicvisioncare.com/` (no `www`)
2. Verify canonical tags point to non-`www` version
3. The double-slash URL (`//servi...`) suggests a link somewhere with a trailing slash on domain + leading slash on path — grep codebase for this

**Risk:** LOW — Internal link audit only.

---

## FIX 7: Author Pages Leaking SEO Value (LOW)

**Problem:** `/author/ankit-patel/` and `/author/dr-mital-patel/` are in sitemap.xml and indexed. Author pages are thin content for a practice website.

**Fix:**
1. Remove author pages from `sitemap.xml`
2. Add `noindex` meta tag to author pages OR redirect them to `/our-doctors/`

**Risk:** LOW — Author pages provide no SEO value for a local practice.

---

## FIX 8: Old `/east-cobb-eye-doctors/` URL Getting Impressions (LOW)

**Problem:** `/east-cobb-eye-doctors/` shows 70 impressions. There's already a redirect for `/eye-doctor-east-cobb-marietta-ga/` → `/eye-doctor-marietta/` but not for this variant.

**Fix:** Already exists: `{ "source": "/east-cobb-eye-doctors/", "destination": "/eye-doctor-marietta/", "permanent": true }` — Verify this is actually in vercel.json (checking...).

Actually checking vercel.json above, I see it IS there. Let me verify:

```
curl -sI "https://classicvisioncare.com/east-cobb-eye-doctors/"
```

If it 301s → fine. If 404 → need to add.

**Risk:** NONE.

---

## Implementation Status

| Fix | Description | Status | Commit |
|-----|-------------|--------|--------|
| **FIX 0** | Breadcrumb fix on 54+6 pages | DONE | `cb59be2` |
| **FIX 1** | Category 404 redirects (17 rules) | DONE | `cb59be2` |
| **FIX 2** | Query param duplicate content redirect | REMOVED — was no-op (dest=source, canonical tags handle it) | `2c2189b` |
| **FIX 3** | Sitemap monitoring | MONITORING | — |
| **FIX 4** | Ocular rosacea redirect chain fix | REMOVED — dead code (trailingSlash fires first); 2-hop chain is SEO-acceptable | `2c2189b` |
| **FIX 5** | CTR optimization (8 pages) | DONE | `9d6dfc6` |
| **FIX 6** | www canonical audit | MONITORING | — |
| **FIX 7** | Author page redirects + sitemap cleanup | DONE | `cb59be2` |
| **FIX 8** | East Cobb URL verification | VERIFIED — already working | — |

---

## Files To Modify

| File | Changes | Risk |
|------|---------|------|
| **60 HTML files** (FIX 0) | Fix breadcrumb schema + visible breadcrumb | LOW — content only, no routing changes |
| `vercel.json` | Add ~18 redirect rules (FIX 1,2,4) | LOW — append-only, no existing rules changed |
| `sitemap.xml` | Remove author pages (FIX 7) | LOW — removing thin content |
| Various HTML files (FIX 5) | Title/meta updates | NONE — content-only |

---

## Rosacea Content Note

The site has TWO ocular rosacea pages:
- **Service page:** `/ocular-rosacea/all-about-ocular-rosacea/` — indexed, 220 clicks, 25K impressions
- **Blog post:** `/blog/ocular-rosacea/` — published 2026-02-25 (commits `2477a7a`, `1c6e812`, `8df9206`)

Stale branch `content/understanding-ocular-rosacea-a-patient-guide` deleted — content was already on `main`.

---

## What We Will NOT Touch

- No changes to existing redirect rules (preserve all current working redirects)
- No changes to robots.txt (already well-configured)
- No changes to Vercel headers/rewrites
- No changes to JavaScript/CSS/build process
- No structural changes to page layout or design
