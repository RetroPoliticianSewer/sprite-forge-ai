"""SpriteEngine — the orchestrator. Backend-agnostic; post-processors are pluggable."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np
from PIL import Image

from spriteforge.config.schema import Config
from spriteforge.core.prompt import build_prompt, SpriteRequest
from spriteforge.core.postprocess import apply_pipeline
from spriteforge.core.backends import get_backend
from spriteforge.utils.logging import get_logger

log = get_logger(__name__)


class Backend(Protocol):
    def generate(self, prompt: str, *, seed: int, steps: int, guidance: float,
                 resolution: int, batch: int) -> list[Image.Image]: ...


@dataclass(slots=True)
class SpriteResult:
    frames: list[Image.Image]
    seed: int
    prompt: str
    backend: str


class SpriteEngine:
    """Owns the diffusion backend and the post-process pipeline.

    Concurrency: single-threaded per instance. The Qt worker wraps this in a
    QThread; do not call from multiple threads.
    """

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.backend: Backend = get_backend(cfg.generation.backend, cfg)

    def generate_sprite(self, req: SpriteRequest) -> SpriteResult:
        prompt = build_prompt(req)
        log.info("generate backend=%s seed=%d res=%d", self.cfg.generation.backend,
                 req.seed, self.cfg.generation.default_resolution)

        raw = self.backend.generate(
            prompt,
            seed=req.seed,
            steps=self.cfg.generation.steps,
            guidance=self.cfg.generation.guidance,
            resolution=self.cfg.generation.default_resolution,
            batch=req.count,
        )

        frames = [apply_pipeline(img, self.cfg.postprocess) for img in raw]
        return SpriteResult(frames=frames, seed=req.seed, prompt=prompt,
                            backend=self.cfg.generation.backend)