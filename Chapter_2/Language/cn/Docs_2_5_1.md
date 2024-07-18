
# 2.5.1 光学三原色色彩空间（RGB Color Space） 

**光学三原色色彩空间（RGB Color Space）** 又被称为 **光三原色空间** 或 **RGB 色彩空间**。光学三原色色彩空间，是对颜色的加法混合论的有效应用。以光学三原色（RGB）的叠波权重作为三维坐标单位轴，来表示大部分可见光颜色的一种色彩模型。从亥姆霍兹的三色理论之后，光学三原色被广泛的用来表示颜色特性，但并没有形成工程化的系统。

<center>
<figure>
   <img width = "300" height = "300"
      src="../../Pictures/cs_rgbclrs1.png" alt="">
   <figcaption>
      <p>图 2-19 光学三原色色彩空间（RGB Color Space）坐标系</p>
   </figcaption>
</figure>
</center>

而由格拉斯曼颜色定律可知，人对颜色的感知其实是比较线性的。所以，光学三原色色彩空间的颜色表示非常简洁。如果记目标颜色为 $$C_{RGB}$$ ，那么 **配色函数** 为：

$$
C_{RGB} =  R \cdot Red + G \cdot Green + B \cdot Blue = Vector[R, G, B]
$$

所有可见光都可以利用此公式表示出来。

光学三原色色彩空间的基准取自 RGB 的锚定，因此 RGB 三色的代表波长选取，将会影响整个光学三原色色彩空间的颜色表示水平。

**由于足够简单且便于量化，基于光学三原色色彩空间配色函数的有局限改版模型，如 IBM RGB、Adobe RGB等，被广泛使用于计算机科学**。


[ref]: References_2.md