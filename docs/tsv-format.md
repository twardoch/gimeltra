---
title: How the rules work
layout: default
nav_order: 3
---

# How the rules work

All of Gimeltra's knowledge lives in one file, `gimeltra/gimeltra.tsv`. Each row
is one abjad letter; each column is a script. `update.py` compiles the TSV into
`gimeltra_data.json`, which the engine loads at runtime.

## The TSV

- The `Latn` column holds the canonical romanization — the anchor every other
  script maps to and from.
- Every other column holds that letter's form in that script, written as a
  cluster of `|`-separated codepoints with a few sigils:

| Sigil | Meaning |
|-------|---------|
| *(bare)* | the letter, used both when converting to and from this script |
| `>x` | `x` is written only when converting **into** this script |
| `<x` | `x` is accepted only when converting **from** this script |
| `~x` | `x` is the word-**final** form of the letter |
| `a%b` | ligature: `a` is rewritten to `b` after conversion |

The special `<Latn` column feeds the *simplify* table, which folds rare Latin
transcriptions onto a base letter so a missing target still resolves.

## The passes

Each conversion runs three passes (see `gimeltra.py`):

1. **Preprocess** — apply `ccmp` cluster rewrites, NFD-decompose, then drop every
   combining mark. This is the abjad reduction.
2. **Convert** — map each character source → target, pivoting through Latin when
   no direct rule exists.
3. **Postprocess** — apply `fina` word-final forms and `liga` ligatures in the
   target script.

## Regenerating the data

Edit the TSV, then rebuild the JSON:

```bash
pip install "gimeltra[update]"
python -m gimeltra.update
```
