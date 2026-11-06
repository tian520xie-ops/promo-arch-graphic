# 版式 token 与骨架代码

两套成熟风格，选一套照抄，不要中途改值。

## 一、浅色手绘知识卡片风（宣传向首选）

| 项 | 值 |
| --- | --- |
| 底色 | 米白 `#F8F4ED` |
| 主文字 | 墨蓝 `#1E3A5C` |
| 次文字 | `#5C6E8A` |
| 强调色 ×4 | 橙红 `#E45A2B`、草绿 `#4F8A54`、明黄 `#E9A63C`、天蓝 `#3E6FB0` |
| 字体 | 标题：站酷快乐体 / 得意黑 / 阿里巴巴普惠体 Heavy；正文：思源黑体 |
| 卡片 | 白底 + 1.8px 彩色描边 + 18px 圆角，**无阴影** |
| 字号 | 标题 44 / 层名 18 / 卡标题 17 / 解释 12 / 标签 12–13 |
| 层带 | `rgba(30,58,92,.045)` 极浅墨蓝，四层同色 |

**每张卡一个强调色，用 `style="--c: var(--orange)"` 传参，描边和标签自动跟随。**

## 二、深色科技风（⚠️ 未验证，勿直接使用）

深色风曾尝试两版（浅蓝玻璃拟态、深空电光风）均被用户否决，**目前没有用户认可的深色方案**。上表旧 token 为早期理论值。

**再做深色图时**：先要用户参考图，用像素分析解构（深底占比/主色占比/发光元素分布），打样过目后再批量——不要凭理论值直接写。

| 项 | 值 |
| --- | --- |
| 底色 | 深蓝径向渐变（中心亮、四周暗）+ 64px 细网格 + 2–3 个模糊光晕 |
| 卡片 | `background: rgba(255,255,255,.06)` + `backdrop-filter: blur(20px)` + `1px rgba(255,255,255,.12)` 描边 |
| 文字 | 白 `#FFFFFF` / 次白 `rgba(255,255,255,.65)` |
| 主色 | 单一品牌蓝，只用于层名竖条、图标、关键强调词 |
| 插画 | 深色底必须配黑底发光插画，`mix-blend-mode: screen` |

## 三、1920×1080 网格（可直接用）

```
外边距：左右 68px，上下 52px
层与层之间：12px
左侧层名栏：固定 100–110px 宽，全图统一
卡片间距：12px
卡片内边距：12px 14px
网格：display: grid; grid-template-rows: 110fr 228fr 175fr 232fr; gap: 12px;
```

行高按内容量分配：纯标签层 95–110、卡片层 175–235。**四个 fr 之和不必等于任何值，比例才是关键。**调完一定截图看底部空白——层太高会显得空，太低会挤。

每层列数按卡片数设：`.lb.c6 { grid-template-columns: repeat(6,1fr) }`，依次 c5 / c4。

## 四、卡片三段结构（关键）

所有卡片统一为：**顶部行（左标题 + 右插画）→ 副标题 → 胶囊标签**。

```html
<div class="card pform" style="--c: var(--blue);">
  <div class="ptop">
    <div class="ptxt">
      <div class="head"><span class="bar"></span><b>要素流通平台</b></div>
      <div class="exp">目录与合约驱动合规流通</div>
    </div>
    <img class="illus" src="assets/illus/pipeline-流通管道.png" alt="">
  </div>
  <div class="chips">
    <span class="chip">资源目录</span><span class="chip">数字合约</span>
  </div>
</div>
```

```css
.card { background:#FFF; border:1.8px solid var(--c, var(--blue)); border-radius:18px;
        padding:12px 14px; display:flex; flex-direction:column; position:relative; }
.ptop { display:flex; align-items:flex-start; justify-content:space-between; gap:8px; flex:none; }
.ptxt { flex:1; min-width:0; }
.ptop .illus { position:static; height:88px; width:auto; flex:none; }
.head { display:flex; align-items:center; gap:8px; }
.head .bar { width:5px; height:18px; border-radius:3px; background:var(--c); }
.exp  { font-size:12px; color:#5C6E8A; margin:6px 0 8px; }
.chips{ display:flex; flex-wrap:wrap; gap:7px; }
.chip { font-size:12px; font-weight:600; padding:3px 8px; border-radius:999px;
        background:color-mix(in srgb, var(--c) 12%, #fff);
        border:1.5px solid color-mix(in srgb, var(--c) 45%, #fff); }
```

这一结构一次写好，四层共用：文字永远在左、插画永远在右上、标签永远在下方，**天然不重叠**，避免"标签压素材"的反复返工。

## 五、插画尺寸基准

| 卡片高度 | 插画高度 | 标签处理 |
| --- | --- | --- |
| 200–240px（平台/底座卡） | 88–96px | 下方整行铺开 |
| 130–180px（保障类短卡） | 88px | 下方铺开，行高留足 |
| 60–90px（场景小卡） | 56–64px | 绝对定位右侧居中，文字右留白 62px |

插画统一取右侧、统一 `align-items: flex-start`，四层视觉节奏才一致。

## 六、装饰（内联 SVG，不用 AI）

```html
<!-- 手绘波浪下划线 -->
<svg viewBox="0 0 200 12" height="10">
  <path d="M2 8 Q25 2 50 7 T100 7 T150 7 T198 6"
        stroke="#E45A2B" stroke-width="5" fill="none" stroke-linecap="round"/>
</svg>
```

只加三处：标题关键词下、层名左侧竖条、底部金句星标。卡片内部一律不加。

## 七、系列图一致性（多张同系列架构图时强制执行）

同一系列（同一产品/同一汇报）的多张架构图，用户会逐张对比。以下参数必须在所有图之间**数值完全一致**，第二张图开工前先从第一张的 HTML 里抄：

| 参数 | 基准值（1920×1080） |
| --- | --- |
| 字号层级 | 页标题 44 / 横幅标题 22 / 卡主标题 19 / 副标题 13 / 层徽章 32+15 / 层名 16 / 胶囊 13.5 |
| 插画占位框 | 全部 60×60（`object-fit: contain`），**含横幅卡**——横幅的 img 不在 `.ptop` 里，必须单独写 `.banner .illus` 规则，否则原图尺寸直接渲染压住整页 |
| 卡片 | 描边 1.8px / 圆角 16 / padding 10×14 / 层带 padding 10×12 / 层带圆角 18 |
| 胶囊 | padding 4px 12px / 描边 1.5px color-mix 45% |

**卡片高度**：以"最简卡"为基准（96px），内容多的层按内容加高（含两行胶囊的卡 ≈130–152px，即基准 ×1.3–1.6），**不要让某层拉到基准 2 倍以上**——插画占比会低于 40%，与系列其他图明显不一致。行高用近比例（如 `1fr 1.35fr 1fr 1fr 0.92fr`）而不是让 flex/grid 自动填满。

**转 PPT（1280×720）**：全部参数 ×2/3（插画 40×40、卡标题 13、页标题 29、层徽章 21+10）；每页行高 = HTML 行高 ×2/3 取整，两页行高必须同源换算，不允许一页 70 一页 104。

## 八、子卡片（分组块）排版方式：按内容密度二选一

同系列图之间允许子卡片版式不同——**按每张图的内容密度选择，不要机械沿用上一张**：

| 版式 | 适用条件 | 实现 |
| --- | --- | --- |
| 纵向铺满（一行一个） | 组数少（≤3/卡）、单组叶子多（长句折行 2–4 行） | `.grps { flex-direction: column }`，组块 `display:block`，组名与叶子同行内联 |
| 并排小卡片（规整网格，行内等宽等高） | 组数多（≥4/卡）、单组叶子短（≤5 项一行放下） | `.grps` 用 CSS Grid：`display:grid; grid-template-columns: repeat(N, 1fr); gap:7px; align-content:center`，**每张卡必须明确列数 N（内联指定，不要依赖 auto-fit 猜测）**，组块 `display:flex; flex-direction:column`（组名一行+叶子一行，即"并列+内部纵向"）；个别超长组加 `.wide { grid-column: 1/-1 }` 跨全行 |

| 一行全横向、宽度随内容 | 用户要求"都横向、按内容调宽度"，组数 3–6 且叶子长短差异大 | `.grps.flow { display:flex; align-items:stretch }` + `.grps.flow .grp { flex:1 1 auto }`：flex-basis 取内容宽、grow/shrink 按内容比例分整行，最长的内容最宽（自然结果，不要手动干预）；层高按最高一组算（≈ 组名+最多折行叶子+padding+标题区） |
| 纵向一行一个（单列网格） | 用户明确要求纵向、或该卡组数 5–6 且叶子短 | `grid-template-columns: 1fr`，每行一个小卡片铺满卡宽。**高度代价最大**：5 组纵向约需 320–340px 层高，是并排版的 2 倍多；用在多卡层会让整图放不下，只能用在内容确实多、且其他层有压缩余量的层。压缩顺序：组块 padding 5→3、组间 gap 7→4、层间 gap 22→20、页面上下 padding 36/40→28/30，最后才是加画布预算 |

判断口诀：**"叶子长、组少 → 铺满；叶子短、组多 → 并排；用户点名要纵向 → 单列，先算画布总高放不放得下再动手"**。混合型（某张卡叶多、其余叶少）以整层多数为准，个别超长组块靠 `max-width:100%` 自然折行。

**插画位置两种模式**：① 标题行内（第 1 类内容多的卡）——插画在 `.ptop` 右侧与标题同行；② 右缘垂直居中（组块占满卡身的卡）——`.card{position:relative}` + `.illus{position:absolute; right:14px; top:50%; transform:translateY(-50%)}`，同时给 `.grps` 设 `padding-right: var(--aw)`，**`--aw` 全图必须统一一个值**（= 最宽插画宽 + 右边距 14 + 间距 12，不要逐卡按各自插画宽算——用户会看出组块右边距不一致，说"大卡片内边距有的有有的没有"），让小卡片右侧与插画保持固定距离、不压图。插画宽度不同没关系，右对齐后右边缘自然对齐。

**跨卡等高铁律**：同一层内，不同卡片的小卡片高度必须一致（用户明确要求）。做法：给该层 `.grp` 统一 `min-height` = 该层最高组的实测高度（用 check_fit 的 dump-dom 思路实测，不要估），配 `justify-content: center` 让矮内容垂直居中——留白均匀分布比顶部堆齐好看。

同时注意：层高跟着内容重算，不要沿用上一张的固定层高；空组（组名无叶子）在并排版里是窄卡，在铺满版里是细条。

## 九、PPT 可编辑页验证流程：slidep lint 优先（2026-11-06）

HTML 侧用 check_fit.py；**slide DSL 侧用 `slidep lint`**（机器实测子元素是否越界，比截图肉眼可靠）：

```bash
slidep lint 文件.pptx --dsl-file slides/xx.slide   # diagnostics 空数组 = 过
```

- 写入：`slidep upsert-dsl 文件.pptx --dsl-file slides/xx.slide --page-index N`
- 截图：`slidep screenshot 文件.pptx --page-index N --out /tmp/x.png`
- 改 slide 源文件前先 `cp` 备份；脚本改完验证 `<Box`/`</Box>` 计数相等。
- 几何调整顺序（禁缩字号）：加层高 → 减 padding/gap → 超长组跨行/两行 → 按内容分宽。

## 十、第三套风格：白底极简商务风（2026-11-06 定稿，插画已打样验证）

| 项 | 值 |
| --- | --- |
| 底色 | 纯白 #FFFFFF，无纹理无网格 |
| 层带 | 极浅灰 #F7F8FA，圆角 10px |
| 卡片 | 白底 + 1px 细灰边 #E8EAEF + 圆角 8px + 左侧品牌色短竖条（3px，上下内缩） |
| 主色 | 单一品牌色贯穿（参考为橙 #FF802E），只用于：层名数字、卡片左竖条、胶囊、标题强调词、右上角阶梯装饰 |
| 文字 | 深蓝灰 #3A4A63 / 次级 #8A94A6 |
| 插画 | **单色线稿**（同品牌色 3px 均匀线宽、端点圆角、少量同色系浅色填充），按语义生成，prompt 模板见下 |

**线稿插画 prompt 模板**（打样验证通过，程序化验收：白底>85%、单色线稿、无杂色）：
「极简商务风线性图标插画：[语义主体描述]。单色品牌橙 #FF802E 细线条（3px 均匀线宽），几何简洁，端点圆角，少量浅橙 #FFF1E6 面积填充点缀。纯白干净背景无任何杂色，完全正面平视的扁平二维视角，无阴影无渐变，白皮书架构图卡片配图风格」——品牌色按用户参考图替换；建议 image-to-image 传参考图（fidelity 0.6）。

**适用**：白皮书、方案书、正式商务汇报。与浅色手绘风（宣传向）、深色科技风（大屏向）并列三选一，风格一旦选定整图贯穿不混用。
