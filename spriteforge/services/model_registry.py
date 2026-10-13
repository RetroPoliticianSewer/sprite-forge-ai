"""Model registry — lists known backends and downloads weights on demand."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from spriteforge.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class ModelEntry:
    name: str
    repo_id: str
    size_gb: float
    license: str


KNOWN_MODELS: tuple[ModelEntry, ...] = (
    ModelEntry("sdxl-turbo", "stabilityai/sdxl-turbo", 6.9, "stability-nc"),
    ModelEntry("sd15-pixel", "nerijs/pixel-art-xl", 2.1, "creativeml-openrail"),
    ModelEntry("flux-schnell", "black-forest-labs/FLUX.1-schnell", 23.8, "apache-2.0"),
)


def list_models() -> tuple[ModelEntry, ...]:
    return KNOWN_MODELS


def is_downloaded(entry: ModelEntry, cache_root: Path) -> bool:
    """Check whether the HF cache holds the snapshot for this model."""
    return (cache_root / entry.repo_id.replace("/", "--")).is_dir()