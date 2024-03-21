
# 1.3.2 响度（Loudness）

**响度（Loudness）**，有时虽不准确但也会被称为 **音量（Volume）**，是指人对声音大小的 **主观感知量（Subjective Perceptions）**，是对声波的 **声压（Acoustic Pressure）** 物理量的感观描述。响度是根据人对不同声压反应，而人为测量出的一种 **非客观（Non-Objective）** 的量化值。

响度的早期单位是 **宋（Sone）**，这是一个 **主观标定的单位**。同 [音高](Docs_1_3_1.md) 一样，来自于 **史丹利·史密斯·史蒂文斯（S. S. Stevens）** 于 1963 年的实验结果 [\[4\]][ref] 。

由于主观成分因素，宋 同样不属于当前 **国际通用的计量体系单位（SI Unit [International System of Units]）**，而且因相对粗粒度而不太经常被采用。工程通用对响度进行衡量的单位，是声压级。

## **声压级（SPL [Sound Pressure Level]）**

**声压级（SPL [Sound Pressure Level]）** 是由 **美国国家标准学会（ANSI [American National Standards Institute]）** 测定，同样为 **主观标定的** 响度单位。但由于相对精确的度量水平，在通常非实验误差情况下，可以作为稳定的工程单位使用。声压级单位为 **分贝（dB）**，常用 $$N$$ 表示代指。

我们有当前最新一次实验室精确测量的 **ANSI/ASA S1.1-2013** 规格为基准 [\[7\]][ref] 。修正锚定 **以 1000Hz 纯音，在人耳能听见的最小阈限压强 $$p_{ref} = 20 \mu Pa$$ 为 $$1 \ dB$$ 值**，由此推导得声压级公式：

$$
{\displaystyle 
 \begin{aligned}
   N &= 20 \cdot \log_{10} \left( \frac{p}{p_{ref}} \right)  \\
 \end{aligned}
}
$$

其中，

- 以 $$p$$ 代表当前目标声音，对应声波的  **[声压（Acoustic Pressure）](Docs_1_2.md)**；
- 以 $$p_{ref}$$ 代表 **参考声压（Reference Acoustic Pressure）**，为规格固定量， $$p_{ref} = 20 \mu Pa$$ ；

而在 ANSI 的声压级单位系统下，记宋体系响度为 $$L_N$$ ，则分贝（dB）与 宋（Sone）存在换算关系：

$$
{\displaystyle 
 \begin{aligned}
   L_N &= 2^{\tfrac{N - 40}{10}}  \\
 \end{aligned}
}
$$

即：

$$
{\displaystyle 
 \begin{aligned}
   N &= 40 + \log_2 \left( L_N \right) \\
 \end{aligned}
}
$$

除 **宋（Sone）** 以外，另一个常见的体系是 **方（Phon）**。在该修订里，规定：

$$
{\displaystyle 
 \begin{aligned}
   40 \ dB = 40 \ Phon = 1 \ Sone \\
 \end{aligned}
}
$$

**一般情况下，宋（Sone）和方（Phon）用于常量标记，而 SPL分贝（dB）用于响度值。**

<br>

但是，从前文我们得知，自然界中的大部分声音，其本身就是复合的。这种情况下怎么评估它的响度呢？

此时，就需要使用 **复合频率下** 的声音计算公式了。

## **复合响度公式（Multi-Source Loudness Formula）**

假设一个 **单一的自然声（Natural Sound）**，记为 $$N_{\sum}$$ 由一组声压为 $$p = [p_0,\ p_1,\ \cdots \ ,\ p_n]$$ 的单频率声波组成，有：

$$
{\displaystyle 
 \begin{aligned}
   N_{\sum} &= 10 \cdot \log_{10} \left( \frac{ {p_0}^2 + {p_1}^2 + \cdots +{p_n}^2 }{ {p_{ref}}^2 } \right)  \\
     &= 10 \cdot \log_{10} \left( \sum^n \left( \frac{p_i}{ p_{ref}} \right)^2 \right)  \\
 \end{aligned}
}
$$

而工程中的单频率声波代表参数，可能直接为响度，如 $$L = [L_0,\ L_1,\ \cdots \ ,\ L_n]$$ 。则带入单频率响度公式，上式可写为：

$$
{\displaystyle 
 \begin{aligned}
   N_{\sum} &= 10 \cdot \log_{10} \left( \sum^n \left( \frac{p_i}{ p_{ref}} \right)^2 \right) = 10 \cdot \log_{10} \left( \sum^n 10^{\frac{L_i}{10\ dB}} \right)  \\
     &= 10 \cdot \log_{10} \left( 10^{\frac{L_0}{10\ dB}} + 10^{\frac{L_1}{10\ dB}} + \cdots + 10^{\frac{L_n}{10\ dB}}  \right)  \\
 \end{aligned}
}
$$

这就是 **声音（复合声波）的响度公式**。

可虽然 **分贝（dB）系统最为广泛且常常被使用**，但却 **仍然不属于** 国际通用的计量体系单位（SI Unit）。 **真正被作为科学的单位，是声强（Sound Intensity）。**

## **声强（Sound Intensity）**

**声强（Sound Intensity）** 是对单个声波强度的科学表示，指声波在单位面积下所具有的声压（Acoustic Pressure），对外功率之和。

声强单位为 瓦每平方（ $$W/m^2$$ ），一般被记为 $$I$$ 表示。有：

$$
{\displaystyle 
 \begin{aligned}
   I &= p \cdot \vec{v} \\
 \end{aligned}
}
$$

其中，
- 以 $$p$$ 代表当前目标声音，对应声波的 **声压（Acoustic Pressure）** ；
- 以 $$\vec{v}$$ 代表机械波的做功方向，是个 **速度量**，**每个维度分量单位都为 米每秒（m/s）** ；

由于一般我们用声强来计算，理想状态的当前声波能量值。为了简化计算，通常会选择均匀介质情况的理想单点声源，作为背景条件。这种情况下，做工方向 $$\vec{v}$$ 就可以被认为是 **球面坐标中，单位平方点的向外法向量了**。

于是，声强 $$I$$ 即可转为，由声压 $$p$$ ，传播介质密度 $$\rho$$ ，和声速 $$c$$ ，计算表示：

$$
{\displaystyle 
 \begin{aligned}
   I &= \frac{p^2} {\rho c} \\
 \end{aligned}
}
$$

因为一般都是在空气介质中进行衡量，所以有 $$\rho \approx 1.293 \ kg/m^3$$ ，而 $$c \approx 343 \ m/s$$ 。 所以，根据声压快速获取对应声音在空气中的声强公式为：

$$
{\displaystyle 
 \begin{aligned}
   I &\approx \frac{p^2} {443.499} \ W/m^2\\
 \end{aligned}
}
$$

使用上式速算时，压强取 帕斯卡（Pa）数量级下的数值即可。

那么，声强和响度是什么关系呢？
很遗憾，两者分属不同系统，并不存在 **直接上的** 关联。但存在 **间接换算** 关系。

## **声强级（SIL）与 声压级（SPL）的换算**

**声强级（SIL [Sound Intensity Level]）** 类似于 **声压级（SPL [Sound Pressure Level]）** 的定义，皆是用来 **主观标定** 响度的单位系统/系统单位。SIL 的单位沿用了 SPL 的 分贝（dB），甚至两者换算公式，都可基本等同。所以，仍然以 $$N$$ 表示声音响度，有：

$$
{\displaystyle 
 \begin{aligned}
   \frac{I}{ I_{ref} } = \frac{p^2}{ {p_{ref}}^2 } &= \left( \frac{p}{ p_{ref} } \right)^2 \\
   N = 20 \cdot \log_{10} \left( \frac{p}{ p_{ref} } \right) &= 10 \cdot \log_{10} \left( \frac{I}{ I_{ref} } \right) \\
 \end{aligned}
}
$$

以 $$N_{\sum}$$ 表复合，取声压 $$p = [p_0,\ p_1,\ \cdots \ ,\ p_n]$$ ，声强 $$I = [I_0,\ I_1,\ \cdots \ ,\ I_n]$$ ，则复合响度公式有：

$$
{\displaystyle 
 \begin{aligned}
   N_{\sum} &= 10 \cdot \log_{10} \left( \sum^n \left( \frac{p_i}{ p_{ref} } \right)^2 \right) = 10 \cdot \log_{10} \left( \sum^n \left( \frac{I_i}{I_{ref}} \right) \right)  \\
     &= 10 \cdot \log_{10} \left( 10^{\frac{L_0}{10\ dB}} + 10^{\frac{L_1}{10\ dB}} + \cdots + 10^{\frac{L_n}{10\ dB}}  \right)  \\
 \end{aligned}
}
$$

至此，两个主客观系统间，达成了转换条件。一般的 $$p_{ref} = 20 \mu Pa$$ 时，有 $$I_{ref} = 1 \ pW/m^2$$ 。**我们用声压级表示响度，而以声强计算能量。**


[ref]: References_1.md