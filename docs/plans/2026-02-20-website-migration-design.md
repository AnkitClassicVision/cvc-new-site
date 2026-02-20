# Website Migration Plan: classicvisioncare.com → Vercel

**Date:** 2026-02-20
**Approach:** Staged Migration (Approach A)
**Domain:** classicvisioncare.com (same domain, platform change)

## Current State

| Component | Current | Target |
|-----------|---------|--------|
| Hosting | Nestify CDN (WordPress) | Vercel (static HTML + serverless) |
| DNS Management | Namecheap | Cloudflare |
| Domain Registrar | Namecheap | Namecheap (no change) |
| Email | Google Workspace | Google Workspace (no change) |
| SSL | Nestify-managed | Vercel auto-provisioned |
| CDN | Nestify CDN | Vercel Edge Network |

## Migration Type

This is a **hosting/platform cutover with URL structure changes** — same domain, new platform, new URL paths. Google's guidance for site moves with URL changes applies. No Change of Address tool needed (same domain).

## Phase 0: Pre-Flight Prep (Before Migration)

### SEO Baseline
- [ ] Export GSC data: indexed URLs, top 20 keywords, average positions
- [ ] Export GA4 data: sessions, organic traffic %, top landing pages
- [ ] Screenshot GSC performance dashboard

### Redirect Audit
- [ ] Screaming Frog crawl of current classicvisioncare.com
- [ ] Cross-reference crawl results against 136 redirects in vercel.json
- [ ] Add missing redirects: /feed/, /wp-admin/, /wp-login.php, additional blog pagination, wp-content/uploads paths

### Vercel Pre-Configuration
- [ ] Add classicvisioncare.com + www.classicvisioncare.com as custom domains in Vercel
- [ ] Issue SSL via TXT DNS challenge at Namecheap
- [ ] Verify SSL: `curl https://classicvisioncare.com --resolve classicvisioncare.com:443:76.76.21.21 -I`

### Compliance
- [ ] Audit /api/contact.js for PHI logging
- [ ] Audit GTM container GTM-TT6JRB7 for PHI capture
- [ ] Review COMPLIANCE_AUDIT.md HIGH issues

### Cloudflare Setup
- [ ] Add classicvisioncare.com to Cloudflare (free plan)
- [ ] Document ALL current DNS records from Namecheap (A, CNAME, MX, TXT, SPF, DKIM, DMARC, CAA, SRV)
- [ ] Configure matching records in Cloudflare (DO NOT activate yet)

## Phase 1: DNS to Cloudflare (Day 1)

**Goal:** DNS management moves to Cloudflare. Site stays on Nestify.

1. Configure all records in Cloudflare to match Namecheap exactly
2. Change nameservers at Namecheap to Cloudflare's assigned NS
3. Wait for propagation (1-24 hours)

### Phase 1 Verification
- [ ] classicvisioncare.com loads WordPress site
- [ ] Send/receive test email on @classicvisioncare.com
- [ ] Cloudflare shows domain "Active"
- [ ] Wait 24-48 hours with stable email

## Phase 2: Switch Hosting to Vercel (Day 3-4)

**Goal:** Website moves from Nestify to Vercel. Email stays on Google Workspace.

### Pre-Switch
- [ ] Lower TTL on A/CNAME to 1 minute in Cloudflare
- [ ] Confirm Vercel SSL is valid
- [ ] Content freeze on WordPress

### The Switch
- [ ] A record @ → 76.76.21.21 (DNS Only / gray cloud)
- [ ] CNAME www → cname.vercel-dns.com (DNS Only / gray cloud)
- [ ] DO NOT touch MX, TXT, SPF, DKIM records

### Phase 2 Verification (first 30 minutes)
- [ ] https://classicvisioncare.com loads new site
- [ ] https://www.classicvisioncare.com redirects to apex
- [ ] robots.txt shows Allow: / (production mode)
- [ ] Test 5 key old-URL redirects
- [ ] Submit booking form end-to-end
- [ ] Send/receive test email
- [ ] SSL certificate valid in browser
- [ ] Mobile device check (Book Now buttons)

## Phase 3: Post-Migration (Day 4+)

### First 24 Hours
- [ ] Submit sitemaps in GSC (sitemap.xml + sitemap-core.xml)
- [ ] Request indexing for homepage + top 5 pages
- [ ] Screaming Frog crawl of new live site
- [ ] Update Google Business Profile links (Marietta + Kennesaw)
- [ ] Verify cvc-new.vercel.app still returns Disallow: /

### First 2 Weeks
- [ ] Monitor GSC daily for crawl errors and 404s
- [ ] Monitor GA4 traffic vs baseline
- [ ] Add redirects for any new 404s found

### First 90 Days
- [ ] Weekly GSC performance comparison
- [ ] Keep Nestify hosting alive for 30+ days as rollback
- [ ] Cancel Nestify after 30 days stable operation

## Known Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Cloudflare orange-cloud conflicts with Vercel | HIGH | Must use DNS Only (gray cloud) |
| wp-content/uploads image URLs will 404 | MEDIUM | Add wildcard redirect or verify no inbound links |
| CAA records blocking Vercel SSL | MEDIUM | Check/remove restrictive CAA records |
| GTM capturing PHI from forms | MEDIUM | Audit GTM container before launch |
| Blog pagination redirect gaps | LOW | Crawl to find all paginated pages |

## Key Technical Details

- Vercel IP: 76.76.21.21
- www CNAME target: cname.vercel-dns.com
- Vercel project: cvc-new (mybcat team)
- GitHub repo: AnkitClassicVision/cvc-new-site (main branch)
- robots.txt: Dynamic via /api/robots.js (auto-detects production vs staging)
- Redirects: 136 rules in vercel.json (permanent 301s)

## Sources

- [Vercel Zero-Downtime Migration](https://vercel.com/kb/guide/zero-downtime-migration)
- [Google: Site Move No URL Changes](https://developers.google.com/search/docs/crawling-indexing/site-move-no-url-changes)
- [Google: Site Move With URL Changes](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)
- [HHS OCR: HIPAA Online Tracking](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/hipaa-online-tracking/index.html)
- [Vercel HIPAA BAA for Pro Teams](https://vercel.com/changelog/hipaa-baas-are-now-available-to-pro-teams)
