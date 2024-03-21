
# 2.5.6 CIE LUV 色彩空间（CIE 1976 L\*, u\*, v\* color space）

1976 年，在 CIE 采纳 CIE LAB 色彩空间的同年，CIE 以 **CIE 1960 UCS 和 CIE 1964 UVW**（这两个在前文色彩度量中介绍过，做为补充型色彩空间，用于量化色温和 CRI 到 CIE 标准体系内）**为基础** 进一步拓展，提出了 **CIE LUV 色彩空间**。

显然，CIE LUV 提出的目的，是为了将 CIE 1960 UCS 和 CIE 1964 UVW 两个色彩空间的 **特性统一** 到单一色彩空间。通过整合两者在度量衡相关量方面的计算，来 **化解得到目标尺度值后的色彩空间互转问题**。我们知道 CIE 1960 UCS 是由 XYZ 拓扑变换而得，CIE 1964 UVW 是由 CIE 1960 UCS 引入白点而得，两者的关键点皆在于平面色度值，而两者区别只在于 UVW 引入了白点。因此，整个问题就变为，找到一个合适的映射函数（狭义配色函数），使得在任何白点取值条件下， CIE LUV 中颜色的色度转 XYZ **皆为线性**。

基于此，LUV 对光亮度参数  进行了依托于白点的非线性变化。以此来保证，在不同白点选取下的色度，都能维持同 UCS 和 UVW 一致的线性转换方式。这一操作使 LUV 色彩空间不论白点如何选取，都能有从 LUV 到 XYZ 的色度的线性变换和逆变换。

如果记目标颜色为 $$C_{LUV}$$ ，那么 LUV 色彩空间的 **配色函数** 为：

$$
C_{LUV} =  L^{\star } \cdot Luminance + Plane(u^{\star },\ v^{\star }) = Vector[L^{\star }, u^{\star }, v^{\star }]
$$
	
记 D65 白点在 XYZ 色彩空间内颜色为 $$C_{D65}$$ ，有色温 1960 UCS 快速计算得：

$$
{\displaystyle 
 \begin{aligned}
   &C_{D65}\ (x_{D65},\ y_{D65},\ Y_{D65}) \approx (0.31271,\ 0.32902,\ 100) \\
 \end{aligned}
}
$$

如果记目标颜色为 $$C_{LUV}$$ ，从 XYZ 到 LUV 有：

$$
{\displaystyle 
 \begin{aligned}
   &(x, y) = (\ \ \ {\frac {X}{X+Y+Z}} \ \ \ \ , \ \ \ {\frac {Y}{X+Y+Z}}  \ \ \ \ ) \\ 
   &(u, v) = ({\frac  {4x}{-2x+12y+3}}, \ {\frac  {9y}{-2x+12y+3}}) \\
   &(u^{\star }, v^{\star }, L^{\star }) = F\!\left({Y}\right) \cdot (
                        13 \cdot \left(u-u_{D65}\right), \ \ \ 
                        13 \cdot \left(v-v_{D65}\right), \ \ \ 
                        1\ 
    )  \\
 \end{aligned}
}
$$

其中：

$$
{\displaystyle 
 \begin{aligned}
   L^{\star } = F(Y)&={
     \begin{cases}
       {\left( {\frac {29}{3}} \right)^3  \cdot {\frac {Y}{Y_{D65}}}}       & \ \ \  {\frac {Y}{Y_{D65}}} \le \delta ^{3} \\
       {116 \cdot {\sqrt [3]{\frac {Y}{Y_{D65}}}} \ - 16}                   & \ \ \  {\frac {Y}{Y_{D65}}} > \delta ^{3} 
     \end{cases}
   }\ \ \ , \ \ \delta ={\tfrac {6}{29}}

 \end{aligned}
}
$$

而从 LUV 到 XYZ，就相当于反向求逆，因此如下：

$$
{\displaystyle 
 \begin{aligned}
   &(u, v) = (
                        {\frac {u^{\star }}{13 \cdot L^{\star }}}  + u_{D65}\ \ , \ \ 
                        {\frac {v^{\star }}{13 \cdot L^{\star }}}  + v_{D65} \ 
                        
    )  \\
   &(x, y) = ({\frac  {9u}{6u-16v+12}}\ \ , \ {\frac  {4v}{6u-16v+12}} \ )  \\
   &(X, Y, Z) =  F^{-1}(L^{\star }) \cdot (
                        {\frac {9 u}{4 v}}, \ \ \ 
                        1, \ \ \ 
                        {\frac {12 - 3 u - 20 v}{4 v}} \ 
    ) \\
 \end{aligned}
}
$$

其中：

$$
{\displaystyle 
 \begin{aligned}
   Y = F^{-1}(L^{\star })&={
     \begin{cases}
       {Y_{D65} \cdot \left( {\frac {3}{29}} \right)^3 \cdot {L^{\star }}}       & \ \ \  L^{\star } \le 8 \\
       {Y_{D65} \cdot \left( {\frac {L^{\star }+16}{116}} \right)^3 }   & \ \ \  L^{\star } > 8 
     \end{cases}
   }

 \end{aligned}
}
$$

同 LAB，CIE LUV 的优势也在于白点确定后的快速计算。

由于 CIE LUV 并没有针对自身 LUV 色度图所在平面，即  所在平面， 做类似于 LAB 的均匀化拓扑变形。因此，LUV 在色差均匀问题上的表现，要逊于 LAB。

但是，基于 LUV 在选定白点后的线性色彩空间转换特性，LUV 在数据传输和色彩压缩方面却起到了意料之外的表现。**其设计思想最终为 YUV 色彩格式的制定打下了理论基础**。

既然将色差问题拆分为均匀化和归一化的间接处理方法不太行，那么以颜色三要素角度出发将色差均匀直接做为目标，是否就能得到完美答案呢？之前我们提到，于 LAB 和 LUV 同时期下的挑战者是美标 HSL。HSL 正是探索这一问题答案的先行者，虽然最终得到的结果 **可能不尽如人意**。


[ref]: References_2.md