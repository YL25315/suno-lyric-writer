#!/usr/bin/env python3
"""Build a copy-paste Suno Custom Mode prompt package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _common import decode_text_bytes, emit_text


def percent(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer from 0 to 100") from exc
    if parsed < 0 or parsed > 100:
        raise argparse.ArgumentTypeError("must be from 0 to 100")
    return parsed


def read_lyrics(path_text: str | None) -> str:
    if not path_text:
        if sys.stdin.isatty():
            return ""
        return decode_text_bytes(sys.stdin.buffer.read()).strip()
    if path_text == "-":
        return decode_text_bytes(sys.stdin.buffer.read()).strip()
    return Path(path_text).read_text(encoding="utf-8").strip()


def build_package(args: argparse.Namespace, lyrics: str) -> dict[str, object]:
    return {
        "title": args.title.strip(),
        "style_of_music": args.style.strip(),
        "lyrics": lyrics,
        "exclude_styles": args.exclude.strip(),
        "reference_analysis": args.reference_analysis.strip(),
        "creative_direction": args.creative_direction.strip(),
        "parameters": {
            "model": args.model,
            "weirdness": args.weirdness,
            "style_influence": args.style_influence,
            "audio_influence": args.audio_influence,
            "vocal": args.vocal,
            "persona": args.persona,
        },
        "production_tips": args.tip,
        "feedback_questions": args.feedback_question,
        "iteration_notes": args.notes.strip(),
    }


def count_words(text: str) -> int:
    return len([part for part in text.replace("\n", " ").split(" ") if part.strip()])


def count_non_cjk_words(text: str) -> int:
    without_cjk = re.sub(r"[\u4e00-\u9fff]+", " ", text)
    return len([part for part in re.split(r"\s+", without_cjk) if part.strip()])


def count_cjk_chars(text: str) -> int:
    return sum(1 for char in text if "\u4e00" <= char <= "\u9fff")


def visible_len(text: str) -> int:
    return len(text.strip())


def lyric_line_checks(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ["Lyric lines: 0"]
    longest_line = max(visible_len(line) for line in lines)
    checks = [f"Lyric lines: {len(lines)}", f"Longest visible line: {longest_line} characters"]
    cjk_lines = [line for line in lines if count_cjk_chars(line)]
    if cjk_lines:
        longest_cjk = max(count_cjk_chars(line) for line in cjk_lines)
        long_cjk_lines = sum(1 for line in cjk_lines if count_cjk_chars(line) > 18)
        checks.extend(
            [
                f"Lyrics CJK characters: {count_cjk_chars(text)}",
                f"Longest CJK line: {longest_cjk} characters",
                f"CJK lines over 18 chars: {long_cjk_lines}",
            ]
        )
    return checks


def field_checks(package: dict[str, object]) -> list[str]:
    style = str(package["style_of_music"])
    lyrics = str(package["lyrics"])
    exclude = str(package["exclude_styles"])
    cjk_count = count_cjk_chars(lyrics)
    checks = [
        f"Style characters: {len(style)}",
        f"Lyrics characters: {len(lyrics)}",
        (
            f"Lyrics non-CJK words: {count_non_cjk_words(lyrics)}"
            if cjk_count
            else f"Lyrics words: {count_words(lyrics)}"
        ),
        *lyric_line_checks(lyrics),
    ]
    if exclude:
        exclude_count = len([item for item in exclude.split(",") if item.strip()])
        checks.append(f"Exclude items: {exclude_count}")
    else:
        checks.append("Exclude items: 0")
    return checks


def render_markdown(package: dict[str, object]) -> str:
    params = package["parameters"]
    if not isinstance(params, dict):
        raise TypeError("package['parameters'] must be a dict")
    tips = package["production_tips"]
    if not isinstance(tips, list):
        raise TypeError("package['production_tips'] must be a list")
    lines = [f"# {package['title']}", ""]
    if package["reference_analysis"]:
        lines.extend(["## Reference Analysis", str(package["reference_analysis"]), ""])
    if package["creative_direction"]:
        lines.extend(["## Creative Direction", str(package["creative_direction"]), ""])
    lines.extend(
        [
            "## Suno Custom Mode",
            "",
            "### Title",
            str(package["title"]),
            "",
            "### Style of Music",
            str(package["style_of_music"]),
            "",
            "### Lyrics",
            str(package["lyrics"]),
            "",
            "### Exclude Styles",
            str(package["exclude_styles"] or "None"),
            "",
            "### Parameters",
            f"- Model: {params.get('model') or 'Newest stable available'}",
            f"- Weirdness: {params.get('weirdness')}%",
            f"- Style Influence: {params.get('style_influence')}%",
            f"- Audio Influence: {params.get('audio_influence') if params.get('audio_influence') is not None else 'N/A'}",
            f"- Vocal: {params.get('vocal') or 'Unspecified'}",
            f"- Persona: {params.get('persona') or 'None'}",
            "",
            "### Field Checks",
            *[f"- {check}" for check in field_checks(package)],
            "",
            "### Production Tips",
            *(
                [f"- {tip}" for tip in tips]
                if tips
                else [
                    "- Generate 2-4 takes before changing the prompt.",
                    "- Change one variable at a time when iterating.",
                ]
            ),
            "",
            "### Iteration Notes",
            str(package["iteration_notes"] or "Generate two takes, keep the stronger melody/chorus, then revise any rushed lines."),
            "",
        ]
    )
    feedback_questions = package["feedback_questions"]
    if not isinstance(feedback_questions, list):
        raise TypeError("package['feedback_questions'] must be a list")
    if feedback_questions:
        lines.extend(["### Next Feedback Questions", *[f"- {question}" for question in feedback_questions], ""])
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--style", required=True, help="Suno Style of Music text")
    parser.add_argument("--lyrics-file", help="Path to lyrics text file, or '-' for stdin")
    parser.add_argument("--exclude", default="")
    parser.add_argument("--reference-analysis", default="")
    parser.add_argument("--creative-direction", default="")
    parser.add_argument("--model", default="Newest stable available")
    parser.add_argument("--weirdness", type=percent, default=45)
    parser.add_argument("--style-influence", type=percent, default=70)
    parser.add_argument("--audio-influence", type=percent)
    parser.add_argument("--vocal", default="")
    parser.add_argument("--persona", default="")
    parser.add_argument("--tip", action="append", default=[], help="Production tip; repeat for multiple tips")
    parser.add_argument("--feedback-question", action="append", default=[], help="Question for the next user feedback pass")
    parser.add_argument("--notes", default="")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    parser.add_argument("--out", help="Write output to this file")
    args = parser.parse_args(argv)
    if not args.title.strip():
        parser.error("--title cannot be empty")
    if not args.style.strip():
        parser.error("--style cannot be empty")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    lyrics = read_lyrics(args.lyrics_file)
    if not lyrics:
        print("error: provide lyrics via --lyrics-file or stdin", file=sys.stderr)
        return 2
    package = build_package(args, lyrics)
    output = (
        json.dumps(package, ensure_ascii=False, indent=2)
        if args.json
        else render_markdown(package)
    )
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        emit_text(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
