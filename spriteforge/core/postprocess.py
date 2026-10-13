"""Post-process pipeline: pixel-snap, palette quantize, outline, alpha trim."""
from __future__ import annotations

import numpy as np
from PIL import Image

from spriteforge.config.schema import PostProcessConfig


def apply_pipeline(img: Image.Image, cfg: PostProcessConfig) -> Image.Image:
    """Run the configured post-processors in order. Returns a new image."""
    out = img.convert("RGBA")
    if cfg.palette_quantize:
        out = _quantize(out, cfg.palette_size)
    if cfg.pixel_snap:
        out = _snap(out)
    if cfg.outline != "none":
        out = _outline(out, cfg.outline)
    out = _trim_alpha(out, cfg.alpha_threshold)
    return out


def _quantize(img: Image.Image, n: int) -> Image.Image:
    return img.convert("P", palette=Image.Palette.ADAPTIVE, colors=n).convert("RGBA")


def _snap(img: Image.Image) -> Image.Image:
    # Nearest-neighbour keeps hard pixel edges; bilinear would smear them.
    w, h = img.size
    return img.resize((w, h), Image.Resampling.NEAREST)


def _outline(img: Image.Image, mode: str) -> Image.Image:
    arr = np.array(img)
    alpha = arr[..., 3] > 0
    edge = np.zeros_like(alpha)
    edge[1:-1, 1:-1] = (
        alpha[1:-1, 1:-1]
        & ~(alpha[:-2, 1:-1] & alpha[2:, 1:-1] & alpha[1:-1, :-2] & alpha[1:-1, 2:])
    )
    arr[edge] = [0, 0, 0, 255]
    return Image.fromarray(arr, "RGBA")


def _trim_alpha(img: Image.Image, threshold: int) -> Image.Image:
    arr = np.array(img)
    arr[..., 3][arr[..., 3] < threshold] = 0
    return Image.fromarray(arr, "RGBA")