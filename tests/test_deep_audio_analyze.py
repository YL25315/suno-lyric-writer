from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest
from conftest import load_script_module


def test_suno_traits_include_half_time_for_fast_bpm():
    module = load_script_module("deep_audio_analyze")
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
    module = load_script_module("deep_audio_analyze")

    assert module.parse_time_seconds("90") == 90.0
    assert module.parse_time_seconds("01:30") == 90.0
    assert module.parse_time_seconds("01:02:03") == 3723.0


def test_parse_time_seconds_rejects_invalid_clock():
    module = load_script_module("deep_audio_analyze")

    assert module.parse_time_seconds("01:99") is None
    assert module.parse_time_seconds("bad") is None


def test_parse_args_rejects_invalid_start():
    module = load_script_module("deep_audio_analyze")

    with pytest.raises(SystemExit):
        module.parse_args(["song.mp3", "--start", "1:99"])


def test_estimate_tempo_handles_empty_envelope():
    module = load_script_module("deep_audio_analyze")

    tempo = module.estimate_tempo([], hop_seconds=0.05, min_bpm=60, max_bpm=180)

    assert tempo == {"bpm": None, "confidence": "low", "candidates": []}


def test_optional_librosa_reports_tempo_and_chroma_errors(monkeypatch):
    module = load_script_module("deep_audio_analyze")
    import numpy as np

    fake_librosa = types.SimpleNamespace()
    fake_librosa.load = lambda *args, **kwargs: (np.ones(100), 100)
    fake_librosa.beat = types.SimpleNamespace(
        beat_track=lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("beat failed"))
    )
    fake_librosa.feature = types.SimpleNamespace(
        chroma_cqt=lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("chroma failed")),
        chroma_stft=lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("fallback failed")),
    )
    monkeypatch.setitem(sys.modules, "librosa", fake_librosa)

    result = module.optional_librosa_analysis(
        Path("song.mp3"),
        sample_rate=100,
        start=None,
        duration=None,
        window_seconds=1.0,
        disabled=False,
    )

    assert result["available"] is False
    assert "chroma analysis failed" in result["reason"]
    assert result["tempo_error"] == "beat failed"
