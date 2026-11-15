#!/usr/bin/env python3
"""Voice: synthesize brief.json's script with local Qwen3-TTS (MLX), check every segment, write episode.m4a.

Runs in the agent's own Python 3.12 venv (RUNTIME/venv-tts), never downloads anything (HF_HUB_OFFLINE=1):
  venv-tts/bin/python -I tts.py <brief.json> <out_dir> --voice memory/voice.json [--sample "text"]

Writes <out_dir>/episode.wav, episode.m4a (AAC 64 kb/s mono, made by macOS afconvert), segments.json and
episode.json {"seconds", "took", "chapters": {chapter_id: start_seconds}}; the last stdout line is that JSON.
Synthesis follows the original project: short chunks (≤ 38 words), up to 3 tries per chunk with a new seed,
a QA check on each chunk (not silent, not cut off, plausible speaking rate). The episode is never sped up.
"""
import argparse
import json
import os
import re
import subprocess
import time

import mlx.core as mx
import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load_model

RUNTIME = os.path.expanduser("~/Library/Application Support/ai-podcast")   # the voice model lives with ai-podcast; sg-podcast shares it
MAX_WORDS = 38
PAUSE = {"sentence": 0.12, "paragraph": 0.45, "chapter": 1.0}


def chunks(paragraph):
    out, cur = [], ""
    for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", paragraph.strip()):
        if cur and len((cur + " " + s).split()) > MAX_WORDS:
            out.append(cur)
            cur = ""
        cur = (cur + " " + s).strip()
    if cur:
        out.append(cur)
    return out


def qa(audio, sr, text):
    secs = len(audio) / sr
    words = len(text.split())
    rms = float(np.sqrt(np.mean(np.square(audio)))) if len(audio) else 0.0
    if rms < 0.003:
        return "silent"
    if not (words / 4.6 <= secs <= words / 1.2 + 1.5):
        return "rate %.1f words/s" % (words / max(secs, 0.01))
    # a long silent stretch inside a chunk usually means the model stalled
    frame = int(sr * 0.05)
    quiet = run = 0
    for i in range(0, len(audio) - frame, frame):
        run = run + 1 if np.sqrt(np.mean(np.square(audio[i:i + frame]))) < 0.002 else 0
        quiet = max(quiet, run)
    if quiet * 0.05 > 2.5:
        return "silence %.1f s inside" % (quiet * 0.05)
    return None


def synth(model, cfg, text, seed):
    mx.random.seed(seed)
    res = list(model.generate_custom_voice(text=text, speaker=cfg["speaker"], language=cfg.get("language", "English"),
                                           instruct=cfg.get("instruct"), temperature=cfg.get("temperature", 0.7),
                                           max_tokens=1100, verbose=False))
    if not res:
        return None, None, 0
    tokens = sum(getattr(r, "token_count", 0) for r in res)
    return np.concatenate([np.asarray(r.audio, dtype=np.float32) for r in res]), res[0].sample_rate, tokens


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("out")
    ap.add_argument("--voice", required=True)
    ap.add_argument("--sample", help="speak this text instead of the brief (to audition a voice)")
    a = ap.parse_args()
    cfg = json.load(open(a.voice))
    model_dir = os.path.join(RUNTIME, cfg["model"])
    if not os.path.exists(os.path.join(model_dir, "config.json")):
        raise SystemExit("model missing at %s (downloads are off here)" % model_dir)
    os.makedirs(a.out, exist_ok=True)
    mx.set_memory_limit(8 * 1024 ** 3)
    mx.set_cache_limit(128 * 1024 ** 2)
    t0 = time.monotonic()
    model = load_model(model_dir)

    if a.sample:
        plan = [("sample", [a.sample])]
    else:
        b = json.load(open(a.brief, encoding="utf-8"))
        paras = [p.strip() for p in re.split(r"\n\s*\n", b["script"]) if p.strip()]
        starts = {c["start_text"].strip(): c["id"] for c in b.get("chapters", [])}
        plan, cur = [], ("intro", [])
        for p in paras:
            cid = next((v for k, v in starts.items() if p.startswith(k)), None)
            if cid:
                if cur[1]:
                    plan.append(cur)
                cur = (cid, [])
            cur[1].append(p)
        plan.append(cur)

    parts, sr, segs, chapters, t = [], None, [], {}, 0.0
    for ci, (cid, paras) in enumerate(plan):
        if ci:
            parts.append(np.zeros(int(sr * PAUSE["chapter"]), np.float32))
            t += PAUSE["chapter"]
        chapters[cid] = round(t, 2)
        for pi, para in enumerate(paras):
            if pi:
                parts.append(np.zeros(int(sr * PAUSE["paragraph"]), np.float32))
                t += PAUSE["paragraph"]
            for ki, text in enumerate(chunks(para)):
                if ki:
                    parts.append(np.zeros(int(sr * PAUSE["sentence"]), np.float32))
                    t += PAUSE["sentence"]
                start = time.monotonic()
                for attempt in range(3):
                    audio, sr_, tokens = synth(model, cfg, text, 42 + attempt)
                    problem = "empty" if audio is None else ("hit token limit" if tokens >= 1100 else qa(audio, sr_, text))
                    if not problem:
                        break
                    mx.clear_cache()
                if problem:
                    raise SystemExit("segment failed QA after 3 tries (%s): %s" % (problem, text[:80]))
                sr = sr_
                parts.append(audio)
                segs.append({"chapter": cid, "text": text, "seconds": round(len(audio) / sr, 2), "tries": attempt + 1,
                             "gen_seconds": round(time.monotonic() - start, 1)})
                t += len(audio) / sr
                mx.clear_cache()
                with open(os.path.join(a.out, "segments.json"), "w") as f:
                    json.dump(segs, f, indent=0)

    audio = np.concatenate(parts)
    # loudness: bring speech RMS to about -20 dBFS, peaks capped at -1 dBFS (no speed change, no compression)
    rms = float(np.sqrt(np.mean(np.square(audio[np.abs(audio) > 0.01])))) or 1e-6
    audio = audio * min(0.1 / rms, 0.89 / float(np.max(np.abs(audio))))
    wav = os.path.join(a.out, "episode.wav")
    sf.write(wav, audio, sr)
    m4a = os.path.join(a.out, "episode.m4a")
    subprocess.run(["/usr/bin/afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", "-c", "1", wav, m4a],
                   check=True, capture_output=True)
    info = {"seconds": round(len(audio) / sr, 1), "took": round(time.monotonic() - t0, 1), "chapters": chapters,
            "segments": len(segs), "retries": sum(s["tries"] - 1 for s in segs), "speaker": cfg["speaker"],
            "model": cfg["model"], "m4a_bytes": os.path.getsize(m4a)}
    with open(os.path.join(a.out, "episode.json"), "w") as f:
        json.dump(info, f, indent=1)
    print(json.dumps(info))


if __name__ == "__main__":
    main()
