
# 七、封装格式与流传输协议（Container Formats & Streaming Protocols）

## **引言**
在第六章的结尾，我们留下了一个新的问题：比特已经压缩好，那么，该如何让它跨越网络，抵达每一块屏幕？

先感受一下这段旅程的艰险。一场 1080p 球赛直播，码率按 6 Mbit/s 计，九十分钟就是约 4 GB 的比特流。它们要穿过拥塞的公网、翻越 NAT 与防火墙、在时延与抖动里保持队形，最后准点落在千万块屏幕上——晚到几秒，欢呼声就输给了邻居家的电视。完成这套运输工作的，是本章的两位主角：**封装格式** 负责把码流组织成可存储、可寻址、可复用的容器；**流传输协议** 负责把容器里的内容安全、及时地送过网络。

有趣的是，这两位主角都不是 "后来发明" 的。容器的历史几乎与数字视频同龄——QuickTime 的 Box 结构今天仍是 MP4 的骨架；协议则是一部浓缩的互联网演进史——从组播时代的 RTP，到 Flash 王朝的 RTMP，再到 HTTP 化的 HLS/DASH 与万物实时的 WebRTC。每一项设计背后，都刻着它诞生年代的网络条件与商业格局。读协议，亦是读史。

本章沿 "容器 → 传输 → 实战" 的主线展开：先解剖 MP4、FLV、MPEG-TS 三种容器的设计取向；再按编年顺序遍历五代流传输协议，看清 "可靠性 - 实时性 - 生态" 天平上的不同配重；最后用两个动手实验，把整章规则按进真实流量里检验。

通过本章节的学习，读者将能够说清主流容器与传输协议的代际脉络与设计取舍，读懂 RTMP、HLS 的报文结构，并能亲手抓包分析一路真实的推流会话。

>**关键字：封装格式、MP4、FLV、MPEG-TS、RTP、RTMP、HLS、DASH、WebRTC、SRT**

## **目录**
* [7.1 从封装说起：容器的使命（The Mission of Containers）](Docs_7_1.md)
	* [7.1.1 裸码流缺什么（What Elementary Streams Lack）](Docs_7_1_1.md)
	* [7.1.2 MP4：为随机访问而生的索引树（MP4 & The Index Tree）](Docs_7_1_2.md)
	* [7.1.3 FLV：为流式传输而生的标签序列（FLV & The Tag Stream）](Docs_7_1_3.md)
	* [7.1.4 MPEG-TS：为容错传输而生的定长包（MPEG-TS & The Fixed-Length Packets）](Docs_7_1_4.md)
	* [7.1.5 三容器设计取向对比（Three Containers, Three Philosophies）](Docs_7_1_5.md)
* [7.2 实时传输奠基：RTP/RTCP（The Foundation of Real-Time Transport）](Docs_7_2.md)
	* [7.2.1 实时传输的诞生与 UDP 的取舍（Real-Time Transport & The UDP Trade-off）](Docs_7_2_1.md)
	* [7.2.2 RTP 固定头：十二字节的自描述（The 12-Byte Self-Describing Header）](Docs_7_2_2.md)
	* [7.2.3 RTCP：质量反馈环与唇同步（RTCP: Feedback Loop & Lip Sync）](Docs_7_2_3.md)
	* [7.2.4 从 RTP 到 WebRTC（From RTP to WebRTC）](Docs_7_2_4.md)
* [7.3 直播时代的霸主：RTMP（RTMP & The Live Streaming Dynasty）](Docs_7_3.md)
	* [7.3.1 Flash 时代的直播王朝（The Flash-Era Live Dynasty）](Docs_7_3_1.md)
	* [7.3.2 握手：C0/C1/C2 与 S0/S1/S2（The RTMP Handshake）](Docs_7_3_2.md)
	* [7.3.3 Chunk 封包：一次消息，多次封装（Chunking & Header Compression）](Docs_7_3_3.md)
	* [7.3.4 Message 类型族与 AMF 编码（Message Types & AMF Encoding）](Docs_7_3_4.md)
	* [7.3.5 命令消息与流管理时序（Commands & Stream Management）](Docs_7_3_5.md)
* [7.4 直播的 HTTP 化：HLS 与 fMP4（HLS & Fragmented MP4）](Docs_7_4.md)
	* [7.4.1 把直播搬进 HTTP（Moving Live Streaming into HTTP）](Docs_7_4_1.md)
	* [7.4.2 两级播放列表：Master 与 Media（Master & Media Playlists）](Docs_7_4_2.md)
	* [7.4.3 分片机制与直播滑动窗（Segments & The Sliding Window）](Docs_7_4_3.md)
	* [7.4.4 自适应码率：客户端的切换艺术（Adaptive Bitrate Switching）](Docs_7_4_4.md)
	* [7.4.5 延迟之战与 LL-HLS（The Latency Battle & LL-HLS）](Docs_7_4_5.md)
* [7.5 现代协议群像：DASH、WebRTC 与 SRT（The Modern Protocol Landscape）](Docs_7_5.md)
	* [7.5.1 DASH：标准化的另一极（MPEG-DASH & The Standards Track）](Docs_7_5_1.md)
	* [7.5.2 WebRTC：RTP 的正统继承者（WebRTC & The Real-Time Heir）](Docs_7_5_2.md)
	* [7.5.3 SRT：弱网回传的 ARQ 路线（SRT & The ARQ Prescription）](Docs_7_5_3.md)
	* [7.5.4 编年史与全景对照（A Chronicle & The Big Picture）](Docs_7_5_4.md)
* [7.6 实战：推流抓包与低延迟拉流（practice_8）](Docs_7_6.md)
* [7.7 本章小结与进阶指引（Summary & Roadmap）](Docs_7_7.md)
* [【在线展示】](Playground_7.md)
* [【参考文献】](References_7.md)
