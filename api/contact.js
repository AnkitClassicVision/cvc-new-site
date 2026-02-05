const MAX_BODY_BYTES = 1024 * 64;

function isTruthy(value) {
  return value === true || value === "true" || value === "1" || value === 1;
}

async function readRawBody(req) {
  if (req.body) {
    if (typeof req.body === "string") return req.body;
    if (Buffer.isBuffer(req.body)) return req.body.toString("utf8");
    // Vercel/Node may already parse JSON
    return JSON.stringify(req.body);
  }

  return await new Promise((resolve, reject) => {
    let bytes = 0;
    let body = "";
    req.on("data", (chunk) => {
      bytes += chunk.length;
      if (bytes > MAX_BODY_BYTES) {
        reject(new Error("Body too large"));
        req.destroy();
        return;
      }
      body += chunk.toString("utf8");
    });
    req.on("end", () => resolve(body));
    req.on("error", reject);
  });
}

function parseBody(raw, contentType) {
  const ct = String(contentType || "").toLowerCase();
  if (ct.includes("application/json")) {
    return raw ? JSON.parse(raw) : {};
  }
  if (ct.includes("application/x-www-form-urlencoded")) {
    const params = new URLSearchParams(raw || "");
    return Object.fromEntries(params.entries());
  }
  // Default: try urlencoded first, then JSON
  try {
    const params = new URLSearchParams(raw || "");
    const obj = Object.fromEntries(params.entries());
    if (Object.keys(obj).length > 0) return obj;
  } catch {}
  try {
    return raw ? JSON.parse(raw) : {};
  } catch {}
  return {};
}

function wantsJson(req) {
  const accept = String(req.headers.accept || "").toLowerCase();
  return accept.includes("application/json") || accept.includes("text/json");
}

function buildRedirectLocation(req, ok) {
  const referer = req.headers.referer;
  if (!referer) return ok ? "/?sent=1" : "/?error=1";
  try {
    const url = new URL(referer);
    const params = url.searchParams;
    params.set(ok ? "sent" : "error", "1");
    return `${url.pathname}?${params.toString()}${url.hash || ""}`;
  } catch {
    return ok ? "/?sent=1" : "/?error=1";
  }
}

async function postWebhook(webhookUrl, payload) {
  const headers = { "content-type": "application/json" };
  if (process.env.CONTACT_WEBHOOK_AUTH_HEADER && process.env.CONTACT_WEBHOOK_AUTH_VALUE) {
    headers[process.env.CONTACT_WEBHOOK_AUTH_HEADER] = process.env.CONTACT_WEBHOOK_AUTH_VALUE;
  }

  const response = await fetch(webhookUrl, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`Webhook failed: ${response.status} ${text}`.slice(0, 300));
  }
}

async function sendResendEmail(payload) {
  const apiKey = process.env.RESEND_API_KEY;
  const to = process.env.CONTACT_EMAIL_TO;
  const from = process.env.CONTACT_EMAIL_FROM || "Classic Vision Care <no-reply@classicvisioncare.com>";
  if (!apiKey || !to) return;

  const subject = `[CVC] ${payload.formType === "booking" ? "Booking request" : "Contact form"} — ${payload.name || "New lead"}`;
  const lines = [
    `Form: ${payload.formType}`,
    payload.page ? `Page: ${payload.page}` : null,
    payload.location ? `Location: ${payload.location}` : null,
    payload.service ? `Service: ${payload.service}` : null,
    payload.reason ? `Reason: ${payload.reason}` : null,
    payload.preferredDate ? `Preferred date/time: ${payload.preferredDate}` : null,
    `Name: ${payload.name || ""}`,
    `Email: ${payload.email || ""}`,
    `Phone: ${payload.phone || ""}`,
    "",
    "Message:",
    payload.message || "",
    "",
    payload.meta?.ip ? `IP: ${payload.meta.ip}` : null,
    payload.meta?.userAgent ? `UA: ${payload.meta.userAgent}` : null,
  ].filter(Boolean);

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      authorization: `Bearer ${apiKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: [to],
      subject,
      text: lines.join("\n"),
    }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Resend failed: ${res.status} ${text}`.slice(0, 300));
  }
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.setHeader("Allow", "POST");
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: false, error: "Method not allowed" }));
    return;
  }

  try {
    const raw = await readRawBody(req);
    const body = parseBody(raw, req.headers["content-type"]);

    // Honeypot
    if (body.website || body.company_website) {
      res.statusCode = 200;
      res.setHeader("Content-Type", "application/json; charset=utf-8");
      res.end(JSON.stringify({ ok: true }));
      return;
    }

    const name = String(body.name || `${body.firstName || ""} ${body.lastName || ""}`).trim();
    const email = String(body.email || "").trim();
    const phone = String(body.phone || "").trim();
    const location = String(body.location || body.preferredLocation || "").trim();
    const reason = String(body.reason || "").trim();
    const service = String(body.service || "").trim();
    const preferredDate = String(body.preferredDate || body.requestedDate || "").trim();
    const message = String(body.message || "").trim();
    const formType = String(body.form_type || body.formType || "contact").trim() || "contact";

    if (!name || !email) {
      const error = "Please include your name and email.";
      if (!wantsJson(req)) {
        res.statusCode = 303;
        res.setHeader("Location", buildRedirectLocation(req, false));
        res.end();
        return;
      }
      res.statusCode = 400;
      res.setHeader("Content-Type", "application/json; charset=utf-8");
      res.end(JSON.stringify({ ok: false, error }));
      return;
    }

    const payload = {
      submittedAt: new Date().toISOString(),
      formType,
      page: body.page || req.headers.referer || "",
      name,
      email,
      phone,
      location,
      reason,
      service,
      preferredDate,
      message,
      consentToContact: isTruthy(body.consentToContact) || isTruthy(body.consent),
      meta: {
        ip: String(req.headers["x-forwarded-for"] || "").split(",")[0].trim(),
        userAgent: String(req.headers["user-agent"] || ""),
      },
    };

    const webhookUrl = process.env.CONTACT_WEBHOOK_URL;
    const hasWebhook = Boolean(webhookUrl);
    const hasResend = Boolean(process.env.RESEND_API_KEY && process.env.CONTACT_EMAIL_TO);

    if (!hasWebhook && !hasResend) {
      const error = "Contact form is not configured. Please call us to book an appointment.";
      if (!wantsJson(req)) {
        res.statusCode = 303;
        res.setHeader("Location", buildRedirectLocation(req, false));
        res.end();
        return;
      }
      res.statusCode = 503;
      res.setHeader("Content-Type", "application/json; charset=utf-8");
      res.end(JSON.stringify({ ok: false, error }));
      return;
    }

    if (hasWebhook) await postWebhook(webhookUrl, payload);
    if (hasResend) await sendResendEmail(payload);

    if (!wantsJson(req)) {
      res.statusCode = 303;
      res.setHeader("Location", buildRedirectLocation(req, true));
      res.end();
      return;
    }

    res.statusCode = 200;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: true }));
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    if (!wantsJson(req)) {
      res.statusCode = 303;
      res.setHeader("Location", buildRedirectLocation(req, false));
      res.end();
      return;
    }
    res.statusCode = 500;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: false, error: message }));
  }
};

