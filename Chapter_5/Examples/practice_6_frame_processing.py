# practice_6: Frame Processing Pipeline (audio & video)
# Chapter_5 / Docs_5_4 companion example.
#
# Pipeline A (audio): load (soundfile)
#           -> low-pass filter (scipy butter, 2 kHz cutoff)
#           -> time stretch 0.75x (librosa) -> pitch shift +3 semitones
#           -> write wav -> before/after comparison figure.
#
# Pipeline B (video): decode practice_5 test video (opencv)
#           -> per-frame: HSV saturation boost x1.4 -> gaussian blur
#              -> unsharp mask sharpen
#           -> write processed mp4 -> side-by-side comparison figure.
#
# Run from anywhere:  python practice_6_frame_processing.py
# Outputs: Chapter_5/Examples/practice_6_audio_processed.wav
#          Chapter_5/Examples/practice_6_video_processed.mp4
# Figures: Chapter_5/Pictures/practice_6_*.png

import time
import numpy as np
import soundfile as sf
import librosa
import cv2
from scipy.signal import butter, sosfiltfilt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_AUDIO = ROOT / "Chapter_1" / "Examples" / "A440_instruments_A4.wav"
SRC_VIDEO = ROOT / "Chapter_5" / "Examples" / "practice_5_test_video.mp4"
OUT_AUDIO = ROOT / "Chapter_5" / "Examples" / "practice_6_audio_processed.wav"
OUT_VIDEO = ROOT / "Chapter_5" / "Examples" / "practice_6_video_processed.mp4"
OUT_DIR = ROOT / "Chapter_5" / "Pictures"

LOWPASS_HZ = 2000.0
STRETCH_RATE = 0.75      # < 1 : slower & longer
PITCH_STEPS = 3          # semitones up
SAT_GAIN = 1.4
BLUR_KSIZE = 5
SHARPEN_AMOUNT = 0.8


# ---------------------------------------------------------------------------
# Pipeline A: audio frame processing
# ---------------------------------------------------------------------------
def process_audio():
    y, sr = sf.read(str(SRC_AUDIO), dtype="float32")
    if y.ndim > 1:
        y = y.mean(axis=1)

    sos = butter(6, LOWPASS_HZ, btype="low", fs=sr, output="sos")
    y_lp = sosfiltfilt(sos, y).astype(np.float32)
    y_slow = librosa.effects.time_stretch(y_lp, rate=STRETCH_RATE)
    y_out = librosa.effects.pitch_shift(y_slow, sr=sr, n_steps=PITCH_STEPS)
    sf.write(str(OUT_AUDIO), y_out, sr)

    stats = {
        "sr": sr,
        "dur_in": len(y) / sr, "dur_out": len(y_out) / sr,
        "rms_in": float(np.sqrt(np.mean(y ** 2))),
        "rms_lp": float(np.sqrt(np.mean(y_lp ** 2))),
        "rms_out": float(np.sqrt(np.mean(y_out ** 2))),
    }
    return y, y_out, sr, stats


def fig_audio_compare(y_in, y_out, sr):
    """Fig: waveform + mel-spectrogram before/after the audio pipeline."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.6))
    for col, (y, name) in enumerate([(y_in, "Original"), (y_out, "Processed")]):
        t = np.arange(len(y)) / sr
        step = max(1, len(y) // 4000)
        axes[0, col].plot(t[::step], y[::step], lw=0.4, color="#3366aa")
        axes[0, col].set_title("%s waveform (%.1fs)" % (name, len(y) / sr), fontsize=10)
        axes[0, col].set_xlabel("time (s)")
        axes[0, col].set_ylim(-1, 1)
        s = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=256)
        db = librosa.power_to_db(s, ref=np.max)
        img = axes[1, col].imshow(db, origin="lower", aspect="auto", cmap="magma",
                                  extent=[0, len(y) / sr, 0, sr / 2], vmin=-80, vmax=0)
        axes[1, col].set_ylim(0, 8000)
        axes[1, col].set_title("%s mel spectrogram" % name, fontsize=10)
        axes[1, col].set_xlabel("time (s)")
        axes[1, col].set_ylabel("frequency (Hz)")
    fig.suptitle("Audio pipeline: low-pass 2kHz -> 0.75x time stretch -> +3 semitones")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "practice_6_audio_compare.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Pipeline B: video frame processing
# ---------------------------------------------------------------------------
def process_frame(frame):
    """saturation boost in HSV -> gaussian blur -> unsharp mask."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * SAT_GAIN, 0, 255)
    out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    blur = cv2.GaussianBlur(out, (BLUR_KSIZE, BLUR_KSIZE), 0)
    return cv2.addWeighted(out, 1.0 + SHARPEN_AMOUNT, blur, -SHARPEN_AMOUNT, 0)


def process_video():
    cap = cv2.VideoCapture(str(SRC_VIDEO))
    if not cap.isOpened():
        raise RuntimeError("VideoCapture failed to open: %s" % SRC_VIDEO)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(OUT_VIDEO), fourcc, fps, (w, h))

    n_frames, t0 = 0, time.perf_counter()
    picks = {}
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        processed = process_frame(frame)
        writer.write(processed)
        if n_frames in (60, 180, 300):
            picks[n_frames] = (frame.copy(), processed.copy())
        n_frames += 1
    cap.release()
    writer.release()
    elapsed = time.perf_counter() - t0
    stats = {"fps": fps, "frames": n_frames, "w": w, "h": h,
             "elapsed": elapsed, "ms_per_frame": elapsed / n_frames * 1000}
    return picks, stats


def fig_video_compare(picks):
    """Fig: original vs processed frames, one row per picked frame."""
    rows = sorted(picks.keys())
    fig, axes = plt.subplots(len(rows), 2, figsize=(9, 3.0 * len(rows)))
    for r, idx in enumerate(rows):
        orig, proc = picks[idx]
        axes[r, 0].imshow(cv2.cvtColor(orig, cv2.COLOR_BGR2RGB))
        axes[r, 0].set_title("frame %d original" % idx, fontsize=10)
        axes[r, 1].imshow(cv2.cvtColor(proc, cv2.COLOR_BGR2RGB))
        axes[r, 1].set_title("frame %d processed (sat x%.1f -> blur -> sharpen)"
                             % (idx, SAT_GAIN), fontsize=10)
        for c in range(2):
            axes[r, c].axis("off")
    fig.suptitle("Video pipeline: per-frame HSV saturation -> gaussian blur -> unsharp mask")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "practice_6_video_compare.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 64)
    print("[A] audio frame processing")
    y_in, y_out, sr, a = process_audio()
    print("    input : %s (%.2fs @ %dHz)"
          % (SRC_AUDIO.relative_to(ROOT), a["dur_in"], a["sr"]))
    print("    chain : low-pass %dHz (butter6) -> time_stretch x%.2f -> pitch %+d st"
          % (LOWPASS_HZ, STRETCH_RATE, PITCH_STEPS))
    print("    output: %s (%.2fs)"
          % (OUT_AUDIO.relative_to(ROOT), a["dur_out"]))
    print("    RMS   : in=%.4f  after lowpass=%.4f  final=%.4f"
          % (a["rms_in"], a["rms_lp"], a["rms_out"]))
    fig_audio_compare(y_in, y_out, sr)

    print("[B] video frame processing")
    picks, v = process_video()
    print("    input : %s (%dx%d @ %.0ffps)"
          % (SRC_VIDEO.relative_to(ROOT), v["w"], v["h"], v["fps"]))
    print("    chain : HSV saturation x%.1f -> gaussian %dx%d -> unsharp %.1f"
          % (SAT_GAIN, BLUR_KSIZE, BLUR_KSIZE, SHARPEN_AMOUNT))
    print("    output: %s" % OUT_VIDEO.relative_to(ROOT))
    print("    perf  : %d frames in %.2fs (%.2f ms/frame)"
          % (v["frames"], v["elapsed"], v["ms_per_frame"]))
    fig_video_compare(picks)

    print("=" * 64)
    print("figures written to %s:" % OUT_DIR.relative_to(ROOT))
    for name in ["practice_6_audio_compare.png", "practice_6_video_compare.png"]:
        print("    %s" % name)
    print("done.")


if __name__ == "__main__":
    main()
