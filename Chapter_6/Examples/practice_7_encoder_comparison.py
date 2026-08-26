#!/usr/bin/env python3
"""practice_7：编码器规格对比实验（x264 vs x265）

实验一（RD 曲线）：同一素材、多档 CRF 扫点，测量码率与 SSIM/PSNR，绘制码率-失真曲线
  —— 合成素材（practice_5 测试视频）+ 真实素材（Xiph foreman 标准序列）双份验证
实验二（环节消融）：
  a) GOP 长度与场景切分 I 帧的影响（合成素材，切点真值 120/240 帧）
  b) 去块滤波开关的画质对比（真实素材，局部放大观察块效应）

依赖：ffmpeg / ffprobe（含 libx264、libx265）、numpy、matplotlib
用法：python practice_7_encoder_comparison.py [exp1|exp2a|exp2b|all]
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from daimon_runtime import setup_plot
setup_plot()

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / "Chapter_5" / "Examples" / "practice_5_test_video.mp4"
PIC = HERE.parent / "Pictures"
DURATION = 12.0  # s，360 帧 @ 30 fps

# 真实世界素材：Xiph foreman（CIF 352×288，300 帧 @ 30000/1001 fps，约 10 s）
# 公开标准测试序列（行业通行基准素材），https://media.xiph.org/video/derf/
FOREMAN = HERE.parent.parent / ".scratch" / "part2_assets" / "assets" / "foreman_cif.y4m"
FOREMAN_DURATION = 10.01

assert SRC.exists(), f"测试素材不存在: {SRC}"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def encode(lib, crf, extra=None, src=SRC, duration=DURATION):
    """编码并返回 (码率 kbps, 输出文件路径)"""
    fd, out = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)
    cmd = ["ffmpeg", "-v", "error", "-i", str(src),
           "-c:v", lib, "-crf", str(crf), "-preset", "medium",
           "-an", "-y", out]
    if extra:
        cmd[5:5] = extra
    run(cmd)
    kbps = os.path.getsize(out) * 8 / duration / 1000
    return kbps, out


def measure(path, src=SRC):
    """对编码结果测 SSIM 与 PSNR（以源视频为参考）"""
    r = subprocess.run(
        ["ffmpeg", "-i", path, "-i", str(src),
         "-lavfi", "[0:v][1:v]ssim;[0:v][1:v]psnr", "-f", "null", "-"],
        capture_output=True, text=True)
    ssim = float(re.search(r"All:([\d.]+)", r.stderr).group(1))
    psnr_m = re.search(r"average:([\d.inf]+)", r.stderr)
    psnr = float(psnr_m.group(1)) if psnr_m else float("nan")
    return ssim, psnr


def grab_frame(path, n, out_png, vf_extra=None):
    vf = f"select=eq(n\\,{n})"
    if vf_extra:
        vf = f"{vf},{vf_extra}"
    run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-vframes", "1", "-y", out_png])


def rd_curve(src, duration, tag, title, out_png):
    """实验一核心：对给定素材做 CRF 扫点并绘制 RD 曲线"""
    crfs = [16, 21, 26, 31, 36]
    data = {}
    for name, lib in [("x264", "libx264"), ("x265", "libx265")]:
        pts = []
        for crf in crfs:
            kbps, out = encode(lib, crf, src=src, duration=duration)
            ssim, psnr = measure(out, src=src)
            os.remove(out)
            pts.append({"crf": crf, "kbps": kbps, "ssim": ssim, "psnr": psnr})
            print(f"  [{tag}] {name} CRF={crf:2d}  码率={kbps:8.1f} kbps  "
                  f"SSIM={ssim:.4f}  PSNR={psnr:.2f} dB")
        data[name] = pts

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), dpi=110)
    for ax, key, label in [(axes[0], "ssim", "SSIM"), (axes[1], "psnr", "PSNR (dB)")]:
        for name, mk, c in [("x264", "o-", "#2E5F8A"), ("x265", "s-", "#B5533C")]:
            xs = [p["kbps"] for p in data[name]]
            ys = [p[key] for p in data[name]]
            ax.plot(xs, ys, mk, color=c, lw=2, ms=6, label=name)
            for p in data[name]:
                ax.annotate(f"{p['crf']}", (p["kbps"], p[key]),
                            textcoords="offset points", xytext=(6, 4), fontsize=8, color=c)
        ax.set_xlabel("码率（kbps）", fontsize=11)
        ax.set_ylabel(label, fontsize=11)
        ax.set_xscale("log")
        ax.grid(True, ls=":", lw=0.6, alpha=0.6)
        ax.legend(fontsize=10)
    axes[0].set_title("码率-SSIM（越靠左上越优，标注为 CRF）", fontsize=11.5)
    axes[1].set_title("码率-PSNR（越靠左上越优，标注为 CRF）", fontsize=11.5)
    fig.suptitle(title, fontsize=12.5, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(PIC / out_png, bbox_inches="tight")
    plt.close(fig)
    return data


def exp1():
    print("=" * 60)
    print("实验一：x264 vs x265 码率-失真曲线（CRF 扫点，preset=medium）")
    results = {}
    results["synthetic"] = rd_curve(
        SRC, DURATION, "合成素材",
        "practice_7 实验一：x264 vs x265 码率-失真曲线（合成素材，360 帧 640×360）",
        "practice_7_rd_curve.png")
    if FOREMAN.exists():
        results["foreman"] = rd_curve(
            FOREMAN, FOREMAN_DURATION, "foreman",
            "practice_7 实验一：x264 vs x265 码率-失真曲线（真实素材 foreman，300 帧 CIF）",
            "practice_7_rd_curve_foreman.png")
    else:
        print("  （跳过真实素材：未找到 foreman_cif.y4m）")
    return results


def exp2a():
    print("=" * 60)
    print("实验二 a：GOP 长度 × 场景切分 I 帧（x264, CRF=28，合成素材）")
    gops = [30, 60, 120, 240, 360]
    results = {}
    for tag, sc in [("scenecut=40（默认）", "40"), ("scenecut=0（关闭）", "0")]:
        pts = []
        for g in gops:
            kbps, out = encode("libx264", 28,
                               extra=["-g", str(g), "-x264-params", f"scenecut={sc}"])
            ssim, psnr = measure(out)
            os.remove(out)
            pts.append({"gop": g, "kbps": kbps, "ssim": ssim, "psnr": psnr})
            print(f"  GOP={g:3d}  {tag}  码率={kbps:8.1f} kbps  "
                  f"SSIM={ssim:.4f}  PSNR={psnr:.2f} dB")
        results[tag] = pts

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), dpi=110)
    for ax, key, label in [(axes[0], "kbps", "码率（kbps）"),
                           (axes[1], "psnr", "PSNR (dB)")]:
        for (tag, mk, c) in [("scenecut=40（默认）", "o-", "#2E5F8A"),
                             ("scenecut=0（关闭）", "s--", "#B5533C")]:
            xs = [p["gop"] for p in results[tag]]
            ys = [p[key] for p in results[tag]]
            ax.plot(xs, ys, mk, color=c, lw=2, ms=6, label=tag)
        ax.set_xlabel("GOP 长度（帧）", fontsize=11)
        ax.set_ylabel(label, fontsize=11)
        ax.set_xticks(gops)
        ax.grid(True, ls=":", lw=0.6, alpha=0.6)
        ax.legend(fontsize=9.5)
    axes[0].set_title("GOP 长度 vs 码率", fontsize=11.5)
    axes[1].set_title("GOP 长度 vs 画质", fontsize=11.5)
    fig.suptitle("practice_7 实验二 a：GOP 长度与场景切分 I 帧的影响"
                 "（合成素材，切点真值：第 120 / 240 帧）", fontsize=12.5, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(PIC / "practice_7_gop_analysis.png", bbox_inches="tight")
    plt.close(fig)
    return results


def exp2b():
    print("=" * 60)
    print("实验二 b：去块滤波开关对比（x264, CRF=32，真实素材局部放大）")
    src, dur = (FOREMAN, FOREMAN_DURATION) if FOREMAN.exists() else (SRC, DURATION)
    results = {}
    variants = {}
    for tag, extra in [("deblock_on", []),
                       ("deblock_off", ["-x264-params", "no-deblock=1"])]:
        kbps, out = encode("libx264", 32, extra=extra, src=src, duration=dur)
        ssim, psnr = measure(out, src=src)
        variants[tag] = {"kbps": kbps, "ssim": ssim, "psnr": psnr, "path": out}
        results[tag] = {"kbps": kbps, "ssim": ssim, "psnr": psnr}
        print(f"  {tag:12s}  码率={kbps:8.1f} kbps  SSIM={ssim:.4f}  PSNR={psnr:.2f} dB")

    # 取 foreman 第 150 帧（画面内容丰富的施工场景），裁剪局部并 3 倍最近邻放大
    is_foreman = FOREMAN.exists() and src == FOREMAN
    frame_n = 150 if is_foreman else 100
    crop = "crop=117:96:90:60,scale=468:384:flags=neighbor" if is_foreman else None
    imgs = []
    for tag in ["deblock_on", "deblock_off"]:
        fd, png = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        grab_frame(variants[tag]["path"], frame_n, png, vf_extra=crop)
        imgs.append((tag, plt.imread(png)))
        os.remove(png)
        os.remove(variants[tag]["path"])

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), dpi=110)
    for ax, (tag, img), title in [
            (axes[0], imgs[0], f"去块滤波开启  PSNR={results['deblock_on']['psnr']:.2f} dB"),
            (axes[1], imgs[1], f"去块滤波关闭  PSNR={results['deblock_off']['psnr']:.2f} dB")]:
        ax.imshow(img)
        ax.set_title(title, fontsize=11.5)
        ax.axis("off")
    zoom_note = "（局部 3 倍放大）" if is_foreman else ""
    fig.suptitle(f"practice_7 实验二 b：环路去块滤波开关的画质对比（x264, CRF=32，第 {frame_n} 帧{zoom_note}）",
                 fontsize=12.5, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(PIC / "practice_7_deblock_compare.png", bbox_inches="tight")
    plt.close(fig)
    return results


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    results = {}
    if which in ("exp1", "all"):
        results["exp1"] = exp1()
    if which in ("exp2a", "all"):
        results["exp2a"] = exp2a()
    if which in ("exp2b", "all"):
        results["exp2b"] = exp2b()
    out_json = HERE / "practice_7_results.json"
    old = {}
    if out_json.exists():
        old = json.load(open(out_json))
    old.update(results)
    with open(out_json, "w") as f:
        json.dump(old, f, ensure_ascii=False, indent=2)
    print("=" * 60)
    print(f"完成。图与数据已写入 {PIC}")


if __name__ == "__main__":
    main()
