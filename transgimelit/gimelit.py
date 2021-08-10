#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from yaplon import reader
from wiktra import Wiktra as wt


wiktra_scripts = {
    "Egyp": "",
    "Phnx": "",
    "Armi": "",
    "Hebr": "",
    "Syrc": "",
    "Arab": "",
    "Chrs": "",
    "Samr": "",
    "Ugar": "",
    "Elym": "",
    "Hatr": "",
    "Phli": "",
    "Prti": "",
    "Mani": "",
    "Nbat": "",
    "Sogo": "",
    "Sarb": "",
    "Palm": "",
    "Phlp": "",
    "Sogd": "",
    "Narb": "",
    "Ethi": "",
    "Grek": "",
    "Brah": "",
}

lang_map_extra = {

}


def translite(text, lang):
    lang_tup = lang_map[lang.lower()]
    lua_str = (
        'res = require("wikt.translit.'
        + lang_tup[0]
        + '-translit").tr("'
        + text
        + '", "'
        + lang_tup[0]
        + '", "'
        + lang_tup[1]
        + '")'
    )
    lua.execute(lua_str)
    return lua.globals().res


with open("gimelit.tsv", "r", encoding="utf-8") as f:
    d = reader.csv(f, header=True)

print(d)
