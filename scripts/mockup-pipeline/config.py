"""Pipeline config — theme-assets architecture (no Shopify Admin API)."""
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = REPO_ROOT / "output" / "mockup-pipeline"
RAW_DIR = OUTPUT_DIR / "01-raw"
DETOURED_DIR = OUTPUT_DIR / "02-detoured"
FINAL_DIR = OUTPUT_DIR / "03-final"
LOG_DIR = OUTPUT_DIR / "logs"

BG_DIR = REPO_ROOT / "assets" / "mockup-backgrounds"

SHOPIFY_THEME_DIR = REPO_ROOT / "shopify-theme"
SHOPIFY_ASSETS_DIR = SHOPIFY_THEME_DIR / "assets"
SHOPIFY_SNIPPETS_DIR = SHOPIFY_THEME_DIR / "snippets"

PRINTIFY_TOKEN = os.environ.get("PRINTIFY_API_TOKEN") or os.environ.get("PRINTIFY_TOKEN")
PRINTIFY_SHOP_ID = "22774508"
PRINTIFY_BASE_URL = "https://api.printify.com/v1"

SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE", "s6btxa-q0.myshopify.com")

BG_BY_COLLECTION = {
    "WANTED":         BG_DIR / "bg-wanted.png",
    "DIRECTION":      BG_DIR / "bg-direction.png",
    "MYTHOLOGIE":     BG_DIR / "bg-mythologie.png",
    "DESIGN HOKUNO":  BG_DIR / "bg-design.png",
}

FINAL_SIZE = (1500, 1500)
PRODUCT_RELATIVE_WIDTH = {
    "tshirt":    0.62,
    "mug":       0.52,
    "casquette": 0.58,
    "phonecase": 0.42,
    "default":   0.55,
}
WEBP_QUALITY = 88

PRINTIFY_DELAY_S = 0.4
SHOPIFY_DELAY_S = 0.6


def ensure_dirs():
    for d in (OUTPUT_DIR, RAW_DIR, DETOURED_DIR, FINAL_DIR, LOG_DIR):
        d.mkdir(parents=True, exist_ok=True)


def require_printify_token():
    if not PRINTIFY_TOKEN:
        raise RuntimeError(
            "PRINTIFY_API_TOKEN (or PRINTIFY_TOKEN) is not set. "
            "Export it before running the pipeline."
        )
