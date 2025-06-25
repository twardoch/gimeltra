#!/usr/bin/env python3

from collections import OrderedDict as od
from pathlib import Path

from yaplon import reader, writer

# od = dict

cwd = Path(__file__).parent


class GimeltraMakeDb:
    def __init__(self):
        with open(Path(cwd, "gimeltra.tsv"), encoding="utf-8") as f:
            self.l = reader.csv(f, header=True)
        self.scs = []
        self.db = od()
        self.db_fina = od()
        self.db_simplify = od()
        self.db_ccmp = od()
        self.db_liga = od()
        self.init_db()
        self.build_db()
        self.save_db()

    def init_db(self):
        for sc in self.l[0]:
            if sc not in ("Name", "<Latn", "Latn"):
                self.scs.append(sc)
                self.db_fina[sc] = od()
                self.db_liga[sc] = od()
                self.db_ccmp[sc] = od()
            if sc not in ("Name", "<Latn"):
                self.db[sc] = od()
                for sc1 in self.l[0]:
                    if sc1 not in ("Name", "<Latn") and sc1 != sc:
                        self.db[sc][sc1] = od()

    def parse_cluster(self, cluster):
        s_to = None  # String used when converting both from and to script
        l_from = []  # List of strings used only when converting from script
        s_fina = None  # Target string used as a final form of s_to
        s_liga_from = None  # Source string used in ligature replacement
        s_liga_to = None  # Target string used in ligature replacement
        l_cmps = cluster.split("|")
        for s in l_cmps:
            if s[0] == "<":
                l_from.append(s[1:])
            elif s[0] == "~":
                s_fina = s[1:]
                l_from.append(s_fina)
            elif s[0] == ">":
                s_to = s[1:]
            else:
                l_main = s.split("%")
                if len(l_main) > 1:
                    s_liga_from = l_main[0]
                    s_liga_to = l_main[1]
                else:
                    l_from.append(l_main[0])
                    s_to = l_main[0]
        return s_to, l_from, s_fina, s_liga_from, s_liga_to

    def add_record(self, latn, sc, s_to, l_from, s_fina, s_liga_from, s_liga_to):
        for s in l_from:
            self.db[sc]["Latn"][s] = latn
        if s_to:
            self.db["Latn"][sc][latn] = s_to
        if s_fina:
            self.db_fina[sc][s_to] = s_fina
        if s_liga_from:
            if not s_liga_to:
                s_liga_to = ""
            self.db_liga[sc][s_liga_from] = s_liga_to
            if s_liga_to:
                self.db_ccmp[sc][s_liga_to] = s_liga_from

    def build_db(self):
        for r in self.l:
            latn = r["Latn"] if r["Latn"] else None
            for sc in self.scs + ["<Latn"]:
                cluster = r[sc] if r[sc] else None
                if cluster:
                    s_to, l_from, s_fina, s_liga_from, s_liga_to = self.parse_cluster(
                        cluster
                    )
                    print(
                        f"latn: {latn}, sc: {sc}, s_to: {s_to}, l_from: {l_from}, s_fina: {s_fina}, s_liga_from: {s_liga_from}, s_liga_to: {s_liga_to}"
                    )
                    if sc == "<Latn":
                        self.db_simplify[latn] = s_to
                    else:
                        self.add_record(
                            latn, sc, s_to, l_from, s_fina, s_liga_from, s_liga_to
                        )

    def save_db(self):
        data = od(
            [
                ("ccmp", self.db_ccmp),
                ("ssub", self.db),
                ("simp", self.db_simplify),
                ("fina", self.db_fina),
                ("liga", self.db_liga),
            ]
        )
        with open(Path(cwd, "gimeltra_data.json"), "w", encoding="utf-8") as f:
            writer.json(data, f)


if __name__ == "__main__":
    mdb = GimeltraMakeDb()
