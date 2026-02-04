# World‑Class Touches (Micro‑Interactions Map)

Goal: keep the current “Forest Editorial” look and IA intact, while making the experience feel premium on desktop + mobile via subtle motion, feedback, and polish.

## Touchpoints

| Area | What users feel | Implementation | Where |
|---|---|---|---|
| Page transitions | “App-like” navigation (subtle) | Fade/slide out on internal link click (disabled for reduced-motion / new-tab) | `scripts/editorial-forest.js` + `styles/editorial-forest.css` |
| Header / Nav | Orientation + confidence | Current page highlight; dropdown motion; sticky scrolled state | `scripts/editorial-forest.js` + `styles/editorial-forest.css` |
| Mobile menu | Fast + tactile | Accordion works consistently; `aria-expanded` updates | `scripts/editorial-forest.js` |
| CTAs & buttons | “Responsive” + premium | Shine sweep on hover; magnetic hover (desktop only); press feedback (touch) | `styles/editorial-forest.css` + `scripts/editorial-forest.js` |
| Cards (services, locations, etc.) | Depth + delight | Lift/soft shadow; hover polish; (optional) spotlight tracking | `styles/editorial-forest.css` + `scripts/editorial-forest.js` |
| Hero (text + media) | “Cinematic” + calm | Aurora mesh; animated gradient text; hero image reveal + Ken Burns; decorative circle drift; optional parallax | `styles/editorial-forest.css` + `scripts/editorial-forest.js` |
| Scroll storytelling | Smooth reveals | IntersectionObserver reveal system; divider animations | `scripts/editorial-forest.js` + `styles/editorial-forest.css` |
| Images | “Finished” loading | Gentle fade-in on late-loading images | `scripts/editorial-forest.js` + `styles/editorial-forest.css` |
| Accessibility | Premium *and* inclusive | Reduced-motion support, visible focus, tap targets | `styles/editorial-forest.css` + `scripts/editorial-forest.js` |

## Component Lab (for testing)

Micro-interactions are easiest to iterate in a sandbox page. Component lab pages live in `.superdesign/design_iterations/` (ignored from deploy by default).

- `cvc_grow/cvc-new/.superdesign/design_iterations/cvc_micro_lab_1.html:1`: buttons, cards, reveal types, internal links.
- `cvc_grow/cvc-new/.superdesign/design_iterations/cvc_transition_links_1.html:1`: quick matrix of internal links to validate transitions + nav highlighting.
- `cvc_grow/cvc-new/.superdesign/design_iterations/cvc_hero_motion_lab_1.html:1`: hero text + image motion comparisons.
