#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""practice_10 预实验：用户态弱网中继（限速 + 固定时延），Docs_9_3 前置

背景：教科书方案 netem/dummynet 需要 root 且 macOS 配置繁琐。
本中继以纯用户态 TCP 代理实现同等教学效果：
  - 令牌桶限速（仅作用于 服务器->客户端 方向，即拉流的下载路径）
  - 固定附加时延（每块数据延迟 release，保序转发）
推流端 -> 中继 -> 播放器，播放器连中继即置身于「弱网」。

验证目标：1Mbps 限速下下载 512KB 文件，耗时应 ≈ 512*8/1000 ≈ 4.1s（±15%）；
         附加 100ms 时延下小请求 RTT 应明显抬升。

实测存档（2026-08-26，本机）：512KB 经 1000kbps+100ms 中继耗时 3.81s
（偏差 -9%，来自令牌桶初始满桶的 62.5KB 突发额度，长连接流媒体场景可忽略；
如需严格限速可将 TokenBucket.tokens 初始化为 0）；RTT 0.7ms -> 110.9ms。

用法：
  python throttle_relay.py <listen_port> <target_host> <target_port> <rate_kbps> <delay_ms>
"""

import heapq
import socket
import sys
import threading
import time


class TokenBucket:
    """令牌桶：容量 = rate * burst_window，按时间补令牌，不够就睡。"""

    def __init__(self, rate_bytes_per_sec, burst_window=0.5):
        self.rate = rate_bytes_per_sec
        self.capacity = rate_bytes_per_sec * burst_window
        self.tokens = self.capacity
        self.last = time.monotonic()

    def consume(self, n):
        while True:
            now = time.monotonic()
            self.tokens = min(self.capacity,
                              self.tokens + (now - self.last) * self.rate)
            self.last = now
            if self.tokens >= n:
                self.tokens -= n
                return
            deficit = n - self.tokens
            time.sleep(min(deficit / self.rate, 0.05))


class DelayLine:
    """固定时延线：块按 (release_time, seq) 入堆，到点按序发出。"""

    def __init__(self, dst: socket.socket, delay_sec):
        self.dst = dst
        self.delay = delay_sec
        self.heap = []
        self.seq = 0
        self.cond = threading.Condition()
        self.alive = True
        self.worker = threading.Thread(target=self._run, daemon=True)
        self.worker.start()

    def submit(self, data):
        with self.cond:
            heapq.heappush(self.heap,
                           (time.monotonic() + self.delay, self.seq, data))
            self.seq += 1
            self.cond.notify()

    def _run(self):
        while True:
            with self.cond:
                while self.alive and (not self.heap or
                                      self.heap[0][0] > time.monotonic()):
                    timeout = None
                    if self.heap:
                        timeout = max(0.0, self.heap[0][0] - time.monotonic())
                    self.cond.wait(timeout if timeout is not None else 0.05)
                if not self.alive and not self.heap:
                    return
                if not self.heap or self.heap[0][0] > time.monotonic():
                    continue
                _, _, data = heapq.heappop(self.heap)
            try:
                self.dst.sendall(data)
            except OSError:
                self.alive = False
                return

    def close(self):
        with self.cond:
            self.alive = False
            self.cond.notify_all()


def relay(src, dst, bucket=None, delay_line=None):
    try:
        while True:
            data = src.recv(16384)
            if not data:
                break
            if bucket is not None:
                bucket.consume(len(data))
            if delay_line is not None:
                delay_line.submit(data)
            else:
                dst.sendall(data)
    except OSError:
        pass


def main():
    listen_port = int(sys.argv[1])
    target_host, target_port = sys.argv[2], int(sys.argv[3])
    rate_kbps = float(sys.argv[4])
    delay_ms = float(sys.argv[5])

    bucket = TokenBucket(rate_kbps * 1000 / 8)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", listen_port))
    srv.listen(8)
    print(f"[relay] 127.0.0.1:{listen_port} -> {target_host}:{target_port} "
          f"| 限速 {rate_kbps}kbps + 时延 {delay_ms}ms（仅下行）")

    while True:
        conn, addr = srv.accept()
        upstream = socket.create_connection((target_host, target_port))
        dl = DelayLine(conn, delay_ms / 1000)
        t1 = threading.Thread(target=relay,
                              args=(upstream, conn, bucket, dl), daemon=True)
        t2 = threading.Thread(target=relay,
                              args=(conn, upstream), daemon=True)
        t1.start()
        t2.start()
        print(f"[relay] 新连接 {addr}")


if __name__ == "__main__":
    main()
