"""Pick product type + source mockup image from a Printify product payload."""

_TYPE_NEEDLES = [
    ("tshirt",    ("T-SHIRT", "TSHIRT", " TEE", "T SHIRT")),
    ("mug",       ("MUG", "TASSE")),
    ("casquette", ("CASQUETTE", " BOB", " HAT")),
    ("phonecase", ("COQUE", " CASE")),
]


def detect_product_type(product: dict) -> str:
    title = (product.get("title") or "").upper()
    padded = f" {title} "
    for ptype, needles in _TYPE_NEEDLES:
        if any(n in padded for n in needles):
            return ptype
    return "default"


_LIGHT_NEEDLES = ("NOIR", "DARK", "BLACK")


def is_dark_product(product: dict) -> bool:
    """True if the product title indicates a dark/black variant."""
    title = (product.get("title") or "").upper()
    return any(n in title for n in _LIGHT_NEEDLES)


def is_light_product(product: dict) -> bool:
    return not is_dark_product(product)


# ─── Light-color preference for non-white variant detouring ────────────────
# When a light product has a non-pure-white color enabled, the rembg
# detouring works because the garment now contrasts with Printify's white BG.
# Order matters: most "neutral / off-white" picks first, then any non-white.
_LIGHT_COLOR_PREFERENCE = (
    "Natural",
    "Cream",
    "Bone",
    "Sport Grey",
    "Ash",
    "Sand",
    "Heather",
    "Oatmeal",
    "Ice Grey",
    "Gravel",  # gray, common on BP 6 Wanted/Direction/Mythologie
)

def pick_light_color(product: dict) -> tuple[str | None, list[int]]:
    """Pick a neutral non-white color from the enabled variants of a light product.

    Uses Printify's product.options to robustly find the color axis (some
    blueprints put color in option[0], others in option[1]; some have no color
    axis at all like mugs BP 478).

    Returns (color_name, [variant_ids]) when a *preferred* neutral color
    (Natural / Cream / Sport Grey / etc.) is enabled. If none is enabled —
    including products with no color axis at all — returns (None, []) and the
    caller must fall back to compose_light.

    We deliberately do NOT accept "any non-white color" as a fallback: that
    would silently swap a White product for an arbitrary Royal/Red mockup.
    """
    options = product.get("options") or []
    color_opt_idx = None
    color_opt = None
    for idx, opt in enumerate(options):
        if (opt.get("type") or "").lower() == "color":
            color_opt_idx = idx
            color_opt = opt
            break
    if color_opt is None:
        return None, []

    val_id_to_name = {v["id"]: (v.get("title") or "") for v in color_opt.get("values") or []}

    by_color: dict[str, list[int]] = {}
    for v in product.get("variants", []):
        if not v.get("is_enabled"):
            continue
        opt_vals = v.get("options") or []
        if color_opt_idx >= len(opt_vals):
            continue
        color_name = val_id_to_name.get(opt_vals[color_opt_idx], "")
        if color_name:
            by_color.setdefault(color_name, []).append(v["id"])

    # Match preferred neutral colors in priority order
    for pref in _LIGHT_COLOR_PREFERENCE:
        for c, ids in by_color.items():
            if c.lower() == pref.lower():
                return c, ids

    return None, []


# T-shirt back-of-shirt template angle IDs (Gildan 5000 / BP 6 family).
# - 102006 = camera_label=back-2 → wrinkled/folded lifestyle back lay (preferred)
# - 92571  = camera_label=back   → clean flat back (fallback)
TSHIRT_BACK_ANGLE_IDS = ("102006", "92571")

# T-shirt position needles, priority order (Printify exposes 'back-2' on some
# blueprints via the position field; on BP 6 it only lives in URL camera_label).
TSHIRT_POSITION_PRIORITY = ("back-2", "back_2", "back2", "back-1", "back")

# Sport tees (BP 145) carry the design on the FRONT (no back print) — invert
# the default back-preference and pick a front view instead.
TSHIRT_FRONT_POSITION_PRIORITY = ("front-2", "front_2", "front2", "front")


def _is_front_print_tshirt(product: dict) -> bool:
    """True if the t-shirt has its design on the front (e.g. Sport BP 145)."""
    title = (product.get("title") or "").upper()
    return "SPORT" in title


def _url_camera_label(src: str) -> str:
    """Extract the camera_label query param from a Printify mockup URL."""
    if not src or "camera_label=" not in src:
        return ""
    return src.split("camera_label=")[-1].split("&")[0].lower()


def _url_contains_angle(src: str, angle_id: str) -> bool:
    return f"/{angle_id}/" in (src or "")


def _angle_position(img: dict) -> str:
    """Normalized angle label, preferring position field, falling back to URL camera_label.

    BP 6 mockups have position='other' for the back-2 angle — the real label is
    only in the URL's camera_label query string. This helper unifies both.
    """
    pos = (img.get("position") or "").lower()
    if pos and pos != "other":
        return pos
    return _url_camera_label(img.get("src", ""))


_POSITION_NEEDLES_BY_TYPE = {
    "mug":       ["front", "default"],
    "casquette": ["front"],
    "phonecase": ["front", "default"],
    "default":   ["front", "default"],
}


def pick_source_mockup(product: dict, ptype: str, color_variant_ids: list[int] | None = None) -> dict:
    """Pick the source mockup image.

    color_variant_ids: when provided, restrict the candidate pool to images whose
    variant_ids intersect the given list. Used to pick the cream/natural variant
    mockup on light products instead of the white one.
    """
    if ptype == "mug":
        return pick_source_mockup_mug(product, color_variant_ids=color_variant_ids)
    if ptype == "tshirt":
        return pick_source_mockup_tshirt(product, color_variant_ids=color_variant_ids)

    imgs = product.get("images", [])
    if not imgs:
        raise ValueError("No mockup images on product")

    pub_imgs = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub_imgs or imgs

    if color_variant_ids:
        wanted = set(color_variant_ids)
        filtered = [i for i in pool if wanted.intersection(i.get("variant_ids") or [])]
        if filtered:
            pool = filtered

    needles = _POSITION_NEEDLES_BY_TYPE.get(ptype, _POSITION_NEEDLES_BY_TYPE["default"])
    for needle in needles:
        for i in pool:
            pos = (i.get("position") or "").lower()
            if needle in pos:
                return i

    for i in pool:
        if i.get("is_default"):
            return i
    return pool[0]


def pick_source_mockup_tshirt(product: dict, color_variant_ids: list[int] | None = None) -> dict:
    """Pick a t-shirt mockup. Default = back-2 (wrinkled back lay) for tees
    with a back print; Sport tees flip to front because the design lives there.

    Priority (back-print tees):
      1. Position / camera_label matches in order: back-2, back_2, back2, back-1, back
      2. Known back angle IDs in URL (102006 before 92571) — for products labeled 'other'
      3. is_default → first image

    Priority (front-print tees, e.g. Sport BP 145):
      1. Position / camera_label matches in order: front-2, front_2, front2, front
      2. is_default → first image
    """
    imgs = product.get("images", [])
    if not imgs:
        raise ValueError("No mockup images on product")

    pub_imgs = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub_imgs or imgs

    if color_variant_ids:
        wanted = set(color_variant_ids)
        filtered = [i for i in pool if wanted.intersection(i.get("variant_ids") or [])]
        if filtered:
            pool = filtered

    if _is_front_print_tshirt(product):
        for needle in TSHIRT_FRONT_POSITION_PRIORITY:
            for i in pool:
                if _angle_position(i) == needle:
                    return i
        for i in pool:
            if i.get("is_default"):
                return i
        return pool[0]

    for needle in TSHIRT_POSITION_PRIORITY:
        for i in pool:
            if _angle_position(i) == needle:
                return i

    for angle in TSHIRT_BACK_ANGLE_IDS:
        for i in pool:
            if _url_contains_angle(i.get("src", ""), angle):
                return i

    for i in pool:
        if i.get("is_default"):
            return i
    return pool[0]


# Mug mockup template IDs that show the design clearly (empirically identified).
# Keys are Printify blueprint_id. Values are angle/template fragments that appear
# in the image src URL pattern: /mockup/{pid}/{variant_id}/{angle_id}/...
MUG_DESIGN_ANGLE_IDS = {
    478: ("6311", "101797"),   # Ceramic Mug 11oz, 15oz (light)
    479: ("6407", "101583"),   # Ceramic Mug Black 11oz, 15oz (dark)
}


def pick_source_mockup_mug(product: dict, color_variant_ids: list[int] | None = None) -> dict:
    """Pick the mug mockup that shows the design clearly (right view, not front)."""
    imgs = product.get("images", [])
    if not imgs:
        raise ValueError("No mockup images on product")

    pub_imgs = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub_imgs or imgs

    if color_variant_ids:
        wanted = set(color_variant_ids)
        filtered = [i for i in pool if wanted.intersection(i.get("variant_ids") or [])]
        if filtered:
            pool = filtered

    bp = product.get("blueprint_id")
    wanted_angles = MUG_DESIGN_ANGLE_IDS.get(bp, ())

    for angle in wanted_angles:
        for i in pool:
            if _url_contains_angle(i.get("src", ""), angle):
                return i

    for i in pool:
        pos = (i.get("position") or "").lower()
        if pos == "other":
            return i

    for i in pool:
        pos = (i.get("position") or "").lower()
        if "front" in pos:
            return i

    for i in pool:
        if i.get("is_default"):
            return i
    return pool[0]
