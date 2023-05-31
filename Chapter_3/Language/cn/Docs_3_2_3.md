
# 3.2.3 拉普拉斯滤波（Laplacian Filter）

**拉普拉斯滤波（Laplacian Filter）** 是一种基于二阶微分方程的差异扩大化算子（Operator）。其不仅可以从灰度出发用于物体的 **边缘锐化（Edge Sharpening）** ，也可以应用于全通道的色彩变化增强，即 **广义锐化（Sharpening）**。

数学上，一阶微分能够突出原函数连续变化的幅度特征（即原函数斜率），二阶微分则进一步扩大了对这种变化趋势（即导数的斜率）的描述。而基于多参数的二阶偏导数方程，在展示参数本身对趋势影响的同时，也能够说明两两参数间的影响关系。

由于是对趋势的求导，以离散数据逼近信号的二阶微分方程，只需要使用目标相邻采样做差值计算即可，且并不会影响周边点各自的趋势判断。正好符合目标情况卷积核，对核内关系闭环和抗干扰的要求。所以，拉普拉斯滤波以卷积核中心点构建包含全部方向参数（Orient Axis）的平面坐标系，核内采样求得中心点突变权重的二阶导数展式。用它增强核内数据中心的突变特征。

## **二维拉普拉斯滤波核**

对于二维信号，即图片信号，来说。拉普拉斯卷积核只有 $$xy$$ 两个方向参数。记原信号为 $$S(x)$$ ，原信号的二阶导数为 $$\nabla^2 S(x)$$ 。仍然取用大小 $$n \times n = 3 \times 3$$ ，中心点 $$\vec{x_c}$$ 的卷积核，记边缘检测拉普帕斯滤波核函数为 $$\mathcal{L}_p(\vec{x_c})$$ ，则：

$$
{\displaystyle 
 \begin{aligned}
    \mathcal{L}_p(\vec{x_c}) = -K \cdot \nabla^2 S(\vec{x_c}) \\
 \end{aligned}
}
$$


考虑到需要调节边缘检测强弱。我们采用强度因子 $$K \in (-\infty, +\infty)$$ 作为权重，以便进行敏感度控制。 **则 $$K$$ 取正值时增强， $$K$$ 取负值时衰减， 绝对值 $$\vert K \vert$$ 大小表示放缩强度。** 记核函数为 $$\mathcal{L}_n(\vec{x_c})$$ ，有：

$$
{\displaystyle 
 \begin{aligned}
    \mathcal{L}_n(\vec{x_c}) =& S(\vec{x_c}) + \mathcal{L}_p(\vec{x_c}) \\
                             =& S(\vec{x_c}) - K \cdot \nabla^2 S(\vec{x_c}) \\
 \end{aligned}
}
$$

若 $$\mathcal{L}_p(\vec{x_c})$$ 不计算偏导数在内，即 **只处理轴方向二阶导数** 。我们就可以得到 **双通（2-Way）拉普拉斯核** ：

$$
{\displaystyle 
 \begin{aligned}
    \nabla^2 S(x) 
    =& \tfrac{\mathrm{d}^2 S(\vec{x_c})}{\mathrm{d}{\vec{x_c}^2}} 
    = \tfrac{ \partial^2 S}{\partial x^2} + \tfrac{ \partial^2 S}{\partial y^2} \\
    =& S(x-1,\ y)\ -\ 2 \cdot S(x,y)\ +\ S(x+1,\ y)\ +\ \\
     & S(x,y-1)\ -\ 2 \cdot S(x,y)\ +\ S(x,y+1) \\
    \mathcal{L}_p(\vec{x_c}) 
    =& -K \cdot \sum_{xy}S_{xy} \cdot 
    {
      \begin{bmatrix} 
        0 ,&  \quad \ \ 1   ,&  \quad \ \ 0      \\
        1 ,&  \quad    -4   ,&  \quad \ \ 1      \\
        0 ,&  \quad \ \ 1   ,&  \quad \ \ 0
      \end{bmatrix}
    }\\
    \mathcal{L}_n(\vec{x_c}) 
    =& - K \cdot \sum_{xy}S_{xy} \cdot 
    {
      \begin{bmatrix} 
        0 ,&  \quad \ \ 1   ,&  \quad \ \ 0      \\
        1 ,&  \quad    -4   ,&  \quad \ \ 1      \\
        0 ,&  \quad \ \ 1   ,&  \quad \ \ 0
      \end{bmatrix}
    }\ +\ S(\vec{x_c}) \\
 \end{aligned}
}
$$

若 $$\mathcal{L}_p(\vec{x_c})$$ **包含对角方向** 的影响，即处理偏导数情况，我们就可以得到 **四通（4-Way）拉普拉斯核** ：

$$
{\displaystyle 
 \begin{aligned}
    \nabla^2 S(x) 
    =& \tfrac{\mathrm{d}^2 S(\vec{x_c})}{\mathrm{d}{\vec{x_c}^2}} 
    = \tfrac{ \partial^2 S}{\partial x^2} + \tfrac{ \partial^2 S}{\partial x \partial y} + \tfrac{ \partial^2 S}{\partial y \partial x}  + \tfrac{ \partial^2 S}{\partial y^2} \\
    =& S(x-1,\ y+0)\ -\ 2 \cdot S(x,\ y)\ +\ S(x+1,\ y+0)\ +\ \\
     & S(x-1,\ y-1)\ -\ 2 \cdot S(x,\ y)\ +\ S(x+1,\ y+1)\ +\ \\
     & S(x+1,\ y-1)\ -\ 2 \cdot S(x,\ y)\ +\ S(x-1,\ y+1)\ +\ \\
     & S(x+0,\ y-1)\ -\ 2 \cdot S(x,\ y)\ +\ S(x+0,\ y+1)\ \\
    \mathcal{L}_p(\vec{x_c}) 
    =& -K \cdot \sum_{xy}S_{xy} \cdot 
    {
      \begin{bmatrix} 
        1 ,&  \quad \ \ 1   ,&  \quad \ \ 1      \\
        1 ,&  \quad    -8   ,&  \quad \ \ 1      \\
        1 ,&  \quad \ \ 1   ,&  \quad \ \ 1
      \end{bmatrix}
    }\\
    \mathcal{L}_n(\vec{x_c}) 
    =& - K \cdot \sum_{xy}S_{xy} \cdot 
    {
      \begin{bmatrix} 
        1 ,&  \quad \ \ 1   ,&  \quad \ \ 1      \\
        1 ,&  \quad    -8   ,&  \quad \ \ 1      \\
        1 ,&  \quad \ \ 1   ,&  \quad \ \ 1
      \end{bmatrix}
    }\ +\ S(\vec{x_c}) \\
 \end{aligned}
}
$$

显然，四通拉普拉斯对中心点突变特征能有更好的提炼。如果需要对更多方向进行评估，则需要增大核面积。根据拉普拉斯二阶微分自身的特性可知，大小为 $$n \times n$$ 的卷积核，可选评估方向为 $$2(n-1)$$ 个，相应的需求采样也会成倍扩增。且增大采样面积仅仅是预先提炼出，中心点周边的相邻点的突变情况。用这些点的加权增强值来计算中心点加权增强值。所以，更大的拉普拉斯核只是利用了小核的富集，反而并不一定能够得到更优秀的筛选结果（比如单核内波动，具有复杂高低差变化时）。**因此，为了相对保证结果的稳定性，我们一般不会采用超过 $$n \times n = 3 \times 3$$ 大小的拉普拉斯卷积核。** 

## **拉普拉斯滤波的 GLSL 渲染程序片**

现在，我们可以依据理论来做 GPU 的动态管线程序片封装了。

如果是 **边缘锐化（Edge Sharpening）** 的场景，数据只采用灰度值处理即可。对于 **原色格式（Primaries Format）为 CIE RGB 1931 色彩空间** 的数据，可按下式用 RGB 快速换算：

$$
Grey = 0.299 \cdot R\ +\ 0.587 \cdot G\ +\ 0.114 \cdot B
$$

**此处演示为了便于说明和展示，选择采用更广泛的适用范围，针对广义锐化（Sharpening）构造像素全通道采样的拉普拉斯滤波器。**

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

没有太多操作，因为关键的部分在 **像素程序片（Pixel Shader/Fragment Shader）** 上。依据双通还是四通做一下区分。我们采用两种实现，双通情况下直接计算，有：

```glsl
precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform mat3 laplacian_matrix;
uniform sampler2D target_texture;

void main()
{
    vec3 output_;
    output_ += texture2D(target_texture, fs_texcoord.xy).rgb * ((only_edge? 0.0 : 1.0) + laplacian_matrix[1][1]);
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(-1, -1) * pixel_bias).rgb * laplacian_matrix[0][0];
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(-1, +1) * pixel_bias).rgb * laplacian_matrix[2][0];
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(+1, -1) * pixel_bias).rgb * laplacian_matrix[0][2];
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(+1, +1) * pixel_bias).rgb * laplacian_matrix[2][2];
    gl_FragColor = vec4(output_, 1.0);
}
```

四通则采用 for 循环实现，传入双通的 **拉普拉斯算子 laplacian_matrix** 即可兼容，有：

```glsl
precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform mat3 laplacian_matrix;
uniform sampler2D target_texture;

void main()
{
    vec3 output_ = only_edge? vec3(0) : texture2D(target_texture, fs_texcoord.xy).rgb;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            output_ += color_sample.rgb * laplacian_matrix[i][j];
        }
    }
    gl_FragColor = vec4(output_, 1.0);
}
```

上述程序片中，我们通过 **only_edge 开关** 控制是否只获取边缘信息。而传入的 **拉普拉斯算子 laplacian_matrix** 和 **相邻像素归一化的偏移距离 pixel_bias** 的操作，只需要在执行前由 CPU 计算一次即可。由于采用 Web 展示，此处方法以 JavaScript 语法实现：

```js
function pixel_bias(width, height) {
    return new Float32Array([
        1.0 / width, 1.0 / height
    ]);
}

function calculate_laplacian_kernel(step, way_count, str_factor) {
    let n = step * 2 + 1;
    let max_way = (n - 1) * 2;
    let cur_way = Math.min(way_count, max_way);
    let way_step = Math.floor(max_way / cur_way);
    let kernel = new Float32Array(n * n);

    for (let i = 0; i < n * n; i = i + way_step) {
        kernel[i] = -str_factor;
    }
    kernel[step + n * step] = cur_way * (n - 1) * str_factor;
    return kernel;
}
```

至此，双通和四通的标准拉普拉斯广义锐化滤波器程序片就完成了。

## **拉普拉斯滤波的局限性**

从卷积核可以看出，拉普拉斯滤波仍然是固定梯度的。但是否启用对角元素（Diagonal Elements）对卷积核特性还是会有较大的影响的。

双通拉普拉斯，只对于横纵方向上的数据敏感，构成的卷积核为 **非各向同性（Not Isotropic）** 卷积核。但是在有权重的方向上，数据变化梯度（Gradient）却是等大的。因此，双通拉普拉斯也 **非各向异性（Not Anisotropic）** 。

四通拉普拉斯，由于引入对角线方向代表的 $$45^{\circ}$$ 、 $$135^{\circ}$$ 、 $$225^{\circ}$$ 、 $$315^{\circ}$$ 的计算，使 $$3 \times 3$$ 核心相邻元素所含所有方向上的梯度都成为等大参考值，因此，四通拉普拉斯的卷积核，为 **各向同性（Isotropic）** 卷积核。

所以，虽然四通拉普拉斯能够更好的提取临界边缘特征，但也会同步的保留并增强高频扰动，从而在结果中留存更多的高频噪音。双通则要相对好一些，但相应的临界特征提取能力也变得更弱。不过，若是能够提升数据源的质量，通过 **先行降噪（NRF [Noise Reduction First]）** 过滤部分干扰。那么理论上，最终提取产物的质量也会有一定程度的提升。**马尔滤波（Marr Filter）** 就是对此方向的探索。

同时，拉普拉斯滤波 **并非是脱离中心参考值的边缘锐化（Edge Sharpening）算法** ，对于一些复杂的边缘位置波动情况，会有 **边缘扩散（Edge Spread）** 的风险。且由于 **包含高权重的中心值参与了计算过程** ，使得拉普拉斯滤波对噪声非常敏感，从而极易丢失边缘方向信息，最终导致检测得到的边缘不连续。基于该情况，部分后续的改进算法采用了 ***去中心化（Center Insensitive）** 思想，来一定程度上避免问题发生。比如， **索贝尔滤波（Sobel Filter）** 。


[ref]: References_3.md