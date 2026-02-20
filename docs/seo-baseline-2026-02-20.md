# SEO Baseline — classicvisioncare.com Migration
**Captured:** 2026-02-20 (migration day)
**Period:** Last 7 days (2026-02-13 to 2026-02-20)

## Overall Performance
| Metric | Value |
|--------|-------|
| Total Clicks | 198 |
| Total Impressions | 36,125 |
| Average CTR | 0.55% |
| Average Position | 12.2 |

## Top 20 Queries (by clicks)
| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| classic vision care | 11 | 27 | 40.7% | 2.6 |
| ocular rosacea treatment | 9 | 328 | 2.7% | 5.2 |
| classic vision care kennesaw | 7 | 36 | 19.4% | 1.0 |
| classic vision care east cobb | 2 | 24 | 8.3% | 1.0 |
| dull ache behind eye | 2 | 54 | 3.7% | 8.1 |
| eye ache | 2 | 41 | 4.9% | 28.2 |
| how to tell if punctal plug fell out | 2 | 23 | 8.7% | 1.0 |
| what is ocular rosacea | 2 | 93 | 2.2% | 3.6 |
| aching eyeball | 1 | 1 | 100.0% | 2.0 |
| best eye cream for ocular rosacea | 1 | 8 | 12.5% | 5.6 |
| classic vision care - kennesaw | 1 | 2 | 50.0% | 1.0 |
| dull headache pain behind eye | 1 | 1 | 100.0% | 3.0 |
| dull pain behind left eye | 1 | 91 | 1.1% | 7.3 |
| dull pain in the eye | 1 | 4 | 25.0% | 3.0 |
| eye doctor close to me | 1 | 2 | 50.0% | 1.0 |
| eye doctor kennesaw, ga | 1 | 3 | 33.3% | 6.7 |
| eye pain | 1 | 31 | 3.2% | 36.9 |
| eye strain symptoms | 1 | 23 | 4.3% | 2.9 |
| eyelid rosacea treatment | 1 | 4 | 25.0% | 1.0 |
| flare up | 1 | 1 | 100.0% | 3.0 |

## Top 20 Pages (by clicks)
| Page | Clicks | Impressions | CTR | Position |
|------|--------|-------------|-----|----------|
| /ocular-rosacea* | 64 | 5,632 | 1.1% | 5.5 |
| /eye-treatments/eye-pain* | 35 | 9,825 | 0.4% | 13.4 |
| / (homepage) | 15 | 1,313 | 1.1% | 15.5 |
| /dry-eyes/punctal-plugs* | 13 | 2,581 | 0.5% | 7.8 |
| /eye-doctor-kennesaw-ga | 13 | 402 | 3.2% | 4.5 |
| /dry-eyes/what-causes-dry-eyes* | 11 | 861 | 1.3% | 5.2 |
| /eye-doctor-east-cobb-marietta-ga* | 11 | 863 | 1.3% | 17.3 |
| /glaucoma/8-tips-to-prevent-glaucoma* | 6 | 2,759 | 0.2% | 2.4 |
| /eye-care/how-to-choose-an-eye-doctor* | 4 | 1,606 | 0.2% | 4.9 |
| /dr-mital-patel | 3 | 133 | 2.3% | 8.4 |
| /blog/dont-rub-your-eyes* | 2 | 43 | 4.7% | 10.3 |
| /contact-lenses* | 2 | 1,649 | 0.1% | 16.6 |
| /eye-treatments* | 2 | 104 | 1.9% | 6.7 |
| Other pages (7) | 7 | ~700 | — | — |

*URL truncated in GSC output — approximate path shown

## Key Page Index Status (Feb 20, 2026)
| URL | Status | Last Crawled |
|-----|--------|-------------|
| / (homepage) | Submitted and indexed | Feb 18, 2026 |
| /ocular-rosacea | Unknown to Google (new URL) | Never |
| /eye-treatments/eye-pain | Unknown to Google (new URL) | Never |
| /dry-eyes/punctal-plugs | Unknown to Google (new URL) | Never |
| /eye-doctor-kennesaw-ga | Unknown to Google (new URL) | Never |

**Note:** Pages showing "Unknown to Google" are the NEW URL paths on the Vercel site. Google still has the OLD WordPress URLs indexed. The 301 redirects in vercel.json will transfer ranking authority as Google re-crawls. This is expected and normal during migration.

## Sitemaps Submitted
- `sitemap.xml` — submitted to GSC on Feb 20, 2026
- `sitemap-core.xml` — submitted to GSC on Feb 20, 2026

## Verification Checks (Feb 20, 2026)
| Check | Result |
|-------|--------|
| robots.txt production rules | PASS — Allow: / for all bots |
| Sitemap accessible (200) | PASS |
| SSL valid | PASS |
| Homepage loads | PASS |
| 301 redirects working | PASS |

## Action Items
- [ ] Toggle www CNAME to DNS Only (gray cloud) in Cloudflare
- [ ] Verify classicvisioncare.com in Bing Webmaster Tools
- [ ] Submit sitemaps to Bing
- [ ] Update Google Business Profile links (Marietta + Kennesaw)
- [ ] Request indexing for top 5 new URLs in GSC web UI
- [ ] Monitor GSC daily for 2 weeks for crawl errors / 404s
- [ ] Compare weekly performance against this baseline
- [ ] Keep Nestify alive 30+ days as rollback
- [ ] Cancel Nestify after 30 days stable

## Notes
- Site migrated from WordPress (Nestify CDN) to Vercel static HTML on Feb 20, 2026
- DNS moved from Namecheap → user's own Cloudflare account (DNS Only mode)
- 136+ 301/308 redirects in vercel.json for old WordPress URL structure
- robots.txt bug fixed same day (static file was shadowing dynamic /api/robots.js rewrite)
- Contact form (/api/contact.js) audited for HIPAA — LOW RISK (no PHI persistence)
