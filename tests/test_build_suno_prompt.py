from __future__ import annotations

import importlib.util
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[1] / "suno-lyric-writer" / "scripts" / "build_suno_prompt.py"
    spec = importlib.util.spec_from_file_location("build_suno_prompt", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_chinese_field_checks_report_cjk_separately():
    module = load_module()
    package = {
        "style_of_music": "Mandarin indie pop",
        "lyrics": "[Verse 1]\n我把旧车票夹进书里\n你没回头",
        "exclude_styles": "",
    }

    checks = module.field_checks(package)

    assert "Lyrics non-CJK words: 2" in checks
    assert "Lyrics CJK characters: 13" in checks
    assert not any(check == "Lyrics words: 1" for check in checks)


def test_english_field_checks_keep_word_count():
    module = load_module()
    package = {
        "style_of_music": "indie pop",
        "lyrics": "I leave the light on\nYou never call",
        "exclude_styles": "harsh autotune",
    }

    checks = module.field_checks(package)

    assert "Lyrics words: 8" in checks
    assert not any("CJK" in check for check in checks)