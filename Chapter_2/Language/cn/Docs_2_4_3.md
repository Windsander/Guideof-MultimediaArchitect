
# 2.4.3 色差（Chromatic Aberration）

**色差（Chromatic Aberration）** 是一个相对概念，指的是两个色度不同的颜色之间的差异。 

- **广义色差（gCA [General Chromatic Aberration]）** 不限定用于对比的两个颜色对应的色调，此时的色差计算的是颜色色度的差异。
- **狭义色差（sCA [Special Chromatic Aberration]）** 则要求对比的两个颜色具有相同的色调，此时的色差计算的仅仅是颜色饱和度的变化。因此，**狭义色差可以被认为是广义色差的一种特殊情况**。

色差的计算为了简洁，通常都选择使用欧式距离表示。记对比的两颜色分别为 $$C_1$$ 、 $$C_2$$ ，色差为 $$C$$ ，广义色差为 $$\Delta C$$ ，有：

$$
{\displaystyle 
 \begin{aligned}
   &C={
        \begin{cases}
          &{\displaystyle gCA: \{\Delta C ={\sqrt {\Delta H ^{2} + \Delta S ^{2} }}  \approx {distance} (C_1,\ C_2)} \} \\
          &{\displaystyle sCA: \{ {\Delta C}|_{({\Delta H = 0})} = {\sqrt {\Delta S ^{2}}} = \Delta S \approx {range} (C_1,\ C_2) \} }
        \end{cases}} \\
 \end{aligned}
}
$$

带入 CIE XYZ 规则，色差的表示就可以直接以色度 $$(x, y)$$ 计算了：

$$
{\displaystyle 
 \begin{aligned}
   &C = {\sqrt {\Delta x ^{2} + \Delta y ^{2} }} \\ 
 \end{aligned}
}
$$

替换了色调饱和度参数，使广义狭义在公式层面得到了统一。


[ref]: References_2.md