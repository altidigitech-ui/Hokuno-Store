#!/usr/bin/env python3
"""Republish a fixed list of Printify products listed in
output/audit-gallery-A-ids.txt (format: `ID | TITRE` per line).

Used after activating new mockup cameras (e.g. "folded") on Printify for those
44 products — pushes the new images to the connected Shopify store via the
Printify Publishing API. Continues on error and logs per product.

Run:
  PRINTIFY_API_TOKEN=... python3 scripts/republish_from_audit_list.py
"""

from __future__ import annotations
import json
import os
import sys
import time
from pathlib import Path

import requests

SHOP_ID = "22774508"
REPO_ROOT = Path(__file__).resolve().parents[1]
ID_LIST = REPO_ROOT / "output" / "audit-gallery-A-ids.txt"
LOG_PATH = Path("/tmp/republish_audit_list_log.json")
HEADERS = {
    "Authorization": f"Bearer {os.environ.get('PRINTIFY_API_TOKEN', '')}",
    "User-Agent": "Hokuno-republish-audit/1.0",
    "Content-Type": "application/json",
}


def load_ids(path: Path) -> list[tuple[str, str]]:
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            pid, title = (s.strip() for s in line.split("|", 1))
        else:
            pid, title = line, ""
        if pid:
            out.append((pid, title))
    return out


def publish_one(product_id: str) -> tuple[bool, str]:
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
    if not ID_LIST.exists():
        print(f"ERROR: {ID_LIST} missing", file=sys.stderr)
        return 1

    ids = load_ids(ID_LIST)
    total = len(ids)
    print(f"Loaded {total} product IDs from {ID_LIST.name}\n")

    results = []
    ok = 0
    fail = 0
    for i, (pid, title) in enumerate(ids, 1):
        success, err = publish_one(pid)
        if success:
            ok += 1
            print(f"[{i:3}/{total}] OK     {pid} — {title}")
        else:
            fail += 1
            print(f"[{i:3}/{total}] FAIL   {pid} — {title}  ::  {err}")
        results.append({"id": pid, "title": title, "ok": success, "error": err})
        time.sleep(0.5)

    LOG_PATH.write_text(
        json.dumps({"total": total, "ok": ok, "fail": fail, "results": results}, indent=2)
    )
    print()
    print("=" * 70)
    print(f"Total: {total}  |  OK: {ok}  |  FAIL: {fail}")
    print(f"Log: {LOG_PATH}")
    print("=" * 70)
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
