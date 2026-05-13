"""Background removal with rembg (u2netp) + alpha cleanup + bbox crop."""
import io

import numpy as np
from PIL import Image
from rembg import new_session, remove

_SESSION = None


def get_session():
    global _SESSION
    if _SESSION is None:
        _SESSION = new_session("u2netp")
    return _SESSION


def detoure(input_bytes: bytes) -> Image.Image:
    """Return an RGBA PIL Image, foreground only, cropped to bbox."""
    output = remove(input_bytes, session=get_session())
    img = Image.open(io.BytesIO(output)).convert("RGBA")

    arr = np.array(img)
    arr[..., 3] = np.where(arr[..., 3] < 30, 0, arr[..., 3])
    img = Image.fromarray(arr)

    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img
