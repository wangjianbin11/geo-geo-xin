---
doc: obsidian-folder-map
title: ASG Obsidian 知识库文件夹映射(权威人类索引)
status: v0.1
verified: true
source: janson-2026-05-16
last_updated: 2026-05-16
---

# ASG Obsidian 知识库文件夹映射

> 这是 Janson 提供的真实 Obsidian 知识库 `ASG-KB-FULL` 文件夹结构的权威人类索引。
> 机器可读版本见 `libraries/obsidian-folder-map.json`。
> 文件夹名(含中文名)= 真实磁盘路径,逐字复制,**不翻译、不臆造**。

**Vault root:** `/Users/apple/Documents/ASG-知识库/ASG-KB-FULL/`

---

## 2.1 一级文件夹(First-level folders)

| 真实文件夹名 | 代码 | MOC | 用途 | 前缀 | 合规 |
|---|---|---|---|---|---|
| 00-企业DNA | DNA | 00-企业DNA-MOC.md | 公司根基、品牌、使命 | 00- | ✅ |
| 01-销售获客 | SALES | 01-销售获客-MOC.md | 客户画像、获客、话术、邮件 | 01- | ✅ |
| 01-GEO市场分析 | GEO | (无,拟并入 11-行业洞察) | 美欧亚拉美市场分析 | 01- | ⚠ 前缀与 SALES 重复 |
| 02-供应链与服务 | SUPPLY | 02-供应链与服务-MOC.md | QC/物流/订单/付款 | 02- | ✅ |
| 03-品牌与营销 | BRAND | 03-品牌与营销-MOC.md | SEO/社媒/内容/Fiverr | 03- | ✅ |
| 04-团队管理 | TEAM | 04-团队管理-MOC.md | 制度/培训/考核 | 04- | ✅ |
| 05-战略复盘 | STRATEGY | 05-战略复盘-MOC.md | 周复盘/月复盘/决策/项目 | 05- | ✅ |
| 06-AI-Agent | AI | 06-AI-Agent-MOC.md | FAQ/Agent矩阵/Skills | 06- | ✅ |
| 07-模板库 | TEMPLATE | 07-模板库-MOC.md | 标准化文档模板 | 07- | ✅ |
| 09-客户案例库-F&Q | CASE | 09-客户案例库-MOC.md | 252个FAQ+客户案例 | 09- | ⚠ 含 `&`,应为 09-客户案例库-FAQ |
| 10-竞品情报库 | COMPETE | 10-竞品情报库-MOC.md | 竞品档案+对比 | 10- | ✅ |
| 11-行业洞察 | INSIGHT | 11-行业洞察-MOC.md | 行业图谱/趋势/政策 | 11- | ✅ |
| 99-Inbox | INBOX | 99-Inbox-MOC.md | 快速捕获临时区 | 99- | ✅ |
| 内容输出库 | CONTENT | (无) | 多平台内容分发 | (无) | ⚠ 无数字前缀 |
| ip知识库 | IP | (无) | Janson个人品牌知识体系(独立) | (无) | ⚠ 无前缀(刻意保持独立) |
| asg 的销售教程 | TRAINING | (无) | 销售培训材料 | (无) | ⚠ 含空格 + 无前缀 |
| 西哥有绝招_副本 | XI_GE | (无) | 内容素材(待整理) | (无) | ⚠ 含 `副本` + 无前缀 |
| ASG_Content | ASG_C | (无) | 空目录(待定用途) | (无) | ⚠ 英文 + 无前缀,空目录 |

---

## 2.2 二级文件夹(Second-level folders,纯中文、无前缀)

**SALES — 01-销售获客/**
- 获客系统 → `SALES.ACQUIRE`
- 客户画像 → `SALES.PERSONA`(7 类客户画像)
- 邮件模板 → `SALES.EMAIL`
- 话术库 → `SALES.SCRIPT`

**SUPPLY — 02-供应链与服务/**
- QC质检 → `SUPPLY.QC`
- 付款结算 → `SUPPLY.PAYMENT`
- 物流方案 → `SUPPLY.LOGISTICS`
- 订单处理 → `SUPPLY.ORDER`

**BRAND — 03-品牌与营销/**
- Fiverr推广 → `BRAND.FIVERR`
- 内容策略 → `BRAND.CONTENT`
- SEO → `BRAND.SEO`
- 社交媒体 → `BRAND.SOCIAL`
- 内容素材 → `BRAND.ASSETS`

**TEAM — 04-团队管理/**
- 绩效考核 → `TEAM.KPI`
- 制度流程 → `TEAM.POLICY`
- 市场专项 → `TEAM.MARKET`
- 培训体系 → `TEAM.TRAIN`

**STRATEGY — 05-战略复盘/**
- 决策记录 → `STRATEGY.DECISION`
- 周复盘 → `STRATEGY.WEEKLY`
- 月复盘 → `STRATEGY.MONTHLY`
- 项目档案 → `STRATEGY.PROJECT`

**AI — 06-AI-Agent/**
- Skills配置 → `AI.SKILLS`
- FAQ知识源 → `AI.FAQ`
- Agent矩阵 → `AI.MATRIX`

**CONTENT — 内容输出库/**
- 推特 → `CONTENT.TWITTER`
- substack → `CONTENT.SUBSTACK`
- medium → `CONTENT.MEDIUM`
- YouTube → `CONTENT.YOUTUBE`
- 领英 → `CONTENT.LINKEDIN`
- seo 谷歌文章 → `CONTENT.SEO`
- Facebook → `CONTENT.FACEBOOK`

**IP — ip知识库/**
- 01-AI自带知识库（基础认知层） → `IP.BASE`
- 02-行业知识库（专业垂类层） → `IP.INDUSTRY`
- 03-IP知识库（个人品牌层） → `IP.BRAND`
- 04-联网知识库（实时信息层） → `IP.REALTIME`

---

## 2.3 根目录散落文件待迁移(Root-loose files needing relocation)

| 当前文件 | 目标位置 / 重命名 | 状态 |
|---|---|---|
| HOME.md | 保留根目录 | ✅ |
| 00-任务一-全库结构诊断与升级方案.md | → 00-企业DNA/ | ✅ |
| ASG销售流程的sop...(1)_副本.docx | → 01-销售获客/，重命名 `ASG销售流程SOP-七大节点执行策略指南.md` | ⚠ 待转换 |
| ...(1)_副本2.docx | → ...-v2.md | ⚠ 待转换 |
| dropshipping 行业的知识库 (1).md | → 11-行业洞察/`Dropshipping行业知识库.md` | ⚠ |
| 行业dropshipping 补充 (2).md | → 11-行业洞察/`Dropshipping行业知识补充.md` | ⚠ |
| 旧网站的知识库更新.md | → 00-企业DNA/`旧网站知识库迁移记录.md` | ⚠ |
| 未命名 2.base | → 07-模板库/ 或删除 | ⚠ 待确认 |

---

## 2.4 命名规则与已知违规(Naming rules & known violations)

**命名规则**
- 文件夹 = `{两位数字}-{中文名}`。
- 编号区间:`00` 核心 / `01-06` 业务 / `07` 工具 / `08` 预留(审计仪表盘待建) /
  `09-11` 智库 / `99` 临时。
- 一级文件夹必须有数字前缀;二级文件夹纯中文、无前缀。
- 不得有空格(用 `-`);不得有特殊字符(`&` → `and`,去掉括号)。
- 文件 = `{类别前缀}-{简明标题}.md`。
- MOC = `{文件夹名}-MOC.md`。
- 禁止 `副本/初版`(改用 `v2/v3`)。
- 模板文件前缀 `模板-`。

**已知违规(known violations)**
- `09-客户案例库-F&Q` 含 `&` → 应为 `09-客户案例库-FAQ`。
- `内容输出库` 无前缀 → `12-内容输出库` 或保留现状。
- `ip知识库` 保持独立(刻意例外)。
- `asg 的销售教程` 含空格 + 无前缀。
- `西哥有绝招_副本` 含 `副本`。
- `ASG_Content` 英文 + 无前缀(空目录)。
- `01-GEO市场分析` 与 `01-销售获客` 前缀重复(拟并入 `11-行业洞察`)。

---

## 2.5 路径构造与代码→文件夹速查(Path construction & quick lookup)

**路径构造:** `{vault_root}/{一级真实文件夹名}/{二级纯中文名}/{类别前缀}-{标题}.md`
例:`/Users/apple/Documents/ASG-知识库/ASG-KB-FULL/01-销售获客/客户画像/01-...md`

**一级代码 → 真实文件夹速查**

| 代码 | 真实文件夹 |
|---|---|
| DNA | 00-企业DNA |
| SALES | 01-销售获客 |
| GEO | 01-GEO市场分析 |
| SUPPLY | 02-供应链与服务 |
| BRAND | 03-品牌与营销 |
| TEAM | 04-团队管理 |
| STRATEGY | 05-战略复盘 |
| AI | 06-AI-Agent |
| TEMPLATE | 07-模板库 |
| CASE | 09-客户案例库-F&Q |
| COMPETE | 10-竞品情报库 |
| INSIGHT | 11-行业洞察 |
| INBOX | 99-Inbox |
| CONTENT | 内容输出库 |
| IP | ip知识库 |
| TRAINING | asg 的销售教程 |
| XI_GE | 西哥有绝招_副本 |
| ASG_C | ASG_Content |

---

> 地图维护信息 — last updated 2026-05-15 / next review 2026-08-15 / maintainer Knowledge Manager
