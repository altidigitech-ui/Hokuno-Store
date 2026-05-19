"""Fix 15 — Design Hokuno mockups: Sport front, colored shorts tint, maillot regen.

Three independent fixes:

  A) SPORT t-shirts (BP 145) — pipeline previously picked the back angle
     (97993), but the design lives on the FRONT. mockup_selector now forces
     the front angle for SPORT tees; we just need to regenerate the cached
     webps so they pick up the new selection.

  B) COLORED SHORTS (BP 978) — Printify only stores ONE white-bodied mockup
     for all 6 color names (Bleu / Rouge / Jaune / Vert / Rose / Bleu Ciel).
     The product variants are all "Black drawstring" — there is no actual
     color axis on Printify. We tint the white body in post-processing,
     keyed off the title color word, so the cards on the storefront actually
     show different colors instead of 6 identical white shorts.

     Tint method: rembg detoure the shorts, then multiplicatively blend
     each pixel toward the target color (white → target, black stays black),
     preserving fabric folds and shadows.

  C) MAILLOT DE BAIN (BP 978) — same base as shorts, classification was
     wrong (lived under "Accessoires" instead of "Short"). 08_character_map.py
     now categorises MAILLOT as 'short' — we also regenerate its webp via
     rembg+compose so the card matches the other short cards.

Run:
    python scripts/mockup-pipeline/15_fix_design_hokuno_visuals.py
    python scripts/mockup-pipeline/15_fix_design_hokuno_visuals.py --dry-run
"""
from __future__ import annotations

import io
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config           # noqa: E402
import printify_client  # noqa: E402
import mockup_selector  # noqa: E402
import detourage        # noqa: E402
import compositing      # noqa: E402


# ── Targets ────────────────────────────────────────────────────────────────

SPORT_TARGETS: list[tuple[str, str]] = [
    # (product_id, handle)
    ("69f91fc0300b32baed0d1c48", "t-shirt-sport-design-hokuno-dark"),
    ("69f8959bfeed9979d10d1130", "t-shirt-sport-design-hokuno-light"),
]

# (product_id, handle, tint_rgb)
# Tints chosen to read clearly on the bg-design pale background.
SHORT_TARGETS: list[tuple[str, str, tuple[int, int, int]]] = [
    ("69f9dc0f7d958848720c19f8", "short-de-bain-design-hokuno-bleu",      (38,  86,  178)),
    ("69f9d22145e1cbc4b50678a1", "short-de-bain-design-hokuno-rose",      (231, 110, 168)),
    ("69f9d20e7d958848720c12c1", "short-de-bain-design-hokuno-jaune",     (235, 192,  50)),
    ("69f9d20944aadacf110bac97", "short-de-bain-design-hokuno-vert",      (52,  140,  76)),
    ("69f9d20344aadacf110bac94", "short-de-bain-design-hokuno-rouge",     (197,  46,  46)),
    ("69f89408feed9979d10d1032", "short-de-bain-design-hokuno-bleu-ciel", (110, 178, 226)),
]

MAILLOT_TARGET: tuple[str, str] = (
    "69f90268ad402ce2b4035348", "maillot-de-bain-design-hokuno-dark",
)


# ── Tint pipeline ──────────────────────────────────────────────────────────

def tint_detoured(det: Image.Image, tint_rgb: tuple[int, int, int]) -> Image.Image:
    """Multiplicatively recolor a detoured RGBA image toward `tint_rgb`.

    Pure-white pixels become exactly `tint_rgb`; darker pixels (folds,
    shadows, drawstring) keep their relative darkness so the fabric still
    looks 3D. Alpha is preserved.
    """
    arr = np.array(det)  # H, W, 4
    rgb = arr[..., :3].astype(np.float32) / 255.0  # 0..1
    factor = np.array(tint_rgb, dtype=np.float32) / 255.0  # 0..1
    tinted = (rgb * factor) * 255.0
    arr[..., :3] = np.clip(tinted, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, mode="RGBA")


def composite_tinted(
    tinted: Image.Image,
    bg_path: Path,
    output_path: Path,
    rel_w: float = 0.62,
) -> Path:
    bg = Image.open(bg_path).convert("RGB").resize(config.FINAL_SIZE, Image.LANCZOS)
    target_w = int(config.FINAL_SIZE[0] * rel_w)
    ratio = target_w / tinted.width
    target_h = int(tinted.height * ratio)
    resized = tinted.resize((target_w, target_h), Image.LANCZOS)
    x = (config.FINAL_SIZE[0] - target_w) // 2
    y = (config.FINAL_SIZE[1] - target_h) // 2
    canvas = bg.convert("RGBA")
    canvas.alpha_composite(resized, dest=(x, y))
    final = canvas.convert("RGB")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(output_path, "WEBP", quality=config.WEBP_QUALITY, method=6)
    return output_path


# ── Per-target processors ──────────────────────────────────────────────────

def process_sport(pid: str, handle: str) -> dict:
    log = {"pid": pid, "handle": handle, "kind": "sport", "status": "?"}
    try:
        product = printify_client._get(f"/shops/{config.PRINTIFY_SHOP_ID}/products/{pid}.json")
    except Exception as e:
        log["status"] = f"fetch-error: {e}"
        return log

    img_meta = mockup_selector.pick_source_mockup_tshirt(product)
    src = img_meta.get("src", "")
    cam = mockup_selector._url_camera_label(src) or img_meta.get("position")
    log["camera"] = cam
    log["src"] = src
    if "front" not in (cam or ""):
        log["status"] = f"WRONG-CAM ({cam!r}) — selector should have picked front"
        return log

    raw = printify_client.download_image(src)
    raw_path = config.RAW_DIR / f"{pid}.png"
    raw_path.write_bytes(raw)

    # Sport-Dark mockup body is genuinely black → rembg works.
    # Sport-Light mockup body is near-white → compose_light is safer.
    is_dark = mockup_selector.is_dark_product(product)
    dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
    bg_path = config.BG_BY_COLLECTION["DESIGN HOKUNO"]
    if dst.exists():
        dst.unlink()
    if is_dark:
        det = detourage.detoure(raw)
        det.save(config.DETOURED_DIR / f"{pid}.png", "PNG")
        compositing.compose(det, bg_path, "tshirt", dst)
        log["strategy"] = "rembg + compose"
    else:
        compositing.compose_light(raw, bg_path, dst)
        log["strategy"] = "compose_light"

    log["asset"] = str(dst.relative_to(config.REPO_ROOT))
    log["status"] = "OK"
    return log


def process_short_tinted(pid: str, handle: str, tint_rgb: tuple[int, int, int]) -> dict:
    log = {"pid": pid, "handle": handle, "kind": "short-tint",
           "tint": tint_rgb, "status": "?"}
    try:
        product = printify_client._get(f"/shops/{config.PRINTIFY_SHOP_ID}/products/{pid}.json")
    except Exception as e:
        log["status"] = f"fetch-error: {e}"
        return log

    imgs = product.get("images") or []
    pub = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub or imgs
    if not pool:
        log["status"] = "no images"
        return log
    img_meta = next(
        (i for i in pool if (i.get("position") or "").lower() == "front"
         or "camera_label=front" in (i.get("src") or "")),
        pool[0],
    )
    src = img_meta.get("src", "")
    log["src"] = src

    raw = printify_client.download_image(src)
    raw_path = config.RAW_DIR / f"{pid}.png"
    raw_path.write_bytes(raw)

    det = detourage.detoure(raw)
    det.save(config.DETOURED_DIR / f"{pid}.png", "PNG")
    tinted = tint_detoured(det, tint_rgb)

    dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
    if dst.exists():
        dst.unlink()
    bg_path = config.BG_BY_COLLECTION["DESIGN HOKUNO"]
    composite_tinted(tinted, bg_path, dst, rel_w=0.55)

    log["asset"] = str(dst.relative_to(config.REPO_ROOT))
    log["status"] = "OK"
    return log


def process_maillot(pid: str, handle: str) -> dict:
    """Maillot has no color in the name → just rembg + compose (no tint)."""
    log = {"pid": pid, "handle": handle, "kind": "maillot", "status": "?"}
    try:
        product = printify_client._get(f"/shops/{config.PRINTIFY_SHOP_ID}/products/{pid}.json")
    except Exception as e:
        log["status"] = f"fetch-error: {e}"
        return log

    imgs = product.get("images") or []
    pub = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub or imgs
    if not pool:
        log["status"] = "no images"
        return log
    img_meta = next(
        (i for i in pool if (i.get("position") or "").lower() == "front"
         or "camera_label=front" in (i.get("src") or "")),
        pool[0],
    )
    raw = printify_client.download_image(img_meta["src"])
    (config.RAW_DIR / f"{pid}.png").write_bytes(raw)

    det = detourage.detoure(raw)
    det.save(config.DETOURED_DIR / f"{pid}.png", "PNG")

    dst = config.SHOPIFY_ASSETS_DIR / f"mockup-{handle}.webp"
    if dst.exists():
        dst.unlink()
    bg_path = config.BG_BY_COLLECTION["DESIGN HOKUNO"]
    compositing.compose(det, bg_path, "default", dst)

    log["asset"] = str(dst.relative_to(config.REPO_ROOT))
    log["status"] = "OK"
    return log


# ── Main ───────────────────────────────────────────────────────────────────

def run() -> int:
    dry = "--dry-run" in sys.argv
    config.ensure_dirs()
    config.require_printify_token()

    print("=" * 78)
    print("FIX 15 — Design Hokuno: Sport front, shorts tint, maillot regen")
    print("=" * 78)

    if dry:
        print("\n(dry-run) Would process:")
        for pid, h in SPORT_TARGETS:
            print(f"  SPORT    {pid}  {h}")
        for pid, h, t in SHORT_TARGETS:
            print(f"  SHORT    {pid}  {h}  tint={t}")
        print(f"  MAILLOT  {MAILLOT_TARGET[0]}  {MAILLOT_TARGET[1]}")
        return 0

    all_logs = []

    print("\n--- SPORT ---")
    for pid, h in SPORT_TARGETS:
        log = process_sport(pid, h)
        print(f"  {log['handle']:<48} cam={log.get('camera','-'):<10} → {log['status']}")
        all_logs.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    print("\n--- SHORTS (tinted) ---")
    for pid, h, t in SHORT_TARGETS:
        log = process_short_tinted(pid, h, t)
        print(f"  {log['handle']:<48} tint={t} → {log['status']}")
        all_logs.append(log)
        time.sleep(config.PRINTIFY_DELAY_S)

    print("\n--- MAILLOT ---")
    pid, h = MAILLOT_TARGET
    log = process_maillot(pid, h)
    print(f"  {log['handle']:<48} → {log['status']}")
    all_logs.append(log)

    n_ok = sum(1 for l in all_logs if l["status"] == "OK")
    n_err = len(all_logs) - n_ok
    print(f"\nDone: {n_ok} OK, {n_err} errors.")
    return 0 if n_err == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
