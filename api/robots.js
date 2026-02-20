module.exports = (req, res) => {
  const host = String(req.headers.host || "").toLowerCase();
  const isClassicVisionCare =
    host === "classicvisioncare.com" || host.endsWith(".classicvisioncare.com");

  let body;

  if (isClassicVisionCare) {
    body = [
      "# Classic Vision Care — Production robots.txt",
      "# Allow AI search/citation crawlers; block AI training crawlers",
      "",
      "User-agent: *",
      "Allow: /",
      "Disallow: /api/",
      "Disallow: /partials/",
      "",
      "# --- Traditional search engines ---",
      "User-agent: Googlebot",
      "Allow: /",
      "",
      "User-agent: bingbot",
      "Allow: /",
      "",
      "User-agent: Applebot",
      "Allow: /",
      "",
      "# --- OpenAI: allow search/citation, block training ---",
      "User-agent: OAI-SearchBot",
      "Allow: /",
      "Crawl-delay: 2",
      "",
      "User-agent: GPTBot",
      "Disallow: /",
      "",
      "# --- Anthropic ---",
      "User-agent: ClaudeBot",
      "Allow: /",
      "Crawl-delay: 4",
      "",
      "# --- Perplexity ---",
      "User-agent: PerplexityBot",
      "Allow: /",
      "Crawl-delay: 2",
      "",
      "# --- Google Gemini (grounding/search, not training) ---",
      "User-agent: Google-Extended",
      "Allow: /",
      "",
      "# --- Common Crawl ---",
      "User-agent: CCBot",
      "Disallow: /",
      "",
      "Sitemap: https://classicvisioncare.com/sitemap.xml",
      "Sitemap: https://classicvisioncare.com/sitemap-core.xml",
      "",
      "# LLM context file",
      "Llms-txt: https://classicvisioncare.com/llms.txt",
    ].join("\n");
  } else {
    // Prevent preview/staging domains (e.g., *.vercel.app) from being indexed.
    body = [
      "User-agent: *",
      "Disallow: /",
      "",
      "Sitemap: https://classicvisioncare.com/sitemap.xml",
    ].join("\n");
  }

  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=300");
  res.statusCode = 200;
  res.end(body + "\n");
};
