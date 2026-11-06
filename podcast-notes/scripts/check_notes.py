#!/usr/bin/env python3
"""
check_notes.py — mechanical self-check of a notes page against the transcript blocks.

Usage:
  python3 check_notes.py notes.html transcripts/ep1-blocks.txt [--names] [--window 4]
        [--ads "10:21-12:44,33:19-34:55"] [--attrib "Host Name,Guest Name"]
  (one episode per call; for a multi-episode page pass --section "Ep 1" to limit to that <h2> block)

What it checks (prints ONLY problems; "0 problems" lines mean the pass is clean):
  NUMBERS   every number in the notes must appear in the transcript. "$4.2 billion" is searched as
            4.2, "$260M" as 260, "2008-09" as 2008 and 09, small numbers also as words (16 -> sixteen).
            FOUND FAR = the number exists in the transcript but not within --window blocks of the
            bullet's own time stamp. Usually a wrong stamp, sometimes a wrong fact.
  QUOTES    every "quoted line" (3+ words) must be close to the transcript: share of the quote's
            3-word runs found anywhere in the transcript. Below 50% = NOT CLOSE: rewrite as a
            paraphrase or fix the words.
  STAMPS    every [m:ss] must be <= the last stamp in the blocks file.
  NAMES     (--names) capitalised words in the notes that never appear in the transcript. Expected
            for fixed Whisper mis-hearings (Marko vs Marco) - the orchestrator eyeballs the list.

  FEW ITEMS fewer than 15 stamped items (or none parsed) = "FAIL: too few stamped items (N)", a hard problem.
  UNITS     "$1 billion" in the notes must have the SAME scale (b/bn/billion, m/million, k/thousand) in the
            transcript window. Transcript forms: "a billion", "4.2 billion", "4 point 2 billion", "4.2b".
            A different scale = "UNIT MISMATCH", a hard problem. FOUND FAR is also a hard problem now.
  GAPS      (report only) stretches of 5+ minutes with no stamped bullet, minus --ads ranges: "GAP m:ss–m:ss (N min)".
  ATTRIB    (--attrib "Host,Guest", report only) each bullet naming the host/guest or "host" is printed with the
            transcript block at its stamp + the next block, so a reviewer can see who said it.

The script can only help check WHO said something (see ATTRIB). Attribution is the human/orchestrator pass:
grep the blocks file for each "X said / X's rule" bullet and read the surrounding block.

Python stdlib only. Exit code 0 when total hard problems == 0, else 1.
"""
import argparse
import html
import re
import sys

WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
    10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
    17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty", 30: "thirty", 40: "forty",
    50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety", 100: "hundred", 1000: "thousand",
}
STOP_CAPS = set("""The A An And But Or So He She It They We You I His Her Its Their Our Your This That These
Those When Why How What Where Who Which If Then Than In On At To For Of With By From As Is Was Are Were
Be Been Not No Yes Ep Main Best Ideas Small Why Lesson Both Show Each All Later Most Many Some Also Before
After Now Here There Host Guest Oct Nov Dec Jan Feb Mar Apr May Jun Jul Aug Sep""".split())


def strip_html(s):
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    return html.unescape(s)


def items(doc, section=None):
    """Return list of (stamp_seconds|None, text) for every <li>, blockquote, .big, .meta."""
    if section:
        m = re.search(r"(?is)<h2[^>]*>[^<]*" + re.escape(section) + r".*?(?=<h2|\Z)", doc)
        doc = m.group(0) if m else doc
    out = []
    for m in re.finditer(r"(?is)<(li|blockquote|div class=\"(?:big|meta)\")[^>]*>(.*?)</(?:li|blockquote|div)>", doc):
        raw = m.group(2)
        txt = re.sub(r"\s+", " ", strip_html(re.sub(r"<[^>]+>", " ", raw))).strip()
        st = re.search(r"\b(\d{1,3}):(\d\d)\b", txt)
        sec = int(st.group(1)) * 60 + int(st.group(2)) if st else None
        out.append((sec, txt))
    return out


def load_blocks(path):
    bl = []
    for line in open(path, encoding="utf-8", errors="ignore"):
        m = re.match(r"\[(\d+):(\d\d)\]\s*(.*)", line)
        if m:
            bl.append((int(m.group(1)) * 60 + int(m.group(2)), m.group(3)))
    return bl


def norm(t):
    t = t.lower().replace("’", "'").replace("‘", "'")
    t = re.sub(r"(?<=\d),(?=\d{3})", "", t)  # 3,000 -> 3000 so it matches the notes
    t = re.sub(r"(?<!\d)\.|\.(?!\d)", " ", t)  # keep 4.2, drop sentence dots
    t = re.sub(r"[^a-z0-9$.'* ]+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t


NUM = re.compile(r"\$?\d[\d,]*(?:\.\d+)?(?:\s?(?:billion|million|thousand|bn|b|m|k)\b)?(?:[–-]\d{2,4}(?:\s?(?:billion|million|thousand|bn|b|m|k)\b)?)?", re.I)


def num_variants(tok):
    tok = tok.strip()
    tok = re.sub(r"(?i)(?<=\d)\s?(billion|million|thousand|bn|b|m|k)$", "", tok) if re.search(r"[–-]\d{2,4}\s?[a-z]+$", tok, re.I) else tok
    rng = re.match(r"(.*?)[–-](\d{2,4})$", tok)
    out = []
    parts = [tok]
    if rng:
        parts = [rng.group(1), rng.group(2)]
    for p in parts:
        core = re.sub(r"(?i)\s?(billion|million|thousand|bn|b|m|k)$", "", p).replace("$", "").replace(",", "")
        if not core:
            continue
        v = [core]
        if re.fullmatch(r"20\d\d|19\d\d", core):
            v += ["'" + core[2:], core[2:]]
        try:
            n = float(core)
            if n == int(n) and int(n) in WORDS:
                v.append(WORDS[int(n)])
            if n == 1 and re.search(r"(?i)million|billion|thousand|[mbk]$", p):
                v.append("a " + re.sub(r"(?i).*?(million|billion|thousand|[mbk])$", r"\1", p).lower())
        except ValueError:
            pass
        out.append((p, v))
    return out


SCALE = {"b": "B", "bn": "B", "billion": "B", "m": "M", "million": "M", "k": "K", "thousand": "K"}
SCALE_RE = r"(billion|million|thousand|bn|b|m|k)"


def scale_of(word):
    return SCALE.get((word or "").lower())


def tnorm(text):
    """norm() plus spoken decimals: '4 point 2 billion' -> '4.2 billion'."""
    return re.sub(r"(\d) point (\d)", r"\1.\2", text)


def transcript_scales(core, near):
    """Scales the transcript attaches to number `core` ('' = none). Spoken 'a billion' counts as 1."""
    forms = [core]
    try:
        n = float(core)
        if n == int(n) and int(n) in WORDS:
            forms.append(WORDS[int(n)])
        if n == 1:
            forms.append("a")
    except ValueError:
        pass
    found = set()
    for f in forms:
        for m in re.finditer(r"(?<![\w.])" + re.escape(f) + r"(?:\s+" + SCALE_RE + r"\b|(" + r"[bmk]" + r")\b|(?![\w.]))", near):
            word = m.group(1) or m.group(2)
            if word:
                found.add(scale_of(word))
            elif f not in ("a",):
                found.add("")
    return found


def parse_ranges(spec):
    out = []
    for part in (spec or "").split(","):
        m = re.match(r"\s*(\d+(?::\d+)+)\s*[-–]\s*(\d+(?::\d+)+)\s*$", part)
        if m:
            out.append((to_sec(m.group(1)), to_sec(m.group(2))))
    return out


def to_sec(t):
    sec = 0
    for x in t.split(":"):
        sec = sec * 60 + int(x)
    return sec


def mmss(sec):
    return f"{sec // 60}:{sec % 60:02d}"


def found_in(variants, text):
    for v in variants:
        if re.search(r"(?<![\w.])" + re.escape(v) + r"(?:s|st|nd|rd|th)?(?![\w])", text):
            return True
    return False


def ngrams(words, n):
    return {" ".join(words[i:i + n]) for i in range(max(0, len(words) - n + 1))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("notes_html")
    ap.add_argument("blocks")
    ap.add_argument("--names", action="store_true")
    ap.add_argument("--window", type=int, default=4, help="blocks on each side of the stamp counted as 'near'")
    ap.add_argument("--ads", help='ad ranges to ignore in gap report, e.g. "10:21-12:44,33:19-34:55"')
    ap.add_argument("--attrib", help='"Host Name,Guest Name": print bullets naming them with the transcript block')
    ap.add_argument("--section", help="limit to the <h2> whose text contains this (e.g. 'Ep 1')")
    a = ap.parse_args()

    doc = open(a.notes_html, encoding="utf-8").read()
    bl = load_blocks(a.blocks)
    if not bl:
        sys.exit("no blocks parsed")
    full = norm(" ".join(t for _, t in bl))
    full_words = full.split()
    tri = ngrams(full_words, 3)
    bi = ngrams(full_words, 2)
    last = bl[-1][0]
    its = items(doc, a.section)
    bad = 0

    print(f"== {a.notes_html} vs {a.blocks}: {len(its)} items, transcript ends [{last // 60}:{last % 60:02d}]")

    # FEW ITEMS
    stamped = sum(1 for sec, _ in its if sec is not None)
    if len(its) == 0 or stamped < 15:
        bad += 1
        print(f"FAIL: too few stamped items ({stamped})")

    # STAMPS
    n = 0
    for sec, txt in its:
        if sec is not None and sec > last + 60:
            n += 1; bad += 1
            print(f"STAMP beyond transcript: {sec // 60}:{sec % 60:02d}  | {txt[:80]}")
    print(f"-- stamps: {n} problems")

    # NUMBERS
    n = 0
    for sec, txt in its:
        near = full
        if sec is not None:
            idx = max(range(len(bl)), key=lambda i: -abs(bl[i][0] - sec))
            idx = min(range(len(bl)), key=lambda i: abs(bl[i][0] - sec))
            near = norm(" ".join(t for _, t in bl[max(0, idx - a.window): idx + a.window + 1]))
        body = re.sub(r"\b\d{1,3}:\d\d\b", " ", txt)  # drop the stamp itself
        for m in NUM.finditer(body):
            for shown, variants in num_variants(m.group(0)):
                if found_in(variants, near):
                    sc = scale_of(re.sub(r"(?i)^.*?\d\s?([a-z]*)$", r"\1", m.group(0)))
                    core = variants[0]
                    if sc and re.fullmatch(r"\d+(?:\.\d+)?", core):
                        have = transcript_scales(core, tnorm(near))
                        if have and sc not in have and any(have):
                            n += 1; bad += 1
                            say = "/".join(sorted(h for h in have if h))
                            print(f"UNIT MISMATCH: notes {shown!r} ({sc}) but transcript near stamp has {core} {say}  | {txt[:90]}")
                    continue
                if found_in(variants, full):
                    n += 1; bad += 1
                    print(f"NUMBER FOUND FAR (not near stamp): {shown:>10}  | {txt[:90]}")
                else:
                    n += 1; bad += 1
                    print(f"NUMBER NOT FOUND:                  {shown:>10}  | {txt[:90]}")
    print(f"-- numbers: {n} problems")

    # QUOTES
    n = 0
    for sec, txt in its:
        quotes = re.findall(r"“([^”]*)”", txt) + re.findall(r'"([^"]*)"', txt)
        for q in quotes:
            w = [x for x in norm(q).split() if "*" not in x]  # f***ed is censored, skip it
            if len(w) < 3:
                continue
            n_ = 2 if len(w) <= 4 else 3
            g = ngrams(w, n_)
            grams = bi if n_ == 2 else tri
            hit = sum(1 for x in g if x in grams) / max(1, len(g))
            if hit < 0.5:
                n += 1; bad += 1
                print(f"QUOTE NOT CLOSE ({int(hit * 100):3d}%): \"{q[:70]}\"")
    print(f"-- quotes: {n} problems")

    # NAMES
    if a.names:
        caps = set()
        for _, txt in its:
            for w in re.findall(r"\b[A-Z][a-z]{2,}\b", txt):
                if w not in STOP_CAPS:
                    caps.add(w)
        missing = sorted(w for w in caps if w.lower() not in full)
        print(f"-- names not in transcript ({len(missing)}): " + ", ".join(missing))

    # GAPS (report only)
    stamps = sorted({sec for sec, _ in its if sec is not None})
    ads = parse_ranges(a.ads)
    pts = [0] + stamps + [last]
    ng = 0
    for lo, hi in zip(pts, pts[1:]):
        pieces = [(lo, hi)]
        for a0, a1 in ads:
            nxt = []
            for p0, p1 in pieces:
                if a1 <= p0 or a0 >= p1:
                    nxt.append((p0, p1))
                else:
                    if a0 > p0:
                        nxt.append((p0, a0))
                    if a1 < p1:
                        nxt.append((a1, p1))
            pieces = nxt
        for p0, p1 in pieces:
            if p1 - p0 >= 300:
                ng += 1
                print(f"GAP {mmss(p0)}–{mmss(p1)} ({round((p1 - p0) / 60)} min)")
    print(f"-- coverage gaps (report only): {ng}")

    # ATTRIB (report only)
    if a.attrib:
        who = [w.strip() for w in a.attrib.split(",") if w.strip()]
        keys = set(who) | {w.split()[0] for w in who}
        pat = re.compile(r"\b(?:" + "|".join(re.escape(k) for k in sorted(keys, key=len, reverse=True)) + r"|[Hh]ost)\b")
        na = 0
        print("-- attribution sheet (confirm WHO said it; report only)")
        for sec, txt in its:
            if not pat.search(txt):
                continue
            na += 1
            print(f"ATTRIB #{na} BULLET: {txt[:300]}")
            if sec is None:
                print("   (no stamp)")
                continue
            idx = min(range(len(bl)), key=lambda i: abs(bl[i][0] - sec))
            for j in (idx, idx + 1):
                if j < len(bl):
                    print(f"   [{mmss(bl[j][0])}] {bl[j][1][:400]}")
        print(f"-- attribution entries: {na}")

    print(f"== total hard problems: {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
