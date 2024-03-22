
# 3.2.4 马尔滤波（Marr Filter）

**马尔滤波（Marr Filter）** 是拉普拉斯滤波采用 **先行降噪（NRF [Noise Reduction First]）** 的改进算法。利用高斯滤波对频率波动性的处理能力，对图片的高频信息进行模糊过滤。再行使标准拉普拉斯边缘检测，筛选突变明显的剩余高频部分并增强，达到更好的效果 [\[14\]][ref] 。

因此马尔滤波也被称为 **拉普拉斯-高斯滤波（LoG [Laplacian of Gaussian]）**，或 **马尔-希德雷斯算法（Marr–Hildreth Algorithm）**。还是以 $$\vert target \vert_1$$ 表示归一化操作。我们记高斯滤波核函数为 $$F_n(\vec{x_c})$$ ，记 LoG 的边缘检测核函数为 $${LoG}_p(\vec{x_c})$$ ，有：

$$
{\displaystyle 
 \begin{aligned}
    {LoG}_n(\vec{x_c}) 
      =& \mathcal{L}_p(\vec{x_c})|_{F_n} 
      =  -K \cdot \nabla^2 F_n(\vec{x_c})  \\
 \end{aligned}
}
$$

其中 $$K$$ 是我们取来控制强度的强度因子，展开简化上式有：

$$
{\displaystyle 
 \begin{aligned}
    {LoG}_p(\vec{x_c}) 
      =& -K \cdot \sum_{xy}S_{xy} \cdot \vert ( -\tfrac{1}{\pi \delta ^4} \cdot [1- \tfrac{(\Delta x^2+\Delta y^2)}{2 \cdot \delta ^2}] \cdot  e ^{-\tfrac{(\Delta x^2+\Delta y^2)}{2 \cdot \delta ^2}})_{xy} \vert_1  \\
 \end{aligned}
}
$$

显然，$${LoG}_p(\vec{x_c})$$ 也满足高斯滤波的特性，在 $$\delta$$ 确定的情况下具有固定大小的算子。如果选用的高斯核大小为 $$3 \times 3$$ ，则考虑到最大程度生效的感受野大小，算法的卷积核必须得保证有至少 $$n \times n \geq 3 \times 3$$ 的取值。但也不能太大。如果超过核心高斯算子大小的 $$5$$ 倍，即 $$n \times n \geq 15 \times 15$$ 时，会非常容易产生采样元素的过度富集，导致边缘取值偏移和过曝问题。 因此，**一般而言 $${LoG}_n(\vec{x_c})$$ 算子的大小会取奇数范围 $$n \times n \in [5 \times 5, \ 11 \times 11]|_{odd}$$ , 记为 $$M_{LoG}$$ 。**

为了便于说明，我们采用 $$n \times n = 9 \times 9$$ 的核大小做计算。当 $$\delta = 1.4$$ 且 $$K = 1.0$$ 时，未归一化的 $$M_{LoG}$$ 可算得为：

$$
{\displaystyle 
 \begin{aligned}
    M_{LoG}|_{\delta=1.4}^{K=1.0}
    =& 
    {
      \begin{bmatrix} 
        0 ,&  \quad \ \ 1   ,&  \quad \ \ 1   ,&  \quad \ \ 2   ,&  \quad \ \ 2   ,&  \quad \ \ 2   ,&  \quad \ \ 1   ,&  \quad \ \ 1   ,&  \quad \ \ 0      \\
        1 ,&  \quad \ \ 2   ,&  \quad \ \ 4   ,&  \quad \ \ 5   ,&  \quad \ \ 5   ,&  \quad \ \ 5   ,&  \quad \ \ 4   ,&  \quad \ \ 2   ,&  \quad \ \ 1      \\
        1 ,&  \quad \ \ 4   ,&  \quad \ \ 5   ,&  \quad \ \ 3   ,&  \quad \ \ 0   ,&  \quad \ \ 3   ,&  \quad \ \ 5   ,&  \quad \ \ 4   ,&  \quad \ \ 1      \\
        2 ,&  \quad \ \ 5   ,&  \quad \ \ 3   ,&  \quad -12     ,&  \quad -24     ,&  \quad -12     ,&  \quad \ \ 3   ,&  \quad \ \ 5   ,&  \quad \ \ 2      \\
        2 ,&  \quad \ \ 5   ,&  \quad \ \ 0   ,&  \quad -24     ,&  \quad -40     ,&  \quad -24     ,&  \quad \ \ 0   ,&  \quad \ \ 5   ,&  \quad \ \ 2      \\
        2 ,&  \quad \ \ 5   ,&  \quad \ \ 3   ,&  \quad -12     ,&  \quad -24     ,&  \quad -12     ,&  \quad \ \ 3   ,&  \quad \ \ 5   ,&  \quad \ \ 2      \\
        1 ,&  \quad \ \ 4   ,&  \quad \ \ 5   ,&  \quad \ \ 3   ,&  \quad \ \ 0   ,&  \quad \ \ 3   ,&  \quad \ \ 5   ,&  \quad \ \ 4   ,&  \quad \ \ 1      \\
        1 ,&  \quad \ \ 2   ,&  \quad \ \ 4   ,&  \quad \ \ 5   ,&  \quad \ \ 5   ,&  \quad \ \ 5   ,&  \quad \ \ 4   ,&  \quad \ \ 2   ,&  \quad \ \ 1      \\
        0 ,&  \quad \ \ 1   ,&  \quad \ \ 1   ,&  \quad \ \ 2   ,&  \quad \ \ 2   ,&  \quad \ \ 2   ,&  \quad \ \ 1   ,&  \quad \ \ 1   ,&  \quad \ \ 0      
      \end{bmatrix}
    } _{9 \times 9} \\
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

除了采样不占优势外，马尔滤波核本身在确定 $$\delta$$ 取值后并不复杂。考虑到最小采样成本，我们一般取用 $$5 \times 5$$ 大小的卷积核。**且不建议对马尔滤波核使用线性采样简化运算，否则会扩大误差。**

## **马尔滤波的 GLSL 渲染程序片**

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

程序化马尔滤波的关键处理部分，依旧在 **像素程序片（Pixel Shader/Fragment Shader）上和 CPU 的马尔算子的计算上**。我们先看像素程序片（Pixel Shader/Fragment Shader）是怎么实现的：

```glsl
precision mediump float;

const int n = 5;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform vec2 pixel_bias;
uniform float marr_matrix[n * n];
uniform sampler2D target_texture;

void main()
{
    vec3 output_;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            output_ += texture2D(target_texture, fs_texcoord.xy + bias).rgb * marr_matrix[i + j * n];
        }
    }
    gl_FragColor = vec4(output_, 1.0);
}
```

完全就是高斯的像素程序片。或者说，对于以矩阵形式传入的固定算子，在程序片的实现上都是可以复用的。**因此，如果遇到类似场景，此类程序片也可以考虑合并或者同态转换。**

而传入的 **马尔算子 marr_matrix** 和 **相邻像素归一化的偏移距离 pixel_bias** 的操作，只需要在执行前由 CPU 计算一次即可。以 JavaScript 语法实现：

```js
function pixel_bias(width, height) {
    return new Float32Array([
        1.0 / width, 1.0 / height
    ]);
}

function calculate_marr_kernel(step, delta) {
    let n = step * 2 + 1;
    let kernel = new Float32Array(n * n);
    let factor_1 = 1.0 / (Math.PI * Math.pow(delta, 4)); // trick: normalized skip
    let factor_2 = 1.0 / (2.0 * delta * delta);

    let normalize_div = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            let diff = Math.pow(i - step, 2) + Math.pow(j - step, 2);
            kernel[j + n * i] = /*factor_1 * (skip) */ (1 - diff * factor_2) * Math.exp(-diff * factor_2);
            normalize_div += kernel[i];
        }
    }
    for (let i = 0; i < kernel.length; i++) {
        kernel[i] /= normalize_div;
    }
    return kernel;
}
```

至此，简易马尔滤波器程序片就完成了。

## **马尔滤波的局限性**

马尔滤波最大问题就在于采样数上。但如果不考虑采样的消耗，其本身也并非毫无缺点。

虽然马尔滤波因 **具有对信号数据所携带高频干扰（即高频噪声）的一定抗性**，使得算法结果相较于拉普拉斯滤波而言，有较大的改善。**但却不能避免非各向异性（Not Anisotropic）引入并增强摩尔纹的缺点。** 且马尔滤波更容易受没有针对中心高权重进行处理，而采用大卷积核进一步 **增加了中心占比** 的影响，出现 **边缘扩散** 和 **非连续** 的问题。

不过在取 $$\delta < 1.0$$ 时，利用高斯算法对波动性的削弱，马尔滤波能够在抑制噪音的同时，进行有限程度并考虑相邻波动特征的边缘增强。这让马尔滤波配合原始数据下，能够达到更自然的滤波效果。所以，**我们一般不采用马尔滤波检测边缘，而是使用其处理广义锐化场景**。

## **马尔滤波的广义锐化应用**

马尔滤波在广义锐化下的核函数是怎样的呢？参考拉普拉斯滤波，我们只需要替换掉权重部分即可：

$$
{\displaystyle 
 \begin{aligned}
    \mathcal{L}_n(\vec{x_c}) =& S(\vec{x_c}) + {LoG}_n(\vec{x_c}) \\
                             =& S(\vec{x_c}) -K \cdot \nabla^2 F_n(\vec{x_c})   \\
 \end{aligned}
}
$$

这里已经有一些复合函数的感觉了。如果我们将数据源 $$S(\vec{x_c})$$ 更换为高斯滤波结果，为区别于 $$F_n(\vec{x_c})$$ ，这里我们记为 $$G_n(\vec{x_c})$$ 。则整个处理函数就成为了，在高斯模糊的基础上再行锐化，达到模糊着色面，增强轮廓边缘的效果。此时的核函数为：

$$
{\displaystyle 
 \begin{aligned}
    \mathcal{L}_n(\vec{x_c}) =& G_n(\vec{x_c}) -K \cdot \nabla^2 F_n(\vec{x_c})   \\
 \end{aligned}
}
$$

以此类推，我们也可以将数据源 $$S(\vec{x_c})$$ 换成其他滤波的结果，将马尔滤波（进一步衍生到所有可行的滤波函数）作为后级处理，**构建连续的滤波处理流水线**。这种思想，即是 **滤波链路（Filter Chain）** 技术的概念起源。

所以，应用于锐化的马尔滤波链路，也被称为 **马尔锐化（Marr Sharpening）**，或简称为 **朴素锐化（Simple Sharpening）** 算法。

## **马尔锐化的 GLSL 渲染程序片**

根据上文的分析，马尔锐化包含两部分：前级数据 和 后级数据。前级数据用于内容主体，后级数据用于叠加锐化。这里我们取用可配置是否采用高斯模糊，作为可选前级数据的程序片方案，对已实现的马尔滤波进行改造。

由于顶点程序片仍然可以被沿用，此处我们单独来看 **像素程序片（Pixel Shader/Fragment Shader）** 该怎么定义：

```glsl
precision mediump float;

const int n = 3;
const int m = 5;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform bool marr_blur;
uniform vec2 pixel_bias;
uniform float gaussian_matrix[n * n];
uniform float marr_matrix[m * m];
uniform float str_factor;
uniform sampler2D target_texture;

vec3 gauss_operation()
{
    vec3 output_;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            output_ += texture2D(target_texture, fs_texcoord.xy + bias).rgb * gaussian_matrix[i + j * n];
        }
    }
    return texture2D(target_texture, fs_texcoord.xy).rgb;
}

vec3 edge_operation()
{
    vec3 output_;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            output_ += color_sample.rgb * marr_matrix[i + j * m];
        }
    }
    return output_;
}

void main()
{
    vec3 output_;
    if (only_edge) {
        output_ = edge_operation();
    } else if (marr_blur) {
        output_ = gauss_operation() - str_factor * edge_operation();
    } else {
        output_ = texture2D(target_texture, fs_texcoord.xy).rgb - str_factor * edge_operation();
    }
    gl_FragColor = vec4(output_, 1.0);
}
```

显然，作为前级输入的高斯滤波，其滤波核大小并不一定需要和后级处理核大小保持一致。我们依旧采用 **强度参数 str_factor**，对锐化介入的强度进行了直接调控。而传入的 **高斯算子 gaussian_matrix** 、 **马尔算子 marr_matrix** 和 **相邻像素归一化的偏移距离 pixel_bias** 的操作，只需要在执行前由 CPU 计算一次即可。以 JavaScript 语法实现：

```js
function pixel_bias(width, height) {
    return new Float32Array([
        1.0 / width, 1.0 / height
    ]);
}

function calculate_gaussian_kernel(step, delta) {
    let n = step * 2 + 1;
    let kernel = new Float32Array(n * n);
    let factor_1 = 1.0 / (Math.sqrt(2.0 * Math.PI) * delta);
    let factor_2 = 1.0 / (2.0 * delta * delta);

    let normalize_div = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            let diff = Math.pow(i - step, 2) + Math.pow(j - step, 2);
            kernel[j + n * i] = factor_1 * Math.exp(-diff * factor_2);
            normalize_div += kernel[i];
        }
    }
    for (let i = 0; i < kernel.length; i++) {
        kernel[i] /= normalize_div;
    }
    return kernel;
}

function calculate_marr_kernel(step, delta) {
    let n = step * 2 + 1;
    let kernel = new Float32Array(n * n);
    let factor_1 = 1.0 / (Math.PI * Math.pow(delta, 4)); // trick: normalized skip
    let factor_2 = 1.0 / (2.0 * delta * delta);

    let normalize_div = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            let diff = Math.pow(i - step, 2) + Math.pow(j - step, 2);
            kernel[j + n * i] = /*factor_1 * (skip) */ (1 - diff * factor_2) * Math.exp(-diff * factor_2);
            normalize_div += kernel[i];
        }
    }
    for (let i = 0; i < kernel.length; i++) {
        kernel[i] /= normalize_div;
    }
    return kernel;
}
```

至此，马尔锐化基本完成。

>看来更稳定的边缘检测，还是需要依赖去中心化的索贝尔滤波了。


[ref]: References_3.md