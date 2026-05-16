#!/usr/bin/env python3
"""Stdlib-only .xlsx -> .csv extractor (no openpyxl/pandas in this env).

Usage:
  python3 tools/xlsx_to_csv.py <file.xlsx> <out_dir> [--prefix NAME]

Writes one CSV per worksheet: <out_dir>/<prefix><NN>_<sheetname>.csv
Prints a manifest (sheet -> rows -> csv path). Handles shared strings,
inline strings, numbers; preserves sparse rows by cell reference.
"""
import csv, os, re, sys, zipfile
import xml.etree.ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PNS = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def col_index(ref):
    m = re.match(r"([A-Z]+)", ref or "A")
    n = 0
    for ch in m.group(1):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def num(s):
    # GSC/keyword exports store numbers as float strings; keep ints clean.
    try:
        f = float(s)
        return str(int(f)) if f.is_integer() else repr(f)
    except (TypeError, ValueError):
        return s


def extract(path, out_dir, prefix=""):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.findall(NS + "si"):
            shared.append("".join(t.text or "" for t in si.iter(NS + "t")))

    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {}
    rel_root = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    for r in rel_root:
        rels[r.get("Id")] = r.get("Target")
    sheets = []
    for s in wb.iter(NS + "sheet"):
        rid = s.get(RNS + "id")
        tgt = rels.get(rid, "")
        if not tgt.startswith("/"):
            tgt = "xl/" + tgt.lstrip("/")
        else:
            tgt = tgt.lstrip("/")
        sheets.append((s.get("name"), tgt))

    os.makedirs(out_dir, exist_ok=True)
    manifest = []
    for idx, (name, wsfile) in enumerate(sheets):
        if wsfile not in z.namelist():
            cands = sorted(n for n in z.namelist()
                           if n.startswith("xl/worksheets/sheet"))
            if idx < len(cands):
                wsfile = cands[idx]
            else:
                continue
        ws = ET.fromstring(z.read(wsfile))
        safe = re.sub(r"[^0-9A-Za-z_]+", "_", name).strip("_") or f"sheet{idx}"
        csv_path = os.path.join(out_dir, f"{prefix}{idx:02d}_{safe}.csv")
        n_rows = 0
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            for row in ws.iter(NS + "row"):
                cells = {}
                maxc = -1
                for c in row.findall(NS + "c"):
                    ci = col_index(c.get("r", "A"))
                    maxc = max(maxc, ci)
                    t = c.get("t")
                    val = ""
                    if t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter(NS + "t"))
                    else:
                        v = c.find(NS + "v")
                        if v is not None and v.text is not None:
                            if t == "s":
                                val = shared[int(v.text)]
                            elif t == "b":
                                val = "TRUE" if v.text == "1" else "FALSE"
                            else:
                                val = num(v.text)
                    cells[ci] = val
                w.writerow([cells.get(i, "") for i in range(maxc + 1)])
                n_rows += 1
        manifest.append((name, n_rows, csv_path))

    print(f"SOURCE: {path}")
    for name, rows, p in manifest:
        print(f"  sheet '{name}': {rows} rows -> {p}")
    return manifest


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    pre = ""
    if "--prefix" in sys.argv:
        pre = sys.argv[sys.argv.index("--prefix") + 1]
    extract(sys.argv[1], sys.argv[2], pre)
