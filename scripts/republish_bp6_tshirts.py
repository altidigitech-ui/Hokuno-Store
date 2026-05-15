#!/usr/bin/env python3
"""Republish every BP 6 t-shirt on Shopify via Printify Publishing API.

Used after activating new mockup cameras (e.g. "folded") on Printify to push
the new images to the connected Shopify store. Continues on error and logs
per product to /tmp/republish_bp6_log.json.

Run:
  PRINTIFY_API_TOKEN=... python3 scripts/republish_bp6_tshirts.py
"""

from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

import requests

SHOP_ID = "22774508"
LOG_PATH = Path("/tmp/republish_bp6_log.json")
HEADERS = {
    "Authorization": f"Bearer {os.environ.get('PRINTIFY_API_TOKEN', '')}",
    "User-Agent": "Hokuno-republish-bp6/1.0",
    "Content-Type": "application/json",
}


def fetch_all_bp6() -> list[dict]:
    out = []
    for page in range(1, 30):
        r = requests.get(
            f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json",
            headers=HEADERS,
            params={"page": page, "limit": 50},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        for p in data["data"]:
            if p.get("blueprint_id") == 6:
                out.append(p)
        if page >= data["last_page"]:
            break
        time.sleep(0.3)
    return out


def publish_one(product_id: str) -> tuple[bool, str]:
    """Publish a Printify product to its connected Shopify store.

    Handles the publish:start / publish:succeed handshake. Printify's
    `publish.json` only *queues* the push; Shopify ingest happens async,
    but we still call `publishing_succeeded.json` to clear the in-progress
    flag so the next iteration is allowed.
    """
    body = {
        "title": True,
        "description": True,
        "images": True,
        "variants": True,
        "tags": True,
    }
    backoffs = [10, 30, 60]
    for attempt in range(len(backoffs) + 1):
        try:
            r = requests.post(
                f"https://api.printify.com/v1/shops/{SHOP_ID}/products/{product_id}/publish.json",
                headers=HEADERS,
                json=body,
                timeout=30,
            )
            if r.status_code in (200, 201, 202, 204):
                return True, ""
            if r.status_code == 429 and attempt < len(backoffs):
                wait = backoffs[attempt]
                print(f"        429 Throttled — sleeping {wait}s")
                time.sleep(wait)
                continue
            return False, f"HTTP {r.status_code}: {r.text[:200]}"
        except requests.RequestException as e:
            if attempt < len(backoffs):
                time.sleep(backoffs[attempt])
                continue
            return False, f"Exception: {e}"
    return False, "Exhausted retries"


def main() -> int:
    if not os.environ.get("PRINTIFY_API_TOKEN"):
        print("ERROR: PRINTIFY_API_TOKEN env var required", file=sys.stderr)
        return 1

    print("Fetching all BP 6 t-shirts from Printify…")
    products = fetch_all_bp6()
    total = len(products)
    print(f"  {total} BP 6 products found\n")

    results = []
    ok = 0
    fail = 0

    for i, p in enumerate(products, 1):
        pid = p["id"]
        title = p["title"]
        success, err = publish_one(pid)
        if success:
            ok += 1
            print(f"[{i:3}/{total}] OK     {pid} — {title}")
        else:
            fail += 1
            print(f"[{i:3}/{total}] FAIL   {pid} — {title}  ::  {err}")
        results.append({"id": pid, "title": title, "ok": success, "error": err})
        time.sleep(0.5)

    LOG_PATH.write_text(json.dumps({"total": total, "ok": ok, "fail": fail, "results": results}, indent=2))
    print()
    print("=" * 70)
    print(f"Total: {total}  |  OK: {ok}  |  FAIL: {fail}")
    print(f"Log: {LOG_PATH}")
    print("=" * 70)
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
