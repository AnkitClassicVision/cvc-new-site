# Website feedback implementation (2026-02-09)

## Scope (requested changes)
- Nav: add **Presbyopia** and **SharpVision** under **Services → Conditions We Treat** (desktop + mobile).
- Replace **MiBoFlo** with **Radio Frequency** across the site (nav + treatment page + key mentions).
- Fix **East Cobb**: map pin(s) and office hours (Monday currently incorrect).
- Footer: improve low-contrast text/icon colors and ensure **Facebook/Instagram** links are correct.
- Page copy fixes:
  - `/comprehensive-eye-exams/`: replace “recommendations” wording with **custom prescription plan**.
  - `/blepharitis/`: replace **LipiScan** mention with **Topcon Myah**.
  - `/computer-eye-strain/`: remove **Vision Therapy** as a solution.
  - `/eyewear/`: clarify/fill **lens options**.
  - `/eye-doctor-marietta/` + `/our-locations/`: remove “Dry Eye Spa” wording for East Cobb (as requested).
  - `/about-us/`: improve hard-to-read font colors (contrast).
- Locations: correct fax numbers where displayed.

## Success criteria (definition of done)
- No `MiBoFlo` mentions in primary navigation or in the updated dry eye service pages; legacy MiBoFlo URLs redirect to **Radio Frequency**.
- No remaining occurrences of `LipiScan` in publicly served pages.
- Services menu includes `Presbyopia` and `SharpVision` in both desktop + mobile nav.
- East Cobb:
  - Map embed(s) resolve to the correct East Cobb address.
  - Monday is not incorrectly shown as “Closed”.
  - “Dry Eye Spa” is not claimed for East Cobb.
- Footer:
  - Social links are valid external URLs (no `#` or empty `href`).
  - Footer text/icons have improved contrast (aim: WCAG AA for normal text).
- Copy changes are reflected on the specified pages and read naturally in context.
- Fax numbers shown on location pages are correct (or removed if intentionally unavailable).

## Testing checklist
### Manual (quick smoke)
1. Open `/index.html` and verify:
   - Services → Conditions menu includes Presbyopia + SharpVision.
   - Dry Eye menu item uses Radio Frequency (not MiBoFlo).
   - Homepage East Cobb location card map pin is correct and hours mention Monday correctly.
   - Footer links to Facebook/Instagram open to the intended profiles.
2. Visit pages and confirm content:
   - `/comprehensive-eye-exams/` (custom prescription plan wording)
   - `/blepharitis/` (Topcon Myah, no LipiScan)
   - `/computer-eye-strain/` (no Vision Therapy solution)
   - `/eyewear/` (lens options section is complete/clear)
   - `/eye-doctor-marietta/` and `/our-locations/` (East Cobb hours + no Dry Eye Spa claim)
   - `/about-us/` (improved readability on low-contrast text)

### Automated (Playwright ideas)
- Crawl internal pages and assert forbidden strings are absent:
  - `MiBoFlo`, `LipiScan`
  - `Vision Therapy` on `/computer-eye-strain/`
- Assert nav renders the new menu labels (desktop + mobile viewport snapshots).
- Basic link checks:
  - Social links in footer are not empty/`#`.
  - (Optional) `HEAD`/`GET` to external social URLs (may be flaky due to bot protection).

## Implementation decisions (resolved)
- **SharpVision** is implemented as an anchor section on the new `/presbyopia/` page: `/presbyopia/#sharpvision`.
- **Radio Frequency** is used as the nav label; pages describe it as *radiofrequency (RF)* where helpful.
- **East Cobb hours** to apply everywhere:
  - Mon 8:00 AM–5:00 PM
  - Tue 9:00 AM–6:00 PM
  - Wed 8:00 AM–5:00 PM
  - Thu 9:00 AM–6:00 PM
  - Fri–Sun Closed
- **Fax numbers** were flagged as incorrect in the feedback; fax lines were removed from the primary location pages until correct numbers are confirmed.
