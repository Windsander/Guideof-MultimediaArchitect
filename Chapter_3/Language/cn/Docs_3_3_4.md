
# 3.3.4 经典三刺激函数（Tristimulus Values Functions）

CIE 在 1931 年同年提出 CIE XYZ 色彩空间，尝试通过人为设计的色感函数 [\[12\]][ref] [\[13\]][ref]，来避 RGB 的 **负色匹配** 问题。为了区别于 CIE RGB 中，通过实验测定拟合而得的三原色色感函数。我们将新的函数称为 **CIE 三刺激函数（Tristimulus Values Functions）** ，用来代替原有 $${\overline {r}}(\lambda )$$ 、 $${\overline {g}}(\lambda )$$ 、 $${\overline {b}}(\lambda )$$ ，记为 $${\overline {x}}(\lambda )$$ 、 $${\overline {y}}(\lambda )$$ 、 $${\overline {z}}(\lambda )$$ 。三个刺激函数对应的刺激曲线如下图：

<center>
<figure>
   <img style="border-radius: 0.3125em;
      box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);" 
      width = "400" height = "400"
      src="../../Pictures/CIE%201931%20XYZ%20cmf.png" alt="">
   <figcaption>
      <p>图 3.3.4-1 CIE 1931 XYZ 采用的三原色色感函数</p>
   </figcaption>
</figure>
</center>

CIE 在三个刺激函数为基准下，确定了的不同波长光的三刺激值分离函数：

$$
{\displaystyle 
 \begin{align*}
 \begin{split} 
   &{\displaystyle X =\int _{0}^{\infty }S(\lambda )\,{\overline {x}}(\lambda )\,d\lambda  } \\
   &{\displaystyle Y =\int _{0}^{\infty }S(\lambda )\,{\overline {y}}(\lambda )\,d\lambda  } \\
   &{\displaystyle Z =\int _{0}^{\infty }S(\lambda )\,{\overline {z}}(\lambda )\,d\lambda  } \\
 \end{split}
 \end{align*}
}
$$

其中，
有 $${\overline {r}}(\lambda )$$ 、 $${\overline {g}}(\lambda )$$ 、 $${\overline {b}}(\lambda )$$ 是将理想刺激值峰值 $$(\mu ,\sigma _{1},\sigma _{2})$$ ，带入高斯公式所得，这和 RGB 色感函数的拟合有一定的不同。峰值  $$(\mu ,\sigma _{1},\sigma _{2})$$ 中， $$\mu$$ 代表峰值波长， $$\sigma _{1}$$ 代表 $$\mu$$ 值左侧生效范围偏移量， $$\sigma _{2}$$ 代表 $$\mu$$ 值右侧生效范围偏移量。XYZ 在度量峰值上取用了理想状态值，有：

$$
{\displaystyle 
   g(\lambda;\ \mu ,\sigma _{1},\sigma _{2}) = 
     {\begin{cases}
        \exp {\bigl (}{-{\tfrac {1}{2}}(\lambda-\mu )^{2}/{\sigma _{1}}^{2}}{\bigr )}, &\lambda<\mu ,\\
        \exp {\bigl (}{-{\tfrac {1}{2}}(\lambda-\mu )^{2}/{\sigma _{2}}^{2}}{\bigr )}, &\lambda\geq \mu .
      \end{cases}
   }
}
$$

推导而出：

$$
{\displaystyle 
 \begin{align*}
 \begin{split} 
   &{\displaystyle {\overline {x}}(\lambda ) = 1.056g(\lambda ;\ 599.8,\ 37.9,\ 31.0)+0.362g(\lambda ;\ 442.0,\ 16.0,\ 26.7)-0.065g(\lambda ;\ 501.1,\ 20.4,\ 26.2) } \\
   &{\displaystyle {\overline {y}}(\lambda ) = 0.821g(\lambda ;\ 568.8,\ 46.9,\ 40.5)+0.286g(\lambda ;\ 530.9,\ 16.3,\ 31.1)  } \\
   &{\displaystyle {\overline {z}}(\lambda ) = 1.217g(\lambda ;\ 437.0,\ 11.8,\ 36.0)+0.681g(\lambda ;\ 459.0,\ 26.0,\ 13.8)  } \\
 \end{split}
 \end{align*}
}
$$

而 $$S(\lambda )$$ 仍然为为目标波长 $$\lambda$$ 的光谱功率分布函数：

$$
{\displaystyle S(\lambda) = L_{\mathrm {e}}(\lambda)_{\theta=2^{\circ}}
                      \approx {\frac {\mathrm {d} ^{2}\Phi _{\mathrm {e} }(\lambda)}{\mathrm {d} A\,\mathrm {d} \Omega }}
                      ={\frac {\mathrm {d} E _{\mathrm {e} }(\lambda)}{d \Omega }}
                   }
$$

同样的，指定波长 $$\lambda$$ 的光线，就能被相对化表示为：

$$
Ray(\lambda)= C(X,Y,Z)
$$

通过以 $$(X,Y,Z)$$ 代替 $$(R,G,B)$$ 的度量方式，CIE XYZ 解决了负色匹配问题。为了区别于 $$(R,G,B)$$ 光学三原色的称谓，我们将 $$(X,Y,Z)$$ 称为 **三刺激值（Tristimulus Values）**。

不过，CIE 1931 RGB & CIE 1931 XYZ 中对于光学三原色标准波长的测量/设置，在现代光学体系中被认为有所偏颇的。在选取基准波长时，1931 RGB 蓝绿取用气态水银（Hg）放电获谱线产生的峰值波长  435.8nm（蓝）和 546.1nm（绿），而红色却因为人眼在对 700nm 波长附近的颜色感知几乎无变化的情况下，人为介入设定为还原配色实验理想值 700nm。这一历史局限性导致的情况，也被基于 RGB 测定而考量的 XYZ 继承了。以致于为两者的 “均色问题” 埋下了伏笔。

即便如此，经典三原色函数和三刺激函数，仍然为现代色彩体系奠定了基础公式。使我们能够 **以数理形式转换对应目标波长的目标光波，到相应的度量衡系统** 。


[ref]: References_3.md