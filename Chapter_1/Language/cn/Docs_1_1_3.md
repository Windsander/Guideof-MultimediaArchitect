
# 1.1.3 快速傅立叶（FFT [Fast Fourier Transform]）

**快速傅立叶是对离散傅立叶的数学逼近。其旨在通过有限点的分布拟合，快速逼近离散傅立叶变换结果。**

快速傅立叶变换最早由 **高斯（Carl Friedrich Gauss，1777 - 1855）** 为了解决天文学中有关于智神星（Pallas）和婚神星（Juno）的位姿计算问题，而在 1805 年提出的 [\[8\]][ref] [\[9\]][ref] 。不过由于种种意料之外的因素，让该论文并没有被及时的发表。因此，论文在当时也没有获得太多的关注。直到计算机开始兴起，有关傅里叶变换等算法的更为低时间复杂度的要求变的迫切，才让后续研究者们又一次察觉到了这一篇文献（以及包括 19 世纪中叶和 20 世纪初的旁类研究）的贡献 [\[9\]][ref] 。

1965 年，来自 IBM 普林斯通实验室的 **詹姆士·库利（James Cooley）** 和来自普林斯通大学的 **约翰·图奇（John Tukey）** 教授，联合发表了基于快速傅里叶变换的机器实现 [\[10\]][ref] ，首次将该算法迁移到了计算机上。他们的研究提出了，通过采用分治法的思想来减少变换所需步数。这成功的使得，多维信号分析所用的傅立叶算法的时间复杂度算法，降至 。促进了数字信号处理（DSP）和计算机图形学的技术更新 [\[11\]][ref] 。所以，为纪念两位的贡献，**这套程序化的快速傅里叶变换（FFT [Fast Fourier Transform]）方法论** ，被称为 **库利-图奇算法（Cooley-Tukey Algorithm）** 。**库利-图奇算法目标是一维信号**，不过高维信号是可以被拆解为低维信号的向量积的，因此 **并不影响其泛化** 。

在库利-图奇算法提出的时候，分治法已经被广泛的用来做计算机数组求最大值（Max）和排序（Sort）的处理当中。虽然离散的数组和周期信号之间，在信息密度和特征上存在较大差异。但如果考虑到周期信号沿传播维度重复，和傅里叶变换傅里叶基的特征，会发现：

如果将一维信号离散傅里叶变换的有限基底函数族 $${\mathcal {F}}_{\omega}$$ 构成的傅里叶基看作最小元，那么对其在时域上进行分组重排，也是可行的。从而使信号的一组基底函数基，能够以树状结构分类，并拆解特征表示原信号函数。

这就是库利-图奇算法的关键，在后续的算法的演进过程中逐步被提炼，形成了时域抽取这一核心概念 [\[11\]][ref] 。

## **快速傅里叶变换的核心 - 时域抽取（DIT [Decimation-in-Time]）**

**时域抽取（DIT [Decimation-in-Time]）是从时域（TD [Time Domain]）对一维信号进行可逆解构的一种数学工具。** 它的工作流包含有两个阶段：

**分组离散傅立叶（Group DFT）** 和 **位反转（Bit Reversal）周期混合** ；

**分组离散傅立叶（Group DFT）*** 是指，在信号的单个周期 $$T$$ 内，以等间距有限次取  个原始离散采样后。将周期内所有采样点信息以 $$step =\tfrac {T}{K} = N$$ 的步长等分，得到 $$K$$ 组顺序连续的子采样分组，依照组别记为样本子集 $$[S_1,S_2,\ ...\ , S_K]$$ 。每组子集都有 $$S_k \in [S((k-1) \cdot N),\ S(k \cdot N)]$$ 的样本取样区间。

此时，记组内索引为 $$n$$ ，有 $$n \in [1,\ N]$$ 。按照顺序从各组中，取组内索引位置为 $$n$$ 的元素，组成包含数据量为 $${\mathcal {F}}_{\omega_n}$$ 的基底函数 $${\mathcal {F}}_{\omega_n}$$ 的波峰数组。可以逐个拟合，得到一组当前一维信号的有限基底函数族 $${\mathcal {F}}_{\omega} = [{\mathcal {F}}_{\omega_1}, {\mathcal {F}}_{\omega_2},\dots,{\mathcal {F}}_{\omega_N}]$$ ，记为当前解的最小傅立叶基。根据一维离散傅立叶变换有：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega} = [{\mathcal {F}}_{\omega_1},{\mathcal {F}}_{\omega_2},& \ ...\ ,{\mathcal {F}}_{\omega_N}] \quad \quad T = NK \\
   \hat{f}(\omega) = \sum_{t = 0}^{T} f(t) \cdot e^{-i \omega t}  \ \ \ \ \ &\Leftrightarrow \ \ \ \ \ 
   f(t) = \frac{1}{K} \sum_{\omega_0}^{\omega_N} \hat{f}(\omega) \cdot {\mathcal {F}}_{\omega}(t)
 \end{aligned}
}
$$

又因 $${\omega_n} = \tfrac{2\pi n}{T}$$ ，强度系数 $$\hat{f}(\omega)$$ 与 $$f(t)$$ 的关系，可以被转换为 $$\hat{f}(n)$$ 与 $$f(t)$$ 的关系：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(\omega) = \sum_{t = 0}^{T} f(t) \cdot e^{-i \omega t} &\rightarrow \hat{f}(n)  =\sum_{t = 0}^{T} f(t) \cdot e^{-i \tfrac{2\pi n}{T} t } \\
   f(t) = \frac{1}{K} \sum_{\omega_0}^{\omega_{N}} \hat{f}(\omega) \cdot {\mathcal {F}}_{\omega}(t)  &\rightarrow f(t) = \frac{1}{K} \sum_{n=1}^{N} \hat{f}(n) \cdot {\mathcal {F}}_{\omega}(t) \\
   \hat{f}(n)  =\sum_{t = 0}^{T} f(t) \cdot e^{-i \tfrac{2\pi n}{T} t }  \quad \quad &\Leftrightarrow \quad \quad
   f(t) = \frac{1}{K} \sum_{n=1}^{N} \hat{f}(n) \cdot {\mathcal {F}}_{\omega}(t)
 \end{aligned}
}
$$

带入 $$K$$ 分组情况（ $$T = NK$$ ），上式可化为：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(n)  =\sum_{k=1}^{K}\sum_{(k-1)N}^{t = kN} f(t) \cdot e^{-i \tfrac{2\pi n}{T} t }  \quad \quad &\Leftrightarrow \quad \quad
   f(t) = \frac{1}{N} \sum_{n=1}^{N} \hat{f}(n) \cdot {\mathcal {F}}_{\omega}(t)
 \end{aligned}
}
$$

即强度系数 $$\hat{f}(n)$$ 存在展开式：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(n)  &= \sum_{k=1}^{K}\sum_{(k-1)N}^{t = kN} f(t) \cdot e^{-i \tfrac{2\pi n}{T} t } \\
               &= \sum_{t=1}^{N} f(t) \cdot e^{-i \tfrac{2\pi t}{T} \cdot n } 
                     + \sum_{t=N+1}^{2N} f(t) \cdot e^{-i \tfrac{2\pi t}{T} \cdot n } 
                     + \ ...\ 
                     + \sum_{(K-1)N+1}^{t=KN} f(t) \cdot e^{-i \tfrac{2\pi t}{T} \cdot n } 
                     + \ f(0) \\
               &= \sum_{t=1}^{N} f(t) \cdot e^{-i \tfrac{2\pi t}{T} \cdot n } 
                     + \sum_{t=1}^{N} f(t+N) \cdot e^{-i \tfrac{2\pi (t+N)}{T} \cdot n } 
                     + \ ...\ 
                     + \sum_{t=1}^{N} f(t + (K-1)N) \cdot e^{-i \tfrac{2\pi (t + (K-1)N)}{T} \cdot n } 
                     + \ f(0) \\
               &= \sum_{k=1}^{K} \sum_{t=1}^{N} f(t+ (k-1)N) \cdot e^{-i \tfrac{2\pi t}{T} n } \cdot e^{-i \tfrac{2\pi (k-1)}{K} n } + \ f(0)
 \end{aligned}
}
$$

**要点就出现在这里**，此时，由于有限基底函数族 $${\mathcal {F}}_{\omega} = [{\mathcal {F}}_{\omega_1}, {\mathcal {F}}_{\omega_2},\dots,{\mathcal {F}}_{\omega_N}]$$ 的拟合样本选取自各个分组的对应角标数据，则显然任意 $${\mathcal {F}}_{\omega_i}$$ 的周期都有 $$T_i = \tfrac{2\pi n}{\omega_i} \geq N$$ 且必然有 $$T_i \mod N = 0$$ 。另外， $$f(0)$$ 信号初相可以直接取 $$f(0) = 0$$ ，而不影响结果。因此，强度系数 $$\hat{f}(n)$$ 关于 $$k$$ 的展开式能进一步精简为：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(n)  &= \sum_{k=1}^{K} (\sum_{t=1}^{N} f(t+ (k-1)N) \cdot e^{-i \tfrac{2\pi t}{T} n }) \cdot e^{-i \tfrac{2\pi (k-1)}{K} n } \\
               &= \sum_{k=1}^{K} e^{-i \tfrac{2\pi (k-1)}{K} n } \cdot (\sum_{(k-1)N}^{t = kN} f(t) \cdot  {\mathcal {F}}_{\omega}^{-1}(n))
 \end{aligned}
}
$$

记 $$\hat{f}_k(n) =\sum_{(k-1)N}^{t = kN} f(t) \cdot  {\mathcal {F}}_{\omega}^{-1}(n)$$ ，则 $$\hat{f}_k(n)$$ 即为分组样本子集 $$[S_1,S_2,\ ...\ , S_K]$$ 在自己的分组样本区间 $$S_k \in [S((k-1) \cdot N),\ S(k \cdot N)]$$ 内，进行离散傅里叶变换的分组强度系数结果。而 $$e^{-i \tfrac{2\pi (k-1)}{K} n }$$ 在样本顺序 $$n$$ 给定时，只与所处分组的组序 $$k$$ 有关，且本身在三角函数空间表现为 $$n(k-1)$$ 的角度固定值，所以我们记其为旋转因子（Rotation Factor） $$R_k(n) = e^{-i \tfrac{2\pi (k-1)}{K} n }$$ 。

将 $$\hat{f}_k(n)$$ 、 $$R_k(n)$$ 带入 $$\hat{f}(n)$$ ，则 $$\hat{f}(n)$$ 最终表现为：

$$
{\displaystyle 
 \begin{aligned}
   R_1(n) & = 1 \\
   \hat{f}(n)  &= \sum_{k=1}^{K} R_k(n) \cdot \hat{f}_k(n) = R_1(n) \cdot \hat{f}_1(n) +  R_2(n) \cdot \hat{f}_2(n) + \ ...\ + R_K(n) \cdot \hat{f}_K(n) \\
   \hat{f}(n)  &= \hat{f}_1(n) +  R_2(n) \cdot \hat{f}_2(n) + \ ...\ + R_K(n) \cdot \hat{f}_K(n) 
 \end{aligned}
}
$$

**上式就是时域抽取（DIT）的分组离散傅立叶（Group DFT）的通用完整过程**。但是，大费周章的这么做有什么用处呢？


[ref]: References_1.md 