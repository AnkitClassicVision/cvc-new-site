# Compliance Audit: Classic Vision Care Website

**Audit Date:** 2026-02-06
**Scope:** All HTML content in `/cvc-new/`
**Auditor:** Automated compliance scanner
**Status:** DRAFT -- pending cross-reference with regulatory research (Task #1)

---

## Summary

The redesigned site is generally well-written and conservative compared to the legacy blog content. The newer pages use hedging language ("may help," "for many children," "results vary") in most places. The legacy blog/article content imported from the old site is where the most problematic claims live.

**Finding counts by severity:**
- HIGH (likely violation): 14
- MEDIUM (should fix): 18
- LOW (best-practice improvement): 12

---

## HIGH-SEVERITY FINDINGS

### H1. "Specializing in" claims on doctor pages (multiple files)

**Files:**
- `/cvc-new/dr-mital-patel-od/index.html:7`
- `/cvc-new/dr-bhumi-patel-od/index.html:7`
- `/cvc-new/eye-doctor-marietta/index.html:811`
- `/cvc-new/eye-doctor-kennesaw-ga/index.html:905`
- (and `pages/` duplicates)

**Problematic text:**
> "Specializing in dry eye treatment, specialty contact lenses, and comprehensive eye care."
> "Specializing in pediatric eye care, myopia control, and comprehensive eye exams."

**Why problematic:** In many states (including under FTC/AOA guidance), optometrists should not use "specializing" unless they hold a board-certified specialty credential recognized by the relevant licensing board. General optometrists are typically not recognized as "specialists." Georgia law (O.C.G.A. 43-1-19) restricts specialty claims to those who can substantiate them.

**Suggested edit:** Change "Specializing in" to "Focused on" or "With a focus on" throughout.

---

### H2. "Board-certified" claims without specifying certifying body

**Files:**
- `/cvc-new/about-us/index.html:61,73`
- `/cvc-new/about-us/index.html:1161` ("Board Certified" heading)
- `/cvc-new/pages/about/index.html:58,70,1108`

**Problematic text:**
> "Board-certified optometrist and founder of Classic Vision Care"
> "Board-certified optometrist specializing in pediatric eye care"

**Why problematic:** Optometry does not have a universally recognized "board certification" in the same way medicine does. The term can mislead consumers into thinking the doctor holds a specialty board certification. If the doctors are licensed and in good standing, that is the standard credential; "board-certified" overstates the credentialing.

**Suggested edit:** Replace with "Licensed optometrist" or remove the "Board Certified" section heading, or specify the actual credential (e.g., "Georgia-licensed optometrist").

---

### H3. "how to cure dry eyes" anchor text

**File:** `/cvc-new/dry-eyes/dry-eyes-symptoms-causes-and-treatment/index.html:518`

**Problematic text:**
> `To determine <a href="/dry-eye-treatment/">how to cure dry eyes</a>`

**Why problematic:** Dry eye disease is a chronic condition with no cure. Using "cure" implies guaranteed resolution. This is both medically inaccurate and potentially deceptive advertising under FTC guidelines.

**Suggested edit:** Change anchor text to "how to manage dry eyes" or "dry eye treatment options."

---

### H4. "eliminate your dry eye symptoms" guarantee language

**File:** `/cvc-new/blog/the-three-types-of-dry-eye/index.html:503`

**Problematic text:**
> "you can reduce or eliminate your dry eye symptoms and improve your overall well-being."

**Why problematic:** "Eliminate" implies a guaranteed cure. Dry eye is a chronic condition; promising elimination of symptoms is misleading.

**Suggested edit:** "you can reduce your dry eye symptoms and improve your comfort."

---

### H5. "Atropine eye drops...will slow down the progression of myopia"

**File:** `/cvc-new/blog/a-parents-guide-to-myopia-progression/index.html:509`

**Problematic text:**
> "Atropine eye drops are low-dose eye drops that will slow down the progression of myopia."

**Why problematic:** The word "will" states a guaranteed outcome. Clinical evidence shows atropine *may* slow progression in *many* children, but results vary. Guaranteed treatment outcomes violate FTC advertising standards.

**Suggested edit:** "Atropine eye drops are low-dose eye drops that may help slow the progression of myopia in many children."

---

### H6. "halting the myopia progression" -- guarantee language

**File:** `/cvc-new/blog/a-parents-guide-to-myopia-progression/index.html:508`

**Problematic text:**
> "These glasses or contact lenses will focus light properly on the retina, halting the myopia progression."

**Why problematic:** "Halting" implies stopping progression entirely, which is not clinically accurate. Myopia management aims to slow, not halt, progression.

**Suggested edit:** "These glasses or contact lenses focus light properly on the retina and may help slow myopia progression."

---

### H7. "world-class care" superlative claim

**File:** `/cvc-new/blog/back-to-school-eye-exams/index.html:500`

**Problematic text:**
> "we're committed to providing world-class care in a welcoming, local setting"

**Why problematic:** "World-class" is an unsubstantiated superlative claim. Under FTC guidelines, comparative/superlative claims require substantiation. Georgia's Fair Business Practices Act (O.C.G.A. 10-1-393) also prohibits deceptive claims.

**Suggested edit:** "we're committed to providing thorough, attentive care in a welcoming, local setting"

---

### H8. "the very best in vision care" / "the very best in eye care"

**Files:**
- `/cvc-new/blog/why-regular-eye-exams-are-essential-at-every-age/index.html:498`
- `/cvc-new/eye-treatment/common-causes-of-eye-infections/index.html:529`

**Problematic text:**
> "Our dedicated and professional team offer the very best in vision care at every stage of life"
> "we always strive to provide the very best in eye care to each and every patient"

**Why problematic:** "The very best" is an unsubstantiated superlative that implies superiority over all competitors.

**Suggested edit:** "Our dedicated and professional team provides comprehensive vision care at every stage of life" / "we always strive to provide quality eye care to each and every patient"

---

### H9. "some of the most consistent, attentive and in-depth eye care in Georgia"

**File:** `/cvc-new/blog/combining-supplements-in-office-treatments/index.html:538`

**Problematic text:**
> "if you want to experience some of the most consistent, attentive and in-depth eye care in Georgia, come and pay us a visit."

**Why problematic:** Comparative superlative claim ("most...in Georgia") without substantiation.

**Suggested edit:** "if you want to experience consistent, attentive, and in-depth eye care, come and pay us a visit."

---

### H10. "industry-leading technology"

**File:** `/cvc-new/eye-infections/index.html:547`

**Problematic text:**
> "Our doctors use industry-leading technology to identify the source of your symptoms"

**Why problematic:** "Industry-leading" is a comparative superlative claim requiring substantiation.

**Suggested edit:** "Our doctors use modern diagnostic technology to identify the source of your symptoms"

---

### H11. "relief that is fast and enduring" -- treatment outcome guarantee

**File:** `/cvc-new/blog/managing-dry-eye-in-georgias-changing-seasons/index.html:530`

**Problematic text:**
> "Our doctors specialize in treating this uncomfortable condition and are committed to providing you with relief that is fast and enduring."

**Why problematic:** Two issues: (1) "specialize" claim without specialty credential, (2) "fast and enduring" relief promises specific outcomes that vary by patient.

**Suggested edit:** "Our doctors focus on treating this uncomfortable condition and work to find a plan that brings you meaningful relief."

---

### H12. "we can slow myopia progression" -- definitive claim

**File:** `/cvc-new/myopia-control/index.html:920`

**Problematic text:**
> "With early intervention and the right treatment, we can slow myopia progression and help protect your child's long-term eye health. The earlier we start, the better the outcomes."

**Why problematic:** "We can slow" and "the better the outcomes" state guaranteed results. Should hedge with "may help" language.

**Suggested edit:** "With early intervention and an appropriate treatment plan, we may be able to help slow myopia progression and support your child's long-term eye health."

---

### H13. "hundreds of young myopia patients treated" -- unverifiable patient count

**Files:**
- `/cvc-new/myopia-control-atropine-eye-drops/index.html:787`
- `/cvc-new/myopia-in-children/index.html:766`
- (and `pages/` duplicates)

**Problematic text:**
> "Classic Vision Care has helped hundreds of Kennesaw and Marietta families slow their children's myopia progression."
> "With over 25 years of experience and hundreds of young myopia patients treated"

**Why problematic:** Specific patient count claims should be verifiable. Additionally, the claim implies a guaranteed outcome ("helped...slow...progression"), which overstates what is achievable for all patients.

**Suggested edit:** "Classic Vision Care has worked with many Kennesaw and Marietta families on myopia management plans." / "With over 25 years of experience and a focus on myopia management"

---

### H14. "clinically proven" without citation

**Files:**
- `/cvc-new/myopia-control/index.html:1067`
- `/cvc-new/contact-lens-exams/index.html:606`
- (and `pages/` duplicates)

**Problematic text:**
> "We offer multiple FDA-approved and clinically proven treatment options."
> "Clinically proven" (bullet point for MiSight)

**Why problematic:** "Clinically proven" without linking to or citing specific studies is an unsubstantiated efficacy claim. While MiSight is indeed FDA-approved with clinical trial data, the bare phrase "clinically proven" without context can be misleading under FTC rules.

**Suggested edit:** "We offer multiple FDA-approved treatment options supported by clinical research." / Add a footnote or parenthetical citing the specific study (e.g., "supported by a 3-year randomized clinical trial").

---

## MEDIUM-SEVERITY FINDINGS

### M1. "Proven Results" / "Proven Myopia Control Methods" headings

**Files:**
- `/cvc-new/myopia-control/index.html:890,996,1066`
- `/cvc-new/dry-eye-treatment/index.html:1143`
- `/cvc-new/myopia-control-atropine-eye-drops/index.html:572`
- `/cvc-new/myopia-control-multifocal-lenses/index.html:662`
- (and `pages/` duplicates)

**Problematic text:** "Proven Results" / "Proven Myopia Control Methods" / "Proven Efficacy"

**Why problematic:** "Proven" as a heading without accompanying citations implies absolute certainty. While the body text often hedges appropriately, the headings are read in isolation (especially by screen readers and search engines).

**Suggested edit:** "Evidence-Based Results" / "Clinically Studied Myopia Control Methods" / "Research-Backed Efficacy"

---

### M2. "state-of-the-art" claims (multiple files)

**Files:**
- `/cvc-new/blog/the-three-types-of-dry-eye/index.html:553`
- `/cvc-new/glaucoma/index.html:661`
- `/cvc-new/eye-care-services/index.html:799`
- `/cvc-new/glasses/do-i-need-glasses/index.html:513`
- `/cvc-new/eye-infections/index.html:542`
- (and `pages/` duplicates)

**Problematic text:** "state-of-the-art diagnostic equipment" / "state-of-the-art dry eye diagnostics" / "state-of-the-art vision technology"

**Why problematic:** "State-of-the-art" implies the absolute latest technology, which is a comparative claim that requires substantiation. If the equipment is current but not literally the newest available, this is misleading.

**Suggested edit:** "modern diagnostic equipment" or "advanced diagnostic equipment"

---

### M3. "cutting-edge technology"

**Files:**
- `/cvc-new/blog/combining-supplements-in-office-treatments/index.html:541`
- `/cvc-new/eye-care-services/index.html:961`
- (and `pages/` duplicates)

**Problematic text:**
> "cutting-edge technology and treatment of the future"
> "personalized care plans and cutting-edge technology"

**Why problematic:** "Cutting-edge" is a technology superlative. "Treatment of the future" compounds the issue by implying something beyond current standard of care.

**Suggested edit:** "modern technology and treatment" / "personalized care plans and current technology"

---

### M4. "advanced technology" combined with "expert care" puffery

**File:** `/cvc-new/blog/why-regular-eye-exams-are-essential-at-every-age/index.html:522`

**Problematic text:**
> "we use advanced technology combined with our expert care to detect any underlying conditions. This allows us to keep your vision in optimum condition."

**Why problematic:** "Keep your vision in optimum condition" is a treatment outcome guarantee. "Expert care" approaches specialty claims.

**Suggested edit:** "we use modern technology and thorough examination techniques to help detect underlying conditions early."

---

### M5. "Pain-free" claims for BlephEx

**Files:**
- `/cvc-new/dry-eye-treatment-blephex/index.html:644`
- `/cvc-new/pages/dry-eye/treatments/blephex.html:591`

**Problematic text:** "Pain-free" (as a large stat-style callout)

**Why problematic:** Individual patient experience varies. Claiming a procedure is universally "pain-free" is a guarantee. Some patients may experience mild discomfort.

**Suggested edit:** "Gentle" or "Comfortable for most patients"

---

### M6. "painless" claims for punctal plugs

**Files:**
- `/cvc-new/dry-eye-treatment-punctal-plugs/index.html:7,12` (meta descriptions)
- `/cvc-new/dry-eyes/punctal-plugs-for-dry-eyes-guide/index.html:521`
- `/cvc-new/pages/dry-eye/treatments/punctal-plugs.html:7,12` (meta descriptions)

**Problematic text:**
> "Tiny, painless inserts that keep your natural tears on your eyes longer."
> "The punctual plug procedure is straightforward and painless."

**Why problematic:** While generally well-tolerated, claiming "painless" is a guarantee about individual experience. Some patients may feel minor discomfort.

**Suggested edit:** "Tiny inserts that are well-tolerated and keep your natural tears on your eyes longer." / "The procedure is straightforward and generally comfortable."

---

### M7. "Immediate Relief" heading for MiBoFlo

**File:** `/cvc-new/dry-eye-treatment-miboflo/index.html:572`

**Problematic text:** `<h3>Immediate Relief</h3>`

**Why problematic:** "Immediate relief" is a treatment outcome claim. Results vary; some patients feel improvement gradually, not immediately.

**Suggested edit:** "Soothing Treatment" or "Relief Begins Here"

---

### M8. "90% of MiSight wearers prefer contacts over glasses"

**Files:**
- `/cvc-new/misight-lenses-for-myopia-control/index.html:680`
- `/cvc-new/pages/myopia/treatments/misight.html` (duplicate)

**Problematic text:**
> "90% of MiSight wearers prefer contacts over glasses"

**Why problematic:** Statistical claim without citation. This likely comes from the CooperVision clinical trial but needs a source citation to comply with FTC substantiation requirements.

**Suggested edit:** Add a citation: "90% of MiSight wearers preferred contacts over glasses in the CooperVision clinical trial (Chamberlain et al., 2019)." or reference "according to the manufacturer's clinical data."

---

### M9. "safe and effective" in punctal plugs blog

**File:** `/cvc-new/dry-eyes/punctal-plugs-for-dry-eyes-guide/index.html:529`

**Problematic text:**
> "While punctal plugs are generally safe and effective, like any medical treatment, they can sometimes cause side effects"

**Why problematic:** The sentence does hedge with "generally" and mentions side effects, which is better than most. However, leading with "safe and effective" before the caveat can still be read as a guarantee. Minor issue.

**Suggested edit:** Acceptable as-is since it hedges. Could strengthen: "While punctal plugs are a well-established treatment option, like any medical procedure..."

---

### M10. "trusted choice" -- implied endorsement

**Files:**
- `/cvc-new/myopia-control-atropine-eye-drops/index.html:787`
- `/cvc-new/school-vision-screening/index.html:695`
- (and `pages/` duplicates)

**Problematic text:**
> "Classic Vision Care is the trusted choice for myopia management in Cobb County."
> "Classic Vision Care is the trusted choice for families throughout Marietta and Cobb County."

**Why problematic:** "The trusted choice" (with the definite article "the") implies being THE singular trusted option, which is a comparative superiority claim.

**Suggested edit:** "Classic Vision Care is a trusted choice for..." (change "the" to "a").

---

### M11. "Provides months of relief from a single treatment" (BlephEx)

**File:** `/cvc-new/dry-eye-treatment-blephex/index.html:689`

**Problematic text:**
> "Provides months of relief from a single treatment"

**Why problematic:** While potentially accurate for many patients, stating this without hedging is a treatment outcome guarantee.

**Suggested edit:** "Many patients experience months of relief from a single treatment"

---

### M12. "Quick Relief" label for treatment comparison

**File:** `/cvc-new/dry-eye-treatment/index.html:998`

**Problematic text:** "Quick Relief" (label in treatment comparison)

**Why problematic:** Implies guaranteed fast results.

**Suggested edit:** "Symptom Support" or "Short-Term Option"

---

### M13. "4-6 months of significant relief" outcome claim

**File:** `/cvc-new/dry-eye-treatment/index.html:1350`

**Problematic text:**
> "many patients enjoy 4-6 months of significant relief before maintenance treatments are needed"

**Why problematic:** While hedged with "many patients," stating a specific timeframe (4-6 months) could be seen as a guaranteed outcome for anyone who is in the "many patients" category.

**Suggested edit:** This is borderline acceptable. Consider: "some patients enjoy several months of improved comfort before maintenance treatments are needed. Results vary."

---

### M14. "more than 80% of learning is visual" unsourced statistic

**File:** `/cvc-new/blog/back-to-school-eye-exams/index.html:502`

**Problematic text:**
> "As more than 80% of learning is visual"

**Why problematic:** This is a commonly cited but poorly sourced statistic. Using it as a factual claim without citation is potentially misleading.

**Suggested edit:** "Because so much of learning depends on vision" (remove unverifiable statistic).

---

### M15. "Ignoring the progression...will lead to lifelong side effects"

**File:** `/cvc-new/blog/a-parents-guide-to-myopia-progression/index.html:498`

**Problematic text:**
> "Ignoring the progression of your child's myopia will lead to lifelong side effects and additional diagnoses."

**Why problematic:** Scare tactic with guaranteed negative outcome. Not all untreated myopia leads to "lifelong side effects." Low and moderate myopia may stabilize without severe complications.

**Suggested edit:** "Without management, myopia may continue to progress during childhood, which can increase the risk of eye health complications later in life."

---

### M16. "myopia control programs that slow nearsightedness progression"

**File:** `/cvc-new/why-choose-us/index.html:589`

**Problematic text:**
> "Pediatric eye care with age-appropriate testing and myopia control programs that slow nearsightedness progression"

**Why problematic:** States as fact that the programs "slow" progression. Should hedge.

**Suggested edit:** "Pediatric eye care with age-appropriate testing and myopia control programs designed to help slow nearsightedness progression"

---

### M17. "experts" / "expert team" in meta descriptions and body copy

**Files:**
- `/cvc-new/blog/index.html:790` ("Classic Vision Care's experts")
- `/cvc-new/eye-treatment/5-steps-to-prevent-diabetic-eye-disease/index.html:480`
- `/cvc-new/blog/the-three-types-of-dry-eye/index.html:556` ("our expert team of doctors")
- `/cvc-new/blog/beating-digital-eye-strain-in-a-screen-filled-world/index.html:531` ("our expertise and advanced technology")
- `/cvc-new/allergies/index.html:7` ("Expert diagnosis and treatment")

**Problematic text:** Various uses of "expert(s)" and "expertise"

**Why problematic:** While less strictly regulated than "specialist," "expert" can imply specialty-level credentials the doctors may not hold. Used sparingly it may be acceptable puffery, but the frequency across the site creates a pattern.

**Suggested edit:** Reduce frequency. Replace most instances with "experienced" or "our doctors" or "our team."

---

### M18. "the trusted provider" (definite article)

**Files:**
- `/cvc-new/blog/back-to-school-eye-exams/index.html:498` ("Classic Vision Care is the trusted provider of back-to-school eye exams in Marietta")
- `/cvc-new/blog/the-three-types-of-dry-eye/index.html:553` ("Classic Vision Care is a trusted provider") -- this one is fine

**Problematic text:**
> "Classic Vision Care is the trusted provider of back-to-school eye exams in Marietta"

**Why problematic:** "The trusted provider" (with definite article) implies singular superiority.

**Suggested edit:** "Classic Vision Care is a trusted provider of back-to-school eye exams in Marietta"

---

## LOW-SEVERITY FINDINGS

### L1. "Dry Eye Spa" branding -- potential "spa" regulation concern

**Files:** Multiple (homepage, dry-eye-treatment, etc.)

**Problematic text:** "Dry Eye Spa" used as a service name throughout.

**Why potentially problematic:** In some jurisdictions, using "spa" for a medical service could create confusion about the nature of the service. However, this is a branding choice and is used descriptively. Low risk if the treatments are clearly medical in context.

**Suggested edit:** No change required, but consider adding a note like "Our Dry Eye Spa is a clinical treatment experience" if regulators inquire.

---

### L2. "advanced treatment options" -- mild puffery

**Files:** Multiple (blog posts, service pages)

**Why potentially problematic:** "Advanced" is mild puffery and generally acceptable, but when combined with other superlatives on the same page, it contributes to an overall pattern.

**Suggested edit:** Acceptable as-is in isolation. Only flag if on a page with multiple other superlatives.

---

### L3. "Latest Technology" section heading

**Files:**
- `/cvc-new/about-us/index.html:1009`
- `/cvc-new/pages/about/index.html:956`

**Problematic text:** "Latest Technology" (section heading)

**Why potentially problematic:** "Latest" is a comparative claim. It would be more defensible to say "Modern" or "Current."

**Suggested edit:** "Modern Technology"

---

### L4. "our optical prices compete with online retailers" -- comparative pricing

**File:** `/cvc-new/why-choose-us/index.html:571`

**Problematic text:**
> "Our optical prices compete with online retailers"

**Why potentially problematic:** Comparative pricing claim that could be challenged. If true and verifiable, it may be acceptable.

**Suggested edit:** Acceptable if substantiated. Consider adding "on many items" for hedging: "Our optical prices are competitive with online retailers on many items."

---

### L5. Testimonial section without disclaimer

**Files:**
- `/cvc-new/testimonials/index.html`
- `/cvc-new/blepharitis/index.html:511` (embedded testimonials header)
- `/cvc-new/eye-infections/index.html:544` (embedded testimonials header)

**Problematic text:** Testimonial sections exist but no disclaimer that "results may vary" or "individual experiences may differ."

**Why potentially problematic:** FTC endorsement guidelines recommend disclaimers on testimonials that could be interpreted as typical results. The testimonials page summarizes themes from reviews without quoting specific patients, which is better, but a general disclaimer would strengthen compliance.

**Suggested edit:** Add a small disclaimer near testimonial sections: "Individual experiences may vary. These themes reflect feedback from patient reviews."

---

### L6. "Non-invasive examination" in schema markup

**Files:**
- `/cvc-new/comprehensive-eye-exams/index.html:30`
- `/cvc-new/pages/services/exams/comprehensive.html:27`

**Problematic text:**
> `"howPerformed": "Non-invasive examination using advanced diagnostic equipment"`

**Why potentially problematic:** "Non-invasive" in structured data is generally accurate for a standard eye exam but could be seen as making a medical claim in the markup. Low risk.

**Suggested edit:** Acceptable as-is.

---

### L7. "recover quickly" in eye infections page

**File:** `/cvc-new/eye-infections/index.html:500`

**Problematic text:**
> "we offer advanced eye infection treatments that help you recover quickly"

**Why potentially problematic:** "Recover quickly" is a mild outcome promise. Recovery time varies by infection type and severity.

**Suggested edit:** "we offer eye infection treatments designed to support your recovery"

---

### L8. "can be life-changing" in specialty contacts intro

**File:** `/cvc-new/specialty-contact-lenses/index.html:506`

**Problematic text:**
> "Specialty contact lenses can be life-changing for comfort and clarity in hard-to-fit eyes."

**Why potentially problematic:** "Life-changing" is subjective puffery. Generally acceptable since it uses "can be" (hedged), but it is a strong emotional claim.

**Suggested edit:** Acceptable as-is with the "can be" hedge.

---

### L9. "highly trained" puffery

**Files:**
- `/cvc-new/eye-infections/index.html:542`

**Problematic text:**
> "Our highly trained eye doctors have extensive experience"

**Why potentially problematic:** "Highly trained" is mild puffery. Generally acceptable but contributes to pattern.

**Suggested edit:** "Our experienced eye doctors" (simpler, same meaning).

---

### L10. "stop their myopia progression before it develops" -- scare language

**File:** `/cvc-new/blog/a-parents-guide-to-myopia-progression/index.html:515`

**Problematic text:**
> "Stop their myopia progression before it develops into mild or high myopia, and possibly more serious eye damage."

**Why potentially problematic:** "Stop" implies complete cessation, which is not what myopia management achieves. Combined with "serious eye damage" this creates fear-based urgency.

**Suggested edit:** "Take steps to help manage their myopia progression before it advances further."

---

### L11. "proven to slow childhood myopia progression" in meta tags

**Files:**
- `/cvc-new/myopia-control-atropine-eye-drops/index.html:7,12`
- `/cvc-new/pages/myopia/treatments/atropine.html:7,12`

**Problematic text (meta description):**
> "Once-daily drops proven to slow childhood myopia progression."

**Why problematic:** "Proven to slow" in a meta description is a definitive claim without space for hedging. Meta descriptions appear in search results and are the first thing patients see.

**Suggested edit:** "Once-daily drops studied for slowing childhood myopia progression." or "Once-daily drops that may help slow childhood myopia progression."

---

### L12. "take control of your child's visual future" -- implied guarantee

**Files:**
- `/cvc-new/myopia-in-children/index.html:766`
- `/cvc-new/pages/myopia/children.html:713`

**Problematic text:**
> "take control of your child's visual future"

**Why potentially problematic:** Implies that treatment guarantees control over outcomes. Mild issue but worth noting.

**Suggested edit:** "take a proactive step for your child's eye health"

---

## PAGES WITH NO SIGNIFICANT ISSUES

The following pages/sections were reviewed and found to be well-written with appropriate hedging:

- `/cvc-new/why-choose-us/index.html` -- Generally excellent. Uses factual claims and appropriate language.
- `/cvc-new/specialty-contact-lenses/index.html` -- Very well written with proper hedging throughout.
- `/cvc-new/dry-eye-treatment-punctal-plugs/index.html` -- Good body copy (meta descriptions need work per M6).
- `/cvc-new/dry-eye-treatment-eye-supplements/index.html` -- Appropriate.
- `/cvc-new/dry-eye-treatment-eye-drops/index.html` -- Good.
- `/cvc-new/glaucoma/index.html` -- Appropriate disease education. "No cure" stated correctly.
- `/cvc-new/macular-degeneration/index.html` -- Appropriate. "No cure" stated correctly.
- `/cvc-new/privacy-policy-2/index.html` -- No marketing claims.
- `/cvc-new/accessibility/index.html` -- No marketing claims.
- `/cvc-new/contact-us/index.html` -- No marketing claims.
- `/cvc-new/careers/index.html` -- Appropriate.
- `/cvc-new/community-involvement/index.html` -- Appropriate.
- `/cvc-new/new-patients/index.html` -- Appropriate.
- `/cvc-new/insurance/index.html` -- Appropriate.
- Most `/cvc-new/pages/` redesigned duplicates mirror the same issues listed above.

---

## PATTERNS AND THEMES

### 1. Legacy Blog Content Is the Biggest Risk
The older blog posts (imported from the previous site) contain the most problematic language: cure claims, superlatives, unhedged treatment guarantees. The redesigned service pages are significantly better.

### 2. "Specializing" Is Used Consistently and Needs Global Fix
The word "specializing" appears in doctor bios, meta descriptions, location pages, and structured data across ~15 files. A global find-and-replace with "focused on" would address this efficiently.

### 3. "Proven" Is Overused
The word "proven" appears in headings, body copy, meta descriptions, and structured data. It should either be replaced with "evidence-based" / "clinically studied" or paired with a citation.

### 4. The "Definite Article" Pattern
Using "the trusted choice" / "the trusted provider" (with "the") implies singular superiority. Changing to "a" is a one-character fix with significant compliance impact.

### 5. Meta Descriptions Need Review
Several meta descriptions contain stronger claims than the body copy they describe, because body copy has room for hedging but meta descriptions are short and punchy. These are particularly important because they appear in search results.

---

## RECOMMENDED PRIORITY ORDER FOR FIXES

1. **H1-H2**: "Specializing" and "Board-certified" -- highest legal risk, global fix
2. **H3-H6**: Cure/guarantee language in legacy content
3. **H7-H11**: Superlative and comparative claims
4. **H12-H14**: Myopia outcome guarantees and unsubstantiated "clinically proven"
5. **M1-M6**: "Proven" headings, "state-of-the-art," pain-free claims
6. **M7-M18**: Other medium findings
7. **L1-L12**: Low-severity improvements

---

*This audit catalogs content issues only. It does not constitute legal advice. Cross-reference findings with the regulatory research in Task #1 before making final edits.*
