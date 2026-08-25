
# 六、音视频编码规格（Audio & Video Codec Specification）

## **引言**
在第五章的结尾，我们留下了一个悬而未决的问题：已经学会如何看懂一帧、如何改变一帧，那么，该如何高效地 "存下" 一百万帧？

先感受一下问题的量级。一段两小时的 1080p 影片，以 25 fps、YUV 4:2:0、8 bit 存储，原始体积约为：

$$
1920 \times 1080 \times 1.5 \ \mathrm{Bytes} \times 25 \ \mathrm{fps} \times 7200 \ \mathrm{s} \approx 560 \ \mathrm{GB}
$$

对应码率约 622 Mbit/s。而今天我们在流媒体上观看同等规格的影片，实际传输码率往往只有 5 Mbit/s 上下——上百倍的差距，靠的便是音视频编码技术。

**编码规格（Codec Specification）** 是这场 "减法" 的官方说明书。它并不规定编码器内部如何实现，而是严格定义 **解码器必须能够还原的码流格式**——只要码流合规，任何厂商的解码器都能正确还原画面与声音。正是这份 "契约"，让内容得以跨设备、跨平台、跨年代地流通。

本章将沿编年史展开：从奠定混合编码框架的 H.261 出发，途经 MPEG-1/2 的存储时代、H.264 的网络时代、H.265 的 4K 时代，直到 H.266/VVC 与 AV1 的当代格局；音频侧则沿 MP3、AAC、Opus 的脉络，梳理编码思想的另一条进化线。我们将看到，四十年来编码的顶层框架几乎未变，**进化的只是框架中每一个环节的工具精度**。

通过本章节的学习，读者将能够说清主流编码规格的代际脉络与技术分工，读懂编码器的标准工作流程，并能亲手测量不同编码器的压缩效率差异。

>**关键字：视频编码、H.26x、MPEG、混合编码、编码四环、率失真**

## **目录**
* [6.1 编码简史与编码四环（Codec History & The Four-Stage Framework）](Docs_6_1.md)
	* [6.1.1 视频编码编年简史（A Chronology of Video Coding Standards）](Docs_6_1_1.md)
	* [6.1.2 压缩何以可能：四类冗余（Four Types of Redundancy）](Docs_6_1_2.md)
	* [6.1.3 编码四环：混合编码框架（The Hybrid Coding Framework）](Docs_6_1_3.md)
* [6.2 H.264/AVC：经典之巅（H.264/AVC in Detail）](Docs_6_2.md)
	* [6.2.1 诞生背景：JVT 与混合框架的成熟](Docs_6_2_1.md)
	* [6.2.2 帧内预测（Intra Prediction）](Docs_6_2_2.md)
	* [6.2.3 帧间预测与运动补偿（Inter Prediction & Motion Compensation）](Docs_6_2_3.md)
	* [6.2.4 变换、量化与熵编码（Transform, Quantization & Entropy Coding）](Docs_6_2_4.md)
	* [6.2.5 Profile/Level 体系与规格导读](Docs_6_2_5.md)
* [6.3 H.265/HEVC：4K 时代的答案（H.265/HEVC in Detail）](Docs_6_3.md)
	* [6.3.1 编码树单元：CTU 与四叉树划分（Coding Tree Unit & Quadtree）](Docs_6_3_1.md)
	* [6.3.2 预测技术的演进（Evolution of Prediction）](Docs_6_3_2.md)
	* [6.3.3 环路滤波与并行化设计（In-loop Filtering & Parallelism）](Docs_6_3_3.md)
* [6.4 H.266/VVC 与 AV1：两条路线的竞赛（H.266/VVC & AV1）](Docs_6_4.md)
	* [6.4.1 VVC：向压缩极限推进（Versatile Video Coding）](Docs_6_4_1.md)
	* [6.4.2 AV1：开源免版税阵营（AOMedia Video 1）](Docs_6_4_2.md)
	* [6.4.3 专利池生态与三代规格对照（Patent Ecosystem & Comparison）](Docs_6_4_3.md)
* [6.5 音频编码规格（Audio Codec Specification）](Docs_6_5.md)
	* [6.5.1 心理声学：音频压缩的地基（Psychoacoustics）](Docs_6_5_1.md)
	* [6.5.2 MP3：开启数字音乐时代（MPEG-1 Layer III）](Docs_6_5_2.md)
	* [6.5.3 AAC：青出于蓝（Advanced Audio Coding）](Docs_6_5_3.md)
	* [6.5.4 Opus：为实时互动而生（Opus, RFC 6716）](Docs_6_5_4.md)
* [6.6 实战：编码器规格对比实验（practice_7）](Docs_6_6.md)
* [6.7 本章小结与进阶指引（Summary & Roadmap）](Docs_6_7.md)
* [【在线展示】](Playground_6.md)
* [【参考文献】](References_6.md)
