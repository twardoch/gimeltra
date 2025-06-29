# Gimeltra: A Versatile Transliteration Tool

Gimeltra is a powerful and straightforward Python 3.9+ command-line tool and library designed for transliterating text between a variety of writing systems. While it supports over 20 scripts, it specializes in those of Semitic origin, offering a simplified, abjad-only transliteration. This means it primarily focuses on consonants, making it particularly useful for tasks like converting modern texts into ancient scripts or for linguistic analysis where vocalization is not critical.

## Who is Gimeltra For?

Gimeltra is aimed at:

*   **Linguists and Researchers:** Studying Semitic languages or historical scripts.
*   **Students:** Learning ancient languages and needing to see textual representations across different scripts.
*   **Developers:** Requiring programmatic transliteration capabilities within their Python applications.
*   **Hobbyists:** Exploring the fascinating world of writing systems.

If you need a quick, scriptable method to convert text between supported scripts without the overhead of complex linguistic models or full phonetic accuracy, Gimeltra is an excellent choice.

## Why Use Gimeltra?

*   **Ease of Use:** Simple command-line interface and Python API.
*   **Speed:** Performs transliteration quickly, suitable for batch processing.
*   **Flexibility:** Supports a wide range of scripts, with a focus on Semitic systems.
*   **Customizable:** Transliteration rules are defined in a human-readable TSV file, allowing for modifications and extensions.
*   **Automatic Script Detection:** Can often infer the input script, simplifying usage.
*   **Transparent Process:** The transliteration steps are logical and can be understood by users.

## Installation

### Prerequisites

*   Python 3.9 or higher.

### Command

You can install Gimeltra directly from its GitHub repository using pip:

```sh
python3 -m pip install --upgrade git+https://github.com/twardoch/gimeltra
```

This will also install its necessary dependencies: `fonttools`, `langcodes`, `yaplon`, and `regex`.

## How to Use Gimeltra

Gimeltra can be used both as a command-line tool (`gimeltrapy`) and as a Python library.

### Command-Line Interface (CLI)

The primary command is `gimeltrapy`.

**Basic Syntax:**

```sh
gimeltrapy [options]
```

**Input Methods:**

1.  **Direct Text Input:** Use the `-t` or `--text` option:
    ```sh
    gimeltrapy -t "لرموز"
    ```
    Output: `lrmwz`

2.  **File Input:** Use the `-i` or `--input` option with a file path:
    ```sh
    gimeltrapy -i my_arabic_text.txt -o Hebr
    ```

3.  **Standard Input (Piping):** Pipe text directly to the command:
    ```sh
    echo "لرموز" | gimeltrapy -o Grek
    ```
    Output: `λρμυζ`

**Specifying Scripts:**

*   `-s <SCRIPT_CODE>` or `--script <SCRIPT_CODE>`: Specify the ISO 15924 code for the input script (e.g., `Arab`, `Hebr`). If omitted, Gimeltra will attempt to auto-detect the script.
*   `-o <SCRIPT_CODE>` or `--to-script <SCRIPT_CODE>`: Specify the ISO 15924 code for the output script. Defaults to `Latn` (Latin) if not provided.

**Examples:**

*   Transliterate Arabic text to Latin (default output script):
    ```sh
    gimeltrapy -t "لرموز"
    # Output: lrmwz
    ```
*   Transliterate Arabic to Hebrew:
    ```sh
    gimeltrapy -t "لرموز" -s Arab -o Hebr
    # Output: לרמוז
    ```
*   Transliterate Arabic to Old North Arabian (Narb):
    ```sh
    gimeltrapy -t "لرموز" -o Narb
    # Output: 𐪁𐪇𐪃𐪅𐪘
    ```
*   Transliterate Arabic to Old Sogdian (Sogo):
    ```sh
    gimeltrapy -t "لرموز" -o Sogo
    # Output: 𐼌𐼘𐼍𐼇𐼈
    ```

**Listing Supported Scripts:**

To see all supported script codes:

```sh
gimeltrapy --stats
```

**Other Options:**

*   `-h, --help`: Show the help message and exit.
*   `-v, --verbose`: Increase output verbosity (e.g., `-vv` for debug).
*   `-V, --version`: Show program version and exit.

### Python Library Usage

Gimeltra can be integrated into your Python projects.

**1. Efficient Method (Recommended):**

Instantiate the `Transliterator` class for multiple operations or when performance is key.

```python
from gimeltra.gimeltra import Transliterator

# Initialize the transliterator once
tr = Transliterator()

# Perform transliterations
hebrew_text = tr.tr("لرموز", sc='Arab', to_sc='Hebr')
print(f"Arabic to Hebrew: {hebrew_text}") # Output: לרמוז

latin_text = tr.tr("שלום", sc='Hebr', to_sc='Latn')
print(f"Hebrew to Latin: {latin_text}") # Output: šlwm

# Auto-detect source script
phoenician_text = tr.tr("𐤀𐤁𐤂", to_sc='Latn') # Assuming Phnx is correctly detected
print(f"Phoenician to Latin (auto-detected): {phoenician_text}") # Output: ʾbg
```

**2. Simpler Method:**

For one-off transliterations, a simpler function is available. This method re-initializes the transliterator on each call, so it's less efficient for multiple uses.

```python
from gimeltra import tr

# Transliterate Arabic to Latin (default target)
latin_text = tr("لرموز")
print(latin_text) # Output: lrmwz

# Transliterate Hebrew to Greek, specifying source script
greek_text = tr("שלום", sc="Hebr", to_sc="Grek")
print(greek_text) # Output: σλωμ
```

---

## Technical Deep Dive

This section delves into the internal workings of Gimeltra, its data structures, and guidelines for contribution.

### How Gimeltra Works: Core Architecture

Gimeltra's transliteration logic is primarily encapsulated in the `gimeltra.gimeltra.Transliterator` class. This class loads its transliteration rules and data from a pre-processed JSON file named `gimeltra_data.json`, which is located in the `gimeltra` package directory.

**Key Components:**

*   **`gimeltra_data.json`:** This is the engine's fuel. It contains several key dictionaries:
    *   `ssub` (Script SUBstitution): The main character-to-character mapping rules, structured as `source_script -> target_script -> {character_map}`.
    *   `ccmp` (Composite Character MaP): Rules for decomposing characters or handling multi-character sequences during preprocessing (e.g., splitting specific ligatures before main processing).
    *   `simp` (SIMPlify): Fallback rules, primarily for simplifying Latin characters when a direct transliteration isn't available.
    *   `fina` (FINAl forms): Rules for converting characters to their final positional forms (e.g., Arabic, Hebrew) during postprocessing.
    *   `liga` (LIGAatures): Rules for forming ligatures from sequences of characters during postprocessing.
*   **`Transliterator` Class:**
    *   Loads `gimeltra_data.json` upon initialization.
    *   Provides the main `tr()` method for performing transliteration.
    *   Includes helper methods for script auto-detection, preprocessing, character conversion, and postprocessing.
*   **Script Auto-Detection (`auto_script` method):** If the source script is not provided, Gimeltra attempts to identify it by analyzing the Unicode script property of each character in the input text (using `fontTools.unicodedata.script`). The most frequently occurring script is chosen.

### The Transliteration Process

When `tr(text, sc, to_sc)` is called, the following steps occur:

1.  **Script Detection (if `sc` is `None`):**
    *   The `auto_script(text)` method is invoked to determine the source script.

2.  **Preprocessing (`_preprocess` method):**
    *   The input `text` is first processed using script-specific rules from the `ccmp` table (e.g., to break down complex ligatures like Arabic "Allah" into constituent letters).
    *   The text is then normalized to Unicode Normalization Form D (NFD) using `fontTools.unicodedata.normalize("NFD", text)`. This decomposes characters into their base forms and combining diacritics.
    *   All diacritical marks (Unicode category `Mark`, `\p{M}`) are removed using `regex.sub(r"\p{M}", "", text)`. This ensures an abjad-focused transliteration.

3.  **Character Conversion (`_convert` method):**
    *   The preprocessed text is iterated character by character.
    *   For each character, Gimeltra attempts to find a transliteration rule in the following order of preference:
        1.  **Direct Mapping:** Check `db[source_script][target_script][character]`.
        2.  **Via Latin (Primary Intermediary):**
            a.  Convert source character to Latin: `latin_char = db[source_script]['Latn'][character]`. If no specific rule, the original character is used as `latin_char`.
            b.  Convert `latin_char` to target script: `db['Latn'][target_script][latin_char]`.
        3.  **Via Simplified Latin (Fallback):** If the previous step yields no result:
            a.  Simplify `latin_char`: `simplified_latin_char = db_simplify.get(latin_char, latin_char)`.
            b.  Convert `simplified_latin_char` to target script: `db['Latn'][target_script][simplified_latin_char]`.
    *   If a character cannot be converted through any of these paths, it is passed through to the output string unchanged.

4.  **Postprocessing (`_postprocess` method):**
    *   **Final Forms:** Contextual rules for final character forms are applied using the `fina` table. For example, a Hebrew Kaph at the end of a word might be converted to Final Kaph. This uses regular expressions to identify characters at word endings.
    *   **Ligatures:** Sequences of characters are replaced by their corresponding ligatures based on rules in the `liga` table.

### Data Files: The Heart of Transliteration

*   **`gimeltra.tsv`:** This Tab-Separated Values file is the human-editable source for all transliteration rules. It resides in the `gimeltra/` directory. You can open and modify this file with spreadsheet software or a text editor that handles TSV well.
*   **`gimeltra_data.json`:** This JSON file is automatically generated from `gimeltra.tsv` by the `gimeltra/update.py` script. It's the actual data file that the `Transliterator` class uses at runtime. It's structured for efficient lookups.
*   **`gimeltra/update.py`:** A Python script responsible for parsing `gimeltra.tsv` and creating/updating `gimeltra_data.json`. It uses the `yaplon` library for ordered JSON output. If you modify `gimeltra.tsv`, you **must** run this script to see your changes reflected in the tool's behavior:
    ```sh
    python gimeltra/update.py
    ```

**Conventions in `gimeltra.tsv`:**

The `gimeltra.tsv` file uses special prefixes within its cells to define rule behaviors:

*   `|`: Separates alternative versions of a character (e.g., `α|Α` for Greek Alpha).
*   `<`: Prefixes a character variant that should only be used when converting *from* this script to Latin (source-only variant for this script's column).
*   `>`: Prefixes a character variant that should only be used when converting *to* this script from Latin (target-only variant for this script's column).
*   `~`: Prefixes a character that represents a final form (e.g., `~ך` for Hebrew Final Kaf).
*   `%`: Separates the "from" (source sequence) and "to" (target ligature) strings for a ligature rule (e.g., `FF%ﬀ` to create the 'ff' ligature).

The `Latn` column in `gimeltra.tsv` acts as the primary pivot for transliterations. The `<Latn` column provides simplified Latin fallbacks for broader, though potentially lossier, compatibility.

### Supported Scripts

Gimeltra supports transliteration for the following scripts (identified by their ISO 15924 codes). You can get an up-to-date list by running `gimeltrapy --stats`:

*   `Latn` (Latin)
*   `Arab` (Arabic)
*   `Ethi` (Ethiopic)
*   `Armi` (Imperial Aramaic)
*   `Brah` (Brahmi)
*   `Chrs` (Chorasmian)
*   `Egyp` (Egyptian hieroglyphs)
*   `Elym` (Elymaic)
*   `Grek` (Greek)
*   `Hatr` (Hatran)
*   `Hebr` (Hebrew)
*   `Mani` (Manichaean)
*   `Narb` (Old North Arabian)
*   `Nbat` (Nabataean)
*   `Palm` (Palmyrene)
*   `Phli` (Inscriptional Pahlavi)
*   `Phlp` (Psalter Pahlavi)
*   `Phnx` (Phoenician)
*   `Prti` (Inscriptional Parthian)
*   `Samr` (Samaritan)
*   `Sarb` (Old South Arabian)
*   `Sogd` (Sogdian)
*   `Sogo` (Old Sogdian)
*   `Syrc` (Syriac)
*   `Ugar` (Ugaritic)

*(This list is based on the initial README and should be verified with `gimeltrapy --stats` for the most current version).*

### Coding Standards and Contributions

*   **Coding Style:** Adhere to PEP 8 Python coding standards.
*   **Dependencies:** Key dependencies are `fonttools[unicode]`, `langcodes[data]`, `yaplon`, and `regex`. These are managed in `requirements.txt` and `setup.py`.
*   **Modifying Transliteration Rules:**
    1.  Edit the `gimeltra/gimeltra.tsv` file with your changes or additions.
    2.  Run the update script: `python gimeltra/update.py` to regenerate `gimeltra_data.json`.
    3.  Test your changes thoroughly using both CLI and programmatic examples.
*   **Submitting Changes:**
    *   Fork the repository on GitHub.
    *   Create a new branch for your feature or bug fix.
    *   Make your changes, including updating `gimeltra.tsv` and running `update.py` if applicable.
    *   Commit your changes with clear, descriptive messages.
    *   Push your branch to your fork.
    *   Open a Pull Request against the main Gimeltra repository.
    *   While no formal test suite was noted in the initial exploration, ensure your changes don't break existing functionality and, if possible, provide examples demonstrating your changes.

## License

Gimeltra is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
Copyright © 2021 Adam Twardoch.

## Other Projects of Interest

*   [Wiktra](https://github.com/kbatsuren/wiktra): Python transliterator for 100+ scripts and 500+ languages, using Wiktionary Lua modules.
*   [Aksharamukha](https://github.com/virtualvinodh/aksharamukha-python): Python transliterator for Indic scripts (94 scripts, 8 romanization methods).
