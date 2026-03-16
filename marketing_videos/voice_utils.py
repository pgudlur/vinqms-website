"""
Shared voiceover + sitar background music + video muxing utilities.
Uses edge-tts (Microsoft Neural TTS) for narration.
Generates a gentle sitar drone via sine wave synthesis for background.
"""

import asyncio
import json
import math
import os
import struct
import subprocess
import tempfile
import wave
import edge_tts

VOICE = "en-US-AndrewNeural"   # Warm, confident, professional
RATE  = "-2%"                   # Slightly slower for clarity

# ── Audio fade parameters (seconds) ──
FADE_IN  = 0.15
FADE_OUT = 0.30

# ── Sitar parameters ──
SITAR_VOLUME = 0.06   # Very gentle background (6% volume)
SAMPLE_RATE  = 44100


def _generate_sitar_wav(duration: float, output_path: str):
    """Generate a gentle sitar-like drone using additive sine synthesis.

    Creates a warm, meditative Indian instrument sound using:
    - Sa (root) + Pa (fifth) + upper Sa drone tones
    - Sympathetic string harmonics
    - Slow amplitude modulation for organic feel
    """
    n_samples = int(SAMPLE_RATE * duration)

    # Sitar drone frequencies (key of D, common sitar tuning)
    sa_freq   = 146.83   # D3 — root drone
    pa_freq   = 220.00   # A3 — fifth drone
    sa_hi     = 293.66   # D4 — upper octave
    tanpura_1 = 440.00   # A4 — sympathetic
    tanpura_2 = 587.33   # D5 — high sympathetic

    samples = []
    for i in range(n_samples):
        t = i / SAMPLE_RATE

        # Slow breathing modulation (organic swell)
        mod1 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.08 * t)    # ~8s cycle
        mod2 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.12 * t + 1.2)  # ~8.3s
        mod3 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.05 * t + 2.5)  # ~20s

        # Very subtle vibrato on main tones (sitar meend effect)
        vib = math.sin(2 * math.pi * 4.5 * t) * 0.8  # 4.5 Hz vibrato

        # Main drone tones with harmonics (sitar has rich overtones)
        sa  = math.sin(2 * math.pi * (sa_freq + vib * 0.3) * t)
        sa2 = math.sin(2 * math.pi * (sa_freq * 2.01) * t) * 0.3  # Slight detuning
        sa3 = math.sin(2 * math.pi * (sa_freq * 3.0) * t) * 0.12

        pa  = math.sin(2 * math.pi * (pa_freq + vib * 0.4) * t) * 0.6
        pa2 = math.sin(2 * math.pi * (pa_freq * 2.0) * t) * 0.18

        hi  = math.sin(2 * math.pi * sa_hi * t) * 0.25 * mod2

        # Sympathetic strings (very quiet, shimmering)
        sym1 = math.sin(2 * math.pi * tanpura_1 * t) * 0.08 * mod3
        sym2 = math.sin(2 * math.pi * tanpura_2 * t) * 0.04 * mod3

        # Buzz/jivari effect — signature sitar sound via clipped waveform
        buzz_raw = math.sin(2 * math.pi * sa_freq * t)
        buzz = max(-0.6, min(0.6, buzz_raw * 1.5)) * 0.15

        # Combine
        sample = (sa + sa2 + sa3 + pa + pa2 + hi + sym1 + sym2 + buzz) * mod1

        # Fade in/out for smoothness
        fade_sec = 3.0
        if t < fade_sec:
            sample *= t / fade_sec
        elif t > duration - fade_sec:
            sample *= (duration - t) / fade_sec

        # Normalize and apply volume
        sample = sample * SITAR_VOLUME * 0.5
        sample = max(-1.0, min(1.0, sample))
        samples.append(sample)

    # Write WAV
    with wave.open(output_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for s in samples:
            wf.writeframes(struct.pack('<h', int(s * 32767)))

    print(f"  Sitar track generated: {duration:.1f}s")


async def _generate_segment(text: str, outpath: str):
    """Generate a single TTS audio segment."""
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(outpath)


def _get_audio_duration(path: str) -> float:
    """Get the duration of an audio file in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return 5.0
    info = json.loads(result.stdout)
    return float(info.get("format", {}).get("duration", 5.0))


def generate_voiceover_segments(segments: list, output_dir: str) -> list:
    """Generate TTS audio for each segment."""
    paths = []
    for i, (text, _, _) in enumerate(segments):
        path = os.path.join(output_dir, f"segment_{i:02d}.mp3")
        asyncio.run(_generate_segment(text, path))
        paths.append(path)
        print(f"  VO segment {i}: {path}")
    return paths


def create_voiceover_track(segments: list, total_duration: float, output_path: str):
    """Create a single audio track from timed voiceover segments."""
    tmpdir = tempfile.mkdtemp(prefix="vinmkt_vo_")

    print("Generating voiceover segments...")
    seg_paths = generate_voiceover_segments(segments, tmpdir)

    inputs = []
    filter_parts = []

    # Silence base track
    inputs.extend([
        "-f", "lavfi", "-t", str(total_duration),
        "-i", "anullsrc=r=44100:cl=mono"
    ])

    for i, (seg_path, (_, start_sec, _)) in enumerate(zip(seg_paths, segments)):
        inputs.extend(["-i", seg_path])
        seg_dur = _get_audio_duration(seg_path)

        if i < len(segments) - 1:
            next_start = segments[i + 1][1]
            if start_sec + seg_dur > next_start - 0.5:
                print(f"  [WARN] Segment {i}: audio {seg_dur:.1f}s "
                      f"(ends ~{start_sec + seg_dur:.1f}s) may overlap "
                      f"next segment at {next_start}s")

        fade_out_start = max(0, seg_dur - FADE_OUT)
        delay_ms = int(start_sec * 1000)

        filter_parts.append(
            f"[{i+1}]"
            f"afade=t=in:st=0:d={FADE_IN},"
            f"afade=t=out:st={fade_out_start:.3f}:d={FADE_OUT},"
            f"adelay={delay_ms}|{delay_ms}"
            f"[s{i}]"
        )

    n_inputs = len(seg_paths) + 1
    mix_inputs = "[0]" + "".join(f"[s{i}]" for i in range(len(seg_paths)))
    filter_parts.append(
        f"{mix_inputs}amix=inputs={n_inputs}:duration=longest"
        f":dropout_transition=2[mixed];"
        f"[mixed]volume={n_inputs}[out]"
    )

    filter_str = ";".join(filter_parts)

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_str,
        "-map", "[out]",
        "-ac", "1", "-ar", "44100",
        "-b:a", "192k",
        output_path
    ]

    print("Mixing voiceover track...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg mix error: {result.stderr[-500:]}")
        raise RuntimeError("Failed to mix voiceover track")

    for p in seg_paths:
        try: os.remove(p)
        except OSError: pass
    try: os.rmdir(tmpdir)
    except OSError: pass

    print(f"Voiceover track saved: {output_path}")


def mux_video_audio_with_music(video_path: str, vo_path: str,
                                output_path: str, duration: float):
    """Combine video + voiceover + sitar background music.

    Generates sitar drone, mixes with voiceover (sitar ducks under speech),
    then muxes with video.
    """
    tmpdir = tempfile.mkdtemp(prefix="vinmkt_mux_")
    sitar_path = os.path.join(tmpdir, "sitar.wav")
    mixed_audio = os.path.join(tmpdir, "mixed_audio.mp3")

    print("Generating sitar background...")
    _generate_sitar_wav(duration, sitar_path)

    # Mix voiceover + sitar: sitar at low volume, VO at full
    cmd = [
        "ffmpeg", "-y",
        "-i", vo_path,
        "-i", sitar_path,
        "-filter_complex",
        "[0]volume=1.0[vo];"
        "[1]volume=0.4[sitar];"  # Extra attenuation on sitar
        "[vo][sitar]amix=inputs=2:duration=longest:dropout_transition=3[out]",
        "-map", "[out]",
        "-ac", "1", "-ar", "44100",
        "-b:a", "192k",
        mixed_audio
    ]

    print("Mixing voiceover + sitar...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg sitar mix error: {result.stderr[-500:]}")
        # Fallback: use voiceover only
        mixed_audio = vo_path

    # Final mux
    cmd2 = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", mixed_audio,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    print(f"Muxing final video -> {output_path}")
    result2 = subprocess.run(cmd2, capture_output=True, text=True)
    if result2.returncode != 0:
        print(f"FFmpeg mux error: {result2.stderr[-500:]}")
        raise RuntimeError("Failed to mux video and audio")

    # Cleanup
    for f in [sitar_path, mixed_audio]:
        try: os.remove(f)
        except OSError: pass
    try: os.rmdir(tmpdir)
    except OSError: pass

    print(f"Final video saved: {output_path}")


def mux_video_audio(video_path: str, audio_path: str, output_path: str):
    """Legacy: Combine video + audio without background music."""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    print(f"Muxing video + audio -> {output_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FFmpeg mux error: {result.stderr[-500:]}")
        raise RuntimeError("Failed to mux video and audio")
    print(f"Final video saved: {output_path}")
