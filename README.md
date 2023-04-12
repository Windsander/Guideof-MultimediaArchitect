# 《音视频开发技术：基础、架构与实践》

## **目的**

本书对音视频工程的各层级技框架与知识点，以由浅入深的解构剖析为主，将工程中所需要的数字信号处理、计算机图形学、色彩学、相关工程规格规范、软件工程及软件框架设计等专业领域学科知识的关键细节，从音视频工程师不同的技术阶段需要面临的问题为出发点，将全书分为三大梯度。每一梯度，统一采用知识图谱串联工程规格与编码实践，全面讲解对应阶段下需要掌握的音视频领域知识历史、原理、算法、设计的相关推导、制定、架构与应用。全书按照技术递进的关系，构成了整体音视频从数据分析、编解码器开发、播放器开发到图形化与图像处理、特效与特效引擎的完整技术栈。使得全书每个章节内部自成一体但确相互关联，从而便于做技术字典、工程手册和整体学习之用。

## **面向**

介于全书重点不在于从基础软件开发进行讲解，因此本书可供参考的门槛为：有一定软件工程实际开发经验、深入了解过平台原理（至少一种，不限于端类型）、对架构有一定程度接触的中高级软件工程师。

书中原理与技术面向全平台，因此主要开发语言为 C/C++。部分平台化及数据分析场景，会一定程度的应用到 C#、Java、Python 等其他语言。

## **难度导向**

### **入门：必需掌握的音视频基础，**
### **对应：入门/初级音视频工程师（T2-1～T2-3｜T5～T7）**

入门的四章也是概念与基础理论最多的章节了。这几张的工程实践较少，但非常重要的原理、规格、定义及多。是后续更为复杂的工程实践中，被音视频工程师们做为根基般的存在。因此非常重要。

	第一章 音视频常用基础算法，属于纯数理基础，对音视频开发过程中常用的 图像/音频 的 分析/处理 算法，进行了梳理和讲解；本章列出的部分，是作者在筛选掉大量非必需算法后的最小知识集合。

	第二章 数字音频的保存与还原，同上。

	第三章 图像色彩的运用与存储，从色彩学发展史到工业体系对色彩的规格定义，章节大章以工程概念的递进关系进行介绍，并在小章节中按照相关规格原理的发现提出时间顺序进行了由浅入深的推导说明。从而保证前后逻辑和发展上的连贯性。

	第四章 音视频的单帧与帧分析，是一个纯工程章节。这一章将对前三章里的知识点，在工程应用上，通过代码和实际操作来进行一次总结。

入门四章完成后，读者将有一定的音视频图像工程分析能力。并能够使用当前掌握的知识来处理音视频基本问题。

### **中级：流的编解码与网络传输，音视频工程常用框架与技术**
### **对应：中级音视频工程师、初级架构师（T3-1～T3-2｜T8～T9）**

	第五章 音视频解码与流传输，是一个综合性较强的章节。这一章将对当前编解码规格进行详细的拆分与解析。通过对 H.264、H.265、H.266 的规格分析，详细的阐述当今音视频工程中，如何对视频保质保量的进行数据压缩和处理。并通过对 主流三协议：RTMP、RTP/RTCP、HLS 的分析，从协议的封装、信号设计、传输过程、规格规定上全面说明了音视频传输过程的各个方面细节。完成本章，将会使读者较为深度的理解编解码与传输，并使其能够有一定程度的规格定制与改进能力。

	第六章 音视频的编解播与流分析，结合了第五章与入门四章的知识要领做工程实践。本章节将注重工程能力建设，从软件工程设计角度剖析音视频的编解播三大经典工程方案，并引导读者建立架构师思维与匹配的动手能力。

中级两章完成后，读者将能够胜任大部分业界的音视频项目工作需求，和一定程度的音视频架构师要求。

### **高级：图像处理技术与特效引擎**
### **对应：中级/高级架构师（T4-1～T4-2｜T10～T12）**

	第七章 图形驱动统一化的理论基础，是为后续章节开始进行的计算机图形处理，进行相关的理论基础铺垫与解析。中级/高级架构师，在工作内容上已不可避免会涉及到音视频2D、3D特效的处理与实践，并会较多的参与到 AI 技术工程化的框架设计工作中。因此，对于计算机图形学的了解是必要且必须的。

	第八章 图形驱动与渲染引擎技术，则是一个较为复杂的复合章节。本章结合作者开源工程实践（UltraDriver），在前面几章铺垫的基础上，深入驱动底层逻辑，剖析了常见渲染引擎的核心元素，并完整的讲解了从GPU通信管线建立到实际场景渲染的完整过程。完成本章，将会使读者对整个渲染驱动有详尽的理解，并能够独立运用GPU驱动特性完成复杂的 3D 渲染工作。

	第九章 音视频播放与特效编辑，结合作者开源工程实践（UltraTimeline），讲解了音视频编辑中的最为关键的技术系统：UTT 统一时间轴系统，通过此系统，读者将能够独立完成一系列复杂音视频的编辑过程。从而在音视频特效处理方面正式的进入工程大门。

高级三章完成后，后续的继续学习提升将脱离工程范畴。因此，更进一步的探索，就要求深入了解算法和硬件驱动，从而衔接到 AI-CV 等方面的相关研究工作，或游戏引擎物理引擎的开发架设。此两个方向的经典文献与著作较多，且已有成熟体系，因此本书既到此为止。

- - -

## **目录**

### 基础实践篇

* [一、音视频常用基础算法](Chapter_1/Language/cn/Apex_1_Introduce.md)
    * [1.1 信号分析的核心算法-傅立叶变换](Chapter_1/Language/cn/Docs_1_1.md)
        * [1.1.1 一维傅立叶（1D-FT）与一维离散傅立叶变换（1D-DFT）](Chapter_1/Language/cn/Docs_1_1_1.md)
        * [1.1.2 二维傅立叶（2D-FT）与二维离散傅立叶变换（2D-DFT）](Chapter_1/Language/cn/Docs_1_1_2.md)
        * [1.1.3 傅立叶变化的经典 - 快速傅立叶变换（FFT）](Chapter_1/Language/cn/Docs_1_1_3.md)
    * [1.2 傅里叶变换的概念延伸-常用滤波算法]()
        * [1.2.1 双边滤波（Bilateral Filter）]()
	    * [1.2.2 高斯滤波（Gauss Filter）]()
	    * [1.2.3 索贝尔滤波（Sobel Filter）]()
	    * [1.2.4 非极大值抑制（NMS [Non-Maximum Suppression]）]()
    * [1.3 时间冗余控制-常用区域检测与运动矢量算法]()
	    * [1.3.1 IoU & GIoU]()
	    * [1.3.2 方向梯度直方图（HOG [Histogram of Oriented Gradient]）]()
	    * [1.3.3 动量预测（Momentum Prediction）& 动量算法（Momentum Algorithm）]()
	    * [1.3.4 双向光流预测（BDOF [Bi-Directional Optical Flow]）]()
	    * [1.3.5 光流仿射修正（OFAC [Optical Flow Affine Correction]）]()
    * [1.4 空间冗余控制-常用图形变换算法]()
	    * [1.4.1 整数离散正余弦变换（DST/DCT）]()
	    * [1.4.2 哈达玛变换（Hadamard Product）]()
	    * [1.4.3 色度残差联合编码（JCCR [Joint Coding of Chroma Residuals]）]()
	    * [1.4.4 高频凋零 & 低频不可分变换（LFNST [Low-Frequency Non-Separable Transform]）]()
    * [1.5 数据离散传输-常用量化算法]()
	    * [1.5.1 标量量化（SQ [Scalar Quantization]）]()
	    * [1.5.2 矢量量化（VQ [Vector Quantization]）]()
	    * [1.5.3 率失真择优量化（RDOQ [Rate Distortion Optimized Quantization]）]()

* [三、色彩的运用与存储](Chapter_3/Language/cn/Apex_3_Introduce.md)
    * [3.1 色彩基础](Chapter_3/Language/cn/Docs_3_1.md)
    * [3.2 颜色三要素（Three Elements of Color）](Chapter_3/Language/cn/Docs_3_2.md)
	    * [3.2.1 色调（Hue）](Chapter_3/Language/cn/Docs_3_2_1.md)
	    * [3.2.2 光亮度（Luminance）](Chapter_3/Language/cn/Docs_3_2_2.md)
	    * [3.2.3 饱和度（Saturation）](Chapter_3/Language/cn/Docs_3_2_3.md)
    * [3.3 色彩的衡量](Chapter_3/Language/cn/Docs_3_3.md)
    	* [3.3.1 配色函数（Color Matching Functions ）](Chapter_3/Language/cn/Docs_3_3_1.md)
	    * [3.3.2 色彩空间（Color Space ）](Chapter_3/Language/cn/Docs_3_3_2.md)
	    * [3.3.3 经典三原色函数（Trichromatic Primaries Functions）](Chapter_3/Language/cn/Docs_3_3_3.md)
	    * [3.3.4 经典三刺激函数（Tristimulus Values Functions）](Chapter_3/Language/cn/Docs_3_3_4.md)
	    * [3.3.5 现代色彩体系（Modern Color System）](Chapter_3/Language/cn/Docs_3_3_5.md)
    * [3.4 色彩的对比](Chapter_3/Language/cn/Docs_3_4.md)
	    * [3.4.1 色域（Color Gamut ）](Chapter_3/Language/cn/Docs_3_4_1.md)
	    * [3.4.2 色度（Chroma）& 色度平面（Chroma Plane）& 色度图（Chroma Diagram）](Chapter_3/Language/cn/Docs_3_4_2.md)
	    * [3.4.3 色差（Chromatic Aberration）](Chapter_3/Language/cn/Docs_3_4_3.md)
	    * [3.4.4 色温（Color Temperature）& 相关色温（Correlated Color Temperature）](Chapter_3/Language/cn/Docs_3_4_4.md)
	    * [3.4.5 标准光源（Standard Illuminants）& 白点（White Point）](Chapter_3/Language/cn/Docs_3_4_5.md)
	    * [3.4.6 显色指数（Color Rendering Index）](Chapter_3/Language/cn/Docs_3_4_6.md)
    * [3.5 经典色彩空间（Classical Color Space）](Chapter_3/Language/cn/Docs_3_5.md)
	    * [3.5.1 光学三原色色彩空间（RGB）](Chapter_3/Language/cn/Docs_3_5_1.md)
	    * [3.5.2 颜料三原色色彩空间（CMY / CMYK ）](Chapter_3/Language/cn/Docs_3_5_2.md)
	    * [3.5.3 CIE RGB 色彩空间（CIE 1931 RGB Color Space）](Chapter_3/Language/cn/Docs_3_5_3.md)
	    * [3.5.4 CIE XYZ 色彩空间（CIE 1931 XYZ Color Space）](Chapter_3/Language/cn/Docs_3_5_4.md)
	    * [3.5.5 CIE LAB 色彩空间（CIE 1976 L*, a*, b* Color Space）](Chapter_3/Language/cn/Docs_3_5_5.md)
	    * [3.5.6 CIE LUV 色彩空间（CIE 1976 L*, u*, v* Color Space）](Chapter_3/Language/cn/Docs_3_5_6.md)
	    * [3.5.7 颜色三要素色彩空间（HSV / HSI / HSL）](Chapter_3/Language/cn/Docs_3_5_7.md)
    * [3.6 色彩的存储](Chapter_3/Language/cn/Docs_3_6.md)
	    * [3.6.1 色彩格式（Color Format）与色彩存储](Chapter_3/Language/cn/Docs_3_6_1.md)
	    * [3.6.2 RGB 体系色彩格式](Chapter_3/Language/cn/Docs_3_6_2.md)
	    * [3.6.3 YUV 体系色彩格式](Chapter_3/Language/cn/Docs_3_6_3.md)