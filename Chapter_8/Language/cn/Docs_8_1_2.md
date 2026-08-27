
# 8.1.2 FFmpeg 六库：分层的艺术（The Six Libraries of FFmpeg）

上一节结尾预告了这套 "事实标准"。它的主人公是 FFmpeg：诞生于 2000 年的开源老兵，二十余年后依然是音视频工程的公共地基，从播放器到转码云，从浏览器到监控摄像头，它的代码跑在几乎每一块能出声的屏幕上。我们解剖它的架构，不只是学一个库，而是学一套被亿级设备验证过的分层方法论。

## **六库职责：官方自述**

FFmpeg 把编解播的全部工作切给六个库，每个库的自我定位都写在头文件开篇 [\[1\]][ref]：

| 库 | 官方自述 | 一句话职责 |
|---|---|---|
| libavformat | "I/O and Muxing/Demuxing Library" | 字节从哪来、属于哪条流 |
| libavcodec | "Encoding/Decoding Library" | 压缩与原始之间的变换 |
| libavutil | 基础设施核心 | 帧、缓冲、时间基、数学，全家共享的地基 |
| libswscale | "Color conversion and scaling library" | 像素格式转换与缩放 |
| libswresample | "Audio resampling, sample format conversion and mixing library" | 音频重采样、采样格式转换与混音 |
| libavfilter | "Graph-based frame editing library" | 以图组织的帧加工 |

## **分层正交：知识地图的工程落点**

这张表最值得细品的是 **正交性**：avformat 对编码一无所知，它解封装出压缩包，从不过问包里是 H.264 还是 AV1；avcodec 对容器一无所知，它拿到包就解码，从不过问包来自 MP4 还是网络流。像素与采样的格式适配，则独立成 swscale 与 swresample 两个 "转换专库"，不与任何一侧耦合 [\[1\]][ref]。

把本书前半的知识地图叠上去，落点严丝合缝：**第七章的容器学问，全部住进 avformat；第六章的编码规格，全部住进 avcodec**，理论学习在工程世界里的坐标，一清二楚。分层的红利也随之兑现：新增一种容器，只需注册一个 demuxer；新增一种编码，只需注册一个 decoder，其余五库纹丝不动。FFmpeg 能以一己之力覆盖数百种格式，靠的就是这道正交切缝。

## **一次播放的六库协作**

播一个文件时，数据沿分工链依次过手：

<center><b>文件/网络 → avformat 解封装出 Packet → avcodec 解码出 Frame → swscale/swresample 格式适配 →（avfilter 可选加工） → 渲染上屏</b></center>

两个数据类型是链上的通用货币：**Packet（压缩包）** 是 avformat 与 avcodec 之间的交接物，**Frame（原始帧）** 是 avcodec 与后续环节的交接物，两者连同时间基、像素格式等公共约定，都定义在 avutil 里。看懂 "Packet 向右、Frame 向下" 的流向，FFmpeg 的 API 就不再是几百个函数的迷宫，而是这条流水线上的一组工位。

六库分层把 "编解播" 这头巨兽切成了六块各自独立的拼图：解封装、编解码、基础设施、图像转换、音频转换、帧加工。复杂性没有消失，但被关进了各自的笼子。笼子之间最微妙的一道接口（avcodec 的输入输出）值得单独细看：8.1.3，收发分离 API 背后的状态机智慧。

[ref]: References_8.md
