
# 一、音视频常用基础算法

## **引言**
音视频中最为重要的组成部分，即是音频处理和视频处理。

音频处理应用到的基础理论，来源自：数字信号处理（Digital Signal Process）、数字合成音效（Digital Audio Effects）、语音识别（Voice Recognition）等领域。视频处理应用到的基础理论，来源自：数字信号处理（Digital Signal Process）、计算机图形学（Computer Graphics）、计算机视觉（Computer Vision）等领域。

这些学科在工程中或多或少的交叉使用，甚至本身大都为交叉学科，但最为核心的始终只有两个，即数字信号处理（DSP）和计算机图形学（CG）。所以，在正式开始学习音视频工程技术之前，首先需要回顾部分基础算法的工程特征。

本章节主要对此简单梳理（非数理、非推倒），并结合伪码和 C/C++ 工程汇总说明。可以做为最小集合的背景算法知识字典，供开发过程中查阅回顾使用。

>**关键字：傅立叶变换、滤波算法、区域检测、光流补正、冗余控制**

## **目录**
* [1.1 信号分析的核心算法 - 傅立叶变换](Docs_1_1.md)
    * [1.1.1 一维傅立叶（1D-FT）与一维离散傅立叶变换（1D-DFT）](Docs_1_1_1.md)
    * [1.1.2 二维傅立叶（2D-FT）与二维离散傅立叶变换（2D-DFT）](Docs_1_1_2.md)
    * [1.1.3 傅立叶变化的经典 - 快速傅立叶变换（FFT）](Docs_1_1_3.md)
	* [1.1.4 傅里叶的硬件优化 - 多常数乘法矩阵逼近（Matrix-MCM Approach）](Docs_1_1_4.md)
* [1.2 频率信息提取 - 常用滤波算法](Docs_1_2.md)
    * [1.2.1 高斯滤波（Gauss Filter）](Docs_1_2_1.md)
	* [1.2.2 双边滤波（Bilateral Filter）](Docs_1_2_2.md)
	* [1.2.3 索贝尔滤波（Sobel Filter）](Docs_1_2_3.md)
	* [1.2.4 非极大值抑制（NMS [Non-Maximum Suppression]）](Docs_1_2_4.md)
* [1.3 时间冗余控制 - 常用区域检测与运动矢量算法]()
	* [1.3.1 IoU & GIoU]()
	* [1.3.2 方向梯度直方图（HOG [Histogram of Oriented Gradient]）]()
	* [1.3.3 动量预测（Momentum Prediction）& 动量算法（Momentum Algorithm）]()
	* [1.3.4 双向光流预测（BDOF [Bi-Directional Optical Flow]）]()
	* [1.3.5 光流仿射修正（OFAC [Optical Flow Affine Correction]）]()
* [1.4 空间冗余控制 - 常用图形变换算法]()
	* [1.4.1 整数离散正余弦变换（DST/DCT）]()
	* [1.4.2 哈达玛变换（Hadamard Product）]()
	* [1.4.3 色度残差联合编码（JCCR [Joint Coding of Chroma Residuals]）]()
	* [1.4.4 高频凋零 & 低频不可分变换（LFNST [Low-Frequency Non-Separable Transform]）]()
* [1.5 数据离散传输 - 常用量化算法]()
	* [1.5.1 标量量化（SQ [Scalar Quantization]）]()
	* [1.5.2 矢量量化（VQ [Vector Quantization]）]()
	* [1.5.3 率失真择优量化（RDOQ [Rate Distortion Optimized Quantization]）]()
