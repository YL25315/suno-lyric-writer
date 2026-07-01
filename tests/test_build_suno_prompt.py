from __future__ import annotations

import argparse

import pytest
from conftest import load_script_module


def test_chinese_field_checks_report_cjk_separately():
    module = load_script_module("build_suno_prompt")
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
    module = load_script_module("build_suno_prompt")
    package = {
        "style_of_music": "indie pop",
        "lyrics": "I leave the light on\nYou never call",
        "exclude_styles": "harsh autotune",
    }

    checks = module.field_checks(package)

    assert "Lyrics words: 8" in checks
    assert not any("CJK" in check for check in checks)


def test_percent_rejects_invalid_values():
    module = load_script_module("build_suno_prompt")

    assert module.percent("70") == 70
    with pytest.raises(argparse.ArgumentTypeError):
        module.percent("101")
    with pytest.raises(argparse.ArgumentTypeError):
        module.percent("loud")


def test_render_markdown_rejects_wrong_runtime_shape():
    module = load_script_module("build_suno_prompt")
    package = {
        "title": "Broken",
        "reference_analysis": "",
        "creative_direction": "",
        "style_of_music": "indie pop",
        "lyrics": "line",
        "exclude_styles": "",
        "parameters": [],
        "production_tips": [],
        "iteration_notes": "",
        "feedback_questions": [],
    }

    with pytest.raises(TypeError, match="parameters"):
        module.render_markdown(package)


def test_build_package_keeps_prompt_fields():
    module = load_script_module("build_suno_prompt")
    args = argparse.Namespace(
        title="Night Bus",
        style="Mandarin indie pop",
        exclude="metal, opera",
        reference_analysis="warm analog drums",
        creative_direction="lonely but driving",
        model="v4.5",
        weirdness=35,
        style_influence=75,
        audio_influence=40,
        vocal="soft male vocal",
        persona="",
        tip=["generate two takes"],
        feedback_question=["Which chorus lands better?"],
        notes="Revise rushed lines.",
    )

    package = module.build_package(args, "first line")

    assert package["title"] == "Night Bus"
    assert package["lyrics"] == "first line"
    assert package["parameters"]["audio_influence"] == 40
    assert package["production_tips"] == ["generate two takes"]
