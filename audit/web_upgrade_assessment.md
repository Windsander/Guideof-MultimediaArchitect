# 网页体验升级评估报告

> 评估对象：本仓库的 GitBook 静态站点构建与发布链路
> 评估方式：配置逐一核对 + 多版本 Node 实测构建 + HonKit 迁移试构建（均为真实执行，非推断）
> 日期锚点：2026-08

## 一、现状盘点

### 1. 工具链

| 组件 | 版本 | 状态 |
|------|------|------|
| gitbook-cli | 2.3.2 | 已安装（/usr/local，Node 10 下工作正常） |
| GitBook | 3.2.3 | 构建实测通过 |
| Node（默认 PATH） | v24.15.0 | **构建失败**：`graceful-fs` 旧版 polyfill 与现代 Node 不兼容（`TypeError: cb.apply is not a function`） |
| Node（/usr/local/bin） | v10.21.0 | **构建成功**，21.6~22.3s，139 页 / 404 个资源文件 |

结论：工具链本身完好，但**对 Node 版本敏感**（GitBook 3.2.3 为 2018 年代码，需 Node 8~12 区间）。已新增 `.nvmrc`（内容 `10`）为使用 nvm 的环境提供版本锚定。

### 2. book.json 插件核对（23 项声明）

全部 23 个声明插件在 `node_modules/` 中已安装且构建时全部加载成功（构建日志逐一 OK）：
theme-default、highlight、fontsettings、search-pro（替代 lunr/search）、insert-logo、custom-favicon、rss、github、expandable-chapters、chapter-fold、back-to-top-button、tbfed-pagefooter、simple-page-toc、graph、chart、advanced-emoji、splitter、code、katex、sharing-plus（替代 sharing）、alerts、url-embed。

发现的配置问题：

1. **`styles/common.css` 声明但文件缺失** —— book.json `styles` 字段对 website/ebook/pdf/mobi/epub 五种输出均引用该文件，构建产物 HTML 中含对应 `<link>`，形成死链。**已修复**：补齐 `styles/common.css`（占位 + 图片窄屏兜底），构建验证产物含该文件。
2. **`hide-element` 配置为死配置** —— `pluginsConfig.hide-element`（隐藏 `.gitbook-link`）存在，但该插件既未在 `plugins` 声明也未安装。当前不报错但也不生效。未改动：安装需联网引入新依赖，是否保留"隐藏 GitBook 官方链接"的意图应由作者确认。
3. **`publish.sh` 推送目标仓库名为 `Project_M`**（`git push -f git@github.com:Windsander/Project_M.git $1:publish`），与本仓库名不一致。疑为从其他项目复制的脚本或历史仓库名，**仅报告未改动**，请作者确认实际发布目标。

### 3. 发布链路

- `publish.sh`：`gitbook install && gitbook build` → `_book/` 内独立 git init → 强推 publish 分支。链路可用，但存在**非书籍内容混入产物**问题：实测构建会把根目录所有未排除文件（含本次新增的 `audit/` 校对报告目录、本地的 `AGENT_PROMPT.md`、`.bookignore`、`.nvmrc` 等）原样拷入站点。
- **已修复**：新增 `.bookignore`（GitBook 3.2.3 原生支持，已实测验证），排除 `audit`、`.scratch`、`AGENT_PROMPT.md`、`.bookignore`、`.nvmrc`。修复后构建产物中上述内容均不存在。

## 二、升级方案对比

| 维度 | 方案 A：原地增强 | 方案 B：HonKit 迁移 | 方案 C：VitePress 重写 |
|------|------------------|---------------------|------------------------|
| 原理 | 保留 GitBook 3.2.3，修复配置、锚定工具链 | 切换到 GitBook 的社区维护 fork（实测可获取 v6.2.2） | 迁移到现代 Vite 系文档框架 |
| 实测结果 | 构建通过，全部插件正常 | **试构建失败**：插件解析阶段报 `search-pro is not found`（HonKit 的插件解析依赖 package.json 声明，本仓库无 package.json；20+ 个老旧插件需逐一适配验证，search-pro/tbfed-pagefooter/insert-logo/url-embed/graph/chart 等均已多年无维护） | 未实测（工作量大） |
| 风险 | 极低（已验证） | 中（插件生态断代，功能可能回退） | 高（所有插件功能需找替代或重写：KaTeX→vitepress 自带、search-pro→vitepress local search、pagefooter/toc/alerts 等需替代方案） |
| 收益 | 消除死链与发布污染，构建可复现 | 摆脱 Node 版本束缚，获得持续维护 | 现代化构建速度、主题与搜索体验 |
| 工作量 | 已完成 | 1~2 天（建 package.json、逐插件适配、回归测试） | 1~2 周（含 140 页内容与插件语法迁移：urlembed/graph/chart/alerts 等自定义块语法均需改写） |

## 三、结论与建议

**推荐方案 A（原地增强），本轮已完成落地**：

1. 新增 `.bookignore` —— 修复发布产物混入非书籍内容（含校对报告目录外泄风险）
2. 补齐 `styles/common.css` —— 修复 book.json 声明的样式死链
3. 新增 `.nvmrc`（`10`）—— 锚定构建所需 Node 版本，避免现代 Node 下 `graceful-fs` 崩溃

**后续可选（需作者确认，本次未动）**：

- 方案 B（HonKit）：中期值得做，可摆脱 Node 10 依赖；但需先补 `package.json` 并逐插件做兼容性回归，建议单独立项。
- `hide-element` 死配置：确认意图后要么安装启用，要么从 pluginsConfig 移除。
- `publish.sh` 目标仓库名 `Project_M`：确认是否应指向本仓库。
- 发布机/CI 若无法使用 Node 10，可考虑用容器（如 `node:10` 镜像）固化构建环境，作为 HonKit 迁移前的过渡。

## 四、验证记录

| 验证项 | 命令/方式 | 结果 |
|--------|-----------|------|
| 默认 Node 构建 | `gitbook build`（Node v24.15.0） | 失败：graceful-fs `cb.apply` TypeError |
| Node 10 构建 | `PATH=/usr/local/bin:$PATH gitbook build` | 成功，21.6~22.3s，139 页 / 404 资源，23 插件全部加载 |
| 内链转换 | 抽查产物 `Docs_5_1_4.html` | `.md` 内链正确转换为 `.html` |
| 样式死链 | 修复前后对比产物 | 修复后 `styles/common.css` 存在于产物 |
| `.bookignore` 生效 | 对照构建产物目录 | audit/、AGENT_PROMPT.md、`.bookignore`、`.nvmrc` 均不进入产物 |
| HonKit 可用性 | `npx honkit --version` / `honkit build` | v6.2.2 可获取；构建失败于插件解析（search-pro） |
