---
title: Home
layout: default
nav_order: 1
---

# Gimeltra

Type a word in Hebrew, read it back in Phoenician. Gimeltra transliterates
consonants between 24 mostly-Semitic writing systems, dropping vowels and marks
so the abjad skeleton carries across alphabets that never shared a keyboard.

It is a small, scriptable tool — no phonetic model, no vocalisation, no
guesswork. One TSV of rules, Latin as the pivot, and a fast per-character pass.

## Install

```bash
pip install gimeltra
```

## Use it

Library:

```python
from gimeltra import tr

tr("שלום", sc="Hebr", to_sc="Latn")   # 'šlwm'
tr("bytk", sc="Latn", to_sc="Phnx")   # '𐤁𐤉𐤕𐤊'
tr("bytk")                            # auto-detects the source script
```

Command line (`gimeltrapy`):

```bash
gimeltrapy -t "שלום" -s Hebr -o Latn
echo "bytk" | gimeltrapy -o Arab
gimeltrapy --stats            # list every supported script
```

Scripts are named by their [ISO 15924](https://unicode.org/iso15924/) code
(`Hebr`, `Arab`, `Latn`, ...). Omit `-s` and Gimeltra guesses the source from
the text.

- [Supported scripts](scripts.md)
- [How the rules work](tsv-format.md)
