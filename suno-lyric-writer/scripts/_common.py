#!/usr/bin/env python3
"""Shared helpers for Suno Lyric Writer scripts."""

from __future__ import annotations

import argparse
import sys


def emit_text(text: str) -> None:
    data = (text + "\n").encode("utf-8")
    if hasattr(sys.stdout, "buffer"):
        sys.stdout.buffer.write(data)
    else:
        sys.stdout.write(text + "\n")


def parse_time_seconds(value: str | None) -> float | None:
    if not value:
        return None
    parts = value.split(":")
    try:
        if len(parts) == 1:
            return float(parts[0])
        if len(parts) == 2:
            minutes = int(parts[0])
            seconds = float(parts[1])
            if seconds >= 60:
                return None
            return minutes * 60 + seconds
        if len(parts) == 3:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            if minutes >= 60 or seconds >= 60:
                return None
            return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        return None
    return None


def time_value(value: str) -> str:
    parsed = parse_time_seconds(value)
    if parsed is None:
        raise argparse.ArgumentTypeError("must be seconds, MM:SS, or HH:MM:SS")
    if parsed < 0:
        raise argparse.ArgumentTypeError("must be 0 or greater")
    return value
