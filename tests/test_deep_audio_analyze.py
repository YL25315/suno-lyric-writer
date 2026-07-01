from __future__ import annotations

import importlib.util
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[1] / "suno-lyric-writer" / "scripts" / "deep_audio_analyze.py"
    spec = importlib.util.spec_from_file_location("deep_audio_analyze", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_suno_traits_include_half_time_for_fast_bpm():
    module = load_module()
    tempo = {
        "bpm": 184,
        "alternate_feels": [{"bpm": 92.0, "feel": "half-time feel"}],
    }
    dynamics = {"dynamic_profile": "strong dynamic contrast", "brightness": "bright/noisy texture"}
    sections = [{"role_hint": "chorus/drop or dense section", "energy": "high"}]
    tonal = {"available": False}

    traits = module.build_suno_traits(tempo, dynamics, sections, tonal, onset_density=40)

    assert traits[0] == "92.0 BPM half-time / 184 BPM double-time feel"


def test_parse_time_seconds_accepts_seconds_and_clock():
    module = load_module()

    assert module.parse_time_seconds("90") == 90.0
    assert module.parse_time_seconds("01:30") == 90.0
    assert module.parse_time_seconds("01:02:03") == 3723.0