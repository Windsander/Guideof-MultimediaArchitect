
# 3.2 频率信息提取 - 常用滤波算法

上一节中，我们就数字信号处理（DSP）的核心算法，傅里叶变换，进行了详细的说明。而在对二维傅里叶变换进行讲解的时候。细心的读者可能已经发现了 **图像在空频分布上的一些特点。在分布的频率（波矢 $${\vec{k}}$$ 的频率 $$\vert {\vec{k}} \vert = \omega$$ ）的占比（强度系数 $$\hat{f}_{\omega}(u,v)$$ ）中，低频信号的占比高，而高频信号的占比低。** 这一现象产生的原因在于：

当一张图片处于色彩变化大且明显的区域时， $${\vec{k}}$$ 平面波在 $$uv$$ 平面上的相邻点，单次数值变化的跨度就越大，直观体现就是波矢 $${\vec{k}}$$ 更长，即频率 $$\omega$$ 更高，波长 $$\lambda$$ 更短。相反，当图片处于色彩变化相对平稳的区域时，相邻两个像素点的色彩差异就越小，单次数值变化的跨度就越小，对应的波矢 $${\vec{k}}$$ 更短，即频率 $$\omega$$ 更低，波长 $$\lambda$$ 更长。这种变化明显处，往往是图片中的噪点或物体的轮廓位置。**显然，色彩差异较小的相邻像素区域，才是占有图片空间较多的部分。**

**传统的图像处理，即是对图像频率的处理。其本质上是根据不同的目标，提炼出图像中被认为有用的信息，这一步被称为滤波（Filter）。滤波是对信号已有频率的过滤，通过增强（阻塞/增强阻塞）一部分频段，来达到筛选的效果。**

因此，由于信息量的关系，滤波算法更多的使用场景是被运用在已得图像的结果上。相较于一维信号，二维信号明显对算法敏捷程度有更低的容忍度。而直接以傅里叶空频分离（SFS）进行科学处理，依旧会有些臃肿。毕竟非分析场景一般不需要特别高的精度，通常只在意一定范围内的频率特征，且并不会对细部有过多的要求。那么有没有满足条件下，针对目标频段的，更实用的变体呢？

考虑到简易的滤波手段多为均值与阈限共同作用。从算法层面，优化均值与阈限的求与取，就是切入点。如果可以将算法抽象为足够小的有限参数单元，我们就能够以 **卷积核（Convolution Nucleus / Convolution Kernel / Sliding Window / Filter）** 数学工具，封装整个运算过程。从而充分的利用现代 GPU 设备进行并行计算，批量处理并降低耗时。

**欲期望达成此要求，被抽象的有限参数单元必然不能太复杂。**

为了便于演示说明，本节采用 **OpenGL 的 GLSL 程序片脚本语言**，并使用 **WebGL 环境预览**，来进行算法的演示工作。其他驱动，如 DirectX 的 HLSL 或 Metal 的 MLSL，皆可参照 GLSL 逻辑达到相同效果。

* [在线演示](Playground_3.md)

[ref]: References_3.md