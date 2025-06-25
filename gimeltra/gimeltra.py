#!/usr/bin/env python3

import json
import logging
from collections import Counter
from pathlib import Path

import regex as re
from fontTools import unicodedata as ucd

cwd = Path(Path(__file__).parent)


class Transliterator:
    def __init__(self):
        with open(Path(cwd, "gimeltra_data.json"), encoding="utf-8") as f:
            data = json.load(f)
        self.db = data["ssub"]
        self.db_ccmp = data["ccmp"]
        self.db_simplify = data["simp"]
        self.db_fina = data["fina"]
        self.db_liga = data["liga"]

    def auto_script(self, text):
        sc_count = Counter([ucd.script(c) for c in text])
        sc = sc_count.most_common(1)[0][0]
        if not sc:
            sc = "Zyyy"
        return sc

    def _tr(self, text, sc, to_sc):
        t = text
        t = self._preprocess(t, sc)
        t = self._convert(t, sc, to_sc)
        t = self._postprocess(t, to_sc)
        return t

    def _preprocess(self, text, sc):
        t = text
        for rule_i, rule_o in self.db_ccmp.get(sc, {}).items():
            t = t.replace(rule_i, rule_o)
        t = ucd.normalize("NFD", t)
        t = re.sub(r"\p{M}", "", t)
        logging.debug(f"Pre: {list(t)}")
        return t

    def _postprocess(self, text, sc):
        t = text
        for rule_i, rule_o in self.db_fina.get(sc, {}).items():
            t = re.subf(rf"(\p{{L}})({rule_i})([^\p{{L}}])", f"{{1}}{rule_o}{{3}}", t)
            t = re.subf(rf"(\p{{L}})({rule_i})$", f"{{1}}{rule_o}", t)
        for rule_i, rule_o in self.db_liga.get(sc, {}).items():
            t = t.replace(rule_i, rule_o)
        logging.debug(f"Post: {list(t)}")
        return t

    def _convert(self, text, sc, to_sc):
        t = ""
        for c in text:
            c_dir = self.db.get(sc, {}).get(to_sc, {}).get(c, None)
            logging.debug(f"C:{c} D:{c_dir}")
            if c_dir:
                t += c_dir
                continue
            c_lat = self.db.get(sc, {}).get("Latn", {}).get(c, c)
            c_tgt = self.db.get("Latn", {}).get(to_sc, {}).get(c_lat, None)
            logging.debug(f"C:{c} L:{c_lat} T:{c_tgt}")

            if not c_tgt:
                c_lat = self.db_simplify.get(c_lat, c_lat)
                c_tgt = self.db.get("Latn", {}).get(to_sc, {}).get(c_lat, c)
            t += c_tgt
        logging.debug(f"Conv: {list(t)}")
        return t

    def tr(self, text, sc=None, to_sc="Latn"):
        if not sc:
            sc = self.auto_script(text)
        logging.debug(
            {
                "script": sc,
                "to_script": to_sc,
            }
        )
        logging.debug(f"Text: {list(text)}")
        res = self._tr(text, sc, to_sc)
        return res


def tr(text, sc=None, to_sc="Latn"):
    tr = Transliterator()
    return tr.tr(text, sc, to_sc)
