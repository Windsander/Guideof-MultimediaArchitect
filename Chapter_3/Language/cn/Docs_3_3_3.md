
# 3.3.3 经典三原色函数（Trichromatic Primaries Functions）

1921 年左右，**威廉·大卫·赖特（W. David Wright，1906 - 1997）** ** [\[26\]][ref] 与 **约翰·吉尔德（John Guild，1889 - 1976）** ** [\[27\]][ref] 分别对光学三原色的基本度量系数进行了更为科学的测定，并分别于1928年 、1932年以论文形式发表了自己的结果。这两个实验，为 **CIE 经典三原色函数（Trichromatic Primaries Functions）标准** 的制定提供了极为关键的帮助。

我们将代表不同可见光波长对人眼视锥细胞的刺激程度的函数，称为色感函数，也就是选取人眼为传感器的 **光谱响应函数（SPF [Spectral Response Function]）**。由色感函数在可见光波段所构成的曲线，称为色感曲线。由实验所拟合的三原色的色感曲线，在 435.8nm（蓝）、 546.1nm（绿）、 700nm（红）处达到最大峰值，如下图：

<center>
<figure>
   <img style="border-radius: 0.3125em;
      box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
      width = "400" height = "400"
      src="../../Pictures/CIE%201931%20RGB%20cmf.png" alt="">
   <figcaption>
      <p>图 3.3.3-1 CIE 1931 RGB 采用的三原色色感函数</p>
   </figcaption>
</figure>
</center>

CIE 在两者实验的基础上，确定了以 **光谱功率分布（SPD [Spectral Power Distribution]）** 为基准的混合波三色分离函数：

$$
{\displaystyle 
 \begin{aligned}
   &{\displaystyle R =\int _{0}^{\infty }S(\lambda )\,{\overline {r}}(\lambda )\,d\lambda  } \\
   &{\displaystyle G =\int _{0}^{\infty }S(\lambda )\,{\overline {g}}(\lambda )\,d\lambda  } \\
   &{\displaystyle B =\int _{0}^{\infty }S(\lambda )\,{\overline {b}}(\lambda )\,d\lambda  } \\
 \end{aligned}
}
$$

其中，
以 $${\overline {r}}(\lambda )$$ 、 $${\overline {g}}(\lambda )$$ 、 $${\overline {b}}(\lambda )$$ 即为基准三原色实验测得的拟合结果的色感函数，存在关系： 

$$
{\displaystyle \int _{0}^{\infty }{\overline {r}}(\lambda )\,d\lambda 
  =\int _{0}^{\infty }{\overline {g}}(\lambda )\,d\lambda 
  =\int _{0}^{\infty }{\overline {b}}(\lambda )\,d\lambda 
}
$$

有 $$S(\lambda )$$ 为目标波长 $$\lambda$$ 的光谱功率分布函数：

$$
{\displaystyle S(\lambda) = L_{\mathrm {e}}(\lambda)_{\theta=2^{\circ}}
                      \approx {\frac {\mathrm {d} ^{2}\Phi _{\mathrm {e} }(\lambda)}{\mathrm {d} A\,\mathrm {d} \Omega }}
                      ={\frac {\mathrm {d} E _{\mathrm {e} }(\lambda)}{d \Omega }}
                   }
$$

SPD 公式式中，$$L_{\mathrm {e}}$$ 为辐射亮度， $$\Phi _{\mathrm {e}}$$ 为辐射通量为， $$E _{\mathrm {e}}$$ 为辐射照射度。

通过这几个属于 **辐射度学（Radiometry）** 中的可被测量物理量，指定波长  的光线，就能被相对化表示为：

$$
Ray(\lambda)= C(R,G,B)
$$

由于 CIE RGB 所采用的改进后的配色实验，仍然存在亥姆霍兹配色实验里就存在的红光波段的负色匹配。

>因此还需要进一步改进才能用于工业应用。


[ref]: References_3.md