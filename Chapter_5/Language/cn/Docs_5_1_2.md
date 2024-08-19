
# 5.1.2 音频分析库（SoundFile、PyAudio、Librosa、Aubio）

在完成对基础库的熟悉后，我们接下来需要做的就是对工程中，音视频分析的相关核心功能库的学习。以音频分析库为切入点。

如果期望对 **一段音频（或音频流）进行解读**，根据我们已有的认知，将当前的音频数据从封装的音频格式，还原为采样模拟信号对应的 **PCM 数字信号载体** 只是第一步。该操作是后续所有工作的起点。

而音频格式在前文已有介绍，分为 **[三大类别](../../../Chapter_1/Language/cn/Docs_1_6.md)**，即 **[无压缩编码格式](../../../Chapter_1/Language/cn/Docs_1_6_2.md)**、**[无损压缩编码格式](../../../Chapter_1/Language/cn/Docs_1_6_3.md)**、**[有损压缩编码格式](../../../Chapter_1/Language/cn/Docs_1_6_4.md)**。虽然能通过一些针对 **某单个类型** 或 **类型族** 的 **音频编解码库** 来做解码工作，但我们在分析过程中，更希望能够通过 **简单而统一** 的方式，排除掉格式本身细部的工程干扰。使我们能够更关注于对 **音频所含有信息本身** 的分析。

既然如此，为何不直接使用大名鼎鼎的 FFMpeg 来完成从 **编解码到分析**，甚至是 **重排**、**编辑** 等操作呢？

其中的关键就在于，FFMpeg 虽然功能强大，但在以 **实时处理**、**数据集成**、**特征提取** 等为主要应用场景的音频分析情况下，FFMpeg 并不具备足够的优势。更不用提 **Python 的使用环境** 和 **对断点调试临时插值**，与 **基础库的高度兼容** 方面的要求了（尤其对 **模型训练时**，提取的数据能够 **直接被训练过程使用** 的这一点）。

所以，音频分析场景，除非只需要当前音视频数据的 **元信息（Metadata）**，即 **头部信息（Header）**，一般会采用以下这些库来进行。至于 **FFMpeg** ，在实际使用中会把其核心能力局限于 **编解码** 和 **转码** 的范围里，虽然 **其核心库** 和 **辅助插件** 是包含了包括滤镜在内的多种功能的，但通常我们只会以 **最简形式接入**。这一部分，伴随着网络推拉流协议和更贴近于规格的编解码协议库（如 x264 等），将在本系列书籍的进阶篇中细讲。此处暂不做更进一步的讨论。

现在，让焦点回到音频分析库上。常用的音频分析库主要有四个，为 **SoundFile**、**PyAudio**、**Librosa**、**Aubio**，分别对应 \[ **音频文件读写**、**音频流数据的输入输出**、**工程乐理分析**、**实时音频处理** \] 的需求。

## **SoundFile（Python Sound File）**

**SoundFile（PySoundFile [Python Sound File]）** 是一个 **用于读写音频文件的 Python 库**，主要被用于解码（或者编码）常用的 **音频格式文件** [\[4\]][ref] 。例如前文介绍过的 **WAV**、**AIFF**、**FLAC** 等大多数常见音频格式，SoundFile 都已完整支持。并且，通过 SoundFile 取出的音频数据，可以和其他音频分析库（如 Librosa、Aubio 等）和科学计算库（如 Numpy、SciPy 等）配合使用。

实际上，SoundFile 核心能力来自于 **C开源库 Libsndfile**，正是 Libsndfile 为它 **提供了多种音频文件格式的支撑**。而 PySoundFile 则可以看做是 Libsndfile 这个 C语言库的 Python 套接访问入口。因此，如果我们在常规工程中存在对音频文件的读写需求，不妨考虑采用 Libsndfile 来处理，它的官网位于 [http://www.mega-nerd.com/libsndfile/](http://www.mega-nerd.com/libsndfile) ，含有该库的相关技术参数。

#### 主要功能：

1. 支持 **WAV**、**AIFF**、**FLAC**、**OGG** 等多种常见 **音频文件格式**，适用于 **广泛的** 音频读写需求
2. **支持长音频处理**，提供快速读写大文件的功能，并可用于临时性的（分块）流式处理
3. 提供 **高可定制化的 API**，允许用户自定义音频处理流程和数据操作，适合快速分析
4. 允许以不同的数据格式（如浮点型、整型）读取和写入音频数据，及 **基本元数据访问**
5. 与主流科学计算库（如 Numpy、Pandas、SciPy 等）的 **无缝集成**
6. **单一的文件操作专精库**，不存在多个子模块，仅有有限但明确的 API 入口

#### 基础库（sf.）的常用函数（简，仅列出名称）：

1. 数据结构：
   [&lt;SoundFile&gt;](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile)
2. 关联文件：
   [open](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.open)
3. 音频读写：
   [read](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.read), 
   [write](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.write)
4. 基本信息：
   [info](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.info)

#### 核心类（sf.SoundFile 即 [&lt;SoundFile&gt;](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile)）的常用函数（简，仅列出名称）：

1. 基础参数：
   [samplerate](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.samplerate), 
   [channels](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.channels), 
   [format](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.format), 
   [subtype](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.subtype), 
   [endian](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.endian), 
   [frames](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.frames)
2. 帧位索引：
   [seek](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.seek), 
   [tell](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.tell)
3. 数据访问：
   [read](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.read), 
   [write](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.write), 
   [read_frames](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.read_frames), 
   [write_frames](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.write_frames)
4. 分块读写：
   [buffer_read](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.buffer_read), 
   [buffer_write](https://python-soundfile.readthedocs.io/en/0.11.0/#soundfile.SoundFile.buffer_write)

由上可知，SoundFile 本身的调用极其简便，但已满足完整的音频文件读写需求。开源项目位于 **[Github:bastibe/python-soundfile](https://github.com/bastibe/python-soundfile)**。使用细节，可自行前往 **[官方档案馆查阅](https://python-soundfile.readthedocs.io/en/0.11.0/)**。

## **PyAudio（Python Audio）**

**PyAudio（Python Audio）** 是音频分析中 **常用的音频输入输出操作库**，即 **音频 I/O 库** [\[5\]][ref] 。换句话说，它提供了一组工具和函数，使得开发者可以在项目的 Python 程序中，利用 PyAudio 已有的函数接口，**快速进行音频的流式（这里指本地流）录制和输出**。同 SoundFile 一样，PyAudio 依赖于底层 **C语言库 PortAudio** 的帮助，而其内核 PortAudio 库实则为一个 **专精于多种操作系统上运行（即跨 Windows、MacOS、Linux 平台）的底层音频输入输出（I/O）库**。

所以，与 SoundFile 注重于对音频文件（即本地音频流结果）的操作不同，PyAudio 或者说 PortAudio 的操作重点，在于 **处理对 “实时” 音频流的捕获和析出**。实时音频流，是能够被连续处理传输的音频数据，例如采样自麦克风输入模数转换后的持续不断的数字信号，或者取自播放音频的连续到来分块数据，即 **过程中音频数据**。

由此，音频分析中常用 PyAudio 来完成对被分析音频的 **“启停转播”（Play/Stop/Seek/Pause）**，所谓 **音频本地流控（LASC [Local Audio Stream Control]）**。

#### 主要功能：

1. 专业音频本地流控 Python 库，支持实时音频流的捕获和播放，适合 **实时音频处理任务**
2. 稳定的 **跨平台兼容性**，完整覆盖主流操作系统，包括 Windows、macOS 和 Linux
3. 灵活的 **音频流配置**，提供多种配置选项，如采样率、通道数、样本格式、缓冲区大小等
4. 提供 **接入式回调**，支持使用回调函数处理音频数据，适合低延迟的实时音频分析
5. 与主流科学计算库 和 其他音频库（如 SoundFile）的 **无缝集成**
6. **单一的音频本地流读写专精库**，不存在多个子模块，仅有有限但明确的 API 入口

#### 基础库（pyaudio.）由于特殊的套接设计，仅用于创建 &lt;PyAudio&gt; 即 PortAudio 实例：

1. 数据结构：
   [&lt;PyAudio&gt;](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio)、
   [&lt;Stream&gt;](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream)
2. 创建实例：
   [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio)

#### 核心类（pyaudio.PyAudio 即 [&lt;PyAudio&gt;](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio) 设备实例）的常用函数（简，仅列出名称）：

1. 销毁实例：
   [terminate](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.terminate)
2. 联音频流：
   [open](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.open) （返回 [&lt;Stream&gt;](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream) 实例，通过 stream_callback 参数配置回调）
3. 设备查询：
   [get_device_count](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_device_count), 
   [get_device_info_by_index](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_device_info_by_index), 
   [get_host_api_count](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_host_api_count), 
   [get_default_input_device_info](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_default_input_device_info), 
   [get_default_output_device_info](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_default_output_device_info), 
   [get_host_api_info_by_index](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_host_api_info_by_index), 
   [get_device_info_by_host_api_device_index](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_device_info_by_host_api_device_index)
4. 参数查验：
   [get_sample_size](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.get_sample_size), 
   [is_format_supported](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.PyAudio.is_format_supported)

#### 核心类的（pyaudio.Stream 即 [&lt;Stream&gt;](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream) 音频流实例）的常用函数（简，仅列出名称）：

1. 音频流启停：
   [start_stream](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.start_stream), 
   [stop_stream](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.stop_stream)
2. 音频流关闭：
   [close](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.close)（注意，&lt;Stream&gt; 的 open 状态来自于设备实例，亦是其初始状态）
3. 流状态检测：
   [is_active](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.is_active), 
   [is_stopped](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.is_stopped)
4. 流数据读写：
   [read](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.read), 
   [write](https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.write)

余下使用细节，可自行前往 **[项目官网](https://people.csail.mit.edu/hubert/pyaudio)** ，或 **[官方档案馆查阅](https://people.csail.mit.edu/hubert/pyaudio/docs/)**。

<br>

上述关键函数已包含 PyAudio 的 **几乎全部调用**，但并没有列出 PyAudio 回调格式。这是因为，这一部分正是 PyAudio 分析适用性的关键。在具体使用中，**PyAudio 回调** 的设定方式，和回调各参数意义与取值，是我们留意的重点。

参考 PyAudio 0.2.14 当前最新版，**回调的设置方式和格式都是固定的**，有：

```python
def callback(in_data, frame_count, time_info, in_status):
    # 在此处处理音频数据（例如，进行实时分析或处理）
    return (out_data, out_status)

p = pyaudio.PyAudio()
stream = p.open(
                format=p.get_format_from_width(2),
                channels=1 if sys.platform == 'darwin' else 2,
                rate=44100,
                input=True,
                output=True,
                stream_callback=callback
)
```

其中，**callback(in_data, frame_count, time_info, status)** 即 **回调传入**，包含四个关键参：

- **in_data** 为 **音频数据的输入流**，通常配合 **np.frombuffer(in_data, dtype=np.int16)** 读取数据
- **frame_count** 为 **输入流当前数据对应音频帧数**，即当前 **in_data** 数据覆盖的 **帧数**
- **time_info** 是一个包含了 **三个设备相关时间戳** 的 **数据字典**，有参数（注意表述）：
    - **input_buffer_adc_time** 表示 **输入音频数据被 ADC 处理时的时间戳（如果适用）**
    - **output_buffer_dac_time** 表示 **输出音频数据被 DAC 处理时的时间戳（如果适用）**
    - **current_time** 表示 当前时间，即 **当前调用触发时的系统时间戳**
- **in_status** 是 **记录当前输入回调时，流状态的枚举类标识**。可取三个状态常量，分别是：
    - **pyaudio.paContinue** 表示 **流继续**，即恢复播放和正常播放时的状态，也是默认状态
    - **pyaudio.paComplete** 表示 **流完成**，即代指当前输入流数据为最末尾的一组
    - **pyaudio.paAbort** 表示 **流中止**，即立刻停止时触发，一般为紧急关流或异常情况

在 **callback 处理完毕后**，回调要求以 **return (out_data, out_status)** 的 **格式返回**。同样：

- **out_data** 为 **音频数据的输出流**，根据协定好的音频 PCM 位数对应的格式输出，**一般同输入**
- **out_status** 是 **记录当前输出的状态**，同 **in_status** 的可取值一致，**一般同 in_status 不变**

配置好 callback 后，我们该如何使用呢？只需要于 **&lt;PyAudio&gt;** 实例调用 open 开启流 **&lt;Stream&gt;** 实体时，以 **stream_callback=callback** 将 **函数句柄以参数传入** 即可生效。而这里的 callback 也可 **根据具体情况修改命名**，比如 audio_analyze_callback 。

随之就可以在回调中，完成分析作业了。

## **Librosa**

**Librosa** 是一个功能强大且易于使用的 **音频/乐理（工程）科学分析库**，成体系的提供了用于 **音频特征提取**、**节拍节奏分析**、**音高（工程）估计**、**音频效果器（滤波、特效接口）** 等处理的算法实现。其设计理念来自于 SciPy 2015 年的第十四届 Python 科学大会中，有关音频处理、音频潜藏信息提取与分析快捷化的讨论 [\[6\]][ref] 。因此，在设计之初就完全采用了，与其他科学计算库（如 NumPy、SciPy）和可视化库（主要指 Matplotlib）的 **无缝集成**。而极强的分析能力和可操作性（工程层面），使 Librosa 成为了我们做 **音频分析与操作时的重要工具**。

**必须熟练掌握。**

#### 主要功能：

1. **临时处理友好**，提供简便的方法，在必要时做临时读取和写入音频文件，支持多种格式
2. **快速时频转换**，提供短时傅里叶变换（STFT）、常规Q变换（CQT）等，方便时频域分析
3. **音频特征提取**，支持对梅尔频率倒谱系数（MFCC）、色度特征、频谱对比度等特征提取
4. **节拍节奏分析**，具有节拍跟踪、起音检测等，音乐（工程）分析能力
5. **分割与重采样**，提供音频分割与重采样工具，便于快速分析对比
6. **调音与音频特效**，具有音高估计和调音功能，并支持音频时间伸缩和音高变换等音频效果
7. 当然还有最重要的【无缝集成】特性

#### 基础库（librosa.）的常用函数（简，仅列出名称）：

1. 音频加载：
   [load](https://librosa.org/doc/main/generated/librosa.load.html), 
   [stream](https://librosa.org/doc/main/generated/librosa.stream.html)
2. 音频生成：
   [clicks](https://librosa.org/doc/main/generated/librosa.clicks.html), 
   [tone](https://librosa.org/doc/main/generated/librosa.tone.html), 
   [chirp](https://librosa.org/doc/main/generated/librosa.chirp.html)
3. 简化分析：
   [to_mono](https://librosa.org/doc/main/generated/librosa.to_mono.html), 
   [resample](https://librosa.org/doc/main/generated/librosa.resample.html), 
   [get_duration](https://librosa.org/doc/main/generated/librosa.get_duration.html), 
   [get_samplerate](https://librosa.org/doc/main/generated/librosa.get_samplerate.html)
4. 时频分析：
   [stft](https://librosa.org/doc/main/generated/librosa.stft.html), 
   [istft](https://librosa.org/doc/main/generated/librosa.istft.html), 
   [reassigned_spectrogram](https://librosa.org/doc/main/generated/librosa.reassigned_spectrogram.html), 
   [cqt](https://librosa.org/doc/main/generated/librosa.cqt.html), 
   [icqt](https://librosa.org/doc/main/generated/librosa.icqt.html), 
   [hybrid_cqt](https://librosa.org/doc/main/generated/librosa.hybrid_cqt.html), 
   [pseudo_cqt](https://librosa.org/doc/main/generated/librosa.pseudo_cqt.html), 
   [vqt](https://librosa.org/doc/main/generated/librosa.vqt.html), 
   [iirt](https://librosa.org/doc/main/generated/librosa.iirt.html), 
   [fmt](https://librosa.org/doc/main/generated/librosa.fmt.html), 
   [magphase](https://librosa.org/doc/main/generated/librosa.magphase.html)
5. 时域校准：
   [autocorrelate](https://librosa.org/doc/main/generated/librosa.autocorrelate.html), 
   [lpc](https://librosa.org/doc/main/generated/librosa.lpc.html), 
   [zero_crossings](https://librosa.org/doc/main/generated/librosa.zero_crossings.html), 
   [mu_compress](https://librosa.org/doc/main/generated/librosa.mu_compress.html), 
   [mu_expand](https://librosa.org/doc/main/generated/librosa.mu_expand.html)
6. 谐波分析：
   [interp_harmonics](https://librosa.org/doc/main/generated/librosa.interp_harmonics.html), 
   [salience](https://librosa.org/doc/main/generated/librosa.salience.html), 
   [f0_harmonics](https://librosa.org/doc/main/generated/librosa.f0_harmonics.html), 
   [phase_vocoder](https://librosa.org/doc/main/generated/librosa.phase_vocoder.html)
7. 相位校准：
   [griffinlim](https://librosa.org/doc/main/generated/librosa.griffinlim.html), 
   [griffinlim_cqt](https://librosa.org/doc/main/generated/librosa.griffinlim_cqt.html)
8. 响度单位换算：
   [amplitude_to_db](https://librosa.org/doc/main/generated/librosa.amplitude_to_db.html), 
   [db_to_amplitude](https://librosa.org/doc/main/generated/librosa.db_to_amplitude.html), 
   [power_to_db](https://librosa.org/doc/main/generated/librosa.power_to_db.html), 
   [db_to_power](https://librosa.org/doc/main/generated/librosa.db_to_power.html), 
   [perceptual_weighting](https://librosa.org/doc/main/generated/librosa.perceptual_weighting.html), 
   [frequency_weighting](https://librosa.org/doc/main/generated/librosa.frequency_weighting.html), 
   [multi_frequency_weighting](https://librosa.org/doc/main/generated/librosa.multi_frequency_weighting.html), 
   [A_weighting](https://librosa.org/doc/main/generated/librosa.A_weighting.html), 
   [B_weighting](https://librosa.org/doc/main/generated/librosa.B_weighting.html), 
   [C_weighting](https://librosa.org/doc/main/generated/librosa.C_weighting.html), 
   [D_weighting](https://librosa.org/doc/main/generated/librosa.D_weighting.html), 
   [pcen](https://librosa.org/doc/main/generated/librosa.pcen.html)
9. 时轴单位换算：
   [frames_to_samples](https://librosa.org/doc/main/generated/librosa.frames_to_samples.html), 
   [frames_to_time](https://librosa.org/doc/main/generated/librosa.frames_to_time.html), 
   [samples_to_frames](https://librosa.org/doc/main/generated/librosa.samples_to_frames.html), 
   [samples_to_time](https://librosa.org/doc/main/generated/librosa.samples_to_time.html), 
   [time_to_frames](https://librosa.org/doc/main/generated/librosa.time_to_frames.html), 
   [time_to_samples](https://librosa.org/doc/main/generated/librosa.time_to_samples.html), 
   [blocks_to_frames](https://librosa.org/doc/main/generated/librosa.blocks_to_frames.html), 
   [blocks_to_samples](https://librosa.org/doc/main/generated/librosa.blocks_to_samples.html), 
   [blocks_to_time](https://librosa.org/doc/main/generated/librosa.blocks_to_time.html)
10. 频率单位换算：
   [hz_to_note](https://librosa.org/doc/main/generated/librosa.hz_to_note.html), 
   [hz_to_midi](https://librosa.org/doc/main/generated/librosa.hz_to_midi.html), 
   [hz_to_svara_h](https://librosa.org/doc/main/generated/librosa.hz_to_svara_h.html), 
   [hz_to_svara_c](https://librosa.org/doc/main/generated/librosa.hz_to_svara_c.html), 
   [hz_to_fjs](https://librosa.org/doc/main/generated/librosa.hz_to_fjs.html), 
   [midi_to_hz](https://librosa.org/doc/main/generated/librosa.midi_to_hz.html), 
   [midi_to_note](https://librosa.org/doc/main/generated/librosa.midi_to_note.html), 
   [midi_to_svara_h](https://librosa.org/doc/main/generated/librosa.midi_to_svara_h.html), 
   [midi_to_svara_c](https://librosa.org/doc/main/generated/librosa.midi_to_svara_c.html), 
   [note_to_midi](https://librosa.org/doc/main/generated/librosa.note_to_midi.html), 
   [note_to_svara_h](https://librosa.org/doc/main/generated/librosa.note_to_svara_h.html), 
   [note_to_svara_c](https://librosa.org/doc/main/generated/librosa.note_to_svara_c.html), 
   [hz_to_mel](https://librosa.org/doc/main/generated/librosa.hz_to_mel.html), 
   [hz_to_octs](https://librosa.org/doc/main/generated/librosa.hz_to_octs.html), 
   [mel_to_hz](https://librosa.org/doc/main/generated/librosa.mel_to_hz.html), 
   [octs_to_hz](https://librosa.org/doc/main/generated/librosa.octs_to_hz.html), 
   [A4_to_tuning](https://librosa.org/doc/main/generated/librosa.A4_to_tuning.html), 
   [tuning_to_A4](https://librosa.org/doc/main/generated/librosa.tuning_to_A4.html)
11. 基底频率生成：
   [fft_frequencies](https://librosa.org/doc/main/generated/librosa.fft_frequencies.html), 
   [cqt_frequencies](https://librosa.org/doc/main/generated/librosa.cqt_frequencies.html), 
   [mel_frequencies](https://librosa.org/doc/main/generated/librosa.mel_frequencies.html), 
   [tempo_frequencies](https://librosa.org/doc/main/generated/librosa.tempo_frequencies.html), 
   [fourier_tempo_frequencies](https://librosa.org/doc/main/generated/librosa.fourier_tempo_frequencies.html)
12. 乐理乐谱工具：
   [key_to_notes](https://librosa.org/doc/main/generated/librosa.key_to_notes.html),
   [key_to_degrees](https://librosa.org/doc/main/generated/librosa.key_to_degrees.html),
   [mela_to_svara](https://librosa.org/doc/main/generated/librosa.mela_to_svara.html),
   [mela_to_degrees](https://librosa.org/doc/main/generated/librosa.mela_to_degrees.html),
   [thaat_to_degrees](https://librosa.org/doc/main/generated/librosa.thaat_to_degrees.html),
   [list_mela](https://librosa.org/doc/main/generated/librosa.list_mela.html),
   [list_thaat](https://librosa.org/doc/main/generated/librosa.list_thaat.html),
   [fifths_to_note](https://librosa.org/doc/main/generated/librosa.fifths_to_note.html),
   [interval_to_fjs](https://librosa.org/doc/main/generated/librosa.interval_to_fjs.html),
   [interval_frequencies](https://librosa.org/doc/main/generated/librosa.interval_frequencies.html),
   [pythagorean_intervals](https://librosa.org/doc/main/generated/librosa.pythagorean_intervals.html),
   [plimit_intervals](https://librosa.org/doc/main/generated/librosa.plimit_intervals.html)
13. 乐理音高音调：
   [pyin](https://librosa.org/doc/main/generated/librosa.pyin.html),
   [yin](https://librosa.org/doc/main/generated/librosa.yin.html),
   [estimate_tuning](https://librosa.org/doc/main/generated/librosa.estimate_tuning.html),
   [pitch_tuning](https://librosa.org/doc/main/generated/librosa.pitch_tuning.html),
   [piptrack](https://librosa.org/doc/main/generated/librosa.piptrack.html)
14. 适配杂项：
   [samples_like](https://librosa.org/doc/main/generated/librosa.samples_like.html),
   [times_like](https://librosa.org/doc/main/generated/librosa.times_like.html),
   [get_fftlib](https://librosa.org/doc/main/generated/librosa.get_fftlib.html),
   [set_fftlib](https://librosa.org/doc/main/generated/librosa.set_fftlib.html)

#### 图表显示扩展（librosa.display.）的常用函数（简，仅列出名称，依赖于 Matplotlib）：

1. 数据可视化：
   [specshow](https://librosa.org/doc/main/generated/librosa.display.specshow.html), 
   [waveshow](https://librosa.org/doc/main/generated/librosa.display.waveshow.html)
2. 坐标轴设置：
   [TimeFormatter](https://librosa.org/doc/main/generated/librosa.display.TimeFormatter.html),
   [NoteFormatter](https://librosa.org/doc/main/generated/librosa.display.NoteFormatter.html),
   [SvaraFormatter](https://librosa.org/doc/main/generated/librosa.display.SvaraFormatter.html), 
   [FJSFormatter](https://librosa.org/doc/main/generated/librosa.display.FJSFormatter.html), 
   [LogHzFormatter](https://librosa.org/doc/main/generated/librosa.display.LogHzFormatter.html), 
   [ChromaFormatter](https://librosa.org/doc/main/generated/librosa.display.ChromaFormatter.html), 
   [ChromaSvaraFormatter](https://librosa.org/doc/main/generated/librosa.display.ChromaSvaraFormatter.html), 
   [ChromaFJSFormatter](https://librosa.org/doc/main/generated/librosa.display.ChromaFJSFormatter.html), 
   [TonnetzFormatter](https://librosa.org/doc/main/generated/librosa.display.TonnetzFormatter.html)
3. 适配杂项：
   [cmap](https://librosa.org/doc/main/generated/librosa.display.cmap.html), 
   [AdaptiveWaveplot](https://librosa.org/doc/main/generated/librosa.display.AdaptiveWaveplot.html)

#### 音频特征提取（librosa.feature.）的常用函数（简，仅列出名称）：

1. 工程频谱特征：
   [chroma_stft](https://librosa.org/doc/main/generated/librosa.feature.chroma_stft.html), 
   [chroma_cqt](https://librosa.org/doc/main/generated/librosa.feature.chroma_cqt.html), 
   [chroma_cens](https://librosa.org/doc/main/generated/librosa.feature.chroma_cens.html), 
   [chroma_vqt](https://librosa.org/doc/main/generated/librosa.feature.chroma_vqt.html), 
   [melspectrogram](https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html), 
   [mfcc](https://librosa.org/doc/main/generated/librosa.feature.mfcc.html), 
   [rms](https://librosa.org/doc/main/generated/librosa.feature.rms.html), 
   [spectral_centroid](https://librosa.org/doc/main/generated/librosa.feature.spectral_centroid.html), 
   [spectral_bandwidth](https://librosa.org/doc/main/generated/librosa.feature.spectral_bandwidth.html), 
   [spectral_contrast](https://librosa.org/doc/main/generated/librosa.feature.spectral_contrast.html), 
   [spectral_flatness](https://librosa.org/doc/main/generated/librosa.feature.spectral_flatness.html), 
   [spectral_rolloff](https://librosa.org/doc/main/generated/librosa.feature.spectral_rolloff.html), 
   [poly_features](https://librosa.org/doc/main/generated/librosa.feature.poly_features.html), 
   [tonnetz](https://librosa.org/doc/main/generated/librosa.feature.tonnetz.html), 
   [zero_crossing_rate](https://librosa.org/doc/main/generated/librosa.feature.zero_crossing_rate.html)
2. 乐理节奏特征：
   [tempo](https://librosa.org/doc/main/generated/librosa.beat.tempo.html), 
   [tempogram](https://librosa.org/doc/main/generated/librosa.feature.tempogram.html), 
   [fourier_tempogram](https://librosa.org/doc/main/generated/librosa.feature.fourier_tempogram.html), 
   [tempogram_ratio](https://librosa.org/doc/main/generated/librosa.feature.tempogram_ratio.html)
3. 特征计算：
   [delta](https://librosa.org/doc/main/generated/librosa.feature.delta.html), 
   [stack_memory](https://librosa.org/doc/main/generated/librosa.feature.stack_memory.html)
4. 反向逆推：
   [inverse.mel_to_stft](https://librosa.org/doc/main/generated/librosa.feature.inverse.mel_to_stft.html), 
   [inverse.mel_to_audio](https://librosa.org/doc/main/generated/librosa.feature.inverse.mel_to_audio.html), 
   [inverse.mfcc_to_mel](https://librosa.org/doc/main/generated/librosa.feature.inverse.mfcc_to_mel.html), 
   [inverse.mfcc_to_audio](https://librosa.org/doc/main/generated/librosa.feature.inverse.mfcc_to_audio.html)

#### 起音检测扩展（librosa.onset.）的常用函数（简，仅列出名称）：

1. 峰值检测：
   [onset_detect](https://librosa.org/doc/main/generated/librosa.onset.onset_detect.html)
2. 小值回溯：
   [onset_backtrack](https://librosa.org/doc/main/generated/librosa.onset.onset_backtrack.html)
3. 强度统计：
   [onset_strength](https://librosa.org/doc/main/generated/librosa.onset.onset_strength.html), 
   [onset_strength_multi](https://librosa.org/doc/main/generated/librosa.onset.onset_strength_multi.html)

#### 节拍节奏扩展（librosa.beat.）的常用函数（简，仅列出名称）：

1. 节拍追踪：
   [beat_track](https://librosa.org/doc/main/generated/librosa.beat.beat_track.html)
2. 主位脉冲：
   [plp](https://librosa.org/doc/main/generated/librosa.beat.plp.html)

#### 语谱分解扩展（librosa.decompose.）的常用函数（简，仅列出名称）：

1. 特征矩阵分解：
   [decompose](https://librosa.org/doc/main/generated/librosa.decompose.decompose.html)
2. 源分离滤波：
   [hpss](https://librosa.org/doc/main/generated/librosa.decompose.hpss.html), 
   [nn_filter](https://librosa.org/doc/main/generated/librosa.decompose.nn_filter.html)

#### 音频效果器扩展（librosa.effects.）的常用函数（简，仅列出名称）：

1. 谐波乐源分离：
   [hpss](https://librosa.org/doc/main/generated/librosa.effects.hpss.html), 
   [harmonic](https://librosa.org/doc/main/generated/librosa.effects.harmonic.html), 
   [percussive](https://librosa.org/doc/main/generated/librosa.effects.percussive.html)
2. 时间伸缩：
   [time_stretch](https://librosa.org/doc/main/generated/librosa.effects.time_stretch.html)
3. 时序混音：
   [remix](https://librosa.org/doc/main/generated/librosa.effects.remix.html)
4. 音高移动：
   [pitch_shift](https://librosa.org/doc/main/generated/librosa.effects.pitch_shift.html)
5. 信号操控：
   [trim](https://librosa.org/doc/main/generated/librosa.effects.trim.html), 
   [split](https://librosa.org/doc/main/generated/librosa.effects.split.html), 
   [preemphasis](https://librosa.org/doc/main/generated/librosa.effects.preemphasis.html), 
   [deemphasis](https://librosa.org/doc/main/generated/librosa.effects.deemphasis.html)

#### 时域分割扩展（librosa.segment.）的常用函数（简，仅列出名称）：

1. 自相似性：
   [cross_similarity](https://librosa.org/doc/main/generated/librosa.segment.cross_similarity.html), 
   [path_enhance](https://librosa.org/doc/main/generated/librosa.segment.path_enhance.html)
2. 重复矩阵：
   [recurrence_matrix](https://librosa.org/doc/main/generated/librosa.segment.recurrence_matrix.html), 
   [lag_to_recurrence](https://librosa.org/doc/main/generated/librosa.segment.lag_to_recurrence.html)
3. 延迟矩阵：
   [timelag_filter](https://librosa.org/doc/main/generated/librosa.segment.timelag_filter.html), 
   [recurrence_to_lag](https://librosa.org/doc/main/generated/librosa.segment.recurrence_to_lag.html)
4. 时域聚类：
   [agglomerative](https://librosa.org/doc/main/generated/librosa.segment.agglomerative.html), 
   [subsegment](https://librosa.org/doc/main/generated/librosa.segment.subsegment.html)

#### 顺序模型扩展（librosa.sequence.）的常用函数（简，仅列出名称）：

1. 顺序对齐：
   [dtw](https://librosa.org/doc/main/generated/librosa.sequence.dtw.html), 
   [rqa](https://librosa.org/doc/main/generated/librosa.sequence.rqa.html)
2. 维特比（Viterbi）解码：
   [viterbi](https://librosa.org/doc/main/generated/librosa.sequence.viterbi.html), 
   [viterbi_discriminative](https://librosa.org/doc/main/generated/librosa.sequence.viterbi_discriminative.html), 
   [viterbi_binary](https://librosa.org/doc/main/generated/librosa.sequence.viterbi_binary.html)
3. 状态转移矩阵：
   [transition_uniform](https://librosa.org/doc/main/generated/librosa.sequence.transition_uniform.html), 
   [transition_loop](https://librosa.org/doc/main/generated/librosa.sequence.transition_loop.html), 
   [transition_cycle](https://librosa.org/doc/main/generated/librosa.sequence.transition_cycle.html), 
   [transition_local](https://librosa.org/doc/main/generated/librosa.sequence.transition_local.html)

#### 跨库通用扩展（librosa.util.）的常用函数（简，仅列出名称）：

1. 数组转换：
   [frame](https://librosa.org/doc/main/generated/librosa.util.frame.html), 
   [pad_center](https://librosa.org/doc/main/generated/librosa.util.pad_center.html), 
   [expand_to](https://librosa.org/doc/main/generated/librosa.util.expand_to.html), 
   [fix_length](https://librosa.org/doc/main/generated/librosa.util.fix_length.html), 
   [fix_frames](https://librosa.org/doc/main/generated/librosa.util.fix_frames.html), 
   [index_to_slice](https://librosa.org/doc/main/generated/librosa.util.index_to_slice.html), 
   [softmask](https://librosa.org/doc/main/generated/librosa.util.softmask.html), 
   [stack](https://librosa.org/doc/main/generated/librosa.util.stack.html), 
   [sync](https://librosa.org/doc/main/generated/librosa.util.sync.html), 
   [axis_sort](https://librosa.org/doc/main/generated/librosa.util.axis_sort.html), 
   [normalize](https://librosa.org/doc/main/generated/librosa.util.normalize.html), 
   [shear](https://librosa.org/doc/main/generated/librosa.util.shear.html), 
   [sparsify_rows](https://librosa.org/doc/main/generated/librosa.util.sparsify_rows.html), 
   [buf_to_float](https://librosa.org/doc/main/generated/librosa.util.buf_to_float.html), 
   [tiny](https://librosa.org/doc/main/generated/librosa.util.tiny.html)
2. 条件匹配：
   [match_intervals](https://librosa.org/doc/main/generated/librosa.util.match_intervals.html), 
   [match_events](https://librosa.org/doc/main/generated/librosa.util.match_events.html)
3. 统计运算：
   [localmax](https://librosa.org/doc/main/generated/librosa.util.localmax.html), 
   [localmin](https://librosa.org/doc/main/generated/librosa.util.localmin.html), 
   [peak_pick](https://librosa.org/doc/main/generated/librosa.util.peak_pick.html), 
   [nils](https://librosa.org/doc/main/generated/librosa.util.nils.html), 
   [cyclic_gradient](https://librosa.org/doc/main/generated/librosa.util.cyclic_gradient.html), 
   [dtype_c2r](https://librosa.org/doc/main/generated/librosa.util.dtype_c2r.html), 
   [dtype_r2c](https://librosa.org/doc/main/generated/librosa.util.dtype_r2c.html), 
   [count_unique](https://librosa.org/doc/main/generated/librosa.util.count_unique.html), 
   [is_unique](https://librosa.org/doc/main/generated/librosa.util.is_unique.html), 
   [abs2](https://librosa.org/doc/main/generated/librosa.util.abs2.html), 
   [phasor](https://librosa.org/doc/main/generated/librosa.util.phasor.html)
4. 输入评估：
   [valid_audio](https://librosa.org/doc/main/generated/librosa.util.valid_audio.html), 
   [valid_int](https://librosa.org/doc/main/generated/librosa.util.valid_int.html), 
   [valid_intervals](https://librosa.org/doc/main/generated/librosa.util.valid_intervals.html), 
   [is_positive_int](https://librosa.org/doc/main/generated/librosa.util.is_positive_int.html)
5. 本库样例：
   [example](https://librosa.org/doc/main/generated/librosa.util.example.html), 
   [example_info](https://librosa.org/doc/main/generated/librosa.util.example_info.html), 
   [list_examples](https://librosa.org/doc/main/generated/librosa.util.list_examples.html), 
   [find_files](https://librosa.org/doc/main/generated/librosa.util.find_files.html), 
   [cite](https://librosa.org/doc/main/generated/librosa.util.cite.html)

具体使用细节，可自行前往项目 **[官方档案馆查阅](https://librosa.org/doc/latest/index.html)** 。

<br>

Librosa 在音频方面，涵盖了大多数基本的科学分析手段，足够一般工程使用。

但在数据科学方面的高度倾注，也让 Librosa 的 **实时性相对有所降低**（本质为复杂度和精度上升，所伴随算力消耗的升高）。可若此时我们对误差有相对较高的容忍度，且更**希望音频处理足够实时和高效时**，就得采用 Aubio 库来达成这一点了。**Aubio 和 Librosa 的特性相反，是满足这种情况有效补充手段。**

[ref]: References_5.md