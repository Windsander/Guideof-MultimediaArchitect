
# 4.6.3 优化算法的优化-应对重点强（弱）化更新

另一个问题，就是针对性处理对结果影响更大/更小的权重，让重要的迭代的迭代更谨慎，而不重要的获得更快衰减。以保证优势权重，剔除不必要影响。

## **自适应梯度算法（AdaGrad/AGA [Adaptive Gradient Algorithm]）**

**迭代公式：**

$$
{\displaystyle 
 \begin{aligned}
   g_{t,i} &= \nabla_\theta J(\theta_i) \\
   G_{t,i} &= \sum _{\tau=1} ^{t} g_{\tau, i}^2 \\
   \theta_{t+1,i} &= \theta_{t,i} - \frac{\eta}{\sqrt{G_{t,i}+\epsilon}} \dot{} g_{t,i} \\
 \end{aligned}
}
$$

以 $$G_{t,i}$$ 为当前索引为 $$[_i]$$ 的参数，所对应从 $$1$$ 到时刻 $$t$$ 的 **所有梯度平方和**。

**自适应梯度算法（AdaGrad/AGA [Adaptive Gradient Algorithm]）** 是将 SGD 的统一学习速率修改为，有一定预测成分在内的，参数对应独立更新的处理方式。这样处理的好处是，每一个不同参数都会根据当前自身变化和总模型结果关系的差异，独立的进行变更，**变化大的会更快，变化小的会更慢**。减少了手动调节学习速率的次数。

缺点也比较明显：

1. 前期需手工设置一个全局的初始学习率，过大值会导致惩罚变化不明显，过小会提前停止
2. 中后期自适应分母会不断累积导致学习速率不断收缩，趋于非常小从而可能提前结束训练

因此，我们有了改进版 RMSprop 法。

## **均方根传播法（RMSprop）**

**迭代公式：**

$$
{\displaystyle 
 \begin{aligned}
   g_{t,i} &= \nabla_\theta J(\theta_i) \quad , \quad  E[g^2]_{t,i} = \gamma E[g^2]_{t-1,i} + (1-\gamma)g_{t,i}^2 \\
   \Delta \theta_{t,i} &= - \frac{\eta}{\sqrt{E[g^2]_{t,i}+\epsilon}}g_{t,i} = - \frac{\eta}{RMS[g]_{t,i}}g_{t,i} \\
   \theta_{t+1,i} &= \theta_{t,i} + \Delta \theta_{t,i} =\theta_{t,i} - \frac{\eta}{\sqrt{E[g^2]_{t,i}+\epsilon}}g_{t,i} \\
 \end{aligned}
}
$$

以 $$E[g^2]_{t,i}$$ 为当前索引为 $$[_i]$$ 的参数，所对应从 $$1$$ 到时刻 $$t$$ 的所有梯度均方和，有：

$$
RMS[g]_{t,i}=\sqrt{E[g^2]_{t,i}+\epsilon}
$$

因为学习速率变化采用的是 **梯度均方和（RMS）**。所以，**某一维度变化较大时，RMS 较大；变化较小时，RMS 较小**。这样就保证了各个维度的变化速率是基于同一个变化量级的，同时也避免了 AdaGrad 中后期的学习速率极速下降，过早停止的问题。而且，因为 RMS 采用近似算法，极大降低了内存消耗（毕竟不需要记录每一次的迭代值了）

不过，RMSprop 可以看出，仍然依赖于全局学习速率  的设定，那么是否能够继续改进不依赖呢？

如果对比两个方法的过程中单位差异，或许能找到答案。

## **AdaGrad 和 RMSprop 单位问题**

我们知道，很多单位是有实际价值的。比如是米（meter），天（day）等，就有具体物理含义。所以，对于迭代使用的加速度 $$\Delta\theta_t$$ ，一个很自然的期望是，的单位和是保持一致的。

但是：

$$
\Delta x \propto g \propto \frac{\partial f}{\partial x} \propto \frac{1}{x}
$$

有 $$\Delta x$$ 和 $$g$$ 为同单位，而与 $$x$$ 的单位互逆。即 $$x^{-1}$$ 表示的瞬时变化才与 $$\Delta x$$ 和 $$g$$ 为同单位。

也就是说，对于 AdaGrad 和 RMSprop 来说，$$\Delta\theta_t$$ 权重变化量最终得到的结果，其单位和 $$\theta_t$$ 单位并不一致，而是对应时间单位的倒数。而我们要的 权重 $$\theta_t$$ 是时间单位的。

如果我们用牛顿法使 $$\Delta x =H_t^{-1 }g_t$$ ， $$H_t$$ 为 Hessian 矩阵，即所有参数指定 $$t$$ 时刻二阶偏导数方阵，有：

$$
\Delta x \propto H^{-1 }g \propto \frac{\tfrac{\partial f}{\partial x}}{\tfrac{\partial^2 f}{\partial^2 x}} \propto \frac{1}{x}
$$

上述变化后，便能将 $$x$$ 、 $$\Delta x$$ 和 $$g$$ 单位一致化。但是 Hessian 矩阵计算量太大，我们没办法直接使用。所以，我们还需要模拟退火牛顿法，有：

$$
\Delta x = \frac{\frac{\partial f}{\partial x}}{\frac{\partial ^2 f}{\partial ^2 x}} \Rightarrow \Delta x_t = -\frac{\sqrt{\sum{ _{\tau=1} ^{t-1}} \Delta x_\tau} }{\sqrt{E[g^2]_t+\epsilon}}
$$

上式在 $$\infty$$  位置近似等价。

如此，既可以保证单位，又能简化运算。同时我们发现，$$\Delta\theta_t$$ 的更新在这种拟合下，后续迭代不再依赖于全局学习速率 $$\eta$$ 。

于是，便有了 AdaDelta 算法。

## **自适应梯度算法改进版（AdaDelta/ADGA [Adaptive Delta Gradient Algorithm]）**

**迭代公式：**

$$
{\displaystyle 
 \begin{aligned}
   g_{t,i} &= \nabla_\theta J(\theta_i) \quad , \quad  E[g^2]_{t,i} = \gamma E[g^2]_{t-1,i} + (1-\gamma)g_{t,i}^2 \\
   \Delta \theta_{t,i} &= - \frac{RMS[\Delta \theta]_{t-1,i}}{RMS[g]_{t,i}}g_{t,i}  \\
   \theta_{t+1,i} &= \theta_{t,i} + \Delta \theta_{t,i} =\theta_{t,i} - \frac{RMS[\Delta \theta]_{t-1,i}}{RMS[g]_{t,i}}g_{t,i} \\
 \end{aligned}
}
$$

以 $$E[g^2]_{t,i}$$ 为当前索引为 $$[_i]$$ 的参数，所对应从 $$1$$ 到时刻 $$t$$ 的所有梯度均方和，有：

$$
RMS[g]_{t,i}=\sqrt{E[g^2]_{t,i}+\epsilon}
$$

相较于前两种，AdaDelta 具有优势：

1. 结合了 AdaGrad 善于处理稀疏梯度和 RMSprop 善于处理非平稳目标的优点 
2. 不需要依赖于 全局学习速率的设置

是一种相对理想的，针对强弱重点的梯度优化算法了。

目前，我们所有的处理方式都是秩针对性的解决单一问题。那么有没有什么方法，可以结合两类的优点呢？既解决鞍点，又能自适应学习速率呢？

当然有，那就是 Adam 自适应实时评估算法。


[ref]: References_4.md