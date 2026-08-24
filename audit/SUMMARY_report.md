# 总报告：《音视频开发技术：原理与实践》全面校对与网页体验升级

> 工作分支：`proofread/web-upgrade`（基于 `gitbook/v1.0`），共 8 个 commit
> 校对范围：全部 140 篇 md（Chapter_1~5 正文 134 篇 + 根目录文档 6 篇），全量逐字审读
> 分类依据：A 文字错误 / B 术语与一致性 / C 技术性存疑（只报告）/ D 链接与资源 / E 排版格式
> 日期锚点：2026-08

## 一、提交清单（每阶段可独立回退）

| commit | 内容 |
|--------|------|
| `cebc17b` | fix: proofread Chapter_1 typos and formats |
| `bc7d15b` | fix: proofread root docs (README/SUMMARY/GUIDER/AUTHOR/COPYRIGHT) |
| `4224b0a` | fix: proofread Chapter_2 typos and formats |
| `2b79116` | fix: proofread Chapter_3 typos and formats |
| `77f0169` | fix: proofread Chapter_4 typos and formats |
| `3f79165` | fix: proofread Chapter_5 typos and formats |
| `ea4c483` | fix: unify internal links to .md style, add cross-scan report |
| `f97dbf7` | feat: fix site config gaps (.bookignore, styles/common.css, .nvmrc), add web upgrade assessment |

## 二、校对汇总

### 总量统计

| 范围 | 审读篇数 | A | B | C（只报告） | D | E |
|------|----------|-----|-----|--------------|-----|-----|
| Chapter_1（24 篇） | 24/24 | 91 | 35 | 38 | 5 | 20 |
| Chapter_2（32 篇） | 32/32 | 76 | 17 | 36 | 6 | 48 |
| Chapter_3（28 篇） | 28/28 | 103 | 35+68* | 52 | 8 | 17 |
| Chapter_4（43 篇） | 43/43 | 46 | 22 | 28 | 1 | 16 |
| Chapter_5（7 篇） | 7/7 | 42 | 4 | 8 | 2 | 7 |
| 根目录文档（6 篇） | 6/6 | 约 10 | 3 | 2 | 2 | — |
| **合计** | **140/140** | **约 368** | **116+68*** | **164** | **24** | **108** |

\* Chapter_3 另有 68 处"傅里叶→傅立叶"全局统一（replace_all）。

各章明细见 `audit/Chapter_N_proofread_report.md`；跨库检查见 `audit/cross_scan_report.md`。

### 专项工作说明

1. **术语统一尺度**（全书一致执行）：傅立叶（非傅里叶）、噪声（非噪音）、做为→作为、示例（非事例）等；不批量改动"的/地"、不做润色式改写，保留作者双语术语体例。
2. **公式抽验**（Chapter_2~4）：格拉斯曼混合律、RGB↔XYZ 矩阵、CIELAB/LUV 转换、Robertson/McCamy CCT、BT.601 系数、DFT/FFT 推导等抽验**均正确**；发现的问题已进入 C 类清单。
3. **示例代码逐行检查**（Chapter_3~5）：修复真实 bug 共 17+ 处——Chapter_3 的 C/GLSL/JS 示例（未初始化、索引错误等 12 处）；Chapter_4 的 16 个输出块以 IEEE 双精度**逐一复算**，修正 12 处与代码实际运行不符的输出；Chapter_5 的 Python 示例（不存在的 `aubio.cqt` API、未初始化变量、非法字面量 `1.1s` 等 5 处）。
4. **引用编号**：五章 References 共 145 条，编号均无断档；正文引用逐条比对，Chapter_2/3/4 共 8 处编号错位已修复（D 类）；引用与内容不匹配者一律入 C 类。
5. **根目录修复要点**（commit `bc7d15b`）：README「日常工作长中→日常工作中」「音视分析→音视频分析 ×2」「工作工程中→工作过程中」「但确→但却」等；SUMMARY「Uncompressed Encode→Lossy Encode」「Mateplotlib→Matplotlib」「傅里叶→傅立叶」；GUIDER「这几张→这几章」「定义及多→定义极多」「大章→大都」「做为→作为」；AUTHOR「您的您宝贵→您的宝贵」；COPYRIGHT「版权申明→版权声明」「《著作权》法→《著作权法》」；SUMMARY/GUIDER 目录装饰 `oragan→orange` ×3。

## 三、交叉扫描结论（脚本化全量检查 + 人工复核）

- 图片资源：**0 缺失**（含 URL 编码、空格、全角字符文件名均正常）
- 站内链接：修复 4 处 `.html`/`?h=` 旧式内链 → `.md` 体例后，**0 失效**
- SUMMARY 目录：与实际文件**完全一一对应**
- 引用编号：无断档；Chapter_3 [12] 为作者"申请 IEEE 授权中"占位（保留），[26] 与 Chapter_4 [7] 为未引用扩展文献（保留）
- Playground 嵌入资源（`{% urlembed %}` 目标）存在且有效

## 四、站点升级

### 已实施（方案 A 原地增强，commit `f97dbf7`，均经构建实测验证）

1. **`.bookignore`**（新增）：阻止 `audit/`、本地草稿、环境锚定文件混入发布产物（实测 GitBook 3.2.3 原生支持）
2. **`styles/common.css`**（补齐）：修复 book.json 五种输出声明的样式死链
3. **`.nvmrc`**（新增，`10`）：锚定构建 Node 版本——实测现代 Node（v24）下 gitbook-cli 直接崩溃，Node 10.21.0 构建成功（约 22s，139 页 / 404 资源 / 23 插件全部加载）

### 评估结论（详见 `audit/web_upgrade_assessment.md`）

- **推荐方案 A 已落地**；方案 B（HonKit）实测试构建失败于插件解析（`search-pro not found`，仓库无 package.json，20+ 老旧插件需逐一适配），列为中期可选项；方案 C（VitePress）为长期重写方向。**迁移类决策均待作者确认，本次未实施。**

### 体验目标逐项核对

| 目标 | 状态 | 依据 |
|------|------|------|
| 目录导航（折叠/高亮/页内 TOC） | ✅ | expandable-chapters、chapter-fold、simple-page-toc 构建日志全部 OK |
| 全文搜索（中文可搜） | ✅ | search-pro 加载 OK，产物含 `search_plus_index.json` 索引 |
| 阅读体验（公式/代码） | ✅ | katex、highlight、code 插件加载 OK；公式抽验无误 |
| 移动端（小屏/图片自适应） | ✅ | theme-default 响应式 + splitter；common.css 补 `img{max-width:100%}` 兜底 |
| 图片无裂图 | ✅ | 交叉扫描 0 缺失 |
| 构建无错误 | ✅ | 成功退出；仅 5 条插件旧 API deprecation 警告（既有，非新增） |
| favicon/logo 保留 | ✅ | `Cover/book_favicon.ico`、`book_logo.png` 源文件与产物均在 |
| 加分项："本页最后更新"页脚 | ✅ 已有 | tbfed-pagefooter 已配置 modify_label |
| 加分项：代码复制按钮 | ✅ 已有 | `code` 插件提供 |
| 加分项：暗色模式 / SEO meta | ⬜ 未实施 | theme-default 无暗色主题；属方案 B/C 收益项，待作者决策 |

说明：以上以构建产物与插件加载日志为依据，未做浏览器端逐页人工目检；如需可视化回归，可在选定最终方案后补做。

## 五、C 类待确认汇总（共 164 项，均未改动原文）

各章 C 类明细（含原文摘录、存疑理由、核查依据、建议改法）见各章报告"待确认清单"。按主题归并的高优先级项：

1. **Chapter_2**（36 项）：个别色度学参数取值与文献归属待作者按原始文献复核
2. **Chapter_3**（52 项）：含矩阵-MCM 小节 `[12]` 引用处"申请 IEEE 授权中"的占位状态待完结
3. **Chapter_4**（28 项）：Softmax 一节输出与代码、公式三方不一致（复算后仍无法三方自洽，未改）
4. **Chapter_5**（8 项）：`numpy.special` 不存在（实为 scipy.special）；NumPy 金融函数 1.18 已移除；pandas `ix` 已废弃；aubio `source.positions` 属性存疑；References_5 [2] 误引医学 PANDAS 论文（应为 McKinney 2010）
5. **根目录**（2 项）：GUIDER 编解码/渲染进阶章节编号与第五章冲突；GUIDER 行首 Tab 段落会被 Markdown 渲染为代码块（需作者确认是否为有意排版）

## 六、遗留建议（不阻塞验收，待作者决策）

1. `Chapter_5/Pictures/parctice_*.png`（4 张）与 `Examples/practice_1_mathetics_libs_using.py` 文件名拼写（parctice/mathetics）：链接当前有效，重命名需 `git mv` 并同步 4+2 处引用
2. `hide-element` 死配置：确认意图后安装启用或移除
3. `publish.sh` 推送目标仓库名 `Project_M` 与本仓库不符，待确认
4. HonKit 迁移立项评估（摆脱 Node 10 依赖）

## 七、验收标准对照

| 标准 | 状态 |
|------|------|
| 全部 140 篇审读完毕 | ✅ 140/140（逐字审读，未抽样跳过） |
| 每章报告齐全 | ✅ `audit/Chapter_1~5_proofread_report.md` + 交叉扫描 + 站点评估 + 本报告 |
| A/B/D/E 类已修复并有记录 | ✅ 约 616 修复点，全部入报告 |
| C 类 100% 带依据与建议改法 | ✅ 164 项，均附核查依据与建议，均未擅改 |
| 站点构建成功 | ✅ Node 10.21.0 实测通过（现代 Node 崩溃已如实记录并给出 `.nvmrc` 锚定） |
| 无裂图、无失效内部链接 | ✅ 交叉扫描双零 |
| 体验目标逐项通过或有说明 | ✅ 见第四节表格 |
| git 历史清晰、报告位于 audit/ | ✅ 8 个 commit，分支 `proofread/web-upgrade` |
