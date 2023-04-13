
# 3.4.1 色域（Color Gamut）

**色域（Color Gamut）** 是一个泛指的广义概念，代表对应色彩空间可被表达的所有颜色构成的区域。不同色彩空间的色域可能是不一样的，所以必须有一个统一的度量衡系统来进行比对。被选中作为度量衡的系统必须能客观的表示颜色的物理信息，并且不受其他主观因素影响。因此，只有设备无关色彩空间可以满足要求。当前最常用的度量衡系统，就是 CIE XYZ 色彩空间。CIE XYZ 色彩空间的色域，涵盖了人眼能够观察到的整个可见光谱范围，被 CIE 称为 **CIE 标准观察者色域（CIE Standard Observer Gamut）** 。简称 **标准色域** 。

通常，我们使用 **CIE 色度图** 来表示 **CIE 标准观察者色域**。

<center>
<figure>
   <img style="border-radius: 0.3125em;
      box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
      width = "400" height = "400"
      src="../../Pictures/CIE1931%20xy%20CP.png" alt="">
   <figcaption>
      <p>图 3.4.1-1 CIE 标准观察者色域在 CIE 色度图上的表示</p>
   </figcaption>
</figure>
</center>

由于 CIE RGB & XYZ 最基本的定义是基于 **2° 角** 的 **视网膜小窝（Fovea Centralis）间隔** 来获取的人眼视觉感受效果。因此，通常我们所称的色域以及其相关概念（如色度等），在未明确说明视网膜小窝间隔夹脚的情况下，都是假定指定基于 2° 角的测量结果（ **除 2° 角外，相对常用的还有 10° 角** ）。


[ref]: References_3.md