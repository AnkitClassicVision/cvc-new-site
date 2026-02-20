/**
 * CVC Contact Form — AWS Lambda Handler
 * HIPAA-compliant form processor for Classic Vision Care.
 *
 * Receives POST from the booking/contact form, validates inputs,
 * and sends notification email via AWS SES.
 *
 * Environment variables (set via Secrets Manager):
 *   CONTACT_EMAIL_TO  — recipient address (office inbox)
 *   SES_FROM_ADDRESS  — verified SES sender address
 */

import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses";
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from "@aws-sdk/client-secrets-manager";

const ses = new SESClient({ region: "us-east-1" });
const sm = new SecretsManagerClient({ region: "us-east-1" });

// ── Cache secrets across warm invocations ──────────────────────
let cachedSecrets = null;

async function getSecrets() {
  if (cachedSecrets) return cachedSecrets;
  const { SecretString } = await sm.send(
    new GetSecretValueCommand({ SecretId: "cvc/contact-form" })
  );
  cachedSecrets = JSON.parse(SecretString);
  return cachedSecrets;
}

// ── CORS ───────────────────────────────────────────────────────
// CORS is handled by the Lambda Function URL configuration.
// Do NOT set CORS headers here — duplicate headers cause browsers
// to reject the response.

// ── Validation ─────────────────────────────────────────────────
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function isValidEmail(email) {
  return EMAIL_RE.test(email) && email.length <= 254;
}

// ── Body parsing ───────────────────────────────────────────────
function parseBody(rawBody, contentType) {
  const ct = (contentType || "").toLowerCase();
  if (ct.includes("application/json")) {
    return rawBody ? JSON.parse(rawBody) : {};
  }
  if (ct.includes("application/x-www-form-urlencoded")) {
    return Object.fromEntries(new URLSearchParams(rawBody).entries());
  }
  // Fallback: try urlencoded, then JSON
  try {
    const obj = Object.fromEntries(new URLSearchParams(rawBody).entries());
    if (Object.keys(obj).length > 0) return obj;
  } catch {}
  try {
    return rawBody ? JSON.parse(rawBody) : {};
  } catch {}
  return {};
}

// ── SES email ──────────────────────────────────────────────────
async function sendEmail(secrets, payload) {
  const to = secrets.CONTACT_EMAIL_TO.split(",").map((e) => e.trim());
  const from = secrets.SES_FROM_ADDRESS || "Classic Vision Care <no-reply@classicvisioncare.com>";

  const subject = `[CVC] ${payload.formType === "booking" ? "Booking request" : "Contact form"} — ${payload.name || "New lead"}`;

  const lines = [
    `Form: ${payload.formType}`,
    payload.page ? `Page: ${payload.page}` : null,
    payload.location ? `Location: ${payload.location}` : null,
    payload.service ? `Service: ${payload.service}` : null,
    payload.patientType ? `Patient type: ${payload.patientType}` : null,
    payload.reason ? `Reason: ${payload.reason}` : null,
    payload.preferredDate ? `Preferred date/time: ${payload.preferredDate}` : null,
    payload.insurance ? `Insurance: ${payload.insurance}` : null,
    "",
    `Name: ${payload.name || ""}`,
    `Email: ${payload.email || ""}`,
    `Phone: ${payload.phone || ""}`,
    "",
    "Message:",
    payload.message || "(none)",
    "",
    `Consent to contact: ${payload.consentToContact ? "Yes" : "No"}`,
    "",
    "---",
    `Submitted: ${payload.submittedAt}`,
    payload.meta?.ip ? `IP: ${payload.meta.ip}` : null,
  ].filter(Boolean);

  await ses.send(
    new SendEmailCommand({
      Source: from,
      Destination: { ToAddresses: to },
      Message: {
        Subject: { Data: subject, Charset: "UTF-8" },
        Body: { Text: { Data: lines.join("\n"), Charset: "UTF-8" } },
      },
    })
  );
}

// ── Lambda handler ─────────────────────────────────────────────
export const handler = async (event) => {
  // CORS preflight is handled by Lambda Function URL config
  if (event.requestContext?.http?.method === "OPTIONS") {
    return { statusCode: 204 };
  }

  // POST only
  if (event.requestContext?.http?.method !== "POST") {
    return {
      statusCode: 405,
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ ok: false, error: "Method not allowed" }),
    };
  }

  try {
    const rawBody = event.isBase64Encoded
      ? Buffer.from(event.body, "base64").toString("utf8")
      : event.body || "";

    const body = parseBody(rawBody, event.headers?.["content-type"]);

    // Honeypot
    if (body.website || body.company_website) {
      return {
        statusCode: 200,
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ ok: true }),
      };
    }

    // Extract fields
    const name = String(body.name || `${body.firstName || ""} ${body.lastName || ""}`).trim();
    const email = String(body.email || "").trim();
    const phone = String(body.phone || "").trim();
    const location = String(body.location || body.preferredLocation || "").trim();
    const reason = String(body.reason || "").trim();
    const service = String(body.service || "").trim();
    const patientType = String(body.patientType || body.patient_type || "").trim();
    const insurance = String(body.insurance || body.insurancePlan || "").trim();
    const preferredDate = String(body.preferredDate || body.requestedDate || "").trim();
    const message = String(body.message || "").trim();
    const formType = String(body.form_type || body.formType || "contact").trim() || "contact";
    const consent = body.consentToContact === "1" || body.consent === "1"
      || body.consentToContact === true || body.consent === true;

    // Validate
    if (!name || !email) {
      return {
        statusCode: 400,
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ ok: false, error: "Please include your name and email." }),
      };
    }
    if (!isValidEmail(email)) {
      return {
        statusCode: 400,
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ ok: false, error: "Please provide a valid email address." }),
      };
    }

    const clientIp = event.requestContext?.http?.sourceIp || "";

    const payload = {
      submittedAt: new Date().toISOString(),
      formType,
      page: body.page || event.headers?.referer || "",
      name,
      email,
      phone,
      location,
      reason,
      service,
      patientType,
      insurance,
      preferredDate,
      message,
      consentToContact: consent,
      meta: {
        ip: clientIp,
        userAgent: event.headers?.["user-agent"] || "",
      },
    };

    // Send email via SES
    const secrets = await getSecrets();
    await sendEmail(secrets, payload);

    // Log submission (audit trail — NO PHI in log, only metadata)
    console.log(
      JSON.stringify({
        event: "form_submission",
        formType,
        location,
        service,
        timestamp: payload.submittedAt,
        ip: clientIp,
      })
    );

    return {
      statusCode: 200,
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ ok: true }),
    };
  } catch (err) {
    console.error("Form processing error:", err.message);
    return {
      statusCode: 500,
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ ok: false, error: "Something went wrong. Please call us." }),
    };
  }
};
