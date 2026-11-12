#!/bin/zsh
# Record ONE take of the whole script.json in Michael's cloned HeyGen voice (free turbo model).
# Writes <video>/.voice-heygen-full/full.raw (WAV) and words.json (HeyGen original_words timestamps).
#
# Why a nested `claude -p`: the HeyGen MCP sign-in only works from the Claude Code CLI; the desktop app's
# OAuth fails with "Invalid redirect URI" (anthropics/claude-code#108607). The CLI keeps its own sign-in.
# Usage: zsh heygen_take.sh <video folder>      (run from the repo root; reads the voice id from AVATAR-MICHAEL.md)
set -eu
V=${1:?video folder}
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
VOICE=$(sed -n 's/^voice_id: *//p' "$ROOT/AVATAR-MICHAEL.md")
MODEL=$(sed -n 's/^voice_model: *\([^ ]*\).*/\1/p' "$ROOT/AVATAR-MICHAEL.md")
[ -n "$VOICE" ] || { echo "no voice_id in AVATAR-MICHAEL.md"; exit 1; }
D="$V/.voice-heygen-full"; mkdir -p "$D"; rm -f "$D/full.raw" "$D/words.json"
TXT=$(python3 -I -c 'import json,re,sys;print("".join(re.sub(r"(?<![A-Za-z])[A-Za-z](?: [A-Za-z](?![A-Za-z]))+",lambda m:m.group(0).replace(" ",""),l["say"]) for l in json.load(open(sys.argv[1]))))' "$V/script.json")
CLAUDE=$(command -v claude || echo "$HOME/.local/bin/claude")
timeout 580 "$CLAUDE" -p "Do this now without asking questions. Call the heygen MCP tool create_speech ONCE with: voice_id $VOICE, model ${MODEL:-heygen-voice-1-turbo-free}, language zh, withTimestamps true, text:
$TXT
Then 1) curl the returned audio URL to $D/full.raw. 2) Use the Write tool to save the response's original_words array, unchanged, as JSON to $D/words.json. Do not create videos, upgrade or buy anything. If the call fails, retry once, then report the exact error. Final reply: duration and whether words were saved." \
  --allowedTools "mcp__heygen__*" "Bash(curl:*)" "Write" 2>&1 | tail -6
[ -s "$D/full.raw" ] && [ -s "$D/words.json" ] || { echo "TAKE FAILED: missing $D/full.raw or words.json (if the error mentions auth, run: claude, then /mcp, sign in to heygen)"; exit 1; }
echo "take ok: $D"
