#!/usr/bin/env python3
"""gimeltra — Transliteration between Semitic and other writing systems.

Provides the Transliterator class and convenience tr() function for
converting text between scripts (Hebrew, Arabic, Syriac, Phoenician,
Ugaritic, etc.) using OpenType-style feature mappings.
"""

import json
import logging
from collections import Counter
from pathlib import Path

import regex as re
from fontTools import unicodedata as ucd

# Directory containing the mapping data file
_DATA_DIR = Path(Path(__file__).parent)

# Fallback script code for undetermined scripts (per ISO 15924)
_UNKNOWN_SCRIPT = "Zyyy"


class Transliterator:
    """Transliterate text between writing systems using OpenType feature tables.

    The transliteration pipeline has three stages:
      1. Normalize input — apply composition rules, strip diacritics
      2. Convert characters — direct mapping or Latin-pivot mapping
      3. Apply final forms and ligatures — context-sensitive replacements
    """

    def __init__(self):
        """Load transliteration data from the JSON mapping file."""
        self._direct_map = None
        self._composition_rules = None
        self._simplification_rules = None
        self._final_form_rules = None
        self._ligature_rules = None
        self._load_data()

    def _load_data(self):
        """Parse the gimeltra_data.json file into structured lookup tables."""
        data_path = Path(_DATA_DIR, "gimeltra_data.json")
        with open(data_path, encoding="utf-8") as f:
            data = json.load(f)
        self._direct_map = data["ssub"]
        self._composition_rules = data["ccmp"]
        self._simplification_rules = data["simp"]
        self._final_form_rules = data["fina"]
        self._ligature_rules = data["liga"]

    def auto_script(self, text):
        """Detect the dominant script of the input text.

        Returns the ISO 15924 script code for the most common script
        found in the text. Falls back to 'Zyyy' (Unknown) if no
        script can be determined.

        Args:
            text: The input string to analyze.

        Returns:
            A four-letter ISO 15924 script code (e.g., 'Hebr', 'Arab').
        """
        script_counts = Counter([ucd.script(char) for char in text])
        dominant_script = script_counts.most_common(1)[0][0]
        return dominant_script if dominant_script else _UNKNOWN_SCRIPT

    def _transliterate_pipeline(self, text, source_script, target_script):
        """Execute the three-stage transliteration pipeline.

        Args:
            text: Input text string.
            source_script: ISO 15924 code of the input script.
            target_script: ISO 15924 code of the output script.

        Returns:
            Transliterated text string.
        """
        normalized = self._normalize_input(text, source_script)
        converted = self._convert_characters(normalized, source_script, target_script)
        finalized = self._apply_final_forms_and_ligatures(converted, target_script)
        return finalized

    def _normalize_input(self, text, source_script):
        """Pre-process input text before character conversion.

        Applies composition rules (ccmp) for the source script, then
        performs Unicode NFD normalization and strips all combining marks
        (diacritics) to produce a clean base-character string.

        Args:
            text: Raw input text.
            source_script: ISO 15924 code of the input script.

        Returns:
            Normalized text with diacritics removed.
        """
        result = text
        # Apply script-specific composition rules (e.g., combine characters)
        for rule_input, rule_output in self._composition_rules.get(source_script, {}).items():
            result = result.replace(rule_input, rule_output)
        # Decompose and strip combining marks
        result = ucd.normalize("NFD", result)
        result = re.sub(r"\p{M}", "", result)
        logging.debug(f"Pre: {list(result)}")
        return result

    def _apply_final_forms_and_ligatures(self, text, target_script):
        """Post-process output text after character conversion.

        Applies context-sensitive final form replacements and ligature
        substitutions for the target script.

        Args:
            text: Converted text from the character mapping stage.
            target_script: ISO 15924 code of the output script.

        Returns:
            Text with final forms and ligatures applied.
        """
        result = text
        # Apply final form rules — context-sensitive: only at word-end positions
        for pattern, replacement in self._final_form_rules.get(target_script, {}).items():
            # Replace when character is preceded by a letter and followed by non-letter
            result = re.subf(
                rf"(\p{{L}})({pattern})([^\p{{L}}])",
                f"{{1}}{replacement}{{3}}",
                result,
            )
            # Also replace at end of string
            result = re.subf(
                rf"(\p{{L}})({pattern})$",
                f"{{1}}{replacement}",
                result,
            )
        # Apply ligature rules — simple string replacements
        for ligature_input, ligature_output in self._ligature_rules.get(target_script, {}).items():
            result = result.replace(ligature_input, ligature_output)
        logging.debug(f"Post: {list(result)}")
        return result

    def _convert_characters(self, text, source_script, target_script):
        """Convert each character from source to target script.

        Uses a three-step lookup for each character:
          1. Direct mapping: source_script → target_script
          2. Latin pivot: source_script → Latin → target_script
          3. Simplification fallback: strip diacritics, retry Latin pivot

        Args:
            text: Normalized input text (diacritics already stripped).
            source_script: ISO 15924 code of the input script.
            target_script: ISO 15924 code of the output script.

        Returns:
            Text with each character converted to the target script.
        """
        result = ""
        for char in text:
            # Step 1: Try direct mapping (source → target)
            direct_mapping = (
                self._direct_map.get(source_script, {})
                .get(target_script, {})
                .get(char, None)
            )
            logging.debug(f"C:{char} D:{direct_mapping}")
            if direct_mapping:
                result += direct_mapping
                continue

            # Step 2: Try Latin pivot (source → Latin → target)
            latin_equivalent = (
                self._direct_map.get(source_script, {})
                .get("Latn", {})
                .get(char, char)
            )
            target_char = (
                self._direct_map.get("Latn", {})
                .get(target_script, {})
                .get(latin_equivalent, None)
            )
            logging.debug(f"C:{char} L:{latin_equivalent} T:{target_char}")

            # Step 3: Simplification fallback — strip diacritics from Latin form
            if not target_char:
                simplified_latin = self._simplification_rules.get(latin_equivalent, latin_equivalent)
                target_char = (
                    self._direct_map.get("Latn", {})
                    .get(target_script, {})
                    .get(simplified_latin, char)
                )
            result += target_char

        logging.debug(f"Conv: {list(result)}")
        return result

    def tr(self, text, sc=None, to_sc="Latn"):
        """Transliterate text between scripts.

        Args:
            text: Input text to transliterate.
            sc: Source script as ISO 15924 code. If None, auto-detected.
            to_sc: Target script as ISO 15924 code. Defaults to 'Latn'.

        Returns:
            Transliterated text string.
        """
        if not sc:
            sc = self.auto_script(text)
        logging.debug({"script": sc, "to_script": to_sc})
        logging.debug(f"Text: {list(text)}")
        return self._transliterate_pipeline(text, sc, to_sc)


def tr(text, sc=None, to_sc="Latn"):
    """Convenience function: transliterate text between scripts.

    Creates a new Transliterator instance and performs a single
    transliteration. For repeated calls, instantiate Transliterator
    directly to avoid reloading the data file each time.

    Args:
        text: Input text to transliterate.
        sc: Source script as ISO 15924 code. If None, auto-detected.
        to_sc: Target script as ISO 15924 code. Defaults to 'Latn'.

    Returns:
        Transliterated text string.
    """
    transliterator = Transliterator()
    return transliterator.tr(text, sc, to_sc)
