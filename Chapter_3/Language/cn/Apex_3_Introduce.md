
# 三、色彩的运用与存储

## **引言**
自人类对世界有认知开始，从寄思于物的艺术创作，日常生活的打扮穿着，再到科学研究对物理规律的探索，色彩始终伴随左右。什么是色彩？色彩是如何被应用到视觉工程的？

本章节主要整理说明了，部分关键光学与色彩学概念的应用和推导。通过对当代计算机图像有关颜色处理发展史的梳理，以期为工程上应用于单一图像处理、色彩权衡对比等工作，和理论上深入理解图像规格标准迭代及原理，提供必要知识图谱。

图像本身是颜色的载体，因此对图像的讨论，也就是对色彩（颜色）的讨论。

>**关键字：色彩基础、色彩空间、色彩格式、配色函数、色度、色温**

## **目录**
* [3.1 色彩基础](Docs_3_1.md)
* [3.2 颜色三要素（Three Elements of Color）](Docs_3_2.md)
	* [3.2.1 色调（Hue）](Docs_3_2_1.md)
	* [3.2.2 光亮度（Luminance）](Docs_3_2_2.md)
	* [3.2.3 饱和度（Saturation）](Docs_3_2_3.md)
* [3.3 色彩的衡量](Docs_3_3.md)
	* [3.3.1 配色函数（Color Matching Functions ）](Docs_3_3_1.md)
	* [3.3.2 色彩空间（Color Space ）](Docs_3_3_2.md)
	* [3.3.3 经典三原色函数（Trichromatic Primaries Functions）](Docs_3_3_3.md)
	* [3.3.4 经典三刺激函数（Tristimulus Values Functions）](Docs_3_3_4.md)
	* [3.3.5 现代色彩体系（Modern Color System）](Docs_3_3_5.md)
* [3.4 色彩的对比](Docs_3_4.md)
	* [3.4.1 色域（Color Gamut ）](Docs_3_4_1.md)
	* [3.4.2 色度（Chroma）& 色度平面（Chroma Plane）& 色度图（Chroma Diagram）](Docs_3_4_2.md)
	* [3.4.3 色差（Chromatic Aberration）](Docs_3_4_3.md)
	* [3.4.4 色温（Color Temperature）& 相关色温（Correlated Color Temperature）](Docs_3_4_4.md)
	* [3.4.5 标准光源（Standard Illuminants）& 白点（White Point）](Docs_3_4_5.md)
	* [3.4.6 显色指数（Color Rendering Index）](Docs_3_4_6.md)
* [3.5 经典色彩空间（Classical Color Space）](Docs_3_5.md)
	* [3.5.1 光学三原色色彩空间（RGB）](Docs_3_5_1.md)
	* [3.5.2 颜料三原色色彩空间（CMY / CMYK ）](Docs_3_5_2.md)
	* [3.5.3 CIE RGB 色彩空间（CIE 1931 RGB Color Space）](Docs_3_5_3.md)
	* [3.5.4 CIE XYZ 色彩空间（CIE 1931 XYZ Color Space）](Docs_3_5_4.md)
	* [3.5.5 CIE LAB 色彩空间（CIE 1976 L\*, a\*, b\* Color Space）](Docs_3_5_5.md)
	* [3.5.6 CIE LUV 色彩空间（CIE 1976 L\*, u\*, v\* Color Space）](Docs_3_5_6.md)
	* [3.5.7 颜色三要素色彩空间（HSV / HSI / HSL）](Docs_3_5_7.md)
* [3.6 色彩的存储](Docs_3_6.md)
	* [3.6.1 色彩格式（Color Format）与色彩存储](Docs_3_6_1.md)
	* [3.6.2 RGB 体系色彩格式](Docs_3_6_2.md)
	* [3.6.3 YUV 体系色彩格式](Docs_3_6_3.md)