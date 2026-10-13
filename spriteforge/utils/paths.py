"""Path helpers. Confines all user-supplied export paths to the export root."""
from __future__ import annotations

from pathlib import Path


def safe_export_path(root: Path, name: str, fmt: str) -> Path:
    """Resolve `name` under `root`, rejecting traversal. Raises ValueError on escape."""
    stem = "".join(c for c in name if c.isalnum() or c in "-_ ").strip().replace(" ", "_") or "sprite"
    ext = {"png": ".png", "spritesheet": ".png", "godot-tres": ".tres"}[fmt]
    candidate = (root / f"{stem}{ext}").resolve()
    if not str(candidate).startswith(str(root.resolve())):
        raise ValueError(f"export path escapes root: {candidate}")
    return candidate