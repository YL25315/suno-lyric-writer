from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from conftest import load_script_module


def test_run_json_reports_non_json_output(monkeypatch):
    module = load_script_module("media_reference_probe")

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0, stdout="not json", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(SystemExit) as exc_info:
        module.run_json(["ffprobe"])

    assert "non-JSON" in str(exc_info.value)
    assert "not json" in str(exc_info.value)


def test_run_command_includes_stderr(monkeypatch):
    module = load_script_module("media_reference_probe")

    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0], output="", stderr="bad codec")

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(SystemExit) as exc_info:
        module.run_command(["ffmpeg"])

    assert "bad codec" in str(exc_info.value)


def test_parse_args_rejects_time_without_extract_audio():
    module = load_script_module("media_reference_probe")

    with pytest.raises(SystemExit):
        module.parse_args(["song.mp3", "--start", "00:30"])


def test_parse_args_rejects_invalid_time_format():
    module = load_script_module("media_reference_probe")

    with pytest.raises(SystemExit):
        module.parse_args(["song.mp3", "--extract-audio", "out.wav", "--duration", "1:99"])


def test_summarize_probe_collects_streams_and_tags():
    module = load_script_module("media_reference_probe")
    probe = {
        "format": {
            "duration": "95.5",
            "format_name": "mp3",
            "format_long_name": "MP3",
            "bit_rate": "192000",
            "tags": {"artist": "demo"},
        },
        "streams": [
            {"codec_type": "audio", "codec_name": "mp3", "sample_rate": "44100", "channels": 2, "duration": "95.5"},
            {"codec_type": "video", "codec_name": "h264", "width": 1920, "height": 1080, "r_frame_rate": "30/1"},
        ],
    }

    summary = module.summarize_probe(Path("song.mp3"), probe)

    assert summary["duration_seconds"] == 95.5
    assert summary["audio_streams"][0]["codec"] == "mp3"
    assert summary["video_streams"][0]["width"] == 1920
    assert summary["tags"] == {"artist": "demo"}


def test_extract_audio_builds_expected_ffmpeg_command(monkeypatch):
    module = load_script_module("media_reference_probe")
    commands = []

    monkeypatch.setattr(module.shutil, "which", lambda name: "ffmpeg" if name == "ffmpeg" else None)
    monkeypatch.setattr(module, "run_command", lambda cmd: commands.append(cmd))

    module.extract_audio(Path("song.mp4"), Path("out.wav"), "00:10", "30")

    assert commands == [
        ["ffmpeg", "-y", "-ss", "00:10", "-i", "song.mp4", "-t", "30", "-vn", "-ac", "1", "-ar", "16000", "out.wav"]
    ]
