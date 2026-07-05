#!/usr/bin/env python3
# this_file: tests/test_gimeltra.py
"""Tests for the Gimeltra transliteration engine."""

import subprocess
import sys

import pytest
from fontTools import unicodedata as ucd

import gimeltra
from gimeltra import Transliterator, tr


def _nfkc(s: str) -> str:
    # Fold presentation-form ligatures (e.g. bet+dagesh U+FB31) to base + mark.
    return ucd.normalize("NFKC", s)


@pytest.fixture(scope="module")
def t() -> Transliterator:
    return Transliterator()


def test_smoke_import() -> None:
    assert gimeltra.__version__
    assert callable(tr)


def test_supported_scripts_present(t: Transliterator) -> None:
    scripts = set(t.db.keys())
    # A representative sample of the 24+ supported scripts must load.
    for sc in ("Latn", "Hebr", "Arab", "Phnx", "Syrc", "Sogd"):
        assert sc in scripts
    assert len(scripts) >= 24


@pytest.mark.parametrize(
    "text, to_sc, expected",
    [
        ("שלום", "Latn", "šlwm"),  # Hebrew -> Latin
        ("bytk", "Hebr", "בּיתך"),  # Latin -> Hebrew (bet+dagesh ligature, final kaf)
        ("bytk", "Arab", "بيتك"),  # Latin -> Arabic
        ("bytk", "Phnx", "𐤁𐤉𐤕𐤊"),  # Latin -> Phoenician
    ],
)
def test_known_conversions(
    t: Transliterator, text: str, to_sc: str, expected: str
) -> None:
    sc = "Latn" if to_sc != "Latn" else "Hebr"
    assert _nfkc(t.tr(text, sc=sc, to_sc=to_sc)) == _nfkc(expected)


def test_latin_pivot_round_trip(t: Transliterator) -> None:
    # Latin -> script -> Latin recovers the abjad skeleton for scripts without a
    # begadkefat-style plosive/fricative split. (Hebrew folds b/v onto one letter,
    # so it is deliberately excluded; see test_hebrew_is_a_fixed_point.)
    skeleton = "bytk"
    for sc in ("Arab", "Phnx", "Syrc", "Sogd"):
        forward = t.tr(skeleton, sc="Latn", to_sc=sc)
        back = t.tr(forward, sc=sc, to_sc="Latn")
        assert back == skeleton, f"{sc}: {skeleton!r} -> {forward!r} -> {back!r}"


def test_hebrew_is_a_fixed_point(t: Transliterator) -> None:
    # Hebrew loses the b/v distinction, so round-tripping is not the identity, but
    # a second pass must be stable: once romanised, converting back and forth again
    # reproduces the same Hebrew.
    forward = t.tr("šlm", sc="Latn", to_sc="Hebr")
    back = t.tr(forward, sc="Hebr", to_sc="Latn")
    forward2 = t.tr(back, sc="Latn", to_sc="Hebr")
    assert forward2 == forward


def test_auto_script_detection(t: Transliterator) -> None:
    assert t.auto_script("שלום") == "Hebr"
    assert t.auto_script("بيت") == "Arab"


def test_auto_script_defaults_when_no_letters(t: Transliterator) -> None:
    assert t.auto_script("") == "Zyyy"
    assert t.auto_script("123 ...") == "Zyyy"


def test_tr_uses_auto_detection(t: Transliterator) -> None:
    # No source script given: it should detect Hebrew and romanise.
    assert t.tr("שלום") == "šlwm"


def test_empty_string(t: Transliterator) -> None:
    assert t.tr("", sc="Hebr", to_sc="Latn") == ""


def test_vowel_marks_are_dropped(t: Transliterator) -> None:
    # Pointed Hebrew (with niqqud) folds to the same abjad skeleton as unpointed.
    pointed = "בַּיִת"
    plain = "בית"
    assert t.tr(pointed, sc="Hebr", to_sc="Latn") == t.tr(
        plain, sc="Hebr", to_sc="Latn"
    )


def test_module_level_tr_helper() -> None:
    assert tr("שלום", sc="Hebr", to_sc="Latn") == "šlwm"


def _run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "gimeltra", *args],
        capture_output=True,
        text=True,
    )


def test_cli_text_conversion() -> None:
    res = _run_cli("-t", "שלום", "-s", "Hebr", "-o", "Latn")
    assert res.returncode == 0
    assert res.stdout.strip() == "šlwm"


def test_cli_stats() -> None:
    res = _run_cli("--stats")
    assert res.returncode == 0
    assert "scripts:" in res.stdout


def test_cli_version() -> None:
    res = _run_cli("-V")
    assert res.returncode == 0
    assert gimeltra.__version__ in res.stdout
