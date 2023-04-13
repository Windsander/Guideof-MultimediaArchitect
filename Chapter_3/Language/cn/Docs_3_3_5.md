
# 3.3.5 现代色彩体系（Modern Color System）

**现代色彩体系（Modern Color System）** 的基石，即为 1931 年由前身为国际光度委员会（1900, IPC [International Photometric Commission]）的国际照明委员会（CIE [International Commission on Illumination]) 提出的 **CIE RGB & CIE YUV 色彩空间** 。

<center>
<figure>
   <img style="border-radius: 0.3125em;
      box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
      width = "800" height = "1000"
      src="../../Pictures/Modern%20Color%20System.png" alt="">
   <figcaption>
      <p>图 3.3.5-1 现代色彩体系（Modern Color System）关系图谱<a href="References_3.md">[20]</a></p>
   </figcaption>
</figure>
</center>

上图很好的展示了 CIE RGB & CIE XYZ 色彩空间与经典物理学概念和其余色彩空间之间的转换关系。当前被广泛用于流媒体传输和图像颜色信息压缩的 **YUV 系列颜色格式（Color Format）** ，便是 CIE RGB 体系下的产物。

既然 CIE RGB 配合 CIE XYZ 色彩空间已经能够达成贯通存粹理论与工程应用的边界，那为什么还要引入或设计其余的色彩空间呢？

其中最典型的问题就在于上文提到的，CIE RGB & CIE XYZ 的“均色问题”。CIE RGB & CIE XYZ 并不能很好的代表人对色彩的直观感受。通俗来讲，就是人对颜色变化的感知是均匀的，而 CIE XYZ 无法将这种主观的均匀感，再不经过参考系转换的情况下，完全等价的表示出来。

所以，CIE 在 1960 年针对性的提出了 **“均匀色彩空间”（UCS [Uniform Color Space]）色彩空间** [\[21\]][ref] [\[22\]][ref]，来尝试进一步整合相关概念并更换规范化体系。UCS 自诞生后便经过了多次迭代，如 1960 UCS、1976 UCS 等。1976 UCS 对于均色度量非常关键，它还有另外一个更为知名的名称，那就是 **CIE LUV 色彩空间** 。

另一方面，因为受限于设备和技术，很多商业化产品（包括软硬件）根本无法表表示出来全部可见光谱区域。这种情况下，虽然 CIE RGB & CIE XYZ 色彩空间能够起到度量颜色的作用，却不适合用于指定设备来有条件的表示有限的颜色。这也让很多设备供应商，不得不根据自身的软硬件情况，来定制一些色彩模型供给设备使用。诸如 sRGB 就属于此类。

即便如此，在整个现代色彩体系之下，CIE RGB & CIE XYZ 色彩空间仍然是最为通用的度量衡体系。这或许是因为，它们较高的推广程度和便于计算的特性决定的。


[ref]: References_3.md