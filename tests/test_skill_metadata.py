from __future__ import annotations

from pathlib import Path

import yaml


def test_skill_frontmatter_is_valid_yaml():
    skill_path = Path(__file__).resolve().parents[1] / "suno-lyric-writer" / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    frontmatter = text.split("---", 2)[1]
    parsed = yaml.safe_load(frontmatter)

    assert parsed["name"] == "muse-lyric"
    assert "Suno" in parsed["description"]
    assert "reference audio" in parsed["description"]


def test_openai_yaml_matches_skill_name():
    yaml_path = Path(__file__).resolve().parents[1] / "suno-lyric-writer" / "agents" / "openai.yaml"
    parsed = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    assert parsed["interface"]["display_name"] == "词灵 / MuseLyric"
    assert "$muse-lyric" in parsed["interface"]["default_prompt"]
    assert parsed["policy"]["allow_implicit_invocation"] is True