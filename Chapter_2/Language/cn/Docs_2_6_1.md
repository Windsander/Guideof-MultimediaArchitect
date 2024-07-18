
# 2.6.1 色彩格式（Color Format）

**色彩格式（Color Format）** 包含了计算机对颜色的 **存储格式（Data Format）** 和 **色彩格式空间（Color Format Space）** 两部分。

同其他工业设备一样，计算机也受自身软硬件的限制，而需要特定的色彩模式。考虑到其本身是一种仅应用于计算机工业体系内（虽然现在计算机无处不在）的 **设备相关色彩空间（Device Dependent Color Space）**，业内将之称为 **色彩格式空间（Color Format Space）**，简称为 **格式空间（Format Space）**。

正如前文所提，色彩格式根据参考设备无关色彩空间的不同，被分为 RGB 色彩格式和 YUV 色彩格式。两者理论均衍生自 CIE 1976 UCS 的补充色彩空间方案，并在之后被分别设备相关化。

- RGB 色彩格式，即 **原色格式（Primaries Format）**，属于 CIE RGB 色彩空间体系；
- YUV 色彩格式，即 **传输格式（Transport Format）**，根据 CIE LUV 特性被分属为 CIE XYZ 色彩空间体系。

**RGB 与 YUV 共同组成了现代计算机色彩格式的两大分类。**

**为了更好的进行对比说明，我们用经典的彩色鹦鹉图片，来辅助说明不同色彩格式对图片携带颜色信息的影响。**

<center>
<figure>
   <img style="border-radius: 0.3125em;
      box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
      width = "350" height = "500"
      src="../../Pictures/RGB_24bits_palette_sample_image.jpeg" alt="">
   <figcaption>
      <p>图 2-28 模板彩色鹦鹉原色图片</p>
   </figcaption>
</figure>
</center>


[ref]: References_2.md