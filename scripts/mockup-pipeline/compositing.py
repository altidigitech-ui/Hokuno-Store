"""Compose a detoured product onto its collection background.

Two strategies:
- compose(): rembg-style — detoured PNG over bg, resized to relative width.
  Works well for dark/colored garments where rembg can isolate the subject.
- compose_light(): bg-replacement — keeps the original mockup pixels intact and
  only replaces near-white pixels CONNECTED TO IMAGE BORDERS with the collection
  bg. Critical for light/white garments where rembg eats the cotton along with the bg.
"""
import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

import config


def compose(
    detoured: Image.Image,
    bg_path: Path,
    product_type: str,
    output_path: Path,
) -> Path:
    bg = Image.open(bg_path).convert("RGB").resize(config.FINAL_SIZE, Image.LANCZOS)

    rel_w = config.PRODUCT_RELATIVE_WIDTH.get(
        product_type, config.PRODUCT_RELATIVE_WIDTH["default"]
    )
    target_w = int(config.FINAL_SIZE[0] * rel_w)
    ratio = target_w / detoured.width
    target_h = int(detoured.height * ratio)
    resized = detoured.resize((target_w, target_h), Image.LANCZOS)

    x = (config.FINAL_SIZE[0] - target_w) // 2
    y = (config.FINAL_SIZE[1] - target_h) // 2

    bg_rgba = bg.convert("RGBA")
    bg_rgba.alpha_composite(resized, dest=(x, y))
    final = bg_rgba.convert("RGB")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(output_path, "WEBP", quality=config.WEBP_QUALITY, method=6)
    return output_path


def compose_light(
    mockup_bytes: bytes,
    bg_path: Path,
    output_path: Path,
    threshold: int = 248,
    blur_radius: int = 3,
    replace_all_near_white: bool = False,
) -> Path:
    """Replace the near-white background (connected to image borders) with bg.

    For t-shirts the body is near-white itself, so we only replace pixels
    connected to the image borders (default mode).

    replace_all_near_white (True for mugs):
        Replace EVERY near-white pixel — not just the ones connected to the
        borders. Mugs have a non-near-white body (gradient shading on the
        ceramic) so the body is preserved automatically by the threshold,
        and this catches the handle's inner hole which is enclosed and
        otherwise stays white. Do NOT enable on tees — their white cotton
        body would get replaced too.
    """
    mockup = Image.open(io.BytesIO(mockup_bytes)).convert("RGB")
    mockup = mockup.resize(config.FINAL_SIZE, Image.LANCZOS)
    bg = Image.open(bg_path).convert("RGB").resize(config.FINAL_SIZE, Image.LANCZOS)

    arr = np.array(mockup)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    near_white = (r >= threshold) & (g >= threshold) & (b >= threshold)

    if replace_all_near_white:
        bg_mask = near_white
    else:
        labels, _ = ndimage.label(near_white)
        border_ids: set[int] = set()
        border_ids.update(labels[0, :].tolist())
        border_ids.update(labels[-1, :].tolist())
        border_ids.update(labels[:, 0].tolist())
        border_ids.update(labels[:, -1].tolist())
        border_ids.discard(0)
        bg_mask = np.isin(labels, list(border_ids))

    mask_img = Image.fromarray((bg_mask * 255).astype(np.uint8))
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    mask = (np.array(mask_img).astype(np.float32) / 255.0)[..., None]

    mockup_arr = arr.astype(np.float32)
    bg_arr = np.array(bg).astype(np.float32)
    result = mockup_arr * (1 - mask) + bg_arr * mask
    final = Image.fromarray(result.clip(0, 255).astype(np.uint8))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    final.save(output_path, "WEBP", quality=config.WEBP_QUALITY, method=6)
    return output_path
