#!/usr/bin/env python3
"""Probe reference audio/video and optionally extract analysis-ready audio."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from _common import emit_text, time_value


def run_json(cmd: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise SystemExit(f"error: missing executable: {cmd[0]}") from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        raise SystemExit(f"error: command failed: {message}") from exc
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        sample = (result.stdout or result.stderr or "").strip()[:800]
        raise SystemExit(f"error: ffprobe returned non-JSON output: {sample or exc}") from exc


def run_command(cmd: list[str]) -> None:
    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise SystemExit(f"error: missing executable: {cmd[0]}") from exc
    except subprocess.CalledProcessError as exc:
        message = (exc.stderr or exc.stdout or "").strip()
        raise SystemExit(f"error: command failed with exit code {exc.returncode}: {message}") from exc


def seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def format_seconds(value: float | None) -> str:
    if value is None:
        return "unknown"
    minutes = int(value // 60)
    secs = value - minutes * 60
    return f"{minutes}:{secs:04.1f}"


def shorten_text(value: object, limit: int = 420) -> str:
    text = str(value).replace("\r\n", "\n").replace("\r", "\n")
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + f"... [truncated {len(text) - limit} chars]"


def summarize_probe(path: Path, probe: dict[str, Any]) -> dict[str, Any]:
    fmt = probe.get("format", {})
    streams = probe.get("streams", [])
    audio = [stream for stream in streams if stream.get("codec_type") == "audio"]
    video = [stream for stream in streams if stream.get("codec_type") == "video"]
    return {
        "path": str(path),
        "duration_seconds": seconds(fmt.get("duration")),
        "format_name": fmt.get("format_name", ""),
        "format_long_name": fmt.get("format_long_name", ""),
        "bit_rate": fmt.get("bit_rate", ""),
        "audio_streams": [
            {
                "codec": stream.get("codec_name", ""),
                "sample_rate": stream.get("sample_rate", ""),
                "channels": stream.get("channels", ""),
                "channel_layout": stream.get("channel_layout", ""),
                "duration_seconds": seconds(stream.get("duration")),
            }
            for stream in audio
        ],
        "video_streams": [
            {
                "codec": stream.get("codec_name", ""),
                "width": stream.get("width", ""),
                "height": stream.get("height", ""),
                "frame_rate": stream.get("r_frame_rate", ""),
                "duration_seconds": seconds(stream.get("duration")),
            }
            for stream in video
        ],
        "tags": fmt.get("tags", {}),
    }


def render_markdown(summary: dict[str, Any], extracted_audio: str | None) -> str:
    lines = [
        "# Reference Media Probe",
        "",
        f"- Path: {summary['path']}",
        f"- Duration: {format_seconds(summary['duration_seconds'])}",
        f"- Format: {summary['format_long_name'] or summary['format_name'] or 'unknown'}",
        f"- Bit rate: {summary['bit_rate'] or 'unknown'}",
        "",
        "## Audio Streams",
    ]
    audio_streams = summary["audio_streams"]
    if audio_streams:
        for idx, stream in enumerate(audio_streams, 1):
            lines.append(
                f"- Audio {idx}: {stream['codec'] or 'unknown'}, "
                f"{stream['sample_rate'] or 'unknown'} Hz, "
                f"{stream['channels'] or 'unknown'} channels, "
                f"{format_seconds(stream['duration_seconds'])}"
            )
    else:
        lines.append("- None detected")
    lines.extend(["", "## Video Streams"])
    video_streams = summary["video_streams"]
    if video_streams:
        for idx, stream in enumerate(video_streams, 1):
            lines.append(
                f"- Video {idx}: {stream['codec'] or 'unknown'}, "
                f"{stream['width'] or '?'}x{stream['height'] or '?'}, "
                f"{stream['frame_rate'] or 'unknown'} fps, "
                f"{format_seconds(stream['duration_seconds'])}"
            )
    else:
        lines.append("- None detected")
    if extracted_audio:
        lines.extend(["", "## Extracted Audio", f"- {extracted_audio}"])
    tags = summary.get("tags") or {}
    if tags:
        lines.extend(["", "## Tags"])
        for key, value in sorted(tags.items()):
            lines.append(f"- {key}: {shorten_text(value)}")
    lines.extend(
        [
            "",
            "## Next Analysis Prompt",
            "Use this media as a reference. Extract genre, tempo feel, groove, instrumentation, vocal tone, production texture, structure, lyric point of view, hook mechanics, and 2-3 Suno-ready creative directions. Borrow traits, not melody or lyrics.",
            "",
        ]
    )
    return "\n".join(lines)


def extract_audio(media_path: Path, out_path: Path, start: str | None, duration: str | None) -> None:
    if not shutil.which("ffmpeg"):
        raise SystemExit("error: ffmpeg is required for --extract-audio")
    cmd = ["ffmpeg", "-y"]
    if start:
        cmd.extend(["-ss", start])
    cmd.extend(["-i", str(media_path)])
    if duration:
        cmd.extend(["-t", duration])
    cmd.extend(["-vn", "-ac", "1", "-ar", "16000", str(out_path)])
    run_command(cmd)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", help="Reference audio or video file")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--extract-audio", help="Write 16 kHz mono WAV for speech/music analysis")
    parser.add_argument("--start", type=time_value, help="Start time for --extract-audio only, e.g. 30 or 00:30")
    parser.add_argument("--duration", type=time_value, help="Duration for --extract-audio only, e.g. 60 or 01:00")
    args = parser.parse_args(argv)
    if (args.start or args.duration) and not args.extract_audio:
        parser.error("--start and --duration only apply when --extract-audio is set")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    media_path = Path(args.media)
    if not media_path.exists():
        print(f"error: media file not found: {media_path}", file=sys.stderr)
        return 2
    if not shutil.which("ffprobe"):
        print("error: ffprobe is required", file=sys.stderr)
        return 2
    probe = run_json(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(media_path),
        ]
    )
    extracted_audio = None
    if args.extract_audio:
        out_path = Path(args.extract_audio)
        extract_audio(media_path, out_path, args.start, args.duration)
        extracted_audio = str(out_path)
    summary = summarize_probe(media_path, probe)
    if args.json:
        if extracted_audio:
            summary["extracted_audio"] = extracted_audio
        emit_text(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        emit_text(render_markdown(summary, extracted_audio))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
