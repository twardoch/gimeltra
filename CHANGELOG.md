<!-- this_file: CHANGELOG.md -->

# Changelog

## Unreleased — Modernization (2026-07-05)

### Build & packaging
- Migrated from `setup.py` to `pyproject.toml` with Hatchling + `hatch-vcs`
  (version now derived from git tags). Removed `setup.py`, `requirements.txt`,
  `MANIFEST.in`.
- Declared runtime dependencies as `fonttools[unicode]` and `regex` only.
  Dropped the unused `langcodes`; moved `yaplon` to an optional `[update]`
  extra used solely by `update.py`. Added `[dev]` extra.
- Corrected the license metadata to MIT (was `GPLv2` in `setup.py`, though the
  LICENSE file and README were already MIT).
- Added `build.sh` and `publish.sh`.
- Wheel ships the ruleset, TSV, and `update.py`; excludes the bulky `.numbers`
  spreadsheet.

### Code
- Added type hints across `gimeltra.py`, `__main__.py`, and the public API.
- Added explanatory comments for the abjad reduction and the Latin-pivot
  conversion, plus the `ccmp`/`fina`/`liga`/`simp` rule passes.
- **Fixed:** `auto_script("")` raised `IndexError` on empty input; it now
  returns `Zyyy` (undetermined).
- **Fixed:** `main()` passed arguments to a zero-arg `cli()`; signatures aligned.
- Version is now resolved via `importlib.metadata` instead of a hard-coded
  string.

### Tests & CI
- Added `tests/test_gimeltra.py`: known conversions, Latin-pivot round-trips,
  auto-detection, vowel-drop, empty input, and CLI smoke tests (17 tests).
- Added GitHub Actions `ci.yml` (ruff + mypy + pytest on Python 3.9–3.13) and
  `release.yml` (build + GitHub release + PyPI trusted publishing on tags).
- Configured ruff and mypy in `pyproject.toml`; both pass clean.

### Docs
- Rewrote `README.md` (trimmed, Quick Start first) and added a Just-the-Docs
  Jekyll site under `docs/` (home, supported-scripts table, TSV rule format).
- Added `CLAUDE.md` with source-file map and architecture notes.
- Added a monochrome line-art project icon at `docs/assets/icon.png`.

## Version 1.0.0 (2021-08-11)

### Initial release
- Support for 24 writing systems (mostly Semitic scripts).
- CLI with input/output script options; Python API.
- Simplified abjad-only, non-standard romanization.
- Contextual final forms, ligatures, character compositions.
- Automatic script detection; bidirectional transliteration.
