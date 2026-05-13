"""Detect which Hokuno collection a Printify product belongs to."""


def detect_collection(product: dict) -> str:
    title = (product.get("title") or "").upper()
    if "WANTED" in title:
        return "WANTED"
    if "DIRECTION" in title:
        return "DIRECTION"
    if "MYTHOLOGIE" in title or "MYTHOLOGY" in title:
        return "MYTHOLOGIE"
    return "DESIGN HOKUNO"
