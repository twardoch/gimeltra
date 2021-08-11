
# Gimeltra

Gimeltra is a Python 3.9+ tool for simple transliteration between 20+ writing systems, mostly of Semitic origin.

_This is primarily intended for translating simple texts from modern to ancient scripts. It uses a non-standard romanization scheme. Arabic, Greek or Hebrew letters outside the “basic” old Semitic set will not transliterate._

## Installation

```sh
python3 -m pip install --upgrade git+https://github.com/twardoch/gimeltra
```

## Usage

### Command-line

```sh
$ gimeltrapy -h
usage: gimeltrapy [-h] [-t TEXT] [-i FILE] [-s SCRIPT] [-o SCRIPT] [--stats] [-v] [-V]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT
  -i FILE, --input FILE
  -s SCRIPT, --script SCRIPT
                        Input script as ISO 15924 code
  -o SCRIPT, --to-script SCRIPT
                        Output script as ISO 15924 code
  --stats               List supported scripts
  -v, --verbose         -v show progress, -vv show debug
  -V, --version         show version and exit
```

Examples:

```sh
$ gimeltrapy -t "لرموز"
lrmwz
$ gimeltrapy -t "لرموز" -o Hebr
לרמוז
$ gimeltrapy -t "لرموز" -o Narb
𐪁𐪇𐪃𐪅𐪘
$ gimeltrapy -t "لرموز" -o Sogo
𐼌𐼘𐼍𐼇𐼈
```

Or from stdin / via piping:

```sh
$ echo لرموز | gimeltrapy -o Grek
λρμυζ
```

### Python

```python
from gimeltra.gimeltra import Transliterator
tr = Transliterator()
print(tr.tr("لرموز", sc='Arab', to_sc='Hebr')
```

Less efficient:

```python
from gimeltra import tr
print(tr("لرموز")
```

## Supported scripts

24 scripts: Latn Arab Ethi Armi Brah Chrs Egyp Elym Grek Hatr Hebr Mani Narb Nbat Palm Phli Phlp Phnx Prti Samr Sarb Sogd Sogo Syrc Ugar

## License

Copyright © 2021 Adam Twardoch, [MIT license](./LICENSE)

## Other projects of interest

- [Wiktra](https://github.com/kbatsuren/wiktra/) — Python transliterator for 100+ scripts and 500+ languages, mostly into Latin but in some cases across other scripts. Uses the Wiktionary transliteration modules written in Lua. Needs Lua runtime.
- [Aksharamukha](https://github.com/virtualvinodh/aksharamukha-python) - Python (plus [JS and web](https://github.com/virtualvinodh/aksharamukha)) transliterator within the Indic cultural sphere, for 94 scripts and 8 romanization methods. Does conversion between scripts.
