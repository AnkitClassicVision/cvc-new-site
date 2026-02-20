# YMYL Content Policy — Classic Vision Care

**Last updated:** February 2026
**Applies to:** All health, medical, and clinical content on classicvisioncare.com

---

## 1. Scope

This policy covers all pages that discuss eye conditions, treatments, procedures, medications, or clinical recommendations. These pages fall under Google's **Your Money or Your Life (YMYL)** classification and require elevated standards of accuracy and trust.

## 2. Content Standards

### Language Rules

- **No diagnosis language.** Never state or imply that reading the page can substitute for an in-person examination. Use phrases like "may help," "can support," or "your doctor will determine."
- **No guaranteed outcomes.** Avoid claims like "will cure," "eliminates," or "guaranteed results." Use "may improve," "designed to support," or "many patients experience."
- **No unsupported statistics.** Any clinical data must include a source citation (study name, journal, year).
- **Patient-first language.** Write for the patient, not for search engines. Avoid keyword stuffing or unnatural phrasing.

### Required Disclaimers

Every health content page must include a medical disclaimer. Use this standard text placed before the CTA section:

> This page is for informational purposes only and does not constitute medical advice. Only a qualified eye care professional can diagnose conditions, recommend treatments, or prescribe medications. Please consult your optometrist for personalized guidance.

### Preferred Citation Sources

When referencing clinical evidence, prefer these authoritative sources:

1. American Academy of Ophthalmology (AAO)
2. American Optometric Association (AOA)
3. Centers for Disease Control and Prevention (CDC)
4. National Institutes of Health / National Eye Institute (NIH/NEI)
5. Peer-reviewed journals (e.g., *Optometry and Vision Science*, *The Open Ophthalmology Journal*)

Format citations as: Author/Organization, Title, Journal/Publisher, Year.

## 3. Content Review Process

### New Health Pages

1. **Draft** — Content writer creates the page following language rules above
2. **Clinical Review** — Dr. Mital Patel or Dr. Bhumi Patel reviews for medical accuracy
3. **Checklist Sign-Off** — Reviewer completes the checklist below
4. **Publish** — Page goes live with "Last reviewed" date
5. **IndexNow** — Submit URL via `scripts/indexnow-submit.py`

### Existing Page Updates

1. When updating medical content, the reviewing doctor must re-confirm accuracy
2. Update the "Last reviewed" `<time>` element with the current date
3. If changing treatment recommendations, add a note to the page's revision history

### Annual Review Cycle

All health content pages should be reviewed at least once per year. The "Last reviewed" date on each page serves as the tracking mechanism.

## 4. Pre-Publish Checklist

Before publishing any health content page, the reviewing clinician must confirm:

- [ ] Page does not diagnose conditions or prescribe treatments
- [ ] No guaranteed outcomes or absolute claims
- [ ] All statistics cite a reputable source
- [ ] Medical disclaimer is present and visible
- [ ] "Last reviewed" date is set to the current month
- [ ] Page does not recommend specific OTC products without clinical context
- [ ] Patient guidance includes "consult your optometrist" language
- [ ] FAQPage schema (if present) matches visible FAQ content
- [ ] Page has been proofread for medical terminology accuracy

## 5. Schema Requirements

Health content pages should include:

- **MedicalWebPage** or **WebPage** type in JSON-LD
- **FAQPage** schema for pages with FAQ sections
- **Physician** schema for doctor profile pages with `alumniOf`, `knowsAbout`, and credentials
- **BreadcrumbList** for navigation context

## 6. Existing Compliance

As of February 2026, the following are in place:

- Medical disclaimers on 25+ health pages
- "Last reviewed" dates on key service pages
- FAQPage schema on all 7 primary service pages
- Physician schema for both Dr. Mital Patel and Dr. Bhumi Patel
- YMYL-safe language reviewed across all condition pages
