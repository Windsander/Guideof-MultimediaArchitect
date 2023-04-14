
# 1.1.1 一维傅立叶（1D-FT）与一维离散傅立叶变换（1D-DFT）

信号学中，将沿平面分布的信号称为一维信号（1D Signal），例如音频信号。

一维傅里叶变换，能够将一组满足狄利克雷条件（Dirichlet Theorem）的一维信号分解到周期性复指数波（Complex Exponential Wave）构成的二维向量空间。

## **从傅里叶级数（FS）到傅里叶变换（FT）**

**狄利克雷条件** 最初被用作傅里叶级数（FS [Fourier Series]）在三角函数域上进行分解的充分不必要条件 [\[2\]][ref] [\[7\]][ref]。在狄利克雷条件描述中，如果选定分析的周期信号  同时满足：

- 【单周期内，连续或存在有限个第一类间断点】；
- 【单周期内，存在有限数目的极大值与极小值】；
- 【单周期内，绝对可积】；

则，此周期信号就一定存在傅里叶三角级数的分解表示。
	
如果记周期信号函数 $$s(t)$$ 的波长（周期）为 $$T$$ ，角频率（角速度）为 $$\tfrac{2\pi}{T}$$ 。则以信号函数波长 $$T$$ 做可变 $$n \in [0, \ N]$$ 等分（即步长 $$Step = \tfrac{1}{N}$$ ）选取分离函数。有分离函数（周期）为 $$\tfrac{T}{n}$$ ，角频率（角速度）为 $${\omega_n} = \tfrac{2\pi n}{T}$$ 。原周期信号函数 $$s(t)$$ 就可以被分解为：

$$
{\displaystyle 
 \begin{aligned}
   s(t) &= \frac{1}{N} \sum_{n =0}^{N} a_n \cdot cos(\tfrac{2\pi n}{T}t)\ \ \ \ \ \  +\ \ \ \ \ \frac{1}{N} \sum_{n =0}^{N} b_n \cdot sin(\tfrac{2\pi n}{T}t) \\ 
   a_n  &= \int_{-\tfrac{T}{2}}^{+\tfrac{T}{2}} s(t) \cdot cos(\omega_n t) \ dt \ \ \ \ \ 
   b_n  = \int_{-\tfrac{T}{2}}^{+\tfrac{T}{2}} s(t) \cdot sin(\omega_n t) \ dt \\
 \end{aligned}
}
$$

如果我们对函数周期进行平移，将区间从 $$(-\tfrac{T}{2},\ +\tfrac{T}{2})$$ 偏移 $$+\tfrac{T}{2}$$ ，即变换到 $$(0,\ T)$$ ，使原周期信号函数 $$s(t)$$ 偏移为奇函数（即 $$s(-t) = - s(t)$$ ），而奇函数式可证明是不需要余弦函数项的。此时，就可以进一步化简 $$s(t)$$ 为存粹正弦函数表示：

$$
{\displaystyle 
 \begin{aligned}
   s(t) &= \frac{1}{N} \sum_{n =0}^{N} b_n \cdot sin(\tfrac{2\pi n}{\lambda}t) = \frac{1}{N} \sum_{n =0}^{N} b_n \cdot sin(\omega_n t)  \\
   b_n  &= \int_{0}^{T} s(t) \cdot sin(\omega_n t) \ dt \\
 \end{aligned}
}
$$

简化表示 $${\omega_n}$$ 为 $${\omega}$$ ，当我们将傅里叶级数从三角函数域，扩展到复变函数域时，基底函数由正余弦函数变为了以 $${\displaystyle 
 \begin{aligned}
   \lambda = \tfrac{2 \pi}{\omega} = \tfrac{T}{n}\\
 \end{aligned}
}$$ 为周期（波长）的复指数函数 $${\displaystyle 
 \begin{aligned}
   {\mathcal {S}}_{\omega}(t) = e^{i\omega t}\\
 \end{aligned}
}$$ 。信号函数 $$s(t)$$ 的分解函数就可以表示为：

$$
{\displaystyle 
 \begin{aligned}
   s(t) &= \frac{1}{N} \sum_{n = 0}^{N} \hat{s}(\tfrac{2\pi n}{T}) \cdot e^{i \tfrac{2\pi n}{T}t}  
         = \frac{1}{N} \sum_{\omega = 0}^{\omega_N} \hat{s}(\omega) \cdot e^{i \omega t}  \\
        &= \frac{1}{N}\sum_{n = 0}^{N} \hat{s}(\omega) \cdot {\mathcal {S}}_{\omega}(t) \\
   \hat{s}(\omega)  &= \int_{0}^{T} s(t) \cdot e^{-i \omega t} \ dt \\
 \end{aligned}
}
$$

根据根据欧拉公式（Euler's Formula）可知 $${\displaystyle 
 \begin{aligned}
   e^{ix} = cos(x) + i \cdot sin(x) \\
 \end{aligned}
}$$ ， 带入上式有：

$$
{\displaystyle 
 \begin{aligned}
   s(t)  &= \frac{1}{N}\sum_{n = 0}^{N} \hat{a}_{\omega} \cdot cos(\omega t) + i \cdot \hat{b}_{\omega} \cdot sin(\omega t)\\
   \hat{a}_{\omega}  &= \hat{s}(-\omega) + \hat{s}(\omega)  \ \ \ \ \ 
   \hat{b}_{\omega}  = \tfrac{1}{i} \cdot (\hat{s}(-\omega)-\hat{s}(\omega)) \\
 \end{aligned}
}
$$
	
转换到欧氏空间下的三角函数表示 $${\mathcal {S}}_{\omega}(t)$$ ，记构成原信号函数 $$s(t)$$ 的复指数函数 $${\mathcal {S}}_{\omega}(t)$$ 的初相为 $$\angle\phi_{\omega}$$ ，振幅为 $$A_{\omega}$$ ，则：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {S}}_{\omega}(t) : \ \ \ \
   \angle\phi_{\omega} = \arctan(\tfrac{\hat{a}_{\omega}}{\hat{b}_{\omega}}) \ \ \ \ 
   A_{\omega} = \sqrt{ (\hat{a}_{\omega}) ^2 + (\hat{b}_{\omega}) ^2 } \\
 \end{aligned}
}
$$

同三角函数域的情况，复变函数域下的傅里叶级数仍然可以进一步精简。我们仍然需要对原函数 $$s(t)$$ 平移 $$+\tfrac{\lambda}{2}$$ 并将周期变换到 $$(0,\ \lambda)$$ ，使 $$s(t)$$ 表现为奇函数。由于原信号函数 $$s(t)$$ 必为实函数的特性，会使得 $$a_{\omega}$$ 与 $$b_{\omega}$$ 互为共轭复数。因此在奇函数条件下， $$a_{\omega}$$ 与 $$b_{\omega}$$ 表现为符号相反的纯虚数，此时：

$$
{\displaystyle 
 \begin{aligned}
   \hat{a}_{\omega}  &= 1 \cdot [\hat{s}(-\omega) + \hat{s}(\omega)] = 0   \ \ \ \ \ 
   \hat{b}_{\omega}  = \tfrac{1}{i} \cdot [\hat{s}(-\omega)-\hat{s}(\omega)] = \tfrac{2}{i} \cdot \hat{s}(-\omega) \\
   s(t)  &= \frac{1}{N} \sum_{\omega =0}^{\omega_N} \ \ \ \ 0 \cdot cos(\omega t) \ \ \ \ \  + \ \ \ \ i \cdot (\tfrac{2}{i} \cdot \hat{s}(-\omega)) \cdot sin(\omega t) \\
         &= \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \  \frac{1}{N}\sum_{n = 0}^{N} \hat{s}(-\omega) \cdot sin(\omega t) \\
 \end{aligned}
}
$$

如果我们将 $$\hat{s}(-\omega)$$ 的负号划入公式，并将离散级数扩展到原信号函数 $$s(t)$$ 的连续实数空间上以积分形式表示。则 $$s(t)$$ 与 $$\hat{s}(-\omega)$$ 的关系就展现为：

$$
{\displaystyle 
 \begin{aligned}
   s(t)  &= \frac{1}{N}\int_{0}^{N} \hat{s}(\omega) \cdot sin(\omega t) \ d{n} \\
   \hat{s}(\omega)  &= \int_{0}^{T} s(t) \cdot sin(-\omega t) \ dt \\
 \end{aligned}
}
$$

这就是傅里叶变换的奇函数表达式，也被称为 **正弦傅里叶变换（SFT [Sine Fourier Transform]）**。

同理，如果我们取偶函数，有 $$a_{\omega}$$ 与 $$b_{\omega}$$ 表现为符号相同的纯实数。即：

$$
{\displaystyle 
 \begin{aligned}
   \hat{a}_{\omega}  &= 1 \cdot [\hat{s}(-\omega) + \hat{s}(\omega)] = 2 \cdot \hat{s}(\omega)   \ \ \ \ \ 
   \hat{b}_{\omega}  = \tfrac{1}{i} \cdot [\hat{s}(-\omega)-\hat{s}(\omega)] = 0 \\
   s(t)  &= \frac{1}{N} \sum_{\omega =0}^{\omega_N} \ \ \ \ {2 \cdot \hat{s}(\omega)} \cdot cos(\omega t) \ \ \ \ \  + \ \ \ \ i \cdot 0 \cdot sin(\omega t) \\
         &= \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \frac{1}{N}\sum_{n = 0}^{N} \hat{s}(\omega) \cdot cos(\omega t) \\
 \end{aligned}
}
$$

采用相同处理，有余 **弦傅里叶变换（CFT [Cosine Fourier Transform]）** 结果如下：

$$
{\displaystyle 
 \begin{aligned}
   s(t)  &= \frac{1}{N} \int_{0}^{N} \hat{s}(\omega) \cdot cos(\omega t) \ d{n} \\
   \hat{s}(\omega)  &= \int_{-\tfrac{T}{2}}^{+\tfrac{T}{2}} s(t) \cdot cos(-\omega t) \ dt \\
 \end{aligned}
}
$$

然而工程中的信号并不存在有限周期且并不都能判定奇偶性，这是否意味着我们无法对其进行分解和化简？

>答案是否定的。首先来看，针对周期性需要进行的操作。

## **解构一维信号 - 时频分离（Time-Frequency Separation）**

如果我们换个角度就会发现，不存在有限周期只不过是因为周期太长，以至函数周期等于信号完整时长或着趋近无穷而导致的。所以我们分解原函数到对应的复指数函数和，所选择基底复指数函数也趋近于无穷，并使其对应频率从 $$0$$ 到 $$\infty$$ 而周期从极大到极小即可。不过在计算上就需要利用傅立叶变化的空间特征了。

结合上文，记被分解的原信号函数为 $$f(t)$$ 。根据傅立叶基的正交特性，如果存在 $${\mathcal {F}}(t)$$ 为当前 $$f(t)$$ 的解函数空间，则必然有 $$f(t) \cdot {\mathcal {F}}_{\omega}^{-1}(t)$$ 内积在时间 $$t$$ 范围为 $$(0,\ \infty)$$ 有固定值 $$\hat{f}(\omega)$$ ，使得：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(\omega) &= \int_{0}^{\infty} f(t) \cdot {\mathcal {F}}_{\omega}^{-1}(t) \ dt  = \int_{0}^{\infty} f(t) \cdot e^{-i \omega t}\ dt \\
 \end{aligned}
}
$$

以函数空间角度排除 $$f(t)$$ 周期干扰。而复指数波的波函数，顾名思义就是复指数函数，有：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(\omega) &= \int_{-\infty}^{+\infty} a_{\omega} \cdot cos(\omega t) + i \cdot b_{\omega} \cdot sin(\omega t) \ dt\\
 \end{aligned}
}
$$

使 $$$ b_{\omega}$$ 可取复数域，就可以转换为：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(\omega) &= \int_{-\infty}^{+\infty} a_{\omega} \cdot cos(\omega t) + b_{\omega} \cdot sin(\omega t) \ dt\\
 \end{aligned}
}
$$

由于实际信号并不能严格确定奇偶性，不过对于小于四维的情况下，大多数条件都能保证其本身为实函数（即函数只有实数域取值），因而构成原信号的分离基底函数是存在不同强度和初项的。我们沿用前文中对初相和振幅的定义，记 $${\mathcal {F}}_{\omega}(t)$$ 初相为 $$\angle\phi_{\omega}$$ ，振幅为 $$A_{\omega}$$ ，则有：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega}(t) : \ \ \ \
   \angle\phi_{\omega} = \arctan(\tfrac{\hat{a}_{\omega}}{\hat{b}_{\omega}}) \ \ \ \ 
   A_{\omega} = \sqrt{ (\hat{a}_{\omega}) ^2 + (\hat{b}_{\omega}) ^2 } \\
 \end{aligned}
}
$$

根据 **帕西瓦尔定理（Parseval’s Theorem）** 转复数空间，我们会发现 $$A_{\omega}$$ 就是 $$\hat{f}(\omega)$$ 取 $$2$$ 范数后的结果，而初项其实就是 $$\hat{f}(\omega)$$ 在 $$t = 0$$ 时，自身相位在复数空间上与实轴的夹角。即：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega}(t) &: \\
   \angle\phi_{\omega} &= \angle{\vert \hat{f}(t) \vert} \ = \arctan(\tfrac{\hat{a}_{\omega}}{\hat{b}_{\omega}}) \\
   A_{\omega} &=\ \  \Vert \hat{f}(t) \Vert _2 =\sqrt{ (\hat{a}_{\omega}) ^2 + (\hat{b}_{\omega}) ^2 } \\
 \end{aligned}
}
$$

进而有：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega}(t) &= A_{\omega} \cdot sin(\omega t -\angle\phi_{\omega}) = A_{\omega} \cdot cos(\omega t +\angle\phi_{\omega}) \\
                              &= {\Vert \hat{f}(t) \Vert _2} \cdot sin(\omega t -\angle{\vert \hat{f}(t) \vert}) 
                               = {\Vert \hat{f}(t) \Vert _2} \cdot cos(\omega t +\angle{\vert \hat{f}(t) \vert}) \\
   \hat{f}(\omega) &= \int_{0}^{\infty} f(t) \cdot e^{-i \omega t}\ dt \ \ \ \ \ \Leftrightarrow \ \ \ \ \ 
   f(t) = \frac{1}{N} \int_{-\infty}^{+\infty} \hat{f}(\omega) \cdot {\mathcal {F}}_{\omega}(t) \ d \omega \\
 \end{aligned}
}
$$

显然，大部分信号都是有限时间下的，且基本都能满足无穷区间的狄利克雷条件，也因此可以使用傅里叶变换分解。

如果频率范围在 $$\omega \in [\omega_{0},\ \omega_{1}]$$ ，对于选定的时间点 $$t = t_c$$ ，有频率 $$\omega$$ 、原函数 $$f(t)$$ 在 $$t = t_c$$ 时的取值 $$f(t_c)$$ 、基底函数族 $${\mathcal {F}}_{\omega}(t)$$ 锁定时间 $$t = t_c$$ 的变体 $${\mathcal {F}}_{t_c}(\omega)$$ ，构成该频率范围的 **频域投影（FDP [Frequency Domain Projection]）**；

反之，如果时间范围在 $$t\in [\ t_0,\ \ t_1]$$ ，对于频率范围 $$\omega \in [\omega_{0},\ \omega_{1}]$$ ，有时间 $$t$$ 、原函数 $$f(t)$$ 、基底函数族 $${\mathcal {F}}_{\omega}(t) $$，就构成了原函数在该时间范围的 **时域投影（TDP [Time Domain Projection]）**。

两者的区别仅在于观察角度的不同：

$$
{\displaystyle 
 \begin{aligned}
   {Frequency\ Domain\ Projection:}  &\ \ (\ \ \omega\ ,\ \ f(t_c)\ ,\ \ {\mathcal {F}}_{t_c}(\omega) \ \ )  \\
   {Time\ Domain\ Projection:}       &\ \ (\ \ t\ \    ,\ \ f(t)\ \ ,\ \ {\mathcal {F}}_{\omega}(t) \ \ \ )  \\
   {\omega \in [\omega_0,\ \omega_n]}   \ \ \ \ & \ \  {\ t\ \in [\ t_0,\ \ t_n\ ]} \\
 \end{aligned}
}
$$

周期的问题解决了，现在我们能够拿到时频分离（Time-Frequency Separation）的原信号函数信息并可以依此还原信号本身。但积分对于计算机来说任务有些繁重。同时，由于计算机只能处理离散化后的数字信号，因此离散化的算法才能够被计算机有效使用。

>所以还需要在此基础上，找到更为便捷的算法实现。

## **精简运算过程 - 一维离散傅立叶变换（1D-DFT）**

如果将积分重新转换为级数形式积化和差表示，并在允许误差范围内取有限子集。那么就能够化解掉大部分运算量，从而得到一个相对理论而言的低时间复杂度算法。这种想法促成了基于计算机运算的一维离散傅立叶（1D-DFT）的诞生。

一维离散傅立叶（1D-DFT [1D-Discrete Fourier Transform]）本质上包含了两部分离散化作业，即对时域的离散化（TDD [Time Domain Discrete]）和对频域的离散化（FDD [Frequency Domain Discrete]）。

**时域离散化（TDD）** 方面，一维离散傅立叶采用了离散时间傅立叶变化（DTFT [Discrete Time Fourier Transform]）中，对时域信号间隔采样的操作。即将：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(\omega) &= \int_{0}^{\infty} f(t) \cdot e^{-i \omega t}\ dt \\
 \end{aligned}
}
$$

以时间采样（切片）数量为 $${n_1}$，转为级数形式：

$$
{\displaystyle 
 \begin{aligned}
   \hat{f}(\omega) &= \sum_{t = t_0}^{t_{n_1}} f(t) \cdot e^{-i \omega t} \\
 \end{aligned}
}
$$

打破时间上的连续性。需要注意的是，此时频域仍然是连续的。
	
**频域离散化（FDD）** 方面，离散傅立叶做的操作就更为直观了。如果在频率采样时就以离散化的方式采样数据，那得到的频域信息天然就是离散的。同样，从某个时刻 $$t = t_c$$ 离散化的频域信息上还原当前实际频率，则也是一个线性求和的过程。因此有：

$$
{\displaystyle 
 \begin{aligned}
   f(t) = \frac{1}{N}  \int_{-\infty}^{+\infty} \hat{f}(\omega) \cdot {\mathcal {F}}_{\omega}(t) \ d \omega  \\
 \end{aligned}
}
$$

以频率采样（切片）数量为 $${n_2}$，转为级数形式：

$$
{\displaystyle 
 \begin{aligned}
   f(t) = \frac{1}{n_2} \sum_{\omega = \omega_0}^{\omega_{n_2}} \hat{f}(\omega) \cdot {\mathcal {F}}_{\omega}(t)  \\
 \end{aligned}
}
$$

而随着有限采样，基底函数族 $${\mathcal {F}}_{\omega}(t) $$$ 构成的解函数空间也是有限维的，即：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega} = [{\mathcal {F}}_{\omega_1},{\mathcal {F}}_{\omega_2},\dots,{\mathcal {F}}_{\omega_{n_2}}] \\
 \end{aligned}
}
$$

至此，由时域离散化（TDD）与频域离散化（FDD）共同构成离散傅立叶（DFT）的完整表达如下所示：

$$
{\displaystyle 
 \begin{aligned}
   {\mathcal {F}}_{\omega} = [{\mathcal {F}}_{\omega_1},&{\mathcal {F}}_{\omega_2},\dots,{\mathcal {F}}_{\omega_{n_2}}]  \\
   \hat{f}(\omega) = \sum_{t = t_0}^{t_{n_1}} f(t) \cdot e^{-i \omega t}  \ \ \ \ \ &\Leftrightarrow \ \ \ \ \ 
   f(t) = \frac{1}{n_2} \sum_{\omega = \omega_0}^{\omega_{n_2}} \hat{f}(\omega) \cdot {\mathcal {F}}_{\omega}(t) \\
 \end{aligned}
}
$$

经过离散化后的有限采样更适合计算机有限的算力，因此才能被程序化。不过由于并没有保存连续的完整信息，经过离散傅里叶变换后再还原的数据，相对于采样自然源的原始数据终归还是会有一定损失的。但是由于变换与逆变换，并不会导致解构再还原后的数据存在差异。所以离散傅里叶变换被归类为 **有损采样（Lossy Sampling）的无损算法（Lossless Algorithm）** 。

## **一维离散傅立叶变换（1D-DFT）的 C 语言实现**

既然需要做程序化，那么首先需要将离散傅里叶变换的过程抽象化。理清逻辑思路的同时，方便构造迭代器和代码的处理流水线。这里我们使用伪码表示：

```C++
/**
 * 1D-DFT [Discrete Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[T] = {...};
 *     Fn[N] = {};
 *     dft_1d(&Fo, &Fn, T, N);
 * [theorem::definitions]
 *   Fo meanings Original Function
 *   Fn meanings Fourier Basis at [n]
 *   pi meanings π
 *   T  meanings Periodic of Fo
 *   N  meanings Slice of Frequency
 *   Wn meanings Angular Frequency of Basis Fn is Wn = ((2*pi*n)/T)
 * [theorem::formula]
 *   Fo[t] = sum_{n=0}^{N-1} x Fn[t] * exp(  i * ((2*pi*n)/T) * t), 0<=n<N
 *   Fn[t] = sum_{t=0}^{T-1} x Fo[t] * exp( -i * ((2*pi*n)/T) * t), 0<=t<T
 *         = sum_{t=0}^{T-1} x Fo[t] * (An * cos(Wn * t) + Bn * sin(Wn * t)), 0<=t<T
 *         = All_in_one(An) * cos(Wn * t) + All_in_one(Bn) * sin(Wn * t), 0<=t<T
 *   So:
 *     An = Re(Fn[t]);  Bn = Im(Fn[t])
 * [logistic]
 * {
 *   result = []; // as byte array
 *   // do TDD:
 *   for n in range(N) {
 *     An = 0; Bn = 0;
 *     // do FDD:
 *     for t in Range(T) {
 *       Wn = (2 * pi * n) / T;
 *       An = Re += Cos(Wn * t) * Fo(t);
 *       Bn = Im += Sin(Wn * t) * Fo(t);
 *     }
 *     result[n] = Fn.to_complex_angular_form(An, Bn)
 *   }
 *   return result;
 * }
 * @param Fo Original Function input array
 *           (already sampled by T as count-of-time-slice)
 * @param Fn Fourier Basis
 *           (already sampled by N as count-of-frequency-slice)
 * @param T  Periodic of Fo, Number of Time Slice
 * @param N  Number of Frequency Slice
 */
```

同时，我们还需要提供离散傅里叶变换的逆变换（IDFT [Inverse Discrete Fourier Transform]）来使得电脑能够还原信息：

```C++
/**
 * 1D-IDFT [Inverse Discrete Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[T] = {};
 *     Fn[N] = {...};
 *     dft_1d(&Fo, &Fn, T, N);
 * [theorem::definitions]
 *   Fo meanings Original Function
 *   Fn meanings Fourier Basis at [n]
 *   pi meanings π
 *   T  meanings Periodic of Fo
 *   N  meanings Slice of Frequency
 *   Wn meanings Angular Frequency of Basis Fn is Wn = ((2*pi*n)/T)
 * [theorem::formula]
 *   Fo[t] = sum_{n=0}^{N-1} x Fn[t], 0<=n<N
 *   Fn[t] = sum_{t=0}^{T-1} x Fo[t] * exp( -i * ((2*pi*n)/T) * t), 0<=t<T
 *         = sum_{t=0}^{T-1} x Fo[t] * (An * cos(Wn * t) + Bn * sin(Wn * t)), 0<=t<T
 *         = All_in_one(An) * cos(Wn * t) + All_in_one(Bn) * sin(Wn * t), 0<=t<T
 *   So:
 *     An = Re(Fn[t]);  Bn = Im(Fn[t])
 * [logistic]
 * {
 *   result = []; // as byte array
 *   // do TDD:
 *   for t in range(T) {
 *     Re = 0; Im = 0;
 *     // do FDD:
 *     for n in Range(N) {
 *       Wn = (2 * pi * n) / T;
 *       An = Re(Fn[n]);
 *       Bn = Im(Fn[n]);
 *       result[t] += Fn[n].to_value(Wn, An, Bn);
 *     }
 *   }
 *   return result;
 * }
 * @param Fo Original Function input array
 *           (already sampled by T as count-of-time-slice)
 * @param Fn Fourier Basis
 *           (already sampled by N as count-of-frequency-slice)
 * @param T  Periodic of Fo, Number of Time Slice
 * @param N  Number of Frequency Slice
 */
```

现在思路有了，只需要以代码实现即可：

```C++
#include "math.h"

#define PI 3.1415926f

typedef struct FBasis {
    double re_;
    double im_;
    double w_;
} FBasis;

void dft_1d(double *Fo, FBasis *Fn, size_t T, size_t N) {
    for (int n = 0; n < N; ++n) {
        double An = 0;
        double Bn = 0;
        double Wn = (2 * PI * n) / T;
        for (int t = 0; t < T; ++t) {
            An += cos(Wn * t) * Fo[t];
            Bn += sin(Wn * t) * Fo[t];
        }
        FBasis e_ = {An, Bn, Wn};
        Fn[n] = e_;
    }
}

void idft_1d(double *Fo, FBasis *Fn, size_t T, size_t N) {
    for (int t = 0; t < T; ++t) {
        for (int n = 0; n < N; ++n) {
            FBasis e_ = Fn[n];
            Fo[t] += (e_.re_ * cos(e_.w_ * t) + e_.im_ * sin(e_.w_ * t)) / N;
        }
    }
}
```

写完后简单测试一下：

```C++
int main(void) {
    FBasis Fn[6] = {};
    double Fo[6] = {1, 2, 3, 4, 5, 6};
    double iFo[6] = {};
    size_t T = sizeof(Fo) / sizeof(double);
    size_t N = sizeof(Fn) / sizeof(FBasis);
    printf("\n Original_data: \n");
    for (int t = 0; t < T; ++t) {
        printf("%f  ", Fo[t]);
    }

    printf("\n DFT_result: \n");
    dft_1d(Fo, Fn, T, N);
    for (int n = 0; n < N; ++n) {
        printf("%f + i %f \n", Fn[n].re_, Fn[n].im_);
    }

    printf("\n IDFT_result: \n");
    idft_1d(iFo, Fn, T, N);
    for (int t = 0; t < T; ++t) {
        printf("%f  ", iFo[t]);
    }

    return 0;
}
```

得到结果和标准几近相同：

```
 Original data: 
1.000000  2.000000  3.000000  4.000000  5.000000  6.000000  

 DFT_result: 
21.000000 + i 0.000000 
-3.000003 + i -5.196152 
-3.000002 + i -1.732048 
-3.000000 + i -0.000002 
-2.999996 + i 1.732057 
-2.999979 + i 5.196158 

 IDFT_result: 
1.000003  2.000000  2.999999  3.999999  4.999999  6.000000   
```

运行结束。

到这里，我们已经基本掌握了傅里叶变换原理和最基础的应用。

**如果拓展傅里叶变换到相对复杂的二维情况，那么和一维时有哪些不同呢？**


[ref]: References_1.md