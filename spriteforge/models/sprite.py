"""Sprite domain object — the thing a user actually edits and exports."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Sprite:
    name: str
    png_path: Path
    width: int
    height: int
    tags: list[str] = field(default_factory=list)
    palette: str = "nes"
    seed: int = 6767

    def is_power_of_two(self) -> bool:
        return (self.width & (self.width - 1)) == 0 and (self.height & (self.height - 1)) == 0