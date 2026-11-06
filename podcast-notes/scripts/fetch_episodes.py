#!/usr/bin/env python3
"""
fetch_episodes.py — show link or name -> public RSS feed -> latest N episodes as MP3.

Usage:
  python3 fetch_episodes.py "<spotify|apple|rss|youtube URL or show name>" [-n 2] [--out DIR] [--dry-run]
  python3 fetch_episodes.py "The Bread Hour" -n 2 --out ./podcast-notes-work/audio

Episode links select THAT episode (never "latest"):
  Apple  .../id<show>?i=<trackId>  -> iTunes lookup of the episode -> matched in the feed by enclosure URL, then title, then date + title (never the date alone).
  Spotify open.spotify.com/episode/<id> -> page og:title (episode) + og:description (show) -> feed item by title
          (exact or >= 0.8 word overlap) or description. No confident match -> exit 5 and list the 5 closest titles.
  Show links, RSS URLs and names keep the "latest -n" behaviour.

Prints one line per episode:  idx | date | duration | title | path (or "(dry run)").
Also prints the feed it resolved, so the orchestrator can confirm it is the right show.

Resolution order (encoded decision):
  1. Spotify show/episode URL  -> page og:title (fallback: oEmbed title) -> iTunes Search API -> feedUrl
  2. Apple Podcasts URL        -> collection id -> iTunes Lookup API -> feedUrl
  3. RSS URL (anything else that returns XML with <item>)
  4. YouTube URL               -> yt-dlp audio (no feed needed)
  5. Plain show name           -> iTunes Search API -> feedUrl
Spotify-exclusive shows (no feed anywhere) -> exit 3 and tell the user to look for the same show on YouTube.

Python stdlib only. Downloads use curl (follows redirects, resumes).
"""
import argparse
import email.utils
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "Mozilla/5.0 (Macintosh) podcast-notes/1.0"
ITUNES_SEARCH = "https://itunes.apple.com/search?media=podcast&limit=5&term="
ITUNES_LOOKUP = "https://itunes.apple.com/lookup?id="


def get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def itunes_search(term):
    data = json.loads(get(ITUNES_SEARCH + urllib.parse.quote(term)))
    return [r for r in data.get("results", []) if r.get("feedUrl")]


def itunes_lookup(cid):
    data = json.loads(get(ITUNES_LOOKUP + cid))
    return [r for r in data.get("results", []) if r.get("feedUrl")]


def spotify_page(url):
    """Return (og_title, show_name_or_None, description). Real HTML: episode pages carry
    og:title = episode title, og:description = '<Show> · Episode'; show pages og:title = show name."""
    try:
        page = get(url).decode("utf-8", "ignore")
    except Exception as e:  # noqa
        print(f"  spotify page fetch failed: {e}", file=sys.stderr)
        page = ""
    def meta(key):
        m = re.search(r'<meta (?:property|name)="' + re.escape(key) + r'" content="([^"]*)"', page)
        return html.unescape(m.group(1)).strip() if m else None
    title, ogd, desc = meta("og:title"), meta("og:description"), meta("description") or ""
    show = None
    if ogd and "·" in ogd:
        show = ogd.split("·")[0].strip()
    if not show:
        m = re.search(r"from (.+?) on Spotify", desc)
        show = m.group(1).strip() if m else None
    if not title:
        try:
            o = json.loads(get("https://open.spotify.com/oembed?url=" + urllib.parse.quote(url, safe="")))
            title = o.get("title")
        except Exception as e:  # noqa
            print(f"  spotify oembed failed: {e}", file=sys.stderr)
    body = re.sub(r"^Listen to this episode from .*? on Spotify\.\s*", "", desc)
    return title, show, body


def pick_feed(results, term):
    """Prefer an exact collectionName match, else the first result. Print all so the human can see."""
    for r in results:
        print(f"  candidate: {r.get('collectionName')} | by {r.get('artistName')} | {r.get('feedUrl')}")
    t = term.strip().lower()
    for r in results:
        if (r.get("collectionName") or "").strip().lower() == t:
            return r
    return results[0] if results else None


def resolve(source):
    """Return (feed, err, target). target = None for show links, or a dict describing ONE wanted episode."""
    s = source.strip()
    if "open.spotify.com" in s:
        title, show, desc = spotify_page(s)
        is_ep = "/episode/" in s
        name = show if is_ep else title
        if not name:
            return None, "spotify page gave no show name (show may be Spotify-exclusive or page blocked)", None
        print(f"  spotify {'episode' if is_ep else 'show'}: {title!r} | show: {name!r}")
        name = re.sub(r"\s*[|–-]\s*Podcast on Spotify.*$", "", name)
        res = itunes_search(name)
        r = pick_feed(res, name)
        if not r:
            return None, f"no iTunes feed for {name!r}", None
        target = {"kind": "spotify", "title": title, "desc": desc} if is_ep else None
        return r["feedUrl"], None, target
    if "podcasts.apple.com" in s:
        m = re.search(r"/id(\d+)", s)
        ep = re.search(r"[?&]i=(\d+)", s)
        target, show_id = None, m.group(1) if m else None
        if ep:
            hit = []
            for q in (ep.group(1) + "&entity=podcastEpisode",
                      (show_id + "&entity=podcastEpisode&limit=200") if show_id else None):
                if not q:
                    continue
                data = json.loads(get(ITUNES_LOOKUP + q))
                hit = [r for r in data.get("results", []) if str(r.get("trackId")) == ep.group(1)]
                if hit:
                    break
            if hit:
                h = hit[0]
                show_id = show_id or str(h.get("collectionId") or "")
                target = {"kind": "apple", "title": h.get("trackName"), "enclosure": h.get("episodeUrl"),
                          "date": (h.get("releaseDate") or "")[:10], "desc": h.get("description") or ""}
                print(f"  apple episode {ep.group(1)}: {target['title']!r} ({target['date']})")
            else:
                return None, f"apple lookup found no episode with id {ep.group(1)}", None
        if not show_id:
            return None, "apple url has no id", None
        res = itunes_lookup(show_id)
        return (res[0]["feedUrl"] if res else None), (None if res else "apple lookup gave no feed"), target
    if re.search(r"(youtube\.com|youtu\.be)/", s):
        return s, "youtube", None
    if re.match(r"https?://", s):
        return s, None, None  # assume RSS
    res = itunes_search(s)
    r = pick_feed(res, s)
    return (r["feedUrl"] if r else None), (None if r else f"no iTunes result for {s!r}"), None


def ntext(t):
    t = html.unescape(t or "").lower().replace("&", " and ")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", t)).strip()


def overlap(a, b):
    """Dice word overlap 0..1 between two titles."""
    x, y = ntext(a).split(), ntext(b).split()
    if not x or not y:
        return 0.0
    sx, sy = set(x), set(y)
    return 2 * len(sx & sy) / (len(sx) + len(sy))


def strip_q(u):
    return (u or "").split("?")[0].rstrip("/")


def select_episode(eps, t):
    """Return (index, how) of the feed item matching target t, or (None, reason)."""
    if t.get("enclosure"):
        for i, e in enumerate(eps):
            if strip_q(e["url"]) == strip_q(t["enclosure"]):
                return i, "enclosure url"
    nt = ntext(t.get("title"))
    for i, e in enumerate(eps):
        if nt and ntext(e["title"]) == nt:
            return i, "exact title"
    scored = sorted(((overlap(t.get("title"), e["title"]), i) for i, e in enumerate(eps)), reverse=True)
    if t["kind"] == "apple" and t.get("date"):
        same = [i for i, e in enumerate(eps) if e["date"] == t["date"]]
        close = [i for i in same if overlap(t.get("title"), eps[i]["title"]) >= 0.5]
        if len(close) == 1:  # the date alone never decides; the title must agree too
            return close[0], "release date + title overlap"
    if scored and scored[0][0] >= 0.8 and (len(scored) < 2 or scored[1][0] < scored[0][0]):
        return scored[0][1], f"title overlap {scored[0][0]:.2f}"
    d = ntext(t.get("desc"))[:120]
    if len(d) >= 60:
        hits = [i for i, e in enumerate(eps) if d in ntext(e.get("desc"))]
        if len(hits) == 1:
            return hits[0], "description text"
    lines = "\n".join(f"    {sc:.2f} | {eps[i]['date']} | {eps[i]['title']}" for sc, i in scored[:5])
    return None, f"no confident match for {t.get('title')!r}. Closest 5 titles in the feed:\n{lines}"


def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    ns = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
    ch = root.find("channel")
    show = (ch.findtext("title") or "").strip() if ch is not None else ""
    eps = []
    for it in root.iter("item"):
        enc = it.find("enclosure")
        url = enc.get("url") if enc is not None else None
        if not url:
            continue
        title = (it.findtext("title") or "").strip()
        pub = it.findtext("pubDate") or ""
        try:
            date = email.utils.parsedate_to_datetime(pub).strftime("%Y-%m-%d")
        except Exception:  # noqa
            date = pub[:16]
        dur = (it.findtext("itunes:duration", namespaces=ns) or "").strip()
        desc = re.sub(r"<[^>]+>", " ", it.findtext("description") or it.findtext("itunes:summary", namespaces=ns) or "")
        eps.append({"title": title, "date": date, "duration": fmt_dur(dur), "url": url, "desc": desc})
    return show, eps


def fmt_dur(d):
    if not d:
        return "?"
    if d.isdigit():
        s = int(d)
        return f"{s // 60} min"
    parts = d.split(":")
    try:
        if len(parts) == 3:
            return f"{int(parts[0]) * 60 + int(parts[1])} min"
        if len(parts) == 2:
            return f"{int(parts[0])} min"
    except ValueError:
        pass
    return d


def slug(s, n=60):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].rstrip("-") or "episode"


def download(url, path):
    cmd = ["curl", "-L", "-sS", "-C", "-", "-A", UA, "-o", path, url]
    subprocess.run(cmd, check=True)


def youtube(url, n, out, dry):
    cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--playlist-end", str(n),
           "-o", os.path.join(out, "%(upload_date)s-%(title).60s.%(ext)s"), "--print", "after_move:filepath", url]
    if dry:
        cmd.insert(1, "--simulate")
        cmd = [c for c in cmd if c not in ("--print", "after_move:filepath")] + ["--print", "%(upload_date)s | %(duration_string)s | %(title)s"]
    print("  yt-dlp:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("-n", type=int, default=2, help="latest N episodes (default 2)")
    ap.add_argument("--out", default=".", help="folder for MP3s")
    ap.add_argument("--dry-run", action="store_true", help="resolve feed + list episodes, download nothing")
    a = ap.parse_args()

    feed, err, target = resolve(a.source)
    if err == "youtube":
        os.makedirs(a.out, exist_ok=True)
        return youtube(feed, a.n, a.out, a.dry_run)
    if not feed:
        print(f"NO FEED: {err}\n-> Spotify-exclusive? Look for the same show on YouTube and pass that link.")
        sys.exit(3)
    print(f"feed: {feed}")
    show, eps = parse_feed(get(feed, timeout=40))
    print(f"show: {show} | {len(eps)} episodes in feed")
    if not eps:
        print("feed has no enclosures")
        sys.exit(4)
    if target:
        idx, how = select_episode(eps, target)
        if idx is None:
            print(f"NO EPISODE MATCH: {how}\n-> Refusing to fall back to the latest episode.", file=sys.stderr)
            sys.exit(5)
        print(f"matched requested episode by {how}")
        eps = [eps[idx]]
    os.makedirs(a.out, exist_ok=True)
    for i, e in enumerate(eps[: a.n], 1):
        path = os.path.join(a.out, f"ep{i}-{e['date']}-{slug(e['title'])}.mp3")
        if not a.dry_run:
            download(e["url"], path)
            size = os.path.getsize(path) // 1_000_000
            where = f"{path} ({size} MB)"
        else:
            where = "(dry run)"
        print(f"{i} | {e['date']} | {e['duration']} | {e['title']} | {where}")


if __name__ == "__main__":
    main()
