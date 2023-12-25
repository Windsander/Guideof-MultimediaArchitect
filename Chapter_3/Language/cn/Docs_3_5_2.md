
# 3.5.2 哈达玛变换（WHT [Walsh-Hadamard Transform]）

除了整数离散正余弦变换（IDST/IDCT）外，在早期的规格中（如 H.264）还会使用一种，被称为 **沃尔什-哈达玛变换（WHT [Walsh-Hadamard Transform]）** 的离散傅立叶的变换变体算法，来代为进一步的富集频域信息。

在之前的傅立叶变换运用中，我们大都选择三角函数或近似拟合，来作为基底函数进行分解。考虑到傅立叶函数，只从周期性上，对基底函数族和目标函数进行了约束。我们是不是可以选择一种，类似于自然排序线性组合的周期性函数，代替正余弦处理，从而获取更符合数据物理介质存储（媒介传输）状态（0/1 双模态）的变换过程呢？

答案是可以的。虽然，从某种意义上，哈达玛变换相当于取用了只拟合正余弦函数极值的特殊函数。但哈达玛变换（WHT）依旧被认为是此类 **非三角函数离散傅立叶变换** ，简称 **非三角函数变换（或非正/余弦变换）** ，的经典代表之一。

考虑周期 $$T=2^n$$ 分段函数：

$$
{\displaystyle 
 \begin{aligned}
  f(x)= & (-1)^{ \lfloor \tfrac{x}{T}  \rfloor } = (-1)^{ \lfloor \tfrac{x}{2^n}  \rfloor } \\
 \end{aligned}
}
$$

记周期 $$T=2^n =N$$ 的原信号函数 $$s(t)$$ 以 $$f(x)$$ 函数族构成基底。根据 **傅立叶级数** 有：

$$
{\displaystyle 
 \begin{aligned}
   s(n)  &= \frac{1}{N}\sum_{k = 0}^{N-1} \hat{s}(k) \cdot (-1)^{nk}  \\
   \hat{s}(k)  &= \sum_{n = 0}^{N-1} s(n) \cdot (-1)^{nk} \\
 \end{aligned}
}
$$

这即是 **哈达玛变换的基础公式** 。

不同于 DST/DCT 需要进行泛化后，才能运用到工程之中的情况。哈达玛变换由于 $$f(x)$$ 本身为偶函数，且始终只有实部的特性，可以直接在原有无扩充的数据集上使用。因此，假设原信号函数 $$s(t) = s(n)$$ 在 $$n \in \mathbb{Z} [0, \ N - 1]$$ 的各节点位置，有样本采样 $$S \in [S_0, \ S_{N - 1}]$$ 。则：

$$
{\displaystyle 
 \begin{aligned}
  WHT:&
   {
        \begin{cases}
          s(n)  &= \frac{1}{N}\sum_{k = 0}^{N-1} \hat{s}(k)  \cdot (-1)^{nk}  
                 = \sqrt{\frac{1}{N}} \cdot \sum_{k = 0}^{N-1} \begin{pmatrix} \sqrt{\frac{1}{N}} \cdot \hat{s}(k) \end{pmatrix} \cdot (-1)^{nk}    \\
          \hat{s}(k)  &= \sum_{n = 0}^{N-1} s(n+\tfrac{1}{2}) \cdot (-1)^{nk}
                 = \sum_{n = 0}^{N-1} s(n)  \cdot (-1)^{nk}  
        \end{cases}
   } \\
 \end{aligned}
}
$$

即：

$$
{\displaystyle 
 \begin{aligned}
  &k \in [0,\ N-1] \quad \quad n \in [0,\ N - 1] \\
  WHT:&
   {
        \begin{cases}
          S_n  &= \frac{1}{\sqrt{N}} \sum_{k = 0}^{N-1} X_k \cdot (-1)^{nk}  \\
          X_k  &= \frac{1}{\sqrt{N}}  \cdot \sum_{n = 0}^{N-1} S_n \cdot (-1)^{nk}
        \end{cases}
   } \\
 \end{aligned}
}
$$

扩展到 **二维** 情况，有：

$$
{\displaystyle 
 \begin{aligned}
  &k(u,v) \& p(x,y)  \in [(0,\ 0),\ (N-1,\ N-1)] \\
  WHT: & X_k(u,v)  = \begin{pmatrix} \frac{1}{\sqrt{N}} \end{pmatrix} ^2 \cdot \sum_{p = (0,0)}^{(N-1,N-1)}S_p(x,y) \cdot (-1)^{xu} \cdot (-1)^{yv} \\ 
 \end{aligned}
}
$$

如此，就可以矩阵表示 WHT 变化为：

$$
{\displaystyle 
 \begin{aligned}
  X_k &= K_{WHT} \cdot S_p \cdot {K_{WHT}}^{T} \\ 
 \end{aligned}
}
$$

其中：

$$
{\displaystyle 
 \begin{aligned}
  K_{WHT} &= \begin{bmatrix}
     \frac{1}{\sqrt{N}} \cdot \sum_{y = 0}^{N-1} \begin{pmatrix} \frac{1}{\sqrt{N}} \cdot \sum_{x = 0}^{N-1} (-1)^{xu} \end{pmatrix} \cdot (-1)^{yv} 
  \end{bmatrix} \\
          &= \frac{1}{\sqrt{N}} \cdot \begin{bmatrix} 
    & (-1)^{i \cdot j} 
  \end{bmatrix} _{N \times N} \\
          &= {K_{WHT}}^{T} = {K_{WHT}}^{-1} \\ 
 \end{aligned}
}
$$

所以，我们通常记 $$N$$ 阶哈达玛矩阵为 $$H_N = \begin{bmatrix}  (-1)^{i \cdot j} \end{bmatrix} _{N \times N} = \sqrt{N} \cdot K_{WHT}$$ ，原式即可简化为：

$$
 {\displaystyle 
 \begin{aligned}
  X_k &= \frac{1}{N} \cdot H \cdot S_p \cdot H \\ 
 \end{aligned}
}
$$

显然，对于 $$H_{2N}$$ 与 $$H_N$$ 有关系：

$$
{\displaystyle 
 \begin{aligned}
  H_{2N} &=  
  \begin{bmatrix} 
    & H_N \ ,   & H_N \\
    & H_N \ ,  -& H_N 
  \end{bmatrix}\\ 
 \end{aligned}
}
$$

常用的哈达玛变换算子主要有 3 种，分别是：

$$
{\displaystyle 
 \begin{aligned}
  H_2 &=  
  \begin{bmatrix} 
    & 1 \ ,   & 1 \\
    & 1 \ ,  -& 1 
  \end{bmatrix} \\ 
 H_4 &=  
  \begin{bmatrix} 
    & H_2 \ ,   & H_2 \\
    & H_2 \ ,  -& H_2 
  \end{bmatrix}=  
  \begin{bmatrix} 
    & 1 ,   & \quad 1 \ ,   & \quad 1 \ ,   & \quad 1   \\
    & 1 ,   & \    -1 \ ,   & \quad 1 \ ,   & \    -1   \\
    & 1 ,   & \quad 1 \ ,   & \    -1 \ ,   & \    -1   \\
    & 1 ,   & \    -1 \ ,   & \    -1 \ ,   & \quad 1   
  \end{bmatrix}\\
 H_8 &=  
  \begin{bmatrix} 
    & H_4 \ ,   & H_4 \\
    & H_4 \ ,  -& H_4 
  \end{bmatrix} =  
  \begin{bmatrix} 
    & H_2 ,   & \quad H_2 \ ,   & \quad H_2 \ ,   & \quad H_2   \\
    & H_2 ,   & \    -H_2 \ ,   & \quad H_2 \ ,   & \    -H_2   \\
    & H_2 ,   & \quad H_2 \ ,   & \    -H_2 \ ,   & \    -H_2   \\
    & H_2 ,   & \    -H_2 \ ,   & \    -H_2 \ ,   & \quad H_2   
  \end{bmatrix}\\
 \end{aligned}
}
$$
	
从上面的推导过程可知，采用哈达玛变换，同样能够将频域中的高低频信息，进行分区汇集。理论上 WHT 也可以代替 IDST/IDCT 来做频域压缩（降低信息熵）前的归类处理。

## **哈达玛变换的常见应用**

考虑到 WHT 是 DST/DCT 的特殊拟合，而基底函数有限。其本身在选取较大的窗口尺寸，且被使用在取值范围差异较大的原信号时，会导致一定程度的误差。工程中除非量化到门电路的粒度，其余大多时间还是用它来求解指定窗口范围，**残差信号（Residual Singnal）** 经哈达玛变换后 **绝对误差和（SATD [Sum of Absolute Transformed Difference]）** 。

而哈达玛变换后绝对误差和（SATD）取值，即是变换求得  的所有元素绝对值之和，有：

$$
{\displaystyle 
 \begin{aligned}
  SATD = \sum_i \sum_j |X_k(i,j)| \\ 
 \end{aligned}
}
$$

**以 SATD 来代替传统绝对误差和（SAD [Sum of Absolute Difference]）。利用 WHT 的加和快速运算特征计算残差趋势，协助时空域运动估计和数据量化的压缩处理。**

## **哈达玛变换的常见应用**

除此之外，如果我们换一种视角，将经过 IDST/IDCT 处理后的一系列子块所得结果，整合各子块得到的直流系数（DC）为一次输入给哈达玛变换。那么根据傅立叶变换特性，WHT 将对已经分离的低频权重信息，再次进行一次基于基底函数的分离。

而哈达玛变换仍属于傅立叶变换，这样的处理会使参与运算的 **直流系数（DC）** 所处子块，再进行一次变化程度的筛选，从而完成进一步细分并降低区域内的取值量级，更便于随后配合其它量化手段，减少信息熵。而小于 $$4 \times 4$$ 大小的哈达玛变换算子，并不会造成太大损失。

这个做法在 H.264 中得到了较为充分的体现。

H.264 中，对 YUV420 传输格式的亮度值 $$Y_k$$ 数据，取用了 $$16 \times 16$$ 点区域构成包含 $$4 \times 4$$ 个子块的范围，进行了两次特殊的哈达玛变换。得到 **二次直流系数矩阵 $$\hat{Y}_k$$ 作为传输值** ：

$$
{\displaystyle 
 \begin{aligned}
  H_{Y_1} =  
  \begin{bmatrix} 
    & 1 ,   & \quad 1 \ ,   & \quad 1 \ ,   & \quad 1   \\
    & 2 ,   & \    -1 \ ,   & \quad 1 \ ,   & \    -2   \\
    & 1 ,   & \quad 1 \ ,   & \    -1 \ ,   & \    -1   \\
    & 1 ,   & \    -2 \ ,   & \    -2 \ ,   & \quad 1   
  \end{bmatrix} \quad &H_{Y_2} =  
  \begin{bmatrix} 
    & 1 ,   & \quad 1 \ ,   & \quad 1 \ ,   & \quad 1   \\
    & 1 ,   & \    -1 \ ,   & \quad 1 \ ,   & \    -1   \\
    & 1 ,   & \quad 1 \ ,   & \    -1 \ ,   & \    -1   \\
    & 1 ,   & \    -1 \ ,   & \    -1 \ ,   & \quad 1   
  \end{bmatrix} \\
  \hat{Y}_k = H_{Y_2}\cdot (H_{Y_1} &\cdot Y_k|_{DC} \cdot H_{Y_1}) \cdot H_{Y_2}
 \end{aligned}
}
$$

而对色度分量 $$C_bC_r$$ 数据，则根据格式的数据组成和排布，取用了 $$8 \times 8$$ 点区域构成包含 $$2 \times 2$$ 个子块的范围，进行了单次标准哈达玛变换。得到 **二次直流系数矩阵 $$\hat{C}_b\hat{C}_r$$ 作为传输值** ： 

$$
{\displaystyle 
 \begin{aligned}
  &H_{C_bC_r} =   
  \begin{bmatrix} 
    & 1 \ ,   & 1 \\
    & 1 \ ,  -& 1 
  \end{bmatrix} \\ 
  \hat{C}_b &= H_{C_bC_r} \cdot C_b|_{DC}  \cdot H_{C_bC_r} \\
  \hat{C}_r &= H_{C_bC_r} \cdot C_r|_{DC}  \cdot H_{C_bC_r} \\
 \end{aligned}
}
$$

不过，随着小模型介入了二次变换压缩直流系数矩阵的过程，这套基于哈达玛变换（WHT）的压缩手段，最终还是被压缩比和还原程度更高的，以 **低频不可分变换（LFNST）为代表的高频凋零技术** ，替代了原有的作用。

因为如上的缘故，在现行最新的规格中，以压缩冗余为目的频域数据分离，大都仍然采用整数离散正余弦变换（IDST/IDCT） 为主要入口技术。哈达玛变换（WHT）则相对局限的，被使用在 SATD 上。


[ref]: References_3.md