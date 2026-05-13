"""Patch product-card.liquid + templates/product.liquid with the mockup handle list, then push.

Architecture inline (no separate snippet) car Shopify Liquid interdit `{% include %}`
dans un snippet rendu via `{% render %}`. La liste des handles est dupliquée
dans les 2 fichiers entre les marqueurs HOKUNO-MOCKUP-LIST:START / :END,
gérés par ce script.

Idempotent : si les marqueurs existent déjà, la liste est remplacée. Sinon, le bloc
mockup complet est inséré au bon endroit.

Run from the repo root:
    python scripts/mockup-pipeline/03_patch_theme.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config  # noqa: E402


SHOPIFY_THEME_ID = "198885507415"  # Hokuno Preview (live)

PRODUCT_CARD = config.SHOPIFY_SNIPPETS_DIR / "product-card.liquid"
PRODUCT_TEMPLATE = config.SHOPIFY_THEME_DIR / "templates" / "product.liquid"

LIST_START = "{%- comment -%}HOKUNO-MOCKUP-LIST:START (auto-géré){%- endcomment -%}"
LIST_END = "{%- comment -%}HOKUNO-MOCKUP-LIST:END{%- endcomment -%}"
LIST_RE = re.compile(
    re.escape(LIST_START) + r"[\s\S]*?" + re.escape(LIST_END),
    re.MULTILINE,
)


def _list_block(handles: list[str], indent: str) -> str:
    lines = [f"{indent}{LIST_START}", f'{indent}{{%- assign mockup_handles = "" -%}}']
    for h in handles:
        lines.append(
            f'{indent}{{%- assign mockup_handles = mockup_handles | append: "{h}," -%}}'
        )
    lines.append(f"{indent}{LIST_END}")
    return "\n".join(lines)


def existing_handles(path: Path) -> list[str]:
    if not path.exists():
        return []
    src = path.read_text()
    m = LIST_RE.search(src)
    if not m:
        return []
    return re.findall(r'append:\s*"([^",]+),"', m.group(0))


def patch_file_list(path: Path, indent: str, all_handles: list[str]) -> str:
    src = path.read_text()
    m = LIST_RE.search(src)
    if not m:
        raise RuntimeError(
            f"{path.name}: marqueurs HOKUNO-MOCKUP-LIST introuvables. "
            "Le patch initial doit avoir été appliqué manuellement avant."
        )
    new_block = _list_block(all_handles, indent)
    new_src = LIST_RE.sub(new_block, src, count=1)
    if new_src == src:
        return "no-change"
    path.write_text(new_src)
    return "updated"


def update_list(new_handles: list[str]) -> tuple[list[str], list[str]]:
    current = existing_handles(PRODUCT_CARD)
    seen = set(current)
    added = [h for h in new_handles if h and h not in seen]
    merged = current + added

    patch_file_list(PRODUCT_CARD, indent="    ", all_handles=merged)
    patch_file_list(PRODUCT_TEMPLATE, indent="      ", all_handles=merged)
    return merged, added


def push_theme() -> int:
    cmd = [
        "shopify", "theme", "push",
        "--store", config.SHOPIFY_STORE,
        "--theme", SHOPIFY_THEME_ID,
        "--allow-live",
        "--nodelete",
    ]
    print(f"\n→ Running: {' '.join(cmd)}  (cwd={config.SHOPIFY_THEME_DIR})")
    result = subprocess.run(cmd, cwd=config.SHOPIFY_THEME_DIR, check=False)
    return result.returncode


def run() -> int:
    config.ensure_dirs()

    upload_log = config.LOG_DIR / "upload_poc_results.json"
    if not upload_log.exists():
        print(f"❌ Missing {upload_log}. Run 02_upload_poc.py first.")
        return 1

    log = json.loads(upload_log.read_text())
    copied = log.get("copied", [])
    if not copied:
        print("❌ No assets in phase 02 — aborting patch.")
        return 1

    new_handles = [c["handle"] for c in copied if c.get("handle")]
    merged, added = update_list(new_handles)

    print(f"  product-card.liquid : {len(merged)} handles ({len(added)} added)")
    print(f"  templates/product.liquid : {len(merged)} handles ({len(added)} added)")

    rc = push_theme()

    print("\n" + "=" * 70)
    if rc == 0:
        print("🛑 PHASE 3 TERMINÉE — POC poussé sur Shopify")
    else:
        print(f"⚠  shopify theme push exit={rc}")
    print("=" * 70)
    print(f"Store : https://{config.SHOPIFY_STORE}")
    print("\nPour chaque cobaye, ouvre la page produit ET la collection associée :")
    for c in copied:
        prod_url = f"https://{config.SHOPIFY_STORE}/products/{c['handle']}"
        col = c.get("collection", "").lower().split()[0]
        col_url = f"https://{config.SHOPIFY_STORE}/collections/{col}"
        print(f"  [{c['collection']:<14}] {prod_url}")
        print(f"  {'':16} (collection : {col_url})")
    print("\n⚠  Si tu vois encore les anciennes images : Ctrl+Shift+R pour vider le cache navigateur.")
    print("Pour rollback : restore product-card.liquid.bak + product.liquid.bak + re-push.")
    print("=" * 70)
    return rc


if __name__ == "__main__":
    sys.exit(run())
