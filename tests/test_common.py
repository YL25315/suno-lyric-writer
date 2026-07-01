from __future__ import annotations

import argparse

import pytest
from conftest import load_script_module


def test_common_time_value_accepts_supported_forms():
    module = load_script_module("_common")

    assert module.time_value("30") == "30"
    assert module.time_value("01:30") == "01:30"
    assert module.time_value("01:02:03") == "01:02:03"


def test_common_time_value_rejects_bad_or_negative_values():
    module = load_script_module("_common")

    with pytest.raises(argparse.ArgumentTypeError):
        module.time_value("-1")
    with pytest.raises(argparse.ArgumentTypeError):
        module.time_value("01:75")
