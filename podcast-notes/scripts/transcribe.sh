#!/usr/bin/env bash
# transcribe.sh - audio file -> 16 kHz mono WAV -> whisper.cpp -> .srt + .txt
#
# Usage:  transcribe.sh <audio.mp3> <out_dir> [basename]
#         transcribe.sh audio/ep1.mp3 transcripts ep1
# Output: <out_dir>/<basename>.srt and <basename>.txt   (then run srt_to_blocks.py)
#
# Needs: ffmpeg, whisper-cli (from whisper-cpp), and a model file.
# Default model: ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin
# Use another model with:  WHISPER_MODEL=/path/to/model.bin transcribe.sh ...
# Threads: WHISPER_THREADS (default 8).
set -euo pipefail

MODEL="${WHISPER_MODEL:-$HOME/.cache/whisper-cpp/ggml-large-v3-turbo.bin}"
THREADS="${WHISPER_THREADS:-8}"

in="${1:?audio file}"; out_dir="${2:?output dir}"; base="${3:-$(basename "${in%.*}")}"
mkdir -p "$out_dir"
wav="$out_dir/$base.wav"

for bin in ffmpeg whisper-cli; do
  command -v "$bin" >/dev/null || { echo "missing $bin (run: brew install ffmpeg whisper-cpp)" >&2; exit 2; }
done
[ -f "$MODEL" ] || { echo "missing model file: $MODEL (see the README for the download command)" >&2; exit 2; }

echo "wav: $in -> $wav"
ffmpeg -y -loglevel error -i "$in" -ar 16000 -ac 1 -c:a pcm_s16le "$wav"

echo "whisper ($THREADS threads): $wav"
start=$(date +%s)
whisper-cli -m "$MODEL" -t "$THREADS" -osrt -otxt -of "$out_dir/$base" -f "$wav" >/dev/null
echo "done in $(( $(date +%s) - start )) s: $out_dir/$base.srt  $out_dir/$base.txt"
rm -f "$wav"
