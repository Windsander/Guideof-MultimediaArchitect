* [在线演示](Playground_5.md)

## 音频帧分析器（对应 5.2 节）

上传本地音频或使用内置 A4 演示音，调整帧长与窗函数，实时观察频谱泄漏与频率分辨率的变化；下方特征曲线同步给出整段音频的 RMS、过零率与频谱质心（对应 5.2.2），拖动帧位置滑块可逐帧对照三者取值。所有数据均在本地处理，不会上传。

{% urlembed %}
../../Examples/Playground/audio_frame_analysis.html
{% endurlembed %}

## 视频帧分析器（对应 5.3 节）

打开本地视频或使用内置演示视频（三段场景合成，含两次硬切），逐帧计算帧差并绘制运动强度曲线；光流场以 HSV 编码呈现逐区域运动矢量（方向 → 色相，幅度 → 亮度，为浏览器实时性采用 LK 稀疏估计，practice_5 工程使用 Farneback 稠密光流）；拖动阈值系数 k 滑块，实时观察场景切分检出的变化。所有数据均在本地处理，不会上传。

{% urlembed %}
../../Examples/Playground/video_frame_analysis.html
{% endurlembed %}

## 帧处理器（对应 5.4 节）

音频区：播放内置演示音或上传本地音频，一键切换原声（A）与处理链（B），处理链依次为低通滤波、OLA 变速与变调（对应 5.4.1 与 practice_6 的管线），三个滑块各自独立调节。图像区：拖动饱和度、高斯模糊与 USM 锐化滑块，左右对比原图与处理结果。所有数据均在本地处理，不会上传。

{% urlembed %}
../../Examples/Playground/frame_processing.html
{% endurlembed %}

[ref]: References_5.md
