
# 4.2.3 神经网络（NN [Neural Network]）

本书中的 **神经网络（NN [Neural Network]）** 主要是对深度神经网络（DNN，这是个大类别，见第一节）中，采用 **反向传播（Back Propagation）** 技术的一类深度神经网络的统称。也被称为 **反向传播神经网络（Back Propagation Neural Network）** ，是个广义分类。

所谓反向传播（BP）算法，是一种 **有监督学习（Supervised Learning）算法** 。它需要一个标记好判定结果的数据集，来进行隐藏层特征权重和偏移的迭代。BP 在当前神经网络的损失函数，计算输出预测值与正确值误差之后，以导数驱动调整神经元的权重和偏移（依赖是否参与运算），以期望下次迭代跟贴近预测结果，减少误差 [\[1\]][ref] 。

而这涵盖了，包括 CNN、RNN、GAN、Transformer 在内的这些经典 DNN 模式。

<center>
<figure>
   <img  
      width = "800" height = "260"
      src="../../Pictures/Alexnet.png" alt="">
    <figcaption>
      <p>图 4.2.3-1 完整的 Alexnet 示意图（工程版）</p>
   </figcaption>
</figure>
</center>

如上图所示，我们以经典 CNN 图像分类模型 AlexNet 为例。

由图可以看出，一个神经网络（NN）的构成，通常由一个输入层、多个隐藏层、一个输出层组成。而隐藏层中，根据具体作用的不同，按照之前提到的层级功能性划分，又可以分为 卷积层、池化层等多种子类型。
不同类型的网络，差异体现在层级的设计上。而层级的排列和执行方式，共同组成了工程流水线（Pipeline）。这一整体，被称为神经网络结构（Nerual Network Structure）。我们在实际工作中，常以 神经网络（NN）、模型（Model）来等价指代 神经网络结构。

当然，我们这里展示的只是最简单的深度神经网络。除了单独使用一个模型外，NN 之间也可以根据各种情况进行组合串联 或 联合训练，共同构成更大的神经网络，这种方式被称为 **神经网络聚合（NNE [Neural Network Ensemble]）** 。

除此之外，当下包括 **大模型（Large Model）** 在内的多种模型融合技术，简称 **多模态（Multi Model）** ，皆开始采用多模型混合的实现。
例如，由 **杨立昆（Yann LeCun）** 提出的，基于 **短期预测（Short Term Prediction）** 和 **长期预测交叉融合（Joint Embedding）** 实现完整连续时效预测，的 **自监督大模型（Self-Supervised Large Model）** 理论中，通过将传统深度学习（指带单一功能深度学习模型）的各个功能层或层组合，拆分为包含：损失模型（Cost Module，类似于一个复杂的，非单一点生效的损失函数替代模型）、感知模型（Perception Module）、规则模型（Policy Module）、动作模型（Action Model）、世界模型（World Model）在内的多种特定任务模型（Specific Model），组合为复杂的连续网络，以期实现模型自学习处理体系。


[ref]: References_4.md