
# 2.5.5 CIE LAB 色彩空间（CIE 1976 L\*, a\*, b\* color space）

1952 年，色彩科学家 **里查德·塞瓦尔·亨特（Richard Sewall Hunter，1909–1991）** 创建了至今任然是业界最高端颜色解决方案供应商的 **亨特联合实验室（HunterLab [Hunter Associates Laboratory]）** ，并在之后提出了著名的 **Hunter L,a,b 色彩空间** 。 Hunter L,a,b 色彩空间结合 CIE XYZ 色彩空间，共同组成了 CIE 1976 LAB 色彩空间的前身。所以，CIE LAB 与 RGB 间需要通过 XYZ 来缔结转换关系。

1976 年，在经过一系列建议的采纳和对 1931 色彩标准体系的完善后，CIE 尝试用一种全新的角度来处理均色问题。CIE 在 Hunter L,a,b 色彩空间的基础上，**沿用了 Hunter L,a,b 的色度处理方式与 CIE XYZ 体系结合** ，将 CIE 标准观察者应用在了 CIE 1976 LAB 色彩空间上。由于 Hunter L,a,b 设定之初的目的，就是将不同颜色间的差异更为显著的客观表示出来，因此 CIE LAB 也继承了这一特点，成为了 **设备无关** 适合于色差比对的色彩空间。

CIE 1976 LAB 将 XYZ 色度图（非色度平面）在其所在平面，以选定白点为中心拓扑变换为圆形，分别代表：**红（Red）、绿（Green）、蓝（Blue）、黄（Yellow）** 的 4 个等大象限（扇区），并以平面中心构建了二维坐标系 $$(a,\ b)$$ 。以平面内向量 $$(a,\ b)$$ 来索引实际色度。

我们知道，单纯的靠色度是没办法完全描述颜色特征的。除了色度外，我们还需要引入光亮度因素。CIE LAB 中的依旧沿用了 1960 UCS 和 1931 XYZ 中对光亮度的处理方式，单取由白到黑的 **灰度线（Grey Line）** 作为了光亮度的刻度。但是对与不同光亮度的切分，LAB 也对 XYZ 原有的亮度表示进行了调整。以在一定程度上保证，每个亮度下切割得到的色度平面都有相对均匀表示。

如果记目标颜色为 $$C_{LAB}$$ ，那么 LAB 色彩空间的 **配色函数** 为：

$$
C_{LAB} =  L^{\star } \cdot Luminance + Plane(a^{\star },\ b^{\star }) = Vector[L^{\star }, a^{\star }, b^{\star }]
$$

记 D65 白点在 XYZ 色彩空间内颜色为 $$C_{D65}$$ ，有色温 1960 UCS 快速计算得：

$$
{\displaystyle 
 \begin{aligned}
   &C_{D65}\ (X_{D65},\ Y_{D65},\ Z_{D65}) \approx (95.049,\ 100,\ 108.884)  \\
 \end{aligned}
}
$$

如果记目标颜色为 $$C_{LAB}$$ ，一单位 XYZ 到一单位 LAB 有：

$$
{\displaystyle 
{\begin{bmatrix} L^{\star } \\ a^{\star } \\ b^{\star } \end{bmatrix}}= 
{\begin{bmatrix} 
  0  &  +116  &    0   & 16  \\
+500 &  -500  &    0   &  0  \\
  0  &  +200  &  -200  &  0  \\
\end{bmatrix}} \cdot {\begin{bmatrix} F(\tfrac{X}{X_{white}}) \\ F(\tfrac{Y}{Y_{white}}) \\ F(\tfrac{Z}{Z_{white}}) \\ 1 \end{bmatrix}}
}
$$

即，从 XYZ 到 LAB 有：

$$
{\displaystyle 
 \begin{aligned}
   L^{\star }&=116 \cdot \ F\!\left({\frac {Y}{Y_{D65}}}\right)-16 \\
   a^{\star }&=500 \cdot \left(F\!\left({\frac {X}{X_{D65}}}\right)-F\!\left({\frac {Y}{Y_{D65}}}\right)\right) \\
   b^{\star }&=200 \cdot \left(F\!\left({\frac {Y}{Y_{D65}}}\right)-F\!\left({\frac {Z}{Z_{D65}}}\right)\right) \\
 \end{aligned}
}
$$

其中：

$$
{\displaystyle 
 \begin{aligned}
   F(n)&={
     \begin{cases}
       {\sqrt [{3}]{n}}                            & \ \ \ n > \delta ^{3} \\
       {\dfrac {n}{3\delta ^{2}}}+{\frac {4}{29}}  & \ \ \ n \le \delta ^{3} 
     \end{cases}
   }\ \ \ , \ \ \delta ={\tfrac {6}{29}}

 \end{aligned}
}
$$

而从 LAB 到 XYZ，就相当于反向求逆，因此如下：

$$
{\displaystyle 
 \begin{aligned}
   X &= X_{D65} \cdot F^{-1}\left({\frac {L^{\star }+16}{116}} + {\frac {a^{\star }}{500}}\right) \\
   Y &= Y_{D65} \cdot F^{-1}\left({\frac {L^{\star }+16}{116}}                            \right) \\
   Z &= Z_{D65} \cdot F^{-1}\left({\frac {L^{\star }+16}{116}} - {\frac {b^{\star }}{200}}\right)
 \end{aligned}
}
$$

其中：

$$
{\displaystyle 
 \begin{aligned}
   F^{-1}(n)&={
     \begin{cases}
       {n^3}                            & \ \ \ n > \delta \\
       {3\delta ^2}(n-{\frac {4}{29})}  & \ \ \ n \le \delta 
     \end{cases}
   }\ \ \ , \ \ \delta ={\tfrac {6}{29}}
 \end{aligned}
}
$$

可见，XYZ 与 LAB 间的转换关系，并不是线性的。由于 CIE LAB 中的白点直接参与了转换运算，白点调参对 LAB 的影响程度会更大一些。带入色差公式 $${\displaystyle 
 \begin{aligned}
   {\displaystyle \Delta C = {\sqrt {\left(\Delta a^{\star}\right)^{2}+\left(\Delta b^{\star}\right)^{2}}}}
 \end{aligned}
}$$ 会发现，通过这种方式切割得到的整个人眼可见光色域范围，色差均匀程度依赖于白点的同时，也并非完全均匀。越靠近色度图白点，色差变化越小；越靠近色度图边缘，色差变化越大，**不过相较于 XYZ 已有很大改善** 。


[ref]: References_2.md