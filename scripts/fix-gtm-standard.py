#!/usr/bin/env python3
"""Replace deferred GTM loading with Google's standard immediate-load snippet."""
import re
import glob
import os

GTM_ID = "GTM-WG6M9ZDV"

# Standard GTM head snippet (goes right before </head>)
HEAD_SNIPPET = f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""

# Standard GTM noscript (goes right after <body...>)
BODY_SNIPPET = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

# Patterns to remove

# 1. Head: DataLayer init block (3 lines)
HEAD_OLD = re.compile(
    r'<!-- DataLayer init.*?-->\s*\n'
    r'<script>window\.dataLayer=window\.dataLayer\|\|\[\];</script>\s*\n'
    r'(<script src="/scripts/tracking\.js" defer></script>\s*\n)?',
    re.DOTALL
)

# 2. Body: Entire deferred GTM block
DEFERRED_GTM = re.compile(
    r'\s*<!-- Deferred GTM Loading.*?-->\s*\n'
    r'\s*<script>\s*\n'
    r'\s*\(function\(\)\{\s*\n'
    r'.*?'
    r'\}\)\(\);\s*\n'
    r'\s*</script>\s*\n'
    r'\s*<!-- GTM noscript fallback -->\s*\n'
    r'\s*<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html\?id=GTM-WG6M9ZDV".*?</iframe></noscript>',
    re.DOTALL
)

# Find all HTML files (exclude node_modules, .superdesign, dev)
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html_files = []
for pattern in ['**/*.html']:
    for f in glob.glob(os.path.join(base, pattern), recursive=True):
        if '/node_modules/' in f or '/.superdesign/' in f or '/dev/' in f:
            continue
        html_files.append(f)

print(f"Processing {len(html_files)} HTML files...")

stats = {'head_replaced': 0, 'head_inserted': 0, 'deferred_removed': 0, 'body_noscript_added': 0, 'skipped': 0}

for filepath in sorted(html_files):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content
    rel = os.path.relpath(filepath, base)

    # Skip files without GTM
    if 'GTM-WG6M9ZDV' not in content:
        stats['skipped'] += 1
        continue

    # Step 1: Remove old head DataLayer block if present
    if HEAD_OLD.search(content):
        content = HEAD_OLD.sub('', content)
        stats['head_replaced'] += 1

    # Step 2: Remove deferred GTM block from body
    if DEFERRED_GTM.search(content):
        content = DEFERRED_GTM.sub('', content)
        stats['deferred_removed'] += 1

    # Step 3: Insert standard head snippet before </head>
    if '<!-- Google Tag Manager -->' not in content:
        content = content.replace('</head>', HEAD_SNIPPET + '\n</head>')
        stats['head_inserted'] += 1

    # Step 4: Insert noscript right after <body...> tag
    if '<!-- Google Tag Manager (noscript) -->' not in content:
        # Match <body> or <body class="..."> etc
        body_match = re.search(r'(<body[^>]*>)', content)
        if body_match:
            body_tag = body_match.group(0)
            content = content.replace(body_tag, body_tag + '\n' + BODY_SNIPPET, 1)
            stats['body_noscript_added'] += 1

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Updated: {rel}")

print(f"\nDone!")
print(f"  Head old blocks removed: {stats['head_replaced']}")
print(f"  Head GTM snippet inserted: {stats['head_inserted']}")
print(f"  Deferred blocks removed: {stats['deferred_removed']}")
print(f"  Body noscript added: {stats['body_noscript_added']}")
print(f"  Skipped (no GTM): {stats['skipped']}")
