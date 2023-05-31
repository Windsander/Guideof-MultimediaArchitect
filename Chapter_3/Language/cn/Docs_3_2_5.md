
# 3.2.5 索贝尔滤波（Sobel Filter）

**索贝尔滤波（Sobel Filter）** 是由 **斯坦福人工智能实验室（SAIL [Stanford Artificial Intelligence Laboratory]）** 的 **艾尔文·索贝尔（Irwin Sobel，1940 - present）** 和 **格雷·费尔德曼（Gary Feldman，1942 - present）** 于 1968 年提出的一种用于 **边缘检测（Edge Detection）** 的 **去中心化（Center Insensitive）一阶离散微分算子** [\[15\]][ref] 。

通过在构建 $$3 \times 3$$ 卷积核中，对横纵两个方向距离中心点不同偏移的相邻点，采用不同的方位权重占比的方式，针对性的计算边缘变化影响。其实，是将平面点漂移的方向向量，拆解为以卷积核中心点构建的 $$xy$$ 坐标系下的方向分量。通过抽象方向分量的 **一维简易高斯分布（1D Simple Gaussian Distribution）** 密度函数到方差同位表示，来记录中心点的运动情况。而核内不同取值，则代表垂直于该取值方向的分量高斯分布函数切片，占当前相位的百分比（ **归一化后** ）。

因此，仍然取用大小 $$n \times n = 3 \times 3$$ ，中心点 $$\vec{x_c}$$ 的卷积核。记原信号为 $$S(x)$$ ，边缘检测索贝尔滤波核函数为 $$\mathcal{S}_p(\vec{x_c})$$ ，则：

$$
{\displaystyle 
 \begin{aligned}
    \mathcal{S}_p(\vec{x_c}) =& K \cdot \sqrt{ {G_x}^{2} + {G_y}^{2} } \\
 \end{aligned}
}
$$

横向 $$x$$ 轴方向的滤波核函数 $$G_x$$ 为：

$$
{\displaystyle 
 \begin{aligned}
    G_x(\vec{x_c}) =& K_x \cdot 
    {
      \begin{bmatrix} 
        +1 ,&  \ \ 0   ,&  \ \ -1      \\
        +2 ,&  \ \ 0   ,&  \ \ -2      \\
        +1 ,&  \ \ 0   ,&  \ \ -1
      \end{bmatrix}
    } \cdot \sum_{xy}^{\vec{x_c}}S_{xy} \in \mathbb{R}^{3 \times 3} \\
 \end{aligned}
}
$$

横向 $$y$$ 轴方向的滤波核函数 $$G_y$$ 为：

$$
{\displaystyle 
 \begin{aligned}
    G_y(\vec{x_c}) =& K_y \cdot 
    {
      \begin{bmatrix} 
        +1 ,&  \  +2   ,&  \     +1      \\
         0 ,&  \ \ 0   ,&  \quad  0      \\
        -1 ,&  \  -2   ,&  \     -1
      \end{bmatrix}
    } \cdot \sum_{xy}^{\vec{x_c}}S_{xy} \in \mathbb{R}^{3 \times 3} \\
 \end{aligned}
}
$$

从上式可知，强度系数 $$K$$ 可以拆分到 $$xy$$ 各自方向的子核中，记为 $$\vec{K} = (K_x,K_y)$$ 。则，当 $$\vec{K} = (0,\ 1)$$ 时 $$\mathcal{S}_p(\vec{x_c}) = K \cdot G_y(\vec{x_c})$$ 只保留纵向滤波结果，当 $$\vec{K} = (1,\ 0)$$ 时 $$\mathcal{S}_p(\vec{x_c}) = K \cdot G_x(\vec{x_c})$$ 只保留横向滤波结果。不过，一般情况下我们不会只进行单边检测，因此方便起见还是采用在整体滤波结果上进行强度控制，即使用 $$K \in \mathbb{R}$$ 来调整。

显然，索贝尔滤波是同时具有 **梯度方向（Orientate）** 和 **强度（Magnitude）** 的。记方向为 $$\Theta$$ ，强度为 $$A$$ 。则有：

$$
{\displaystyle 
 \begin{aligned}
    A =& \vert {\mathcal{S}_p(\vec{x_c})} \vert = K \cdot \sqrt{ {G_x}^{2} + {G_y}^{2} } \\
    \Theta =& \angle \mathcal{S}_p(\vec{x_c})\ = {atan2}(G_y,\ G_x)\\
 \end{aligned}
}
$$

此时，有 $${LoG}_n(\vec{x_c})|_{\delta=1.4}^{K=1.0}$$ 可表示如下：

$$
{\displaystyle 
 \begin{aligned}
    {LoG}_n(\vec{x_c})|_{\delta=1.4}
      =& \sum_{xy}S_{xy} \cdot \vert (M_{LoG}|_{\delta=1.4}^{K=1.0}) \vert_1   \in \mathbb{R}^{9 \times 9} \\
 \end{aligned}
}
$$

因此，用索贝尔滤波也可以得到图像中心像素的 **运动漂移信息** ，可用于 **方向梯度直方图（HOG [Histogram of Oriented Gradient]）** 的获取。此部分我们在随后的章节中进行。

那么，基于索贝尔滤波的边界检测该怎样实现呢？

## **马尔滤波的 GLSL 渲染程序片**

现在，我们可以依据理论来做 GPU 的动态管线程序片封装。

首先，我们需要定义 **顶点程序片（Vertex Shader）** 。通过该程序片指定 GPU 的绘制区域，以及纹理与物体的点位映射。由于我们是对整个视窗界面进行处理，所以可以采用对传入的顶点数据进行坐标变换的方式，来求得顶点映射的纹理坐标，减少少量数据通信：

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

程序化索贝尔滤波的关键处理部分，依旧在 **像素程序片（Pixel Shader/Fragment Shader）上和 CPU 的索贝尔算子的计算上** 。我们先看像素程序片（Pixel Shader/Fragment Shader）是怎么实现的：

```glsl
precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform mat3 sobel_matrix_x;
uniform mat3 sobel_matrix_y;
uniform sampler2D target_texture;

void main()
{
    vec3 output_ = only_edge? vec3(0) : texture2D(target_texture, fs_texcoord.xy).rgb;
    vec3 color_center_x;
    vec3 color_center_y;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            color_center_x += color_sample.rgb * sobel_matrix_x[i][j];
            color_center_y += color_sample.rgb * sobel_matrix_y[i][j];
        }
    }
    output_ += vec3(
        length(vec2(color_center_x.r, color_center_y.r)),
        length(vec2(color_center_x.g, color_center_y.g)),
        length(vec2(color_center_x.b, color_center_y.b))
    );
    gl_FragColor = vec4(output_, 1.0);
}
```

我们依旧采用 **强度参数 str_factor** ，对锐化介入的强度进行直接调控。而传入的 **索贝尔算子分为两个方向记为 sobel_matrix_x 和 sobel_matrix_y** 。同 **相邻像素归一化的偏移距离 pixel_bias** 的操作，只需要在执行前由 CPU 计算一次即可。以 JavaScript 语法实现：

```js
function pixel_bias(width, height) {
    return new Float32Array([
        1.0 / width, 1.0 / height
    ]);
}

function calculate_sobel_kernel(use_horizontal, str_factor) {
    let kernel = new Float32Array(use_horizontal ? [
        +1.0, 0.0, -1.0,
        +2.0, 0.0, -2.0,
        +1.0, 0.0, -1.0
    ] : [
        +1.0, +2.0, +1.0,
          0.0,  0.0,  0.0,
        -1.0, -2.0, -1.0
    ])

    for (let i = 0; i < 9; i++) {
        kernel[i] *= str_factor;
    }
    return kernel;
}
```

至此，简易索贝尔滤波器程序片就完成了。

## **马尔滤波的局限性**

虽然索贝尔滤波通过去中心化检测目标像素点周边的运动情况，检测结果也 **相对准确** ，并摆脱了 **由卷积核中心权值造成像素富集而导致对干扰抗性较弱的问题** 。但也正因此 **进一步扩大了边缘扩散（Edge Spread）的风险** 。且当物体轮廓处的灰度（光亮度）变化过于发散时，算法会有一定程度的丢失，即 **对抗弱边缘（Weak Edge）的能力较差**。

不过，这些缺点在只需要边缘位置的情况下，可以通过 **阈值限定二值化（Thresholding）** 来得到一定程度的改善（ **这种做法经常出现在机器学习的数据前处理过程中** ）。由于一般音视频工程并不会需要如此精度，考虑到索贝尔滤波的快捷、简单、高效和高干扰抗性的特点，算法本身常被用于各种场景下的 **边缘数据提取** 和 **像素信息预测** 过程。但本身不适合(也不应该)作为噪音抑制算法使用。

经过几个滤波算法的辨析，我们发现想要真正的有效抑制噪音，达到自然模糊且边缘保存的目的，单纯以多 **非各向异性** 滤波器组合的形式，还是很难得到同 **各向异性** 滤波算法相同的效果。

当然，不同的算法各有自身的优势，并非是独一的非此即彼的对立关系。作为工程师，在不同需求下，还是要灵活取用和组合达成所求。


[ref]: References_3.md