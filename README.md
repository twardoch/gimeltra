
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
