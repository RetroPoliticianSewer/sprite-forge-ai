"""Handles export actions: PNG, spritesheet, and Godot .tres."""
from __future__ import annotations

from pathlib import Path

from spriteforge.services.exporter import export_png, export_spritesheet, export_godot_tres
from spriteforge.utils.paths import safe_export_path


def handle_export(frames: list, fmt: str, export_root: str, name: str) -> Path:
    """Dispatch to the correct exporter. Returns the written path."""
    out_dir = Path(export_root).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = safe_export_path(out_dir, name, fmt)

    if fmt == "png":
        return export_png(frames, target)
    if fmt == "spritesheet":
        return export_spritesheet(frames, target)
    if fmt == "godot-tres":
        return export_godot_tres(frames, target)
    raise ValueError(f"unsupported export format: {fmt!r}")