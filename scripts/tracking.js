(function () {
  function push(eventName, data) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: eventName }, data || {}));
  }

  function closestAnchor(el) {
    if (!el) return null;
    if (el.closest) return el.closest("a");
    while (el && el.tagName !== "A") el = el.parentNode;
    return el && el.tagName === "A" ? el : null;
  }

  document.addEventListener(
    "click",
    function (e) {
      const a = closestAnchor(e.target);
      if (!a) return;
      const href = String(a.getAttribute("href") || "");

      if (href.startsWith("tel:")) {
        push("cvc_phone_click", { cvc_phone: href.replace(/^tel:/, "") });
        return;
      }

      if (href.includes("/book-now/")) {
        push("cvc_book_click", { cvc_href: href });
      }
    },
    true
  );
})();

