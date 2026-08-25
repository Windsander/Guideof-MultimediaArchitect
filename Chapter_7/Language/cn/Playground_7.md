* [在线演示](Playground_7.md)

## RTMP Chunk 切片模拟器（对应 7.3.3 节）

输入消息长度与 Chunk Size，模拟器按 7.3.3 的规则实时切片：观察 Basic Header 三型与 Message Header 四型（fmt 0/1/2/3）的选择过程、每一片的头部开销，以及切片数量与 Chunk Size 的此消彼长。内置 practice_8 实测参数（ffmpeg 协商 65536B 切片），可一键对照真实推流的封包行为。所有计算均在本地完成，不会上传。

{% urlembed %}
../../Examples/Playground/rtmp_chunk_slicer.html
{% endurlembed %}

[ref]: References_7.md
