"""Exporters: PNG, spritesheet, Godot 4 .tres. All write atomic (tmp + rename)."""
from __future__ import annotations

import json
import os
from pathlib import Path

from PIL import Image


def _atomic_write(path: Path, data: bytes) -> Path:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)
    return path


def export_png(frames: list[Image.Image], target: Path) -> Path:
    if not frames:
        raise ValueError("no frames to export")
    buf = _png_bytes(frames[0])
    return _atomic_write(target, buf)


def export_spritesheet(frames: list[Image.Image], target: Path) -> Path:
    if not frames:
        raise ValueError("no frames to export")
    w, h = frames[0].size
    sheet = Image.new("RGBA", (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * w, 0))
    return _atomic_write(target, _png_bytes(sheet))


def export_godot_tres(frames: list[Image.Image], target: Path) -> Path:
    # Companion PNG next to the .tres so Godot can resolve the texture.
    png_target = target.with_suffix(".png")
    export_spritesheet(frames, png_target)
    meta = {
        "resource_name": target.stem,
        "resource_type": "SpriteFrames",
        "png": png_target.name,
        "frame_count": len(frames),
        "frame_size": list(frames[0].size),
    }
    return _atomic_write(target, json.dumps(meta, indent=2).encode("utf-8"))


def _png_bytes(img: Image.Image) -> bytes:
    from io import BytesIO
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()