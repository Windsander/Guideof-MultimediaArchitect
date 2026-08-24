# Chapter 5 校对报告

> 校对范围：`Chapter_5/Language/cn/` 全部 7 篇（Apex 章首页 + Docs_5_1 ~ Docs_5_1_4 + References_5）
> 行号说明：以下行号均为**修改前原文行号**；同一文件多处修改按行号排序。
> 分类依据：A 文字错误 / B 术语与一致性 / C 技术性存疑（只报告）/ D 链接与资源 / E 排版格式

## 统计

- 审读篇数：**7 / 7（全量逐字审读，含全部示例代码逐行检查）**
- A 类：42 修复点
- B 类：4 修复点
- C 类：8 项（见待确认清单，**均未改动原文**）
- D 类：2 修复点（无效文件引用）
- E 类：7 修复点
- **示例代码专项检查**：本章 3 个工程示例（数学库/声学库/图形库）的 Python 代码逐行检查。修复真实 bug 5 处：`aubio.cqt`（不存在的 API）→ `aubio.dct`、`aubio.specdesc` 参数形式错误、`spectrogram` 未初始化（NameError）、`scaleFactor=1.1s` 非法字面量（语法错误）、自定义函数名 `ploting` 拼写（定义与调用同步修正）。
- 引用编号：References_5 共 10 条，编号连续；1 条引用与所述内容不匹配列入 C 类。

## A/B/D/E 类修复清单

### Apex_5_Introduce.md
- [A] 章节目录 `Mateplotlib` → `Matplotlib`

### Docs_5_1.md
- 无修改

### Docs_5_1_1.md（常用数学库）
- [A] `Mateplotlib` → `Matplotlib` ×2
- [B] `傅里叶` → `傅立叶` ×3（全书统一尺度）
- [A] `一维亥姆霍兹变换` → `一维厄米对称变换（Hermitian FFT）` | hfft 为 Hermitian FFT，与亥姆霍兹（Helmholtz）无关
- [A] `一维快速傅立叶法` → `一维实数傅立叶变换（实输入 FFT）` | 对应 rfft 的实际语义
- [A] `做为` → `作为`；[A] `事例` → `示例` ×2
- [A] `加利福利亚` → `加利福尼亚` ×3（California 译名）
- [A] 自定义函数名 `ploting` → `plotting` ×5（定义处与全部调用处同步修正）
- [E] `**Matplotlib（...Library**）` 加粗标记断裂 → `**...Library）**`

### Docs_5_1_2.md（常用声学库）
- [E] `常规Q变换` → `常规 Q 变换`
- [A] `主要求` → `主要诉求`；[A] `并向当局限` → `并相当局限`（缺字/衍字）
- [A] `四个关键参` → `四个关键参数`
- [E] `C开源库` / `C语言库` / `C语言 作为` / `由于是 C语言库` 中英文间补空格 ×4
- [A] `练习事例` → `练习示例`
- [A] 代码 `aubio.cqt(16)` → `aubio.dct(16)` | aubio 无 cqt 接口，同行注释即为"离散余弦变换（DCT）"
- [A] 代码 `aubio.specdesc(aubio.specdesc_type.centroid, 1024)` → `aubio.specdesc("centroid", 1024)` | aubio Python 绑定以字符串指定谱描述子类型，无 `specdesc_type` 枚举
- [A] 代码 while 循环前补 `spectrogram = []` | 原代码 `spectrogram.append(...)` 未初始化，运行即 NameError

### Docs_5_1_3.md（常用图形与视频库）
- [A] :16 图 5-6 图注 `简易音频播放器的运行效果图` → `解码后必要环节流程示意图` | 图注复制自图 5-5，图片实为 after_decoder_workflow_simple_cn.png
- [A] :33 `Python 的 Tinker 界面库` → `Tkinter`
- [A] :45 `注意区别库名为` → `注意区分库名为`
- [A] :136 链接文本 `image_specification_OpenImageI` → `image_specification_OpenImageIO`（URL 内含 OpenImageIO 可证）
- [A] :179 `相机补益` → `相机补偿`
- [A] :387/:574 `三维影射模块` → `三维映射模块` ×2
- [A] :583/:587 `Registeration` → `Registration` ×2（Coarse Global / Fine Local Registration）
- [A] :589 `tolerence` → `tolerance`（ICP 收敛容差参数名）
- [A] :595 `来获关键点场景内的位姿矩阵` → `来获取关键点在场景内的位姿矩阵`（缺字）
- [A] :741 `练习事例` → `练习示例`
- [A] :808 `际上，这一次的 Demo` → `实际上，这一次的 Demo`（句首缺字）
- [A] 代码 :923 `scaleFactor=1.1s,` → `scaleFactor=1.1,` | `1.1s` 为非法字面量，直接语法错误
- [D] :762/:799 `install_grapic_libs.py` → `install_graphic_libs.py` ×2 | 磁盘实际文件为 `Chapter_5/Examples/env_prepare/install_graphic_libs.py`，原引用与执行命令均指向不存在的文件
- [A] :804 `完成音频库的环境准备工作` → `完成视频库的环境准备工作` | 本小节为视频库安装（自 :762 起），系从音频小节复制的残留

### Docs_5_1_4.md（常用音频处理软件）
- [A] 标题 `Audiacity` → `Audacity`
- [B] `外部噪音` → `噪声`（全书统一尺度）
- [A] `Stream Analyze` → `Stream Analysis`；`Frame Analyze` → `Frame Analysis`（Sonic Visualiser 功能名）
- [A] `的官` → `的官网`（缺字）
- [E] `这 3款 软件` → `这 3 款软件`

### References_5.md
- 无修改（C 类 1 项）

## C 类待确认清单（技术存疑，仅报告未改动）

| # | 位置 | 内容 | 存疑说明 |
|---|------|------|----------|
| 1 | Docs_5_1_1 | `numpy.special` 子库 | NumPy 无 `special` 子模块，特殊函数在 `scipy.special`；疑为笔误或版本混淆 |
| 2 | Docs_5_1_1 | NumPy 金融函数列表 | `np.fv`/`np.pv` 等金融函数自 NumPy 1.18 起已移除（迁移至 numpy-financial），按现行版本所述不可用 |
| 3 | Docs_5_1_1 | Timedelta 属性列表含 `is_leap_year` | `is_leap_year` 为 pandas Timestamp 属性，Timedelta 无此属性 |
| 4 | Docs_5_1_1 | pandas `ix` 索引器示例 | `ix` 自 pandas 0.20 起废弃、1.0 移除，现行版本应使用 `loc`/`iloc` |
| 5 | Docs_5_1_2 | `source.positions` 属性 | aubio source 对象是否有 `positions` 属性存疑（常见为 `get_position`/`duration` 等接口形态），待按所用 aubio 版本核实 |
| 6 | Docs_5_1_2 | 代码 `channels=self.audio_data.shape[1]` | 单声道音频 `shape` 为一维，`shape[1]` 将越界；需按声道分支处理 |
| 7 | Docs_5_1_3 :506 | HS 法 / LK 法引用链接 | 使用 `?h=` GitBook 搜索式内链，非稳定锚点，迁移构建系统后可能失效，待全站内链统一评估 |
| 8 | References_5 [2] | pandas 库引用文献 | 所引为医学领域 PANDAS（儿科自身免疫神经精神障碍）论文，与 pandas 数据库无关；应为 McKinney 2010（Data Structures for Statistical Computing in Python） |

## 遗留建议

1. **图片文件名拼写**：`Chapter_5/Pictures/parctice_2_logistics.png`、`parctice_2_GUI_example.png`、`parctice_3_logistics.png`、`parctice_3_GUI_example.png` 四处磁盘文件名 `parctice` 疑为 `practice` 笔误（同目录 `practice_1_result_*.png` 拼写正确）。md 引用与磁盘文件名一致、链接有效，故**本次未改动**；如需修正应 `git mv` 重命名并同步更新 Docs_5_1_2.md（2 处）、Docs_5_1_3.md（2 处）引用，建议作者确认后处理。
2. **示例脚本文件名拼写**：`Chapter_5/Examples/practice_1_mathetics_libs_using.py` 中 `mathetics` 疑为 `mathematics` 笔误（同目录另有 `practice_2_acoustics_libs_using.py`、`practice_3_graphics_libs_using.py` 命名规律）。md 引用（Docs_5_1_1.md :688/:877）与磁盘一致、链接有效，本次未改动，建议作者确认后随重命名同步更新。
