
# 4.6.4 自适应实时评估算法（Adam [Adaptive Moment Estimation]）

**自适应实时评估算法（Adam [Adaptive Moment Estimation]）**，相当于RMSprop 和 Momentum 结合的一种算法，标准Adam 可以认为是 一阶AdaDelta 的动量改进版。

**迭代公式：**

$$
{\displaystyle 
 \begin{aligned}
   g_{t,i} &= \nabla_\theta J(\theta_i) \\
   m_{t,i} &= \beta_1   m_{t-1,i} + (1-\beta_1) g_{t,i} \\
   v_{t,i} &= \beta_2 \ v_{t-1,i} + (1-\beta_2) g_{t,i}^2 \\
   \Delta \theta_{t,i} &= - \frac{\eta}{\sqrt{\hat{v}_{t,i}}+\epsilon}\hat{m}_{t,i}  \\
   \theta_{t+1, i} &= \theta_{t,i} +\Delta \theta_{t,i} =\theta_{t,i} - \frac{\eta}{\sqrt{\hat{v}_{t,i}}+\epsilon}\hat{m}_{t,i}  \\
 \end{aligned}
}
$$

其中 $$\hat{m}_t$$ 、 $$\hat{v}_t$$ 是我们为了防止 $$m$$ 、 $$v$$ 被初始化时为 $$0$$ 导致向 $$0$$ 偏移而做的 **偏差校正值** ，有：

$$
{\displaystyle 
 \begin{aligned}
   \hat{m}_t &= \frac{m_t}{1-\beta_1}  \\
   \hat{v}_t &= \frac{v_t}{1-\beta_2}  \\
 \end{aligned}
}
$$

取 经验系数 $$\beta_1$$ 、 $$\beta_1$$ ，Hinton建议 $$\beta_1 = 0.9$$ ，$$\beta_2 = 0.999$$
取 $$\eta$$ 防爆因子，建议 $$\epsilon = \text{10e -8}= 10^{−8 }$$ 避免干扰运算

Adam 很好的结合了前辈们的各种优化处理手段，成为了集大成之优化函数。因此，Adam是被经常使用的，现代主流优化函数之一。


[ref]: References_4.md