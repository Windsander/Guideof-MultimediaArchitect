# practice_5: Video Frame Analysis Pipeline
# Chapter_5 / Docs_5_3 companion example.
#
# Pipeline: synthesize a deterministic 3-scene test video (opencv)
#           -> decode & inspect (VideoCapture, fps/PTS/resolution)
#           -> frame representation (RGB vs YUV channels)
#           -> inter-frame analysis (frame difference -> scene-cut detection,
#              Farneback dense optical flow -> motion field)
#           -> moving-target tracking (motion blob centroid trajectory)
#           -> report figures.
#
# Run from anywhere:  python practice_5_video_frame_analysis.py
# Video  is written to Chapter_5/Examples/practice_5_test_video.mp4
# Figures are written to Chapter_5/Pictures/practice_5_*.png

import numpy as np
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VIDEO_PATH = ROOT / "Chapter_5" / "Examples" / "practice_5_test_video.mp4"
OUT_DIR = ROOT / "Chapter_5" / "Pictures"

WIDTH, HEIGHT = 640, 360
FPS = 30
SCENE_LEN = 4                       # seconds per scene
N_SCENES = 3
TOTAL_FRAMES = FPS * SCENE_LEN * N_SCENES   # 360
CUTS_GT = [FPS * SCENE_LEN, FPS * SCENE_LEN * 2]  # hard cuts at frame 120 / 240

rng = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# 1. Test-video synthesis: three scenes with distinct motion signatures
# ---------------------------------------------------------------------------
def scene_a(t):
    """Dark-blue gradient background, one white circle on a sine path."""
    x = np.linspace(0, 1, WIDTH, dtype=np.float32)[None, :]
    y = np.linspace(0, 1, HEIGHT, dtype=np.float32)[:, None]
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    frame[..., 0] = 0.55 + 0.25 * x            # B channel gradient
    frame[..., 1] = 0.15 + 0.10 * y
    frame[..., 2] = 0.10
    cx = int(WIDTH * (0.15 + 0.7 * (t / SCENE_LEN)))
    cy = int(HEIGHT * (0.5 + 0.3 * np.sin(2 * np.pi * t / SCENE_LEN)))
    cv2.circle(frame, (cx, cy), 28, (1.0, 1.0, 1.0), -1)
    return frame


def scene_b(t):
    """Warm background, two rectangles: one drifting, one bouncing."""
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    frame[..., 0] = 0.12
    frame[..., 1] = 0.25
    frame[..., 2] = 0.60
    x1 = int(WIDTH * (0.75 - 0.5 * (t / SCENE_LEN)))
    cv2.rectangle(frame, (x1, 60), (x1 + 70, 130), (0.2, 0.9, 0.9), -1)
    period = 1.2
    phase = (t % period) / period
    y2 = int(HEIGHT * (0.15 + 0.6 * (1.0 - abs(2 * phase - 1.0))))
    cv2.rectangle(frame, (430, y2), (500, y2 + 70), (0.9, 0.5, 0.2), -1)
    return frame


def scene_c(t):
    """Black background, one small square on a fast diagonal dash."""
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    cx = int((WIDTH * 1.4 * (t / SCENE_LEN) + 40) % (WIDTH + 80)) - 40
    cy = int((HEIGHT * 0.8 * (t / SCENE_LEN) + 30) % HEIGHT)
    cv2.rectangle(frame, (cx, cy), (cx + 40, cy + 40), (0.9, 0.9, 0.9), -1)
    return frame


SCENES = [scene_a, scene_b, scene_c]


def synthesize_video(path):
    """Render the three scenes into one mp4 with hard cuts; slight sensor noise."""
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, FPS, (WIDTH, HEIGHT))
    if not writer.isOpened():
        raise RuntimeError("VideoWriter failed to open: %s" % path)
    for i in range(TOTAL_FRAMES):
        scene_idx = i // (FPS * SCENE_LEN)
        t = (i % (FPS * SCENE_LEN)) / FPS
        frame = SCENES[scene_idx](t)
        frame += rng.normal(0.0, 0.012, frame.shape).astype(np.float32)  # sensor noise
        writer.write((np.clip(frame, 0, 1) * 255).astype(np.uint8))
    writer.release()
    return path


# ---------------------------------------------------------------------------
# 2. Decode & inspect
# ---------------------------------------------------------------------------
def decode_all(path):
    """Read every frame back into a uint8 BGR array plus per-frame PTS (ms)."""
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise RuntimeError("VideoCapture failed to open: %s" % path)
    fps_read = cap.get(cv2.CAP_PROP_FPS)
    frames, pts_ms = [], []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        pts_ms.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        frames.append(frame)
    cap.release()
    return np.stack(frames), np.array(pts_ms), fps_read


def gray_f(frames, i):
    """i-th frame as float32 grayscale in [0, 1]."""
    return cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0


# ---------------------------------------------------------------------------
# 3. Figures
# ---------------------------------------------------------------------------
def fig_timeline(frames):
    """Fig: montage around the two hard cuts + one frame per scene."""
    picks = [(60, "Scene A  t=2.00s"),
             (119, "Scene A  last frame (119)"),
             (120, "Scene B  first frame (120)  <- hard cut"),
             (180, "Scene B  t=6.00s"),
             (239, "Scene B  last frame (239)"),
             (240, "Scene C  first frame (240)  <- hard cut")]
    fig, axes = plt.subplots(2, 3, figsize=(11, 5.6))
    for ax, (idx, title) in zip(axes.ravel(), picks):
        ax.imshow(cv2.cvtColor(frames[idx], cv2.COLOR_BGR2RGB))
        ax.set_title(title, fontsize=9)
        ax.axis("off")
    fig.suptitle("Test video timeline: 3 scenes, hard cuts at frame 120 / 240")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "practice_5_video_timeline.png", dpi=130)
    plt.close(fig)


def fig_yuv_decompose(frames):
    """Fig: one frame decomposed into R/G/B and Y/U/V channels."""
    frame = frames[150]  # inside scene B
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    panels = [("Original (RGB display)", rgb, None),
              ("R", rgb[..., 0], "gray"), ("G", rgb[..., 1], "gray"),
              ("B", rgb[..., 2], "gray"),
              ("Y (luma)", yuv[..., 0], "gray"),
              ("U (Cb)", yuv[..., 1], "gray"), ("V (Cr)", yuv[..., 2], "gray")]
    fig, axes = plt.subplots(2, 4, figsize=(11, 5.4))
    axes[0, 0].imshow(rgb)
    axes[0, 0].set_title("Original (RGB display)", fontsize=9)
    axes[0, 0].axis("off")
    axes[1, 0].axis("off")
    for ax, (title, ch, cmap) in zip([axes[0, 1], axes[0, 2], axes[0, 3],
                                      axes[1, 1], axes[1, 2], axes[1, 3]],
                                     panels[1:]):
        ax.imshow(ch, cmap=cmap, vmin=0, vmax=255)
        ax.set_title(title, fontsize=9)
        ax.axis("off")
    fig.suptitle("One frame, two representations: R/G/B vs Y/U/V (frame 150)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "practice_5_yuv_decompose.png", dpi=130)
    plt.close(fig)


def frame_diff_curve(frames):
    """Mean absolute gray difference between consecutive frames."""
    g = np.stack([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
                  for f in frames])
    diff = np.mean(np.abs(np.diff(g, axis=0)), axis=(1, 2))
    return diff  # diff[i] = distance(frame i, frame i+1), len = n-1


def detect_cuts(diff, k=8.0, min_gap=15):
    """Scene-cut detection: diff value exceeding median + k * MAD."""
    med = np.median(diff)
    mad = np.median(np.abs(diff - med)) + 1e-9
    thr = med + k * mad
    cand = np.where(diff > thr)[0]
    cuts = []
    for c in cand:
        if not cuts or c - cuts[-1] > min_gap:
            cuts.append(int(c))
    return cuts, thr


def fig_frame_diff(diff, cuts, thr):
    """Fig: motion-intensity curve with detected cuts."""
    t = np.arange(len(diff)) / FPS
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(t, diff, lw=1.2, color="#3366aa", label="mean |frame i+1 - frame i|")
    ax.axhline(thr, color="#cc3333", ls="--", lw=1.0, label="threshold (median + 8*MAD)")
    ymax = float(diff.max()) * 1.05
    ax.set_ylim(0, ymax)
    for c in cuts:
        ax.axvline(c / FPS, color="#cc3333", lw=1.4, alpha=0.8)
        ax.annotate("cut @ frame %d" % c, (c / FPS, ymax * 0.72),
                    ha="center", fontsize=9, color="#cc3333",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#cc3333",
                              alpha=0.85, lw=0.6))
    for s, name in enumerate(["Scene A", "Scene B", "Scene C"]):
        ax.text((s + 0.5) * SCENE_LEN, ax.get_ylim()[1] * 0.02, name,
                ha="center", fontsize=10, color="#555555")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("mean abs diff (0-1)")
    ax.set_title("Inter-frame difference -> motion intensity -> scene-cut detection")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "practice_5_result_0.png", dpi=130)
    plt.close(fig)


def gray_u(frames, i):
    """i-th frame as uint8 grayscale (Farneback expects full-range input)."""
    return cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)


def flow_hsv(prev_g, next_g):
    """Farneback dense optical flow -> (hsv visualization, magnitude)."""
    flow = cv2.calcOpticalFlowFarneback(prev_g, next_g, None,
                                        pyr_scale=0.5, levels=3, winsize=15,
                                        iterations=3, poly_n=5, poly_sigma=1.2,
                                        flags=0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv = np.zeros((prev_g.shape[0], prev_g.shape[1], 3), dtype=np.uint8)
    hsv[..., 0] = (ang * 180 / np.pi / 2).astype(np.uint8)   # hue = direction
    hsv[..., 1] = 255
    hsv[..., 2] = (np.clip(mag / (mag.max() + 1e-9), 0, 1) * 255).astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB), mag, flow


def fig_optical_flow(frames):
    """Fig: dense flow on a smooth-motion pair (scene A) vs fast-motion pair (scene C)."""
    pairs = [(60, "Scene A frame 60->61 (smooth sine motion)"),
             (300, "Scene C frame 300->301 (fast diagonal dash)")]
    stats = []
    fig, axes = plt.subplots(2, 3, figsize=(11, 6.4))
    for row, (i, name) in enumerate(pairs):
        p, n = gray_u(frames, i), gray_u(frames, i + 1)
        vis, mag, flow = flow_hsv(p, n)
        stats.append((i, float(mag.mean()), float(mag.max()),
                      float(np.mean(mag > 1.0) * 100)))
        axes[row, 0].imshow(cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB))
        axes[row, 0].set_title(name + "\n(current frame)", fontsize=9)
        axes[row, 1].imshow(vis)
        axes[row, 1].set_title("Farneback dense flow\n(hue=direction, value=magnitude)", fontsize=9)
        step = 24
        yy, xx = np.mgrid[step // 2:HEIGHT:step, step // 2:WIDTH:step]
        axes[row, 2].imshow(cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB), alpha=0.35)
        axes[row, 2].quiver(xx, yy, flow[::step, ::step, 0], -flow[::step, ::step, 1],
                            color="#224488", angles="xy", scale_units="xy",
                            scale=0.2, width=0.004)
        axes[row, 2].set_title("flow vectors (subsampled, 5x exaggerated)", fontsize=9)
        for c in range(3):
            axes[row, c].axis("off")
    fig.suptitle("Dense optical flow (Farneback): smooth vs fast motion")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "practice_5_result_1.png", dpi=130)
    plt.close(fig)
    return stats


def track_targets(frames, diff_thresh=0.18):
    """Track the dominant moving blob per frame via consecutive-frame difference."""
    trajectories = {0: [], 1: [], 2: []}
    prev = gray_f(frames, 0)
    for i in range(1, len(frames)):
        cur = gray_f(frames, i)
        scene = min(i // (FPS * SCENE_LEN), 2)
        if i % (FPS * SCENE_LEN) == 0:      # first frame after a cut: reset
            prev = cur
            continue
        mask = (np.abs(cur - prev) > diff_thresh).astype(np.uint8) * 255
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if cnts:
            big = max(cnts, key=cv2.contourArea)
            if cv2.contourArea(big) > 80:
                m = cv2.moments(big)
                trajectories[scene].append((i, m["m10"] / m["m00"], m["m01"] / m["m00"]))
        prev = cur
    return trajectories


def fig_tracking(frames, trajectories):
    """Fig: per-scene centroid trajectories over the scene's mid frame."""
    colors = {0: "#ff4444", 1: "#2266ff", 2: "#22aa55"}
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.0))
    for s in range(3):
        mid = frames[s * FPS * SCENE_LEN + FPS * SCENE_LEN // 2]
        axes[s].imshow(cv2.cvtColor(mid, cv2.COLOR_BGR2RGB), alpha=0.55)
        pts = trajectories[s]
        if pts:
            xs = [p[1] for p in pts]
            ys = [p[2] for p in pts]
            axes[s].plot(xs, ys, ".-", color=colors[s], ms=2.5, lw=0.9)
            axes[s].plot(xs[0], ys[0], "o", color="#ffffff", ms=6, mec=colors[s])
        axes[s].set_title("Scene %s: tracked %d positions" % ("ABC"[s], len(pts)),
                          fontsize=10)
        axes[s].axis("off")
    fig.suptitle("Moving-target tracking: dominant motion-blob centroid trajectory")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "practice_5_result_2.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 64)
    print("[1] synthesize test video")
    synthesize_video(VIDEO_PATH)
    size_kb = VIDEO_PATH.stat().st_size / 1024
    print("    written: %s (%.0f KB)" % (VIDEO_PATH.relative_to(ROOT), size_kb))

    print("[2] decode & inspect")
    frames, pts_ms, fps_read = decode_all(VIDEO_PATH)
    duration = len(frames) / fps_read
    print("    container props : fps=%.2f  frames=%d  resolution=%dx%d  duration=%.2fs"
          % (fps_read, len(frames), WIDTH, HEIGHT, duration))
    print("    PTS samples (ms): frame0=%.1f  frame1=%.1f  frame120=%.1f  last=%.1f"
          % (pts_ms[0], pts_ms[1], pts_ms[120], pts_ms[-1]))
    print("    nominal frame interval: %.2f ms" % (1000.0 / fps_read))

    print("[3] figures: timeline & YUV decomposition")
    fig_timeline(frames)
    fig_yuv_decompose(frames)

    print("[4] inter-frame analysis: frame difference & scene-cut detection")
    diff = frame_diff_curve(frames)
    cuts, thr = detect_cuts(diff)
    print("    diff stats: median=%.4f  threshold=%.4f  max=%.4f"
          % (float(np.median(diff)), float(thr), float(diff.max())))
    print("    ground-truth cuts at frames: %s" % CUTS_GT)
    print("    detected cuts at frames  : %s (0-based index of the last pre-cut frame)"
          % cuts)
    fig_frame_diff(diff, cuts, thr)

    print("[5] dense optical flow (Farneback)")
    for i, mean_mag, max_mag, move_pct in fig_optical_flow(frames):
        print("    pair %4d->%-4d: mean |flow|=%.2f px/frame, max=%.2f px/frame, "
              "moving pixels(>1px)=%.1f%%"
              % (i, i + 1, mean_mag, max_mag, move_pct))

    print("[6] moving-target tracking (motion-blob centroid)")
    traj = track_targets(frames)
    for s in range(3):
        pts = traj[s]
        if pts:
            xs = np.array([p[1] for p in pts])
            ys = np.array([p[2] for p in pts])
            print("    scene %s: %d tracked positions, x range [%.0f, %.0f], "
                  "y range [%.0f, %.0f]"
                  % ("ABC"[s], len(pts), xs.min(), xs.max(), ys.min(), ys.max()))
    fig_tracking(frames, traj)

    print("=" * 64)
    print("figures written to %s:" % OUT_DIR.relative_to(ROOT))
    for name in ["practice_5_video_timeline.png", "practice_5_yuv_decompose.png",
                 "practice_5_result_0.png", "practice_5_result_1.png",
                 "practice_5_result_2.png"]:
        print("    %s" % name)
    print("done.")


if __name__ == "__main__":
    main()
