#!/usr/bin/env python3
"""Analyze reference audio for Suno-ready musical traits."""

from __future__ import annotations

import argparse
import array
import json
import math
import shutil
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any

from _common import emit_text, parse_time_seconds, time_value

PITCH_CLASSES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def format_seconds(value: float | None) -> str:
    if value is None:
        return "unknown"
    minutes = int(value // 60)
    secs = value - minutes * 60
    return f"{minutes}:{secs:04.1f}"


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    pos = (len(ordered) - 1) * pct
    low = int(math.floor(pos))
    high = int(math.ceil(pos))
    if low == high:
        return ordered[low]
    return ordered[low] * (high - pos) + ordered[high] * (pos - low)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def stdev(values: list[float]) -> float:
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def run_ffmpeg_pcm(
    media_path: Path,
    sample_rate: int,
    start: str | None,
    duration: str | None,
    max_duration: float,
) -> bytes:
    if not shutil.which("ffmpeg"):
        raise SystemExit("error: ffmpeg is required")
    cmd = ["ffmpeg", "-v", "error", "-nostdin"]
    if start:
        cmd.extend(["-ss", start])
    cmd.extend(["-i", str(media_path)])
    effective_duration = duration
    if not effective_duration and max_duration > 0:
        effective_duration = str(max_duration)
    if effective_duration:
        cmd.extend(["-t", effective_duration])
    cmd.extend(["-vn", "-ac", "1", "-ar", str(sample_rate), "-f", "s16le", "pipe:1"])
    try:
        result = subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="replace").strip()
        raise SystemExit(f"error: ffmpeg failed: {stderr or exc}") from exc
    return result.stdout


def decode_pcm_samples(pcm: bytes) -> array.array:
    samples = array.array("h")
    samples.frombytes(pcm)
    if sys.byteorder != "little":
        samples.byteswap()
    return samples


def frame_features(
    samples: array.array,
    sample_rate: int,
    frame_seconds: float,
    hop_seconds: float,
) -> list[dict[str, float]]:
    frame_size = max(128, int(sample_rate * frame_seconds))
    hop_size = max(64, int(sample_rate * hop_seconds))
    if len(samples) < frame_size:
        return []
    frames: list[dict[str, float]] = []
    scale = 32768.0
    for start in range(0, len(samples) - frame_size + 1, hop_size):
        end = start + frame_size
        sum_sq = 0.0
        crossings = 0
        prev = samples[start]
        for value in samples[start:end]:
            sample = value / scale
            sum_sq += sample * sample
            if (value >= 0 and prev < 0) or (value < 0 and prev >= 0):
                crossings += 1
            prev = value
        frames.append(
            {
                "time": start / sample_rate,
                "rms": math.sqrt(sum_sq / frame_size),
                "zcr": crossings / frame_size,
            }
        )
    return frames


def moving_average(values: list[float], radius: int) -> list[float]:
    if radius <= 0 or not values:
        return values[:]
    smoothed: list[float] = []
    for idx in range(len(values)):
        start = max(0, idx - radius)
        end = min(len(values), idx + radius + 1)
        smoothed.append(mean(values[start:end]))
    return smoothed


def onset_envelope(frames: list[dict[str, float]]) -> list[float]:
    if not frames:
        return []
    energies = moving_average([math.log(frame["rms"] + 1e-7) for frame in frames], 2)
    flux = [0.0]
    for idx in range(1, len(energies)):
        flux.append(max(0.0, energies[idx] - energies[idx - 1]))
    noise_floor = percentile(flux, 0.55)
    return [max(0.0, value - noise_floor) for value in flux]


def estimate_tempo(
    envelope: list[float],
    hop_seconds: float,
    min_bpm: int,
    max_bpm: int,
) -> dict[str, Any]:
    if len(envelope) < 20 or max(envelope, default=0.0) <= 0:
        return {"bpm": None, "confidence": "low", "candidates": []}
    threshold = percentile(envelope, 0.70)
    env = [value if value >= threshold else 0.0 for value in envelope]
    scores: list[tuple[float, int]] = []
    for bpm in range(min_bpm, max_bpm + 1):
        lag = int(round(60.0 / (bpm * hop_seconds)))
        if lag < 1 or lag >= len(env):
            continue
        score = 0.0
        for idx in range(lag, len(env)):
            score += env[idx] * env[idx - lag]
        if 2 * lag < len(env):
            harmonic = 0.0
            for idx in range(2 * lag, len(env)):
                harmonic += env[idx] * env[idx - 2 * lag]
            score += 0.35 * harmonic
        scores.append((score / max(1, len(env) - lag), bpm))
    if not scores:
        return {"bpm": None, "confidence": "low", "candidates": []}
    scores.sort(reverse=True)
    top_score = scores[0][0]
    candidates = [
        {"bpm": bpm, "score": round(score, 6)}
        for score, bpm in scores[:5]
        if top_score > 0 and score >= top_score * 0.65
    ]
    confidence = "high" if top_score > 0.002 else "medium" if top_score > 0.0004 else "low"
    bpm = scores[0][1]
    alternate_feels: list[dict[str, Any]] = []
    if bpm >= 150 and bpm / 2 >= min_bpm:
        alternate_feels.append({"bpm": round(bpm / 2, 1), "feel": "half-time feel"})
    if bpm <= 85 and bpm * 2 <= max_bpm:
        alternate_feels.append({"bpm": bpm * 2, "feel": "double-time feel"})
    return {
        "bpm": bpm,
        "confidence": confidence,
        "candidates": candidates,
        "alternate_feels": alternate_feels,
    }


def detect_onset_peaks(envelope: list[float], hop_seconds: float) -> list[float]:
    if len(envelope) < 3:
        return []
    threshold = max(percentile(envelope, 0.85), mean(envelope) + stdev(envelope) * 0.5)
    peaks: list[float] = []
    min_gap = max(1, int(0.12 / hop_seconds))
    last_peak = -min_gap
    for idx in range(1, len(envelope) - 1):
        if idx - last_peak < min_gap:
            continue
        if envelope[idx] >= threshold and envelope[idx] >= envelope[idx - 1] and envelope[idx] >= envelope[idx + 1]:
            peaks.append(idx * hop_seconds)
            last_peak = idx
    return peaks


def energy_level(value: float, peak: float) -> str:
    rel = value / peak if peak else 0.0
    if rel < 0.10:
        return "quiet"
    if rel < 0.28:
        return "low"
    if rel < 0.50:
        return "mid"
    if rel < 0.75:
        return "high"
    return "peak"


def window_analysis(
    frames: list[dict[str, float]],
    envelope: list[float],
    window_seconds: float,
    duration_seconds: float,
) -> list[dict[str, Any]]:
    if not frames:
        return []
    window_count = max(1, int(math.ceil(duration_seconds / window_seconds)))
    buckets: list[dict[str, list[float]]] = [
        {"rms": [], "zcr": [], "flux": []} for _ in range(window_count)
    ]
    for idx, frame in enumerate(frames):
        bucket_idx = min(window_count - 1, int(frame["time"] // window_seconds))
        buckets[bucket_idx]["rms"].append(frame["rms"])
        buckets[bucket_idx]["zcr"].append(frame["zcr"])
        if idx < len(envelope):
            buckets[bucket_idx]["flux"].append(envelope[idx])
    peak_rms = max((max(bucket["rms"]) for bucket in buckets if bucket["rms"]), default=0.0)
    raw_windows: list[dict[str, Any]] = []
    for idx, bucket in enumerate(buckets):
        if not bucket["rms"]:
            continue
        start = idx * window_seconds
        end = min(duration_seconds, (idx + 1) * window_seconds)
        avg_rms = mean(bucket["rms"])
        raw_windows.append(
            {
                "start": start,
                "end": end,
                "energy": energy_level(avg_rms, peak_rms),
                "mean_rms": avg_rms,
                "peak_rms": max(bucket["rms"]),
                "mean_zcr": mean(bucket["zcr"]),
                "onset_flux": sum(bucket["flux"]),
            }
        )
    return merge_windows(raw_windows)


def merge_windows(windows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for window in windows:
        if merged and merged[-1]["energy"] == window["energy"]:
            previous = merged[-1]
            previous["end"] = window["end"]
            previous["mean_rms"] = (previous["mean_rms"] + window["mean_rms"]) / 2
            previous["peak_rms"] = max(previous["peak_rms"], window["peak_rms"])
            previous["mean_zcr"] = (previous["mean_zcr"] + window["mean_zcr"]) / 2
            previous["onset_flux"] += window["onset_flux"]
        else:
            merged.append(window.copy())
    for idx, window in enumerate(merged):
        window["role_hint"] = role_hint(idx, merged)
        window["start"] = format_seconds(window["start"])
        window["end"] = format_seconds(window["end"])
        window["mean_rms"] = round(window["mean_rms"], 4)
        window["peak_rms"] = round(window["peak_rms"], 4)
        window["mean_zcr"] = round(window["mean_zcr"], 4)
        window["onset_flux"] = round(window["onset_flux"], 4)
    return merged


def role_hint(idx: int, windows: list[dict[str, Any]]) -> str:
    current = windows[idx]
    energy = current["energy"]
    prev_energy = windows[idx - 1]["energy"] if idx > 0 else None
    next_energy = windows[idx + 1]["energy"] if idx + 1 < len(windows) else None
    high_set = {"high", "peak"}
    low_set = {"quiet", "low"}
    if idx == 0 and energy in low_set:
        return "intro"
    if idx == len(windows) - 1 and energy in low_set:
        return "outro"
    if energy in high_set and prev_energy in low_set:
        return "chorus/drop lift"
    if energy in high_set:
        return "chorus/drop or dense section"
    if energy in low_set and prev_energy in high_set:
        return "breakdown or bridge"
    if next_energy in high_set and energy == "mid":
        return "pre-chorus/build"
    return "verse/groove"


def tempo_feel(bpm: int | None) -> str:
    if bpm is None:
        return "unknown tempo feel"
    if bpm < 70:
        return "slow ballad feel"
    if bpm < 95:
        return "mid-tempo groove"
    if bpm < 125:
        return "upbeat pop groove"
    if bpm < 155:
        return "dance or double-time feel"
    return "fast / high-energy feel"


def brightness_label(zcr_value: float) -> str:
    if zcr_value < 0.035:
        return "dark/warm texture"
    if zcr_value < 0.075:
        return "balanced brightness"
    return "bright/noisy texture"


def dynamic_label(rms_values: list[float]) -> str:
    if not rms_values:
        return "unknown dynamics"
    spread = percentile(rms_values, 0.90) - percentile(rms_values, 0.10)
    if spread < 0.015:
        return "steady compressed energy"
    if spread < 0.05:
        return "moderate section contrast"
    return "strong dynamic contrast"


def key_from_chroma(chroma: Any) -> dict[str, Any]:
    import numpy as np  # type: ignore

    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    chroma = np.asarray(chroma, dtype=float)
    if chroma.sum() <= 0:
        return {"key": None, "mode": None, "confidence": "low"}
    chroma = chroma / chroma.sum()
    scores: list[tuple[float, str, str]] = []
    for root in range(12):
        major_score = float(np.corrcoef(chroma, np.roll(major_profile, root))[0, 1])
        minor_score = float(np.corrcoef(chroma, np.roll(minor_profile, root))[0, 1])
        scores.append((major_score, PITCH_CLASSES[root], "major"))
        scores.append((minor_score, PITCH_CLASSES[root], "minor"))
    scores.sort(reverse=True)
    best = scores[0]
    confidence = "high" if best[0] > 0.65 else "medium" if best[0] > 0.45 else "low"
    return {"key": best[1], "mode": best[2], "confidence": confidence, "score": round(best[0], 3)}


def chord_from_chroma(chroma: Any) -> tuple[str, float]:
    import numpy as np  # type: ignore

    chroma = np.asarray(chroma, dtype=float)
    if chroma.sum() <= 0:
        return "unknown", 0.0
    chroma = chroma / chroma.sum()
    templates: list[tuple[str, Any]] = []
    for root in range(12):
        major = np.zeros(12)
        major[[root, (root + 4) % 12, (root + 7) % 12]] = [1.0, 0.8, 0.9]
        minor = np.zeros(12)
        minor[[root, (root + 3) % 12, (root + 7) % 12]] = [1.0, 0.8, 0.9]
        templates.append((PITCH_CLASSES[root], major))
        templates.append((PITCH_CLASSES[root] + "m", minor))
    scores = [(float(np.dot(chroma, template)), name) for name, template in templates]
    scores.sort(reverse=True)
    return scores[0][1], round(scores[0][0], 3)


def optional_librosa_analysis(
    media_path: Path,
    sample_rate: int,
    start: str | None,
    duration: str | None,
    window_seconds: float,
    disabled: bool,
) -> dict[str, Any]:
    if disabled:
        return {"available": False, "reason": "disabled by --no-librosa"}
    try:
        import librosa  # type: ignore
        import numpy as np  # type: ignore
    except ImportError:
        return {
            "available": False,
            "reason": "install optional dependencies for key/chord analysis: python -m pip install librosa numpy scipy soundfile",
        }
    offset = parse_time_seconds(start) or 0.0
    duration_seconds = parse_time_seconds(duration)
    try:
        y, sr = librosa.load(str(media_path), sr=sample_rate, mono=True, offset=offset, duration=duration_seconds)
    except Exception as exc:
        return {"available": False, "reason": f"librosa failed to load audio: {exc}"}
    if len(y) == 0:
        return {"available": False, "reason": "no audio decoded by librosa"}
    tempo_value = None
    tempo_error = ""
    beats = []
    try:
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        tempo_value = float(np.ravel(tempo)[0]) if np.size(tempo) else None
    except Exception as exc:
        tempo_error = str(exc)
    else:
        tempo_error = ""
    try:
        try:
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        except Exception:
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    except Exception as exc:
        return {
            "available": False,
            "reason": f"librosa chroma analysis failed: {exc}",
            "librosa_tempo_bpm": round(tempo_value, 1) if tempo_value else None,
            "beat_count": int(len(beats)),
            "tempo_error": tempo_error,
        }
    mean_chroma = np.mean(chroma, axis=1)
    key = key_from_chroma(mean_chroma)
    chord_windows: list[dict[str, Any]] = []
    samples_per_window = max(1, int(window_seconds * sr))
    for start_sample in range(0, len(y), samples_per_window):
        end_sample = min(len(y), start_sample + samples_per_window)
        if end_sample - start_sample < sr:
            continue
        chunk = y[start_sample:end_sample]
        try:
            try:
                chunk_chroma = librosa.feature.chroma_cqt(y=chunk, sr=sr)
            except Exception:
                chunk_chroma = librosa.feature.chroma_stft(y=chunk, sr=sr)
        except Exception:
            continue
        chord, confidence = chord_from_chroma(np.mean(chunk_chroma, axis=1))
        chord_windows.append(
            {
                "start": format_seconds(start_sample / sr),
                "end": format_seconds(end_sample / sr),
                "chord_guess": chord,
                "confidence": confidence,
            }
        )
    return {
        "available": True,
        "librosa_tempo_bpm": round(tempo_value, 1) if tempo_value else None,
        "beat_count": int(len(beats)),
        "tempo_error": tempo_error,
        "key_guess": key,
        "chord_windows": merge_chord_windows(chord_windows[:24]),
    }


def merge_chord_windows(windows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for window in windows:
        if merged and merged[-1]["chord_guess"] == window["chord_guess"]:
            merged[-1]["end"] = window["end"]
            merged[-1]["confidence"] = round((merged[-1]["confidence"] + window["confidence"]) / 2, 3)
        else:
            merged.append(window.copy())
    return merged


def build_suno_traits(
    tempo: dict[str, Any],
    dynamics: dict[str, Any],
    sections: list[dict[str, Any]],
    tonal: dict[str, Any],
    onset_density: float,
) -> list[str]:
    traits: list[str] = []
    bpm = tempo.get("bpm")
    if bpm:
        alternates = tempo.get("alternate_feels") or []
        if alternates and alternates[0].get("feel") == "half-time feel":
            traits.append(f"{alternates[0]['bpm']} BPM half-time / {bpm} BPM double-time feel")
        elif alternates and alternates[0].get("feel") == "double-time feel":
            traits.append(f"{bpm} BPM base pulse / {alternates[0]['bpm']} BPM double-time feel")
        else:
            traits.append(f"{bpm} BPM {tempo_feel(bpm)}")
    key_guess = tonal.get("key_guess") if tonal.get("available") else None
    if isinstance(key_guess, dict) and key_guess.get("key") and key_guess.get("mode"):
        traits.append(f"{key_guess['key']} {key_guess['mode']} tonal center")
    traits.append(dynamics["dynamic_profile"])
    traits.append(dynamics["brightness"])
    if any("chorus/drop" in section["role_hint"] for section in sections):
        traits.append("clear chorus/drop energy lift")
    elif len({section["energy"] for section in sections}) >= 3:
        traits.append("noticeable section energy changes")
    else:
        traits.append("steady arrangement energy")
    if onset_density > 65:
        traits.append("busy rhythmic movement")
    elif onset_density > 30:
        traits.append("moderate groove activity")
    else:
        traits.append("sparse percussion or soft attack")
    return traits


def analyze(args: argparse.Namespace) -> dict[str, Any]:
    media_path = Path(args.media)
    if not media_path.exists():
        raise SystemExit(f"error: media file not found: {media_path}")
    pcm = run_ffmpeg_pcm(media_path, args.sample_rate, args.start, args.duration, args.max_duration)
    samples = decode_pcm_samples(pcm)
    if not samples:
        raise SystemExit("error: no audio samples decoded")
    duration_seconds = len(samples) / args.sample_rate
    frames = frame_features(samples, args.sample_rate, args.frame_seconds, args.hop_seconds)
    if not frames:
        raise SystemExit("error: audio is too short to analyze")
    envelope = onset_envelope(frames)
    tempo = estimate_tempo(envelope, args.hop_seconds, args.min_bpm, args.max_bpm)
    peaks = detect_onset_peaks(envelope, args.hop_seconds)
    onset_density = len(peaks) / max(0.001, duration_seconds / 60.0)
    rms_values = [frame["rms"] for frame in frames]
    zcr_values = [frame["zcr"] for frame in frames]
    sections = window_analysis(frames, envelope, args.window_seconds, duration_seconds)
    tonal = optional_librosa_analysis(
        media_path,
        args.sample_rate,
        args.start,
        args.duration,
        args.window_seconds,
        args.no_librosa,
    )
    dynamics = {
        "average_rms": round(mean(rms_values), 4),
        "peak_rms": round(max(rms_values), 4),
        "rms_p10": round(percentile(rms_values, 0.10), 4),
        "rms_p90": round(percentile(rms_values, 0.90), 4),
        "dynamic_profile": dynamic_label(rms_values),
        "average_zero_crossing_rate": round(mean(zcr_values), 4),
        "brightness": brightness_label(mean(zcr_values)),
        "onset_peaks_per_minute": round(onset_density, 1),
    }
    traits = build_suno_traits(tempo, dynamics, sections, tonal, onset_density)
    return {
        "path": str(media_path),
        "analysis_tier": "ffmpeg+librosa" if tonal.get("available") else "ffmpeg-only",
        "duration_analyzed_seconds": round(duration_seconds, 2),
        "sample_rate": args.sample_rate,
        "tempo": tempo,
        "dynamics": dynamics,
        "energy_sections": sections,
        "tonal_analysis": tonal,
        "suno_style_traits": traits,
        "suno_style_prompt_seed": ", ".join(traits),
        "caveats": [
            "Tempo, section, key, and chord estimates are creative guidance, not musicological proof.",
            (
                f"PCM is decoded in memory; default analysis is capped at {args.max_duration:g} seconds unless --duration or --max-duration changes it."
                if args.max_duration > 0
                else "PCM is decoded in memory; use --duration for very long files."
            ),
            "Chord and key guesses require optional librosa dependencies.",
            "Use the traits to describe a new song; do not copy melody, lyrics, or distinctive arrangement signatures.",
        ],
    }


def render_markdown(result: dict[str, Any]) -> str:
    tempo = result["tempo"]
    dynamics = result["dynamics"]
    tonal = result["tonal_analysis"]
    lines = [
        "# Deep Audio Analysis",
        "",
        f"- Path: {result['path']}",
        f"- Analysis tier: {result['analysis_tier']}",
        f"- Duration analyzed: {format_seconds(result['duration_analyzed_seconds'])}",
        f"- Sample rate: {result['sample_rate']} Hz",
        "",
        "## Tempo And Groove",
        f"- BPM estimate: {tempo.get('bpm') or 'unknown'} ({tempo.get('confidence', 'low')} confidence)",
    ]
    candidates = tempo.get("candidates") or []
    if candidates:
        lines.append("- Tempo candidates: " + ", ".join(str(item["bpm"]) for item in candidates))
    alternates = tempo.get("alternate_feels") or []
    if alternates:
        lines.append(
            "- Alternate feel: "
            + ", ".join(f"{item['bpm']} BPM {item['feel']}" for item in alternates)
        )
    lines.extend(
        [
            f"- Onset peaks per minute: {dynamics['onset_peaks_per_minute']}",
            f"- Groove feel: {tempo_feel(tempo.get('bpm'))}",
            "",
            "## Dynamics And Texture",
            f"- Dynamic profile: {dynamics['dynamic_profile']}",
            f"- Brightness proxy: {dynamics['brightness']}",
            f"- Average RMS: {dynamics['average_rms']}",
            f"- Peak RMS: {dynamics['peak_rms']}",
            "",
            "## Energy Sections",
        ]
    )
    for section in result["energy_sections"][:16]:
        lines.append(
            f"- {section['start']} - {section['end']}: {section['energy']}, {section['role_hint']}"
        )
    lines.extend(["", "## Tonal Analysis"])
    if tonal.get("available"):
        key = tonal.get("key_guess") or {}
        lines.append(
            f"- Key guess: {key.get('key') or 'unknown'} {key.get('mode') or ''} ({key.get('confidence', 'low')} confidence)"
        )
        if tonal.get("librosa_tempo_bpm"):
            lines.append(f"- Librosa tempo cross-check: {tonal['librosa_tempo_bpm']} BPM")
        chord_windows = tonal.get("chord_windows") or []
        if chord_windows:
            lines.append("- Rough chord windows:")
            for chord in chord_windows[:12]:
                lines.append(
                    f"  - {chord['start']} - {chord['end']}: {chord['chord_guess']} ({chord['confidence']})"
                )
    else:
        lines.append(f"- Not available: {tonal.get('reason', 'optional dependencies missing')}")
    lines.extend(
        [
            "",
            "## Suno Style Traits",
            *[f"- {trait}" for trait in result["suno_style_traits"]],
            "",
            "## Suno Style Prompt Seed",
            result["suno_style_prompt_seed"],
            "",
            "## Caveats",
            *[f"- {caveat}" for caveat in result["caveats"]],
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("media", help="Reference audio or video file")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    parser.add_argument("--out", help="Write output to a file")
    parser.add_argument("--start", type=time_value, help="Start time, e.g. 30 or 00:30")
    parser.add_argument("--duration", type=time_value, help="Analyze duration, e.g. 90 or 01:30")
    parser.add_argument(
        "--max-duration",
        type=float,
        default=600.0,
        help="Maximum seconds to decode when --duration is omitted; use 0 to analyze the full file",
    )
    parser.add_argument("--sample-rate", type=int, default=11025)
    parser.add_argument("--frame-seconds", type=float, default=0.10)
    parser.add_argument("--hop-seconds", type=float, default=0.05)
    parser.add_argument("--window-seconds", type=float, default=12.0)
    parser.add_argument("--min-bpm", type=int, default=55)
    parser.add_argument("--max-bpm", type=int, default=190)
    parser.add_argument("--no-librosa", action="store_true", help="Skip optional librosa key/chord analysis")
    args = parser.parse_args(argv)
    if args.sample_rate < 4000:
        parser.error("--sample-rate must be at least 4000")
    if args.frame_seconds <= 0 or args.hop_seconds <= 0 or args.window_seconds <= 0:
        parser.error("frame, hop, and window durations must be positive")
    if args.min_bpm <= 0 or args.max_bpm <= args.min_bpm:
        parser.error("BPM range is invalid")
    if args.max_duration < 0:
        parser.error("--max-duration must be 0 or greater")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = analyze(args)
    output = json.dumps(result, ensure_ascii=False, indent=2) if args.json else render_markdown(result)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        emit_text(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
