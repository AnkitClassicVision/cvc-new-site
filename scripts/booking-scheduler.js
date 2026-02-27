/**
 * booking-scheduler.js
 * Post-submission Eye Cloud Pro scheduler enhancement.
 * Reversible: remove this <script> tag to revert to default form behavior.
 */
(function () {
  "use strict";

  var LOCATION_SIDS = {
    kennesaw: "272D0EB500F5C1EBD886AEF4A7D020D2",
    eastcobb: "B78B4DB74589050F338AD46B1F366721",
    either: "272D0EB500F5C1EBD886AEF4A7D020D2", // default to Kennesaw
  };
  var DEFAULT_SID = LOCATION_SIDS.kennesaw;
  var IFRAME_TIMEOUT_MS = 8000;
  var TRANSITION_MS = 400;

  var form = document.getElementById("booking-request-form");
  var statusEl = document.getElementById("booking-form-status");
  var formContainer = document.getElementById("booking-form");
  if (!form || !statusEl || !formContainer) return;

  // --- Guard: only activate after a real form submission, not ?sent=1 flash ---
  var formWasSubmitted = false;

  // --- State: capture form data before forms.js resets it ---
  var capturedLocation = "";
  var capturedName = "";

  form.addEventListener(
    "submit",
    function () {
      formWasSubmitted = true;
      var locSelect = form.querySelector('[name="location"]');
      var nameInput = form.querySelector('[name="name"]');
      capturedLocation = locSelect ? locSelect.value : "";
      capturedName = nameInput ? nameInput.value : "";
    },
    true // capture phase — runs before forms.js
  );

  // --- Observe success state set by forms.js ---
  var observer = new MutationObserver(function () {
    if (!formWasSubmitted) return; // ignore ?sent=1 flash messages
    if (statusEl.classList.contains("bg-green-50")) {
      observer.disconnect();
      startTransition();
    } else if (statusEl.classList.contains("bg-red-50")) {
      // Error state — don't trigger scheduler, let forms.js error show
      observer.disconnect();
    }
  });

  observer.observe(statusEl, {
    attributes: true,
    attributeFilter: ["class"],
  });

  // --- Transition: form out, scheduler in ---
  function startTransition() {
    var sid = LOCATION_SIDS[capturedLocation] || DEFAULT_SID;
    var displayName = capturedName ? capturedName.split(" ")[0] : "";

    // Hide the existing status message (forms.js already set it)
    statusEl.classList.add("hidden");

    // Slide form container out
    formContainer.style.transition = "opacity " + TRANSITION_MS + "ms ease, transform " + TRANSITION_MS + "ms ease";
    formContainer.style.opacity = "0";
    formContainer.style.transform = "translateY(-20px)";

    setTimeout(function () {
      formContainer.style.display = "none";

      // Build and insert the scheduler section
      var schedulerHTML = buildSchedulerHTML(sid, displayName);
      var schedulerEl = document.createElement("div");
      schedulerEl.id = "booking-scheduler";
      schedulerEl.setAttribute("role", "region");
      schedulerEl.setAttribute("aria-label", "Appointment confirmation and online scheduler");
      schedulerEl.innerHTML = schedulerHTML;
      schedulerEl.style.opacity = "0";
      schedulerEl.style.transform = "translateY(20px)";
      schedulerEl.style.transition = "opacity " + TRANSITION_MS + "ms ease, transform " + TRANSITION_MS + "ms ease";

      formContainer.parentNode.insertBefore(schedulerEl, formContainer.nextSibling);

      // Fade in
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          schedulerEl.style.opacity = "1";
          schedulerEl.style.transform = "translateY(0)";
        });
      });

      // Move focus to the thank-you heading for screen readers and keyboard users
      var heading = schedulerEl.querySelector("h2");
      if (heading) {
        heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
      }

      // Scroll to the thank-you section
      schedulerEl.scrollIntoView({ behavior: "smooth", block: "start" });

      // Start iframe load with timeout
      initIframe(schedulerEl, sid);
    }, TRANSITION_MS);
  }

  function buildSchedulerHTML(sid, firstName) {
    var greeting = firstName ? "Thank you, " + escapeHtml(firstName) + "!" : "Thank you!";
    var iframeUrl = "https://web.opticalpos.com/site/!appt_req?sid=" + sid;

    return (
      '<div class="mt-8 mb-8">' +
        // Thank you card
        '<div class="bg-white rounded-2xl shadow-lg p-8 lg:p-10 text-center mb-8" role="status" aria-live="polite">' +
          '<div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-50 mb-4">' +
            '<svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">' +
              '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>' +
            "</svg>" +
          "</div>" +
          '<h2 class="font-display text-2xl md:text-3xl text-cvc-charcoal mb-3">' + greeting + "</h2>" +
          '<p class="text-gray-600 max-w-xl mx-auto text-lg">We\u2019ve received your appointment request and will get back to you as soon as possible.</p>' +
        "</div>" +
        // Scheduler section
        '<div id="scheduler-section">' +
          '<div class="text-center mb-6">' +
            '<p class="text-gray-600">Want to pick a time now? You can also book directly below.</p>' +
            '<p class="text-sm text-gray-400 mt-1">You may need to re-enter some details in the scheduler.</p>' +
          "</div>" +
          '<div id="iframe-loading" class="flex flex-col items-center justify-center py-12" aria-live="polite">' +
            '<div class="w-10 h-10 border-4 border-cvc-teal-200 border-t-cvc-teal-500 rounded-full animate-spin mb-4" aria-hidden="true"></div>' +
            '<p class="text-gray-500 text-sm">Loading online scheduler\u2026</p>' +
          "</div>" +
          '<iframe id="eyecloud-iframe"' +
            ' src="' + iframeUrl + '"' +
            ' title="Book an appointment online with Eye Cloud Pro"' +
            ' class="w-full rounded-xl shadow-lg border border-gray-200 hidden"' +
            ' style="min-height:900px"' +
            ' loading="eager"' +
            ' allow="clipboard-write"' +
          "></iframe>" +
        "</div>" +
      "</div>"
    );
  }

  function initIframe(container, sid) {
    var iframe = container.querySelector("#eyecloud-iframe");
    var loading = container.querySelector("#iframe-loading");
    var schedulerSection = container.querySelector("#scheduler-section");
    if (!iframe || !loading || !schedulerSection) return;

    var loaded = false;
    var timedOut = false;

    // On successful load
    iframe.addEventListener("load", function () {
      if (timedOut) return;
      loaded = true;
      loading.style.display = "none";
      iframe.classList.remove("hidden");

      // Adjust height for mobile
      if (window.innerWidth < 768) {
        iframe.style.minHeight = "700px";
      }
    });

    // Timeout: quietly remove scheduler section
    setTimeout(function () {
      if (loaded) return;
      timedOut = true;
      schedulerSection.style.transition = "opacity 300ms ease";
      schedulerSection.style.opacity = "0";
      setTimeout(function () {
        schedulerSection.remove();
      }, 300);
    }, IFRAME_TIMEOUT_MS);
  }

  function escapeHtml(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
})();
