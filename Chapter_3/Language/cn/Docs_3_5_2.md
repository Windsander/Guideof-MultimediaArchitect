
# 3.5.2 颜料三原色色彩空间（CMY / CMYK Color Space） 

**颜料三原色色彩空间** ，根据其是否包含对黑色（Black）的描述，被分为 **印刷三分色模型（CMY Color Space）** 即 **CMY 色彩空间** ，和 **印刷四分色模型（CMYK Color Space）** 即 **CMYK 色彩空间** 。其中，CMY 即指代颜料三原色，K 则为 Black 取尾字母，以和纯蓝色（Blue）作为区分。 颜料三原色色彩空间，是对颜色的减法混合论的直接应用。

<center>
<figure>
   <img style="border-radius: 0.3125em;
      box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
      width = "400" height = "400"
      src="../../Pictures/cs_cmyclrs1.png" alt="">
   <figcaption>
      <p>图 3.5.2-1 颜料三原色色彩空间（CMY/CMYK Color Space）坐标系</p>
   </figcaption>
</figure>
</center>

对于 CMY 色彩空间，如果记目标颜色为 $$C_{CMY}$$ ，那么配色函数为：

$$
C_{CMY} =  C \cdot Cyan + M \cdot Magenta  + Y \cdot Yellow = Vector[C, M, Y]
$$

可以发现 CMY 色彩空间与 RGB 色彩空间，恰好以立方体质心堆成。因此存在转换：

$$
C_{CMY} = 1 - C_{RGB}
$$

印刷三分色模型最早被应用于人们于绘画中。通过对颜料三原色的调色板混合，可以形成不同的颜色。由于 CMY 色彩空间在人类历史长河中，已被应用于绘画创作许久，因此这个颜色空间较难追溯最初的提出者了。不过真正对颜料三原色进行色彩空间的标准化工作，还是在打印机被发明后。

无论是喷墨打印机、照相打印机，还是激光打印机。打印出的结果都是依靠反射光被人们观察到的。这决定了此类型工程和绘画基本一致。早期打印机采用 CMY 色彩空间，并用红、青、黄三色混合，来实现黑色的显示。但是，这样混合出的黑色在显示上偏红黑。为了应对这种现象，人们在工程上引入了独立的黑色墨盒，以求解决黑色的打印问题。因此，为了描述被独立引入的黑色在颜色还原上的转换，提出了 CMYK 色彩空间。

**CMYK 色彩空间** ，对黑色进行了重设。如果记目标颜色为 $$C_{CMYK}$$ ，那么配色函数为：

$$
C_{CMYK} =  C \cdot Cyan + M \cdot Magenta  + Y \cdot Yellow + K \cdot Black = Vector[C, M, Y, K]
$$
	
由于 CMYK 比 CMY 多一维度K，从 CMY 到 CMYK 的映射就需要进行升维。

记 $$K = 1$$ 时， $$C_{CMYK} =  Vector[0,\ 0,\ 0,\ 1]$$ ，那么 $$K \neq 1$$ 时就有：

$$
{\begin{bmatrix} C \\ M \\ Y \\K \end{bmatrix}} = {\begin{bmatrix}  (C^{\prime} - K) / (1-K)  \\ (M^{\prime} -K ) / (1-K) \\ (Y^{\prime} - K) / (1-K) \\K \end{bmatrix}} \ \ | \ \ [K = min(C^{\prime}, M^{\prime}, Y^{\prime}),\ \ K \neq 1]
$$

而从 CMYK 到 CMY 的映射，就简单了：

$$
{\begin{bmatrix} C^{\prime}  \\ M^{\prime} \\ Y^{\prime} \end{bmatrix}} = {\begin{bmatrix} (1-K) \cdot C + K \\ (1-K) \cdot M + K \\ (1-K) \cdot Y + K \end{bmatrix}}
$$

而对于 CYMK 色彩空间和 RGB 色彩空间互转，就有需要以 CMY 色彩空间作为桥梁。先根据转换方向，通过 CMY 色彩空间进行 $$C_{RGB} \rightarrow C_{CMY}$$ 或者 $$ C_{CMYK} \rightarrow C_{CMY}$$ ，再通过 CMY 与 RGB 与 CMYK 的关系，进行间接转换。


[ref]: References_3.md