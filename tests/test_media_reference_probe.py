from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest


def load_module():
    path = Path(__file__).resolve().parents[1] / "suno-lyric-writer" / "scripts" / "media_reference_probe.py"
    spec = importlib.util.spec_from_file_location("media_reference_probe", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run_json_reports_non_json_output(monkeypatch):
    module = load_module()

    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(args[0], 0, stdout="not json", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(SystemExit) as exc_info:
        module.run_json(["ffprobe"])

    assert "non-JSON" in str(exc_info.value)
    assert "not json" in str(exc_info.value)


def test_run_command_includes_stderr(monkeypatch):
    module = load_module()

    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0], output="", stderr="bad codec")

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(SystemExit) as exc_info:
        module.run_command(["ffmpeg"])

    assert "bad codec" in str(exc_info.value)