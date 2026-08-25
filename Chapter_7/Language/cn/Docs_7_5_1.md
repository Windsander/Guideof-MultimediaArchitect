
# 7.5.1 DASH：标准化的另一极（MPEG-DASH & The Standards Track）

## **MPEG 的回应：厂商中立的自适应流**

HLS 问世三年后的 2012 年，MPEG 发布了 ISO/IEC 23009-1——DASH（Dynamic Adaptive Streaming over HTTP）。它常被读作对 Apple 私有路线的标准化回应：同样是 HTTP 分片加 ABR 的骨架，但出身是国际标准，不绑定任何厂商生态。规范本体是付费文档，本书的引述以 DASH 产业论坛的互操作指南（DASH-IF IOP v4.3）为据 [\[12\]][ref]——这个产业联盟的存在本身就很说明问题：标准写得再全，落到实现仍需一份 "怎么才算合规" 的公共约定，这就是 Profile 与 IOP 的意义。

## **MPD：单文件承载全部层级**

HLS 用两级 m3u8 组织索引，DASH 把全部层级装进一份 XML 文档——**MPD（Media Presentation Description）** [\[12\]][ref]：

<center><b>MPD → Period（时段） → AdaptationSet（适配集） → Representation（代表） → Segment（分片）</b></center>

- **Period**：一段连续的时间区间，首个 Period 的 start 属性必填（相对可用时刻的偏移）；多 Period 可拼出广告插入、内容更替的时间线
- **AdaptationSet**：按媒体类型、语言、视角分组的适配集合——一组视频档、一组多语言音轨各占其一，与 HLS 的 EXT-X-MEDIA 编组异曲同工
- **Representation**：一个码率档，相当于 HLS 的一条 Variant Stream，带宽、编码、分辨率属性齐备
- **Segment**：分片本体，挂在 Representation 之下

与 HLS 两级索引的对位一望而知：MPD 单文件 ≈ Master + Media 两级列表之和。单文件换来的是一次请求拿全全局视图，代价是直播场景下文档需要增量更新。

## **分片寻址：模板的艺术**

DASH 分片的 URL 不必逐条罗列，而是交给 **SegmentTemplate** 模板生成：`@media` 属性写下形如 `chunk_$Number$.m4s` 的模板，`$Number$`（分片序号）或 `$Time$`（分片起始时间戳）在请求时代入，`@startNumber` 约定首片序号，`@timescale` 提供时间单位的换算基准 [\[12\]][ref]。

模板之外有一条硬约束值得圈点：**`@duration` 与 `SegmentTimeline` 二者必居其一** [\[12\]][ref]——等长分片用一个 duration 属性一言蔽之；不等长的（比如广告边界、编码器波动）则改用 SegmentTimeline 逐片声明时长。一个模板机制，把 "规则" 与 "枚举" 两种寻址方式统一收编。

直播场景里，MPD 以 `type="dynamic"` 加 `minimumUpdatePeriod` 周期性增量更新，客户端定时重取——与 HLS 的滑动窗口是同一套心跳，只是换了个账本格式。

## **CMAF：两大阵营的合流**

HLS 与 DASH 对峙多年，真正的和解来自分片格式的统一。7.4.3 留下的那个记号——CMAF（Common Media Application Format）——此刻兑现：它以 fMP4 为基础，规定了一套 **两个阵营都能直接消费的分片格式**。一套分片文件，配两份清单（m3u8 与 MPD），即可同时喂饱 HLS 与 DASH 客户端——CDN 缓存从此只需存一份内容，分发成本应声而落。容器层的标准化，再次化解了清单层的路线之争。

## **小结**

DASH 的故事是标准化方法论的故事：单文件 MPD 承载全部层级、模板化分片寻址、Profile 约束互操作。它与 HLS 的技术内核早已同源，差异更多在生态与治理。而下一节的这位主角，选择的应用场景完全不同——它不要秒级的 "直播"，要的是毫秒级的 "对话"。

[ref]: References_7.md
