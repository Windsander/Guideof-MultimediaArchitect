#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""practice_9 预实验：音视频同步策略对比（离散事件仿真，Docs_8_3 前置）

模型设定（与 8.2 节 ffplay 机制一一对应）：
  - 音频：按采样数严格走时（虚拟声卡），每 1024 采样一个消费节拍
          —— 音频是「不可压缩」的时间基准
  - 视频：解码有代价且不均（重帧 50~80ms、常规帧 15~35ms，种子固定可复现），
          解码完成帧进入显示队列
  - 显示策略三选一：
      free     自由运行：解出即播，帧间隔固定 1/30s，不看音频时钟
      master   音频主时钟：对齐 ffplay 规则 —— 晚超 40ms 丢帧、早超 40ms 重复
      video    视频主时钟：音频迁就视频（此处退化为与 free 类似的对照）

输出：
  practice_9_sync_results.json  两种策略的逐帧显示记录与统计
  practice_9_sync_compare.png   A-V 偏差随时间变化曲线（预实验用，英文标注）

依据：ffplay.c（FFmpeg n8.0）compute_target_delay / video_refresh，
      阈值 AV_SYNC_THRESHOLD_MIN=0.04（见 CH8_SYNC_FACTS.md B 节）
"""

import json
import sys
from pathlib import Path

import av
import numpy as np

HERE = Path(__file__).resolve().parent
CLIP = HERE / "practice_9_av_sync_test.mkv"

FPS = 30
FRAME_INTERVAL = 1.0 / FPS
SYNC_THRESHOLD = 0.040          # 40ms，对齐 ffplay AV_SYNC_THRESHOLD_MIN
AUDIO_TICK = 1024 / 44100       # 音频消费节拍（≈23.2ms）

rng = np.random.default_rng(42)  # 固定种子，实验可复现


# ---------------------------------------------------------------------------
# 素材读取：音频节拍表 + 视频帧 PTS 表
# ---------------------------------------------------------------------------

def load_timelines():
    # 注意：同一 container 走到 EOF 后不能再次 decode，两个流各开一次
    audio_ticks, consumed, total = [], 0, 0
    c = av.open(str(CLIP))
    for fr in c.decode(audio=0):
        total += fr.samples
        while total - consumed >= 1024:      # 每消费 1024 采样 = 一个虚拟声卡节拍
            consumed += 1024
            audio_ticks.append(consumed)     # 时刻 = consumed/44100，单调递增
    c.close()
    c = av.open(str(CLIP))
    video_pts = [float(fr.pts * fr.time_base) for fr in c.decode(video=0)]
    c.close()
    audio_times = [s / 44100.0 for s in audio_ticks]
    return audio_times, video_pts


# ---------------------------------------------------------------------------
# 解码代价模型：制造不均匀的「重帧」
# ---------------------------------------------------------------------------

def decode_costs(n):
    costs = rng.uniform(0.015, 0.035, size=n)     # 常规帧 15~35ms
    heavy = rng.random(n) < 0.08                   # 8% 重帧
    costs[heavy] = rng.uniform(0.050, 0.080, size=int(heavy.sum()))
    # 持续压力段（第 3~6 秒）：模拟机器算力不足 / 码流过重，
    # 解码均耗 1.5 倍 -> 段内超过 33.3ms/帧的显示节拍而持续落后；
    # 段后恢复正常，解码逐步追回（落后可恢复的弹性场景）
    costs[90:180] *= 1.5
    return costs


def ready_times(video_pts, costs):
    """顺序解码：第 j 帧开始解码的时刻 = max(上一帧完成时刻)。"""
    ready, t = [], 0.0
    for c in costs:
        t += c
        ready.append(t)
    return ready


# ---------------------------------------------------------------------------
# 策略一：自由运行（不解同步问题，让世界自然漂移）
# ---------------------------------------------------------------------------

def run_free(video_pts, ready):
    records = []
    t_disp = 0.0
    for pts, rdy in zip(video_pts, ready):
        t_disp = max(t_disp + FRAME_INTERVAL, rdy)   # 解不完就只能晚播
        records.append({"pts": pts, "disp": t_disp,
                        "offset": t_disp - pts, "action": "show"})
    return records


# ---------------------------------------------------------------------------
# 策略二：音频主时钟（ffplay 规则：晚丢早重）
# ---------------------------------------------------------------------------

def run_master(video_pts, ready, audio_times):
    records = []
    q = list(zip(video_pts, ready))       # 待显示队列（按 pts 序）
    idx, last_shown = 0, None
    for a_t in audio_times:
        while idx < len(q):
            pts, rdy = q[idx]
            if rdy > a_t:                  # 还没解出来
                break
            diff = a_t - pts               # 音频时钟 - 帧 PTS
            if diff > SYNC_THRESHOLD:
                records.append({"pts": pts, "disp": None,
                                "offset": None, "action": "drop"})
                idx += 1
                continue
            if diff < -SYNC_THRESHOLD:
                break                      # 未到显示时刻，等待下一节拍
            action = "show" if last_shown != pts else "repeat"
            records.append({"pts": pts, "disp": a_t,
                            "offset": a_t - pts, "action": action})
            last_shown = pts
            idx += 1
    # 音频播完后兜底显示剩余帧
    while idx < len(q):
        pts, rdy = q[idx]
        records.append({"pts": pts, "disp": rdy,
                        "offset": rdy - pts, "action": "show(tail)"})
        idx += 1
    return records


# ---------------------------------------------------------------------------
# 统计与出图
# ---------------------------------------------------------------------------

def summarize(records):
    # 统计只计音频播期内受同步策略管辖的帧；tail（音频播完后的兜底）单列
    inband = [r for r in records if not r["action"].endswith("(tail)")]
    offs = [r["offset"] for r in inband if r["offset"] is not None]
    drops = sum(1 for r in inband if r["action"] == "drop")
    tail = sum(1 for r in records if r["action"].endswith("(tail)"))
    return {
        "shown": len(offs),
        "dropped": drops,
        "tail": tail,
        "offset_mean_ms": round(float(np.mean(offs)) * 1000, 2),
        "offset_std_ms": round(float(np.std(offs)) * 1000, 2),
        "offset_max_ms": round(float(np.max(offs)) * 1000, 2),
        "offset_min_ms": round(float(np.min(offs)) * 1000, 2),
    }


def main():
    audio_times, video_pts = load_timelines()
    costs = decode_costs(len(video_pts))
    ready = ready_times(video_pts, costs)
    print(f"素材: {len(video_pts)} 帧视频 / {len(audio_times)} 个音频节拍")
    print(f"解码总代价 {costs.sum():.2f}s（素材时长 {video_pts[-1]:.2f}s，"
          f"解码必然跟不上 -> 同步策略必须介入）")

    rec_free = run_free(video_pts, ready)
    rec_master = run_master(video_pts, ready, audio_times)

    stats = {"free": summarize(rec_free), "master": summarize(rec_master)}
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    out_json = HERE / "practice_9_sync_results.json"
    out_json.write_text(json.dumps({
        "stats": stats, "free": rec_free, "master": rec_master,
    }, ensure_ascii=False))
    print(f"结果 -> {out_json}")

    # ---- 预实验出图（英文标注；成书图件届时由 managed python + setup_plot 重绘）
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 4.2))
    for rec, name, color in ((rec_free, "free-run", "#B5533C"),
                             (rec_master, "audio-master", "#2E5F8A")):
        inband = [r for r in rec if not r["action"].endswith("(tail)")]
        xs = [r["pts"] for r in inband if r["offset"] is not None]
        ys = [r["offset"] * 1000 for r in inband if r["offset"] is not None]
        ax.plot(xs, ys, label=name, color=color, lw=1.2)
    # 丢帧发生的时刻：音频主时钟策略「保同步」的代价可视化
    drops = [r["pts"] for r in rec_master if r["action"] == "drop"]
    ax.scatter(drops, [-60] * len(drops), marker="x", c="#B5533C",
               s=14, lw=0.7, label="dropped frame")
    ax.axhline(40, ls="--", c="#999", lw=0.8)
    ax.axhline(-40, ls="--", c="#999", lw=0.8)
    ax.set_xlabel("presentation time (s)")
    ax.set_ylabel("A-V offset (ms)")
    ax.set_title("practice_9 dry-run: A-V offset, free-run vs audio-master clock")
    ax.legend()
    out_png = HERE / "practice_9_sync_compare.png"
    fig.savefig(out_png, bbox_inches="tight", dpi=110)
    print(f"图件 -> {out_png}")


if __name__ == "__main__":
    main()
