
# 3.1.2 二维傅立叶（2D-FT）与二维离散傅立叶变换（2D-DFT）

信号学中，将沿空间分布的信号称为二维信号（2D Signal）。图像信号就是二维信号。

二维傅里叶变换，能够将一组二维信号分解到 **周期性复平面波（Complex Plane Wave）** 构成的三维向量空间。

什么是平面波呢？延空间传播的选定波，若有任意时刻的相位相同的点连接起来得到的波阵面（同相位面）为互相平行的平面，就可以被称为 **平面波（Plane Wave）**。如果平面波同时满足简谐振动（即以正余弦规律振动）的特征，则可称为 **平面简谐波（Plane Harmonic Waves）** 。复平面波则指的是在复数空间下的平面波。

## **从一维到二维傅里叶变换（2D-FT）**

如果说一维信号是由一组数据延单一方向排布组成的数字序列，那么二维信号就是由一组数据延横向和纵向两个方向排布构成的数字平面。在一维信号处理时，我们将复指数函数分解为一系列一维简谐波的组合。同样的处理方式，我们也可以类比应用在二维信号场景，将构成二维信号的相关复平面波分解为在复数空间下的一系列复平面简谐波的聚合，进而把二维信号以相关强度参数，转化为平面简谐波的叠加表示。

一维信号和二维信号仅仅是维度上的差异。因此，结合向量空间，我们引入波的方向矢量，并取其大小等于当前波的角频率来表示波本身，称为波矢 $${\vec{k}}$$ 。将波矢为 $${\vec{k}}$$ 的平面简谐波，称为 $${\vec{k}}$$ 平面波。

对于周期为 $$T$$ 的一维信号，因为时间只能沿着时间轴正向流动，所以此时的 $${\vec{k}}$$ 不存在方向。其基础波函数的波矢 $${\vec{k}}$$ 只有大小，即 $$\omega = \vert {\vec{k}} \vert$$ 。所以在一维傅里叶变换中，我们只考虑了时间与频率的关系，即一维的时频关系。

对于周期为 $$T$$ 的二维信号，以可变 $$n$$ 等分选取作为基础的复平面波，记波函数为 $${\mathcal {F}}_{\omega}(x,y)$$ ，则波长（周期）$$\lambda = \tfrac{T}{n}$$ ，角频率（角速度）为 $$\omega = \vert {\vec{k}} \vert = \tfrac{2\pi}{\lambda}$$ 。将 $${\mathcal {F}}_{\omega}(x,y)$$ 的传播方向 $$(u,v)$$ 限定 $$u \in [-\tfrac{U}{2}, \ +\tfrac{U}{2}]$$ ，$$v \in [-\tfrac{V}{2}, \ +\tfrac{V}{2}]$$ 的范围。则 $$(u,v)$$ 与原点的欧式距离，实际代表的是该方向上的分割强度值 $$n$$ ，有：

$$
{\displaystyle 
 \begin{aligned}
    \sqrt{U^2 \ \ + \ \ V^2} \ =  \ T \ \ \ \rightarrow \ \ \ \sqrt{(\tfrac{u}{T})^2 \ \ + \ \ (\tfrac{v}{T})^2} \ = \ n \\
 \end{aligned}
}
$$

因此，代表 $${\mathcal {F}}_{\omega}(x,y)$$ 的波矢 $${\vec{k}} = (\tfrac{2 \pi \cdot {u}}{U} \ , \ \tfrac{2 \pi \cdot {v}}{V} ) = (\xi, \ \eta)$$ ，推得：

$$
{\displaystyle 
 \begin{aligned}
    &\omega = \vert {\vec{k}} \vert = \sqrt{({\tfrac{2 \pi \cdot u}{U}})^2 + ({\tfrac{2 \pi \cdot v}{V}})^2} = \tfrac{2 \pi}{\lambda} \\ 
       & \quad \rightarrow {\xi}^2 \ \ + \ \ {\eta}^2 \ =  \ {\omega}^2 \\
 \end{aligned}
}
$$
$$
{\displaystyle 
 {\mathcal {F}_{\omega}(x,y)} = e^{i \vec{k} \cdot (x,y)^T } 
     = e^{i \cdot {2 \pi} (\tfrac{u}{U}x+\tfrac{v}{V}y)} 
     = {\mathcal {F}_{\xi}(x)} \cdot {\mathcal {F}_{\eta}(y)}
}
$$

上式对复平面波 $${\mathcal {F}}_{\omega}(x,y)$$ 的拆解，从数理上表明了，$${\mathcal {F}}_{\omega}(x,y)$$ 是由沿着 $$x$$ 轴方向的一维波 $${\mathcal {F}}_{\xi}(x)$$ 和沿着 $$y$$ 轴方向的一维波 $${\mathcal {F}}_{\eta}(y)$$ 两部分构成。其中，$$\xi = \tfrac{2\pi \cdot u}{U}$$ 为 $${\mathcal {F}}_{\xi}(x)$$ 的角频率，$$\eta = \tfrac{2\pi \cdot v}{V}$$ 为 $${\mathcal {F}}_{\eta}(y)$$ 的角频率。点位 $$(x,y)$$ 在二维信号中代表的是实际像素数据在数字平面上的空间位置信息。所以在处理二维傅里叶变换时，我们需要考虑的是平面空间点 $$\vec{P}(x,y)$$ 与 $${\vec{k}}$$ 平面波间的关系，即二维的空频关系。


## **解构二维信号 - 空频分离（Spacial-Frequency Separation）**

记原二维信号的函数表达为 $$f(x,y)$$ ，有任意点 $$\vec{P}(x,y)$$ 可取 $$x \in [0, \ W]$$ ， $$y \in [0, \ H]$$ ，那么对于二维信号来说，周期 $$T= \sqrt{W^2+H^2}$$。保持 $$u \in [-\tfrac{U}{2}, \ \tfrac{U}{2}]$$ 、$$v \in [-\tfrac{V}{2}, \ \tfrac{V}{2}]$$ 范围，则 $${\mathcal {F}}_{\omega}(x,y)$$ 沿传播方向角频率 $$(\xi, \eta)$$ 就有 $$\xi \in [-\pi, \ +\pi]$$ ， $$\eta \in [-\pi, \ +\pi]$$ 。则由一维拓展至二维傅里叶级数可知， $$f(x,y)$$ 与波函数 $${\mathcal {F}}_{\omega}(x,y)$$ 的分量权重系数 $${\hat{a}_{\omega}} (u, v) $$ 、 $${\hat{b}_{\omega}} (u, v) $$ 存在：

$$
{\displaystyle 
 \begin{aligned}
   f(x, y) &= \frac{1}{U\cdot V} (\sum_{u =0}^{\infty} \sum_{v =0}^{\infty} {\hat{a}_{\omega}} \cdot cos(\vec{k} \cdot \vec{P}^T)\ \ \  + \ \ \sum_{u =0}^{\infty} \sum_{v =0}^{\infty} {\hat{b}_{\omega}} \cdot sin(\vec{k} \cdot \vec{P}^T)) \\ 
   {\hat{a}_{\omega}} (u, v) &= \int_{0}^{H} \int_{0}^{W} f(x,y) \cdot cos({2 \pi} \cdot (\tfrac{u}{U}x+\tfrac{v}{V}y)) \ dx \ dy \\ 
   {\hat{b}_{\omega}} (u, v) &= \int_{0}^{H} \int_{0}^{W} f(x,y) \cdot sin({2 \pi} \cdot (\tfrac{u}{U}x+\tfrac{v}{V}y)) \ dx \ dy \\ 
 \end{aligned}
}
$$

取 $${\mathcal {F}}_{\omega}(x,y)$$ 初相为 $$\angle\phi_{\omega}$$ ，振幅为 $$A_{\omega}$$ ，则仍然有 $${\mathcal {F}}_{\omega}(x,y)$$ 的简谐波特征表示：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega}(x,y) &: \\
   \angle\phi_{\omega} &= \angle{\vert \hat{f}(x,y) \vert} \ = \arctan(\tfrac{\hat{a}_{\omega}}{\hat{b}_{\omega}}) \\
   A_{\omega} &=\ \  \Vert \hat{f}(x,y) \Vert _2 =\sqrt{ (\hat{a}_{\omega}) ^2 + (\hat{b}_{\omega}) ^2 } \\
 \end{aligned}
}
$$

因此，带入 $${\mathcal {F}}_{\omega}(x,y)$$ ，有 $$f(x,y)$$ 的二维傅里叶变换展开为：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega}(x,y) &= {\mathcal {F}}_{\omega} (\vec{P})
                              = A_{\omega} \cdot sin(\vec{k} \cdot \vec{P}^T -\angle\phi_{\omega}) = A_{\omega} \cdot cos(\vec{k} \cdot \vec{P}^T +\angle\phi_{\omega}) \\
                              &= {\Vert \hat{f}(x,y) \Vert _2} \cdot sin(\omega \cdot \vec{v}^T -\angle{\vert \hat{f}(x,y) \vert}) 
                               = {\Vert \hat{f}(x,y) \Vert _2} \cdot cos(\omega \cdot \vec{v}^T +\angle{\vert \hat{f}(x,y) \vert}) \\
   \hat{f}(u,v) &= \int_{0}^{H} \int_{0}^{W} f(x,y) \cdot e^{-i (ux+vy)}\ dx \ dy \ \ \ \ \ \Leftrightarrow \ \ \ \ \ 
   f(x,y) = \frac{1}{U\cdot V} \int_{-\tfrac{V}{2}}^{+\tfrac{V}{2}} \int_{-\tfrac{U}{2}}^{+\tfrac{U}{2}} \hat{f}(u,v) \cdot {\mathcal {F}}_{\omega}(x, y) \ du \ dv \\
 \end{aligned}
}
$$

一般情况为了方便起见，常取 $$U =  W$$ 、 $$V =  H$$ ，化简分离参数。上式即为二维傅里叶变换的基本形式。

如果波矢范围在 $$\vec{k} \in [\vec{k_0},\ \vec{k_1}]$$ ，对于任意数据平面的像素点 $$P(x,y)$$ ，有频率 $$\omega = \Vert \vec{k} \Vert_2$$ 传播方向 $$(u,v)$$ 、基底函数族 $${\mathcal {F}}_{\omega}(x,y) $$ 的强度系数 $$\hat{f}_{\omega}(u,v)$$ ，构成该波矢范围的 **频域投影（FDP [Frequency Domain Projection]）**；

反之，如果选定像素点 $$P(x,y)$$ ，对于波矢范围在 $$\vec{k} \in [\vec{k_0},\ \vec{k_1}]$$ ，有平面位置 $$P(x,y)$$ 、原函数值 $$f(x,y)$$ 、基底函数族 $${\mathcal {F}}_{\omega}(x,y) $$ ，构成原函数在该空间（二维）范围的 **空域投影（SDP [Spacial Domain Projection]）**。

两者的区别同一维一样，仅在于观察角度的不同：

$$
{\displaystyle 
 \begin{aligned}
   {Frequency\ Domain\ Projection:}  &\ \ (\ \ u\ \    ,\ \ v\ \    ,\ \ \hat{f}_{\omega}(u,v)\ \ )  \\
   {Spacial\ Domain\ Projection:}       &\ \ (\ \ x\ \    ,\ \ y\ \    ,\ \ f(x,y)\ \ ,\ \ {\mathcal {F}}_{\omega}(x,y) \ \ )  \\
   {\vec{k} \in [\vec{k_0},\ \vec{k_1}]}   \ \ \ \ & \ \  {\ \vec{P}(x,y)\ \in [\ (0,\ 0)\ \ ,\ \ (W,\ H)\ ]} \\
 \end{aligned}
}
$$

显然，二维和一维情况的差异很明显且必然：二维傅里叶变换下所获的的分离投影结果位于三维欧式空间，而非一维时的平面（二维）。

## **精简运算过程 - 二维离散傅立叶变换（2D-DFT）**

同一维傅里叶变换需要做时域离散化（TDD）和频域离散化（FDD）来精简运算量。二维傅里叶变换由于引入了新的维度，更需要依赖离散化处理，才能被计算机在有限算力的前提下使用。

二维离散傅里叶变换（2D-DFT）分为 **空域离散化（SDD [Spacial Domain Discrete]）** 和 **频域离散化（FDD [Frequency Domain Discrete]）** 。当然，此处的空域为二维空域（平面），是不包含 $$z$$ 轴的。我们将两者结合称为 **空频离散化（SFD [Spacial Frequency Discrete]）**。

如果取任意点 $$\vec{P}(x,y)$$ 可取 $$x \in [0, \ 1, \ \ ...\  , \ W]$$ ， $$y \in [0, \ 1, \ \ ...\  , \ H]$$ ，只取整数位置。同时， $$u \in [-\tfrac{U}{2}, \ \ ...\  , \ +\tfrac{U}{2}]$$ 、 $$v \in [-\tfrac{V}{2}, \ \ ...\  , \ +\tfrac{V}{2}]$$ ，有离散 $$\vec{k} \in [\vec{k_0}, \ \vec{k_1}, \ \ ...\ , \ \vec{k_{n}}]$$ ， $$n = UV = HW$$ ，则：

$$
{\displaystyle 
 \begin{aligned}
   SDD: \ \ \hat{f}(u,v) &= \sum_{x = 0}^{W} \sum_{y = 0}^{H}  f(x,y) \cdot e^{-i (ux+vy)} \\
   FDD: \ \ f(x,y) &=  \frac{1}{U\cdot V} \sum_{u=-U/2}^{+U/2} \sum_{v= -V/2}^{+V/2} \hat{f}(u,v) \cdot {\mathcal {F}}_{\omega}(x, y) \\
 \end{aligned}
}
$$

至此，由空域离散化（SDD）与频域离散化（FDD）共同构成二维离散傅立叶（2D-DFT）的完整表达如下所示：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega} = [{\mathcal {F}}_{\vec{k_0}},&{\mathcal {F}}_{\vec{k_1}},\ ...\ ,{\mathcal {F}}_{\vec{k_n}}]  \\
   \hat{f}(u,v) = \sum_{x = 0}^{W} \sum_{y = 0}^{H}  f(x,y) \cdot e^{-i (ux+vy)}  \ \ \ \ \ \Leftrightarrow & \ \ \ \ \ 
   f(x,y) = \frac{1}{U\cdot V} \sum_{u=-U/2}^{+U/2} \sum_{v= -V/2}^{+V/2} \hat{f}(u,v) \cdot {\mathcal {F}}_{\omega}(x, y) \\
 \end{aligned}
}
$$

利用上式，既可做算法实现。

## **二维离散傅立叶变换（1D-DFT）的 C 语言实现**

第一步还是将二维离散傅立叶变化的过程抽象化。这里依旧采用伪码表示：

```C++
/**
 * 2D-DFT [Discrete Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[W][H] = {...};
 *     Fn[U][V] = {};
 *     dft_2d(&Fo, &Fn);
 * [logistic]
 * {
 *   result[U][V] = []; // as byte 2D-array
 *   // do SDD:
 *   for u in range(NU-Horizontal_Slices) {
 *   for v in range(NV-Vertical_Slices)   {
 *     An = 0; Bn = 0;
 *     // do FDD:
 *     for y in Range(Height) {
 *     for x in Range(Wight)  {
 *       Wn = (2 * PI) * Vec< (u / U , v / V)>;
 *       An = Re += Cos(Wn · Vec<x,y>T) * Fo(t);
 *       Bn = Im += Sin(Wn · Vec<x,y>T) * Fo(t);
 *     }}
 *     result[u][v] = Fn.to_complex_angular_form(An, Bn)
 *   }}
 *   return result;
 * }
 * @param original_ Original Function input 2D-array
 *           (image include width & height)
 * @param analyzed_ Fourier Basis info in 2D
 */
```

同时，二维情况也需要提供离散傅里叶变换的逆变换（IDFT [Inverse Discrete Fourier Transform]）来使得电脑能够还原信息：

```C++
/**
 * 2D-IDFT [Inverse Discrete Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[W][H] = {};
 *     Fn[U][V] = {...};
 *     idft_2d(&Fo, &Fn);
 * [logistic]
 * {
 *   result[W][H] = []; // as byte 2D-array
 *   // do SDD:
 *   for y in Range(Height) {
 *   for x in Range(Wight)  {
 *     Re = 0; Im = 0;
 *     // do FDD:
 *     for u in range(NU-Horizontal_Slices) {
 *     for v in range(NV-Vertical_Slices)   {
 *       Wn = (2 * PI) * Vec< (u / U , v / V)>;;
 *       An = Re * (Fn[n] · Vec<x,y>T);
 *       Bn = Im * (Fn[n] · Vec<x,y>T);
 *       result[t] += Fn[n].to_value(Wn, An, Bn) / (U * V);
 *     }}
 *   }
 *   return result;
 * }
 * @param original_ Original Function input 2D-array
 *           (image include width & height)
 * @param analyzed_ Fourier Basis analyzed info in 2D
 */
```

接下来只需要根据思路做代码实现即可：

```C++
#include "stdio.h"
#include "math.h"

#define PI 3.1415926f

typedef struct FBasis {
    double re_;
    double im_;
    double w_[2];
} FBasis;

typedef struct Signal2DOriginal {
    int GW_;
    int GH_;
    double *Fo_;
} Signal2DOriginal;

typedef struct Signal2DAnalyzed {
    int NU_;
    int NV_;
    FBasis *Fn_;
} Signal2DAnalyzed;

void dft_2d(Signal2DOriginal *original_, Signal2DAnalyzed *analyzed_) {
    for (int u = 0; u < analyzed_->NU_; ++u) {
        for (int v = 0; v < analyzed_->NV_; ++v) {
            double An = 0;
            double Bn = 0;
            double Un = (2 * PI / analyzed_->NU_) * u  ;
            double Vn = (2 * PI / analyzed_->NV_) * v  ;
            for (int y = 0; y < original_->GH_; ++y) {
                for (int x = 0; x < original_->GW_; ++x) {
                    An += cos(Un * x + Vn * y) * original_->Fo_[y * original_->GW_ + x];
                    Bn += sin(Un * x + Vn * y) * original_->Fo_[y * original_->GW_ + x];
                }
            }
            FBasis e_ = {An, Bn, {Un, Vn}};
            analyzed_->Fn_[u * analyzed_->NV_ + v] = e_;
        }
    }
}

void idft_2d(Signal2DOriginal *original_, Signal2DAnalyzed *analyzed_) {
    for (int y = 0; y < original_->GH_; ++y) {
        for (int x = 0; x < original_->GW_; ++x) {
            for (int u = 0; u < analyzed_->NU_; ++u) {
                for (int v = 0; v < analyzed_->NV_; ++v) {
                    FBasis e_ = analyzed_->Fn_[u * analyzed_->NV_ + v];
                    original_->Fo_[y * original_->GW_ + x] += (
                        e_.re_ * cos(e_.w_[0] * x + e_.w_[1] * y) +
                        e_.im_ * sin(e_.w_[0] * x + e_.w_[1] * y)
                    ) / (analyzed_->NU_ * analyzed_->NV_);
                }
            }
        }
    }
}
```

写完后还是需要简单测试一下：

```C++
int main(void) {
    double input_data_[36] = {
        1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f,
        2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 1.0f,
        3.0f, 4.0f, 5.0f, 6.0f, 1.0f, 2.0f,
        4.0f, 5.0f, 6.0f, 1.0f, 2.0f, 3.0f,
        5.0f, 6.0f, 1.0f, 2.0f, 3.0f, 4.0f,
        6.0f, 1.0f, 2.0f, 3.0f, 4.0f, 5.0f
    };
    FBasis output_data_[36] = {};
    double versed_data_[36] = {};

    Signal2DOriginal Fo = {
        6, 6,
        input_data_
    };
    Signal2DAnalyzed Fn = {
        6, 6,
        output_data_
    };
    Signal2DOriginal iFo = {
        6, 6,
        versed_data_
    };

    printf("\n Original_data: \n");
    for (int y = 0; y < Fo.GH_; ++y) {
        for (int x = 0; x < Fo.GW_; ++x) {
            printf("%f  ", Fo.Fo_[x + y * Fo.GW_]);
        }
        printf("\n");
    }

    printf("\n DFT_result: \n");
    dft_2d(&Fo, &Fn);
    for (int v = 0; v < Fn.NV_; ++v) {
        for (int u = 0; u < Fn.NU_; ++u) {
            printf("%.3f + i %.3f   ", 
                    Fn.Fn_[u + v * Fn.NU_].re_, 
                    Fn.Fn_[u + v * Fn.NU_].im_
            );
        }
        printf("\n");
    }

    printf("\n IDFT_result: \n");
    idft_2d(&iFo, &Fn);
    for (int y = 0; y < iFo.GH_; ++y) {
        for (int x = 0; x < iFo.GW_; ++x) {
            printf("%f  ", iFo.Fo_[x + y * Fo.GW_]);
        }
        printf("\n");
    }

    return 0;
}
```

得到结果和标准几近相同：

```
 Original_data: 
1.000000  2.000000  3.000000  4.000000  5.000000  6.000000  
2.000000  3.000000  4.000000  5.000000  6.000000  1.000000  
3.000000  4.000000  5.000000  6.000000  1.000000  2.000000  
4.000000  5.000000  6.000000  1.000000  2.000000  3.000000  
5.000000  6.000000  1.000000  2.000000  3.000000  4.000000  
6.000000  1.000000  2.000000  3.000000  4.000000  5.000000  

 DFT_result: 
126.000 + i 0.000   -0.000 + i 0.000   -0.000 + i 0.000   0.000 + i 0.000   0.000 + i 0.000   0.000 + i 0.000   
-0.000 + i 0.000   -18.000 + i -31.177   0.000 + i 0.000   0.000 + i -0.000   0.000 + i -0.000   0.000 + i -0.000   
-0.000 + i 0.000   0.000 + i 0.000   -18.000 + i -10.392   0.000 + i -0.000   0.000 + i -0.000   0.000 + i -0.000   
0.000 + i 0.000   0.000 + i -0.000   0.000 + i -0.000   -18.000 + i 0.000   0.000 + i -0.000   -0.000 + i -0.000   
0.000 + i 0.000   0.000 + i -0.000   0.000 + i -0.000   0.000 + i -0.000   -18.000 + i 10.392   -0.000 + i -0.000   
0.000 + i 0.000   0.000 + i -0.000   0.000 + i -0.000   -0.000 + i -0.000   -0.000 + i -0.000   -18.000 + i 31.177   

 IDFT_result: 
1.000007  2.000001  2.999999  3.999999  5.000001  6.000003  
2.000001  2.999998  3.999998  4.999998  5.999999  1.000000  
2.999999  3.999998  4.999997  5.999998  0.999998  2.000000  
3.999999  4.999998  5.999998  0.999997  1.999999  3.000001  
5.000001  5.999999  0.999998  1.999999  3.000000  4.000003  
6.000003  1.000000  2.000000  3.000001  4.000003  5.000005
```

运行结束。

二维离散傅里叶变换到此结束，那么更多维度的傅里叶变换该怎么处理呢？我们只需要拓展波矢 $${\vec{k}}$$ 的维度即可。而多维和一维、二维情况，在离散傅里叶变换的逻辑流程上并没有不同。但是，随着波矢 $${\vec{k}}$$ 的参数维度扩展，我们发现现有的直接计算法实现的离散傅里叶变换，其算法时间复杂度 $$O\{ n^2\}$$ 已不足以支撑超过二维参数量后的敏捷计算。因此，我们迫切需要一种更快的代替算法。

>这就是促成快速傅立叶蝴蝶法工程化的要素。


[ref]: References_3.md 