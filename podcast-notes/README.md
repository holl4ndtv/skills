# podcast-notes

## What it does

It turns a podcast episode into one web page of detailed notes. The page has time stamps, the main
lessons, the big moments, the best lines, and the small things that are easy to miss.

It downloads the audio, turns it into text on your own Mac (free), and has Claude write the notes.
Scripts then check the numbers, quotes and time stamps against the text.

## What you need

| Tool | What it is for | Cost |
|---|---|---|
| A Mac (Apple Silicon works best) | The steps below use Homebrew. Windows is not supported. | Free |
| Claude Code | Runs the skill and writes the notes | Needs a Claude plan or API credits |
| Homebrew | Installs the tools below | Free |
| ffmpeg | Converts audio | Free |
| whisper.cpp | Turns speech into text on your Mac | Free |
| A Whisper model file (1.6 GB) | The "brain" of whisper.cpp | Free |
| python3 | Runs the helper scripts (no extra packages) | Free, comes with the Mac developer tools |
| yt-dlp (optional) | Only for YouTube links | Free |

Disk space: about 2 GB for the model, plus the audio files.

## Install

1. Install Homebrew if you do not have it. Go to https://brew.sh and copy the one-line command from the page into the Terminal app.
2. Install the tools:

   ```bash
   brew install ffmpeg whisper-cpp
   brew install yt-dlp    # optional, for YouTube links
   ```

3. Download the Whisper model (1.6 GB, one time):

   ```bash
   mkdir -p ~/.cache/whisper-cpp
   curl -L -o ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin \
     https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
   ```

   Want a faster, smaller test? Download `ggml-base.en.bin` (about 150 MB) from the same address, then run with
   `WHISPER_MODEL=~/.cache/whisper-cpp/ggml-base.en.bin`. The notes will be less accurate.

4. Copy the skill folder into Claude Code. If you cloned this repo to `~/skills`:

   ```bash
   mkdir -p ~/.claude/skills
   cp -R ~/skills/podcast-notes ~/.claude/skills/
   ```

5. Check the install:

   ```bash
   command -v ffmpeg whisper-cli python3
   ls ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin
   python3 ~/.claude/skills/podcast-notes/tests/test_fixtures.py \
     ~/.claude/skills/podcast-notes/tests/sample/sample-notes.html \
     ~/.claude/skills/podcast-notes/tests/sample/sample.json
   ```

   The last line of the test output must say `fixture failures: 0`.

## Test it

Open Claude Code, then type:

> Make podcast notes for the latest episode of "99% Invisible"

You can also paste a Spotify, Apple Podcasts or RSS link, or a YouTube link to a podcast episode.
The first run downloads the audio and takes a few minutes. You get one HTML page and the path to it.

## Notes

- A show that exists only on Spotify has no public audio feed. The skill then asks for a YouTube link of the same show.
- The test sample in `tests/sample/` is made up. It is not from a real episode.
- Notes come from an automatic transcript. Names and numbers can be wrong. The scripts catch many errors, not all.

## How I use it

I send it a podcast link and read the page on my phone.

## Credits

Written by Yauhen Massalski. MIT license (see the LICENSE file in the root of this repo).
Uses whisper.cpp (https://github.com/ggml-org/whisper.cpp, MIT) and ffmpeg (https://ffmpeg.org) as separate tools. They are not included here.
