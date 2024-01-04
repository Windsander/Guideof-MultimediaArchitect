
# 4.6.1 经典优化算法（Classic Optimize Function）

常用的经典优化算法，主要有三种，分别是：随即梯度下降法（SGD）、批量梯度下降法（BGD）、小批梯度下降法（MBGD）。

## **随机梯度下降法（SGD [Stochastic Gradient Descent]）**

**迭代公式：**

$$
{\displaystyle 
 \begin{aligned}
   \theta_t = \theta_{t-1} - \eta \dot{} \nabla_\theta J(\theta ; x_i; y_i) \\
 \end{aligned}
}
$$

每次更新时，只对当前对应批次的被选用样本数据，进行 损失函数（Loss） 计算，一次计算一次更新。因为计算少，所以速度快，并且可以实现实时计算，支持动态的样本添加。

## **批量梯度下降法（BGD [Batch Gradient Descent]）**

**迭代公式：**

$$
{\displaystyle 
 \begin{aligned}
   \theta_t = \theta_{t-1} - \eta \dot{} \nabla_\theta J(\theta) \\
 \end{aligned}
}
$$

每次迭代需要计算当前批次整个数据集 损失函数（Loss） ，更新梯度。所以每次计算的耗时比较高。对于大批量数据来说，比较难以处理，更新不实时。简单的说，就是粒度太大。

## **小批梯度下降法（MBGD [Mini-Batch Gradient Descent]）**

**迭代公式：**

$$
{\displaystyle 
 \begin{aligned}
   \theta_t = \theta_{t-1} - \eta \dot{} \nabla_\theta J(\theta ; x_{(i:i+n)}; y_{(i:i+n)}) \\
 \end{aligned}
}
$$

针对 BGD 每次都需要对当前批次数据集的问题，MBGD 进行了改良，每一次更新，取当前批次中的一组子样本集合来进行 损失函数（Loss）计算，降低参数更新方差计算，收敛更稳定，并且因为采用子批次构成矩阵运算，更加有优势。

## **基础优化算法比较**

三个经典算法各有优劣，基本可以以下表来判断。

$$
{\displaystyle 
 \begin{aligned}
  粒度：        &小   \   &SGD < MBGD < BGD   \quad   &大 \\
  速度：        &慢   \   &BGD < MBGD < SGD   \quad   &快 \\
  收敛：        &低   \   &SGD < MBGD < BGD   \quad   &高 \\
  过拟合：      &低   \   &SGD < MBGD < BGD   \quad   &高 \\
 \end{aligned}
}
$$

因为 SGD 每次处理数据单取一个样本点，相比于 MBGD 的当前批次全数据取子集，和 BGD 当前批次扫描全部数据，SGD 更新权重每次计算出的梯度变化幅度相对都会比较大一些，所以不容易在梯度更新上陷入局部最优解。这也是 SGD 较其余两种基本算法的最大优势。建议没有特殊要求，而需要在这三种算法中做选择的话，优先使用 SGD。

当然，他们都有同样的缺点，那就是：

1. 仍存在易陷入局部最小值或鞍点震荡问题，以 BGD 为最
2. 仍存在无法根据不同参数重要程度进行变速权重更新问题，即全权重更新速度统一问题

不过，既然有了疑问，那自然有解决办法。


[ref]: References_4.md