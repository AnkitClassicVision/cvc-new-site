# Image Migration Plan — wp-content/uploads → /images/content/

**Generated:** 2026-02-26
**Status:** PLAN — awaiting approval
**Risk Level:** MEDIUM (68 pages affected, SEO-critical site)

---

## Executive Summary

**The Problem:** `vercel.json` line 77 redirects ALL `/wp-content/uploads/*` requests to `/` (homepage) with a 308. But 83 tracked images at those paths are actively referenced by 68 HTML pages (683 total references: 615 relative + 68 absolute). Every content image on the site is broken in production — they redirect to homepage instead of displaying.

**The Fix:** Migrate images to `/images/content/`, update all HTML references, and replace the catch-all redirect with a path-preserving redirect for external backlinks.

**Key Constraint:** Vercel redirects fire BEFORE filesystem (confirmed by Gemini research and production curl test). This means we cannot simply remove the redirect — we must update the HTML references AND move the files.

---

## Agent-Team Research Summary

| Agent | Key Finding |
|-------|-------------|
| **Gemini** | Vercel redirects take priority over filesystem — the redirect wins even if the file exists. Path-preserving redirects (`/:path*`) work. Google Image rankings transfer via 301 but take weeks. |
| **Claude** | 83 images, 60 unique bases (23 size variants), 175 current redirects (850 capacity remaining). Images have good attributes: width/height, loading="lazy", decoding="async", srcset. No image build pipeline exists. |
| **Codex** | (Timed out — audit completed by Claude directly) |

### Verified Facts
- **83 images** tracked in `wp-content/uploads/` (6.1 MB total)
- **76 used, 7 unused** — all 7 unused are `2463401` size variants (150x150, 300x200, 400x250, 400x284, 400x516, 510x382, 768x512)
- **60 unique base images** (23 are responsive variants like `-480x320`)
- **615 relative** URL references (`/wp-content/uploads/...`)
- **68 absolute** URL references (`https://classicvisioncare.com/wp-content/uploads/...`)
- **683 total references** across 68 HTML files
- **175 redirects** currently in vercel.json (1024 limit → 849 remaining)
- Images already have `width`, `height`, `loading="lazy"`, `decoding="async"`, `srcset`
- **1 dangling reference** — `blog/why-your-eyes-get-so-dry-in-the-winter/index.html` references `Screenshot-2025-11-24-at-12.56.08-PM.png` which was deleted from git (needs replacement image)

---

## Migration Strategy: Atomic Single-Commit Deploy

We do everything in ONE commit so Vercel deploys all changes atomically:
1. Move images to new location
2. Update all HTML references
3. Replace the redirect rule

No intermediate state where images could break.

---

## Step-by-Step Plan

### Step 1: Move Images (preserve directory structure)

Move `wp-content/uploads/` → `images/content/` preserving the date-based subdirectory structure:

```
wp-content/uploads/2022/12/child-is-happy-with-her-eyeglasses.jpg
→ images/content/2022/12/child-is-happy-with-her-eyeglasses.jpg

wp-content/uploads/2023/09/2463401.jpg
→ images/content/2023/09/2463401.jpg

wp-content/uploads/2023/09/2463401-480x320.jpg
→ images/content/2023/09/2463401-480x320.jpg
```

**Why `images/content/`?**
- Existing `/images/` directory already has `Cache-Control: public, max-age=31536000, immutable` header
- So migrated images get aggressive caching automatically
- Clean namespace: `content/` = blog/article content images

**Commands:**
```bash
# Delete 7 unused 2463401 size variants first
git rm wp-content/uploads/2023/09/2463401-150x150.jpg
git rm wp-content/uploads/2023/09/2463401-300x200.jpg
git rm wp-content/uploads/2023/09/2463401-400x250.jpg
git rm wp-content/uploads/2023/09/2463401-400x284.jpg
git rm wp-content/uploads/2023/09/2463401-400x516.jpg
git rm wp-content/uploads/2023/09/2463401-510x382.jpg
git rm wp-content/uploads/2023/09/2463401-768x512.jpg

# Move remaining 76 images
mkdir -p images/content
git mv wp-content/uploads/2022 images/content/2022
git mv wp-content/uploads/2023 images/content/2023
git mv wp-content/uploads/2024 images/content/2024
git mv wp-content/uploads/2025 images/content/2025
```

### Step 2: Update All HTML References (68 files, 683 references)

Two types of references to update:

**A. Relative URLs (615 occurrences):**
```
/wp-content/uploads/  →  /images/content/
```

**B. Absolute URLs (68 occurrences in JSON-LD schema + og:image):**
```
https://classicvisioncare.com/wp-content/uploads/  →  https://classicvisioncare.com/images/content/
```

**Method:** Use `sed` or a script to do a global find-and-replace across all HTML files. Both patterns reduce to the same substitution:
```
wp-content/uploads/ → images/content/
```

**Step 2b: Fix dangling screenshot reference**

`blog/why-your-eyes-get-so-dry-in-the-winter/index.html` line 29 and 513 reference `Screenshot-2025-11-24-at-12.56.08-PM.png` which was deleted. This needs a replacement image (e.g., a relevant stock photo or generated hero image placed in `images/content/`).

**Verification:** After replacement, grep to confirm zero remaining references:
```bash
grep -r "wp-content/uploads/" --include="*.html" . | wc -l
# Expected: 0
```

### Step 3: Update vercel.json Redirect

**Remove line 77:**
```json
{ "source": "/wp-content/uploads/:path*", "destination": "/", "permanent": true }
```

**Replace with path-preserving redirect:**
```json
{ "source": "/wp-content/uploads/:path*", "destination": "/images/content/:path*", "permanent": true }
```

**Why keep a redirect?**
- External sites may link to old `/wp-content/uploads/` image URLs
- Google Image Search may have indexed old URLs
- 301 redirects transfer ranking signals (confirmed by Gemini)
- Only 1 redirect rule needed (uses `:path*` wildcard)

**Also keep separate rules for non-image wp-content paths:**
```json
{ "source": "/wp-content/plugins/:path*", "destination": "/", "permanent": true },
{ "source": "/wp-content/themes/:path*", "destination": "/", "permanent": true }
```

Wait — actually the current rule catches ALL `/wp-content/uploads/*`. Since we're changing it to redirect to `/images/content/:path*`, non-image files (if any existed in uploads) would 404 at the new path anyway. This is fine because:
- Only images ever existed in WP uploads
- The redirect preserves the path, so image requests work
- Non-upload wp-content paths (`/wp-content/plugins/`, `/wp-content/themes/`) are NOT matched by this rule (it only matches `/wp-content/uploads/`)

### Step 4: Verify — Pre-Commit Checks

Before committing, run these verification checks:

```bash
# 1. No remaining wp-content/uploads references in HTML
grep -r "wp-content/uploads/" --include="*.html" . | wc -l
# Expected: 0

# 2. All moved images exist at new paths
for f in $(git ls-files images/content/); do
  [ -f "$f" ] && echo "OK: $f" || echo "MISSING: $f"
done

# 3. vercel.json is valid JSON
python3 -c "import json; json.load(open('vercel.json')); print('Valid JSON')"

# 4. Redirect count still under limit
python3 -c "import json; d=json.load(open('vercel.json')); print(f'Redirects: {len(d[\"redirects\"])}')"

# 5. No old wp-content directory left (should be empty after git mv)
ls wp-content/uploads/ 2>/dev/null && echo "STILL HAS FILES" || echo "CLEAN"
```

### Step 5: Commit & Push (Atomic Deploy)

```bash
git add -A
git commit -m "Migrate wp-content/uploads images to /images/content/

- Move 83 images preserving directory structure
- Update 683 references across 68 HTML files
- Replace homepage redirect with path-preserving redirect
- External backlinks to old paths now 301 to new location"
git push
```

### Step 6: Post-Deploy Verification

After Vercel deploys (~30-60 seconds):

```bash
# 1. New image path serves correctly
curl -sI https://classicvisioncare.com/images/content/2023/09/2463401.jpg | head -5
# Expected: HTTP/2 200, Cache-Control: immutable

# 2. Old path redirects to new path
curl -sI https://classicvisioncare.com/wp-content/uploads/2023/09/2463401.jpg | head -5
# Expected: HTTP/2 308, Location: /images/content/2023/09/2463401.jpg

# 3. Spot-check 5 pages for working images
for page in \
  "contact-lenses/am-i-a-candidate-for-contact-lenses/" \
  "glaucoma/who-is-at-risk-for-glaucoma/" \
  "blog/beating-digital-eye-strain-in-a-screen-filled-world/" \
  "dry-eyes/5-common-signs-of-dry-eyes/" \
  "eye-treatment/dull-pain-behind-your-eyes-heres-why/"; do
  echo "Checking $page..."
  curl -s "https://classicvisioncare.com/$page" | grep -c "images/content/"
done

# 4. No remaining references to old path
curl -s https://classicvisioncare.com/blog/ | grep -c "wp-content/uploads"
# Expected: 0

# 5. Cache headers present on images
curl -sI https://classicvisioncare.com/images/content/2022/12/child-is-happy-with-her-eyeglasses.jpg | grep -i cache
# Expected: Cache-Control: public, max-age=31536000, immutable
```

---

## Rollback Strategy

If something goes wrong after deploy:

```bash
git revert HEAD
git push
```

This atomically reverts all changes (images move back, HTML references restored, redirect rule restored). Vercel deploys in ~30 seconds.

---

## What We Are NOT Doing (and Why)

| Skipped Item | Reason |
|-------------|--------|
| **WebP conversion** | Images are only 6.1MB total. Conversion adds complexity for minimal gain. Can be done later as a separate optimization. |
| **Image renaming** | Numeric filenames (2463401.jpg) are ugly but changing them would break srcset references and require more complex mapping. Keep as-is. |
| **Image optimization** | Images already have width/height, loading="lazy", decoding="async", and srcset. No CWV improvement needed. |
| **Sitemap image index** | No image URLs in sitemap currently. Not needed — Google discovers images via page crawl. |
| **Individual redirects** | One wildcard redirect (`/wp-content/uploads/:path*` → `/images/content/:path*`) handles all paths. No need for 83 individual rules. |

---

## Success Criteria

- [ ] Zero `wp-content/uploads/` references in any HTML file
- [ ] All 83 images serve HTTP 200 from `/images/content/` paths
- [ ] Old `/wp-content/uploads/` paths return 301 → `/images/content/` (not 308 → `/`)
- [ ] Cache-Control headers present on all images (immutable, 1-year)
- [ ] No CLS regression (images already have width/height)
- [ ] vercel.json valid JSON with ≤1024 redirects
- [ ] All 68 affected pages render correctly with visible images

---

## Files Modified

| File/Directory | Change | Count |
|---------------|--------|-------|
| `images/content/**` | NEW — migrated images | 76 files |
| `wp-content/uploads/**` | DELETED — 76 moved, 7 unused deleted | 83 files |
| `68 HTML files` | Replace wp-content/uploads → images/content | 683 references |
| `blog/why-your-eyes-get-so-dry-in-the-winter/index.html` | Fix dangling screenshot reference | 2 references |
| `vercel.json` | Replace redirect destination | 1 line |

**Total redirect count after change:** 164 (unchanged — same rule, different destination)
