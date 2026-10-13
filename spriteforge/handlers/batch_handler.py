"""Batch job runner — reads a queue of SpriteRequests from JSON and fans them out."""
from __future__ import annotations

import json
from pathlib import Path

from spriteforge.core.engine import SpriteEngine
from spriteforge.core.prompt import SpriteRequest
from spriteforge.handlers.export_handler import handle_export
from spriteforge.utils.logging import get_logger

log = get_logger(__name__)


def run_batch(engine: SpriteEngine, job_file: Path, export_root: str) -> int:
    """Execute a batch job file. Returns number of sprites written."""
    jobs = json.loads(job_file.read_text(encoding="utf-8"))
    written = 0
    for idx, job in enumerate(jobs):
        req = SpriteRequest(**job)
        result = engine.generate_sprite(req)
        for frame_idx, frame in enumerate(result.frames):
            name = f"{job.get('subject', 'sprite')}_{idx}_{frame_idx}"
            handle_export([frame], "png", export_root, name)
            written += 1
    log.info("batch done: %d sprites written", written)
    return written