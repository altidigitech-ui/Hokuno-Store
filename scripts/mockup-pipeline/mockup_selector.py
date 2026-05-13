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


_POSITION_NEEDLES_BY_TYPE = {
    "tshirt":    ["back-2", "back_2", "back-1", "back"],
    "mug":       ["front", "default"],
    "casquette": ["front"],
    "phonecase": ["front", "default"],
    "default":   ["front", "default"],
}


def pick_source_mockup(product: dict, ptype: str) -> dict:
    if ptype == "mug":
        return pick_source_mockup_mug(product)
    if ptype == "tshirt":
        return pick_source_mockup_tshirt(product)

    imgs = product.get("images", [])
    if not imgs:
        raise ValueError("No mockup images on product")

    pub_imgs = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub_imgs or imgs

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


# T-shirt back-of-shirt template angle IDs, by Printify BP 6 (Gildan 5000).
# Some legacy product mockups don't have explicit position="back" labels
# (everything labeled "other"), so we also match angle ID in the image URL.
TSHIRT_BACK_ANGLE_IDS = ("92571", "102006")


def pick_source_mockup_tshirt(product: dict) -> dict:
    """Pick a t-shirt back mockup. Handles legacy products without 'back' position."""
    imgs = product.get("images", [])
    if not imgs:
        raise ValueError("No mockup images on product")

    pub_imgs = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub_imgs or imgs

    # Priority 1: explicit back-* position label
    for needle in ("back-2", "back_2", "back-1", "back"):
        for i in pool:
            if needle in (i.get("position") or "").lower():
                return i

    # Priority 2: known back angle IDs in image URL (legacy products labeled "other")
    for angle in TSHIRT_BACK_ANGLE_IDS:
        for i in pool:
            if _url_contains_angle(i.get("src", ""), angle):
                return i

    # Priority 3: default / first image
    for i in pool:
        if i.get("is_default"):
            return i
    return pool[0]


# Mug mockup template IDs that show the design clearly (empirically identified).
# Keys are Printify blueprint_id. The values are angle/template fragments that
# appear in the image src URL pattern: /mockup/{pid}/{variant_id}/{angle_id}/...
# Listed in priority order; the first match wins.
MUG_DESIGN_ANGLE_IDS = {
    478: ("6311", "101797"),   # Ceramic Mug 11oz, 15oz (light)
    479: ("6407", "101583"),   # Ceramic Mug Black 11oz, 15oz (dark)
}


def _url_contains_angle(src: str, angle_id: str) -> bool:
    return f"/{angle_id}/" in (src or "")


def pick_source_mockup_mug(product: dict) -> dict:
    """Pick the mug mockup that shows the design clearly.

    The default Printify 'front' angle hides the design behind the handle for
    BP 478 / BP 479. The right view shows it. We pick by template angle id
    (hardcoded for known blueprints), then fall back to position/default.
    """
    imgs = product.get("images", [])
    if not imgs:
        raise ValueError("No mockup images on product")

    pub_imgs = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub_imgs or imgs

    bp = product.get("blueprint_id")
    wanted_angles = MUG_DESIGN_ANGLE_IDS.get(bp, ())

    # Priority 1: angle IDs known to show the design
    for angle in wanted_angles:
        for i in pool:
            if _url_contains_angle(i.get("src", ""), angle):
                return i

    # Priority 2: anything that's NOT the "front" default (which hides the design
    # for these blueprints) — try the first "other" position.
    for i in pool:
        pos = (i.get("position") or "").lower()
        if pos == "other":
            return i

    # Priority 3: front default
    for i in pool:
        pos = (i.get("position") or "").lower()
        if "front" in pos:
            return i

    for i in pool:
        if i.get("is_default"):
            return i
    return pool[0]
