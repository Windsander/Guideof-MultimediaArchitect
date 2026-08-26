
# 八、解码与播放（Decoding & Playback）

## **引言**
第七章的结尾，我们许下了一个承诺：亲手造一台播放器。

先掂一掂这个承诺的分量。编码好的码流已经乘上容器与协议的快车抵达眼前，可它仍是一堆沉默的比特——H.264 的 NAL 单元躺在 FLV 的 Tag 里，AAC 的帧躲在 ADTS 头后面，等着一台机器把它们还原成光与声。这台机器的工作分两段：**解码**，按规格的逆运算把比特还原成帧；**播放**，按时间的纪律把帧交给感官。前一段有规格书可循，后一段却是纯工程的深水区——帧解对了只是及格，在对的时刻上屏才是满分。

有趣的是，这台机器的全部零件我们都已见过。第六章的编码四环，倒过来就是解码的流水线；第五章的 PTS，正是播放节拍的裁判；第七章的队列与背压，将在播放器管线里再度重演。本章要做的就是把这些散落的零件装成整机——沿 "解码器 → 播放器 → 实战" 的主线：先解剖解码器框架的本质、分层与状态机；再深入播放器核心的三个问题，看主时钟与抖动缓冲如何治理时间；最后用一场同步策略对比实验，让整章理论在数据里显影。

通过本章节的学习，读者将能够说清解码器框架的设计要素与 FFmpeg 六库的分工，讲透音画同步的主时钟机制与抖动缓冲的权衡，并能亲手搭建一台可复现的播放器仿真骨架。

>**关键字：解码器、FFmpeg、收发分离、PTS/DTS、音画同步、主时钟、抖动缓冲、渲染管线**

## **目录**
* [8.1 解码器框架设计（Decoder Framework Design）](Docs_8_1.md)
	* [8.1.1 从规格到代码：解码器的本质（From Spec to Code）](Docs_8_1_1.md)
	* [8.1.2 FFmpeg 六库：分层的艺术（The Six Libraries of FFmpeg）](Docs_8_1_2.md)
	* [8.1.3 收发分离：解码 API 的状态机（The Send/Receive State Machine）](Docs_8_1_3.md)
	* [8.1.4 管线与 seek：工程落地的暗坑（Pipelines, Seek & The Pitfalls）](Docs_8_1_4.md)
* [8.2 播放器核心系统（Player Core Systems）](Docs_8_2.md)
	* [8.2.1 播放器的三个问题：何时解，何时显，对谁齐（Three Questions of A Player）](Docs_8_2_1.md)
	* [8.2.2 音画同步：主时钟的三种策略（A/V Sync & The Three Master Clocks）](Docs_8_2_2.md)
	* [8.2.3 抖动缓冲：与网络和解的艺术（Jitter Buffer & The Art of Compromise）](Docs_8_2_3.md)
	* [8.2.4 渲染管线：从 YUV 到视网膜（The Render Pipeline）](Docs_8_2_4.md)
* [8.3 实战：音画同步策略对比实验（practice_9）](Docs_8_3.md)
* [8.4 本章小结与进阶指引（Summary & Roadmap）](Docs_8_4.md)
* [【在线展示】](Playground_8.md)
* [【参考文献】](References_8.md)
