
# 5.1.3 视频分析库（PyOpenCV、Color-Science）

和音频一样，外部工程里，对视频的分析处理焦点多在于 **帧分析**，并非于流分析。或者说，有关音视频编解码与网络流的评估，是属于完整编解码工程内部范畴。其更多的是与网络子系统进行结合，并依托于诸如 ITU-T（或其他音视频组织，较少）提出的相关协议（如 H.264、H.265 等）约束之标准规格背景，来作为整体工程中的 **子评估系统**。所以，**音视频流分析（Audio/Video Stream Analysis）和编解码协议是强耦合的**，一般会将之归属于 **编解码器内部监测** 部分，**平行于项目的正常作业流水线**，来监控各个环节。

而 **视频帧分析（Video Frame Analysis）** 或 **帧处理（Frame Processing）** 的有效介入点，是在 **编码前（Before encoding）** 和 **解码后（After decoding）**。此时，我们用来处理的数据，已经是纯粹的 **[色彩格式（Color Format）](../../../Chapter_2/Language/cn/Docs_2_6_1.md)** 数据了。

以解码为例，在解码后的必要环节是什么样的呢？

<center>
<figure>
   <img  
      width = "600" height = "225"
      src="../../Pictures/after_decoder_workflow_simple_cn.png" alt="">
    <figcaption>
      <p>图 5-6 简易音频播放器的运行效果图</p>
   </figcaption>
</figure>
</center>

首先，是 **颜色空间转换**，亦是大量使用第二章知识的地方。一般解码后的图像因为考虑到存储空间成本，会采用 **[传输格式（Transport Format）](../../../Chapter_2/Language/cn/Docs_2_6_3.md)**，即 **[YUV 体系色彩格式](../../../Chapter_2/Language/cn/Docs_2_6_3.md)**。

不过，**只凭借 YUV 是无法做为 唯一且足够泛化的 随后步骤起点的**。这并不是指 YUV体系的色彩格式 无法直接交由如 OpenGL、DirectX、Vulkan 等驱动处理，相反这些驱动内部往往已经通过 **模式编程方法**，完成了一些 **固定格式自硬件抽象层（HAL）的映射式转换工作**（原理同第二章中，已讲解并推导过的色彩空间转换，部分算子的硬件化实现在驱动层面的组合）。**同理于 RGB，在硬件支持的情况下，直接以 YUV 上屏在流程上会更简短**。可当我们的目的是需要对每一帧的图片，做 **基于传统图形学算法上的调整**，或 **为模型进行特征分析/提取的预处理** 时，未经存储空间压缩并贴近人自然感受的 **[原色格式（Primaries Format）](../../../Chapter_2/Language/cn/Docs_2_6_2.md)**，即 **[RGB 体系色彩格式](../../../Chapter_2/Language/cn/Docs_2_6_2.md)**，还是会更便于操作。

另外，并不一定是由 YUV 转 RGB，在某些场景，我们也会要求将 RGB 转 YUV，或完成两个体系内的其他细分类型互转。所以，**具体如何转换是 由后续步骤所需的输入而定**，相当灵活。

<br>

在色彩格式转换后，则是 **帧分析与预处理步骤**。这一步完成 **对前者输出帧数据的特征提取与解析**。将会使用到相关的分析方法，例如 **[二维傅立叶](../../../Chapter_3/Language/cn/Docs_3_1_2.md)** 或其他 **[基础图像算法](../../../Chapter_3/Language/cn/Apex_3_Introduce.md)**、**[滤波核](../../../Chapter_3/Language/cn/Docs_3_2.md)** 或 **[模型接入](../../../Chapter_4/Language/cn/Apex_4_Introduce.md)**。此处也是我们本节进行操作的重点。

<br>

最后一步是 **GPU 上屏缓冲和通信**，则需要由 **选定的图形驱动（Vulkan 等）来建立相应的信道，提供指令通信和显存更新功能**。本节中，这些相关的环境和上屏更新，是由 **Python 的 Tinker 界面库走系统 UI 环境** 或 **常用视频分析库（如 OpenCV）在 库内自行维护**。暂不需要我们介入。

而当需要项目自行处理驱动和 GPU 通信环境上下文维护时，整个渲染引擎的部分，都应当在 **同一个主体环境下**（也可以用代表其通信句柄名的，实时上下文/通信上下文，来代指），辅助其他（如果需要）用于 **时间片复用** 或 **GPU 信令预封装** 的 **辅助环境**（如 延迟上下文 或 类似的自定义指令组装结构）使用。从而方便各个 **前后关联密切环节的处理结果**，在 **GPU 资源池中实现互通**。

这一涉及驱动资源协同和池化设计的部分，就属于 **图形引擎（Graphics Engine）** 的关键处理技术之一了。让我们在未来的进阶一册中再单独讲解。

常用的视频分析库主要有两个，为 **Colour-Science**、**PyOpenCV**，分别对应 \[ **颜色科学综合分析**、**图像处理与科学计算** \] 的需求。常被用于 **工程原型验证（即设计思路的验证）** 和 **外部（指工程外）帧分析**。

**尤其是 PyOpenCV，该库是重中之重。不仅是视频分析的核心库，在业务中也会经常直接使用到它的 C++ 内核。**

## **Colour-Science（Color-Science）**

**Colour-Science（Color-Science）** 是一个专注于 **色彩科学计算**、**光谱分析**、**色彩转换** 和 **色彩管理** 的 **Python 计算库**。其由 Colour Developers 开发和维护，旨在为色彩科学领域的研究和应用提供一个 **全面而强大的工具集** [\[8\]][ref] 。**注意区别库名为 Colour-Science 。**

#### 主要功能：

1. 色彩空间转换，支持 CIE 标准下的 **[RGB](../../../Chapter_2/Language/cn/Docs_2_5_3.md)**、**[XYZ](../../../Chapter_2/Language/cn/Docs_2_5_4.md)**、**[LAB](../../../Chapter_2/Language/cn/Docs_2_5_5.md)**、**[LUV](../../../Chapter_2/Language/cn/Docs_2_5_6.md)** 等各种 **[色彩空间](../../../Chapter_2/Language/cn/Docs_2_5.md)** **转换与互转**
2. 支持色彩科学如 **[黑体辐射](../../../Chapter_2/Language/cn/Docs_2_3_1.md)**、**[辐射亮度](../../../Chapter_2/Language/cn/Docs_2_3_1.md)**、**[色温](../../../Chapter_2/Language/cn/Docs_2_3_1.md)** 等的 **[物理量评估](../../../Chapter_2/Language/cn/Docs_2_3.md)**
3. 提供感官量与科学量间的换算，支持 **[配色函数](../../../Chapter_2/Language/cn/Docs_2_3_2.md)** 和 **[CIE 统一化色彩差异对比计算](../../../Chapter_2/Language/cn/Docs_2_4.md)**
4. 支持由设备制造商提供的 **LUT**、**CSV**、**XRite** 等 **不同种色彩配置文件** 校准、评估、转换
5. 能够提供完备的色彩学分析图表可视化能力

Colour-Science 是一个 **相当齐全的色彩科学库**，其方法基本涵盖了现行大部分通用（或较广范围使用）的色彩规格，并实现了相互间的联结。通过它，我们能够轻易的将不同色彩系统内的自定义变量等内部概念，**转换到统一 CIE 规格下衡量**。当然，也可以反向提供相应的配置内容。

由于库的体量过于巨大，此处仅列出部分相对高频次使用的函数，仅供参考。

#### 核心模块（colour.）的常用函数（简，仅列出名称）：

1. 色彩空间：
   [RGB_COLOURSPACES](https://colour.readthedocs.io/en/latest/generated/colour.RGB_COLOURSPACES.html), 
   [RGB_to_XYZ](https://colour.readthedocs.io/en/latest/generated/colour.RGB_to_XYZ.html), 
   [XYZ_to_RGB](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_RGB.html), 
   [XYZ_to_Lab](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_Lab.html), 
   [Lab_to_XYZ](https://colour.readthedocs.io/en/latest/generated/colour.Lab_to_XYZ.html), 
   [xyY_to_XYZ](https://colour.readthedocs.io/en/latest/generated/colour.xyY_to_XYZ.html), 
   [XYZ_to_xyY](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_xyY.html), 
   [LMS_to_XYZ](https://colour.readthedocs.io/en/latest/generated/colour.LMS_to_XYZ.html), 
   [XYZ_to_LMS](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_LMS.html), 
   [UCS_to_XYZ](https://colour.readthedocs.io/en/latest/generated/colour.UCS_to_XYZ.html), 
   [XYZ_to_UCS](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_UCS.html)
2. 色彩比对：
   [XYZ_to_xy](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_xy.html), 
   [xy_to_XYZ](https://colour.readthedocs.io/en/latest/generated/colour.xy_to_XYZ.html), 
   [XYZ_to_uv](https://colour.readthedocs.io/en/latest/generated/colour.XYZ_to_uv.html), 
   [uv_to_XYZ](https://colour.readthedocs.io/en/latest/generated/colour.uv_to_XYZ.html)
3. 色温转换：
   [xy_to_CCT](https://colour.readthedocs.io/en/latest/generated/colour.xy_to_CCT.html), 
   [CCT_to_xy](https://colour.readthedocs.io/en/latest/generated/colour.CCT_to_xy.html)
4. 色彩感知：
   [chromatic_adaptation](https://colour.readthedocs.io/en/latest/generated/colour.chromatic_adaptation.html), 
   [contrast_sensitivity_function](https://colour.readthedocs.io/en/latest/generated/colour.contrast_sensitivity_function.html), 
   [corresponding_chromaticities_prediction](https://colour.readthedocs.io/en/latest/generated/colour.corresponding_chromaticities_prediction.html)
5. 色差计算：
   [delta_E](https://colour.readthedocs.io/en/latest/generated/colour.delta_E.html) (CIE 1976, CIE 1994, CIE 2000, CMC etc.), 
   [index_stress](https://colour.readthedocs.io/en/latest/generated/colour.index_stress.html) (Kruskal’s Standardized Residual Sum of Squares)
6. 光度计算：
   [lightness](https://colour.readthedocs.io/en/latest/generated/colour.lightness.html), 
   [whiteness](https://colour.readthedocs.io/en/latest/generated/colour.whiteness.html), 
   [yellowness](https://colour.readthedocs.io/en/latest/generated/colour.yellowness.html), 
   [luminance](https://colour.readthedocs.io/en/latest/generated/colour.luminance.html), 
   [luminous_flux](https://colour.readthedocs.io/en/latest/generated/colour.luminous_flux.html), 
   [luminous_efficacy](https://colour.readthedocs.io/en/latest/generated/colour.luminous_efficacy.html),
   [luminous_efficiency](https://colour.readthedocs.io/en/latest/generated/colour.luminous_efficiency.html), 
7. 光谱处理：
   [&lt;SpectralDistribution&gt;](https://colour.readthedocs.io/en/latest/generated/colour.SpectralDistribution.html) 光谱分析的主体类, 
   [sd_to_XYZ](https://colour.readthedocs.io/en/latest/generated/colour.sd_to_XYZ.html), 
   [sd_blackbody](https://colour.readthedocs.io/en/latest/generated/colour.sd_blackbody.html), 
   [sd_ones](https://colour.readthedocs.io/en/latest/generated/colour.sd_ones.html), 
   [sd_zeros](https://colour.readthedocs.io/en/latest/generated/colour.sd_zeros.html), 
   [sd_gaussian](https://colour.readthedocs.io/en/latest/generated/colour.sd_gaussian.html), 
   [sd_CIE_standard_illuminant_A](https://colour.readthedocs.io/en/latest/generated/colour.sd_CIE_standard_illuminant_A.html)
   [sd_CIE_illuminant_D_series](https://colour.readthedocs.io/en/latest/generated/colour.sd_CIE_illuminant_D_series.html)
8. 颜色代数：
   [table_interpolation](https://colour.readthedocs.io/en/latest/generated/colour.table_interpolation.html), 
   [kernel_nearest_neighbour](https://colour.readthedocs.io/en/latest/generated/colour.kernel_nearest_neighbour.html), 
   [kernel_linear](https://colour.readthedocs.io/en/latest/generated/colour.kernel_linear.html), 
   [kernel_sinc](https://colour.readthedocs.io/en/latest/generated/colour.kernel_sinc.html), 
   [kernel_lanczos](https://colour.readthedocs.io/en/latest/generated/colour.kernel_lanczos.html), 
   [kernel_cardinal_spline](https://colour.readthedocs.io/en/latest/generated/colour.kernel_cardinal_spline.html), 
9. 数据读写：
   [read_image](https://colour.readthedocs.io/en/latest/generated/colour.read_image.html), 
   [write_image](https://colour.readthedocs.io/en/latest/generated/colour.write_image.html), 
   [read_LUT](https://colour.readthedocs.io/en/latest/generated/colour.read_LUT.html), 
   [write_LUT](https://colour.readthedocs.io/en/latest/generated/colour.write_LUT.html), 
   [read_sds_from_csv_file](https://colour.readthedocs.io/en/latest/generated/colour.read_sds_from_csv_file.html), 
   [write_sds_to_csv_file](https://colour.readthedocs.io/en/latest/generated/colour.write_sds_to_csv_file.html), 
   [read_spectral_data_from_csv_file](https://colour.readthedocs.io/en/latest/generated/colour.read_spectral_data_from_csv_file.html), 
   [read_sds_from_xrite_file](https://colour.readthedocs.io/en/latest/generated/colour.read_sds_from_xrite_file.html), 

#### 辅助模块（colour.&lt;扩展前缀&gt;.）的常用函数（简，仅列出名称）：

1. 绘图可视化（**plotting.**）：
   [plot_single_colour_swatch](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_single_colour_swatch.html), 
   [plot_multi_colour_swatches](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_multi_colour_swatches.html), 
   [plot_single_sd](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_single_sd.html), 
   [plot_multi_sds](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_multi_sds.html), 
   [plot_single_illuminant_sd](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_single_illuminant_sd.html), 
   [plot_multi_illuminant_sds](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_multi_illuminant_sds.html), 
   [plot_single_lightness_function](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_single_lightness_function.html), 
   [plot_multi_lightness_functions](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_multi_lightness_functions.html), 
   [plot_single_luminance_function](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_single_luminance_function.html), 
   [plot_multi_luminance_functions](https://colour.readthedocs.io/en/latest/generated/colour.plotting.plot_multi_luminance_functions.html)
2. 读写扩展（**io.**）：
   [image_specification_OpenImageI](https://colour.readthedocs.io/en/latest/generated/colour.io.image_specification_OpenImageIO.html)
   [LUT_to_LUT](https://colour.readthedocs.io/en/latest/generated/colour.io.LUT_to_LUT.html), 
3. 色彩模型（**models.**）：
   [RGB_COLOURSPACE_CIE_RGB](https://colour.readthedocs.io/en/latest/generated/colour.models.RGB_COLOURSPACE_CIE_RGB.html), 
   [RGB_COLOURSPACE_BT709](https://colour.readthedocs.io/en/latest/generated/colour.models.RGB_COLOURSPACE_BT709.html), 
   [RGB_COLOURSPACE_BT2020](https://colour.readthedocs.io/en/latest/generated/colour.models.RGB_COLOURSPACE_BT2020.html), 
   [RGB_COLOURSPACE_DCI_P3](https://colour.readthedocs.io/en/latest/generated/colour.models.RGB_COLOURSPACE_DCI_P3.html), 
   [RGB_COLOURSPACE_sRGB](https://colour.readthedocs.io/en/latest/generated/colour.models.RGB_COLOURSPACE_sRGB.html)
4. 色温扩展（**temperature.**）：
   [mired_to_CCT](https://colour.readthedocs.io/en/latest/generated/colour.temperature.mired_to_CCT.html), 
   [CCT_to_mired](https://colour.readthedocs.io/en/latest/generated/colour.temperature.CCT_to_mired.html), 
   [xy_to_CCT_CIE_D](https://colour.readthedocs.io/en/latest/generated/colour.temperature.xy_to_CCT_CIE_D.html), 
   [CCT_to_xy_CIE_D](https://colour.readthedocs.io/en/latest/generated/colour.temperature.CCT_to_xy_CIE_D.html)
5. 光谱恢复（**recovery.**）：
   [sd_Jakob2019](https://colour.readthedocs.io/en/latest/generated/colour.recovery.sd_Jakob2019.html), 
   [LUT3D_Jakob2019](https://colour.readthedocs.io/en/latest/generated/colour.recovery.LUT3D_Jakob2019.html), 
   [XYZ_to_sd_Jakob2019](https://colour.readthedocs.io/en/latest/generated/colour.recovery.XYZ_to_sd_Jakob2019.html), 
   [find_coefficients_Jakob2019](https://colour.readthedocs.io/en/latest/generated/colour.recovery.find_coefficients_Jakob2019.html)
6. 代数扩展（**algebra.**）：
   [euclidean_distance](https://colour.readthedocs.io/en/latest/generated/colour.algebra.euclidean_distance.html), 
   [manhattan_distance](https://colour.readthedocs.io/en/latest/generated/colour.algebra.manhattan_distance.html), 
   [eigen_decomposition](https://colour.readthedocs.io/en/latest/generated/colour.algebra.eigen_decomposition.html), 
   [vecmul](https://colour.readthedocs.io/en/latest/generated/colour.algebra.vecmul.html)

**Colour 开源项目** 位于：**[Github:colour-science/colour](https://github.com/colour-science/colour)** 。使用细节，可自行前往官方档案馆查阅：**[官方档案馆查阅](https://www.colour-science.org/)** 。

## **PyOpenCV（Python Entry of Open Source Computer Vision Library）**

**PyOpenCV（Python OpenCV）** 是 **计算机视觉和图像机器学习 OpenCV 库** 的 **官方 Python 套接接口**，项目自 Intel 奠基，现由 OpenCV 开源开发社区进行维护 [\[9\]][ref] 。其核心 OpenCV 覆盖了数百个计算机视觉算法，并 **官方预训练好了** 大量用于 **传统 CV 的 ML 功能线下模型**（详见 **[Github:OpenCV-contrib/Modules](https://github.com/opencv/opencv_contrib/tree/master/modules)** ），囊括从 **简单图像处理** 到 **复杂应用的视觉任务**，如边缘检测、图像滤波、基础变换（旋转、缩放、错切、仿射变换）、对象检测等，都可通过调用其方法功能实现。并且，考虑到机器学习拓展性，本身提供了 **对模型训练和推理的相关扩展接口**，方便处理中使用。

此外，OpenCV 有着对图片、视频文件、视频流（本地流、网络流）等数据源的完整支持，**使得基本大部分涉及视频的分析工作，都能够用该库一库解决**。非常强大。但其是一个以计算机视觉和 2D 图像处理为核心的库，具有 **有限** 的 3D 功能，**并不专注于全面的 3D 图形学处理**。

另外需要注意的是 OpenCV **并不是** 专门用于进行深度学习的框架，虽然能够进行推理，可 **并不能** 达到最好的资源利用效率和训练与推理性能。这点在应用或非分析工程中，当存在大量模型处理需求或模型流水线时，应该考虑。

#### 主要功能：

1. **图像处理**，支持图像读取、写入、滤波、变换、边缘检测等基本操作
2. **视频处理**，支持视频文件的读取、写入、帧捕获和视频流处理
3. **特征检测**，提供关键点检测和特征匹配，如 SIFT、SURF、ORB 等
4. **对象检测**，支持 Haar 级联分类器、深度学习模型（如 YOLO、SSD）等
5. **机器学习**，支持多种机器学习算法，如 SVM、KNN、决策树等
6. **三维重建**，提供立体匹配、相机标定、三维重建功能（有限）
7. **图像分割**，支持阈值分割、轮廓检测、分水岭算法等
8. **相机补益**，支持镜头畸变校正和图像增强
9. **运动分析**，提供光流计算和运动跟踪功能
10. **图像拼接**，支持全景图像拼接和图像对齐
11. **GPU 加速**，部分算法支持 GPU 加速，提升计算性能
12. **高级图像处理**，支持图像金字塔、模板匹配、霍夫变换（Hough）等高级操作
13. **丰富的库和模块**，集成了大量的图像处理和分析工具
14. **良好的库兼容性**，可以与 NumPy、SciPy 等科学计算库结合使用
15. **多模型格式支持**，支持 Caffe、TensorFlow、ONNX（关键） 等多种框架的模型格式
16. **跨平台支持**，可以在主流操作系统（Windows、macOS、Linux）上运行

**由于 OpenCV 对 API 入口进行了统一，以下模块调用前缀皆为 “cv2.”，比如 “cv2.add”，后续如无特殊说明，则按此依据。**

因为 OpenCV 的复杂度，我们参考官方的 **核心库（对应 opencv-python）** 和 **扩展库（opencv-contrib-python）** 两大分类，将主要的常用函数和封装，也拆分为 **两部分描述**。

### 首先，是核心库（opencv-python）所包含的内部模块。

#### 核心模块（cv2.core）的常用函数（简，仅列出名称）：

1. 基本数据结构：
   [&lt;Mat&gt;](https://docs.opencv.org/4.x/d3/d63/classcv_1_1Mat.html)、 
   [&lt;Point&gt;](https://docs.opencv.org/4.x/d6/d50/classcv_1_1Point__.html)、 
   [&lt;Size&gt;](https://docs.opencv.org/4.x/d2/df9/classcv_1_1Size__.html)、 
   [&lt;Rect&gt;](https://docs.opencv.org/4.x/d2/d44/classcv_1_1Rect__.html)、 
   [&lt;Scalar&gt;](https://docs.opencv.org/4.x/d1/da0/classcv_1_1Scalar__.html)
2. 基本算法和操作：
   [add](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga10ac1bfb180e2cfda1701d06c24fdbd6),
   [subtract](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#gaa0f00d98b4b5edeaeb7b8333b2de353b),
   [multiply](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga979d898a58d7f61c53003e162e7ad89f),
   [divide](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga1f96b569cac4c286642b34eff098138e),
   [absdiff](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga6fef31bc8c4071cbc114a758a2b79c14)
3. 线性代数：
   [solve](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga12b43690dbd31fed96f213eefead2373),
   [invert](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#gad278044679d4ecf20f7622cc151aaaa2),
   [determinant](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#gaf802bd9ca3e07b8b6170645ef0611d0c),
   [eigen](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga9fa0d58657f60eaa6c71f6fbb40456e3)
4. 随机数生成：
   [&lt;RNG&gt;](https://docs.opencv.org/4.x/d1/dd6/classcv_1_1RNG.html),
   [randu](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga1ba1026dca0807b27057ba6a49d258c0),
   [randn](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#gaeff1f61e972d133a04ce3a5f81cf6808)
5. 类型转换：
   [convertScaleAbs](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga3460e9c9f37b563ab9dd550c4d8c4e7d),
   [normalize](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga7bcf47a1df78cf575162e0aed44960cb)
6. 数据操作：
   [minMaxLoc](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga8873b86a29c5af51cafdcee82f8150a7),
   [meanStdDev](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga846c858f4004d59493d7c6a4354b301d),
   [reduce](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga4b78072a303f29d9031d56e5638da78e)
7. 输入输出：
   [imread](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#gacbaa02cffc4ec2422dfa2e24412a99e2),
   [imwrite](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#ga8ac397bd09e48851665edbe12aa28f25),
   [imdecode](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#gaad518fe65098fd32446bd5b9c4f8b531),
   [imencode](https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html#ga4e9883ae1f619bcbe875b7038520ea78)
8. 时间操作：
   [getTickCount](https://docs.opencv.org/4.x/db/de0/group__core__utils.html#gae73f58000611a1af25dd36d496bf4487),
   [getTickFrequency](https://docs.opencv.org/4.x/db/de0/group__core__utils.html#ga705441a9ef01f47acdc55d87fbe5090c),
   [getCPUTickCount](https://docs.opencv.org/4.x/db/de0/group__core__utils.html#gaf3070efdcfef6f1e7ac28d2b6a29a7c0)
9. 图像克隆和复制：
   [copyMakeBorder](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga2ac1049c2c3dd25c2b41bffe17658a36)
10. 数学函数：
   [exp](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga3e10108e2162c338f1b848af619f39e5),
   [log](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga937ecdce4679a77168730830a955bea7),
   [sqrt](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga186222c3919657890f88df5a1f64a7d7),
   [pow](https://docs.opencv.org/4.x/d2/de8/group__core__array.html#gaf0d056b5bd1dc92500d6f6cf6bac41ef)

#### 图像处理模块（cv2.imgproc）的基础函数（简，仅列出名称）：

1. 基本图像变换：
   [resize](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#ga47a974309e9102f5f08231edc7e7529d), 
   [warpAffine](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#ga0203d9ee5fcd28d40dbc4a1ea4451983), 
   [warpPerspective](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gaf73673a7e8e18ec6963e3774e6a94b87)
2. 颜色空间转换：
   [cvtColor](https://docs.opencv.org/4.x/db/d64/tutorial_js_colorspaces.html#autotoc_md1564), 
   [inRange](https://docs.opencv.org/4.x/db/d64/tutorial_js_colorspaces.html#autotoc_md1564)
3. 图像滤波：
   [GaussianBlur](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html), 
   [medianBlur](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html), 
   [bilateralFilter](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html), 
   [blur](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga8c45db9afe636703801b0b2e440fce37)
4. 阈值处理：
   [threshold](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html), 
   [adaptiveThreshold](https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html)
5. 直方图处理：
   [calcHist](https://docs.opencv.org/4.x/d1/db7/tutorial_py_histogram_begins.html), 
   [equalizeHist](https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html)
6. 几何变换：
   [getRotationMatrix2D](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gafbbc470ce83812914a70abfb604f4326), 
   [getAffineTransform](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#ga8f6d378f9f8eebb5cb55cd3ae295a999), 
   [getPerspectiveTransform](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gae66ba39ba2e47dd0750555c7e986ab85)
7. 图像金字塔：
   [pyrUp](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gada75b59bdaaca411ed6fee10085eb784), 
   [pyrDown](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaf9bba239dfca11654cb7f50f889fc2ff)
8. 图像插值：
   [linearPolar](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gaa38a6884ac8b6e0b9bed47939b5362f3), 
   [remap](https://docs.opencv.org/4.x/da/d54/group__imgproc__transform.html#gab75ef31ce5cdfb5c44b6da5f3b908ea4)
9. 直线与形状绘制：
   [line](https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga7078a9fae8c7e7d13d24dac2520ae4a2), 
   [rectangle](https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga07d2f74cadcf8e305e810ce8eed13bc9), 
   [circle](https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#gaf10604b069374903dbd0f0488cb43670), 
   [ellipse](https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga57be400d8eff22fb946ae90c8e7441f9), 
   [putText](https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html#ga5126f47f883d730f633d74f07456c576)

#### 图像处理模块（cv2.imgproc）的结构分析与形态学（Morphology）函数（简，仅列出名称）：

1. 边缘检测：
   [Canny](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html), 
   [Sobel](https://docs.opencv.org/4.x/d2/d2c/tutorial_sobel_derivatives.html), 
   [Laplacian](https://docs.opencv.org/4.x/d5/db5/tutorial_laplace_operator.html), 
   [Scharr](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaa13106761eedf14798f37aa2d60404c9)
2. 霍夫变换：
   [HoughLines](https://docs.opencv.org/4.x/d3/de6/tutorial_js_houghlines.html), 
   [HoughLinesP](https://docs.opencv.org/4.x/d3/de6/tutorial_js_houghlines.html), 
   [HoughCircles](https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html)
3. 轮廓检测：
   [findContours](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html), 
   [drawContours](https://docs.opencv.org/4.x/d4/d73/tutorial_py_contours_begin.html)
4. 形态学操作：
   [morphologyEx](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html), 
   [erode](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html), 
   [dilate](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html)
5. 矩形拟合：
   [boundingRect](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html), 
   [minAreaRect](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)
6. 圆形拟合：
   [minEnclosingCircle](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)
7. 椭圆拟合：
   [fitEllipse](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)
8. 多边形拟合：
   [approxPolyDP](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)
9. 凸闭包计算：
   [convexHull](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html), 
   [convexityDefects](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#gada4437098113fd8683c932e0567f47ba)
10. 形状匹配：
   [matchShapes](https://docs.opencv.org/4.x/d5/d45/tutorial_py_contours_more_functions.html)

#### 视频处理模块（cv2.videoio）的常用函数（简，仅列出名称）：

1. 视频捕获：
   [&lt;VideoCapture&gt;](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html), 
   [isOpened](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#a9d2ca36789e7fcfe7a7be3b328038585), 
   [read](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#a473055e77dd7faa4d26d686226b292c1), 
   [release](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#afb4ab689e553ba2c8f0fec41b9344ae6)
2. 视频写入：
   [&lt;VideoWriter&gt;](https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html), 
   [write](https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html#a30ebbc09c122332f62bd706b43f02a98), 
   [release](https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html#a667f737e56d5ba6b0533c6c7bf941140)
3. 视频属性：
   [get](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#a4751a18e10b6a1a7e4f7f8b5a2332b56), 
   [set](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html#a0f3f8481c4de9038b78ebd0b331d7ab4) （归属 [&lt;VideoCapture&gt;](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html) 创建的流句柄所有）
4. 视频编码：
   [&lt;VideoWriter_fourcc&gt;](https://docs.opencv.org/4.x/dd/d9e/classcv_1_1VideoWriter.html#afec93f94dc6c0b3e28f4dd153bc5a7f0)

<br>

四个关键音频库介绍完毕，那么现在，让我们用它们做些简单的实践。

---

## **简单练习：用 常用视频库 完成 带有均色分析的简易单人脸跟踪识别**

为了相对可能的便利，我们需要让这个练习用播放器有一个 UI 界面，且能根据需要的自主选择音频文件。而 **波形图（Waveform）** 就是整个音频所有频段在 **波形切面（TLS）** 叠加后的投影。

对于界面，我们需要引入 **Tkinter** 库来协助进行绘制。Tkinter 是 Python 标准模块其中之一，专用于创建图形用户界面（GUI）的工具，提供了一系列简易的按钮、图表、交互组件和标准布局。这里只需了解即可。

练习事例按照标准工程工作流进行。

#### 第一步，确立已知信息：

1. 数据来源：用户自选的 "*.wav *.flac *.mp3" 音频格式文件（如需可自行在源码中拓展）
2. 处理环境：依赖 <常用数学库>、<常用音频库>，Python 脚本执行
3. 工程目标：
    1) 提供一个具有 GUI 的简易音频格式文件播放器，自选择播放音频文件，可控播放/暂停
    2) 图形界面显示选定音频文件的波形图，并提供 Seekbar 可进行 Seek 操作

#### 第二步，准备执行环境：

检测是否已经安装了 **Python** 和 **pip（对应 Python 版本 2.x）** 或 **pip3（对应 Python 版本 3.x）** 包管理器。此步骤同我们在 **[&lt;常用数学库&gt; 的练习](Docs_5_1_1.md)** 中的操作一致，执行脚本即可：

```bash
	python install_pip.py
	python install_math_libs.py
```

完成对 **Python 环境** 的准备和 **<常用数学库>** 的安装。具体脚本实现，可回顾上一节。

同理，对于 **<常用音频库>** 的准备工作，我们也按照脚本方式进行流程化的封装。创建自动化脚本 **<a href="../../Examples/env_prepare/install_acoustic_libs.py" target="_blank">install_acoustic_libs.py</a>** 如下：

```python
import subprocess
import sys
import platform


def is_package_installed(package_name):
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package_name], check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


def install_package(package_name):
    print(f"Installing {package_name}...")
    subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
    subprocess.run([sys.executable, "-m", "pip", "show", package_name], check=True)

def is_portaudio_installed():
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(["brew", "list", "portaudio"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif platform.system() == "Linux":
            result = subprocess.run(["dpkg", "-s", "portaudio19-dev"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            return True  # Assume portaudio is handled manually on other platforms
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def install_portaudio():
    if platform.system() == "Darwin":  # macOS
        print("Installing portaudio using Homebrew...")
        subprocess.run(["brew", "install", "portaudio"], check=True)
    elif platform.system() == "Linux":
        print("Installing portaudio using APT...")
        subprocess.run(["sudo", "apt-get", "install", "-y", "portaudio19-dev"], check=True)
    else:
        print("Please install portaudio manually for your platform.")
        sys.exit(1)

def main():
    packages = ["soundfile", "pyaudio", "librosa"]

    for package in packages:
        if package == "pyaudio":
            if not is_portaudio_installed():
                install_portaudio()
            if is_package_installed(package):
                print(f"{package} is already installed.")
            else:
                install_package(package)
                print(f"{package} has been installed.")
        else:
            if is_package_installed(package):
                print(f"{package} is already installed.")
            else:
                install_package(package)
                print(f"{package} has been installed.")


if __name__ == "__main__":
    main()
```

此处有个流程上的关键，即 PyAudio 依赖于 PortAudio 库提供的 **音频输入输出设备拨接**。我们需要在安装 PyAudio 前，**先行安装 PortAudio** 以保证 PyAudio 的正常执行，否则会报如下的 **IO访问错误**：

```bash
    OSError: [Errno -9986] Internal PortAudio error
```

PyAudio 的安装过程由于 **未配置对 PortAudio 的强依赖标注**，且 **PortAudio 并未提供 pip 的可用包**。因此，不会在 pip 包管理安装过程中，自行获取前置库。需要我们 **手动在脚本中完成 检测 与 安装**。

随后，使用 Python 执行脚本：

```bash
	python install_acoustic_libs.py
```

如果包已安装，则会输出 **"[基础音频库] is already installed."**。如果包未安装，则会安装该包并输出 **"[基础音频库] has been installed."**，并显示包的详细信息。

到此，完成音频库的环境准备工作。

为什么建议 **采用执行脚本的形式**，对需要的库进行准备流水封装呢？因为这是一个非常好的习惯。而随着工作的积累，相关的 **工具库快速部署脚本会逐步的累积**，形成足够支撑大部分情况的 **一键部署工具集**。在这过程中，工程师 **可以养成对环境准备以流水线方式处理的逻辑链**，使之后再遇到新的情况时，也能快速的理清思维，便于减轻维护工作压力。

#### 第三步，搭建音频播放器：

由于只是个简易播放器，我们选择在单一文件中实现所有基本功能。

首先，需要思考一下，必要包含于 GUI 的交互组件都有哪些。有：
1. **停止（Stop）**：用于在音频开始播放后，停止播放并重置音频到起始位置；
2. **播放/暂停（Play/Pause）**：用于控制音频的播放，与过程中暂停；
3. **打开（Open）**：用于满足选择要播放的音频格式文件；
4. **进度条（Seekbar）**：用于提供 Seek 功能，并实时显示播放进度

而纯粹的用于显示展示于 GUI 的组件，只有：	
1. **波形图（Waveform）**：在 “打开” 选择音频文件后，显示该音频波形图；

至此，我们获得了此播放器的基本交互逻辑。

<center>
<figure>
   <img  
      width = "800" height = "520"
      src="../../Pictures/parctice_2_logistics.png" alt="">
    <figcaption>
      <p>图 5-4 简易音频播放器的交互逻辑关系示意图</p>
   </figcaption>
</figure>
</center>

根据上图交互关系，**将每一个节点作为函数封装**，就能轻松完成相关实现了。编写代码：

```python
import tkinter as tk
from tkinter import filedialog
import numpy as np
import soundfile as sf
import pyaudio
import threading
import queue
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Audio Player")

        # Initialize pyaudio
        self.pyaudio_instance = pyaudio.PyAudio()

        # Create control buttons frame
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop_audio)
        self.stop_button.pack(side=tk.LEFT)

        self.play_pause_button = tk.Button(self.control_frame, text="Play", command=self.toggle_play_pause)
        self.play_pause_button.pack(side=tk.LEFT)

        self.open_button = tk.Button(self.control_frame, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT)

        self.playing = False
        self.audio_data = None
        self.fs = None
        self.current_frame = 0
        self.stream = None

        # Create matplotlib figure and axes for waveform display
        self.fig, self.ax_waveform = plt.subplots(figsize=(6, 3.6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create progress bar
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(side=tk.TOP, fill=tk.X)
        self.progress_bar = tk.Scale(self.progress_frame, from_=0, to=1000, orient=tk.HORIZONTAL, showvalue=0)
        self.progress_bar.pack(fill=tk.X, expand=True)

        # Timer to update waveform line
        self.update_interval = 1  # milliseconds

        # Create thread event to stop update thread
        self.update_thread_event = threading.Event()

        # Queue for inter-thread communication
        self.queue = queue.Queue()

        # Flag variable to detect if the progress bar is being dragged
        self.is_seeking = False
        self.was_playing = False  # Mark the playback state when seeking

        # Bind events
        self.progress_bar.bind("<Button-1>", self.on_seek_start)
        self.progress_bar.bind("<ButtonRelease-1>", self.on_seek_end)
        self.progress_bar.bind("<B1-Motion>", self.on_seek)

        # Start thread to update progress bar
        self.root.after(self.update_interval, self.update_progress_bar)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac *.mp3")])
        if file_path:
            self.audio_data, self.fs = sf.read(file_path, dtype='float32')
            self.current_frame = 0
            duration = len(self.audio_data) / self.fs
            self.progress_bar.config(to=duration * 1000)  # Set the maximum value of the progress bar to the audio duration in milliseconds
            self.play_pause_button.config(text="Play")
            self.playing = False
            self.plot_waveform()

    def toggle_play_pause(self):
        if self.playing:
            self.play_pause_button.config(text="Play")
            self.playing = False
            self.pause_audio()
            self.update_thread_event.set()  # Stop update thread
        else:
            self.play_pause_button.config(text="Pause")
            self.playing = True
            self.update_thread_event.clear()  # Clear update thread event
            threading.Thread(target=self.play_audio).start()

    def audio_callback(self, in_data, frame_count, time_info, status):
        end_frame = self.current_frame + frame_count
        data = self.audio_data[self.current_frame:end_frame].tobytes()
        self.current_frame = end_frame
        self.queue.put(end_frame / self.fs * 1000)  # Current time (milliseconds)
        if self.current_frame >= len(self.audio_data):
            return (data, pyaudio.paComplete)
        return (data, pyaudio.paContinue)

    def pause_audio(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def play_audio(self):
        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paFloat32,
            channels=self.audio_data.shape[1],
            rate=self.fs,
            output=True,
            stream_callback=self.audio_callback
        )
        self.stream.start_stream()

    def stop_audio(self):
        self.playing = False
        self.current_frame = 0
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.play_pause_button.config(text="Play")
        # Reset the red line to the beginning
        self.update_thread_event.set()  # Stop update thread
        self.plot_waveform()  # Reset waveform plot
        self.progress_bar.set(0)

    def plot_waveform(self):
        self.ax_waveform.clear()
        time_axis = np.linspace(0, len(self.audio_data) / self.fs, num=len(self.audio_data))
        self.ax_waveform.plot(time_axis, self.audio_data)
        self.ax_waveform.set_title("Waveform")
        self.ax_waveform.set_xlabel("Time (s)")  # Set x-axis label to seconds
        self.ax_waveform.set_ylabel("Amplitude")
        self.canvas.draw()

    def update_progress_bar(self):
        try:
            while not self.queue.empty():
                current_time = self.queue.get_nowait()
                if not self.is_seeking:  # Only update when not dragging the progress bar
                    self.progress_bar.set(current_time)
        except queue.Empty:
            pass
        self.root.after(self.update_interval, self.update_progress_bar)

    def on_seek_start(self, event):
        self.was_playing = self.playing  # Record the playback state when seeking
        if self.playing:
            self.toggle_play_pause()  # Pause playback
        self.is_seeking = True  # Mark that the progress bar is being dragged

    def on_seek(self, event):
        # Update current_frame in real-time
        value = self.progress_bar.get()
        self.current_frame = int(float(value) / 1000 * self.fs)

    def on_seek_end(self, event):
        self.is_seeking = False  # Mark that dragging has ended
        self.plot_waveform()  # Update waveform plot
        if self.was_playing:  # If it was playing before, resume playback
            self.toggle_play_pause()

    def seek(self, value):
        if self.audio_data is not None:
            self.current_frame = int(float(value) / 1000 * self.fs)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.mainloop()
```

有运行效果如下：

<center>
<figure>
   <img  
      width = "600" height = "435"
      src="../../Pictures/parctice_2_GUI_example.png" alt="">
    <figcaption>
      <p>图 5-5 简易音频播放器的运行效果图</p>
   </figcaption>
</figure>
</center>


至此，对音频库的练习完毕。


[ref]: References_5.md