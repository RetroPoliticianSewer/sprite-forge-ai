# Contributing to sprite-forge-ai

sprite-forge-ai is an open-source desktop tool for generating 2D game
sprites, tilesets, and animation frames with local diffusion models.
Contributions are welcome — read this before opening a PR.

## Dev setup

```bash
git clone https://github.com/sprite-forge-ai/sprite-forge-ai
cd sprite-forge-ai
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install -e ".[dev]"
python -m spriteforge.app
```

Python 3.11+ required. CUDA 12.1+ recommended; CPU fallback works but is
slow (expect 20–40s per 64x64 sprite on a modern Ryzen).

## Branch + commit style

- Branch: `feat/<scope>`, `fix/<scope>`, `chore/<scope>`
- Commits: conventional commits, imperative mood, <=72 char subject
- One logical change per PR. No reformat-everything PRs.

## What we want

- New sprite post-processors (outline, palette quantize, pixel-snap)
- New export targets (Godot 4 `.tres`, Unity `.meta`, Aseprite `.aseprite`)
- Backend adapters for new diffusion pipelines (SDXL-Turbo, Flux-schnell)
- Determinism fixes — same seed + same prompt must yield same PNG bytes

## What we reject

- Anything that phones home. This tool runs offline by default.
- Model weights committed to the repo. Use the downloader.
- Silent behavior changes to the seed contract.

## Tests

```bash
pytest -q
pytest --cov=spriteforge --cov-report=term-missing
```

Every new post-processor needs a golden-image test under
`tests/fixtures/`.