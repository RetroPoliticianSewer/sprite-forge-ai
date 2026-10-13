"""Pydantic schema mirroring config/default.toml. Fails loud on malformed config."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    name: str
    version: str
    theme: Literal["dark", "light"] = "dark"


class GenerationConfig(BaseModel):
    backend: Literal["sdxl-turbo", "sd15-pixel", "flux-schnell"]
    default_resolution: int = Field(ge=16, le=512)
    steps: int = Field(ge=1, le=50)
    guidance: float = Field(ge=0.0, le=20.0)
    batch_size: int = Field(ge=1, le=32)
    seed: int
    device: Literal["auto", "cuda", "cpu", "mps"] = "auto"


class PostProcessConfig(BaseModel):
    pixel_snap: bool = True
    palette_quantize: bool = True
    palette_size: int = Field(ge=2, le=256)
    outline: Literal["none", "1px-dark", "2px-dark", "selective"] = "1px-dark"
    alpha_threshold: int = Field(ge=0, le=255)


class ExportConfig(BaseModel):
    export_root: str = "./exports"
    formats: list[str] = ["png"]
    spritesheet_padding: int = Field(ge=0, le=16)


class SecurityConfig(BaseModel):
    allow_pickle: bool = False
    max_export_bytes: int = 268_435_456


class Config(BaseModel):
    app: AppConfig
    generation: GenerationConfig
    postprocess: PostProcessConfig
    export: ExportConfig
    security: SecurityConfig