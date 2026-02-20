(function () {
  var FORM_ENDPOINT =
    "https://dfi7etyxk2ugdsbdy7s7m43sxy0egmvg.lambda-url.us-east-1.on.aws/";

  function setStatus(el, type, message) {
    if (!el) return;
    el.classList.remove("hidden");
    el.classList.remove("bg-green-50", "border-green-200", "text-green-900");
    el.classList.remove("bg-red-50", "border-red-200", "text-red-900");

    if (type === "success") {
      el.classList.add("bg-green-50", "border", "border-green-200", "text-green-900");
    } else if (type === "error") {
      el.classList.add("bg-red-50", "border", "border-red-200", "text-red-900");
    }

    el.textContent = message;
  }

  function optionExists(select, value) {
    if (!select) return false;
    return Array.from(select.options).some((opt) => opt.value === value);
  }

  function attachFormHandler(form) {
    const statusId = form.getAttribute("data-status-id");
    const statusEl = statusId ? document.getElementById(statusId) : null;
    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');

    form.addEventListener("submit", async function (e) {
      if (!window.fetch || !window.URLSearchParams || !window.FormData) return;
      e.preventDefault();

      try {
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.setAttribute("aria-busy", "true");
        }

        const data = new URLSearchParams();
        const fd = new FormData(form);
        for (const [key, value] of fd.entries()) {
          data.append(key, String(value));
        }

        if (!data.get("page")) data.set("page", window.location.href);
        if (!data.get("form_type")) {
          const type = form.getAttribute("data-cvc-form");
          if (type) data.set("form_type", type);
        }

        const response = await fetch(FORM_ENDPOINT, {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
          },
          body: data.toString(),
        });

        const json = await response.json().catch(() => ({}));
        if (!response.ok || !json.ok) {
          throw new Error(json.error || "Unable to submit the form.");
        }

        form.reset();
        setStatus(statusEl, "success", "Thanks! We got your message and will reach out soon.");

        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
          event: "cvc_form_submit",
          cvc_form_type: data.get("form_type") || "",
          cvc_location: data.get("location") || "",
          cvc_service: data.get("service") || data.get("reason") || "",
        });
      } catch (err) {
        const fallback =
          "Sorry — something went wrong. Please call Kennesaw (770) 499-2020 or East Cobb (678) 560-8065.";
        setStatus(statusEl, "error", fallback);
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.removeAttribute("aria-busy");
        }
      }
    });
  }

  function applyQueryAutofill() {
    const params = new URLSearchParams(window.location.search);
    const location = params.get("location");
    const service = params.get("service");

    if (location) {
      const selects = document.querySelectorAll('select[name="location"]');
      selects.forEach((sel) => {
        if (optionExists(sel, location)) sel.value = location;
      });
    }

    if (service) {
      const selects = document.querySelectorAll('select[name="service"]');
      selects.forEach((sel) => {
        if (optionExists(sel, service)) sel.value = service;
      });
    }

    if ((location || service) && document.getElementById("booking-form")) {
      document.getElementById("booking-form").scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  function showFlashMessages() {
    const params = new URLSearchParams(window.location.search);
    const isSent = params.get("sent") === "1";
    const isError = params.get("error") === "1";
    if (!isSent && !isError) return;

    const firstStatus = document.querySelector("[data-cvc-status]");
    if (!firstStatus) return;
    setStatus(
      firstStatus,
      isSent ? "success" : "error",
      isSent
        ? "Thanks! We got your message and will reach out soon."
        : "Sorry — something went wrong. Please call Kennesaw (770) 499-2020 or East Cobb (678) 560-8065."
    );
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("form[data-cvc-form]").forEach(attachFormHandler);
    applyQueryAutofill();
    showFlashMessages();
  });
})();

