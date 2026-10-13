"""LocalDiffusionBackend — wraps a diffusers pipeline for offline sprite generation."""
from __future__ import annotations

from PIL import Image

from spriteforge.config.schema import Config
from spriteforge.utils.logging import get_logger

log = get_logger(__name__)


class LocalDiffusionBackend:
    """Thin wrapper around a diffusers `StableDiffusionPipeline`.

    Lazy-loads the model on first `generate` call so the UI can start fast.
    Device selection honors cfg.generation.device; "auto" picks cuda > mps > cpu.
    """

    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self._pipe = None

    def _ensure_pipe(self):
        if self._pipe is not None:
            return self._pipe
        import torch
        from diffusers import AutoPipelineForText2Image

        device = self._pick_device(torch)
        log.info("loading backend=%s on %s", self.cfg.generation.backend, device)
        pipe = AutoPipelineForText2Image.from_pretrained(
            self._model_id(), torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
        self._pipe = pipe.to(device)
        return self._pipe

    def _model_id(self) -> str:
        return {
            "sdxl-turbo": "stabilityai/sdxl-turbo",
            "sd15-pixel": "nerijs/pixel-art-xl",
            "flux-schnell": "black-forest-labs/FLUX.1-schnell",
        }[self.cfg.generation.backend]

    @staticmethod
    def _pick_device(torch) -> str:
        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def generate(self, prompt: str, *, seed: int, steps: int, guidance: float,
                 resolution: int, batch: int) -> list[Image.Image]:
        import torch

        pipe = self._ensure_pipe()
        gen = torch.Generator(device=pipe.device).manual_seed(seed)
        result = pipe(
            prompt=prompt,
            num_inference_steps=steps,
            guidance_scale=guidance,
            height=resolution,
            width=resolution,
            num_images_per_prompt=batch,
            generator=gen,
        )
        return list(result.images)