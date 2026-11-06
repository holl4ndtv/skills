#!/usr/bin/env python3
"""
srt_to_blocks.py — merge a Whisper SRT into fixed-length blocks with ONE [m:ss] stamp each.

Usage:
  python3 srt_to_blocks.py transcripts/ep2.srt transcripts/ep2-blocks.txt [--seconds 45]

Why: raw SRT costs ~2x the tokens of the same words in blocks. The note-writer only needs
one stamp per ~45 s to cite "[12:10]". Stamps are minutes:seconds and minutes can go past 59
(so 84 min shows as [83:54], matching the format the notes use).

Python stdlib only.
"""
import argparse
import re
import sys

CUE = re.compile(r"(\d+):(\d\d):(\d\d)[,.](\d{1,3})\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d{1,3})")


def to_sec(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_srt(text):
    cues = []
    start = None
    buf = []
    for line in text.splitlines():
        m = CUE.match(line.strip())
        if m:
            if start is not None and buf:
                cues.append((start, " ".join(buf)))
            start = to_sec(*m.groups()[:4])
            buf = []
            continue
        t = line.strip()
        if not t or t.isdigit():
            if not t and start is not None and buf:
                cues.append((start, " ".join(buf)))
                start, buf = None, []
            continue
        buf.append(t)
    if start is not None and buf:
        cues.append((start, " ".join(buf)))
    return cues


def stamp(sec):
    sec = int(sec)
    return f"[{sec // 60}:{sec % 60:02d}]"


def blocks(cues, size):
    """Rolling window: a new block starts at the first cue that begins >= `size` seconds
    after the current block's first cue. The stamp is that cue's real start ([1:31], not
    [1:30]), so a stamp in the notes always points at words that are really said there."""
    out = []
    cur, cur_start = [], None
    for start, text in cues:
        if cur_start is None:
            cur_start = start
        elif start >= cur_start + size:
            out.append((cur_start, " ".join(cur)))
            cur, cur_start = [], start
        cur.append(text)
    if cur:
        out.append((cur_start, " ".join(cur)))
    return out


def clean(t):
    t = re.sub(r"\s+", " ", t).strip()
    # Whisper repeats a cue's text when audio is silent; drop exact immediate duplicates.
    t = re.sub(r"\b(\w+(?: \w+){2,8})(?: \1\b)+", r"\1", t)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("srt")
    ap.add_argument("out")
    ap.add_argument("--seconds", type=int, default=45)
    a = ap.parse_args()
    with open(a.srt, encoding="utf-8", errors="ignore") as f:
        cues = parse_srt(f.read())
    if not cues:
        print("no cues parsed", file=sys.stderr)
        sys.exit(2)
    bl = blocks(cues, a.seconds)
    with open(a.out, "w", encoding="utf-8") as f:
        for sec, text in bl:
            f.write(f"{stamp(sec)} {clean(text)}\n")
    words = sum(len(t.split()) for _, t in bl)
    print(f"{a.srt}: {len(cues)} cues -> {len(bl)} blocks of {a.seconds}s, {words} words, last stamp {stamp(bl[-1][0])} -> {a.out}")


if __name__ == "__main__":
    main()
