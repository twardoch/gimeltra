
# Gimeltra

Gimeltra is a Python 3.9+ tool for simple transliteration between 20+ writing systems, mostly of Semitic origin.

Gimeltra performs simplified abjad-only transliteration, and is primarily intended for translating simple texts from modern to ancient scripts. It uses a non-standard romanization scheme. Arabic, Greek or Hebrew letters outside the basic consonant set will not transliterate.

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

## Supported scripts / tech background

Gimeltra supports 24 scripts: Latn (Latin), Arab (Arabic), Ethi (Ethiopic), Armi (Imperial Aramaic), Brah (Brahmi), Chrs (Chorasmian), Egyp (Egyptian hieroglyphs), Elym (Elymaic), Grek (Greek), Hatr (Hatran), Hebr (Hebrew), Mani (Manichaean), Narb (Old North Arabian), Nbat (Nabataean), Palm (Palmyrene), Phli (Inscriptional Pahlavi), Phlp (Psalter Pahlavi), Phnx (Phoenician), Prti (Inscriptional Parthian), Samr (Samaritan), Sarb (Old South Arabian), Sogd (Sogdian), Sogo (Old Sogdian), Syrc (Syriac), Ugar (Ugaritic)

The below [table](gimeltra/) exists in `.numbers` and `.tsv` formats. The `.numbers` file is the source, which I export to `.tsv`, and then I [update](gimeltra/update.py) the `.json`, which the transliterator uses.

There are some simple conventions in the table:

- `|` separates alternate versions of a character
- `<` prefix means that we should only convert from this character but not to it
- `>` prefix means that we should only convert to this character but not from it
- `~` prefix indicates that this is a final form
- `%` separates the from and to strings of a character ligature

(Keep on mind that if the characters in the table are RTL, the browser renders the entire cell as RTL and changes `>` to `<` and vice versa 😀 )

The `Latn` column serves as the intermediary (all conversions are done from the source script through `Latn` to the target script). The column contains some characters that have equivalents only in some scripts. This allows less lossy coversion between, say, Hebrew and Arabic or Ethiopic and Old South Arabian.

The `<Latn` column provides fallback Latin characters if the target script does not have an equivalent to the `Latn` character. This gives lossier but still plausible conversion.

The conversion uses the [JSON](gimeltra/gimeltra_data.json) file derived from these tables. The selection of the conversion rules is based on ISO 15924 script codes. The code mimics a simple OpenType glyph processing model, but with Unicode characters:

- preprocessing with a `ccmp` table (splitting ligatures into single letters)
- character replacement in the `csub` table — first checking source-target script mapping, but if that does not exist, conversion into Latin and then from Latin
- postprocessing with `fina` table (contextual final forms), and then finally `liga` table (ligatures).


|Latn|<Latn|Name  |Arab|Ethi|Armi|Brah|Chrs  |Egyp|Elym|Grek      |Hatr|Hebr  |Mani|Narb|Nbat  |Palm  |Phli|Phlp|Phnx|Prti|Samr|Sarb|Sogd|Sogo   |Syrc |Ugar  |
|----|-----|------|----|----|----|----|------|----|----|----------|----|------|----|----|------|------|----|----|----|----|----|----|----|-------|-----|------|
|ʾ   |     |Aleph |ا   |አ   |𐡀  |𑀅  |𐾰&#124;<𐾱|𓃾  |𐿠  |α&#124;<Α      |𐣠  |א     |𐫀  |𐪑  |𐢁&#124;~𐢀|𐡠    |𐭠  |𐮀  |𐤀  |𐭀  |ࠀ   |𐩱  |𐼰  |𐼀&#124;~𐼁 |ܐ    |𐎀    |
|b   |     |Bet   |ب   |በ   |𐡁  |𑀩  |𐾲    |𓉐  |𐿡  |>β&#124;<Β     |𐣡  |בּ     |𐫁  |𐪈  |𐢃&#124;~𐢂|𐡡    |𐭡  |𐮁  |𐤁  |𐭁  |ࠁ   |𐩨  |𐼱  |𐼂&#124;~𐼃 |ܒ    |𐎁    |
|g   |     |Gimel |غ   |ገ   |𐡂  |𑀕  |𐾳    |𓌙  |𐿢  |γ&#124;<Γ      |𐣢  |ג     |𐫃  |𐪔  |𐢄    |𐡢    |𐭢  |𐮂  |𐤂  |𐭂  |ࠂ   |𐩴  |𐼲  |𐼄     |ܓ&#124;<ܔ |𐎂    |
|d   |     |Daleth|د   |ደ   |𐡃  |𑀥  |𐾴    |𓇯  |𐿣  |δ&#124;<Δ      |𐣣  |ד     |𐫅  |𐪕  |𐢅    |𐡣    |𐭣  |𐮃  |𐤃  |𐭃  |ࠃ   |𐩵  |𐼹  |𐼌     |ܕ&#124;<ܕ݂|𐎄    |
|h   |     |He    |ه   |ሀ   |𐡄  |𑀳  |𐾵    |𓀠  |𐿤  |ε&#124;<Ε      |𐣤  |ה     |𐫆  |𐪀  |𐢇&#124;~𐢆|𐡤    |𐭤  |𐮄  |𐤄  |𐭄  |ࠄ   |𐩠  |𐼳  |𐼆&#124;~𐼅 |ܗ    |𐎅    |
|w   |     |Waw   |و   |ወ   |𐡅  |𑀯  |𐾶&#124;<𐾷|𓏲  |𐿥  |υ&#124;<Υ      |𐣥  |ו     |𐫇  |𐪅  |𐢈    |𐡥    |>𐭥 |>𐮅 |𐤅  |𐭅  |ࠅ   |𐩥  |𐼴  |𐼇     |ܘ    |𐎆    |
|z   |     |Zayin |ز   |ዘ   |𐡆  |𑀚  |𐾸    |𓏭  |𐿦  |ζ&#124;<Ζ      |𐣦  |ז     |𐫉  |𐪘  |𐢉    |𐡦    |𐭦  |𐮆  |𐤆  |𐭆  |ࠆ   |>𐩹 |𐼵  |𐼈     |ܙ    |𐎇    |
|ḥ   |     |Het   |ح   |ሐ   |𐡇  |𑀖  |𐾹    |𓉗  |𐿧  |η&#124;<Η      |𐣧  |ח     |𐫍  |𐪂  |𐢊    |𐡧    |𐭧  |𐮇  |𐤇  |𐭇  |ࠇ   |𐩢  |𐼶  |𐼉     |ܚ&#124;<ܚ݂|𐎈    |
|ṭ   |     |Tet   |ط   |ጠ   |𐡈  |𑀣  |>𐿄   |𓄤  |𐿨  |θ&#124;<Θ      |𐣨  |ט     |𐫎  |𐪉  |𐢋    |𐡨    |𐭨  |>𐮑 |𐤈  |𐭈  |ࠈ   |𐩷  |>𐽃 |>𐼔    |ܛ&#124;<ܜ |𐎉    |
|y   |     |Yod   |ي   |የ   |𐡉  |𑀬  |𐾺    |𓂝  |𐿩  |ι&#124;<Ι      |𐣩  |י     |𐫏  |𐪚  |𐢍&#124;~𐢌|𐡩    |𐭩  |𐮈  |𐤉  |𐭉  |ࠉ   |𐩺  |𐼷  |𐼊     |ܝ    |𐎊    |
|k   |     |Kaf   |ك   |ከ   |𐡊  |𑀓  |𐾻    |𓂧  |𐿪  |κ&#124;<Κ      |𐣪  |כ&#124;~ך  |𐫐  |𐪋  |𐢏&#124;~𐢎|𐡪    |𐭪  |𐮉  |𐤊  |𐭊  |ࠊ   |𐩫  |𐼸  |𐼋     |ܟ&#124;<ܟ݂|𐎋    |
|l   |     |Lamd  |ل   |ለ   |𐡋  |𑀮  |𐾼    |𓌅  |𐿫  |λ&#124;<Λ      |𐣫  |ל     |𐫓  |𐪁  |𐢑&#124;~𐢐|𐡫    |𐭫  |𐮊  |𐤋  |𐭋  |ࠋ   |𐩡  |𐽄  |>𐼌    |ܠ    |𐎍    |
|m   |     |Mem   |م   |መ   |𐡌  |𑀫  |𐾽    |𓈖  |𐿬  |μ&#124;<Μ      |𐣬  |מ&#124;~ם  |𐫖  |𐪃  |𐢓&#124;~𐢒|𐡬    |𐭬  |𐮋  |𐤌  |𐭌  |ࠌ   |𐩣  |𐼺  |𐼍     |ܡ    |𐎎    |
|n   |     |Nun   |ن   |ነ   |𐡍  |𑀦  |𐾾    |𓆓  |𐿭  |ν&#124;<Ν      |𐣭  |נ&#124;~ן  |𐫗  |𐪌  |𐢕&#124;~𐢔|𐡭&#124;<𐡮|𐭭  |𐮌  |𐤍  |𐭍  |ࠍ   |𐩬  |𐼻  |𐼎&#124;~𐼏 |ܢܢ&#124;<ܢ|𐎐    |
|s   |     |Samekh|س   |ሰ   |𐡎  |𑀱  |𐾿    |𓊽  |𐿮  |σ&#124;~ς&#124;<Σ   |𐣮  |ס     |𐫘  |𐪊  |𐢖    |𐡯    |𐭮  |𐮍  |𐤎  |𐭎  |ࠎ   |𐩪  |𐼼  |𐼑     |ܣ    |𐎒    |
|ʿ   |     |Ain   |ع   |ዐ   |𐡏  |𑀏  |𐿀    |𓁹  |𐿯  |ο&#124;<ω&#124;<Ο&#124;<Ω|𐣯  |ע     |𐫙  |𐪒  |𐢗    |𐡰    |𐭥  |𐮅  |𐤏  |𐭏  |ࠏ   |𐩲  |𐼽  |𐼓&#124;<𐼒 |ܥ    |𐎓    |
|p   |     |Pe    |پ   |ፐ   |𐡐  |𑀧  |𐿁    |𓂋  |𐿰  |π&#124;<Π      |𐣰  |פ&#124;~ף  |𐫛  |>𐪐 |𐢘    |𐡱    |𐭯  |𐮎  |𐤐  |𐭐  |>ࠐ  |>𐩰 |𐼾  |𐼔     |ܦ    |𐎔    |
|ṣ   |     |Sade  |ض   |ጸ   |𐡑  |𑀘  |>𐾿   |𓇑  |𐿱  |ϻ&#124;<Ϻ      |𐣱  |צ&#124;~ץ  |𐫝  |𐪎  |𐢙    |𐡲    |𐭰  |𐮏  |𐤑  |𐭑  |ࠑ   |𐩮  |𐼿  |𐼕&#124;~𐼖 |ܨ    |𐎕    |
|q   |     |Qof   |ق   |ቀ   |𐡒  |𑀔  |>𐾻   |𓃻  |𐿲  |ϙ&#124;<Ϙ      |𐣲  |ק     |𐫞  |𐪄  |𐢚    |𐡳    |𐭬  |𐮋  |𐤒  |𐭒  |ࠒ   |𐩤  |>𐼸 |>𐼋    |ܩ    |𐎖    |
|r   |     |Resh  |ر   |ረ   |𐡓  |𑀭  |𐿂    |𓁶  |𐿳  |ρ&#124;<Ρ      |𐣣  |ר     |𐫡  |𐪇  |𐢛    |𐡴    |>𐭥 |>𐮅 |𐤓  |𐭓  |ࠓ   |𐩧  |𐽀  |𐼘     |ܪ    |𐎗    |
|š   |     |Shin  |ش   |ሠ   |𐡔  |𑀰  |𐿃    |𓌓  |𐿴  |ξ&#124;<Ξ      |𐣴  |ש     |𐫢  |𐪏  |𐢝&#124;~𐢜|𐡵    |𐭱  |𐮐  |𐤔  |𐭔  |ࠔ   |𐩦  |𐽁  |𐼙     |ܫ    |𐎌&#124;<𐎝|
|t   |     |Tau   |ت   |ተ   |𐡕  |𑀢  |𐿄    |𓏴  |𐿵  |τ&#124;<Τ      |𐣵  |ת     |𐫤  |𐪗  |𐢞    |𐡶    |𐭲  |𐮑  |𐤕  |𐭕  |ࠕ   |𐩩  |𐽂  |𐼚&#124;~𐼛 |ܬ    |𐎚    |
|ḍ   |d    |      |ض   |    |    |    |      |    |    |          |    |      |    |𐪓  |      |      |    |    |    |    |    |    |    |       |     |      |
|f   |p    |      |ف   |ፈ   |    |    |      |    |    |φ&#124;<Φ      |    |פּ&#124;~ףּ  |    |𐪐  |      |      |    |    |    |    |ࠐ   |𐩰  |𐽃  |>𐼔    |     |      |
|ġ   |h    |      |    |    |    |    |      |    |    |          |    |גּ     |    |𐪖  |      |      |    |    |    |    |    |    |    |       |     |𐎙    |
|ḏ   |d    |      |ذ   |    |    |    |      |    |    |          |    |דּ     |    |    |      |      |    |    |    |    |    |𐩹  |    |       |     |      |
|ḵ   |k    |      |خ   |    |    |    |      |    |    |          |    |כּ&#124;~ךּ  |    |    |      |      |    |    |    |    |    |    |    |       |     |      |
|ḫ   |ḥ    |      |    |ኀ   |    |    |      |    |    |          |    |      |    |    |      |      |    |    |    |    |    |𐩭  |    |       |     |      |
|j   |g    |      |ج   |    |    |    |      |    |    |          |    |ג׳    |    |    |      |      |    |    |    |    |    |    |    |       |     |      |
|v   |b    |      |    |    |    |    |      |    |    |β         |    |ב     |    |    |      |      |    |    |    |    |    |    |    |       |     |𐎜    |
|č   |tš   |      |چ   |ፀ   |    |    |      |    |    |          |    |צ׳&#124;~ץ׳|    |    |      |      |    |    |    |    |    |    |    |       |     |      |
|ṯ   |t    |      |ث   |    |    |    |      |    |    |          |    |תּ     |    |    |      |      |    |    |    |    |    |    |    |       |     |𐎘    |
|ẓ   |z    |      |ظ   |    |    |    |      |    |    |          |    |      |    |    |      |      |    |    |    |    |    |    |    |       |     |𐎑    |
|ž   |z    |      |    |    |    |    |      |    |    |          |    |ז׳    |    |    |      |      |    |    |    |    |    |    |    |       |     |      |
|p̣  |p    |      |    |ጰ   |    |    |      |    |    |          |    |      |    |    |      |      |    |    |    |    |    |    |    |       |     |      |
|    |     |      |    |    |    |    |      |    |    |          |    |      |    |    |      |      |    |    |    |    |    |    |    |𐼓𐼌%𐼧|     |      |


## License

Copyright © 2021 Adam Twardoch, [MIT license](./LICENSE)

## Other projects of interest

- [Wiktra](https://github.com/kbatsuren/wiktra/) — Python transliterator for 100+ scripts and 500+ languages, mostly into Latin but in some cases across other scripts. Uses the Wiktionary transliteration modules written in Lua. Needs Lua runtime.
- [Aksharamukha](https://github.com/virtualvinodh/aksharamukha-python) - Python (plus [JS and web](https://github.com/virtualvinodh/aksharamukha)) transliterator within the Indic cultural sphere, for 94 scripts and 8 romanization methods. Does conversion between scripts.
