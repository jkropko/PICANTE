"""Segment and parse reference lists from extracted PDF text into match_references.py CSVs."""
import csv, re, sys
from pathlib import Path

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
CFG = {  # seed: (style, end_line_exclusive or None, header lines to drop)
    "06": ("numbered", None, []),
    "13": ("numbered", None, ["A Practitioner-Led Investigation of Public Interest Technologists in Civil Society",
                              "Uploaded 10 August 2025"]),
    "20": ("numbered", None, []),
    "22": ("authoryear", None, []),
    "23": ("authoryear", 918, []),
}
YEAR = r"((?:19|20)\d\d[a-z]?|n\.d\.|Forthcoming)\."
INITIAL = re.compile(r"^(?:[A-Z]|[A-Z]\.-?[A-Z]|[A-Z][a-z]?\.?-[A-Z]|Jr|Sr|St|al)$")

def join(lines):
    out = ""
    for l in lines:
        l = l.strip()
        if not l: continue
        last = out.split(" ")[-1] if out else ""
        url_cont = (re.search(r"(https?:|doi\.org|10\.\d{4,}/|www\.)", last) and re.search(r"[:/._-]$", last)) or l.startswith("//")
        out = out + l if url_cont else (out + " " + l if out else l)
    out = out.replace("\x02", "")                       # broken hyphenation from PDF text layer
    out = re.sub(r"\s?[\u00b4\u02c7\u00a8\u02dc\u0060\u02da\u02c6\u00b8]\s?", " ", out)  # loose accent marks
    return re.sub(r"\s+", " ", out)

def section(s, end):
    L = (SRC / f"seed{s}.txt").read_text().splitlines()
    i = next(k for k, l in enumerate(L) if re.fullmatch(r"\s*references\s*", l, re.I))
    sec = L[i + 1:end]
    drop = set(CFG[s][2])
    return [l for l in sec if l.strip() not in drop and not re.fullmatch(r"\s*\d{1,4}\s*", l)]

def split_numbered(text):
    parts = re.split(r"\[(\d+)\]\s*", text)
    return [(int(parts[k]), parts[k + 1].strip()) for k in range(1, len(parts) - 1, 2)]

def split_authoryear(text):
    """Entry starts where the author list preceding each 'YYYY.' begins: scan back to
    the last '. ' whose preceding token is not an initial."""
    marks = [m for m in re.finditer(r"(?<=\S)\s" + YEAR + r"\s", text)]
    starts = []
    for m in marks:
        j, lo = m.start(), (starts[-1][1] if starts else 0)
        k = j
        while True:
            p = text.rfind(". ", lo, k)
            if p < 0: s0 = lo; break
            tok = text[:p].split(" ")[-1]
            if INITIAL.match(tok) or tok.endswith(";") or tok.endswith(","):
                k = p; continue
            s0 = p + 2; break
        # reject year markers that sit inside a title/venue (author segment too long or has no comma/and)
        seg = text[s0:j]
        if len(seg) > 1500 or not (("," in seg) or (" and " in seg) or len(seg.split()) <= 4):
            continue
        if re.search(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept?|Oct|Nov|Dec)\.?$|\d$|\baccessed\b", seg.strip(), re.I):
            continue
        starts.append((s0, m.end(), m))
    entries = []
    for n, (s0, e, m) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(text)
        entries.append((n + 1, text[s0:end].strip()))
    # A truncated source leaves an author fragment with no year after the last entry: drop it.
    if entries:
        n, raw = entries[-1]
        tail = re.search(r"\.\s([A-Z][^.]*,[^.]*)$", raw)
        if tail and not re.search(YEAR, tail.group(1)):
            entries[-1] = (n, raw[:tail.start() + 1])
            print(f"  dropped truncated fragment: {tail.group(1)[:60]!r}")
    return entries

def parse(raw):
    m = re.search(r"(?:^|\s)" + YEAR + r"\s", raw)
    authors, year, rest = (raw[:m.start()], m.group(1)[:4], raw[m.end():]) if m else ("", "", raw)
    if not m:  # numbered entry without a year after authors: 'Authors. Title. Venue'
        a = re.match(r"(.+?(?:\w{2,}|\)))\.\s(.*)", raw)
        if a: authors, rest = a.group(1), a.group(2)
        y = re.search(r"\b(19|20)\d\d\b", raw); year = y.group(0) if y else ""
    t = re.match(r"(.+?[.?!])(?=\s+(?:In\s|[A-Z0-9]|$))", rest)
    title = (t.group(1) if t else rest).strip().rstrip(".")
    a = authors.strip().rstrip(".")
    if ";" in a or re.match(r"^[^,]+, (?:[A-Z]\.)", a):
        first = a.split(",")[0]
    else:
        first = re.split(r",| and ", a)[0].strip().split(" ")[-1] if a else ""
    doi = re.search(r"10\.\d{4,9}/[^\s\"<>]+", raw)
    return first.strip(), year, title, doi.group(0).rstrip(".,;)") if doi else ""

for s, (style, end, _) in CFG.items():
    text = join(section(s, end))
    ents = split_numbered(text) if style == "numbered" else split_authoryear(text)
    with open(OUT / f"seed{s}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["ref_no", "raw", "first_author", "year", "title", "doi"])
        for n, raw in ents:
            w.writerow([n, raw, *parse(raw)])
    print(s, style, len(ents))
