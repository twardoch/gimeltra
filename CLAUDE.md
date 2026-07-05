<!-- this_file: CLAUDE.md -->

# CLAUDE.md — Gimeltra

Abjad transliteration between 24 mostly-Semitic writing systems. Python 3.9+
library and `gimeltrapy` CLI. Flat package layout, hatch + hatch-vcs build.

## Source files

| File | Role |
|------|------|
| `gimeltra/__init__.py` | Public API (`tr`, `Transliterator`), version via `importlib.metadata` |
| `gimeltra/gimeltra.py` | Engine: preprocess → convert → postprocess |
| `gimeltra/__main__.py` | CLI (`gimeltrapy`); run with `python -m gimeltra` |
| `gimeltra/update.py` | Dev tool: compiles `gimeltra.tsv` → `gimeltra_data.json` (needs `[update]` extra) |
| `gimeltra/gimeltra.tsv` | Source of all rules — the file to edit |
| `gimeltra/gimeltra_data.json` | Generated ruleset loaded at runtime |
| `tests/test_gimeltra.py` | Pytest suite (conversions, round-trips, CLI, edges) |

## Architecture notes

- **Latin is the pivot.** Direct source→target rules are used when present;
  otherwise the character is routed source→Latin→target, so any pair works.
- **Abjad reduction happens in `_preprocess`:** NFD decompose, then drop every
  `\p{M}` combining mark. Vowels and diacritics are intentionally lost — the
  transform is lossy and not always reversible.
- **Rule tables** (keys in `gimeltra_data.json`): `ccmp` (cluster pre-rewrites),
  `ssub` (script→script substitutions), `simp` (fold rare Latin variants),
  `fina` (word-final forms), `liga` (post-conversion ligatures).
- **Version** is derived from git tags by hatch-vcs; never hard-code it.

## Conventions

- Keep the flat `gimeltra/` package (a `src/` migration is noted in `TODO.md`).
- Every source file starts with a `this_file:` header.
- Verify with `./build.sh` (ruff + mypy + pytest + build) before releasing.
- Output can carry Unicode presentation-form ligatures (e.g. Hebrew bet+dagesh
  U+FB31); compare with NFKC normalization in tests.
