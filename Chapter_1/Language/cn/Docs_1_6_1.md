
# 1.6.1 音频格式（Audio Format）

**音频格式（Audio Format）**，也被称为 **音频文件格式（Audio File Format）**。其被用来指代，对当前目标 **音频数字信号（Digital Signal）** 数据，进行保存至数字存储设备中的 **处理方式和最终数据结果**。

即，音频格式 包含了两部分重要的信息：**压缩算法（Compress Formula）** 和 **存储格式（Data Format）**。**两者共同构成了 音频格式 的核心属性。**

不过，由于存储格式大都是由压缩算法决定，且采用相同于原数字信号本身的数字码表示方式进行存储。**可以说压缩算法的差异，才是决定不同音频格式间差异的关键。** 而音频的存储格式，在这一点上，仅仅作为压缩算法的运算结果，并不起主导作用。

三者关系如下所示：

<center>
<figure>
   <img  
      width = "600" height = "110"
      src="../../Pictures/Audio_Format_cn.png" alt="">
</figure>
</center>

所以，根据格式本身所采用的压缩算法类型，音频格式可以分为 **三大种类**：

- **未压缩音频格式（Uncompressed [Uncompressed Audio Format]）**，不采用任何压缩算法直接存储，例如前文提到的 PCM 音频格式；

- **无损压缩音频格式（Lossless [Lossless Compression Audio Format]）**，采用无损压缩算法，对数字信号进行压缩后的存储格式，例如 FLAC 音频格式；

- **有损压缩音频格式（Lossy [Lossy Compression Audio Format]）**，采用有损压缩算法后，得到的存储格式，例如著名的 MP3 音频格式；

显然，想要理解这几类的划分，从 **压缩算法** 入手，是个较好的切入点。


[ref]: References_1.md