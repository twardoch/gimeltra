---
title: Supported scripts
layout: default
nav_order: 2
---

# Supported scripts

Gimeltra converts between any pair of the scripts below. Latin (`Latn`) is the
pivot: a pair without a direct rule is routed source → Latin → target, so every
combination works even when no one wrote a rule for it directly.

Pass the ISO 15924 code to `-s` / `--script` (source) and `-o` / `--to-script`
(target).

| Code | Script |
|------|--------|
| `Latn` | Latin (pivot / romanization) |
| `Arab` | Arabic |
| `Armi` | Imperial Aramaic |
| `Brah` | Brahmi |
| `Chrs` | Chorasmian |
| `Egyp` | Egyptian Hieroglyphs |
| `Elym` | Elymaic |
| `Ethi` | Ethiopic |
| `Grek` | Greek |
| `Hatr` | Hatran |
| `Hebr` | Hebrew |
| `Mani` | Manichaean |
| `Narb` | Old North Arabian |
| `Nbat` | Nabataean |
| `Palm` | Palmyrene |
| `Phli` | Inscriptional Pahlavi |
| `Phlp` | Psalter Pahlavi |
| `Phnx` | Phoenician |
| `Prti` | Inscriptional Parthian |
| `Samr` | Samaritan |
| `Sarb` | Old South Arabian |
| `Sogd` | Sogdian |
| `Sogo` | Old Sogdian |
| `Syrc` | Syriac |
| `Ugar` | Ugaritic |

Run `gimeltrapy --stats` to print the live list from the installed ruleset.

## What "abjad-only" means

Gimeltra decomposes the input and strips every combining mark before mapping.
Vowel points, niqqud, and harakat are discarded; only the consonantal skeleton
survives. That is what lets a modern Hebrew word land cleanly in an ancient
script — and why the transform is not reversible when a script folds two sounds
onto one letter (Hebrew `bet` carries both *b* and *v*).
