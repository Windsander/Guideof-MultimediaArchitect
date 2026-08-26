# 《音视频开发技术：原理与实践》©

<p align='left'>
<a href="https://github.com/Windsander" target="_blank"><img src="https://img.shields.io/badge/%E4%BD%9C%E8%80%85-%E6%9D%8E%E8%BF%B0%E5%8D%9A-000000.svg?style=flat&logo=GitHub"></a>
<a href="https://www.zhihu.com/people/ArikanLi" target="_blank"><img src="https://img.shields.io/badge/%E5%B0%8F%E5%B2%9B%E4%B8%8A%E7%9A%84%E9%BB%91%E6%A1%83%E5%85%AD-Arikan.Li-000000.svg?style=flat&logo=zhihu"></a>
<a href="https://github.com/Windsander/Guideof-MultimediaArchitect" target="_blank"><img alt="GitBook" src="https://img.shields.io/github/stars/Windsander/Guideof-MultimediaArchitect?label=Stars&style=flat&logo=GitBook"></a>
</p>

[<font color=orange> =[>> 关于作者© <<]= </font>](AUTHOR.md)

[<font color=orange> =[>> 赞助本作© <<]= </font>](DONATE.md)

[<font color=red> =[>> 版权声明© <<]= </font>](COPYRIGHT.md)

## **目标**

对于音视频工程师/架构师来说，日常工作中总会有大量的知识技术积累，亟待梳理以期望能够被快速检索查阅。但由于工程技术所处领域的复合特征，往往针对一个工程问题所需要的专业知识，不论深浅程度，都会横跨几门学科。而想要获取有效的处理问题所能使用的信息，都需要依次回顾、搜集和关联。这样必不可少会花费大量时间查阅各类大部头资料和文献。而这么做往往是因为，对于待解答问题非常重要的知识点，分布碎片化导致的。

**音视频规格的跨度构成了本身技术的多个维度，使得我们并不能按照以往的工程思维，从单一角度来考虑涉及此类型的复合问题**。

因此，本书的目的旨在以工程解决方案的实践思路过程，对相关联的各学科核心知识进行串联。以求用一套完整且关联的技术栈模板，来贯穿当下多媒体技术的所有核心技术模块。从而 **为读者提供针对多媒体（音视频）分析/处理/整合/架构方面，有效技术指导与学习路线**。

## **特色**

本书结合作者工作实践，对架构师日常工作过程中涉及使用到的：数字信号处理、计算机图形学、色彩学、相关工程规格规范、驱动特征及软件框架设计等，领域的专业学科知识进行了梳理和提炼。从音视频工程师不同的技术阶段需要面临的问题为出发点，将

全书分为，**音视频基础与音视频分析**、**流媒体规格与简易编解码播放框架设计**、**通用统一化音视频编辑框架与渲染驱动设计**，三大阶段。每一阶段，统一采用知识图谱串联工程规格与编码实践，全面讲解对应技术阶段下需要掌握的，多媒体（音视频）技术之简史、原理、算法、设计及相关推导、制定、架构与应用。

基于此，全书按照技术逐级递进的关系，构成了整体音视频从数据分析、编解码器开发、播放器开发到图形化与图像处理、特效与特效引擎的 **完整技术栈**。使得全书每个章节内部自成一体但却相互关联，从而便于做技术字典、工程手册和整体学习之用。

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

* [一、音频的保存与还原](Chapter_1/Language/cn/Apex_1_Introduce.md)
    * [1.1 音频基础](Chapter_1/Language/cn/Docs_1_1.md)
	* [1.2 声波三要素（Three Elements of Acoustics）](Chapter_1/Language/cn/Docs_1_2.md)
	* [1.3 声音三要素（Three Elements of Sounds）](Chapter_1/Language/cn/Docs_1_3.md)
		* [1.3.1 音高（Pitch）](Chapter_1/Language/cn/Docs_1_3_1.md)
		* [1.3.2 响度（Loudness）](Chapter_1/Language/cn/Docs_1_3_2.md)
		* [1.3.3 音色（Timbre）](Chapter_1/Language/cn/Docs_1_3_3.md)
	* [1.4 声音的解构](Chapter_1/Language/cn/Docs_1_4.md)
		* [1.4.1 乐理：音调（Notes） & 五度圈（Circle of Fifths）](Chapter_1/Language/cn/Docs_1_4_1.md)
		* [1.4.2 乐理：和声（Harmony） & 和弦（Chord）& 调性网络（Tonnetz）](Chapter_1/Language/cn/Docs_1_4_2.md)
		* [1.4.3 感观：等响曲线（ELLC [Equal Loudness-Level Contour]）](Chapter_1/Language/cn/Docs_1_4_3.md)
		* [1.4.4 感观：频响曲线（FRC [Frequency Response Contour]）](Chapter_1/Language/cn/Docs_1_4_4.md)
		* [1.4.5 工程：频谱图（Spectrum）](Chapter_1/Language/cn/Docs_1_4_5.md)
	* [1.5 声音数字化](Chapter_1/Language/cn/Docs_1_5.md)
		* [1.5.1 数字信号（Digital Signal）& 模拟信号（Analog Signal）& 真实波源（Original Source）](Chapter_1/Language/cn/Docs_1_5_1.md)
		* [1.5.2 模数转换（A/D [Analog-to-Digital]）](Chapter_1/Language/cn/Docs_1_5_2.md)
		* [1.5.3 数模转换（D/A [Digital-to-Analog]）](Chapter_1/Language/cn/Docs_1_5_3.md)
		* [1.5.4 脉冲编码调制（PCM）& 脉冲密度调制（PDM）](Chapter_1/Language/cn/Docs_1_5_4.md)
	* [1.6 音频的存储](Chapter_1/Language/cn/Docs_1_6.md)
		* [1.6.1 音频格式（Audio Format）](Chapter_1/Language/cn/Docs_1_6_1.md)
		* [1.6.2 无压缩编码格式（Uncompressed Encode）](Chapter_1/Language/cn/Docs_1_6_2.md)
		* [1.6.3 无损压缩编码格式（Lossless Encode）](Chapter_1/Language/cn/Docs_1_6_3.md)
		* [1.6.4 有损压缩编码格式（Lossy Encode）](Chapter_1/Language/cn/Docs_1_6_4.md)
	* [【参考文献】](Chapter_1/Language/cn/References_1.md)

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
	    * [3.2.6 各向异性扩散（Anisotropic Diffusion）](Chapter_3/Language/cn/Docs_3_2_6.md)
    * [3.3 时间冗余控制 - 常用特征提取与朴素阈值处理](Chapter_3/Language/cn/Docs_3_3.md)
	    * [3.3.1 方向梯度直方图（HOG [Histogram of Oriented Gradient]）](Chapter_3/Language/cn/Docs_3_3_1.md)
	    * [3.3.2 朴素目标检测结果度量 - IoU & GIoU](Chapter_3/Language/cn/Docs_3_3_2.md)
	    * [3.3.3 朴素目标检测物体锁定 - 分步滑动窗口（Simple Sliding Window）](Chapter_3/Language/cn/Docs_3_3_3.md)
    * [3.4 空域冗余控制 - 基础光流算法与色度压缩](Chapter_3/Language/cn/Docs_3_4.md)
	    * [3.4.1 传统光流法（Classic Optical Flow Methods）](Chapter_3/Language/cn/Docs_3_4_1.md)
	    * [3.4.2 双向光流预测（BDOF [Bi-Directional Optical Flow]）](Chapter_3/Language/cn/Docs_3_4_2.md)
	    * [3.4.3 光流仿射修正（PROF [Affine Prediction Refinement With Optical Flow]）](Chapter_3/Language/cn/Docs_3_4_3.md)
	    * [3.4.4 色度缩放亮度映射（LMCS [Luma Mapping with Chroma Scaling]）](Chapter_3/Language/cn/Docs_3_4_4.md)
    * [3.5 频域冗余控制 - 基础变换编码](Chapter_3/Language/cn/Docs_3_5.md)
	    * [3.5.1 整数离散正余弦变换（DST/DCT）](Chapter_3/Language/cn/Docs_3_5_1.md)
	    * [3.5.2 哈达玛变换（WHT [Walsh-Hadamard Transform]）](Chapter_3/Language/cn/Docs_3_5_2.md)
	    * [3.5.3 低频不可分变换（LFNST [Low-Frequency Non-Separable Transform]）](Chapter_3/Language/cn/Docs_3_5_3.md)
    * [【参考文献】](Chapter_3/Language/cn/References_3.md)

<br>

* [四、音视频机器学习基础](Chapter_4/Language/cn/Apex_4_Introduce.md)
	* [4.1 发展概览](Chapter_4/Language/cn/Docs_4_1.md)
	* [4.2 模型工程基础](Chapter_4/Language/cn/Docs_4_2.md)
		* [4.2.1 算子（Operator）& 层（Layer）](Chapter_4/Language/cn/Docs_4_2_1.md)
		* [4.2.2 神经元（Neuron）](Chapter_4/Language/cn/Docs_4_2_2.md)
		* [4.2.3 神经网络（NN [Neural Network]）](Chapter_4/Language/cn/Docs_4_2_3.md)
		* [4.2.4 特征选择（Feature Selection）](Chapter_4/Language/cn/Docs_4_2_4.md)
	* [4.3 经典激活函数（Classic Activation Function）](Chapter_4/Language/cn/Docs_4_3.md)
		* [4.3.1 Sigmoid](Chapter_4/Language/cn/Docs_4_3_1.md)
		* [4.3.2 Tanh](Chapter_4/Language/cn/Docs_4_3_2.md)
		* [4.3.3 Softplus](Chapter_4/Language/cn/Docs_4_3_3.md)
		* [4.3.4 ReLU 族 ](Chapter_4/Language/cn/Docs_4_3_4.md)
		* [4.3.5 ELU & SELU](Chapter_4/Language/cn/Docs_4_3_5.md)
		* [4.3.6 Mish](Chapter_4/Language/cn/Docs_4_3_6.md)
		* [4.3.7 Swish 族 ](Chapter_4/Language/cn/Docs_4_3_7.md)
	* [4.4 连接函数/衰减函数（Connection/Attenuation Function）](Chapter_4/Language/cn/Docs_4_4.md)
		* [4.4.1 Dropout](Chapter_4/Language/cn/Docs_4_4_1.md)
		* [4.4.2 Maxout](Chapter_4/Language/cn/Docs_4_4_2.md)
		* [4.4.3 SoftMax](Chapter_4/Language/cn/Docs_4_4_3.md)
	* [4.5 损失函数（Loss Function）](Chapter_4/Language/cn/Docs_4_5.md)
		* [4.5.1 回归项-平均绝对误差（MAE [Mean Absolute Error]）](Chapter_4/Language/cn/Docs_4_5_1.md)
		* [4.5.2 回归项-均方误差（MSE [Mean Squared Error]）](Chapter_4/Language/cn/Docs_4_5_2.md)
		* [4.5.3 回归项-休伯损失（Huber Loss）](Chapter_4/Language/cn/Docs_4_5_3.md)
		* [4.5.4 回归项-分位数损失（Quantile Loss）](Chapter_4/Language/cn/Docs_4_5_4.md)
		* [4.5.5 分类项-对数损失（Log Loss）](Chapter_4/Language/cn/Docs_4_5_5.md)
		* [4.5.6 分类项-交叉熵损失（Cross Entropy Loss）](Chapter_4/Language/cn/Docs_4_5_6.md)
		* [4.5.7 分类项-合页损失（Hinge Loss）](Chapter_4/Language/cn/Docs_4_5_7.md)
		* [4.5.8 分类项-对比损失（Contrastive Loss）](Chapter_4/Language/cn/Docs_4_5_8.md)
		* [4.5.9 分类项-三元损失（Triplet Loss）](Chapter_4/Language/cn/Docs_4_5_9.md)
		* [4.5.10 分类项-对组排异损失（N-Pair Loss）](Chapter_4/Language/cn/Docs_4_5_10.md)
		* [4.5.11 正则项-L1 惩罚](Chapter_4/Language/cn/Docs_4_5_11.md)
		* [4.5.12 正则项-L2 惩罚](Chapter_4/Language/cn/Docs_4_5_12.md)
	* [4.6 常用最优化算法（Optimizer Operator）](Chapter_4/Language/cn/Docs_4_6.md)
		* [4.6.1 基础优化算法](Chapter_4/Language/cn/Docs_4_6_1.md)
		* [4.6.2 优化算法的优化-应对震荡](Chapter_4/Language/cn/Docs_4_6_2.md)
		* [4.6.3 优化算法的优化-应对重点强（弱）化更新](Chapter_4/Language/cn/Docs_4_6_3.md)
		* [4.6.4 自适应实时评估算法（Adam [Adaptive Moment Estimation]）](Chapter_4/Language/cn/Docs_4_6_4.md)
		* [4.6.5 优化算法对比与使用建议](Chapter_4/Language/cn/Docs_4_6_5.md)
	* [4.7 模型结构速览](Chapter_4/Language/cn/Docs_4_7.md)
		* [4.7.1 卷积神经网络（CNN [Convolutional Neural Network]）](Chapter_4/Language/cn/Docs_4_7_1.md)
		* [4.7.2 循环神经网络（RNN [Recurrent Neural Network]）](Chapter_4/Language/cn/Docs_4_7_2.md)
		* [4.7.3 自注意力网络（Transformer）](Chapter_4/Language/cn/Docs_4_7_3.md)
    * [【参考文献】](Chapter_4/Language/cn/References_4.md)

<br>


* [五、音视频帧分析与数据处理](Chapter_5/Language/cn/Apex_5_Introduce.md)
	* [5.1 音视频帧与环境准备](Chapter_5/Language/cn/Docs_5_1.md)
		* [5.1.1 常用数学库（Numpy、Pandas、Matplotlib）](Chapter_5/Language/cn/Docs_5_1_1.md)
		* [5.1.2 音频分析库（SoundFile、PyAudio、Librosa、Aubio）](Chapter_5/Language/cn/Docs_5_1_2.md)
		* [5.1.3 视频分析库（PyOpenCV、Color-Science）](Chapter_5/Language/cn/Docs_5_1_3.md)
		* [5.1.4 其他分析软件](Chapter_5/Language/cn/Docs_5_1_4.md)
	* [5.2 音频帧分析实践（Audio Frame Analysis）](Chapter_5/Language/cn/Docs_5_2.md)
		* [5.2.1 音频帧的切分与加窗（Frame Blocking & Windowing）](Chapter_5/Language/cn/Docs_5_2_1.md)
		* [5.2.2 时域与频域特征（Time/Frequency Domain Features）](Chapter_5/Language/cn/Docs_5_2_2.md)
		* [5.2.3 实战：A4 标准音的特征分析工程](Chapter_5/Language/cn/Docs_5_2_3.md)
	* [5.3 视频帧分析实践（Video Frame Analysis）](Chapter_5/Language/cn/Docs_5_3.md)
		* [5.3.1 视频帧的提取与表示（Frame Extraction & Representation）](Chapter_5/Language/cn/Docs_5_3_1.md)
		* [5.3.2 帧间分析：帧差、光流与场景切分（Frame Difference, Optical Flow & Scene-Cut Detection）](Chapter_5/Language/cn/Docs_5_3_2.md)
		* [5.3.3 实战：测试视频的场景切分与目标跟踪工程](Chapter_5/Language/cn/Docs_5_3_3.md)
	* [5.4 音视频帧处理实践（Audio & Video Frame Processing）](Chapter_5/Language/cn/Docs_5_4.md)
		* [5.4.1 音频帧处理：滤波、变速与变调（Filtering, Time-Stretch & Pitch-Shift）](Chapter_5/Language/cn/Docs_5_4_1.md)
		* [5.4.2 视频帧处理：色彩、滤波与几何变换（Color, Filtering & Geometric Transform）](Chapter_5/Language/cn/Docs_5_4_2.md)
		* [5.4.3 实战：音视频帧批量处理工程](Chapter_5/Language/cn/Docs_5_4_3.md)
	* [5.5 本章小结与进阶指引（Summary & Roadmap）](Chapter_5/Language/cn/Docs_5_5.md)
	* [【参考文献】](Chapter_5/Language/cn/References_5.md)


<br>
<br>

### 流媒体规格与简易编解码播放框架设计

* [六、音视频编码规格（Audio & Video Codec Specification）](Chapter_6/Language/cn/Apex_6_Introduce.md)
	* [6.1 编码简史与编码四环（Codec History & The Four-Stage Framework）](Chapter_6/Language/cn/Docs_6_1.md)
		* [6.1.1 视频编码编年简史（A Chronology of Video Coding Standards）](Chapter_6/Language/cn/Docs_6_1_1.md)
		* [6.1.2 压缩何以可能：四类冗余（Four Types of Redundancy）](Chapter_6/Language/cn/Docs_6_1_2.md)
		* [6.1.3 编码四环：混合编码框架（The Hybrid Coding Framework）](Chapter_6/Language/cn/Docs_6_1_3.md)
	* [6.2 H.264/AVC：经典之巅（H.264/AVC in Detail）](Chapter_6/Language/cn/Docs_6_2.md)
		* [6.2.1 诞生背景：JVT 与混合框架的成熟](Chapter_6/Language/cn/Docs_6_2_1.md)
		* [6.2.2 帧内预测（Intra Prediction）](Chapter_6/Language/cn/Docs_6_2_2.md)
		* [6.2.3 帧间预测与运动补偿（Inter Prediction & Motion Compensation）](Chapter_6/Language/cn/Docs_6_2_3.md)
		* [6.2.4 变换、量化与熵编码（Transform, Quantization & Entropy Coding）](Chapter_6/Language/cn/Docs_6_2_4.md)
		* [6.2.5 Profile/Level 体系与规格导读](Chapter_6/Language/cn/Docs_6_2_5.md)
	* [6.3 H.265/HEVC：4K 时代的答案（H.265/HEVC in Detail）](Chapter_6/Language/cn/Docs_6_3.md)
		* [6.3.1 编码树单元：CTU 与四叉树划分（Coding Tree Unit & Quadtree）](Chapter_6/Language/cn/Docs_6_3_1.md)
		* [6.3.2 预测技术的演进（Evolution of Prediction）](Chapter_6/Language/cn/Docs_6_3_2.md)
		* [6.3.3 环路滤波与并行化设计（In-loop Filtering & Parallelism）](Chapter_6/Language/cn/Docs_6_3_3.md)
	* [6.4 H.266/VVC 与 AV1：两条路线的竞赛（H.266/VVC & AV1）](Chapter_6/Language/cn/Docs_6_4.md)
		* [6.4.1 VVC：向压缩极限推进（Versatile Video Coding）](Chapter_6/Language/cn/Docs_6_4_1.md)
		* [6.4.2 AV1：开源免版税阵营（AOMedia Video 1）](Chapter_6/Language/cn/Docs_6_4_2.md)
		* [6.4.3 专利池生态与三代规格对照（Patent Ecosystem & Comparison）](Chapter_6/Language/cn/Docs_6_4_3.md)
	* [6.5 音频编码规格（Audio Codec Specification）](Chapter_6/Language/cn/Docs_6_5.md)
		* [6.5.1 心理声学：音频压缩的地基（Psychoacoustics）](Chapter_6/Language/cn/Docs_6_5_1.md)
		* [6.5.2 MP3：开启数字音乐时代（MPEG-1 Layer III）](Chapter_6/Language/cn/Docs_6_5_2.md)
		* [6.5.3 AAC：青出于蓝（Advanced Audio Coding）](Chapter_6/Language/cn/Docs_6_5_3.md)
		* [6.5.4 Opus：为实时互动而生（Opus, RFC 6716）](Chapter_6/Language/cn/Docs_6_5_4.md)
	* [6.6 实战：编码器规格对比实验（practice_7）](Chapter_6/Language/cn/Docs_6_6.md)
	* [6.7 本章小结与进阶指引（Summary & Roadmap）](Chapter_6/Language/cn/Docs_6_7.md)
	* [【参考文献】](Chapter_6/Language/cn/References_6.md)

<br>

* [七、封装格式与流传输协议（Container Formats & Streaming Protocols）](Chapter_7/Language/cn/Apex_7_Introduce.md)
	* [7.1 从封装说起：容器的使命（The Mission of Containers）](Chapter_7/Language/cn/Docs_7_1.md)
		* [7.1.1 裸码流缺什么（What Elementary Streams Lack）](Chapter_7/Language/cn/Docs_7_1_1.md)
		* [7.1.2 MP4：为随机访问而生的索引树（MP4 & The Index Tree）](Chapter_7/Language/cn/Docs_7_1_2.md)
		* [7.1.3 FLV：为流式传输而生的标签序列（FLV & The Tag Stream）](Chapter_7/Language/cn/Docs_7_1_3.md)
		* [7.1.4 MPEG-TS：为容错传输而生的定长包（MPEG-TS & The Fixed-Length Packets）](Chapter_7/Language/cn/Docs_7_1_4.md)
		* [7.1.5 三容器设计取向对比（Three Containers, Three Philosophies）](Chapter_7/Language/cn/Docs_7_1_5.md)
	* [7.2 实时传输奠基：RTP/RTCP（The Foundation of Real-Time Transport）](Chapter_7/Language/cn/Docs_7_2.md)
		* [7.2.1 实时传输的诞生与 UDP 的取舍（Real-Time Transport & The UDP Trade-off）](Chapter_7/Language/cn/Docs_7_2_1.md)
		* [7.2.2 RTP 固定头：十二字节的自描述（The 12-Byte Self-Describing Header）](Chapter_7/Language/cn/Docs_7_2_2.md)
		* [7.2.3 RTCP：质量反馈环与唇同步（RTCP: Feedback Loop & Lip Sync）](Chapter_7/Language/cn/Docs_7_2_3.md)
		* [7.2.4 从 RTP 到 WebRTC（From RTP to WebRTC）](Chapter_7/Language/cn/Docs_7_2_4.md)
	* [7.3 直播时代的霸主：RTMP（RTMP & The Live Streaming Dynasty）](Chapter_7/Language/cn/Docs_7_3.md)
		* [7.3.1 Flash 时代的直播王朝（The Flash-Era Live Dynasty）](Chapter_7/Language/cn/Docs_7_3_1.md)
		* [7.3.2 握手：C0/C1/C2 与 S0/S1/S2（The RTMP Handshake）](Chapter_7/Language/cn/Docs_7_3_2.md)
		* [7.3.3 Chunk 封包：一次消息，多次封装（Chunking & Header Compression）](Chapter_7/Language/cn/Docs_7_3_3.md)
		* [7.3.4 Message 类型族与 AMF 编码（Message Types & AMF Encoding）](Chapter_7/Language/cn/Docs_7_3_4.md)
		* [7.3.5 命令消息与流管理时序（Commands & Stream Management）](Chapter_7/Language/cn/Docs_7_3_5.md)
	* [7.4 直播的 HTTP 化：HLS 与 fMP4（HLS & Fragmented MP4）](Chapter_7/Language/cn/Docs_7_4.md)
		* [7.4.1 把直播搬进 HTTP（Moving Live Streaming into HTTP）](Chapter_7/Language/cn/Docs_7_4_1.md)
		* [7.4.2 两级播放列表：Master 与 Media（Master & Media Playlists）](Chapter_7/Language/cn/Docs_7_4_2.md)
		* [7.4.3 分片机制与直播滑动窗（Segments & The Sliding Window）](Chapter_7/Language/cn/Docs_7_4_3.md)
		* [7.4.4 自适应码率：客户端的切换艺术（Adaptive Bitrate Switching）](Chapter_7/Language/cn/Docs_7_4_4.md)
		* [7.4.5 延迟之战与 LL-HLS（The Latency Battle & LL-HLS）](Chapter_7/Language/cn/Docs_7_4_5.md)
	* [7.5 现代协议群像：DASH、WebRTC 与 SRT（The Modern Protocol Landscape）](Chapter_7/Language/cn/Docs_7_5.md)
		* [7.5.1 DASH：标准化的另一极（MPEG-DASH & The Standards Track）](Chapter_7/Language/cn/Docs_7_5_1.md)
		* [7.5.2 WebRTC：RTP 的正统继承者（WebRTC & The Real-Time Heir）](Chapter_7/Language/cn/Docs_7_5_2.md)
		* [7.5.3 SRT：弱网回传的 ARQ 路线（SRT & The ARQ Prescription）](Chapter_7/Language/cn/Docs_7_5_3.md)
		* [7.5.4 编年史与全景对照（A Chronicle & The Big Picture）](Chapter_7/Language/cn/Docs_7_5_4.md)
	* [7.6 实战：推流抓包与低延迟拉流（practice_8）](Chapter_7/Language/cn/Docs_7_6.md)
	* [7.7 本章小结与进阶指引（Summary & Roadmap）](Chapter_7/Language/cn/Docs_7_7.md)
	* [【参考文献】](Chapter_7/Language/cn/References_7.md)

<br>

* [八、解码与播放（Decoding & Playback）](Chapter_8/Language/cn/Apex_8_Introduce.md)
	* [8.1 解码器框架设计（Decoder Framework Design）](Chapter_8/Language/cn/Docs_8_1.md)
		* [8.1.1 从规格到代码：解码器的本质（From Spec to Code）](Chapter_8/Language/cn/Docs_8_1_1.md)
		* [8.1.2 FFmpeg 六库：分层的艺术（The Six Libraries of FFmpeg）](Chapter_8/Language/cn/Docs_8_1_2.md)
		* [8.1.3 收发分离：解码 API 的状态机（The Send/Receive State Machine）](Chapter_8/Language/cn/Docs_8_1_3.md)
		* [8.1.4 管线与 seek：工程落地的暗坑（Pipelines, Seek & The Pitfalls）](Chapter_8/Language/cn/Docs_8_1_4.md)
	* [8.2 播放器核心系统（Player Core Systems）](Chapter_8/Language/cn/Docs_8_2.md)
		* [8.2.1 播放器的三个问题：何时解，何时显，对谁齐（Three Questions of A Player）](Chapter_8/Language/cn/Docs_8_2_1.md)
		* [8.2.2 音画同步：主时钟的三种策略（A/V Sync & The Three Master Clocks）](Chapter_8/Language/cn/Docs_8_2_2.md)
		* [8.2.3 抖动缓冲：与网络和解的艺术（Jitter Buffer & The Art of Compromise）](Chapter_8/Language/cn/Docs_8_2_3.md)
		* [8.2.4 渲染管线：从 YUV 到视网膜（The Render Pipeline）](Chapter_8/Language/cn/Docs_8_2_4.md)
	* [8.3 实战：音画同步策略对比实验（practice_9）](Chapter_8/Language/cn/Docs_8_3.md)
	* [8.4 本章小结与进阶指引（Summary & Roadmap）](Chapter_8/Language/cn/Docs_8_4.md)
	* [【参考文献】](Chapter_8/Language/cn/References_8.md)

<br>

* [九、流媒体链路与流分析（Streaming Pipeline & Stream Analysis）](Chapter_9/Language/cn/Apex_9_Introduce.md)
	* [9.1 现代流媒体链路全景（The Streaming Pipeline）](Chapter_9/Language/cn/Docs_9_1.md)
		* [9.1.1 一场直播的完整旅程（The Journey of A Live Stream）](Chapter_9/Language/cn/Docs_9_1_1.md)
		* [9.1.2 端到端延迟：从采集到视网膜（Glass-to-Glass Latency）](Chapter_9/Language/cn/Docs_9_1_2.md)
		* [9.1.3 链路各环节的角色与故障域（Roles & Failure Domains）](Chapter_9/Language/cn/Docs_9_1_3.md)
		* [9.1.4 协议在链路两端的分工（Protocols at Both Ends）](Chapter_9/Language/cn/Docs_9_1_4.md)
	* [9.2 流分析与质量监控（Stream Analysis & QoE）](Chapter_9/Language/cn/Docs_9_2.md)
		* [9.2.1 QoE 指标体系：给体验号脉（The QoE Metrics）](Chapter_9/Language/cn/Docs_9_2_1.md)
		* [9.2.2 播放端埋点与上报（Player Instrumentation）](Chapter_9/Language/cn/Docs_9_2_2.md)
		* [9.2.3 服务端链路监控（Server-Side Monitoring）](Chapter_9/Language/cn/Docs_9_2_3.md)
		* [9.2.4 从帧级到会话级：数据分析方法（From Frames to Sessions）](Chapter_9/Language/cn/Docs_9_2_4.md)
	* [9.3 实战：链路搭建与质量分析（practice_10）](Chapter_9/Language/cn/Docs_9_3.md)
	* [9.4 阶段小结与进阶指引（Summary & Roadmap）](Chapter_9/Language/cn/Docs_9_4.md)
	* [【参考文献】](Chapter_9/Language/cn/References_9.md)


<br>
<br>

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。<br />
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.