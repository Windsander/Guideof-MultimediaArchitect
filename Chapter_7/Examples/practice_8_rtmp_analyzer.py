#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""practice_8：RTMP 推流抓包与逐字节还原（Chapter_7 / Docs_7_6 配套示例）

模式一（proxy）：本机代理抓流 —— 监听 1936 端口，原样转发到 1935 端口的
    MediaMTX 服务器，双向字节流分别落盘为 rtmp_c2s.bin / rtmp_s2c.bin。
    （有条件直接使用 Wireshark / tcpdump 的读者，可跳过本模式，
      用「Follow TCP Stream」导出等价的双向字节流。）

模式二（parse）：按 Adobe RTMP Specification v1.0（2012-12-21）逐字节解析
    落盘文件，依次还原三个层次：
      握手（规范 §5.2）→ Chunk 拆分（§5.3）→ Message 重组与 AMF0 命令解读

完整实验步骤（详见 7.6 节正文）：
    1. mediamtx mediamtx.yml            # 最小配置只需两行：paths: / all:
    2. python practice_8_rtmp_analyzer.py proxy
    3. ffmpeg -re -i test.mp4 -c copy -f flv rtmp://127.0.0.1:1936/live/test
    4. 推流几秒后 Ctrl+C 停止代理，再执行：
       python practice_8_rtmp_analyzer.py parse

依赖：仅 Python 标准库（3.7+），无需安装任何第三方包。
"""

import socket
import struct
import sys
import threading
from pathlib import Path

LISTEN_PORT = 1936        # 代理监听端口（ffmpeg 推流地址指向这里）
TARGET_PORT = 1935        # RTMP 服务器端口（MediaMTX 默认 1935）

C2S_FILE = Path("rtmp_c2s.bin")   # 客户端 -> 服务器 字节流
S2C_FILE = Path("rtmp_s2c.bin")   # 服务器 -> 客户端 字节流


# ---------------------------------------------------------------------------
# 模式一：TCP 代理抓流
# ---------------------------------------------------------------------------
# 思路：代理坐在推流端与服务器之间，对每个方向各起一个线程做
# 「边转发、边落盘」（tee）。RTMP 本身不加密，字节流即是协议全貌。

def run_proxy():
    c2s_f, s2c_f = open(C2S_FILE, "wb"), open(S2C_FILE, "wb")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", LISTEN_PORT))
    srv.listen(1)
    print(f"[proxy] 监听 127.0.0.1:{LISTEN_PORT} -> 127.0.0.1:{TARGET_PORT}")
    print(f"[proxy] 请推流至 rtmp://127.0.0.1:{LISTEN_PORT}/live/test ...")

    conn, addr = srv.accept()
    print(f"[proxy] 客户端已连接: {addr}")
    upstream = socket.create_connection(("127.0.0.1", TARGET_PORT))

    def tee(src, dst, fh, tag):
        try:
            while True:
                data = src.recv(65536)
                if not data:
                    break
                fh.write(data)          # 落盘：原始字节，一个不漏
                fh.flush()
                dst.sendall(data)       # 转发：对通信双方完全透明
        except OSError:
            pass
        finally:
            print(f"[proxy] {tag} 方向流结束")

    t1 = threading.Thread(target=tee, args=(conn, upstream, c2s_f, "C->S"), daemon=True)
    t2 = threading.Thread(target=tee, args=(upstream, conn, s2c_f, "S->C"), daemon=True)
    t1.start()
    t2.start()
    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("\n[proxy] 手动停止")
    conn.close()
    upstream.close()
    srv.close()
    c2s_f.close()
    s2c_f.close()
    print(f"[proxy] 抓包已保存: {C2S_FILE}, {S2C_FILE}")
    print(f"[proxy] 下一步: python {Path(__file__).name} parse")


# ---------------------------------------------------------------------------
# AMF0 迷你解码器
# ---------------------------------------------------------------------------
# RTMP 的命令消息（connect / createStream / publish ...）与数据消息
# （@setDataFrame）都以 AMF0 编码。这里只实现读懂推流过程所需的子集：
# Number / Boolean / String / Object / Null / ECMA Array / Date。
# 类型标记字节的完整清单见 AMF0 规范，常见值：
#   0x00 Number(8B 双精度)  0x01 Boolean  0x02 String(2B 长度+UTF-8)
#   0x03 Object(键值对, 以 00 00 09 结尾)  0x05 Null
#   0x08 ECMA Array(4B 计数 + 键值对)     0x0B Date

class AMF0:
    def __init__(self, data: bytes):
        self.d, self.p = data, 0

    def _read(self, n):
        b = self.d[self.p:self.p + n]
        self.p += n
        return b

    def read_value(self):
        t = self._read(1)[0]
        if t == 0x00:   # Number：大端双精度浮点
            return struct.unpack(">d", self._read(8))[0]
        if t == 0x01:   # Boolean
            return bool(self._read(1)[0])
        if t == 0x02:   # String：2 字节长度 + UTF-8
            n = struct.unpack(">H", self._read(2))[0]
            return self._read(n).decode("utf-8", "replace")
        if t == 0x03:   # Object：键值对序列，空键 + 0x09 结束
            return self._read_kv_pairs()
        if t == 0x05:   # Null
            return None
        if t == 0x08:   # ECMA Array：4 字节计数（仅参考），随后同 Object
            self._read(4)
            return self._read_kv_pairs()
        if t == 0x0B:   # Date：8B 毫秒时间戳 + 2B 时区
            v = struct.unpack(">d", self._read(8))[0]
            self._read(2)
            return v
        return f"<amf0-type-0x{t:02x} unsupported>"

    def _read_kv_pairs(self):
        obj = {}
        while self.p < len(self.d):
            n = struct.unpack(">H", self._read(2))[0]
            if n == 0 and self.p < len(self.d) and self.d[self.p] == 0x09:
                self.p += 1                      # 00 00 09：对象结束标记
                break
            key = self._read(n).decode("utf-8", "replace")
            obj[key] = self.read_value()
        return obj


def amf0_all(data: bytes):
    """顺序解出载荷中的全部 AMF0 值，容忍尾部残留字节。"""
    dec, out = AMF0(data), []
    while dec.p < len(data):
        try:
            out.append(dec.read_value())
        except Exception:
            out.append(f"<undecoded {len(data) - dec.p}B>")
            break
    return out


# ---------------------------------------------------------------------------
# Chunk 流解析器（规范 §5.3）
# ---------------------------------------------------------------------------

# Message 类型号速查（规范 §5.4 与 §7）
MSG_TYPE_NAMES = {
    1: "Set Chunk Size", 2: "Abort Message", 3: "Acknowledgement",
    4: "User Control", 5: "Window Acknowledgement Size", 6: "Set Peer Bandwidth",
    8: "Audio", 9: "Video", 15: "Data AMF3", 16: "SharedObject AMF3",
    17: "Command AMF3", 18: "Data AMF0", 19: "SharedObject AMF0",
    20: "Command AMF0", 22: "Aggregate",
}


class ChunkStreamParser:
    """把一段字节流逐字节还原为 Message 序列。

    解析状态分两层：
      self.chunk_size —— 当前生效的最大块长，随 Set Chunk Size 控制消息更新；
      self.streams    —— 每个 Chunk Stream ID 各自记住「前一块的头部」，
                        因为 fmt=1/2/3 的块都省略了部分字段，要靠它补全。
    """

    def __init__(self, data: bytes, skip_handshake: int):
        self.d, self.p = data, skip_handshake
        self.chunk_size = 128            # 协商前的默认值（规范 §5.4.1）
        self.streams = {}                # cs_id -> 该流的解析状态
        self.messages = []               # 还原出的完整 Message

    def _read(self, n):
        b = self.d[self.p:self.p + n]
        self.p += n
        return b

    def _stream(self, csid):
        return self.streams.setdefault(csid, {
            "msg_len": 0, "msg_type": 0, "ms_id": 0,
            "timestamp": 0, "delta": 0,
            "buf": bytearray(),          # 正在重组中的消息载荷
        })

    def parse(self):
        while self.p < len(self.d):
            if not self._parse_one_chunk():
                break
        return self.messages

    def _parse_one_chunk(self):
        # ---- Basic Header（§5.3.1.1）：fmt(2bit) + cs_id(6bit/扩展)
        b0 = self._read(1)
        if len(b0) < 1:
            return False
        fmt, csid = b0[0] >> 6, b0[0] & 0x3F
        if csid == 0:                    # 2 字节型：cs_id = 64 + 第二字节
            csid = self._read(1)[0] + 64
        elif csid == 1:                  # 3 字节型：cs_id = 64 + 小端两字节
            b1, b2 = self._read(2)
            csid = b2 * 256 + b1 + 64
        st = self._stream(csid)

        # ---- Message Header（§5.3.1.2）：长度随 fmt 递减
        # fmt=0 (11B)：时间戳3 + 消息长3 + 类型1 + 流ID4(小端) —— 新消息的完整自描述
        # fmt=1 (7B) ：省流ID（与前块同流）；fmt=2 (3B)：只剩时间戳增量
        # fmt=3 (0B) ：全部沿用前块 —— 同一消息的后续块、或同流同参数的新消息
        ts_field = None
        if fmt == 0:
            ts_field = int.from_bytes(self._read(3), "big")
            st["msg_len"] = int.from_bytes(self._read(3), "big")
            st["msg_type"] = self._read(1)[0]
            st["ms_id"] = int.from_bytes(self._read(4), "little")
            st["buf"] = bytearray()
            st["delta"] = ts_field
        elif fmt == 1:
            ts_field = int.from_bytes(self._read(3), "big")
            st["msg_len"] = int.from_bytes(self._read(3), "big")
            st["msg_type"] = self._read(1)[0]
            st["buf"] = bytearray()
            st["delta"] = ts_field
        elif fmt == 2:
            ts_field = int.from_bytes(self._read(3), "big")
            st["buf"] = bytearray()
            st["delta"] = ts_field
        else:                            # fmt == 3
            ts_field = st["delta"]
        if ts_field == 0xFFFFFF:         # 三字节装不下：扩展时间戳（§5.3.1.3）
            ts_field = int.from_bytes(self._read(4), "big")

        # ---- 时间戳基准的维护
        # fmt=0 给绝对值；fmt=1/2 给增量；fmt=3 若是「新消息的首块」
        # （上一块恰好收完了前一条消息），同样要累加增量。
        if fmt == 0:
            st["timestamp"] = ts_field
        elif fmt in (1, 2):
            st["timestamp"] += ts_field
        elif len(st["buf"]) == 0 and st["msg_len"] > 0 and st.get("_just_finished"):
            st["timestamp"] += ts_field

        # ---- Chunk Data：每块最多 chunk_size 字节
        need = st["msg_len"] - len(st["buf"])
        take = min(self.chunk_size, need)
        st["buf"] += self._read(take)

        if len(st["buf"]) >= st["msg_len"] and st["msg_len"] > 0:
            self.messages.append({
                "cs_id": csid,
                "timestamp": st["timestamp"], "type": st["msg_type"],
                "ms_id": st["ms_id"], "payload": bytes(st["buf"]),
            })
            # Set Chunk Size（§5.4.1）：立即作用于本方向的后续块
            if st["msg_type"] == 1 and len(st["buf"]) >= 4:
                self.chunk_size = int.from_bytes(st["buf"][:4], "big") & 0x7FFFFFFF
            st["_just_finished"] = True
            st["buf"] = bytearray()
        else:
            st["_just_finished"] = False
        return True


# ---------------------------------------------------------------------------
# Message 解读：把还原出的载荷翻译成可读信息
# ---------------------------------------------------------------------------

def describe_message(m):
    t, payload = m["type"], m["payload"]
    name = MSG_TYPE_NAMES.get(t, f"type-{t}")
    base = f"  ts={m['timestamp']:>8}ms  cs={m['cs_id']:<2} ms={m['ms_id']:<2} [{name}] {len(payload)}B"

    if t == 1:      # Set Chunk Size：载荷 4 字节大端
        return base + f"  -> chunk_size={int.from_bytes(payload[:4], 'big')}"
    if t == 5:      # Window Acknowledgement Size
        return base + f"  -> window={int.from_bytes(payload[:4], 'big')}"
    if t == 6:      # Set Peer Bandwidth：窗口 4B + 限制类型 1B
        return base + f"  -> window={int.from_bytes(payload[:4], 'big')} limit={payload[4]}"
    if t == 4:      # User Control：事件号 2B 起
        ev = int.from_bytes(payload[:2], "big")
        return base + f"  -> event={ev}"
    if t in (17, 20):
        # 命令消息：AMF0 序列 = 命令名, 事务ID, [命令对象], [参数...]
        vals = amf0_all(payload)
        head = vals[0] if vals else "?"
        tid = vals[1] if len(vals) > 1 else "?"
        extra = ""
        if head == "connect" and len(vals) > 2 and isinstance(vals[2], dict):
            extra = f" app={vals[2].get('app')}"
        if head in ("createStream",) and len(vals) > 3:
            extra = f" stream_id={vals[3]}"
        if head == "publish" and len(vals) > 4:
            extra = f" stream={vals[4]!r}"
        if head == "_result" and len(vals) > 3 and isinstance(vals[3], (int, float)):
            extra = f" stream_id={vals[3]}"
        return base + f"  -> {head} tid={tid}{extra}"
    if t in (15, 18):
        # 数据消息：@setDataFrame + onMetaData（ECMA Array 形式的元数据键值对）
        vals = amf0_all(payload)
        keys = []
        for v in vals:
            if isinstance(v, dict):
                keys = list(v.keys())[:8]
                break
        return base + f"  -> {vals[0] if vals else '?'} keys={keys}"
    if t == 9 and payload:
        # 视频：首字节 = FrameType(4bit)|CodecID(4bit)；AVC 时第二字节为包类型
        ft, cid = payload[0] >> 4, payload[0] & 0x0F
        pk = payload[1] if cid == 7 and len(payload) > 1 else None
        pk_name = {0: "seq-header", 1: "NALU", 2: "end-of-seq"}.get(pk, "?")
        return base + f"  -> frame_type={ft} codec={cid} avc_pkt={pk_name}"
    if t == 8 and payload:
        # 音频：首字节 = SoundFormat(4bit)|...；AAC 时第二字节为包类型
        sf = payload[0] >> 4
        pk = payload[1] if sf == 10 and len(payload) > 1 else None
        return base + f"  -> sound_format={sf} aac_pkt={'seq-header' if pk == 0 else 'raw' if pk == 1 else '-'}"
    return base


# ---------------------------------------------------------------------------
# 模式二：解析落盘文件
# ---------------------------------------------------------------------------

def parse_direction(path: Path, skip_handshake: int, tag: str):
    if not path.exists():
        print(f"\n===== {tag}：未找到 {path}，跳过 =====")
        return
    data = path.read_bytes()
    print(f"\n===== {tag} ({path.name}, {len(data)} bytes) =====")

    # ---- 握手（§5.2）：1 + 1536 + 1536 字节，逐字段验证
    if tag == "C->S":
        c0, c1, c2 = data[0], data[1:1537], data[1537:3073]
        print(f"handshake: C0 version={c0} (expect 3)")
        print(f"  C1 time={int.from_bytes(c1[:4], 'big')} zero={c1[4:8].hex()} random={len(c1) - 8}B")
        print(f"  C2 time(echo of S1)={int.from_bytes(c2[:4], 'big')} time2={int.from_bytes(c2[4:8], 'big')}")
    else:
        s0, s1, s2 = data[0], data[1:1537], data[1537:3073]
        print(f"handshake: S0 version={s0} (expect 3)")
        print(f"  S1 time={int.from_bytes(s1[:4], 'big')} zero={s1[4:8].hex()} random={len(s1) - 8}B")
        print(f"  S2 time(echo of C1)={int.from_bytes(s2[:4], 'big')} time2={int.from_bytes(s2[4:8], 'big')}")

    # ---- Chunk -> Message 还原
    parser = ChunkStreamParser(data, skip_handshake)
    msgs = parser.parse()
    print(f"chunk_size(final)={parser.chunk_size}, messages parsed={len(msgs)}")
    for m in msgs[:60]:
        print(describe_message(m))
    if len(msgs) > 60:
        print(f"  ... 其余 {len(msgs) - 60} 条（音视频数据为主）")

    # ---- 按类型汇总，直观感受「信令寥寥几条，数据成千上万」
    stats = {}
    for m in msgs:
        name = MSG_TYPE_NAMES.get(m["type"], f"type-{m['type']}")
        stats[name] = stats.get(name, 0) + 1
    summary = ", ".join(f"{k}×{v}" for k, v in
                        sorted(stats.items(), key=lambda kv: -kv[1]))
    print(f"summary: {summary}")


def run_parse():
    # 握手长度：C->S 方向为 C0+C1+C2 = 1+1536+1536；
    # S->C 方向为 S0+S1+S2，布局相同，跳过等量字节即可。
    parse_direction(C2S_FILE, 1537 + 1536, "C->S")
    parse_direction(S2C_FILE, 1 + 1536 + 1536, "S->C")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "parse"
    if mode == "proxy":
        run_proxy()
    else:
        run_parse()
