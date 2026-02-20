#!/usr/bin/env python3
"""Submit URLs to IndexNow for instant indexing on Bing and participating engines.

Usage:
    python scripts/indexnow-submit.py https://classicvisioncare.com/ai-profile/
    python scripts/indexnow-submit.py https://classicvisioncare.com/page1/ https://classicvisioncare.com/page2/
"""

import sys
import json
import urllib.request

INDEXNOW_KEY = "6ff6962686d14de48b844bea300b6570"
HOST = "classicvisioncare.com"
ENDPOINT = "https://api.indexnow.org/indexnow"


def submit_urls(urls):
    if len(urls) == 1:
        # Single URL submission via GET
        url = f"{ENDPOINT}?url={urls[0]}&key={INDEXNOW_KEY}"
        req = urllib.request.Request(url)
        try:
            resp = urllib.request.urlopen(req)
            print(f"OK ({resp.status}): {urls[0]}")
        except urllib.error.HTTPError as e:
            print(f"ERROR ({e.code}): {urls[0]} — {e.reason}")
    else:
        # Batch submission via POST
        payload = {
            "host": HOST,
            "key": INDEXNOW_KEY,
            "keyLocation": f"https://{HOST}/{INDEXNOW_KEY}.txt",
            "urlList": urls
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        try:
            resp = urllib.request.urlopen(req)
            print(f"OK ({resp.status}): submitted {len(urls)} URLs")
        except urllib.error.HTTPError as e:
            print(f"ERROR ({e.code}): {e.reason}")

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/indexnow-submit.py <url> [<url2> ...]")
        sys.exit(1)
    urls = sys.argv[1:]
    sys.exit(submit_urls(urls))
