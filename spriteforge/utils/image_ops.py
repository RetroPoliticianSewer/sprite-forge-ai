"""Low-level image helpers used by postprocess and exporters."""
from __future__ import annotations

import numpy as np
from PIL import Image


def bbox_of_alpha(img: Image.Image, threshold: int = 1) -> tuple[int, int, int, int]:
    """Return the tight (l, t, r, b) bounding box of non-transparent pixels."""
    alpha = np.array(img.convert("RGBA"))[..., 3]
    ys, xs = np.where(alpha >= threshold)
    if ys.size == 0:
        return (0, 0, img.width, img.height)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def autocrop(img: Image.Image, threshold: int = 1) -> Image.Image:
    return img.crop(bbox_of_alpha(img, threshold))