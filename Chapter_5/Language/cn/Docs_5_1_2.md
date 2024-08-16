
# 5.1.2 音频分析库（SoundFile、PyAudio、Librosa、Aubio）

在完成对基础库的熟悉后，我们接下来需要做的就是对工程中，音视频分析的相关核心功能库的学习。以音频分析库为切入点。

如果期望对 **一段音频（或音频流）进行解读**，根据我们已有的认知，将当前的音频数据从封装的音频格式，还原为采样模拟信号对应的 **PCM 数字信号载体** 只是第一步。该操作是后续所有工作的起点。

而音频格式在前文已有介绍，分为 **[三大类别](../../../Chapter_1/Language/cn/Docs_1_6.md)**，即 **[无压缩编码格式](../../../Chapter_1/Language/cn/Docs_1_6_2.md)**、**[无损压缩编码格式](../../../Chapter_1/Language/cn/Docs_1_6_3.md)**、**[有损压缩编码格式](../../../Chapter_1/Language/cn/Docs_1_6_4.md)**。虽然能通过一些针对 **某单个类型** 或 **类型族** 的 **音频编解码库** 来做解码工作，但我们在分析过程中，更希望能够通过 **简单而统一** 的方式，排除掉格式本身细部的工程干扰。使我们能够更关注于对 **音频所含有信息本身** 的分析。

既然如此，为何不直接使用大名鼎鼎的 FFMpeg 来完成从 **编解码到分析**，甚至是 **重排**、**编辑** 等操作呢？

其中的关键就在于，FFMpeg 虽然功能强大，但在以 **实时处理**、**数据集成**、**特征提取** 等为主要应用场景的音频分析情况下，FFMpeg 并不具备足够的优势。更不用提 **Python 的使用环境** 和 **对断点调试临时插值**，与 **基础库的高度兼容** 方面的要求了（尤其对 **模型训练时**，提取的数据能够 **直接被训练过程使用** 的这一点）。

所以，音频分析场景，除非只需要当前音视频数据的 **元信息（Metadata）**，即 **头部信息（Header）**，一般会采用以下这些库来进行。至于 **FFMpeg** ，在实际使用中会把其核心能力局限于 **编解码** 和 **转码** 的范围里，虽然 **其核心库** 和 **辅助插件** 是包含了包括滤镜在内的多种功能的，但通常我们只会以 **最简形式接入**。这一部分，伴随着网络推拉流协议和更贴近于规格的编解码协议库（如 x264 等），将在本系列书籍的进阶篇中细讲。此处暂不做更进一步的讨论。

现在，让焦点回到音频分析库上。常用的音频分析库主要有四个，为 **SoundFile**、**PyAudio**、**Librosa**、**Aubio**，分别对应 \[ **音频文件读写**、**音频流数据的输入输出**、**工程乐理分析**、**实时音频处理** \] 的需求。

## **SoundFile（Python Sound File）**

**SoundFile（PySoundFile [Python Sound File]）** 是一个 **用于读写音频文件的 Python 库**，主要被用于解码（或者编码）常用的音频格式文件 [4] 。例如前文介绍过的 **WAV**、**AIFF**、**FLAC** 等大多数常见音频格式，SoundFile 都已完整支持。并且，通过 SoundFile 取出的音频数据，可以和其他音频分析库（如 Librosa、Aubio 等）和科学计算库（如 Numpy、SciPy 等）配合使用。

实际上，SoundFile 核心能力来自于 **C开源库 Libsndfile**，正是 Libsndfile 为它 **提供了多种音频文件格式的支撑**。而 PySoundFile 则可以看做是 Libsndfile 这个 C语言库的 Python 套接访问入口。因此，如果我们在常规工程中存在对音频文件的读写需求，不妨考虑采用 Libsndfile 来处理，它的官网位于 [http://www.mega-nerd.com/libsndfile/](http://www.mega-nerd.com/libsndfile) ，含有该库的相关技术参数。

#### 主要功能：

1. 支持 **WAV**、**AIFF**、**FLAC**、**OGG** 等多种常见 **音频文件格式**，适用于 **广泛的** 音频读写需求
2. **支持长音频处理**，提供快速读写大文件的功能，并可用于临时性的（分块）流式处理
3. 提供 **高可定制化的 API**，允许用户自定义音频处理流程和数据操作，适合快速分析
4. 允许以不同的数据格式（如浮点型、整型）读取和写入音频数据，及 **基本元数据访问**
5. 与主流科学计算库（如 Numpy、Pandas、SciPy 等）的 **无缝集成**
6. **单一的文件操作专精库**，不存在多个子模块，仅有有限但明确的 API 入口

#### 基础库（sf.）的常用函数（简，仅列出名称）：

1. 数据结构：[&lt;SoundFile&gt;](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile)
2. 关联文件：[open](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.open)
3. 音频读写：[read](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.read), [write](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.write)
4. 基本信息：[info](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.info)

#### 核心类（sf.SoundFile 即 [&lt;SoundFile&gt;](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile)）的常用函数（简，仅列出名称）：

1. 基础参数：[samplerate](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.samplerate), [channels](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.channels), [format](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.format), [subtype](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.subtype), [endian](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.endian), [frames](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.frames)
2. 帧位索引：[seek](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.seek), [tell](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.tell)
3. 数据访问：[read](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.read), [write](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.write), [read_frames](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.read_frames), [write_frames](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.write_frames)
4. 分块读写：[buffer_read](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.buffer_read), [buffer_write](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.buffer_write)

由上可知，SoundFile 本身的调用极其简便，但已满足完整的音频文件读写需求。开源项目位于 **[Github:bastibe/python-soundfile](https://github.com/bastibe/python-soundfile)**。使用细节，可自行前往 **[官方档案馆查阅](https://python-soundfile.readthedocs.io/en/0.11.0/)**。


[ref]: References_5.md