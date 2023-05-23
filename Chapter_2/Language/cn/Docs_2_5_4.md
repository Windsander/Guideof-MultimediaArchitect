
# 2.5.4 CIE XYZ 色彩空间（CIE 1931 XYZ Color Space）

1931年，**国际照明委员会（CIE [International Commission on Illumination]）** 提出，以经过设计的 XYZ 基准坐标系来锚定 RGB 边界的方案可以解决问题。这一映射方案所对应的颜色描述模型，被称为 **XYZ 色彩空间（XYZ Color Space）** [\[12\]][ref] [\[13\]][ref] 。

CIE 以线性等式关系构建了 XYZ 系统与 RGB 系统的转换，以三刺激函数（Tristimulus Values Functions）使可见光基于 XYZ 坐标的混合向量全部局限于正象限 [X≥0, Y≥0, Z≥0]。

如果记目标颜色为 $$C_{XYZ}$$ ，一单位 RGB 到一单位 XYZ 有：

从 $$R \rightarrow X$$  的转换因子为 $$C_{rx}$$ ，从 $$G \rightarrow Y$$ 的转换因子为 $$C_{gy}$$ ，从 $$B \rightarrow Z$$ 的转换因子为 $$C_{bz}$$ 

那么 XYZ 色彩空间的 **配色函数** 为：

$$
C_{XYZ} =  X \cdot C_{rx}R + Y \cdot C_{gy}G  + Z \cdot C_{bz}B = Vector[X, Y, Z]
$$

而从 RGB 到 XYZ 是天然可转的，记转换矩阵为 $$M_{RGB2XYZ}$$ ，那么有映射：

$$
C_{XYZ} =  M_{RGB2XYZ} \cdot C_{RGB}
$$

即：

$$
{\displaystyle 
{\begin{bmatrix} X \\ Y \\ Z \end{bmatrix}}= 
{\begin{bmatrix} 
+0.490\,00  &  +0.310\,00  &  +0.200\,00\\
+0.176\,97  &  +0.812\,40  &  +0.010\,63\\
+0.000\,00  &  +0.010\,00  &  +0.990\,00
\end{bmatrix}} \cdot {\begin{bmatrix} R \\ G \\ B \end{bmatrix}}
}
$$

而从 XYZ 到 RGB，就相当于反向求逆，因此如下：

$$
C_{XYZ} =  {M_{RGB2XYZ}}^{-1} \cdot C_{RGB} 
$$

即：

$$
{\displaystyle
{\begin{bmatrix}R\\G\\B\end{bmatrix}} \approx 
{\begin{bmatrix}
+2.364\,61385  &  -0.896\,54057  &  -0.468\,07328\\
-0.515\,16621  &  +1.426\,40810  &  +0.088\,75810\\
+0.005\,20370  &  -0.014\,40816  &  +1.009\,20446
\end{bmatrix}}{\begin{bmatrix}X\\Y\\Z\end{bmatrix}}}
$$

其中， $$M_{RGB2XYZ}$$ 为测量所得 [\[12\]][ref]（见前文）推导而出的坐标映射矩阵。

基于此映射关系，所有实际可见波长的 **视觉单色（Monochromat）和混合色** 在经过坐标转换后，都可以被描述到由 XYZ 色彩空间。这为统一视觉颜色对比标准和迭代推进色彩空间色设计，创造了有力基础工具。工程中为了表示设备颜色特性，常将设备颜色范围以 XYZ 色彩空间的色度图切面，即 **CIE 标准色度图（CIE Standard Observer Chromaticity Diagram）** 表示。因此，CIE XYZ 颜色空间的配色函数也被称为 **“CIE 标准观测者（CIE Standard Observer ）”函数** 。

但 XYZ 的也继承了 RGB 的 **“均匀色差”** (即 **平均色差** 问题) 挑战（见前文）。人眼各类视锥细胞的数目是存在差异的。纯物理描述转换为感知上的情况，在 RGB 与 XYZ 所选基准波长条件下，就会因为人对光学三原色光线的敏感程度不同，产生冷色调区域相近颜色富集，而暖色调相近颜色离散的问题。如果取用广义色差 ，即两个颜色的欧式距离，为色差 $$\Delta C$$ 的话。那么 XYZ 色彩空间中，单位 $$\Delta C$$ 的颜色变化情况就显得不那么均匀。这个就是 **平均色差** 问题。

如何处理平均色差问题？CIE 和美标给出了不同的思路。CIE 将色差问题，拆分为色度图均匀化和白点取值影响归一化两个问题，区分考虑。提出了着重于细微色差变化的 CIE LAB 色彩空间标准，和偏重标准光源线性归一化的 CIE LUV 色彩空间标准。而美标则以商业出发点，追求色彩还原更接近人眼生理感受，同时还要兼顾工业体系中对色彩信息的精细度要求，进而推进了颜色三要素色彩空间的制定。


[ref]: References_2.md