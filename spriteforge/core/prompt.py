"""Prompt builder. Turns a SpriteRequest into a diffusion-ready prompt string."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


SpriteKind = Literal["character", "enemy", "item", "tile", "effect", "ui"]
ViewAngle = Literal["side", "top-down", "isometric", "three-quarter"]


@dataclass(slots=True)
class SpriteRequest:
    subject: str
    kind: SpriteKind = "character"
    view: ViewAngle = "side"
    palette: str = "nes"
    count: int = 1
    seed: int = 6767
    style_tags: list[str] = field(default_factory=list)


_STYLE_SUFFIX = {
    "nes": "8-bit NES palette, limited to 24 colors, crisp pixels",
    "snes": "16-bit SNES palette, 48 colors, soft dithering",
    "gb": "Game Boy 4-shade green palette, chunky pixels",
    "modern": "modern pixel art, 64 colors, subtle shading, clean outlines",
}


def build_prompt(req: SpriteRequest) -> str:
    """Compose the final prompt. Deterministic given identical input."""
    palette_line = _STYLE_SUFFIX.get(req.palette, _STYLE_SUFFIX["nes"])
    tags = ", ".join(req.style_tags) if req.style_tags else "no extra tags"
    return (
        f"{req.subject}, 2D game {req.kind} sprite, {req.view} view, "
        f"transparent background, centered, {palette_line}, {tags}"
    )