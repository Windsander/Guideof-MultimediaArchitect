#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""practice_10：直播链路搭建与质量分析（Docs_9_3 实战）

链路（全部本机闭环）：
  条码帧生成 -> ffmpeg 推 RTMP -> MediaMTX -> 三路拉流
    A1: RTMP 直拉（基线延迟）
    A2: HLS 直拉（分片延迟）
    B : HLS 经 throttle_relay 弱网中继（900kbps + 300ms，仅下行）

质量方法（对应 9.2 体系）：
  - 端到端延迟：条码烧录真实墙钟，拉流端读回相减 = glass-to-glass（9.1.2）
  - 卡顿：以拉到的帧到达时刻回放仿真——应显时刻无帧即记一次卡顿，
    累计卡顿时长与次数（9.2.1 口径）
产出：practice_10_results.json + practice_10_latency.png（预实验图）

用法（需 .scratch/venv8 的 PyAV 与 PATH 中的 ffmpeg/mediamtx）：
  python practice_10_link_quality.py
"""

import json
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

import av
import numpy as np

HERE = Path(__file__).resolve().parent
RELAY = HERE / "throttle_relay.py"

WIDTH, HEIGHT = 640, 360
FPS = 30
CELL = 10
SYNC = [1, 0, 1, 0, 1, 0, 1, 0]
N_SYNC = len(SYNC)
N_TS, N_SEQ = 32, 16
N_CELLS = N_SYNC + N_TS + N_SEQ

RTMP_URL = "rtmp://127.0.0.1:1935/live/p10"
HLS_URL = "http://127.0.0.1:8888/live/p10/index.m3u8"
RELAY_PORT = 18988
HLS_VIA_RELAY = f"http://127.0.0.1:{RELAY_PORT}/live/p10/index.m3u8"

PHASE_SECONDS = 12          # 每个拉流相位的采集窗口
PUSH_SECONDS = 55           # 推流总时长（覆盖三相位 + HLS 启动余量）


# ---------------------------------------------------------------------------
# 条码（与 ts_barcode_proto.py 相同格式；时间戳改用真实墙钟）
# ---------------------------------------------------------------------------

def bits_of(value, nbits):
    return [(value >> (nbits - 1 - i)) & 1 for i in range(nbits)]


def write_barcode(img, ts_ms, seq):
    bits = SYNC + bits_of(ts_ms & 0xFFFFFFFF, N_TS) + bits_of(seq & 0xFFFF, N_SEQ)
    for i, b in enumerate(bits):
        img[0:CELL, i * CELL:(i + 1) * CELL] = 255 if b else 0
    return img


def read_barcode(img):
    bits = []
    for i in range(N_CELLS):
        y0, x0 = CELL // 2 - 2, i * CELL + CELL // 2 - 2
        bits.append(1 if img[y0:y0 + 4, x0:x0 + 4].mean() > 128 else 0)
    if bits[:N_SYNC] != SYNC:
        raise ValueError("同步头损坏")
    ts, seq = 0, 0
    for b in bits[N_SYNC:N_SYNC + N_TS]:
        ts = (ts << 1) | b
    for b in bits[N_SYNC + N_TS:]:
        seq = (seq << 1) | b
    return ts, seq


rng = np.random.default_rng(42)

def make_frame(idx, ts_ms):
    img = np.full((HEIGHT, WIDTH), 24, dtype=np.uint8)
    bar_w = 60
    x = int((idx % FPS) / FPS * (WIDTH - bar_w))
    img[HEIGHT // 2 - 20:HEIGHT // 2 + 20, x:x + bar_w] = 120
    # 底部噪声带：把码率抬到 ~1.5Mbps，弱网中继才有压可施
    # （纯静态内容仅 ~22kbps，900kbps 限速不构成压力）
    img[HEIGHT - 80:, :] = rng.integers(0, 90, size=(80, WIDTH), dtype=np.uint8)
    write_barcode(img, ts_ms, idx)
    return np.stack([img, img, img], axis=-1)


# ---------------------------------------------------------------------------
# 进程管理：MediaMTX + 推流 + 中继
# ---------------------------------------------------------------------------

def start_mediamtx():
    p = subprocess.Popen(["mediamtx", str(HERE.parent / "mediamtx.yml")],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, cwd=HERE)
    import socket
    for _ in range(40):                     # 就绪探针：等 RTMP 端口可连接
        try:
            s = socket.create_connection(("127.0.0.1", 1935), timeout=0.5)
            s.close()
            return p
        except OSError:
            time.sleep(0.25)
    raise RuntimeError("MediaMTX 未就绪")


def start_publisher():
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
           "-an", "-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency",
           "-g", "60", "-crf", "23", "-f", "flv", RTMP_URL]
    proc = None
    for attempt in range(3):                # 推流失败重试（服务器未就绪等）
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2.0)
        if proc.poll() is None:
            break
        print(f"  [warn] 推流第 {attempt + 1} 次启动失败，重试")
    if proc.poll() is not None:
        raise RuntimeError("推流启动失败")

    def feed():
        start = time.time()
        n = PUSH_SECONDS * FPS
        for i in range(n):
            ts_ms = int(time.time() * 1000) & 0xFFFFFFFF
            try:
                proc.stdin.write(make_frame(i % 65536, ts_ms).tobytes())
            except (BrokenPipeError, ValueError):
                return
            nxt = start + (i + 1) / FPS
            if nxt > time.time():
                time.sleep(nxt - time.time())
        try:
            proc.stdin.close()
        except Exception:
            pass

    t = threading.Thread(target=feed, daemon=True)
    t.start()
    return proc, t


def start_relay():
    p = subprocess.Popen([sys.executable, str(RELAY), str(RELAY_PORT),
                          "127.0.0.1", "8888", "900", "300"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    return p


# ---------------------------------------------------------------------------
# 拉流采集：读回条码，记录 (帧序号, 烧录时刻, 到达时刻)
# ---------------------------------------------------------------------------

def pull(url, seconds, wait_playlist=False):
    if wait_playlist:
        deadline = time.time() + 30
        while time.time() < deadline:
            try:
                urllib.request.urlopen(url, timeout=2).read()
                break
            except Exception:
                time.sleep(0.5)
    rows = []
    deadline = time.time() + seconds
    try:
        c = av.open(url, options={"rw_timeout": "5000000"} if
                    url.startswith("rtmp") else {})
        for fr in c.decode(video=0):
            arrival = time.time()
            try:
                ts, seq = read_barcode(fr.to_ndarray(format="gray"))
                am = int(arrival * 1000) & 0xFFFFFFFF
                lat = (am - ts) & 0xFFFFFFFF        # 32 位回绕安全差值
                if lat > 0x7FFFFFFF:
                    lat -= 0x100000000
                rows.append({"seq": seq,
                             "ts_ms": ts, "arrival_ms": am,
                             "latency_ms": round(float(lat), 1)})
            except ValueError:
                pass
            if time.time() > deadline:
                break
        c.close()
    except Exception as e:
        print(f"  [warn] 拉流异常({url[:40]}...): {e}")
    return rows


# ---------------------------------------------------------------------------
# 卡顿回放仿真（9.2.1 口径：缓冲耗尽 -> 重新蓄水）
# ---------------------------------------------------------------------------

def stall_analysis(rows):
    if len(rows) < 10:
        return {"stalls": 0, "stall_seconds": 0.0}
    rows = sorted(rows, key=lambda r: r["arrival_ms"])
    t0 = rows[0]["arrival_ms"] / 1000.0
    stalls, stall_t, n = 0, 0.0, 0
    for i in range(1, len(rows)):
        due = t0 + i / FPS                      # 第 i 帧应显时刻
        got = rows[i]["arrival_ms"] / 1000.0    # 实际到达时刻
        if got > due + 0.05:                    # 宽限 50ms
            stalls += 1
            stall_t += got - due
        t0 = max(t0, got - i / FPS)             # 卡顿时钟顺延（重新起播）
        n += 1
    play_seconds = n / FPS
    return {"stalls": stalls,
            "stall_seconds": round(stall_t, 2),
            "stall_ratio": round(stall_t / play_seconds, 4),
            "play_seconds": round(play_seconds, 1)}


def summarize(rows, warmup_ms=3000):
    """稳态延迟统计：剔除每个相位前 warmup_ms 的追帧回放量。"""
    if not rows:
        return {}
    t0 = min(r["arrival_ms"] for r in rows)
    steady = [r for r in rows
              if ((r["arrival_ms"] - t0) & 0xFFFFFFFF) >= warmup_ms]
    lat = sorted(r["latency_ms"] for r in steady or rows)
    p = lambda q: round(lat[min(len(lat) - 1, int(q * len(lat)))], 1)
    return {"frames": len(lat), "p50": p(0.50), "p95": p(0.95),
            "mean": round(sum(lat) / len(lat), 1)}


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main():
    print("[1/5] 启动 MediaMTX ...")
    mtx = start_mediamtx()
    print("[2/5] 启动条码推流 (RTMP) ...")
    pub, feed_t = start_publisher()
    time.sleep(3)                       # 等推流登记

    print("[3/5] 相位 A1：RTMP 直拉 ...")
    a1 = pull(RTMP_URL, PHASE_SECONDS)

    print("[4/5] 相位 A2：HLS 直拉 ...")
    a2 = pull(HLS_URL, PHASE_SECONDS, wait_playlist=True)

    print("[5/5] 相位 B：HLS 经弱网中继 (900kbps + 300ms) ...")
    relay = start_relay()
    b = pull(HLS_VIA_RELAY, PHASE_SECONDS, wait_playlist=True)

    for p in (relay, pub, mtx):
        p.terminate()
    results = {
        "A1_rtmp": {"latency": summarize(a1), "stall": stall_analysis(a1)},
        "A2_hls": {"latency": summarize(a2), "stall": stall_analysis(a2)},
        "B_hls_weaknet": {"latency": summarize(b), "stall": stall_analysis(b)},
    }
    out = HERE / "practice_10_results.json"
    out.write_text(json.dumps({"summary": results,
                               "A1": a1, "A2": a2, "B": b}, ensure_ascii=False))
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"结果 -> {out}")


if __name__ == "__main__":
    main()
