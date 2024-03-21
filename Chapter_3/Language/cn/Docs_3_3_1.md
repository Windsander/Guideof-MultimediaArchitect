
# 3.3.1 方向梯度直方图（HOG [Histogram of Oriented Gradient]）

在前文中，我们提到了索贝尔滤波（Sobel Filter）卷积核对中心点周边方向信息的提炼，可以被用来获取方向梯度直方图的梯度矢量计算中。那么什么是方向梯度直方图呢？

方向梯度直方图最早的 **概念原型（Prototype）** 来自于 **罗伯特·麦康纳尔（Robert K. McConnell）** 在 1986 年申请的有关模式识别专利中，对 **视野（FoV [Field of View]）** 方向性输入产生输出结果差异的判断过程。并于 1994 年 **三菱电子研究实验室（Mitsubishi Electric Research Laboratories）** 在手势识别应用的区域检测过程中，首次总结为当前称谓 [\[16\]][ref] 。**最终经过 2005 年 CVPR 顶会参会论文验证，重新确认了 HOG 在动态检测上的高适配度，才开始被人熟知** [\[17\]][ref] 。

**方向梯度直方图（HOG [Histogram of Oriented Gradient]）** 是对用于提炼并描述区域范围内像素漂移情况方法论的概念抽象。是对过程的抽象，而非对结果的抽象。由于本身最终运算能够表示为处理单元形式，因而属于 **特征描述算子（Feature Descriptor）** 的一种。整体思想则是在单元间隔均匀的卷积核内，使用重叠的局部梯度提炼算法并 **录表统计归一化（Normalization）**，以取得中心点变化方向矢量。方法常结合 **阈值限定（Thresholding）** 筛选结果，提高运动预测的准确度。

显然，方向梯度直方图并不只适用于索贝尔， **只要能够提供中心点周边梯度变化的大小和方向的算子，都可以被应用于 HOG 的求解中**。一个方向梯度直方图是否优秀，最大的影响点就在于梯度提炼的是否精准。

## **HOG 的标准处理流**

HOG 有一套相对固定的标准过程的。基本可以按照如下顺序进行：

1. 数据优化，通过滤波算法（如高斯滤波），减少干扰信息并增强灰度（光亮度）对比；
2. 梯度计算，通过梯度滤波器（如索贝尔滤波）提取图像每个像素的梯度矢量；
3. 分组抽象，指定梯度矢量采样卷积核范围，即分组（Cell）
4. 矢量合并，将分组内所有像素的梯度矢量，以方向投票统计合并权重，获取 HOG
5. 块归一化，指定块大小（由分组为单位），整合 HOG 统计结果并归一化快内分组权重

五个步骤，共同构成了方向梯度直方图方法论本身。 **且四五两步概念不同，但密不可分。**

## **数据优化**

数据优化的目的是为了增强光亮度变化差异，并减少干扰噪声，从而更好的保存并放大像素梯度变化情况。我们记原信号为 $$S(x)$$ ，记经过滤波降噪和修饰后的灰度（光亮度）数据为 $$S_g(x)$$ 。从 $$S(x)$$ 到 $$S_g(x)$$ 的处理过程就不再赘述（见滤波，类比处理）。记经过优化函数 $$O_g(x)$$ 处理，以 $$S_g(x)$$ 获取的优化结果为 $$S_o(x)$$ 。那么，相对简单的处理方式，就是直接对 $$S_g(x)$$ 进行 伽马矫正（Gamma Correction）来得到 $$S_o(x)$$ 。取伽马因子为 $$\gamma$$ ，矫正系数（Adjust Factor）为 $$A$$ （一般情况 $$A = 1.0$$ 为常量），有：

$$
{\displaystyle 
 \begin{aligned}
    O_g(x) =& Gamma(S) = A \cdot S(x)^{\gamma} \\
 \end{aligned}
}
$$

**伽马矫正（Gamma Correction）** 本是用于应对，早期 **阴极射线管（CRT [Cathode Ray Tube]）显示器** 的电子偏转特征，引入的采样源数据非线性转换算法。传统的 CRT 显示器在显示时就会完成对偏转数据的自然逆向过程，而在 **液晶显示器（LCD [Liquid Crystal Display]）** 上，则需要 **主动的实现这一反向运算**，否则会面临数据亮度过爆的问题。

由于采样时采用 $$\gamma < 1$$ 应用于数据修正, 所以 $$\gamma < 1$$ 时的 $$\gamma$$ 值被称为 **编码伽马值（Encoding Gamma）**。相应的，$$\gamma > 1$$ 时的 $$\gamma$$ 值被称为 **解码伽马值（Decoding Gamma）**。而采样到还原的过程中，对伽马矫正的不同运用被分别称为 **伽马编码（Gamma Encode）** 和 **伽马解码（Gamma Decode）**。

<center>
<figure>
   <img  
      width = "500" height = "200"
      src="../../Pictures/gamma_correction_flow_02.png" alt="">
    <figcaption>
      <p>图 3.3.1-1 原数据经过伽马编解码（伽马矫正）的还原过程示意图</p>
   </figcaption>
</figure>
</center>

	
伽马矫正本身的作用正是针对原图色彩通道数据，进行非线性的映射。衍生为对图片整体光亮度的调节，因此在灰度值上的体现最为明显。我们利用这种特性，来增强图片的对比信息，放大像素梯度变化。

这一步，通常取用 $$\gamma \in [0.45,\ 1.25]$$ 区间内的值，或 $$\gamma = 0.5$$ 的原论文推荐值来进行修正。得到用于后续处理的灰度数据源 $$S_o(x)$$ 。

## **梯度计算**

在经过优化得到高对比度的 **灰度（光亮度）图** 后，就可以利用一些方向梯度卷积核算法，来计算每一个像素点光亮度变换的梯度矢量了。

此时应用边缘检测索贝尔滤波，目的同 HOG 的默认设定中，采用横纵方向均取 **单一中线** 的简化 **普雷维特算子（Prewitt Operator）**，以求取梯度 **方向（Orientate）** 和 **强度（Magnitude）** 的作用一致。显然，并不只有索贝尔算法或普雷维特算法，适用于方向梯度直方图中梯度矢量的计算。**只要能够提供中心点周边梯度变化的大小和方向的算子，都可以被应用于 HOG 的此步的求解计算中。**

我们记方向为 $$\Theta$$ ，强度为 $$A$$ ，横向 $$x$$ 轴方向的滤波核函数 $$G_x$$ ，纵向 $$y$$ 轴方向的滤波核函数 $$G_y$$ 。强度系数 $$K$$ 为同态值 $$K= K_x = K_y$$$ 。此处不含推导展示结论。

记 **边缘检测普雷维特滤波核函数** 为 $$\mathcal{P}_p(\vec{x_c})$$ ，有：

$$
{\displaystyle 
 \begin{aligned}
    G_x =& K_x \cdot 
    {
      \begin{bmatrix} 
        +1 ,&  \quad 0   ,&  \quad -1
      \end{bmatrix}
    } \ \cdot S_o(\vec{x_c})^{3 \times 1} \\
    G_y =& K_y \cdot 
    {
      \begin{bmatrix} 
        +1 ,&  \quad 0   ,&  \quad -1
      \end{bmatrix} ^{T}
    } \cdot S_o(\vec{x_c})^{1 \times 3} \\
    A =& \vert {\mathcal{P}_p(\vec{x_c})} \vert = K \cdot \sqrt{ {G_x}^{2} + {G_y}^{2} } \\
    \Theta =& \angle \mathcal{P}_p(\vec{x_c})\ = {atan2}(G_y,\ G_x)\\
 \end{aligned}
}
$$

记 **边缘检测索贝尔滤波核函数** 为 $$\mathcal{S}_p(\vec{x_c})$$ ，有：

$$
{\displaystyle 
 \begin{aligned}
    G_x =& K_x \cdot 
    {
      \begin{bmatrix} 
        +1 ,&  \quad \ \ 0   ,&  \quad \ \ -1      \\
        +2 ,&  \quad \ \ 0   ,&  \quad \ \ -2      \\
        +1 ,&  \quad \ \ 0   ,&  \quad \ \ -1
      \end{bmatrix}
    } \cdot S_o(\vec{x_c})^{3 \times 3} \\
    G_y =& K_y \cdot 
    {
      \begin{bmatrix} 
        +1 ,&  \quad \  +2   ,&  \quad \     +1      \\
         0 ,&  \quad \ \ 0   ,&  \quad \quad  0      \\
        -1 ,&  \quad \  -2   ,&  \quad \     -1
      \end{bmatrix}
    } \cdot S_o(\vec{x_c})^{3 \times 3} \\
    A =& \vert {\mathcal{S}_p(\vec{x_c})} \vert = K \cdot \sqrt{ {G_x}^{2} + {G_y}^{2} } \\
    \Theta =& \angle \mathcal{S}_p(\vec{x_c})\ = {atan2}(G_y,\ G_x)\\
 \end{aligned}
}
$$

更明确的，当我们采用不同算法进行梯度计算时，梯度提炼的结果，将会在较大程度上影响最终得到的方向梯度直方图。是需要更准确、更快捷，还是需要高抗性、低波动，应以实际工程角度考量。根据具体需要来采用不同的边缘检测算法。

**而梯度方向和强度的计算则可统一为共识：**

$$
{\displaystyle 
 \begin{aligned}
    A =& K \cdot \sqrt{ {G_x}^{2} + {G_y}^{2} } \\
    \Theta =& \angle \ [{tan^{-1}}(\tfrac{G_y}{G_x})] \\
 \end{aligned}
}
$$

称为 **通用卷积核梯度矢量公式（Formula of Kernel Gradient Vector）**。

经过此步计算后，灰度数据源 $$S_o(x)$$ 的输入就被转换为原信号为 $$S(x)$$ 的所有像素点，梯度方向数据集 $$\Theta(x)$$ 和 梯度强度数据集 $$A(x)$$ 。不过此时的数据量相对较大，不便于计算处理，还需 **简化信息量**。

## **分组抽象 & 矢量合并**

**分组抽象的目的是为了提炼每个像素点的数据，汇总分组内逐个像素特征到分组整体的单元特征。** 由于原有梯度方向的平面完整性，以 $$\Theta$$ 范围即便只限定为整数角，也包含 $$[0^{\circ},\ 360^{\circ})$$ 共 $$360$$ 个取值。 **这样造成的数据膨胀，不利于有限算力的处理。** 因此，以尽可能不损失方向包含实际意义为前提， **将角度按照权重分割** 来表示原梯度包含信息，是个不错的办法。

假设我们将 $$[0^{\circ},\ 360^{\circ})$$ 按照 $$\angle \Theta = [\Theta_0\ ,\ ...\ ,\ \Theta_{\theta-1}]$$ 的边界角度，拆分为 $$\theta$$ 个指定方向。记存在像素点 $$\vec{x_c}$$ 的梯度 $$\vec{G}(\vec{x_c}) = (A_c,\ \Theta_c)$$ 的方向落于角度区间 $$[\Theta_a,\ \Theta_b)$$ 内，有：

$$
{\displaystyle 
 \begin{aligned}
    A_c = W_a & \cdot A_a + W_b \cdot A_b \\
    \Theta_c = W_a & \cdot \Theta_a + W_b \cdot \Theta_b \\
    W_a = \frac{\Theta_c - \Theta_a}{\Theta_b - \Theta_a} & \quad \quad W_b = \frac{\Theta_b - \Theta_c}{\Theta_b - \Theta_a} \\
 \end{aligned}
}
$$

其中 $$W_a + W_b = 1$$ ，按照权重 $$W_a$$ 、 $$W_b$$ 即可拆分 $$\vec{G}(\vec{x_c})$$ 数据到 $$\Theta_a$$ 、 $$\Theta_b$$ 角度分量混合表示。记两个角度方向的分量分别为 $$\vec{G_a}$$ 、 $$\vec{G_b}$$ ，则：

$$
{\displaystyle 
 \begin{aligned}
    \vec{G_a} =& (W_a \cdot A_c ,\ W_a \cdot \Theta_c) \\
    \vec{G_b} =& (W_b \cdot A_c ,\ W_a \cdot \Theta_c) \\
    \vec{G}(\vec{x_c}) &= \vec{G_a} + \vec{G_b} \\
 \end{aligned}
}
$$

显然，以 $$\angle \Theta = [\Theta_0\ ,\ ...\ ,\ \Theta_{\theta-1}]$$  **指定方向的矢量合形式表示**， $$\vec{G}(\vec{x_c})$$ 除了 $$\Theta_a$$  、 $$\Theta_b$$ 角度外，**其余角度分量为 $$0$$ ，** 有：

$$
{\displaystyle 
 \begin{aligned}
    \vec{G}(\vec{x_c}) &= \angle \Theta(0, \ ...\ , W_a, W_b,\ ...\ ,0) \\
 \end{aligned}
}
$$

由于不需要考虑反向的数据还原，核内采样按照 $$\angle \Theta = [\Theta_0\ ,\ ...\ ,\ \Theta_{\theta-1}]$$ 的边界角度的方向矢量合形式求和，即可完成分组内的特征整合。记得到分组的 $$\theta$$ 维特征向量 $$\vec{Cell}$$ ，则：

$$
{\displaystyle 
 \begin{aligned}
    \vec{Cell} &= \sum  \angle \vec{G}(\vec{x_c})  \\
 \end{aligned}
}
$$

**那么现在的问题就是如何分组，或者分为几组了。**

当采样核为 $$n \times n$$ 时，我们取边界整数点出发过核心 $$(\tfrac {1}{2}n,\ \tfrac {1}{2}n)$$ 的连线，加上对角线一起作为分组分割线。 **由任意两条相邻分割线间的夹角，构成以核心为原点的角度分组。** 所以， $$\angle \Theta = [\Theta_0\ ,\ ...\ ,\ \Theta_{\theta-1}]$$ 代表的正是分割线角度。因此，当不区分夹角及其对角方向时，中心角能够分为 $$\theta = n + 1$$ 组，称为 **无符号梯度（Unsigned Gradient）** 分组。当考虑夹角与对角方向互反时，中心角能够分为 $$\theta = 2(n+1)$$ 组，称为 **有符号梯度（Signed Gradient）** 分组。

采样核一般为 $$n \times n = 8 \times 8$$ 大小，此时无符号梯度以方向标记，可分为 $$9$$ 组即:

$$
{\displaystyle 
 \begin{aligned}
    \angle \Theta =& [0^{\circ},\ 20^{\circ},\ 40^{\circ},\ 60^{\circ},\ 80^{\circ},\ 100^{\circ},\ 120^{\circ},\ 140^{\circ},\ 160^{\circ}]  \\
 \end{aligned}
}
$$

<center>
<figure>
   <img  
      width = "300" height = "300"
      src="../../Pictures/3_3_1-1.png" alt="">
</figure>
</center>


而有符号梯度则可分为 $$18$$ 组：

$$
{\displaystyle 
 \begin{aligned}
    \angle \Theta = 
    \begin{bmatrix} 
        &\angle \Theta_{lt}  \\
        &\angle \Theta_{rb}
    \end{bmatrix} =
    \begin{bmatrix} 
          0^{\circ},&  20^{\circ},&  40^{\circ},&  60^{\circ},&  80^{\circ},& 100^{\circ},& 120^{\circ},& 140^{\circ},& 160^{\circ}  \\
        180^{\circ},& 200^{\circ},& 220^{\circ},& 240^{\circ},& 260^{\circ},& 280^{\circ},& 300^{\circ},& 320^{\circ},& 340^{\circ}
    \end{bmatrix}
 \end{aligned}
}
$$

<center>
<figure>
   <img  
      width = "300" height = "300"
      src="../../Pictures/3_3_1-2.png" alt="">
</figure>
</center>


以无符号梯度的 $$9$$ 组分组为例，统计只需累计入组即可：

<center>
<figure>
   <img  
      width = "420" height = "300"
      src="../../Pictures/hog-histogram-1.png" alt="">
    <figcaption>
      <p>图 3.3.1-2 核大小  的无符号梯度（Unsigned Gradient）分组示意图</p>
   </figcaption>
</figure>
</center>

**随后依次统计分组的采样核内数据**。上图数据统计结果如下（概略图）：

<center>
<figure>
   <img  
      width = "420" height = "300"
      src="../../Pictures/histogram-8x8-cell.png" alt="">
    <figcaption>
      <p>图 3.3.1-3 无符号梯度分组的单组采样核内统计结果示意直方图</p>
   </figcaption>
</figure>
</center>

统计完毕时，特征向量 $$\vec{Cell}$$ 随即生成完毕。我们以 $$W_{\theta}$$ 表示分组的特征向量，在方向 $$\theta$$ 上的强度大小（即此方向矢量的秩），则对于无符号梯度（Unsigned Gradient）分组：

$$
{\displaystyle 
 \begin{aligned}
    \vec{Cell} &= \sum  \angle \vec{G}(\vec{x_c}) = \vec{\Theta}(W_{0^{\circ}}, \ ...\ , W_{160^{\circ}}) \in \mathbb{R}^{9 \times 1} \\
 \end{aligned}
}
$$

同样，对有符号梯度（Signed Gradient）分组：

$$
{\displaystyle 
 \begin{aligned}
    \vec{Cell} &= \sum  \angle \vec{G}(\vec{x_c}) = \vec{\Theta}(W_{0^{\circ}}, \ ...\ , W_{160^{\circ}}, \ ...\ , W_{340^{\circ}}) \in \mathbb{R}^{18 \times 1} \\
 \end{aligned}
}
$$

至此，完成分组提炼。

**这种对数据梯度的蒸馏手段非常重要，因为它不只可以运用于物体识别等情况的中间步骤，也可以被运用于粗糙的运动特征检测。**

而从分组的数据得来的分组特征，还需要归一化才能被有效使用。

## **块归一化**

由于分组内梯度矢量的分解叠加有可能会使某个方向上的梯度强度 **远超其他方向**，因而造成该方向上的灰度（光亮度）变化会极大的影响结果。 **这样的影响当然是有利的，但无法相对统一的权重，也会给处理带来大量的不确定性。** 如图例：

<center>
<figure>
   <img  
      width = "400" height = "700"
      src="../../Pictures/hog-example-1.png" alt="">
    <figcaption>
      <p>图 3.3.1-4 块归一化说明图例（数据源）</p>
   </figcaption>
</figure>
</center>

**取绿色框中以 $$n \times n = 8 \times 8$$ 采样核，经过前几步以无符号梯度（Unsigned Gradient）方式处理，会得到的四个分组：**

<center>
<figure>
   <img  
      width = "500" height = "490"
      src="../../Pictures/hog-example-2.png" alt="">
    <figcaption>
      <p>图 3.3.1-5 图例（数据源）绿色框中四个分组特征向量直方图表示</p>
   </figcaption>
</figure>
</center>

**如果能够将这种变化趋势原封不动的保存下来，并缩小尺度到统一标准，就可以实现即保证特征不被不必要的削减，也有足够一致的度量衡。** 因此，归一化就是解决办法。

**归一化（Normalization）** 是将目标数据集，按照总体权重等比放缩到指定区间范围的一种数学工具。通常我们选取当前采样分组包含的数据，即为归一化的目标数据集。组与组间独立归一化。但 **块归一化（Block Normalization）** 和一般情况下不完全一样，是以 **块（Block）** 为样本源而非 **组（Cell）** 样本源本身，来进行归一化处理的。

**什么是块（Block）呢？**

**块（Block）是对于由一系列分组（Cell）按照一定规则（例如四叉树、标准单元等）组合构成的分组并集单元的称谓。** 是组的集合。对块的分法有各种形式，但在方向梯度直方图中，使用的是一种直接切入的固定设置。记块大小为 $$N \times N$$ ，块的最小单位为组，则取 $$N \times N = 2 \times 2$$ 的固定大小组采样，构成 HOG 的分块。即图例中的绿色方块：

<center>
<figure>
   <img  
      width = "100" height = "100"
      src="../../Pictures/hog-example-4.png" alt="">
    <figcaption>
      <p>图 3.3.1-6 图例（数据源）块划分单一块示意图</p>
   </figcaption>
</figure>
</center>

同分组一样，分块的目的也是为了更好的将特征数据进行汇总。只不过分块时的基础单元，从分组时的像素梯度矢量，变为了分组特征向量。记分块为 $$Block$$ ，分块特征向量为 $$\vec{Block}$$ 。仍以 $$\vert target \vert_1$$ 表示归一化操作，有：

$$
{\displaystyle 
 \begin{aligned}
    \vec{Block} &= \vert [\vec{Cell}_1,\ \vec{Cell}_2,\ \vec{Cell}_3,\ \vec{Cell}_4] \vert_1  \in \mathbb{R}^{(N \times N) \cdot \theta \times 1}  \\
 \end{aligned}
}
$$

可见，在 $$2 \times 2$$ 大小的固定分块下，分块特征向量  的维度即为分组特征向量方向的 $$4$$ 倍，即 $$(N \times N) \cdot \theta$$ 。如果我们采用 L-2 归一化（即 L2范数）处理，记归一化因子为 $$L_2$$ ，则：

$$
{\displaystyle 
 \begin{aligned}
    L_2 &= \sqrt{|\vec{Cell}_1 |^2+\ |\vec{Cell}_2 |^2+\ |\vec{Cell}_3 |^2+\ |\vec{Cell}_4 |^2}  \\
        &= \sqrt{\sum  (| \angle \vec{G}_1|^2 +\ | \angle \vec{G}_2|^2  +\ | \angle \vec{G}_3|^2  +\ | \angle \vec{G}_4|^2 )} \\
    \vec{Block} 
        &= \frac{1}{L_2}[\vec{Cell}_1,\ \vec{Cell}_2,\ \vec{Cell}_3,\ \vec{Cell}_4] \in \mathbb{R}^{(N \times N) \cdot \theta \times 1}  
 \end{aligned}
}
$$

那么，对图例中的分组进行块归一化到 $$[0,\ 1]$$ 区间，所得如下：

<center>
<figure>
   <img  
      width = "600" height = "290"
      src="../../Pictures/hog-example-3.png" alt="">
    <figcaption>
      <p>图 3.3.1-7 图例（数据源）绿色框对应块的块归一化特征向量结果</p>
   </figcaption>
</figure>
</center>

之后，按照块大小为步长，对全图分块计算即可得到输入图片的方向梯度直方图运算结果。达成对图片整体和分块区域的运动检测目的。

那么，在具体实践中是怎么做的呢？

同前文中对滤波的处理方法类似，**对于此类存在核操作流的方法论，为了充分利用 GPU 并行计算能力，通用思路仍然是抽象为可执行的渲染程序片来交由 GPU 加速。**

## **以索贝尔梯度计算 HOG 的 GLSL 渲染程序片**

现在，我们可以依据理论来做 GPU 的动态管线程序片封装。

首先，我们需要定义 **顶点程序片（Vertex Shader）**。通过该程序片指定 GPU 的绘制区域，以及纹理与物体的点位映射。由于我们是对整个视窗界面进行处理，所以可以采用对传入的顶点数据进行坐标变换的方式，来求得顶点映射的纹理坐标，减少少量数据通信：

```glsl
attribute vec3 position;

varying vec4 fs_position;
varying vec2 fs_texcoord;

void main()
{
    fs_position = vec4(position.x, position.y, position.z, 1.0);
    fs_texcoord = (position.xy + vec2(1.0, 1.0)) / 2.0;
    gl_Position = fs_position;
}
```

程序化 HOG 的关键处理部分，依旧在 **像素程序片（Pixel Shader/Fragment Shader）** 上。相比之前对于滤波算法的实现，这里 **显然复杂得多** ：

```glsl
precision mediump float;

const float PI = 3.1415927;

const int n = 8;
const int N = 2;
const int SIZE_CV = (n + 1);
const int SIZE_BV = /*N * N **/ SIZE_CV; // for orientation weight sum

const float ANGLE_GAP = 20.0 * PI / 180.0;
const vec3 ANGLE_0   = vec3(cos(ANGLE_GAP * 0.0), sin(ANGLE_GAP * 0.0), 100); // x=cos y=sin z=cot
const vec3 ANGLE_20  = vec3(cos(ANGLE_GAP * 1.0), sin(ANGLE_GAP * 1.0), 2.74747742);
const vec3 ANGLE_40  = vec3(cos(ANGLE_GAP * 2.0), sin(ANGLE_GAP * 2.0), 1.19175359);
const vec3 ANGLE_60  = vec3(cos(ANGLE_GAP * 3.0), sin(ANGLE_GAP * 3.0), 0.57735027);
const vec3 ANGLE_80  = vec3(cos(ANGLE_GAP * 4.0), sin(ANGLE_GAP * 4.0), 0.17632698);
const vec3 ANGLE_100 = vec3(cos(ANGLE_GAP * 5.0), sin(ANGLE_GAP * 5.0), -0.17632698);
const vec3 ANGLE_120 = vec3(cos(ANGLE_GAP * 6.0), sin(ANGLE_GAP * 6.0), -0.57735027);
const vec3 ANGLE_140 = vec3(cos(ANGLE_GAP * 7.0), sin(ANGLE_GAP * 7.0), -1.19175359);
const vec3 ANGLE_160 = vec3(cos(ANGLE_GAP * 8.0), sin(ANGLE_GAP * 8.0), -2.74747742);
const vec3 ANGLE_180 = vec3(cos(ANGLE_GAP * 9.0), sin(ANGLE_GAP * 9.0), -100);

const float CELL_TILE_SIZE      = 8.0;   //pixels
const float BLOCK_TILE_SIZE     = 2.0;   //cells

const float HOG_TILE_SIZE       = 16.0;  //pixels(n*N)
const float HOG_SHAFT_LENGTH    = 14.0;
const float HOG_SHAFT_THICKNESS = 0.5;
const float HOG_SHAFT_HEAD_RATE = 64.0;
const vec3  HOG_COLOR           = vec3(1.0, 1.0, 0.0);
const float HOG_MIN_MAGNITUDE   = 0.1;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform mat3 sobel_matrix_x;
uniform mat3 sobel_matrix_y;
uniform float hog_magnitude_limit;
uniform sampler2D target_texture;

/* Simple Grey */
float grey(vec3 c)
{
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2];
}

/* Calucate HOG Orient-hog Density (pixel by pixel) */
float hog_density(vec2 target_coord, vec3 field_vector) {
    vec2 ori_pos = target_coord.xy / pixel_bias;
    vec2 tile_center = (floor(ori_pos / HOG_TILE_SIZE) + 0.5) * HOG_TILE_SIZE;
    float magnitude = abs(field_vector.z);
    if (magnitude > max(HOG_MIN_MAGNITUDE, hog_magnitude_limit)) {
        float distance = clamp(magnitude * HOG_SHAFT_LENGTH, 0.1, HOG_SHAFT_LENGTH);
        vec2 normalizer = normalize(field_vector.xy);
        vec2 tile_offset = ori_pos - tile_center;
        float density = HOG_SHAFT_THICKNESS / HOG_SHAFT_HEAD_RATE - max(
        abs(dot(tile_offset, vec2(+normalizer.y, -normalizer.x))),
        abs(dot(tile_offset, vec2(+normalizer.x, +normalizer.y))) - distance
        );
        return clamp(1.0 + density, 0.0, 1.0);
    }
    return 0.0;
}

/* Calucate Sobel Field at target center */
vec3 sobel_edge_detection(vec2 target_coord) {
    float gradient_center_x;
    float gradient_center_y;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            float check_grey = grey(color_sample.rgb);
            gradient_center_x += check_grey * sobel_matrix_x[i][j];
            gradient_center_y += check_grey * sobel_matrix_y[i][j];
        }
    }
    // float rectangle = (atan(gradient_center_y, gradient_center_x) + 2.0 * PI) / (PI);
    vec2  orientate = vec2(gradient_center_x, gradient_center_y);
    float magnitude = length(orientate);
    return vec3(orientate, magnitude);
}

/* Calucate Cell Feature at target center */
mat3 cell_feature_extraction(vec2 target_coord) {
    mat3  result;
    float bias_unit = float(n-1)/2.0;
    vec2 ori_pos = target_coord.xy / pixel_bias;
    vec2 cell_center = (floor(ori_pos / CELL_TILE_SIZE) + 0.5) * CELL_TILE_SIZE;

    float normalization_factor = 0.0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(float(i)-bias_unit, float(j)-bias_unit) * pixel_bias;
            vec3 field_vector = sobel_edge_detection(cell_center.xy + bias);
            float seek_to =  (field_vector.x+ 0.0001)  / (field_vector.y + 0.0001) ;
            float wight = 0.0;
            float wight_as = 0.0;
            {
                wight = field_vector[2] * wight_as;
                if (ANGLE_0.z>= seek_to && seek_to >= ANGLE_20.z){
                    wight_as = abs((seek_to - ANGLE_0.z)/(ANGLE_20.z - ANGLE_0.z));
                    result[0][0] += field_vector[2] *wight_as;
                    result[0][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_20.z>= seek_to && seek_to >= ANGLE_40.z){
                    wight_as = abs((seek_to - ANGLE_20.z)/(ANGLE_40.z - ANGLE_20.z));
                    result[0][1] += field_vector[2] * wight_as;
                    result[0][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_40.z>= seek_to && seek_to >= ANGLE_60.z){
                    wight_as = abs((seek_to - ANGLE_40.z)/(ANGLE_60.z - ANGLE_40.z));
                    result[0][2] += field_vector[2] * wight_as;
                    result[1][0] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_60.z>= seek_to && seek_to >= ANGLE_80.z){
                    wight_as = abs((seek_to - ANGLE_60.z)/(ANGLE_80.z - ANGLE_60.z));
                    result[1][0] += field_vector[2] * wight_as;
                    result[1][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_80.z>= seek_to && seek_to >= ANGLE_100.z){
                    wight_as = abs((seek_to - ANGLE_80.z)/(ANGLE_100.z - ANGLE_80.z));
                    result[1][1] += field_vector[2] * wight_as;
                    result[1][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_100.z>= seek_to && seek_to >= ANGLE_120.z){
                    wight_as = abs((seek_to - ANGLE_100.z)/(ANGLE_120.z - ANGLE_100.z));
                    result[1][2] += field_vector[2] * wight_as;
                    result[2][0] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_120.z>= seek_to && seek_to >= ANGLE_140.z){
                    wight_as = abs((seek_to - ANGLE_120.z)/(ANGLE_140.z - ANGLE_120.z));
                    result[2][0] += field_vector[2] * wight_as;
                    result[2][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_140.z>= seek_to && seek_to >= ANGLE_160.z){
                    wight_as = abs((seek_to - ANGLE_140.z)/(ANGLE_160.z - ANGLE_140.z));
                    result[2][1] += field_vector[2] * wight_as;
                    result[2][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_160.z>= seek_to && seek_to >= ANGLE_180.z){
                    wight_as = abs((seek_to - ANGLE_160.z)/(ANGLE_180.z - ANGLE_160.z));
                    result[2][2] += field_vector[2] * wight_as;
                    result[0][0] += field_vector[2] * (1.0 - wight_as);
                }
            }
        }
    }
    return result;
}

/* Calucate Block Feature at target center */
float block_feature_extraction(vec2 target_coord) {
    float orient_hog_density = 0.0;
    float block_feature_vector[SIZE_BV];

    vec2 cell_bias = vec2(n, n) * pixel_bias;
    mat3 cell_lt = cell_feature_extraction(target_coord);
    mat3 cell_rt = cell_feature_extraction(target_coord + vec2(cell_bias.x, 0.0));
    mat3 cell_lb = cell_feature_extraction(target_coord + vec2(0.0, cell_bias.y));
    mat3 cell_rb = cell_feature_extraction(target_coord + cell_bias);

    float normalization_factor = 0.0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            normalization_factor += cell_lt[i][j] + cell_rt[i][j] + cell_lb[i][j] + cell_rb[i][j];
            block_feature_vector[i*3+j] = cell_lt[i][j] + cell_rt[i][j] + cell_lb[i][j] + cell_rb[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*0] = cell_lt[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*1] = cell_rt[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*2] = cell_lb[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*3] = cell_rb[i][j];
        }
    }
    for (int i = 0; i < SIZE_BV; i++) {
        // block_feature_vector[i] = block_feature_vector[i] / normalization_factor;
        vec3 field_vector;
        int at = int(mod(float(i) , 9.0));
        float weight = block_feature_vector[i] / normalization_factor;
        if (at == 0){
            field_vector = vec3(ANGLE_0.xy, weight);
        } else if (at == 1){
            field_vector = vec3(ANGLE_20.xy, weight);
        } else if (at == 2){
            field_vector = vec3(ANGLE_40.xy, weight);
        } else if (at == 3){
            field_vector = vec3(ANGLE_60.xy, weight);
        } else if (at == 4){
            field_vector = vec3(ANGLE_80.xy, weight);
        } else if (at == 5){
            field_vector = vec3(ANGLE_100.xy, weight);
        } else if (at == 6){
            field_vector = vec3(ANGLE_120.xy, weight);
        } else if (at == 7){
            field_vector = vec3(ANGLE_140.xy, weight);
        } else if (at == 8){
            field_vector = vec3(ANGLE_160.xy, weight);
        }
        orient_hog_density += hog_density(target_coord, field_vector);
    }
    return orient_hog_density;
}

void main()
{
    vec3 output_ = only_edge? vec3(0) : texture2D(target_texture, fs_texcoord.xy).rgb;
    float orient_hog_density = block_feature_extraction(fs_texcoord.xy);
    vec3 hogs_ = orient_hog_density * HOG_COLOR;
    gl_FragColor = vec4(output_ + hogs_, 1.0);
}
```

样例采用 **单一流水线过程**，我们将几个关键流程节点封装为方法，实现了 HOG 的处理。相对于顶点程序片，像素程序片不太容易理解，还需分步拆开解读。

## **HOG 片元着色器（Fragment Shader）的细节拆解**

首先需要在处理前，进行一部分方法和常量准备。这些 **前置工作包含两个部分**。

**第一部分由纯常量构成。用于辅助实现 方向梯度直方图（HOG）算法 中，各个步骤所使用到的关键恒定参数，有：**

```glsl
const float PI = 3.1415927;

const int n = 8;
const int N = 2;
const int SIZE_CV = (n + 1);
const int SIZE_BV = /*N * N **/ SIZE_CV; // for orientation weight sum

const float ANGLE_GAP = 20.0 * PI / 180.0;
const vec3 ANGLE_0   = vec3(cos(ANGLE_GAP * 0.0), sin(ANGLE_GAP * 0.0), 100);  // x=cos y=sin z=cot
const vec3 ANGLE_20  = vec3(cos(ANGLE_GAP * 1.0), sin(ANGLE_GAP * 1.0), 2.74747742);
const vec3 ANGLE_40  = vec3(cos(ANGLE_GAP * 2.0), sin(ANGLE_GAP * 2.0), 1.19175359);
const vec3 ANGLE_60  = vec3(cos(ANGLE_GAP * 3.0), sin(ANGLE_GAP * 3.0), 0.57735027);
const vec3 ANGLE_80  = vec3(cos(ANGLE_GAP * 4.0), sin(ANGLE_GAP * 4.0), 0.17632698);
const vec3 ANGLE_100 = vec3(cos(ANGLE_GAP * 5.0), sin(ANGLE_GAP * 5.0), -0.17632698);
const vec3 ANGLE_120 = vec3(cos(ANGLE_GAP * 6.0), sin(ANGLE_GAP * 6.0), -0.57735027);
const vec3 ANGLE_140 = vec3(cos(ANGLE_GAP * 7.0), sin(ANGLE_GAP * 7.0), -1.19175359);
const vec3 ANGLE_160 = vec3(cos(ANGLE_GAP * 8.0), sin(ANGLE_GAP * 8.0), -2.74747742);
const vec3 ANGLE_180 = vec3(cos(ANGLE_GAP * 9.0), sin(ANGLE_GAP * 9.0), -100);
	
const float CELL_TILE_SIZE      = 8.0;   //pixels
const float BLOCK_TILE_SIZE     = 2.0;   //cells
```

**第二部分则包含常量和辅助方法。用于辅助 HOG 最终结果的图像化显示，有：**

```glsl
const float CELL_TILE_SIZE      = 8.0;   //pixels
const float BLOCK_TILE_SIZE     = 2.0;   //cells

const float HOG_TILE_SIZE       = 16.0;  //pixels(n*N)
const float HOG_SHAFT_LENGTH    = 14.0;
const float HOG_SHAFT_THICKNESS = 0.5;
const float HOG_SHAFT_HEAD_RATE = 64.0;
const vec3  HOG_COLOR           = vec3(1.0, 1.0, 0.0);
const float HOG_MIN_MAGNITUDE   = 0.1;

/* Simple Grey */
float grey(vec3 c)
{
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2];
}

/* Calucate HOG Orient-hog Density (pixel by pixel) */
float hog_density(vec2 target_coord, vec3 field_vector) {
    vec2 ori_pos = target_coord.xy / pixel_bias;
    vec2 tile_center = (floor(ori_pos / HOG_TILE_SIZE) + 0.5) * HOG_TILE_SIZE;
    float magnitude = abs(field_vector.z);
    if (magnitude > max(HOG_MIN_MAGNITUDE, hog_magnitude_limit)) {
        float distance = clamp(magnitude * HOG_SHAFT_LENGTH, 0.1, HOG_SHAFT_LENGTH);
        vec2 normalizer = normalize(field_vector.xy);
        vec2 tile_offset = ori_pos - tile_center;
        float density = HOG_SHAFT_THICKNESS / HOG_SHAFT_HEAD_RATE - max(
        abs(dot(tile_offset, vec2(+normalizer.y, -normalizer.x))),
        abs(dot(tile_offset, vec2(+normalizer.x, +normalizer.y))) - distance
        );
        return clamp(1.0 + density, 0.0, 1.0);
    }
    return 0.0;
}
```

灰度（光亮度）值采用 **BT.601 的狭隘区间（Narrow Range）** 标准快速计算，运用中也可以替换为均值（部分场景）或根据情况更换其他标准（ **如 RGB数据 非采样得原始数据的标准原色格式而来，则因根据转换前的传输格式来选择配套的规格**，见上一章）。

注意以 **HOG_[xx]** 为格式的常量。**这些常量被用于计算，上屏显示的无符号梯度（Unsigned Gradient）对应方向上的权重柱形轴。** 柱形轴过分块中心，轴的长度和颜色的深浅（即能量密度）代表归一化后的权重大小。而方法计算所得 density 则为当前像素点对应块内位置的能量密度值。显然，密度值只有在轴方向上才存在有效值。另一方面，较小的能量密度也不具有代表性，需要通过 **阈值限定进行过滤**，此处采用 **max(HOG_MIN_MAGNITUDE, hog_magnitude_limit)** 进行设置。

准备完成后，就该正式流程的处理了。这里的封装思路，是以 **生成的最小结果单元为分割依据** 进行的。所以，将 HOG 步骤方法封为一下三个：

- sobel_edge_detection 针对 **像素点（Pixel）梯度矢量** 的 **索贝尔边界检测**

```glsl
/* Calucate Sobel Field at target center */
vec3 sobel_edge_detection(vec2 target_coord) {
    float gradient_center_x;
    float gradient_center_y;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            float check_grey = grey(color_sample.rgb);
            gradient_center_x += check_grey * sobel_matrix_x[i][j];
            gradient_center_y += check_grey * sobel_matrix_y[i][j];
        }
    }
    // float rectangle = (atan(gradient_center_y, gradient_center_x) + 2.0 * PI) / (PI);
    vec2  orientate = vec2(gradient_center_x, gradient_center_y);
    float magnitude = length(orientate);
    return vec3(orientate, magnitude);
}
```

- cell_feature_extraction 针对 **分组（Cell）特征提取** 为结果的 **矢量统计合并**

```glsl
/* Calucate Cell Feature at target center */
mat3 cell_feature_extraction(vec2 target_coord) {
    mat3  result;
    float bias_unit = float(n-1)/2.0;
    vec2 ori_pos = target_coord.xy / pixel_bias;
    vec2 cell_center = (floor(ori_pos / CELL_TILE_SIZE) + 0.5) * CELL_TILE_SIZE;

    float normalization_factor = 0.0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(float(i)-bias_unit, float(j)-bias_unit) * pixel_bias;
            vec3 field_vector = sobel_edge_detection(cell_center.xy + bias);
            float seek_to =  (field_vector.x+ 0.0001)  / (field_vector.y + 0.0001) ;
            float wight = 0.0;
            float wight_as = 0.0;
            {
                wight = field_vector[2] * wight_as;
                if (ANGLE_0.z>= seek_to && seek_to >= ANGLE_20.z){
                    wight_as = abs((seek_to - ANGLE_0.z)/(ANGLE_20.z - ANGLE_0.z));
                    result[0][0] += field_vector[2] *wight_as;
                    result[0][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_20.z>= seek_to && seek_to >= ANGLE_40.z){
                    wight_as = abs((seek_to - ANGLE_20.z)/(ANGLE_40.z - ANGLE_20.z));
                    result[0][1] += field_vector[2] * wight_as;
                    result[0][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_40.z>= seek_to && seek_to >= ANGLE_60.z){
                    wight_as = abs((seek_to - ANGLE_40.z)/(ANGLE_60.z - ANGLE_40.z));
                    result[0][2] += field_vector[2] * wight_as;
                    result[1][0] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_60.z>= seek_to && seek_to >= ANGLE_80.z){
                    wight_as = abs((seek_to - ANGLE_60.z)/(ANGLE_80.z - ANGLE_60.z));
                    result[1][0] += field_vector[2] * wight_as;
                    result[1][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_80.z>= seek_to && seek_to >= ANGLE_100.z){
                    wight_as = abs((seek_to - ANGLE_80.z)/(ANGLE_100.z - ANGLE_80.z));
                    result[1][1] += field_vector[2] * wight_as;
                    result[1][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_100.z>= seek_to && seek_to >= ANGLE_120.z){
                    wight_as = abs((seek_to - ANGLE_100.z)/(ANGLE_120.z - ANGLE_100.z));
                    result[1][2] += field_vector[2] * wight_as;
                    result[2][0] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_120.z>= seek_to && seek_to >= ANGLE_140.z){
                    wight_as = abs((seek_to - ANGLE_120.z)/(ANGLE_140.z - ANGLE_120.z));
                    result[2][0] += field_vector[2] * wight_as;
                    result[2][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_140.z>= seek_to && seek_to >= ANGLE_160.z){
                    wight_as = abs((seek_to - ANGLE_140.z)/(ANGLE_160.z - ANGLE_140.z));
                    result[2][1] += field_vector[2] * wight_as;
                    result[2][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_160.z>= seek_to && seek_to >= ANGLE_180.z){
                    wight_as = abs((seek_to - ANGLE_160.z)/(ANGLE_180.z - ANGLE_160.z));
                    result[2][2] += field_vector[2] * wight_as;
                    result[0][0] += field_vector[2] * (1.0 - wight_as);
                }
            }
        }
    }
    return result;
}
```

- block_feature_extraction 针对 **分块（Block）特征提取** 为结果的 **块归一化**

```glsl
/* Calucate Block Feature at target center */
float block_feature_extraction(vec2 target_coord) {
    float orient_hog_density = 0.0;
    float block_feature_vector[SIZE_BV];

    vec2 cell_bias = vec2(n, n) * pixel_bias;
    mat3 cell_lt = cell_feature_extraction(target_coord);
    mat3 cell_rt = cell_feature_extraction(target_coord + vec2(cell_bias.x, 0.0));
    mat3 cell_lb = cell_feature_extraction(target_coord + vec2(0.0, cell_bias.y));
    mat3 cell_rb = cell_feature_extraction(target_coord + cell_bias);

    float normalization_factor = 0.0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            normalization_factor += cell_lt[i][j] + cell_rt[i][j] + cell_lb[i][j] + cell_rb[i][j];
            block_feature_vector[i*3+j] = cell_lt[i][j] + cell_rt[i][j] + cell_lb[i][j] + cell_rb[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*0] = cell_lt[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*1] = cell_rt[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*2] = cell_lb[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*3] = cell_rb[i][j];
        }
    }
    for (int i = 0; i < SIZE_BV; i++) {
        // block_feature_vector[i] = block_feature_vector[i] / normalization_factor;
        vec3 field_vector;
        int at = int(mod(float(i) , 9.0));
        float weight = block_feature_vector[i] / normalization_factor;
        if (at == 0){
            field_vector = vec3(ANGLE_0.xy, weight);
        } else if (at == 1){
            field_vector = vec3(ANGLE_20.xy, weight);
        } else if (at == 2){
            field_vector = vec3(ANGLE_40.xy, weight);
        } else if (at == 3){
            field_vector = vec3(ANGLE_60.xy, weight);
        } else if (at == 4){
            field_vector = vec3(ANGLE_80.xy, weight);
        } else if (at == 5){
            field_vector = vec3(ANGLE_100.xy, weight);
        } else if (at == 6){
            field_vector = vec3(ANGLE_120.xy, weight);
        } else if (at == 7){
            field_vector = vec3(ANGLE_140.xy, weight);
        } else if (at == 8){
            field_vector = vec3(ANGLE_160.xy, weight);
        }
        orient_hog_density += hog_density(target_coord, field_vector);
    }
    return orient_hog_density;
}
```

考虑到思路连贯性，样例中的实现将所有步骤放在一张纹理过程中处理，且没有对核计算做优化。这会导致每个像素都存在一次 **HOG 计算金字塔**，而按理来说 **一个块内并不需要重复计算**。样例中相当于将块内运算重复了 $$16 \times 16$$ 次，极大的增加了消耗。

因此，在实际应用中，需要对上文的实现进行改造。 **把文中程序片内的各个步骤的方法，分配到不同阶的程序片中，并优化纹理过程。** 之后才能被更为高效的予以运用。介于骨干并无不同，此处就不再展开赘述。

经过处理后的最终结果，以能量密度的形式附加到当前像素点的色彩值上，实现最终的图形化展示：

```glsl
void main()
{
    vec3 output_ = only_edge? vec3(0) : texture2D(target_texture, fs_texcoord.xy).rgb;
    float orient_hog_density = block_feature_extraction(fs_texcoord.xy);
    vec3 hogs_ = orient_hog_density * HOG_COLOR;
    gl_FragColor = vec4(output_ + hogs_, 1.0);
}

```

现在，整个 HOG 的简易程序片就完成了。

**到此为止，方向梯度直方图技术可以初步应用于音视频当中了。** 虽然在上文样例的渲染程序片实现过程中，但从普遍意义上来讲，HOG 仍然属于相对高消耗的算法， HOG 提供的方法论更多被应用在 **编解码规格制定的时域冗余处理** 上。其本身具有一定的 **硬件门槛**。

## **HOG 最终产物的用处**

假设输入帧长宽为 $$W \times H = 256 \times 256$$ 。按照前文采用块大小 $$2 \times 2$$ ，分组大小 $$8 \times 8$$ 进行处理，则得到方向梯度直方图最终输出结果为包含 $$16 \times 16 = 256$$ 个块特征向量的数据集合。每一个块特征向量由 $$(2 \times 2) \cdot 9  = 36$$ 维（参数）构成。为了方便描述，我们将输出数据集称为 **HOG 数据帧**。

**HOG 数据帧（HOG Frame）更多被作为经过特征提取后的预处理输入数据，传入目标物体检测等人工智能计算机视觉方向的算法模型。** 通过模型获取的物体识别结果后，再利用训练好的目标跟踪模型，或传统目标跟踪算法（诸如：核卷积滤波（KCF [Kernelized Correlation Filter]）[18] 、MOSSE 算法等）等，来获取视频流中运动物体在时序上的关联性。

那么，用于判断目标检测结果是否准确的方法，也就是目标检测模型的 **损失函数（Loss Function）** 是什么呢？


[ref]: References_3.md