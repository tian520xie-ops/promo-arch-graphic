# 架构图工坊 · 宣传型架构图技能包

> 技术标识：`promo-arch-graphic`（技能目录名，系统识别用，不随中文名改动）

## 这是什么

一个生成**宣传型架构图 / 图文卡片**的技能（skill）：用 HTML/CSS 锁定版式、文字与配色（100% 可控），AI 只负责插画素材，Chrome 无头截图出高清成品图；需要时可再重建为**原生可编辑的 PPT 页**。第一张对了，后面张张都对，适合需要反复改文案、批量出系列图的场景。

## 产物形态

每次完整交付 = 1 份 HTML（版式母版，1920×1080）+ 1 张高清 PNG（3840×2160）+（按需）写入 PPT 的一页原生可编辑页。

## 安装

1. 把整个 `promo-arch-graphic` 文件夹拷到技能目录：
   - macOS / Linux：`~/.workbuddy/skills/promo-arch-graphic`
   - Windows：`%USERPROFILE%\.workbuddy\skills\promo-arch-graphic`
2. 重启会话或新开对话，技能即被识别加载。

## 使用方式

对 AI 说"做一张 XX 产品架构图 / 宣传图 / 知识卡片"即可触发。技能内置六步流程：

内容表 → HTML 骨架 → 插画出图打样 → 回填 → 装饰验收 → 出片（+可选 PPT 重建）

### 依赖

- Chrome（无头截图，脚本自动调用）
- Python3 + Pillow（插画底色归一化）
- 可选 PPT 通道：`slidep` CLI（upsert-dsl / lint / screenshot）

无 Chrome/Python 时 HTML 出图仍可手动浏览器截图，PPT 通道不可用。

## 目录结构

```
promo-arch-graphic/
├── SKILL.md                     # 主文档：六步流程 + 实现约束（入口，先读这个）
├── README.md                    # 本说明
├── assets/
│   └── template-1920x1080.html  # 四层架构图骨架模板，改内容即用
├── references/                  # 按需查阅的规范文档
│   ├── content-table.md         # 内容表四列规范、压层规则
│   ├── layout-tokens.md         # 两套风格 token、子卡片四版式、lint 验证流程
│   ├── equal-card-trapezoid.md  # 梯形版式条件、PPT 字号现行标准（第八节）、分宽法
│   ├── illustration.md          # 插画提示词模板、打样、后处理
│   └── pitfalls.md              # 23 条实战踩坑清单（真实翻车实录）
├── samples/                     # 风格与版式参考样图
│   ├── 风格样图/                # 2 风格成品图 + 3 版式截图
│   └── 版式说明/风格与版式速查.md # 2 风格 × 3 版式速查表
└── scripts/
    ├── check_fit.py             # HTML 几何体检（Chrome 实测包住/对齐/裁切）
    ├── check_html.py            # div 嵌套校验
    ├── export_png.sh            # Chrome 无头截图（1x/2x）
    └── normalize_illus.py       # 插画底色归一 + 角部检测
```

## 核心铁律（摘录）

- 版式/文字/装饰 100% 代码写死，绝不给图像模型；插画只出素材
- 大卡片必须完整包住小卡片——跑 check_fit.py 机器检查，不靠肉眼
- 内容红线：不添加原图没有的文字
- PPT 字号用整数磅（正文 10.67px=8pt / 组名 12px=9pt / 卡标题 16px=12pt / 层名 17.33px=13pt），行距 1.2
- 小卡按内容宽度 flex 加权，不默认等宽
- 放不下先调几何（层高/间距/折行），禁止缩字号

## 版本与更新

- 每次更新按语义打 tag：小改进 `v1.0.x`、新增风格/版式 `v1.x.0`、流程大改 `vx.0.0`
- **最新版本内容看 [CHANGELOG.md](CHANGELOG.md)**，历史逐版本都在里面
- 当前：**v1.0.0** —— 2 种已验证风格（浅色手绘卡片风 / 白底极简商务风）+ 3 种已验证版式（等宽网格铺满 / 等大卡片对称梯形 / 行横排底座展开）+ 5 张参考样图 + 速查表
