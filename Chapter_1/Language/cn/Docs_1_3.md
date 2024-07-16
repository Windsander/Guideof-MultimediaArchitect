<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hex Data Display</title>
    <style>
        .hex-container {
            text-align: center;
        }
        .hex-data {
            display: inline-block;
            text-align: left;
            font-weight: bold;
            font-family: monospace;
            white-space: pre;
        }
    </style>
</head>

# 1.3 声音三要素（Three Elements of Sounds）

**声音三要素（Three Elements of Sounds）** 是人们从 **心理声学（Psychoacoustics）** 角度，对最能影响人对声音本身感官感受的，三个最重要关键参数的归纳。分别是：**音高（Pitch）** 、 **响度（Loudness）** 、 **音色（Timbre）**。

## **预备乐理（声乐）知识**

由于 **声音（Sounds）** 和 **音乐（Musics）** 密不可分。而很多知识，尤其是人的主观认知，总是会和先验艺术有关。为了接下来的工程方面理解，这里先非展开的，提前介绍一些关键 **声乐（艺术）概念** ：

- **纯音（Pure Tone）**，是指单一频率的正弦函数波形声波的声音；
- **音阶（Octave）**，即倍频程，指半频率增减的八度音阶。属于工程声乐学；
- **音程（Interval）**，指两个纯音之间所差的音阶体系下的距离，即度数；
- **音名（Names）**，指音阶不变的前提下，相隔八度的纯音的集合。属于声乐术语（艺术）；
- **音级（Steps）**，指同音名下，从低到高的每个独立纯音的层级。属于声乐术语（艺术）；
- **半音（Semitone）**，指音程为音阶一半的音名，即（八度下的）四度音；
- **音调（Notes）**，全体音名、半音的统称。在欧拉提出 [调性网络](Docs_1_4_1.md) 后，来自于网络拓扑；
- **音分（Cent）**，人为对两个相邻半音间的音程，以 **波长比** 为 $$^{1200}\sqrt{2}$$ ，作 100 非等分；
- **音序（Sequence）**，指顺序排列下，同音级的相邻两个音调的距离；

除了八度音外，还有 **七度音（Heptachord）** 和 **五度音（宫商角徵羽）**，本文从工程特点出发， **统一用八度音（Octave）代指音阶（音阶英文是 Gamut、Scale，易与其它概念造成混淆）**。

理想的音阶是由纯音构成。 **下文若无说明，音阶 均采用理想音阶（Ideal Octave）。** 而 八度指的是在八度音下，同一个音名两个相临音级差异，即音程，为 八度。
八度音阶包含 **7 个音名，5 个半音，8 个音级**，即钢琴键位：

<center>
<figure>
   <img  
      width = "800" height = "100"
      src="../../Pictures/Octave_piano_keybord.png" alt="">
    <figcaption>
      <p>图 1-6 八度音钢琴键盘示意图</p>
   </figcaption>
</figure>
</center>

图中，黑色琴键为半音，白色琴键为纯音（理想）。 **而 C4 则是 A4（440 Hz）对应通用 A440 标准下的基准键（Standard Key），有 C4 为 261.63Hz 标准。** Hz 是频率的单位，我们将在后续介绍。

A440 八度音阶又被称为 **斯图加特音阶（Stuttgart Octave）**，属于 **ISO 16 标准**。根据标准，有音阶频率表如下：

<center>
<table style="width:90%; border-collapse: collapse;">
  <tr style="background-color: #d5d5d5; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; text-align: center; vertical-align: middle;">Steps<br>Names</th>
    <th style="border: 1px solid #ddd; padding: 5px;">0</th>
    <th style="border: 1px solid #ddd; padding: 5px;">1</th>
    <th style="border: 1px solid #ddd; padding: 5px;">2</th>
    <th style="border: 1px solid #ddd; padding: 5px;">3</th>
    <th style="border: 1px solid #ddd; padding: 5px;">4</th>
    <th style="border: 1px solid #ddd; padding: 5px;">5</th>
    <th style="border: 1px solid #ddd; padding: 5px;">6</th>
    <th style="border: 1px solid #ddd; padding: 5px;">7</th>
    <th style="border: 1px solid #ddd; padding: 5px;">8</th>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">C</th>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">16.352<br>(−48)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">32.703<br>(−36)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">65.406<br>(−24)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">130.81<br>(−12)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">261.63<br>(0)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">523.25<br>(+12)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1046.5<br>(+24)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">2093.0<br>(+36)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">4186.0<br>(+48)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">C♯/D♭</th>
    <td style="border: 1px solid #ddd; padding: 5px;">17.324<br>(−47)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">34.648<br>(−35)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">69.296<br>(−23)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">138.59<br>(−11)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">277.18<br>(+1)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">554.37<br>(+13)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1108.7<br>(+25)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">2217.5<br>(+37)</td>
    <td style="border: 1px solid #ddd; padding: 5px;">4434.9<br>(+49)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">D</th>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">18.354<br>(−46)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">36.708<br>(−34)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">73.416<br>(−22)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">146.83<br>(−10)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">293.66<br>(+2)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">587.33<br>(+14)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1174.7<br>(+26)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">2349.3<br>(+38)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">4698.6<br>(+50)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">D♯/E♭</th>
    <td style="border: 1px solid #ddd; padding: 5px;">19.445<br>(−45)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">38.891<br>(−33)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">77.782<br>(−21)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">155.56<br>(−9)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">311.13<br>(+3)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">622.25<br>(+15)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1244.5<br>(+27)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">2489.0<br>(+39)</td>
    <td style="border: 1px solid #ddd; padding: 5px;">4978.0<br>(+51)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">E</th>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">20.602<br>(−44)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">41.203<br>(−32)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">82.407<br>(−20)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">164.81<br>(−8)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">329.63<br>(+4)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">659.26<br>(+16)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1318.5<br>(+28)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">2637.0<br>(+40)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">5274.0<br>(+52)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">F</th>
    <td style="border: 1px solid #ddd; padding: 5px;">21.827<br>(−43)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">43.654<br>(−31)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">87.307<br>(−19)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">174.61<br>(−7)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">349.23<br>(+5)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">698.46<br>(+17)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1396.9<br>(+29)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">2793.8<br>(+41)</td>
    <td style="border: 1px solid #ddd; padding: 5px;">5587.7<br>(+53)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">F♯/G♭</th>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">23.125<br>(−42)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">46.249<br>(−30)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">92.499<br>(−18)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">185.00<br>(−6)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">369.99<br>(+6)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">739.99<br>(+18)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1480.0<br>(+30)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">2960.0<br>(+42)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">5919.9<br>(+54)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">G</th>
    <td style="border: 1px solid #ddd; padding: 5px;">24.500<br>(−41)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">48.999<br>(−29)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">97.999<br>(−17)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">196.00<br>(−5)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">392.00<br>(+7)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">783.99<br>(+19)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1568.0<br>(+31)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">3136.0<br>(+43)</td>
    <td style="border: 1px solid #ddd; padding: 5px;">6271.9<br>(+55)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">G♯/A♭</th>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">25.957<br>(−40)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">51.913<br>(−28)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">103.83<br>(−16)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">207.65<br>(−4)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">415.30<br>(+8)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">830.61<br>(+20)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1661.2<br>(+32)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">3322.4<br>(+44)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">6644.9<br>(+56)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">A</th>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">27.500<br>(−39)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">55.000<br>(−27)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">110.00<br>(−15)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">220.00<br>(−3)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">440.00<br>(+9)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">880.00<br>(+21)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1760.0<br>(+33)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">3520.0<br>(+45)</td>
    <td style="border: 1px solid #ddd; padding: 5px;">7040.0<br>(+57)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">A♯/B♭</th>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">29.135<br>(−38)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">58.270<br>(−26)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">116.54<br>(−14)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">233.08<br>(−2)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">466.16<br>(+10)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">932.33<br>(+22)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1864.7<br>(+34)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">3729.3<br>(+46)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffffff;">7458.6<br>(+58)</td>
  </tr>
  <tr style="background-color: #f2f2f2; text-align: center; vertical-align: middle;">
    <th style="border: 1px solid #ddd; padding: 5px; background-color: #d5d5d5;">B</th>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">30.868<br>(−37)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">61.735<br>(−25)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">123.47<br>(−13)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">246.94<br>(−1)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">493.88<br>(+11)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">987.77<br>(+23)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">1975.5<br>(+35)</td>
    <td style="border: 1px solid #ddd; padding: 5px; background-color: #ffd84b;">3951.1<br>(+47)</td>
    <td style="border: 1px solid #ddd; padding: 5px;">7902.1<br>(+59)</td>
  </tr>
</table>
</center>

<br>

表格横向为音级，纵向为音名（包含半音）。橙色为标准钢琴，所包含的八度音阶。表中数值格式为：

<center>
<b>
【对应频率（Hz）】（距离 C4 基准的（+/-）音序）
</b>
</center>

<br>

简单乐理知识准备就绪。现在，读者肯定存在大量思考，比如：什么或为什么是频率？这和声音三元素又有什么关系？乐理和工程又是怎么关联的？

让我们带着这些知识和疑问，来进入细节。


[ref]: References_1.md