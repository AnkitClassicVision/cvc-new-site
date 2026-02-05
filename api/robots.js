module.exports = (req, res) => {
  const host = String(req.headers.host || "").toLowerCase();
  const isClassicVisionCare =
    host === "classicvisioncare.com" || host.endsWith(".classicvisioncare.com");

  const lines = ["User-agent: *"];
  if (isClassicVisionCare) {
    lines.push("Allow: /");
    lines.push("Sitemap: https://classicvisioncare.com/sitemap.xml");
  } else {
    // Prevent preview/staging domains (e.g., *.vercel.app) from being indexed.
    lines.push("Disallow: /");
    lines.push("Sitemap: https://classicvisioncare.com/sitemap.xml");
  }

  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=300");
  res.statusCode = 200;
  res.end(lines.join("\n") + "\n");
};

