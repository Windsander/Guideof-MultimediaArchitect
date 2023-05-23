
# 2.2.3 光亮度（Luminance）

**光亮度（Luminance）** 也被称为辉度，是指固定光所照射单位平面面积光照区域的物理发光强度，单位是尼特（ $$Nit$$ ），代表烛光每立方米（ $$cd/m^2$$ ，candela per square metre）。光亮度属于光度学（Luminosity）概念。区别于亮度（Brightness）这种用来形容人生理光强直接感受的主观描述，光亮度是从可见光谱范围计量的物理量。

光亮度的计算依赖于发光强度度量。而 **发光强度（Luminous Intensity）** 则是用于表示光源给定方向上单位立体角内光通量的物理量，又被称为光强或光度，单位是烛光（ $$cd$$ ， $$candela$$ ）。

如果记光亮度为 $$L_{\mathrm {v}}$$ ，发光强度为 $$I_{\mathrm {v}}$$ ，那么两者单位间的关系为

$$
1 \ Nit = 1 \ cd/m^2 
$$

光亮度的测量方法在格拉斯曼时期，并没有太好的量化标准，因此更多的是作为一个参数来配合其他要素进行颜色描述的。现如今，对于光亮度的国际统一测量标准如下图所示：

<center>
<figure>
   <img width = "500" height = "350"
      src="../../Pictures/luminance%20definition.png" alt=""/>
   <figcaption>
      <p>图 2.2.3-1 光亮度测量实验与关键变量示意图</p>
   </figcaption>
</figure>
</center>


其中， 
- 记 $$\Sigma$$ 代表光源，$$S$$ 代表接受光线的物体照射表面， 
- 记 $${d\Sigma}$$ , 代表发光源上包含到达照射表面指定定向光线出发点的无穷小面积，
- 记 $$dS$$ 代表照射表面上包含指定出发点的光源定向光线照射目标点的无穷小面积，
- 记 $$d\Omega_\Sigma$$ , 代表光线出发点与 $$dS$$ 所构锥体立体角（Solid Angle）的球面度（sr: Steradian）, 
- 记 $$d\Omega_S$$ , 代表光线接受点与 $$d\Sigma$$ 所构锥体立体角（Solid Angle）的球面度（sr: Steradian）, 
- 记 $$n_\Sigma$$ 代表 $$d\Sigma$$ 的法向量， $$\theta_\Sigma$$ 代表 $$n_\Sigma$$ 与指定定向光线的夹角， 
- 记 $$n_S$$ 代表 $$dS$$ 的法向量， $$\theta_S$$ 代表 $$n_S$$ 与指定定向光线的夹角，

如果取国际通用单位制，且光线在传播过程中经过的介质为无损介质的话，那么就存在如下的光亮度计算公式：

$$
{\displaystyle L_{\mathrm {v}_{\Sigma } }={\frac {\mathrm {d} ^{2}\Phi _{\mathrm {v} }}{\mathrm {d} \Sigma \,\mathrm {d} \Omega _{\Sigma }\cos \theta _{\Sigma }}}={\frac {\mathrm {d} ^{2}\Phi _{\mathrm {v} }}{\mathrm {d} S\,\mathrm {d} \Omega _{S}\cos \theta _{S}}}=L_{\mathrm {v}_{\mathrm {S}}}}
$$

取出入面积及立体角相等，记同等出入面积为 $$A$$ ，立体角为 $$\Omega$$ ，照射角为 $$\theta$$ ，则有：

$$
{\displaystyle 
 \begin{aligned}
   &{d} \Omega = {d} \Omega _{\Sigma } = {d} \Omega _{S} \\
   &{d} \theta \ = {d} \theta _{\Sigma }\ = {d} \theta _{S} \\
   &{d} A = {d} {\Sigma }\ \  = {d} {S} \\
 \end{aligned}
}
$$
$$
L_{\mathrm {v}} = {\frac {\mathrm {d} ^{2}\Phi _{\mathrm {v} }}{\mathrm {d} A\,\mathrm {d} \Omega \cos \theta }}
$$

公式中，

以 $$\Phi _{\mathrm {v} }$$ 代表 **光通量（Luminous Flux）** , 单位是流明（ $$lm$$ ，$$lumen$$ ），是指标度可见光对人眼的视觉刺激程度，是光度学下的人眼视觉特性导出量（规格量）。$$1\ cd$$ 点光源在单位立体角（ $$1\ sr$$ ）下的光通量为 $$1\ lm$$ , 即 $$1 \ lm = 1 \ cd \cdot sr$$ 。光通量计算公式是：

$$
{I _{\mathrm {v}}} = {\frac {\mathrm {d} \Phi _{\mathrm {v} }}{\mathrm {d} \Omega}} 
\rightarrow  
{\Phi _{\mathrm {v}}} = \int _{\Sigma } I_v \cdot  {d} \Omega
$$

如果记 $$E_{\mathrm {v}_{\Sigma }}$$ 为单位光源面积发出的光通量即 **光出射度（Luminous Exitance）** ，记 $$E_{\mathrm {v}_{S }}$$ 为单位受照面积接受的光通量即 **光照度（Illumination）** 。那么在无损截止情况下 $$E_{\mathrm {v}_{\Sigma }} = E_{\mathrm {v}_{S }}$$ ，我们记为 $$E_{\mathrm {v}}$$ 。被称为光照射度，单位是勒克斯（ $$lux$$ ， $$lx$$ ）。 $$1 \ lx = 1 \ lm/m^2$$ 有：

$$
E_{\mathrm {v}} = {\frac {\mathrm {d} \Phi _{\mathrm {v} }}{\mathrm {d} A}}
$$

则 $${\mathrm {d} ^{2}\Phi _{\mathrm {v} }}$$ 代表由 $$d\Sigma$$ 发出的光线，在 $$d\Omega_\Sigma$$ 为球面度的立体角下的全方向光通量，即：

$$
d^{2}\Phi _{\mathrm {v} } = dE_{\mathrm {v}} \cdot dA
$$

那么整个公式就可以化简为：

$$
{\displaystyle L_{\mathrm {v} }={\frac {\mathrm {d} E _{\mathrm {v} }}{d \Omega \cdot \cos \theta }}}
$$

这个公式就是我们在光度学角度，用来计算物体 **理想亮度的标准公式** 。

如果需要计算介质造成的损耗，那么公式需要引入 **光展量（Etendue）** ，即在材质折射率下的光束所通过的面积和光束所占有的立体角的积分。我们计 $$G$$ 代表光展量， $$n$$ 代表折射率，则光展量公式：

$$
{\displaystyle G=\int _{\Sigma }\!\int _{S}\mathrm {d} G}
\rightarrow
{\mathrm {d}G }=n^{2} \cdot {\mathrm {d} A\,\mathrm {d} \Omega \cos \theta }
$$

对于无损介质，折射率 $$n=1$$ 。因此，整个亮度公式在知道光展量的情况下，就可以简化为：

$$
{\displaystyle L_{\mathrm {v} }=n^{2}{\frac {\mathrm {d} \Phi _{\mathrm {v} }}{\mathrm {d} G}}} = {\frac {\mathrm {d} \Phi _{\mathrm {v} }}{\mathrm {d} G}}|_{n=1}
$$

光亮度不会影响物体的色彩信息，而仅代表物体本身发光的强度。决定物体本身颜色信息的，则是物体所具有的色调和饱和度属性。

光度单位体系是一套反映视觉亮暗特性的光辐射计量单位，被选作基本量的不是光通量而是发光强度，因此这套公式只适用于可见光范围。对光的更为客观的描述则依赖于辐射度学的相关概念。辐射度学从黑体辐射与能量密度的学角度出发更换了物理学参照物，将光度学系统提出的度量理念适用范围，扩展到了包含长短波的完整电磁波段。进而间接的促成了色温概念在色彩学的应用。这个会在后文中有关颜色度量的章节额外说明。

由于光亮度的这种自成体系的特性。在颜色的三要素的应用中，**它通常被分离单独处理** 。所以，**现代工程体系中不会直接的应用光度学里的光亮度公式** ，而是采用 **[辐射亮度（Radiance）](Docs_2_3_1.md)** 的科学物理量，结合 **[色温（Color Temperature）](Docs_2_4_4.md)** ，或 **色彩空间（Color Space）如 [HSL 的色彩强度（Intensity）](Docs_2_5_7.md)** 的自设定参数，等概念平替。

至此，色彩学的经典理论：格拉斯曼颜色定律，所引申出的重要配参已准备完毕。问题随之而来：

>**我们能否将描述自然现象的参考标准，应用在有局限的实际生产活动中**。


[ref]: References_2.md