# Security Policy

## Scope

sprite-forge-ai is a **local, offline** desktop tool. It does not
transmit prompts, seeds, or generated assets anywhere. The only network
activity is the explicit model-weight downloader in
`spriteforge/services/model_registry.py`, which is user-initiated.

## Reporting a vulnerability

Open a private security advisory on GitHub, or email
`security@sprite-forge-ai.dev`. Do not open a public issue for
unpatched vulnerabilities.

Include: affected version, reproduction steps, and whether the issue
involves arbitrary file write, pickle deserialization, or model-weight
tampering.

## Known attack surface

- **Model loading** — `.safetensors` only. `.ckpt` / `.pt` pickle
  loading is disabled by default (`allow_pickle = false` in
  `config/default.toml`). Enabling it is on you.
- **Plugin post-processors** — loaded from `spriteforge/plugins/`.
  Third-party plugins run with full process privileges. Audit before
  installing.
- **Export paths** — user-supplied output directories are normalized
  and confined to the configured `export_root`.

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security  |
| < 0.3   | no        |