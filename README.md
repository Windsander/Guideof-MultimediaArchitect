# 《音视频开发技术：原理与实践》©

<p align='left'>
<a href="https://github.com/Windsander" target="_blank"><img src="https://img.shields.io/badge/%E4%BD%9C%E8%80%85-%E6%9D%8E%E8%BF%B0%E5%8D%9A-000000.svg?style=flat&logo=GitHub"></a>
<a href="https://www.zhihu.com/people/ArikanLi" target="_blank"><img src="https://img.shields.io/badge/%E5%B0%8F%E5%B2%9B%E4%B8%8A%E7%9A%84%E9%BB%91%E6%A1%83%E5%85%AD-Arikan.Li-000000.svg?style=flat&logo=zhihu"></a>
<a href="https://github.com/Windsander/Guideof-MultimediaArchitect" target="_blank"><img alt="GitBook" src="https://img.shields.io/github/stars/Windsander/Guideof-MultimediaArchitect?label=Stars&style=flat&logo=GitBook"></a>
</p>

[<font color=oragan> =[>> 关于作者© <<]= </font>](AUTHOR.md)

[<font color=oragan> =[>> 赞助本作© <<]= </font>](DONATE.md)

[<font color=red> =[>> 版权申明© <<]= </font>](COPYRIGHT.md)

## **目标**

对于音视频工程师/架构师来说，日常工作长中总会有大量的知识技术积累，亟待梳理以期望能够被快速检索查阅。但由于工程技术所处领域的复合特征，往往针对一个工程问题所需要的专业知识，不论深浅程度，都会横跨几门学科。而想要获取有效的处理问题所能使用的信息，都需要依次回顾、搜集和关联。这样必不可少会花费大量时间查阅各类大部头资料和文献。而这么做往往是因为，对于待解答问题非常重要的知识点，分布碎片化导致的。

**音视频规格的跨度构成了本身技术的多个维度，使得我们并不能按照以往的工程思维，从单一角度来考虑涉及此类型的复合问题**。

因此，本书的目的旨在以工程解决方案的实践思路过程，对相关联的各学科核心知识进行串联。以求用一套完整且关联的技术栈模板，来贯穿当下多媒体技术的所有核心技术模块。从而 **为读者提供针对多媒体（音视频）分析/处理/整合/架构方面，有效技术指导与学习路线**。

## **特色**

本书结合作者工作实践，对架构师日常工作工程中涉及使用到的：数字信号处理、计算机图形学、色彩学、相关工程规格规范、驱动特征及软件框架设计等，领域的专业学科知识进行了梳理和提炼。从音视频工程师不同的技术阶段需要面临的问题为出发点，将

全书分为，**音视频基础与音视分析**、**流媒体规格与简易编解码播放框架设计**、**通用统一化音视频编辑框架与渲染驱动设计**，三大阶段。每一阶段，统一采用知识图谱串联工程规格与编码实践，全面讲解对应技术阶段下需要掌握的，多媒体（音视频）技术之简史、原理、算法、设计及相关推导、制定、架构与应用。

基于此，全书按照技术逐级递进的关系，构成了整体音视频从数据分析、编解码器开发、播放器开发到图形化与图像处理、特效与特效引擎的 **完整技术栈**。使得全书每个章节内部自成一体但确相互关联，从而便于做技术字典、工程手册和整体学习之用。

## **面向**

书中原理与技术面向全平台，因此主要开发语言为 C/C++。部分平台化及数据分析场景，会一定程度的应用到 C#、Java、Python 等其他语言。本书适合：
- **初入音视频开发的新手**：
本书为您提供了完整学习路径，对于打算初入本行业的开发者，本书能够帮您梳理完整的音视频开发技术路线。协助您成功入行。

- **有基础的音视频工程师**：
本书为您提供了知识技术字典，对于日常开发工作中涉及到的相关问题分析，本书能够帮您快速定位到所需要的核心知识点，进而方便您进一步根据所给信息来做出判断，或根据提示方向来进行深度资料查阅。

- **多媒体编解开发者友好**：
本书为您提供了ITU-T的编解码协议技术索引和讲解，您可以快速通过本书查阅常用 **H.264、H.265、H.266** 的关键资料和技术对比。

- **流媒体协议开发者友好**：
本书为您提供了常用流协议的拆分解析，您可以快速通过本书查阅常用 **RTP/RTCP、RTMP、HLS** 的规格设定和消息类型。

- **学研成果转向生产部署**：
本书为您提供了理论转实践的事例方案，对于将研究成果转换到实际工业生产活动的老师，本书能够为您介绍一些现已有成功实践的多媒体方面学转产探索。协助您梳理思路。

- **硬核的多媒体技术大咖**：
若您是深耕此领域多年的老师，您不妨将本书当作一次有趣的思维之旅，从不同的视角感受音视频工程魅力，希望本书能为您提供一些帮助。当然，也更希望获得您的交流。

**为方便您定位章节难度，此处提供 [<font color=red> =[>> 难度向导 <<]= </font>](GUIDER.md) 建议。**

受限于作者，本书难免存在一些不足，您可以 **[Book-issues](https://github.com/Windsander/Guideof-MultimediaArchitect/issues)** 进行反馈，感谢您的帮助！

- - -

## **目录**

### 音视频工程基础

* [一、数字音频的保存与还原](Chapter_2/Language/cn/Apex_2_Introduce.md)
    * [1.1 音频基础](Chapter_2/Language/cn/Docs_2_1.md)
	* [1.2 音频三要素（Three Elements of Audio）]()
		* [1.2.1 幅度 & 响度（Volume）]()
		* [1.2.2 频率 & 音调（Pitch）]()
		* [1.2.3 波形 & 音色（Timbre）]()
	* [1.3 音频的解构]()
		* [1.3.1 时域图（Time Domain Graph） & 频域图（Frequency Domain Graph）]()
		* [1.3.2 频谱图（Spectrogram）]()
		* [1.3.3 主观调性（Tone）& 调性网络（Tonnetz）]()
	* [1.4 音频的采样与调制]()
		* [1.4.1 数字信号（Digital Signal）& 模拟信号（Analog Signal）]()
		* [1.4.3 采样率（Sample Rate） & 采样位深（Bit Depth） & 采样声道（Channel）]()
		* [1.4.2 脉冲编码调制（PCM [Pulse-Code Modulation]）]()
		* [1.4.3 脉冲密度调制（PDM [Pulse-Density Modulation]）]()
	* [1.5 音频的存储]()
		* [1.5.1 音频格式（Audio Format）]()
		* [1.5.2 无压缩编码格式（Uncompressed Encode）]()
		* [1.5.3 无损压缩编码格式（Lossless Encode）]()
		* [1.5.4 有损压缩编码格式（Uncompressed Encode）]()

<br>

* [二、色彩的运用与存储](Chapter_2/Language/cn/Apex_2_Introduce.md)
    * [2.1 色彩基础](Chapter_2/Language/cn/Docs_2_1.md)
    * [2.2 颜色三要素（Three Elements of Color）](Chapter_2/Language/cn/Docs_2_2.md)
	    * [2.2.1 色调（Hue）](Chapter_2/Language/cn/Docs_2_2_1.md)
	    * [2.2.2 饱和度（Saturation）](Chapter_2/Language/cn/Docs_2_2_2.md)
	    * [2.2.3 光亮度（Luminance）](Chapter_2/Language/cn/Docs_2_2_3.md)
    * [2.3 色彩的衡量](Chapter_2/Language/cn/Docs_2_3.md)
    	* [2.3.1 辐射亮度（Radiance）& 色温（Color Temperature）& 颜色的量化](Chapter_2/Language/cn/Docs_2_3_1.md)
	    * [2.3.2 配色函数（Color Matching Functions）& 色彩空间（Color Space）](Chapter_2/Language/cn/Docs_2_3_2.md)
	    * [2.3.3 经典三原色函数（Trichromatic Primaries Functions）](Chapter_2/Language/cn/Docs_2_3_3.md)
	    * [2.3.4 经典三刺激函数（Tristimulus Values Functions）](Chapter_2/Language/cn/Docs_2_3_4.md)
	    * [2.3.5 现代色彩体系（Modern Color System）](Chapter_2/Language/cn/Docs_2_3_5.md)
    * [2.4 色彩的对比](Chapter_2/Language/cn/Docs_2_4.md)
	    * [2.4.1 色域（Color Gamut ）](Chapter_2/Language/cn/Docs_2_4_1.md)
	    * [2.4.2 色度（Chroma）& 色度平面（Chroma Plane）& 色度图（Chroma Diagram）](Chapter_2/Language/cn/Docs_2_4_2.md)
	    * [2.4.3 色差（Chromatic Aberration）](Chapter_2/Language/cn/Docs_2_4_3.md)
	    * [2.4.4 色温（Color Temperature）& 相关色温（Correlated Color Temperature）](Chapter_2/Language/cn/Docs_2_4_4.md)
	    * [2.4.5 标准光源（Standard Illuminants）& 白点（White Point）](Chapter_2/Language/cn/Docs_2_4_5.md)
	    * [2.4.6 显色指数（Color Rendering Index）](Chapter_2/Language/cn/Docs_2_4_6.md)
    * [2.5 经典色彩空间（Classical Color Space）](Chapter_2/Language/cn/Docs_2_5.md)
	    * [2.5.1 光学三原色色彩空间（RGB）](Chapter_2/Language/cn/Docs_2_5_1.md)
	    * [2.5.2 颜料三原色色彩空间（CMY / CMYK ）](Chapter_2/Language/cn/Docs_2_5_2.md)
	    * [2.5.3 CIE RGB 色彩空间（CIE 1931 RGB Color Space）](Chapter_2/Language/cn/Docs_2_5_3.md)
	    * [2.5.4 CIE XYZ 色彩空间（CIE 1931 XYZ Color Space）](Chapter_2/Language/cn/Docs_2_5_4.md)
	    * [2.5.5 CIE LAB 色彩空间（CIE 1976 L\*, a\*, b\* Color Space）](Chapter_2/Language/cn/Docs_2_5_5.md)
	    * [2.5.6 CIE LUV 色彩空间（CIE 1976 L\*, u\*, v\* Color Space）](Chapter_2/Language/cn/Docs_2_5_6.md)
	    * [2.5.7 颜色三要素色彩空间（HSV / HSI / HSL）](Chapter_2/Language/cn/Docs_2_5_7.md)
    * [2.6 色彩的存储](Chapter_2/Language/cn/Docs_2_6.md)
	    * [2.6.1 色彩格式（Color Format）与色彩存储](Chapter_2/Language/cn/Docs_2_6_1.md)
	    * [2.6.2 RGB 体系色彩格式](Chapter_2/Language/cn/Docs_2_6_2.md)
	    * [2.6.3 YUV 体系色彩格式](Chapter_2/Language/cn/Docs_2_6_3.md)
	* [【参考文献】](Chapter_2/Language/cn/References_2.md)

<br>

* [三、音视频常用基础算法](Chapter_3/Language/cn/Apex_3_Introduce.md)
    * [3.1 信号分析的核心算法 - 傅立叶变换](Chapter_3/Language/cn/Docs_3_1.md)
        * [3.1.1 一维傅立叶（1D-FT）与一维离散傅立叶变换（1D-DFT）](Chapter_3/Language/cn/Docs_3_1_1.md)
        * [3.1.2 二维傅立叶（2D-FT）与二维离散傅立叶变换（2D-DFT）](Chapter_3/Language/cn/Docs_3_1_2.md)
        * [3.1.3 傅立叶变化的经典 - 快速傅立叶变换（FFT）](Chapter_3/Language/cn/Docs_3_1_3.md)
		* [3.1.4 傅里叶的硬件优化 - 多常数乘法矩阵逼近（Matrix-MCM Approach）](Chapter_3/Language/cn/Docs_3_1_4.md)
    * [3.2 频率信息提取 - 常用滤波算法](Chapter_3/Language/cn/Docs_3_2.md)
	    * [3.2.1 高斯滤波（Gauss Filter）](Chapter_3/Language/cn/Docs_3_2_1.md)
        * [3.2.2 双边滤波（Bilateral Filter）](Chapter_3/Language/cn/Docs_3_2_2.md)
	    * [3.2.3 拉普拉斯滤波（Laplacian Filter）](Chapter_3/Language/cn/Docs_3_2_3.md)
	    * [3.2.4 马尔滤波（Marr Filter）](Chapter_3/Language/cn/Docs_3_2_4.md)
	    * [3.2.5 索贝尔滤波（Sobel Filter）](Chapter_3/Language/cn/Docs_3_2_5.md)
	    * [3.2.6 非极大值抑制（NMS [Non-Maximum Suppression]）](Chapter_3/Language/cn/Docs_3_2_6.md)
    * [3.3 时间冗余控制 - 常用区域检测与运动矢量算法]()
	    * [3.3.1 IoU & GIoU]()
	    * [3.3.2 方向梯度直方图（HOG [Histogram of Oriented Gradient]）]()
	    * [3.3.3 动量预测（Momentum Prediction）& 动量算法（Momentum Algorithm）]()
	    * [3.3.4 双向光流预测（BDOF [Bi-Directional Optical Flow]）]()
	    * [3.3.5 光流仿射修正（OFAC [Optical Flow Affine Correction]）]()
    * [3.4 空间冗余控制 - 常用图形变换算法]()
	    * [3.4.1 整数离散正余弦变换（DST/DCT）]()
	    * [3.4.2 哈达玛变换（Hadamard Product）]()
	    * [3.4.3 色度残差联合编码（JCCR [Joint Coding of Chroma Residuals]）]()
	    * [3.4.4 高频凋零 & 低频不可分变换（LFNST [Low-Frequency Non-Separable Transform]）]()
    * [3.5 数据离散传输 - 常用量化算法]()
	    * [3.5.1 标量量化（SQ [Scalar Quantization]）]()
	    * [3.5.2 矢量量化（VQ [Vector Quantization]）]()
	    * [3.5.3 率失真择优量化（RDOQ [Rate Distortion Optimized Quantization]）]()
    * [【参考文献】](Chapter_3/Language/cn/References_3.md)

<br>

* [四、音视频的单帧与帧分析]()
	* [4.1 单帧的概念]()
		* [4.1.1 音频帧（Chunk）& 视频帧（Frame）]()
		* [4.1.2 时间戳（Timestamp）]()
	* [4.1 常用分析工具介绍]()
		* [4.1.1 视频分析 StreamEye & YUV-Viewer]()
		* [4.1.2 音频分析 Audacity & Sonic Visualizer]()
	* [4.2 常用分析 Python 库介绍]()
		* [4.2.1 常用 Python 数学库（Numpy、Pandas、Mateplotlib）]()
		* [4.2.2 视频分析库 ffmpeg-py、color-science]()
		* [4.2.3 音频分析库 librosa]()
	* [4.3 通过 Python 的手写程序片处理]()
		* [4.3.1 搭建基本分析环境]()
		* [4.3.2 分析一段音频]()
		* [4.3.3 分析一段视频]()


<br>
<br>

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。<br />
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.