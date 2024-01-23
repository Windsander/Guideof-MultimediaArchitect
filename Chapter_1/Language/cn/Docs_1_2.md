
# 1.2 声波三要素（Three Elements of Acoustics）

**声音（Sounds）** 是对所有由振动产生，可以被人感知并理解的，由固体、液体、气体等介质而传播的一类 **声波（Acoustic Wave）** 的统称 [\[1\]][ref] 。即，只有被人能够听到的声波，才属于声音。所以，声音是有人感官参与并制定，对声波相对主观的一种描述。由于本质仍是声波，客观对声波的测定量，也是同作用于声音的。什么是声波呢？

**声波（Acoustic Wave）** 是指在介质中传播的机械波。其本质是振动中的质点，在介质中以波的形式传播 [\[2\]][ref] 。因此，声波既可以是 **纵波（Longitudinal Wave）** ，也可以是 **横波（Transverse Wave）** 。

根据两种基本机械波的特性，
- **横声波（Transverse Acoustic Wave）** 只能在固体介质中传播；
- **纵声波（Longitudinal Acoustic Wave）** 则能在固/液/气或介于中间态的介质中传播；

## **理想声波方程式（Ideal Acoustic Wave Equation）**

即然是机械波，那么从波的传播角度，就可以根据机械波的物理性，测量出衡量声波的一维传播方向关系：

$$
{\displaystyle 
 \begin{aligned}
   \frac{\partial^2 p}{\partial t^2} = c^2 \cdot \frac{\partial^2 p}{\partial x^2} \\
 \end{aligned}
}
$$

其中，
以 $$c$$ 代表 **声速（Propagation Speed）** ，即声波的传播速度，单位常用 米/秒（m/s）
以 $$p$$ 代表 **声压（Acoustic Pressure）** ，即声波的压强，单位为 帕斯卡（Pa）
以 $$x$$ 代表 **声位（Spatial Position）** ，即声波的当前空间位置，单位为常用 米（m）
以 $$t$$ 代表 时刻，单位常用 秒（s）

这就是著名的 **一维声波恒等式（1D Acoustic Wave Equation）** 。而以 $$\vec{x}$$ 表示当前声位在空间中距离发出点（即原点，我们假设声波从原点产生）的位姿，将传播从一维扩展到 $$dim(\vec{x}) = n$$ 维空间，则有：

$$
{\displaystyle 
 \begin{aligned}
   \frac{\partial^2 p}{\partial t^2} 
        &= c^2 \cdot \nabla^2 p = c^2 \cdot \Delta p_{\vec{x}} \\
        &= c^2 \cdot \sum_{i=0}^{\dim(\vec{x})} \left( \frac{\partial^2 p}{\partial x_i^2} \right) \\
 \end{aligned}
}
$$

得到了通用的 **理想声波方程（Ideal Acoustic Wave Equation）** ，也称为 **费曼三维声波恒等式（Feynman's 3D Acoustic Wave Equation）** [\[3\]][ref] 。

可见，时间 $$t$$ 时的声压有关时间的二阶偏导数，和该时刻下，声波所处空间位置的二阶导数与声速的平方，成正相关。那么在介质均匀的理想条件下，已知 声速 $$c$$ 、声压 $$p$$ 、声位 $$x$$ 中的任何两个量，都能推导出时刻 $$t$$ 的另外一个定量取值。

因此，**声速（Propagation Speed）** 、**声压（Acoustic Pressure）** 、**声位（Spatial Position）** 被称为 **声波三要素（Three Elements of Acoustics）** 。

但是，**人对声音的感知充满了主观因素**，纯物理测量值虽然能够描述声音的客观特性，却无法度量声音的主观成分。我们还需要介于主客观之间的兼容标的，来协助对主观感受的量化表示。不过，根据声波三要素，我们却可由此来对新定主观体系下的度量衡，进行客观测定。并用于不同参考系下的转换表示。**这点即是声音三要素的底层科学支撑，很重要。**

什么是 **声音三要素（Three Elements of Sounds）** 呢？


[ref]: References_1.md