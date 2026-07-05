#!/usr/bin/env python3
# this_file: gimeltra/gimeltra.py
"""Abjad transliteration engine.

Scripts are named by their ISO 15924 code (``Hebr``, ``Arab``, ``Latn``, ...).
The rules live in ``gimeltra_data.json``, compiled from ``gimeltra.tsv`` by
``update.py``. Latin (``Latn``) is the pivot: any pair that lacks a direct
mapping is routed source -> Latin -> target.
"""

import json
import logging
from collections import Counter
from pathlib import Path
from typing import Optional

import regex as re
from fontTools import unicodedata as ucd

# Rule table: {source_script: {target_script: {source_char: target_char}}}.
ScriptTable = dict[str, dict[str, dict[str, str]]]
# Per-script rewrite passes: {script: {pattern: replacement}}.
RuleMap = dict[str, dict[str, str]]

cwd = Path(Path(__file__).parent)


class Transliterator:
    """Transliterate abjad text between supported scripts."""

    def __init__(self) -> None:
        with open(Path(cwd, "gimeltra_data.json"), encoding="utf-8") as f:
            data = json.load(f)
        self.db: ScriptTable = data["ssub"]  # source -> target substitutions
        self.db_ccmp: RuleMap = data["ccmp"]  # pre-decompose glyph clusters
        self.db_simplify: dict[str, str] = data["simp"]  # fold rare Latin variants
        self.db_fina: RuleMap = data["fina"]  # word-final contextual forms
        self.db_liga: RuleMap = data["liga"]  # post-conversion ligatures

    def auto_script(self, text: str) -> str:
        """Guess the source script as the most common ISO 15924 code in ``text``."""
        sc_count = Counter([ucd.script(c) for c in text])
        if not sc_count:  # empty input has no characters to vote on
            return "Zyyy"  # ISO 15924 "undetermined"
        sc = sc_count.most_common(1)[0][0]
        if not sc:
            sc = "Zyyy"
        return sc

    def _tr(self, text: str, sc: str, to_sc: str) -> str:
        t = text
        t = self._preprocess(t, sc)
        t = self._convert(t, sc, to_sc)
        t = self._postprocess(t, to_sc)
        return t

    def _preprocess(self, text: str, sc: str) -> str:
        """Normalise the source: apply ``ccmp`` clusters, then strip all marks.

        ``ccmp`` rewrites precomposed clusters into their base letters so the
        per-character converter can see them. NFD decomposition followed by
        dropping every combining mark (``\\p{M}``) is what makes the transform
        abjad-only: vowel points and diacritics are discarded, consonants stay.
        """
        t = text
        for rule_i, rule_o in self.db_ccmp.get(sc, {}).items():
            t = t.replace(rule_i, rule_o)
        t = ucd.normalize("NFD", t)
        t = re.sub(r"\p{M}", "", t)
        logging.debug(f"Pre: {list(t)}")
        return t

    def _postprocess(self, text: str, sc: str) -> str:
        """Apply target-script final forms (``fina``) and ligatures (``liga``).

        A ``fina`` rule swaps a letter for its word-final variant when it sits
        between a letter and a boundary (e.g. Hebrew mem -> final mem). ``liga``
        then joins character pairs the script writes as a single glyph.
        """
        t = text
        for rule_i, rule_o in self.db_fina.get(sc, {}).items():
            t = re.subf(rf"(\p{{L}})({rule_i})([^\p{{L}}])", f"{{1}}{rule_o}{{3}}", t)
            t = re.subf(rf"(\p{{L}})({rule_i})$", f"{{1}}{rule_o}", t)
        for rule_i, rule_o in self.db_liga.get(sc, {}).items():
            t = t.replace(rule_i, rule_o)
        logging.debug(f"Post: {list(t)}")
        return t

    def _convert(self, text: str, sc: str, to_sc: str) -> str:
        """Map each character, pivoting through Latin when no direct rule exists."""
        t = ""
        for c in text:
            # Prefer a direct source -> target rule when one is defined.
            c_dir = self.db.get(sc, {}).get(to_sc, {}).get(c, None)
            logging.debug(f"C:{c} D:{c_dir}")
            if c_dir:
                t += c_dir
                continue
            # Otherwise pivot: source -> Latin -> target.
            c_lat = self.db.get(sc, {}).get("Latn", {}).get(c, c)
            c_tgt = self.db.get("Latn", {}).get(to_sc, {}).get(c_lat, None)
            logging.debug(f"C:{c} L:{c_lat} T:{c_tgt}")

            if not c_tgt:
                # Fold a rare Latin transcription onto its base, then retry.
                c_lat = self.db_simplify.get(c_lat, c_lat)
                c_tgt = self.db.get("Latn", {}).get(to_sc, {}).get(c_lat, c)
            t += c_tgt
        logging.debug(f"Conv: {list(t)}")
        return t

    def tr(self, text: str, sc: Optional[str] = None, to_sc: str = "Latn") -> str:
        """Transliterate ``text`` from ``sc`` to ``to_sc``.

        ``sc`` defaults to auto-detection; ``to_sc`` defaults to Latin.
        """
        if not sc:
            sc = self.auto_script(text)
        logging.debug(
            {
                "script": sc,
                "to_script": to_sc,
            }
        )
        logging.debug(f"Text: {list(text)}")
        res = self._tr(text, sc, to_sc)
        return res


def tr(text: str, sc: Optional[str] = None, to_sc: str = "Latn") -> str:
    """One-shot helper: transliterate ``text`` without keeping an instance around."""
    tr = Transliterator()
    return tr.tr(text, sc, to_sc)
