"""Batch job model — one row in a batch JSON file."""
from __future__ import annotations

from pydantic import BaseModel, Field


class BatchJob(BaseModel):
    subject: str
    kind: str = "character"
    view: str = "side"
    palette: str = "nes"
    count: int = Field(default=1, ge=1, le=32)
    seed: int = 6767
    style_tags: list[str] = []