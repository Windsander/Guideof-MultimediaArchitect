
# 1.5.4 脉冲编码调制（PCM）& 脉冲密度调制（PDM）

实际上，为了避免理解中的混淆，我们在上文中介绍的 模数转换（A/D）和 数模转换（D/A）方式，都是基于 **脉冲编码调制（PCM [Pulse-Code Modulation]）** 进行的。能够完成数模模数转换的方法，除了 PCM 法外，还有 **脉冲密度调制（PDM [Pulse-Density Modulation]）**，以及一系列不同出发点的调制模式，比如 **脉冲带宽调制（PDM [Pulse-Width Modulation]）** 等。由于在本领域内相对非主流，或是已经属于相对落后技术，亦不再讨论。

本节主要以相对具有代表性的 PCM 与 PDM 进行比对。

**脉冲编码调制（PCM [Pulse-Code Modulation]）** 是通过将模拟信号的 **电压幅度**，以 **离散数字码** 的形式等效表示，从而转换为数字信号。其在转换前后 **时序（周期）上是一致的**。转换后的数字信号，**幅度变化拟合原有模拟信号幅度变化轮廓**。

**脉冲密度调制（PDM [Pulse-Density Modulation]）** 则是将模拟信号的 **电压幅度**，以 **一段时间内的高密度脉冲数量** 来表示，从而转换为数字脉冲。其在 **时序（周期）上是差异的**，转换后的数字信号，**幅度二元变化（只有 0/1 值）**。

主要的不同，来自于对模拟信号 **幅度抽象模式**。

## **PCM & PDM 异同辨析**

基于 **PCM** 的 A/D、D/A 过程，**数字信号是二维信号**，时序信息与幅度信息依旧保持为两个维度。而基于 **PDM** 的 A/D、D/A 过程，**数字信号是一维信号**，原模拟信号的时序信息和幅度信息，被叠加到同一维度上，以采样频率对应周期长度进行了转后数字信号单一维度上的分片。

相应的，对于 PCM 法所得结果幅度切割程度的重要指标，**采样位深（Sampling Bit Depth）**，则 **不存在于 PDM 法中**。

PDM 采用 **过采样系数（Oversampling Ratio）** 配合 **数字信号采样率（Digital Sampling Rate）** 的方式，来表示 **采样分辨率（Sampling Resolution）**。即 PDM 和 PCM 的采样率，在意义上是不一样的：

- **PCM 采样率**，代表在一个时钟信号周期内，设备对模拟信号采样的次数；
- **PDM 采样率**，代表在一个时钟信号周期内，设备对模拟信号一次采样的幅度累计上限；

因此，PDM 设备在一个时钟信号周期内，仅仅数字化模拟信号 **一个时刻**。PCM 设备在一个时钟信号周期内，则数字化模拟信号 **多个时刻**。

需要注意的是，**PDM 采样率（Samplerate）** 决定了 PDM 设备的 **可采样幅度范围**，但这 **并不** 意味着可以等价于设备的时钟频率，这是两个概念。仍然记该 PDM 设备 **参考输入（Reference Input）** 大小为 $$V_{Ref}$$ ，**数字信号采样率（Digital Sampling Rate）** 为 $$F_{ADC}$$ ，**过采样系数（Oversampling Ratio）** 为 $$S_{r}$$ ，而 **采样率（Digital Sampling Rate）** 为 $$F$$ 。则顺序 $$i$$ 的 **二元数字信号（0-1 Digital Signal）** 值 $$D_i$$ 与几个量间的关系有：

$$
{\displaystyle 
 \begin{aligned}
   \sum_{i=0}^{S_r \cdot F} D_i 
   &= \begin{cases}
     1 &, \ \frac{V_{Ano}}{V_{Ref}} > 0 \\
     0 &, \ \frac{V_{Ano}}{V_{Ref}} = 0
   \end{cases} \\
 \end{aligned}
}
$$

一个时钟信号周期内 $$D_i = 1$$ 累积个数，就是 PDM 数字信号的 **脉冲密度（Pulse Density）**。我们记脉冲密度为 $$I_p$$ ，原模拟信号被采样时间点为 $$t$$ 则：

$$
{\displaystyle 
 \begin{aligned}
   I_p = \left( \sum D_i \cdot (S_r \cdot F) \right)_{t} \\
 \end{aligned}
}
$$

所以，对 PDM 设备来说，$$I_p$$ 才代表了原模拟信号在 $$t$$ 时的 **等效振幅（即电压）**，有：

$$
{\displaystyle 
 \begin{aligned}
   V_{Ano}(t) = I_p(t) \Leftrightarrow \sum_{i =C \cdot t}^{C \cdot t \ +\ S_r \cdot F} D_i \\
 \end{aligned}
}
$$

其中，**时钟频率（Clock Frequency）** 记为 $$C$$ 。

所以，PDM 是完全不同于 PCM 的方法论。

**而不论是 PCM 还是 PDM，其理想情况下都可以保持转换还原前后，原模拟信号不发生改变。** 对于 **PDM** 来说，最显著的特点就是在同等情况下，能够提供 **比 PCM 更细腻的分辨率**，但缺点也很明显，即 **更窄的动态范围**（时钟周期性和等效较低的对原模拟信号的采样频率）。

此外，PDM 受分时分区的采样频率，和通过电压控制的开关门电路累计计数关系，而易受外界和设备自身影响，导致容易引入内外噪音干扰。不过由于只需要按频率对应的一个周期内，累计幅度时发送单一信号（$$1 \cdot V_{Ref}$$），无幅度累计发送单一信号（$$0 \cdot V_{Ref}$$）的方式，转换数字信息。而使 PDM 的构造显然要简单于 PCM 方式的 ADC、DAC，这让用 PDM 方式构造的该类设备，具有较低能耗和低造价（制造简单）的优势。

由于这些原因，PDM 设备常被用在一些低电力和相对精度较低的需求场景，如电器控制单元、LED灯驱动器、一些微型麦克风设备等，相对更靠近使用端的设备。
相比之下，PCM 的处理方式，显然更容易相对完整的保存原有模拟信号信息。

<br>

**音视频工程场景中，我们常处理的音频信号，基本为 PCM 方式获取的数字信号。** 对于想要进行调整的 PDM 数字信号，通常需要转换为 PCM 数字信号后，再行以 PCM 更具优势的直接编辑方式，进行相关操作。而位于计算机体系内用来实现音频存储的数字信号基础类型，亦为 PCM 类型的数字信号。

由此可见 PCM 数字信号的重要性。


[ref]: References_1.md