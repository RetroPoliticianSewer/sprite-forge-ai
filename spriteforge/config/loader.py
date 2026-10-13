"""Loads TOML config from disk and validates it against the schema."""
from __future__ import annotations

import tomli
from pathlib import Path

from spriteforge.config.schema import Config


def load_config(path: Path) -> Config:
    """Read a TOML file and return a validated Config. Raises on malformed input."""
    if not path.is_file():
        raise FileNotFoundError(f"config not found: {path}")
    with path.open("rb") as fh:
        raw = tomli.load(fh)
    return Config.model_validate(raw)