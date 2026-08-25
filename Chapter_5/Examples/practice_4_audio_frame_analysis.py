# practice_4: Audio Frame Analysis Pipeline
# Chapter_5 / Docs_5_2 companion example.
#
# Pipeline: load (soundfile) -> frame blocking & windowing (numpy, hand-written)
#           -> feature extraction (librosa) -> pitch/onset tracking -> report figures.
#
# Run from anywhere:  python practice_4_audio_frame_analysis.py
# Outputs are written to Chapter_5/Pictures/practice_4_result_*.png

import numpy as np
import soundfile as sf
import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_STANDARD = ROOT / "Chapter_1" / "Examples" / "A440_standard_A4.wav"
SRC_INSTRUMENT = ROOT / "Chapter_1" / "Examples" / "A440_instruments_A4.wav"
OUT_DIR = ROOT / "Chapter_5" / "Pictures"

FRAME_LEN = 1024          # ~23.2 ms @ 44.1 kHz, inside the 20-40 ms convention
HOP_LEN = FRAME_LEN // 2  # 50% overlap


def load_mono(path):
    """Read an audio file and downmix to mono float32 in [-1, 1]."""
    data, sr = sf.read(str(path), dtype="float32")
    if data.ndim > 1:
        data = data.mean(axis=1)
    return data, sr


def frame_blocking(y, frame_len, hop_len):
    """Split a 1-D signal into overlapping frames: (n_frames, frame_len)."""
    n_frames = 1 + (len(y) - frame_len) // hop_len
    idx = np.arange(frame_len)[None, :] + hop_len * np.arange(n_frames)[:, None]
    return y[idx]


def mag_db(frame, sr):
    """Single-sided magnitude spectrum in dB of one windowed frame."""
    spec = np.abs(np.fft.rfft(frame))
    spec = spec / (len(frame) / 2)
    freqs = np.fft.rfftfreq(len(frame), d=1.0 / sr)
    return freqs, 20.0 * np.log10(spec + 1e-12)


def demo_windowing(y, sr):
    """Fig 0: rectangular vs Hann window on one frame -> spectral leakage."""
    center = int(sr * 1.0)  # frame starting at t = 1.0 s
    frame = y[center:center + FRAME_LEN]
    rect = np.ones(FRAME_LEN)
    hann = np.hanning(FRAME_LEN)

    f_r, db_r = mag_db(frame * rect, sr)
    f_h, db_h = mag_db(frame * hann, sr)

    fig, axes = plt.subplots(2, 1, figsize=(9, 6))
    t = np.arange(FRAME_LEN) / sr * 1000.0
    axes[0].plot(t, frame, color="0.4", lw=0.8, label="Frame (t=1.0s)")
    axes[0].plot(t, frame * hann, color="tab:red", lw=0.8, label="After Hann window")
    axes[0].set_title("Frame Blocking & Windowing (frame=1024, hop=512)")
    axes[0].set_xlabel("Time (ms)")
    axes[0].set_ylabel("Amplitude")
    axes[0].legend(loc="upper right")

    axes[1].plot(f_r, db_r, color="0.4", lw=0.9, label="Rectangular window")
    axes[1].plot(f_h, db_h, color="tab:red", lw=0.9, label="Hann window")
    axes[1].set_xlim(0, 2000)
    axes[1].set_ylim(-80, 10)
    axes[1].set_title("Spectral Leakage: Rectangular vs Hann")
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Magnitude (dB)")
    axes[1].legend(loc="upper right")

    fig.tight_layout()
    out = OUT_DIR / "practice_4_result_0.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def demo_features(y, sr):
    """Fig 1: short-time RMS / ZCR / spectral centroid curves."""
    rms = librosa.feature.rms(y=y, frame_length=FRAME_LEN, hop_length=HOP_LEN)[0]
    zcr = librosa.feature.zero_crossing_rate(y=y, frame_length=FRAME_LEN, hop_length=HOP_LEN)[0]
    cent = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=FRAME_LEN, hop_length=HOP_LEN)[0]
    times = librosa.times_like(rms, sr=sr, hop_length=HOP_LEN)

    fig, axes = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
    axes[0].plot(times, rms, color="tab:blue", lw=0.9)
    axes[0].set_title("Short-Time RMS (loudness cue)")
    axes[0].set_ylabel("RMS")
    axes[1].plot(times, zcr, color="tab:green", lw=0.9)
    axes[1].set_title("Zero-Crossing Rate (noisiness cue)")
    axes[1].set_ylabel("ZCR")
    axes[2].plot(times, cent, color="tab:purple", lw=0.9)
    axes[2].set_title("Spectral Centroid (brightness cue)")
    axes[2].set_ylabel("Hz")
    axes[2].set_xlabel("Time (s)")

    fig.suptitle("Time/Frequency Domain Features - A440 instruments A4")
    fig.tight_layout()
    out = OUT_DIR / "practice_4_result_1.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def demo_pitch_chroma(y_std, y_ins, sr):
    """Fig 2: pitch track of the standard A4 + chroma of the instrument take."""
    y_seg = y_std[: sr * 8]  # first 8 s is enough for a stable pitch track
    f0, voiced, _ = librosa.pyin(
        y_seg, fmin=100, fmax=1000, sr=sr,
        frame_length=FRAME_LEN * 2, hop_length=HOP_LEN,
    )
    t_f0 = librosa.times_like(f0, sr=sr, hop_length=HOP_LEN)

    chroma = librosa.feature.chroma_stft(y=y_ins, sr=sr, n_fft=FRAME_LEN * 2, hop_length=HOP_LEN)

    fig, axes = plt.subplots(2, 1, figsize=(9, 7))
    axes[0].plot(t_f0, f0, color="tab:red", lw=1.2, label="pyin pitch track")
    axes[0].axhline(440.0, color="0.3", ls="--", lw=0.9, label="A4 = 440 Hz")
    axes[0].set_ylim(300, 600)
    axes[0].set_title("Pitch Tracking - A440 standard A4")
    axes[0].set_ylabel("Frequency (Hz)")
    axes[0].legend(loc="upper right")

    img = librosa.display.specshow(
        chroma, x_axis="time", y_axis="chroma", sr=sr, hop_length=HOP_LEN, ax=axes[1],
    )
    axes[1].set_title("Chroma Features - A440 instruments A4")
    fig.colorbar(img, ax=axes[1], format="%0.2f")

    fig.tight_layout()
    out = OUT_DIR / "practice_4_result_2.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)

    voiced_f0 = f0[~np.isnan(f0)]
    return out, float(np.median(voiced_f0)), float(np.mean(voiced))


def demo_frame_schematic(y, sr):
    """Schematic: overlapping frame blocking on a waveform segment."""
    seg = y[: int(sr * 0.12)]  # 120 ms excerpt
    t = np.arange(len(seg)) / sr * 1000.0

    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(t, seg, color="0.35", lw=0.9)

    n_show = 5
    for m in range(n_show):
        s = m * HOP_LEN
        e = s + FRAME_LEN
        if e > len(seg):
            break
        ax.plot([t[s], t[e], t[e], t[s], t[s]],
                [-0.14, -0.14, -0.19 - 0.02 * m, -0.19 - 0.02 * m, -0.14],
                color="tab:red", lw=1.0)
        ax.annotate(f"frame {m}", xy=((t[s] + t[e]) / 2, -0.155 - 0.02 * m),
                    ha="center", fontsize=8, color="tab:red")
    ax.annotate("", xy=(t[HOP_LEN], 0.13), xytext=(t[0], 0.13),
                arrowprops=dict(arrowstyle="->", color="tab:blue"))
    ax.text(t[HOP_LEN // 2], 0.145, "hop", ha="center", fontsize=8, color="tab:blue")
    ax.annotate("", xy=(t[FRAME_LEN], -0.115), xytext=(t[0], -0.115),
                arrowprops=dict(arrowstyle="<->", color="tab:blue"))
    ax.text(t[FRAME_LEN // 2], -0.108, "frame length", ha="center", fontsize=8, color="tab:blue")

    ax.set_ylim(-0.3, 0.17)
    ax.set_title("Frame Blocking with 50% Overlap (frame=1024, hop=512, fs=44.1kHz)")
    ax.set_xlabel("Time (ms)")
    ax.set_yticks([])
    fig.tight_layout()
    out = OUT_DIR / "practice_4_frame_blocking.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    y_std, sr = load_mono(SRC_STANDARD)
    y_ins, _ = load_mono(SRC_INSTRUMENT)

    # sanity of the hand-written frame blocking
    frames = frame_blocking(y_std, FRAME_LEN, HOP_LEN)
    print(f"[frames] standard A4 -> {frames.shape[0]} frames x {frames.shape[1]} samples "
          f"({FRAME_LEN / sr * 1000:.1f} ms frame, {HOP_LEN / sr * 1000:.1f} ms hop)")

    p0 = demo_windowing(y_std, sr)
    p1 = demo_features(y_ins, sr)
    p2, f0_med, voiced_ratio = demo_pitch_chroma(y_std, y_ins, sr)
    ps = demo_frame_schematic(y_std, sr)

    # numeric summary for the text
    peak_frame = frames[frames.shape[0] // 2] * np.hanning(FRAME_LEN)
    freqs, db = mag_db(peak_frame, sr)
    peak_hz = float(freqs[int(np.argmax(db))])

    tempo, beats = librosa.beat.beat_track(y=y_ins, sr=sr, hop_length=HOP_LEN)
    tempo_val = float(np.atleast_1d(tempo)[0])

    print(f"[figure] {ps.name}, {p0.name}, {p1.name}, {p2.name} -> {OUT_DIR}")
    print(f"[verify] FFT peak of one frame : {peak_hz:.1f} Hz")
    print(f"[verify] pyin median pitch     : {f0_med:.2f} Hz (voiced {voiced_ratio * 100:.0f}%)")
    print(f"[verify] beat track tempo      : {tempo_val:.1f} BPM, {len(beats)} beats")


if __name__ == "__main__":
    main()
