
# 四、音视频机器学习基础

## **引言**
在前一章中，我们对基础音视频的关键技术工具，进行了详细介绍。其中，不少地方需要用到机器学习相关的处理手段。可见结合机器学习尤其是深度学习模型的优秀能力，来强化现有音视频工程的各方面，已逐步成为主流趋势。

因此，需要我们对机器学习这个大类技术族，有初步的认知。

整个机器学习（ML）的发展历程中，总有不一样的想法和更先进（或特色）的方法论被各路探索者们提出来。而深度学习（DL [Deep Learning]）作为机器学习（ML [Machine Learning]）的实现手段之一，最初的概念早在上个世纪就已经被 Hinton、Bengio、LeCun 等学者提出。受到近年来快速增长的计算机算力和大数据云建设，而得以真正落地。

如果回顾机器学习的发展会发现，过程中通常是多条路线方法论并行的。在历史上（现认为 2019 至今属于第三次高峰），前两次小高峰都是伴随着计算机硬件技术的突破，而带来的飞跃性变革。从单层感知器模型（Single-Perception）到多层感知器模型（Multi-Perception）再到深度信念网络（Deep Belief Network），直至今天百花齐放的 DL。整个历史中的每一次迭代，更像是多次多维度的技术积累准备齐全后，才应运而生的。

本章节主要整理说明了，当下机器学习至 2019 年前的发展简史，并阐明了部分算法的必要基础概念。只给出核心原理，不包含理论证明和推导过程。

>**关键字：机器学习分类、深度学习、激活函数、损失函数、最优化算法**

## **目录**
* [4.1 发展概览](Docs_4_1.md)
* [4.2 模型工程基础](Docs_4_2.md)
	* [4.2.1 算子（Operator）& 层（Layer）](Docs_4_2_1.md)
	* [4.2.2 神经元（Neuron）](Docs_4_2_2.md)
	* [4.2.3 神经网络（NN [Neural Network]）](Docs_4_2_3.md)
	* [4.2.4 特征选择（Feature Selection）](Docs_4_2_4.md)
* [4.3 经典激活函数（Classic Activation Function）](Docs_4_3.md)
	* [4.3.1 Sigmoid](Docs_4_3_1.md)
	* [4.3.2 Tanh](Docs_4_3_2.md)
	* [4.3.3 Softplus](Docs_4_3_3.md)
	* [4.3.4 ReLU 族 ](Docs_4_3_4.md)
	* [4.3.5 ELU & SELU](Docs_4_3_5.md)
	* [4.3.6 Mish](Docs_4_3_6.md)
	* [4.3.7 Swish 族 ](Docs_4_3_7.md)
* [4.4 连接函数/衰减函数（Connection/Attenuation Function）](Docs_4_4.md)
	* [4.4.1 Dropout](Docs_4_4_1.md)
	* [4.4.2 Maxout](Docs_4_4_2.md)
	* [4.4.3 SoftMax](Docs_4_4_3.md)
* [4.5 损失函数（Loss Function）](Docs_4_5.md)
	* [4.5.1 回归项-平均绝对误差（MAE [Mean Absolute Error]）](Docs_4_5_1.md)
	* [4.5.2 回归项-均方误差（MSE [Mean Squared Error]）](Docs_4_5_2.md)
	* [4.5.3 回归项-休伯损失（Huber Loss）](Docs_4_5_3.md)
	* [4.5.4 回归项-分位数损失（Quantile Loss）](Docs_4_5_4.md)
	* [4.5.5 分类项-对数损失（Log Loss）](Docs_4_5_5.md)
	* [4.5.6 分类项-交叉熵损失（Cross Entropy Loss）](Docs_4_5_6.md)
	* [4.5.7 分类项-合页损失（Hinge Loss）](Docs_4_5_7.md)
	* [4.5.8 分类项-对比损失（Contrastive Loss）](Docs_4_5_8.md)
	* [4.5.9 分类项-三元损失（Triplet Loss）](Docs_4_5_9.md)
	* [4.5.10 分类项-对组排异损失（N-Pair Loss）](Docs_4_5_10.md)
	* [4.5.11 正则项-L1 惩罚](Docs_4_5_11.md)
	* [4.5.12 正则项-L2 惩罚](Docs_4_5_12.md)
* [4.6 优化算法/优化器（Optimizer）](Docs_4_6.md)
	* [4.6.1 经典优化算法（Classic Optimize Function）](Docs_4_6_1.md)
	* [4.6.2 优化算法的优化-应对震荡](Docs_4_6_2.md)
	* [4.6.3 优化算法的优化-应对重点强（弱）化更新](Docs_4_6_3.md)
	* [4.6.4 自适应实时评估算法（Adam [Adaptive Moment Estimation]）](Docs_4_6_4.md)
	* [4.6.5 优化算法对比与使用建议](Docs_4_6_5.md)
* [4.7 模型结构速览](Docs_4_7.md)
	* [4.7.1 卷积神经网络（CNN [Convolutional Neural Network]）](Docs_4_7_1.md)
	* [4.7.2 循环神经网络（RNN [Recurrent Neural Network]）](Docs_4_7_2.md)
	* [4.7.3 经典模型：Transformer](Docs_4_7_3.md)
* [【参考文献】](References_4.md)
