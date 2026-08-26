* [在线演示](Playground_6.md)

## DCT 变换与量化演示器（对应 6.1.3 与 6.2.4）

选择内置纹理（平滑渐变 / 锐利边缘 / 随机噪声）或上传本地图片取 8×8 块，依次展示 DCT 系数热力图、量化结果与重建块；拖动量化步长滑块（可叠加 JPEG 标准亮度量化表），实时观察非零系数计数、Zig-Zag 最后非零位置、估算信息量与重建 PSNR 的变化。所有数据均在本地处理，不会上传。

{% urlembed %}
../../Examples/Playground/dct_quantization.html
{% endurlembed %}

[ref]: References_6.md
