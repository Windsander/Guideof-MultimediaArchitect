
# 3.6 色彩的存储

1960年，来自 **贝尔实验室（Bell Laboratories）** 的 **穆罕默德·阿塔拉（Mohamed M. Atalla，1924 - 2009）** 和 **姜大元（Dawon Kahng，1931 - 1992）** ，发现 **金属氧化物半导体（MOS [Metal Oxide Semiconductor]）** 可以借由场效应进行信息存储的现象，成功开发了 **金属氧化物半导体场效应晶体管（MOSFET [Metal Oxide Semiconductor Field Effect Transistor]）** 。随后，贝尔实验室（Bell Laboratories）联合喷气推进实验室（Jet Propulsion Laboratory）与其他研究机构，就 **“提高图像在计算机处理过程中的效果增强”** ，提出了一系列用于数字图像处理（Digital Image Processing）的方法。其中 **“关于如何利用有限的物理存储空间来保存图片像素点”** 的部分，为图片灰度单色存储的提供了可行方案 [\[44\]][ref]。

这一系列理论于 **1964年 应用在了徘徊者7号月面探测器（Space Detector Ranger 7）的计算机软硬件设计上，并以此得到了 4300 张高分辨率月面摄影** 。

月面壮举极大的鼓舞了计算机图形学的发展，同时也让图片压缩存储需求开始变得至关重要。在此背景下，1979年，首个 **单片数字信号处理器（DSP [Digital Signal Processor]）** 诞生了。数字信号处理器通过 **离散余弦变换（DCT）** 技术对图片进行了 **数模转换** 。该技术使图像像素能够以 0-1 单字节码（1-bit）的形式，存储在计算机晶体管中，形成了最初的 1-bit 灰度单色格式 [\[45\]][ref]。 **让离散化存储颜色成为了计算机图像像素存储的物理共识。**

随着 19世纪 80年代个人电脑的快速发展。灰度图格式也从 **单字节码（1-bit）** ，经过 **IBM 单色显示屏适配器（MDA [Monochrome Display Adapter]）** **2-bit 格式** ，Commodore 128 所搭载 **8563 显示控制器（VDC [Video Display Controller]）** 提供的 **4-bit 格式** ，演变到了**Apple II 与 IBM 5150** 的 **8-bit 单色格式** 。

1981 年，IBM 结合 CIE 1976 UCS 在 RGB 色彩空间上的补充，开发并发布了携带彩色数据编解码 **IBM 彩色图形适配器（CGA [Color Graphics Adapter]）** 的 **IBM 5153** 。 标志着计算机正式进入了彩色时代。自此开启了计算机 **现代色彩格式（Modern Color Format）** 的大门。


[ref]: References_3.md