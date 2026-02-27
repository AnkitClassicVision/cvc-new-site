# Specification: Native Appointment Booking Integration

## System Overview

Classic Vision Care (classicvisioncare.com) needs a frictionless appointment booking flow that captures every lead while connecting patients to real-time scheduling via Eye Cloud Pro (web.opticalpos.com). The system serves patients visiting the website across two locations (Kennesaw and East Cobb/Marietta), ensuring no opportunity is lost — whether the patient books online, can't find a time, or has an urgent need. The existing static site on Vercel with Tailwind CSS is the foundation.

---

## Behavioral Contract

### Primary Flows

**When** a patient clicks any "Book Now" CTA on the site, **the system** navigates to the existing `/book-now/` page. The current booking request form remains as-is (location, service, name, email, phone, preferred date/time, message). A new "This is urgent" checkbox is added to the form.

**When** the patient selects a location, **the system** pre-selects that location if the patient arrived from a location-specific page (e.g., `/eye-doctor-kennesaw-ga/`) or the URL contains a `?location=` parameter.

**When** the patient submits the booking request form, **the system** immediately sends a lead notification email to the clinic (via the existing `/api/contact` endpoint) containing all collected information, including the urgent flag if checked.

**When** the urgent checkbox is checked, **the system** adds "[URGENT]" to the email subject line so the team can identify and act on it immediately.

**When** the lead email is sent successfully, **the system** performs a smooth slide/fade transition: the booking request form collapses and is replaced by a two-part view — (1) a thank-you confirmation and (2) the Eye Cloud Pro scheduler iframe below. The URL stays at `/book-now/`.

**When** the transition happens, **the system** displays a branded thank-you confirmation that communicates (in human language): "Thank you! We've received your request and will get back to you as soon as possible." Below this, a secondary prompt introduces the scheduler: "Want to pick a time now? You can also book directly below." with a brief note: "You may need to re-enter some details in the scheduler."

**When** the transition message is shown, **the system** loads the Eye Cloud Pro scheduling iframe for the selected location below the message.

**When** the Eye Cloud Pro iframe is loading, **the system** shows a branded loading state (skeleton/spinner in the site's design language) so the patient knows something is happening.

**When** the Eye Cloud Pro iframe loads successfully, **the system** auto-resizes the iframe container to match the content height where possible. As a fallback, uses a generous minimum height (900px on desktop, 700px on mobile) with smooth internal scrolling if needed.

**When** the patient completes a booking inside the Eye Cloud Pro iframe, **the system** does not interfere — Eye Cloud Pro handles confirmation within its own UI.

**When** the patient scrolls past or ignores the scheduler, **the system** requires no further action — the thank-you message already confirmed their request was received. No additional "we'll call you" messaging below the iframe.

### Error Flows

**When** the Eye Cloud Pro iframe fails to load within 8 seconds, **the system** quietly removes the scheduler section entirely (the "Want to pick a time now?" prompt and loading state disappear). The thank-you confirmation remains — the patient's request is already captured. No error messages, no broken iframe, no blank space.

**When** the Eye Cloud Pro iframe fails to load, **the system** does NOT show an error state or apologize — the thank-you message is already the complete experience. The scheduler was a bonus, not a requirement.

**When** the `/api/contact` endpoint fails to send the lead email, **the system** retries once, and if it fails again, shows the patient a fallback message with the clinic's phone number for the selected location so the opportunity is not lost.

**When** the patient submits the intake form without completing all required fields, **the system** shows inline validation messages on the specific fields that need attention — no alert boxes, no page reloads.

### Boundary Conditions

**When** the patient navigates directly to `/book-now/` without coming from a location page and without URL parameters, **the system** requires them to select a location before proceeding.

**When** the patient is on a mobile device, **the system** renders the entire flow (intake form + messaging + iframe) within a single scrollable view — no horizontal scroll, no content clipped off-screen.

**When** the patient has JavaScript disabled, **the system** shows a static fallback with the clinic phone numbers for both locations.

---

## Explicit Non-Behaviors

**The system must not** collect insurance information, date of birth, address, or any demographic data beyond name, email, phone, location, service, and urgency — because Eye Cloud Pro will collect detailed patient information in its own form, and double-collecting creates friction.

**The system must not** open Eye Cloud Pro in a new tab or navigate the patient away from classicvisioncare.com — because leaving the site breaks the branded experience and increases abandonment.

**The system must not** attempt to call Eye Cloud Pro's API directly, proxy requests through a server-side function, or bypass reCAPTCHA Enterprise — because there is no public API, no CORS support, and automating reCAPTCHA violates Google's Terms of Service.

**The system must not** hide or skip the Eye Cloud Pro iframe's own patient information form — because the iframe is a self-contained third-party application whose internal flow cannot be modified.

**The system must not** over-promise about callbacks in the post-submission messaging — the thank-you confirms the request was received and the team will respond ASAP. The scheduler is presented as a secondary convenience ("want to pick a time now?"), not as an expectation.

**The system must not** send the lead email AFTER the iframe loads — it must send BEFORE, so the lead is captured even if the patient bounces during the iframe loading or scheduling step.

**The system must not** auto-play sounds, show pop-ups, or create any jarring transitions — the flow must feel calm and professional, matching the clinical brand.

---

## Integration Boundaries

### Eye Cloud Pro (web.opticalpos.com) — Iframe Embed

**Data flowing in:** The iframe URL includes a `sid` parameter identifying the location:
- Kennesaw: `https://web.opticalpos.com/site/!appt_req?sid=272D0EB500F5C1EBD886AEF4A7D020D2`
- East Cobb: `https://web.opticalpos.com/site/!appt_req?sid=B78B4DB74589050F338AD46B1F366721`

**Data flowing out:** None. The iframe is opaque — the parent page cannot read events, form state, or confirmation status from inside the iframe due to cross-origin restrictions.

**Expected contract:** The iframe loads the Eye Cloud Pro appointment request wizard (reCAPTCHA → Service → DateTime → Patient Info → Confirmation). The parent page has no control over or visibility into this flow.

**When unavailable:** The iframe loading is monitored via a timeout. If the iframe does not fire its `load` event within 8 seconds, the system treats it as unavailable and shows the fallback message. The patient's lead info has already been captured via email.

**Pre-filling patient data:** Cross-origin iframe restrictions prevent the parent page from injecting data into the Eye Cloud Pro form. The patient will need to re-enter name, email, and phone inside the iframe. The transition message should include a brief note: "You may need to re-enter some details in the scheduler below."

**Development approach:** Use the real iframe URLs during development. No mock/simulated twin — the iframe behavior cannot be meaningfully simulated.

### Existing `/api/contact` Endpoint — Lead Email

**Data flowing in:** POST request with JSON body containing:
```
{
  "name": "string (required)",
  "email": "string (required)",
  "phone": "string (required)",
  "location": "kennesaw" | "eastcobb" (required),
  "service": "string (required)",
  "urgent": boolean,
  "message": "string (auto-generated, e.g., 'Online booking request — [urgent if flagged]')",
  "source": "booking-flow"
}
```

**Data flowing out:** JSON response with success/error status.

**Expected contract:** The endpoint validates inputs, verifies Cloudflare Turnstile token, sends email via Resend, and optionally fires webhook. Returns `{ success: true }` or `{ success: false, error: "message" }`.

**When unavailable:** Retry once after 2-second delay. If still failing, show phone number fallback.

### Cloudflare Turnstile — Bot Protection

**Data flowing in:** Turnstile widget renders on the intake form page, produces a token on implicit challenge completion.

**Data flowing out:** Token sent with the `/api/contact` POST request for server-side verification.

**When unavailable:** The form should still be submittable — degrade gracefully by skipping Turnstile verification if the widget fails to load (the existing honeypot and rate limiting provide secondary protection).

---

## Behavioral Scenarios

### Happy Path Scenarios

**Scenario 1: Patient books successfully from location page**

Setup: Patient is on `/eye-doctor-kennesaw-ga/` page.
Action: Patient clicks "Book Now" CTA → navigates to `/book-now/?location=kennesaw`. Kennesaw is pre-selected. Patient fills in name, email, phone, selects "Comprehensive Eye Exam," and submits.
Observable: The form smoothly slides/fades out. A thank-you message appears: "Thank you! We'll get back to you ASAP." Below it, a secondary prompt: "Want to pick a time now?" with the Eye Cloud Pro scheduler for Kennesaw loading underneath. Patient optionally completes the Eye Cloud Pro flow. The clinic received a lead email within seconds of the initial form submission — before the patient even touched the scheduler.

**Scenario 2: Patient can't find a time and relies on callback**

Setup: Patient navigates directly to `/book-now/` with no pre-selected location.
Action: Patient selects East Cobb, fills in the form, submits. Form slides out, transition message and Eye Cloud Pro scheduler for East Cobb appear. Patient browses available times but doesn't find one that works. Patient scrolls past the scheduler.
Observable: The thank-you message already confirmed the request was received — no additional messaging needed below the scheduler. The clinic received the lead email at form submission. The patient can close the page knowing their request is handled, or optionally book a time in the scheduler.

**Scenario 3: Urgent appointment request**

Setup: Patient is on any page and clicks "Book Now" → navigates to `/book-now/`.
Action: Patient fills in the form and checks the "This is urgent" checkbox. Submits.
Observable: The lead email received by the clinic has "[URGENT]" in the subject line. The transition message still appears and the scheduler still loads — the urgent flag doesn't skip the scheduling step. The patient can still book online if a time is available, but the clinic is alerted for priority follow-up.

### Error Scenarios

**Scenario 4: Eye Cloud Pro iframe fails to load**

Setup: Eye Cloud Pro is experiencing an outage or the patient's network is slow.
Action: Patient completes the intake form and submits successfully. The transition message appears. The iframe loading state shows for 8 seconds.
Observable: After 8 seconds, the loading state disappears. The "Want to pick a time now?" section is quietly removed. The patient still sees the thank-you confirmation — their request is already captured. No broken iframe, no error codes, no blank white space. The experience feels intentional and complete.

**Scenario 5: Lead email API fails**

Setup: Resend API or `/api/contact` endpoint is down.
Action: Patient fills in the intake form and submits.
Observable: The system retries once. On second failure, the patient sees: "We're having trouble processing your request. Please call us directly:" followed by the phone number for their selected location. The Eye Cloud Pro scheduler does NOT load — because without the lead captured, showing the scheduler risks losing the patient entirely if they abandon during the Eye Cloud flow.

### Edge Case Scenarios

**Scenario 6: Patient on mobile device with slow connection**

Setup: Patient is on an iPhone on 3G, visiting from a Google search result.
Action: Patient taps "Book Now," fills in the intake form, and submits.
Observable: The entire flow is usable in a single vertical scroll. No horizontal overflow, no content hidden behind the iframe boundary. The intake form fields are large enough to tap without zooming. The iframe, when it loads, is scrollable within its container. If the iframe is too slow, the fallback message appears. The patient is never stuck.

**Scenario 7: Patient rapidly clicks "Book Now" multiple times**

Setup: Patient clicks the "Book Now" CTA, then quickly clicks it again, or double-taps on mobile.
Action: Multiple rapid interactions with the booking trigger.
Observable: Only one intake form instance appears. The form submit button disables after first click to prevent duplicate lead emails. If the patient manages to trigger two submissions, the backend rate limiting (existing in `/api/contact`) prevents duplicate emails.

---

## Resolved Ambiguities

| # | Decision |
|---|----------|
| AW-1 | Navigate to `/book-now/` page — no modals. All "Book Now" CTAs go to `/book-now/` as they do today. |
| AW-2 | Auto-resize iframe where possible. Fallback to generous minimum height (900px desktop / 700px mobile) with smooth internal scrolling. |
| AW-3 | Urgent flag adds `[URGENT]` prefix to email subject line. No additional channels (SMS, webhook) for now. |
| AW-4 | Smooth slide/fade transition — form collapses, transition message + iframe appear in its place. |
| AW-5 | Keep existing `/book-now/` page and form as-is. The Eye Cloud Pro integration is a post-submission enhancement — after the patient submits the existing form, the scheduler appears. The existing form is NOT replaced. |
| AW-6 | Keep marketing-friendly service names (Comprehensive Eye Exam, Dry Eye Consultation, etc.). These are lead qualifiers, not Eye Cloud Pro field mappings. |
| AW-7 | Brief, non-alarming note embedded within the transition message: "You may need to re-enter some details in the scheduler below." |

## Remaining Ambiguity Warnings

### AW-8: Reversibility mechanism

**What's ambiguous:** The user wants this to be reversible if they don't like it. What mechanism should be used?

**Recommended approach:** Implement as a standalone JavaScript module (`/scripts/booking-scheduler.js`) that enhances the existing form's submit handler. To revert, remove the script tag — the existing form and `/api/contact` flow continue working unchanged. No modifications to the existing form HTML or `forms.js` logic — the new script hooks into the form's submit event and adds the post-submission iframe behavior.

**Question to resolve:** Is a removable script tag sufficient for rollback? Or do you want a feature flag (e.g., URL param `?scheduler=on` to enable, absent to disable)?

---

## Implementation Constraints

- **Platform:** Static site on Vercel — serverless functions in `/api/`, HTML pages, Tailwind CSS, vanilla JS
- **No framework migration:** Do not introduce React, Vue, Next.js, or any SPA framework. Build with vanilla JS + existing Tailwind classes
- **Styling:** Must use the existing Tailwind config (`cvc-teal`, `cvc-gold`, `cvc-cream`, `cvc-charcoal` color palette, TT Norms Pro + Montserrat fonts)
- **Existing infrastructure:** Use the existing `/api/contact` endpoint (modify if needed to support new fields like `urgent` and `source`)
- **Do not modify existing form HTML or `forms.js`** — the new behavior is additive, implemented as a separate script that enhances the post-submission flow
- **CAPTCHA:** Continue using Cloudflare Turnstile (already integrated)
- **Eye Cloud Pro iframe URLs are hardcoded** — the `sid` values are static identifiers for each location
- **No server-side proxy to Eye Cloud Pro** — all interaction is via iframe embed only
- **Performance target:** Intake form must be interactive within 1 second of page load. Total time from form submission to seeing the scheduler should be under 5 seconds on a 4G connection
- **Accessibility:** Form must be keyboard-navigable and screen-reader compatible (WCAG 2.1 AA minimum)
- **Browser support:** Modern browsers (Chrome, Safari, Firefox, Edge — last 2 versions) + iOS Safari and Chrome on Android
- **Reversibility:** Implementation must be fully reversible by removing a single script tag. The existing booking form and email flow must work identically with or without the enhancement script
- **Local testing:** Must be testable locally (e.g., via `npx serve .` or Vercel CLI `vercel dev`) before deploying. The iframe will load the real Eye Cloud Pro scheduler even in local dev since it's a cross-origin embed
