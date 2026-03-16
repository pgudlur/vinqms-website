"""Measure actual TTS durations for all 4 marketing videos and report overlaps."""
import asyncio
import json
import os
import subprocess
import tempfile
import edge_tts
import importlib
import sys

sys.path.insert(0, os.path.dirname(__file__))

VOICE = "en-US-AndrewNeural"
RATE = "-2%"

async def gen(text, path):
    c = edge_tts.Communicate(text, VOICE, rate=RATE)
    await c.save(path)

def duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True)
    return float(json.loads(r.stdout).get("format", {}).get("duration", 0))

VIDEO_FILES = [
    "video1_vinquality_overview",
    "video2_vinquality_modules",
    "video3_vinfmea_overview",
    "video4_vinfmea_controlplans",
]

tmpdir = tempfile.mkdtemp(prefix="vo_check_")
issues = []

for vf in VIDEO_FILES:
    mod = importlib.import_module(vf)
    segs = mod.VO_SEGMENTS
    vid_dur = mod.DURATION

    print(f"\n{'='*60}")
    print(f"  {vf}  (DURATION={vid_dur}s, {len(segs)} segments)")
    print(f"{'='*60}")

    for i, (text, start, end) in enumerate(segs):
        mp3 = os.path.join(tmpdir, f"{vf}_s{i}.mp3")
        asyncio.run(gen(text, mp3))
        dur = duration(mp3)
        audio_end = start + dur

        overlap = ""
        if i < len(segs) - 1:
            next_start = segs[i + 1][1]
            gap = next_start - audio_end
            if gap < 0.5:
                overlap = f"  *** OVERLAP by {-gap:.1f}s ***" if gap < 0 else f"  *** GAP ONLY {gap:.1f}s ***"
                issues.append((vf, i, start, dur, audio_end, next_start, gap))
        else:
            if audio_end > vid_dur:
                overlap = f"  *** EXCEEDS VIDEO by {audio_end - vid_dur:.1f}s ***"
                issues.append((vf, i, start, dur, audio_end, vid_dur, vid_dur - audio_end))

        print(f"  Seg {i}: start={start:.1f}s  TTS={dur:.1f}s  ends={audio_end:.1f}s{overlap}")
        os.remove(mp3)

print(f"\n{'='*60}")
print(f"  SUMMARY: {len(issues)} issues found")
print(f"{'='*60}")
for vf, i, start, dur, audio_end, next_start, gap in issues:
    print(f"  {vf} seg {i}: audio ends {audio_end:.1f}s, "
          f"next at {next_start:.1f}s, gap={gap:.1f}s")

os.rmdir(tmpdir)
