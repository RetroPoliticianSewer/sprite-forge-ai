"""Backend registry. Maps config name -> concrete diffusion pipeline wrapper."""
from __future__ import annotations

from typing import Callable

from spriteforge.config.schema import Config
from spriteforge.services.diffusion_local import LocalDiffusionBackend


_REGISTRY: dict[str, Callable[[Config], object]] = {}


def register(name: str) -> Callable[[Callable[[Config], object]], Callable[[Config], object]]:
    def deco(fn: Callable[[Config], object]) -> Callable[[Config], object]:
        _REGISTRY[name] = fn
        return fn
    return deco


def get_backend(name: str, cfg: Config) -> object:
    if name not in _REGISTRY:
        raise KeyError(f"unknown backend: {name!r} (have {sorted(_REGISTRY)})")
    return _REGISTRY[name](cfg)


@register("sdxl-turbo")
@register("sd15-pixel")
@register("flux-schnell")
def _local(cfg: Config) -> object:
    return LocalDiffusionBackend(cfg)