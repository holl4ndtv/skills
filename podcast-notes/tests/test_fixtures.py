#!/usr/bin/env python3
"""Saved fact test: checks a notes page against a hand-verified fixture.

  python3 tests/test_fixtures.py <notes.html> tests/<fixture>.json

must_have: each pattern must appear somewhere in the notes (missed-detail check).
must_not:  no single sentence may match ALL of `all` and NONE of `none`
           (wrong year / wrong pairing check).
owner:     every bullet matching `match` must match `require` and not `forbid`
           (who-said-it check, judged on the whole bullet). Exit 1 on any failure.
Use it after changing the rubric or the writer prompt: re-run the writer on the
fixture episode and this must pass.
"""
import html, json, re, sys


def text_of(doc):
    doc = re.sub(r"(?s)<style.*?</style>|<script.*?</script>", " ", doc)
    doc = re.sub(r"<(li|p|h\d|blockquote|div|tr)\b", r"\n<\1", doc)
    return html.unescape(re.sub(r"<[^>]+>", " ", doc))


def sentences(t):
    out = []
    for line in t.split("\n"):
        out += [s.strip() for s in re.split(r"(?<=[.!?])\s+", line) if s.strip()]
    return out


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    t = text_of(open(sys.argv[1], encoding="utf-8").read())
    fx = json.load(open(sys.argv[2]))
    sents = sentences(t)
    fails = 0
    for m in fx["must_have"]:
        if re.search(m["pattern"], t, re.I):
            print(f"ok    have  {m['id']}")
        else:
            fails += 1
            print(f"FAIL  have  {m['id']}: missing. {m['why']}")
    for m in fx["must_not"]:
        hits = [s for s in sents
                if all(re.search(p, s, re.I) for p in m["all"])
                and not any(re.search(p, s, re.I) for p in m.get("none", []))]
        if hits:
            fails += 1
            print(f"FAIL  not   {m['id']}: {m['why']}\n        > {hits[0][:200]}")
        else:
            print(f"ok    not   {m['id']}")
    bullets = [b.strip() for b in t.split("\n") if b.strip()]
    for m in fx.get("owner", []):
        bad = [b for b in bullets if re.search(m["match"], b, re.I)
               and (not re.search(m["require"], b, re.I) or re.search(m["forbid"], b, re.I))]
        if bad:
            fails += 1
            print(f"FAIL  owner {m['id']}: {m['why']}\n        > {bad[0][:200]}")
        else:
            print(f"ok    owner {m['id']}")
    print(f"== fixture failures: {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
