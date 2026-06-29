// Cloudflare Pages Function  ->  POST /api/enquiry
// Files a website enquiry into the Sooprema CRM via the /property-enquiry endpoint.
//
// SECURITY: the API secret never touches the browser or the static site. It lives in
// Cloudflare Pages "Environment variables / Secrets" and is read here at runtime:
//   SOOPREMA_AGENCY, SOOPREMA_PUBLIC_KEY, SOOPREMA_SECRET_KEY, SOOPREMA_URL  (SOOPREMA_LANG optional)
// This code runs server-side on Cloudflare's edge.

export async function onRequestPost({ request, env }) {
  const json = (obj, status = 200) =>
    new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json" } });

  if (!env.SOOPREMA_SECRET_KEY || !env.SOOPREMA_PUBLIC_KEY || !env.SOOPREMA_AGENCY || !env.SOOPREMA_URL) {
    return json({ ok: false, error: "Enquiry service is not configured yet." }, 503);
  }

  let body;
  try { body = await request.json(); } catch (e) { return json({ ok: false, error: "Bad request." }, 400); }

  const id = String(body.id || "").trim();
  const name = String(body.name || "").trim();
  const email = String(body.email || "").trim();
  const phone = String(body.phone || "").trim();
  const message = String(body.message || "").slice(0, 2000);
  const consent = body.consent ? 1 : 0;

  if (!id || !name || !email || !phone) return json({ ok: false, error: "Please fill in your name, email and phone." }, 400);
  if (!consent) return json({ ok: false, error: "Consent is required to send an enquiry." }, 400);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({ ok: false, error: "Please enter a valid email address." }, 400);

  // Auth: HMAC-SHA256 of the current unix timestamp, keyed by the secret (hex).
  const ts = Math.floor(Date.now() / 1000).toString();
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", enc.encode(env.SOOPREMA_SECRET_KEY),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(ts));
  const hash = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");

  const form = new URLSearchParams({
    agency: env.SOOPREMA_AGENCY,
    language: env.SOOPREMA_LANG || "en",
    id, name, email, phone, message,
    communications: String(consent),
  });

  const url = env.SOOPREMA_URL.replace(/\/+$/, "") + "/property-enquiry";
  let resp;
  try {
    resp = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": "Basic " + env.SOOPREMA_PUBLIC_KEY + ":" + hash,
        "X-Timestamp": ts,
        "content-type": "application/x-www-form-urlencoded",
      },
      body: form.toString(),
    });
  } catch (e) {
    return json({ ok: false, error: "Could not reach the CRM. Please try WhatsApp." }, 502);
  }

  let data = {};
  try { data = await resp.json(); } catch (e) {}
  const status = data && data.response && data.response.status;
  if (status === "ok") return json({ ok: true });
  return json({ ok: false, error: (data && data.response && data.response.reason) || "The enquiry could not be filed." }, 502);
}
