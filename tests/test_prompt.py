"""Prompt builder determinism + shape tests."""
from spriteforge.core.prompt import SpriteRequest, build_prompt


def test_prompt_is_deterministic():
    req = SpriteRequest(subject="goblin archer", kind="enemy", view="side", palette="nes", seed=42)
    assert build_prompt(req) == build_prompt(req)


def test_prompt_contains_palette_line():
    req = SpriteRequest(subject="slime", palette="gb")
    out = build_prompt(req)
    assert "Game Boy" in out
    assert "transparent background" in out


def test_prompt_includes_tags():
    req = SpriteRequest(subject="knight", style_tags=["metallic", "worn armor"])
    assert "metallic" in build_prompt(req)