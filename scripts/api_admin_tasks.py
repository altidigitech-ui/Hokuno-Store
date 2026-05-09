#!/usr/bin/env python3
"""
Admin API helpers for Hokuno content cleanup.

Reads the Shopify CLI session token from ~/.config/shopify-cli-kit-nodejs/config.json
and uses it as a Bearer token against the Admin GraphQL API.

Subcommands:
  fix-titles   Replace "/17" with "/46" in every matching product title.
  tag-langs    Add lang-fr / lang-en tag to every product in Wanted + Direction
               collections, based on the " EN" marker in the title.
"""

import argparse
import json
import os
import sys
import time
from urllib import request, error

API_VERSION = "2024-10"
STORE = os.environ.get("SHOPIFY_STORE", "s6btxa-q0.myshopify.com").strip()
ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"


def load_cli_token() -> str:
    cfg_path = os.path.expanduser("~/.config/shopify-cli-kit-nodejs/config.json")
    with open(cfg_path) as f:
        cfg = json.load(f)
    session = json.loads(cfg["sessionStore"])
    for users in session.values():
        for ud in users.values():
            tok = ud.get("identity", {}).get("accessToken")
            if tok:
                return tok
    raise RuntimeError("No CLI session token. Run `shopify auth login` first.")


TOKEN = load_cli_token()


def gql(query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Hokuno-Admin-Tasks/1.0",
        },
        method="POST",
    )
    for attempt in range(4):
        try:
            with request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                if data.get("errors"):
                    # Throttling — retry with backoff
                    if any(e.get("extensions", {}).get("code") == "THROTTLED" for e in data["errors"]):
                        time.sleep(1.5 ** attempt)
                        continue
                    raise RuntimeError(f"GraphQL: {data['errors']}")
                return data["data"]
        except error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")
            if e.code in (429, 502, 503) and attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
        except error.URLError:
            if attempt < 3:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError("Exhausted retries")


# ---------------------------------------------------------------------------
# fix-titles : replace /17 with /46 in product titles
# ---------------------------------------------------------------------------

PRODUCTS_BY_QUERY = """
query products($cursor: String, $q: String!) {
  products(first: 100, after: $cursor, query: $q) {
    pageInfo { hasNextPage endCursor }
    edges { node { id title } }
  }
}
"""

PRODUCT_UPDATE_TITLE = """
mutation update($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id title }
    userErrors { field message }
  }
}
"""


def iter_products_matching(q: str):
    cursor = None
    while True:
        data = gql(PRODUCTS_BY_QUERY, {"cursor": cursor, "q": q})
        page = data["products"]
        for edge in page["edges"]:
            yield edge["node"]
        if not page["pageInfo"]["hasNextPage"]:
            return
        cursor = page["pageInfo"]["endCursor"]


def fix_titles():
    print("→ Querying products with '/17' in title…")
    matches = list(iter_products_matching("title:*17*"))
    # Filter precisely — Shopify search is permissive
    matches = [p for p in matches if "/17" in p["title"]]
    print(f"  {len(matches)} products to update.\n")
    if not matches:
        return
    fixed = 0
    skipped = 0
    failed = []
    for p in matches:
        old = p["title"]
        new = old.replace("/17", "/46")
        if old == new:
            skipped += 1
            continue
        data = gql(PRODUCT_UPDATE_TITLE, {"input": {"id": p["id"], "title": new}})
        errs = data["productUpdate"]["userErrors"]
        if errs:
            failed.append((old, errs))
            print(f"  ✗ {old}  →  ERRORS {errs}")
        else:
            fixed += 1
            print(f"  ✓ {old}  →  {new}")
        time.sleep(0.05)
    print(f"\nSummary: {fixed} fixed / {skipped} no-op / {len(failed)} failed")
    if failed:
        sys.exit(1)


# ---------------------------------------------------------------------------
# tag-langs : add lang-fr / lang-en to Wanted + Direction collection products
# ---------------------------------------------------------------------------

COLLECTION_PRODUCTS_QUERY = """
query collection($handle: String!, $cursor: String) {
  collectionByHandle(handle: $handle) {
    id
    title
    products(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      edges { node { id title tags } }
    }
  }
}
"""

PRODUCT_UPDATE_TAGS = """
mutation update($input: ProductInput!) {
  productUpdate(input: $input) {
    product { id title tags }
    userErrors { field message }
  }
}
"""


def iter_collection_products(handle: str):
    cursor = None
    while True:
        data = gql(COLLECTION_PRODUCTS_QUERY, {"handle": handle, "cursor": cursor})
        col = data["collectionByHandle"]
        if col is None:
            print(f"  ⚠ collection '{handle}' not found")
            return
        page = col["products"]
        for edge in page["edges"]:
            yield edge["node"]
        if not page["pageInfo"]["hasNextPage"]:
            return
        cursor = page["pageInfo"]["endCursor"]


def is_english_title(title: str) -> bool:
    """A title is English if it contains ' EN ' or ends with ' EN'."""
    t = title.strip()
    return " EN " in f" {t} " or t.endswith(" EN")


def tag_langs():
    handles = ["wanted", "direction"]
    seen_ids: set[str] = set()
    fr_added = 0
    en_added = 0
    skipped = 0
    failed = []

    for handle in handles:
        print(f"\n→ Collection '{handle}'…")
        products = list(iter_collection_products(handle))
        print(f"  {len(products)} products in collection")

        for p in products:
            if p["id"] in seen_ids:
                continue
            seen_ids.add(p["id"])

            current_tags = [t.strip() for t in p["tags"] if t.strip()]
            target_lang = "lang-en" if is_english_title(p["title"]) else "lang-fr"
            other_lang = "lang-fr" if target_lang == "lang-en" else "lang-en"

            new_tags = [t for t in current_tags if t != other_lang]
            if target_lang in new_tags:
                # Already tagged correctly, no change needed unless we just stripped the wrong tag
                if new_tags == current_tags:
                    skipped += 1
                    continue
            else:
                new_tags.append(target_lang)

            if sorted(new_tags) == sorted(current_tags):
                skipped += 1
                continue

            data = gql(PRODUCT_UPDATE_TAGS, {"input": {"id": p["id"], "tags": new_tags}})
            errs = data["productUpdate"]["userErrors"]
            if errs:
                failed.append((p["title"], errs))
                print(f"  ✗ {p['title']}  →  {errs}")
                continue

            if target_lang == "lang-fr":
                fr_added += 1
            else:
                en_added += 1
            print(f"  ✓ [{target_lang}] {p['title']}")
            time.sleep(0.05)

    print(f"\nSummary: lang-fr={fr_added}  lang-en={en_added}  unchanged={skipped}  failed={len(failed)}")
    if failed:
        sys.exit(1)


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fix-titles", "tag-langs", "all"])
    args = ap.parse_args()

    print(f"Store: {STORE}")
    print(f"API:   {ENDPOINT}\n")

    if args.cmd in ("fix-titles", "all"):
        fix_titles()
    if args.cmd in ("tag-langs", "all"):
        tag_langs()


if __name__ == "__main__":
    main()
