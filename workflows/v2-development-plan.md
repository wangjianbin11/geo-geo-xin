# ASG Content OS v2 开发方案

- **版本：** v2.0 设计稿
- **目标读者：** Janson（决策） / Claude Code（执行）
- **编写依据：** 现有 21-Step Workflow（43 篇验证） + 李笑来式 13 层架构（可借鉴部分） + 8 条反驳修正
- **编写日期：** 2026 年 5 月

> 说明：本文档由设计会话整理落盘。原始方案中部分对照表来自飞书文档，
> 未能随文本迁移，文中以 `【表格待补：...】` 标注，需在实施阶段补全。

---

## 第 0 章 | 项目背景与目标

### 0.1 现状摘要

ASG Dropshipping 已建立一套运行中的英文内容生产体系。这套体系已经跑通 43 篇文章 + 215 条社交内容（5 平台 × 43 篇）的产出验证，核心组件包括：

- 核心生产 Skills：asg-seo-writer (21-step) + geo-optimizer v1.0
- 平台改编 Skills：LinkedIn / Twitter / Medium / Substack 共 4 个
- 未封装方法论：Facebook Page / Facebook Groups
- 未开发：YouTube / Service Pages / 短视频
- 锚定资产：ASG canonical data + 7 个真实案例库 + Janson voice 规则
- 完整 cluster 构建能力：UK Topical Cluster（#37+#42+#43）已成功验证

### 0.2 现状诊断（基于 43 篇运行经验）

**强项（必须保留）：**

1. 21 步流程的严谨性 + 每个 H2 单独确认机制
2. Janson 第一人称权威声音 + 8 年实战数据锚定
3. GEO 优化思维（Answer Block / Key Takeaway / FAQ Schema）
4. en-GB / en-US 语言纪律 + 市场对应能力
5. Topical Cluster 主动构建意识

**弱项（必须升级）：**

1. 没有反馈环路：43 篇文章后不知道哪几篇 work，哪几篇没动静
2. 没有写前判断层：所有话题默认升级到 Pillar，没有 GO/MODIFY/KILL 决定
3. 资产没有结构化：ASG 数据、案例、外部权威源散落，靠记忆调用
4. 关键词没有动态池：每个关键词都是孤立一次性使用
5. QC 是软约束：Final QC 不是强制 Gate，不合格也能进入下一步
6. 存量没人管：43 篇文章发完就结束，没有维护和升级机制

### 0.3 v2 升级目标

**核心目标：让系统从"盲打高质量内容"升级为"看见自己 + 持续进化"。**

具体到可衡量结果：

【表格待补：v2 可衡量结果目标表（原飞书文档内容）】

### 0.4 v2 不做什么（明确边界）

为避免方案膨胀失控，明确划定不在本期升级范围：

- ❌ YouTube 长视频——投入产出比当前不明，延后
- ❌ 大规模内容自动化（自动爬虫 / 自动抓取）——我们的内容核心价值是 Janson 第一手经验，不需要外部信息源自动化
- ❌ 复杂的 LLM 测试基础设施（fixtures / replay / regression）——这是李笑来体系里的工程化部分，对我们当前规模过度设计
- ❌ 多人协作工作流——按当前 Janson 单人 + AI 协作模式设计，不引入团队角色

✅ 本期只做：能让现有体系"看见自己 + 强制约束 + 复用资产 + 反馈进化"的最小完整改造。

### 0.5 v2.1 演进方向预告（n8n 化设计前置）

> **v2.1 演进方向预告：** v2 所有 Skills 设计时必须保证"接口标准化、输入输出结构化、可独立调用"，目的是 v2 稳定后可平滑迁移到 n8n 工作流，实现批量化文章生产（多话题并行触发、跨 Skill 自动流转、定时调度、Webhook 接入 Obsidian/GitHub）。当前阶段不实现 n8n，但所有 Skill 的输入输出必须使用 JSON 结构化文件，避免硬编码对话依赖。

---

## 第 1 章 | v2 系统整体架构

### 1.1 三层架构图

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ASG Content OS v2 — 三层架构
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┌─────────────────────────────────────────────────┐
│  ① 资产层 (Asset Layer)                          │
│  · 规则文档 (Constitution / Gate / Voice Bible)  │
│  · 知识库 (Facts / Cases / Sources / Voices)     │
│  · 关键词池 (Dynamic Topic Pool)                 │
│  · 反馈数据 (Performance Data)                   │
│         ↑↓ 被引用 / 被更新                        │
├─────────────────────────────────────────────────┤
│  ② 执行层 (Execution Layer)                      │
│  · Pre-Production Skills (写前判断)              │
│      - asg-strategic-filter                     │
│      - asg-keyword-researcher                   │
│  · Production Skills (写作核心)                  │
│      - asg-seo-writer (升级版 21 步)             │
│      - geo-optimizer v1.0                       │
│  · Post-Production Skills (写后审核 + 分发)      │
│      - asg-editorial-gate                       │
│      - asg-voice-checker                        │
│      - 5 个平台适配 Skills                       │
│      - short-video-adapter                      │
│         ↑↓ 调用资产 / 产出内容                    │
├─────────────────────────────────────────────────┤
│  ③ 反馈层 (Feedback Layer)                       │
│  · 性能数据收集 (GSC / Ahrefs / AI 引用)         │
│  · 月度审计 (存量文章状态 + 关键词池更新)         │
│  · 规则迭代 (Constitution / Gate 修订)           │
│         ↑ 反哺资产层                              │
└─────────────────────────────────────────────────┘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.2 三层职责划分

**① 资产层：被引用的对象（静态 + 半静态）**

【表格待补：资产层职责划分表（原飞书文档内容）】

**② 执行层：被触发的 Skills（动态执行）**

按生产阶段分三组：

```
Pre-Production (写前)
  ↓
Production (写作)
  ↓
Post-Production (写后 + 分发)
```

每组 Skills 在不同阶段被触发，强制依赖资产层——这是 v2 最关键的设计：Skills 不再"凭空生成"，必须从资产层调用规则、案例、数据。

**③ 反馈层：让系统看见自己**

```
内容发布 → 数据收集 → 月度审计 → 资产更新 → 下一轮内容
```

这是 v1 完全缺失的环节，也是 v2 最重要的升级。

### 1.3 v1 → v2 核心差异

【表格待补：v1 → v2 核心差异对照表（原飞书文档内容）】

### 1.4 不变的部分（核心保留）

虽然是 v2，但以下核心资产和规则必须 100% 保留：

- ✅ Janson 第一人称权威声音（8 年实战 + 5,000+ stores + 5M+ 订单）
- ✅ ASG canonical data（200 人/4 仓库/0.3% 缺陷率等）
- ✅ 21 步 Workflow 的严谨性精神（每个 H2 单独确认）
- ✅ GEO 优化所有元素（Answer Block / Key Takeaway / Schema）
- ✅ en-GB / en-US 语言纪律
- ✅ 内/外链 4+10 资产准备前置规则
- ✅ Topical Cluster 主动构建意识
- ✅ "不能敷衍"深度标准

这些是 ASG 内容护城河，v2 升级不动这些。v2 升级的是这些资产之外的"系统性能力"。

---

## 第 2 章 | 物理存储分层方案

### 2.1 四层物理存储

```
Layer 1: Claude.ai Skills
  位置: /mnt/skills/user/
  形态: SKILL.md + 资源文件
  内容: 所有可执行 Skills

Layer 2: GitHub Repo (asg-content-os)
  位置: github.com/[您的账号]/asg-content-os
  形态: Git 仓库 (版本控制)
  内容:
    /rulebooks/    规则文档
    /libraries/    知识库
    /workflows/    流程文档
    /templates/    模板
    /skills/       Skills 镜像 (备份)

Layer 3: Claude Project Knowledge
  位置: Claude.ai 项目知识库
  形态: 上传的 .md / .json 文件
  内容: GitHub 仓库的关键文件镜像
  作用: 让 Claude 会话能直接引用

Layer 4: Janson 工作台
  位置: Notion / Obsidian / Google Sheet
  形态: 个人选择
  内容:
    - GSC / Ahrefs 数据收集
    - 客户问题原始记录
    - 月度审计工作底稿
    - 个人灵感笔记
```

### 2.2 数据流向

```
资产更新数据流：
Janson 工作台
   ↓ (月度整理)
GitHub Repo (规则 + 库)
   ↓ (同步)
Claude Project Knowledge
   ↓ (会话引用)
Claude.ai Skills (执行)
   ↓ (产出内容)
[文章 / 社交 / 视频]
   ↓ (发布后)
GSC / 询盘数据
   ↓ (拉到 Janson 工作台)
[闭环]
```

### 2.3 GitHub 仓库结构（关键设计）

> 注：第 11 章对此做了重大修订——拆分为 `asg-content-os`（工程仓库）
> 与 `asg-knowledge-vault`（Obsidian 镜像）两个仓库。以下为初版单仓结构，
> 实际以第 11 章为准。

```
asg-content-os/
├── README.md                          # 项目说明 + 使用指南
├── AGENTS.md                          # Skills 索引 + 调用关系图
├── CHANGELOG.md                       # 版本更新记录
│
├── rulebooks/                         # 规则文档（声明式）
│   ├── asg-content-constitution.md   # 内容宪法（最高约束）
│   ├── asg-voice-bible.md             # Janson 声音规范
│   ├── asg-publishing-gate.md         # 发布门禁清单
│   ├── asg-risk-compliance.md         # 风险与合规
│   └── asg-geo-standards.md           # GEO 优化标准
│
├── libraries/                         # 知识库（被调用的资产）
│   ├── facts/
│   │   ├── asg-canonical-data.md     # 锚定数据
│   │   └── asg-service-capabilities.md
│   ├── cases/
│   │   ├── case-uk-brand.md          # 7 个核心案例
│   │   ├── case-jewelry-brand.md
│   │   ├── case-apparel-brand.md
│   │   ├── case-banking.md
│   │   ├── case-1688-sourcing.md
│   │   ├── case-black-friday.md
│   │   └── case-uk-shipping.md
│   ├── sources/
│   │   ├── authority-pool.md         # 外部权威 URL 池
│   │   └── citation-templates.md
│   ├── voices/
│   │   ├── customer-questions.md     # 客户真实问题
│   │   └── customer-objections.md    # 客户异议
│   └── topics/
│       ├── topic-pool.md             # 动态关键词池
│       ├── cluster-map.md            # Cluster 构建地图
│       └── retired-topics.md         # 已淘汰主题
│
├── workflows/                         # 流程文档
│   ├── content-os-v2-flow.md         # v2 完整流程图
│   ├── 21-step-upgrade-mapping.md    # 21 步升级映射
│   ├── monthly-audit-sop.md          # 月度审计 SOP
│   └── stock-migration-plan.md       # 43 篇存量迁移计划
│
├── skills/                            # Skills 镜像（GitHub 备份）
│   ├── pre-production/
│   │   ├── asg-strategic-filter.skill
│   │   └── asg-keyword-researcher.skill
│   ├── production/
│   │   ├── asg-seo-writer-v2.skill   # 升级版
│   │   └── geo-optimizer.skill
│   └── post-production/
│       ├── asg-editorial-gate.skill
│       ├── asg-voice-checker.skill
│       ├── linkedin-seo-adapter.skill
│       ├── twitter-seo-adapter.skill
│       ├── medium-seo-adapter.skill
│       ├── substack-seo-adapter.skill
│       ├── facebook-page-adapter.skill
│       ├── facebook-groups-adapter.skill
│       └── short-video-adapter.skill
│
├── templates/                         # 模板
│   ├── article-template.html         # WordPress 文章模板
│   ├── brief-template.md             # 文章 Brief 模板
│   └── audit-template.md             # 审计模板
│
└── data/                              # 数据
    ├── articles-stock-audit.csv       # 43 篇存量审计表
    ├── performance-monthly.csv        # 月度表现数据
    └── keyword-tracker.csv            # 关键词追踪
```

### 2.4 各层职责对照

【表格待补：各层职责对照表（原飞书文档内容）】

### 2.5 关键设计原则

- **原则 1：单一真实源（Single Source of Truth）** — GitHub 仓库是规则和库的唯一真实源。Skills 引用的内容，必须通过 Project Knowledge 同步自 GitHub，不允许 Skill 内部硬编码规则。
- **原则 2：执行与定义分离** — Skills 只负责"如何做"（how），规则和库负责"做什么 + 用什么"（what）。Skill 升级时不影响规则和库；规则修订时不需要重写 Skill。
- **原则 3：可追溯性** — 所有规则和库的修改通过 Git commit 追溯。任何"为什么这次和上次写得不一样？"的问题都能在 commit history 里找到答案。
- **原则 4：渐进迁移** — v2 不是一夜替换 v1。先建立 GitHub 仓库 + 最关键的 3 个 Skill，跑通一篇文章验证，再扩展。详见第 8 章优先级规划。

---

## 第 3 章 | 21-Step Workflow 升级映射表

这一章是整个方案最重要的衔接环节。它回答的核心问题是：43 篇验证过的 21 步，每一步在 v2 里怎么改？

### 3.1 总体策略

21 步不被替换，而是按 4 类动作升级：

【表格待补：21 步升级 4 类动作总体策略表（原飞书文档内容）】

### 3.2 完整 21 步升级映射

【表格待补：21-Step Workflow Upgrade Mapping 完整映射表（原飞书文档内容）】

### 3.3 关键解读

**🟢 保留的 7 个步骤（Steps 7, 11, 12, 14, 15-17, 19）：**

这些是 v1 体系中经过 43 篇验证、不需要也不应该动的核心环节：

- 分段写作 + 每 H2 单独确认是 ASG 内容质量护城河
- 资产清单 / 大纲锁定 / 标题确认是流程严谨性骨架
- Rank Math Settings 已成熟稳定

**🟡 增强的 8 个步骤：**

这些步骤本身逻辑正确，但 v1 中信息来源是 AI 临时判断，v2 升级为接入历史数据 / 资产库：

> 例：Step 13 (5 Title Options)
> - v1：AI 凭判断给 5 个候选
> - v2：AI 给 5 个候选 + 历史标题模式 CTR 数据参考（"动词起头的标题平均 CTR 8.2%，问号结尾的 6.1%..."）

**🟠 升级的 6 个步骤：**

这些步骤需要结构性修改但保留核心动作：

> 例：Step 9 (外部权威链接 10 个)
> - v1：AI 临时挑 10 个权威源
> - v2：从 Authority Pool（结构化分类的外部权威库）按主题匹配调用，确保链接质量一致 + 复用率提升

**🔴 重构的 1 个步骤：**

只有 Step 20 是质变升级：

- v1：Final QC Report 是自我检查，AI 自评后给报告，但不阻断流程
- v2：升级为 asg-editorial-gate Skill 强制执行，不合格输出 "❌ BLOCK + 修改清单"，必须修复才能进入 Step 21

**🆕 新增的 8 个步骤：**

【表格待补：8 个新增步骤说明表（原飞书文档内容）】

### 3.4 升级前后对比图

```
v1: 21 步线性流程
─────────────────────────────────────
用户给话题
   ↓
[Step 1-21] 21 步执行
   ↓
发布
[结束]

v2: 28 步循环流程 (升级版)
─────────────────────────────────────
用户提议话题
   ↓
[Step 0] Strategic Filter
   ↓ (GO / MODIFY / KILL)
[Step 0.5] Keyword Researcher
   ↓
[Step 1-21] 升级版核心流程
   ↓
[Step 22] Voice Check
   ↓
[Step 23] Publish 打包
   ↓
[Step 24] 平台分发
   ↓
[Step 25] Performance 写入
   ↓
[Step 26] 30 天后自动检查
   ↓
[Step 27] 月度数据回流
   ↓
[反哺 Step 0] (闭环)
```

### 3.5 升级带来的最大变化

- **v1 时代：** "我们写一篇关于 X 的文章吧"
- **v2 时代：** "Filter 评分 X 拿到 78 分 GO，类型推荐 Pillar，自动匹配到 UK Topical Cluster，从 Cases Library 调用 3 个相关案例，从 Authority Pool 抽取 10 个外链，21 步严谨执行，Editorial Gate 通过，5 平台分发，30 天后自动回报表现。"

**核心差别：v2 让每一次写作都自动接入资产、自动留下数据、自动反哺系统。**

---

## 第 4 章 | v2 完整流程设计（28 步详细版）

### 4.1 完整流程总览

v2 流程总计 28 步，分为 5 个阶段：

```
Phase A | Pre-Production (写前判断)
  Steps 0 - 0.5       共 2 步
Phase B | Production Core (核心写作)
  Steps 1 - 17        共 17 步
Phase C | Quality Control (质量控制)
  Steps 18 - 22       共 5 步
Phase D | Publishing & Distribution (发布与分发)
  Steps 23 - 24       共 2 步
Phase E | Feedback Loop (反馈循环)
  Steps 25 - 27       共 3 步

总计 28 步
跨越约 30-45 天（含 30 天自动表现检查）
单篇文章生产实际人时：3-4 小时
```

### 4.2 28 步完整设计表

【表格待补：28 步完整设计表（原飞书文档内容）】

### 4.3 关键节点解读

**4 个 Janson 强制确认点（不可绕过）：**

```
① Step 0：Filter GO 决定
   → 没有这个，AI 自己说写就写
② Step 14：标题 + 大纲锁定
   → 没有这个，AI 凭直觉跑完全篇
③ Step 20：Editorial Gate 决定
   → 没有这个，质量没有底线
④ Step 24：平台分发逐个确认
   → 没有这个，错误内容会被批量扩散
```

**3 个数据回流闭环：**

```
闭环 ①: Performance → Topic Pool
   高表现关键词推进状态
   低表现关键词降级或淘汰
闭环 ②: Performance → Title/Meta 模式库
   高 CTR 模式累积成新规则
   低 CTR 模式从推荐列表移除
闭环 ③: Editorial Gate 拦截 → Rulebook
   反复出现的拦截原因 → 升级为新规则
   误拦截案例 → 修订规则边界
```

### 4.4 每篇文章的真实时间分布

```
Phase A (Pre-Production):    15-30 分钟
Phase B (Production Core):   2-3 小时
Phase C (Quality Control):   30 分钟
Phase D (Publishing):        30-60 分钟
Phase E (Feedback):          每月集中 1-2 小时
──────────────────────────────────────────
单篇文章 Janson 实际投入: 3-4.5 小时
其中 AI 工作占 ~80%，确认/审查占 ~20%
```

与 v1 对比：v1 单篇耗时也是 3-4 小时，v2 时间持平但产出物从"一篇文章 + 社交"升级为"一篇文章 + 社交 + 短视频 + 反馈数据 + 资产更新"。

---

## 第 5 章 | Skills 开发清单

### 5.1 Skills 总清单（16 个，第 11 章新增 Benchmarker → 17 个）

```
【Pre-Production Skills (写前)】
1. asg-strategic-filter         🆕 新增
2. asg-keyword-researcher       🆕 新增

【Production Skills (写作核心)】
3. asg-seo-writer-v2            🟠 升级 (v1 → v2)
4. geo-optimizer                🟢 保留

【Quality Control Skills (质量控制)】
5. asg-editorial-gate           🆕 新增
6. asg-voice-checker            🆕 新增

【Platform Adapter Skills (平台分发)】
7. linkedin-seo-adapter         🟢 保留
8. twitter-seo-adapter          🟢 保留
9. medium-seo-adapter           🟢 保留
10. substack-seo-adapter        🟢 保留 + 启用 (清积压)
11. facebook-page-adapter       🆕 新增 (从 inline 封装)
12. facebook-groups-adapter     🆕 新增 (从 inline 封装)
13. short-video-adapter         🆕 新增

【Future Expansion (暂不开发)】
14. youtube-longform-adapter    ⏸️ 延后
15. asg-service-page-writer     ⏸️ 延后

【可选辅助 Skills】
16. asg-stock-auditor           🆕 一次性使用 (43 篇审计)

【第 11 章新增】
17. asg-geo-benchmarker         🆕 每周对标校准
```

### 5.2 每个 Skill 的详细规格

#### Skill 1: asg-strategic-filter 🆕

- **作用：** 在文章写作前进行战略筛选，决定 GO/MODIFY/KILL，避免低价值话题进入 21 步流程。
- **输入：** Janson 提议的话题描述；Topic Pool 当前状态；过去 90 天 Performance Data
- **输出：** STRATEGIC FILTER 评分报告（6 项 0-10 分维度：搜索量 vs KD 比值 / 商业意图匹配度 / 客户旅程位置 / Cluster 适配性 / ASG 独家数据支撑度 / 与近期文章重复度）；综合判断 GO(≥70) / MODIFY(50-69) / KILL(<50)；推荐文章类型 + Cluster 归属 + 优先级
- **触发时机：** Step 0 - 任何新话题提议时
- **强制调用：** ✅ YES - 不通过 Filter 不能进入 Step 0.5
- **与现有 Skill 关系：** 在 asg-seo-writer 之前调用；输出作为 Keyword Researcher 输入

#### Skill 2: asg-keyword-researcher 🆕

- **作用：** 对 Filter 通过的话题，把 Janson 从外部工具拉来的原始关键词数据加工成关键词规范文档（**不自己造数据**）。
- **输入：** Filter 通过的话题；Topic Pool 状态；Cluster Map
- **输出：** 关键词规范文档（主关键词 + SEO/GEO 放置规则 + 建议密度 + 语义共现词 + cluster 数据 + 互链建议）
- **触发时机：** Step 0.5 - Filter 通过后
- **强制调用：** ✅ YES - 没有规范文档不能进入 21 步流程
- **与现有 Skill 关系：** 接 Strategic Filter 输出；产出物直接传给 asg-seo-writer-v2 作为 Step 1 输入

#### Skill 3: asg-seo-writer-v2 🟠

- **作用：** v1 asg-seo-writer 升级版，执行 Steps 1-19 的核心写作流程。
- **升级要点（v1 → v2）：** 1) 强制从 Library 调用资产；2) 接入 Performance Data；3) 每个 H2 标注 Library 来源；4) 历史标题/Meta CTR 参考；5) HTML 自动 embed 4 种 Schema；6) 每个 ASG 数据引用含 Library ID
- **输入：** 关键词规范文档；Filter 评分报告；Cases/Facts/Authority/Voices Library；Cluster Map；Performance Data
- **输出：** Steps 1-19 完整产出物；最终 WordPress HTML + Rank Math Settings
- **强制调用：** ✅ YES + 必须搭配 geo-optimizer

#### Skill 4: geo-optimizer 🟢

- **作用：** GEO（生成式引擎优化）约束 + 自检，v1 已稳定，v2 保留。
- **不变：** Answer Capsule / Key Takeaway / FAQ Schema / 表格列表结构化 / 外部权威源每 200-300 字 / 段落规则（2-4 句）
- **v2 微调：** 与 editorial-gate 协同（GEO 自检后必须过 Gate）；与 Voice Checker 协同
- **强制调用：** ✅ YES

#### Skill 5: asg-editorial-gate 🆕（最重要的新 Skill）

- **作用：** Step 20 强制审核 Gate，决定文章是否能进入发布流程。
- **审核维度（10 项硬检查）：** 主词位置 / 主词密度 / 语义共现词 / Schema 4 种 / 内外链 4+10 / ASG 数据≥9 引用 / 每个 H2 有 GEO Block+KT / 段落规则 / 禁用词扫描 / Library 来源标注
- **输出：** ✅ PASS(10/10) → Step 21；⚠️ MODIFY(1-2 项轻微) → 自动修复重过；❌ BLOCK(≥3 项或硬伤) → 返回 Janson 决定
- **强制调用：** ✅ YES - 这是 v2 的核心 Gate

#### Skill 6: asg-voice-checker 🆕

- **作用：** Janson 第一人称声音一致性强制检查。
- **检查维度（5 项）：** 第一人称密度 / 实战锚定语句 / 中性专家化警告 / AI 痕迹扫描 / en-GB·en-US 一致性
- **输出：** PASS / FLAG + 问题段落 + 改写建议
- **触发时机：** Step 22 - Editorial Gate PASS 之后
- **强制调用：** ✅ YES

#### Skills 7-12: 平台适配 Skills

- 7-10. linkedin / twitter / medium / substack：🟢 v1 已稳定，v2 不动结构，增加 Library 引用规范化 + Voice Bible 引用统一
- 11-12. facebook-page / facebook-groups：🆕 把 v1 inline 方法论封装为正式 Skill（facebook-page 投票互动型 500-750 词；facebook-groups 经验教训+清单型 500-650 词，严格合规无 URL/无 DM）

#### Skill 13: short-video-adapter 🆕

- **作用：** 从已完成文章提取 5-10 个 60-90 秒短视频脚本，覆盖 TikTok / Reels / Shorts。
- **输出每个短视频包含：** Hook 段(前 3 秒) / 主体段(30-60 秒) / CTA 段 / 字幕(含 SEO) / 拍摄建议 / 三平台适配版本
- **强制调用：** 按 Janson 配置（推荐每篇至少 3 个短视频）

#### Skill 14-15: 延后的 Skills

- ⏸️ youtube-longform-adapter — 待短视频跑通 3 个月后再启动
- ⏸️ asg-service-page-writer — 等 v2 主流程稳定 3-6 个月后再做

#### Skill 16: asg-stock-auditor 🆕（一次性）

- **作用：** 一次性使用 - 43 篇存量文章状态审计。
- **输出：** 43 篇存量审计表（CSV/MD），每篇标注 SEO 排名 / FS 状态 / AI 引用 / 询盘归因 / 升级建议(KEEP/UPGRADE/REWRITE/KILL) / 优先级 / cluster 归属 + 整体洞察
- **强制调用：** ✅ 必须做完，才能开始第 44 篇

### 5.3 Skills 调用关系图

```
Step 0 ━━ asg-strategic-filter
              ↓ (GO 决定)
Step 0.5 ━ asg-keyword-researcher
              ↓ (规范文档)
Step 1-19 ━ asg-seo-writer-v2 + geo-optimizer
              ↓ (HTML + 设置)
Step 20 ━━ asg-editorial-gate
              ↓ (PASS)
Step 21 ━━ asg-seo-writer-v2 (Meta 生成)
              ↓
Step 22 ━━ asg-voice-checker
              ↓ (PASS)
Step 23 ━━ Publish 工程化打包
              ↓
Step 24 ━━ 7 个平台 Skills 并行触发
   ├ linkedin-seo-adapter
   ├ twitter-seo-adapter
   ├ medium-seo-adapter
   ├ substack-seo-adapter
   ├ facebook-page-adapter
   ├ facebook-groups-adapter
   └ short-video-adapter
```

---

## 第 6 章 | 规则文档清单（Rulebooks）

### 6.1 规则文档总清单（5 份，第 11 章新增 Obsidian 规范 → 6 份）

```
1. asg-content-constitution.md    🆕 新增（最高约束）
2. asg-voice-bible.md             🆕 新增
3. asg-publishing-gate.md         🆕 新增
4. asg-risk-compliance.md         🆕 新增
5. asg-geo-standards.md           🟠 升级（v1 散在 geo-optimizer，独立成文档）
6. obsidian-knowledge-base-standards.md  🆕 第 11 章新增

存储位置: /rulebooks/ 目录
版本控制: Git commit
修订频率: 季度（月度可临时修订）
```

### 6.2 每份规则文档的功能边界

#### Rulebook 1: asg-content-constitution.md 🆕（内容宪法，最高约束法，约 1,500-2,000 字）

章节：Article 1 使命与边界 / 2 第一人称权威原则 / 3 内容深度标准 / 4 真实性原则 / 5 客户尊重 / 6 竞品引用 / 7 信息时效 / 8 与商业目标关系。所有 Skills 必须引用，Editorial Gate 直接核查。

#### Rulebook 2: asg-voice-bible.md 🆕（Janson 声音圣经，约 2,500-3,500 字）

章节：人格画像 / 第一人称规则 / 锚定语句模板库 / 句式偏好 / 禁用语句库 / 数据呈现风格 / 案例叙述模式 / 与读者关系 / en-GB·en-US 用法 / 行业术语边界。被 asg-seo-writer-v2 引用 + asg-voice-checker 强制核查。

#### Rulebook 3: asg-publishing-gate.md 🆕（发布门禁清单，约 1,200-1,800 字）

10 个 Gate：SEO 硬指标 / GEO 结构 / Library 引用 / 内外链 / Schema / Voice / 禁用词 / 数据准确性 / 风险合规 / 重复内容。每项标注通过标准 + 失败处理 + 修复模板。asg-editorial-gate 直接执行。

#### Rulebook 4: asg-risk-compliance.md 🆕（风险与合规，约 1,500 字）

章节：竞品名称使用 / 客户案例匿名化 / 数据声明 / 行业声明 / 国家合规(REACH/CPSIA/FTC) / 法律免责 / 知识产权 / 数据隐私(GDPR/CCPA)。涉及法律/财务/健康类话题强制激活。

#### Rulebook 5: asg-geo-standards.md 🟠（GEO 优化标准，约 1,800 字）

章节：Answer Capsule / Key Takeaway / FAQ Schema / 表格设计 / 列表设计 / 段落规则 / 外部权威源密度 / Schema 4 种 / 配图 Alt / 内外链锚文本。被 geo-optimizer + editorial-gate 引用。**由 Benchmarker 每月校准。**

### 6.3 规则文档之间的关系

```
        Constitution (最高约束)
              ↓
        ┌─────┴─────┬─────┬─────┐
        ↓           ↓     ↓     ↓
    Voice Bible  Risk   GEO  Publishing
                Comp.  Std.    Gate
        ↑           ↑     ↑     ↑
        └─────┬─────┴─────┴─────┘
              ↓
        被 Skills 引用

Constitution = 宪法 (最高法)
其他 = 子法 (执行细则)
Publishing Gate = 总验收法
```

---

## 第 7 章 | 知识库清单（Libraries）

> 重要：第 11 章对本章做了根本性修订。Janson 的 Obsidian 已是 16+ 文件夹
> 企业级知识库。v2 不"建 5 个新 Library"，而是"为现有 Obsidian 结构建调用
> 规范 + 同步机制"。本章保留原始 Library 设计作为数据结构参考，实际映射以
> 第 11 章为准。

### 7.1 Library 总清单（原设计 5 个）

```
1. Facts Library            🟠 整理升级 → 对应 Obsidian /00-企业DNA
2. Cases Library            🟠 整理升级 → 对应 Obsidian /09-客户案例库-F&Q
3. Authority Pool           🟠 整理升级 → 对应 Obsidian /11-行业洞察
4. Voices Library           🆕 新增     → 对应 Obsidian /01-销售获客
5. Topics Pool              🆕 新增     → v2 新建（阶段 2 顺带建）
```

### 7.2 每个 Library 的详细规格（数据结构参考）

#### Library 1: Facts Library 🟠 — ASG 锚定数据库

存 ASG canonical data / 服务能力 / QC 数据 / 时效 / 网络 / 经验数据。每个数据点标注引用 ID（FACT-001...）+ 最后更新时间 + 来源 + 适用文章类型。AI 引用必须含 FACT ID。不公开：单个供应商名单 / 单笔订单金额 / 单个客户详情。

#### Library 2: Cases Library 🟠 — 真实案例库

7 个核心案例（每个独立 .md）：UK-brand £5,500→£42K / jewelry $8K→$42K / apparel $15K→$80K / banking $15K→$80K / 1688-sourcing $42K→$68K / black-friday $80K→$245K / uk-shipping £1.85→£0.92。每案例含 Case ID / Before/After / Key Numbers / ASG Role / Adaptable Articles / Magnitude。Writer 强制引用 ≥1 个 case，Gate 检查 case ID 标注。

#### Library 3: Authority Pool 🟠 — 外部权威源池

43 篇累积的外部权威源，按 government / industry-bodies / carriers / research / platforms 分类。每源含 URL / Type / Authority Score / Topics / Last Verified / Usage Count / Citation Template。Step 9 强制从此池调用 10 个。

#### Library 4: Voices Library 🆕 — 客户声音库

从真实客户对话累积：问题 / 痛点 / 异议 / 成功反馈（原话脱敏）。含 Frequency / Context / Source / Counter framework / Related article。用于 Step 3(PAA) / Step 5(差异化) / Step 13(FAQ 设计)。不公开客户姓名/邮箱/规模具体数据。

#### Library 5: Topics Pool 🆕 — 动态关键词主题池

5 种状态：observed → candidate → trial → active → retired。含 topic-pool.md + cluster-map.md。用于 Step 0(Filter) / Step 0.5(Keyword) / Step 8(内链) / 月度审计。

### 7.3 Library 与流程的对接关系

```
Step 0   Strategic Filter → Topics Pool + Performance Data
Step 0.5 Keyword Researcher → Topics Pool
Step 3   PAA 提取 → Voices Library + Performance Data
Step 4-5 SERP 差距+差异化 → Cases + Facts Library
Step 8   内部链接 → Cluster Map (Topics Pool)
Step 9   外部权威链接 → Authority Pool
Step 10  ASG 一手数据 → Facts + Cases Library
Step 12  5 Title Options → Performance Data
Step 21  Meta Description → Performance Data
Step 27  月度数据回流 → 更新 Topics Pool + Performance Data
```

### 7.4 不公开数据原则（统一规则）

- ❌ 不公开：客户真实姓名/公司名 / 联系方式 / 单笔订单金额 / ASG 内部定价 / 供应商名单 / 员工信息 / 内部财务
- ✅ 可使用（匿名化后）：客户行业+国家 / 业务规模区间 / 案例 before/after 百分比 / 客户问题原话脱敏 / 行业统计 / ASG 整体运营数据

---

## 第 8 章 | 开发优先级与阶段规划

### 8.1 三阶段路线图

```
阶段 1：地基（4-6 周）
  目标: 把"看不见的资产"挖出来摆好
阶段 2：骨架（6-8 周）
  目标: 把核心 Skills 跑通，第 44 篇用 v2 写
阶段 3：循环（持续）
  目标: 反馈闭环建立，系统开始进化
```

### 8.2 阶段 1：地基（4-6 周）

**这个阶段一篇新文章都不写。** 做 4 件事，按顺序：

1. **搭 GitHub 仓库** — 按第 2 章目录结构（实际按第 11 章拆双仓）。Claude Code 半天完成。
2. **43 篇存量审计** — 调用 asg-stock-auditor，输入 43 篇 URL + GSC/Ahrefs 数据，输出 KEEP/UPGRADE/REWRITE/KILL 表。**必须在写第 44 篇前做完。** 建议至少接 GSC（免费）。
3. **4 个 Library 沉淀** — Facts（80% 可代做，从 43 篇反向提取）/ Cases（7 个标准化）/ Authority（去重分类）/ Voices（需 Janson 手动从 WhatsApp+Email 捞）。Topics Pool 暂不建。
4. **写 3 份核心规则文档** — constitution / voice-bible / publishing-gate（其余 2 份阶段 2 写）。

**阶段 1 验收：** GitHub 仓库可访问 ✅ / 43 篇审计表完成（CSV+MD）✅ / 4 个 Library ≥v0.1 ✅ / 3 份规则文档 ≥v0.1 ✅

### 8.3 阶段 2：骨架（6-8 周）

5 个 Skills 必须先做，按依赖顺序：

【表格待补：阶段 2 五个核心 Skills 依赖顺序表（原飞书文档内容）】

依赖顺序为：asg-strategic-filter → asg-keyword-researcher → asg-seo-writer-v2 → asg-editorial-gate → asg-voice-checker（第 11 章补充 asg-geo-benchmarker，共 6 个）。

**第 44 篇文章作为验证案例：** 阶段 2 末尾必须用完整 v2 流程（28 步）跑一篇文章，从 Filter 到 Editorial Gate 到 Voice Check 全程走通。

**阶段 2 验收：** 5 个核心 Skills 能独立调用 ✅ / 协同跑通第 44 篇 ✅ / Editorial Gate 至少 BLOCK 过一次 ✅ / 4 个 Library 在写作中被实际调用 ≥20 次 ✅

### 8.4 阶段 3：循环（持续）

1. **平台分发完整化** — 封装 facebook-page/groups + short-video 三个 Skills，Substack 启动批量产出。
2. **Feedback Loop 启动** — 每月一次月度审计 SOP（首次 4-6 小时，跑顺后 2-3 小时）：拉 GSC → 人工核查 AI 引用 → 标注表现 → 更新 Topics Pool → 更新 Cluster Map → 修订 Performance Data → 必要时修订 Rulebook。

### 8.5 时间预估

```
阶段 1 地基:    4-6 周  (并行可以更快)
阶段 2 骨架:    6-8 周
阶段 3 循环:    持续运行
总计完整建成 v2: 约 3-4 个月
"够用版"（阶段 1+2）: 约 10-14 周
```

### 8.6 三种文章类型的处理（重要补充）

Pillar / Share / Response 是完全不同的产品：

- **Pillar（顶梁柱型）：** 3,000-5,000 字 / 6-7 个 H2 / cluster 中心 / Library 调用密度最高（≥9 ASG 数据 + ≥10 外链 + ≥4 内链）/ 3-4 小时 / 完整 28 步 / 长视频+完整 5 平台
- **Share（分享型）：** 2,000-3,000 字 / 清单排名结构 / 比较型意图 / 中等密度 / 2-3 小时 / 25 步 / 短视频+Twitter thread
- **Response（回答型）：** 1,200-2,000 字 / 直接回答结构 / 信息型意图 / 较低密度 / 1.5-2 小时 / 22 步 / 短视频+FAQ Schema

Filter 输出必须明确推荐三种之一，asg-strategic-filter 必须内置三种类型决策树。

---

## 第 9 章 | 每个 Skill / 文档的开发规格

### 9.1 开发规格统一模板（8 部分）

1. 身份（名称/版本/阶段） 2. 作用（一句话） 3. 触发条件 4. 输入 5. 核心逻辑 6. 输出 7. 依赖 8. 验收标准

### 9.2 Skill #1：asg-strategic-filter

- **身份：** v1.0 / 阶段 2（优先级最高）/ `/skills/pre-production/asg-strategic-filter.skill`
- **作用：** Janson 提议话题后立即评分，决定进入流程/调整/弃。
- **触发：** Janson 说出新话题/上传清单/要求"下一篇写什么"，必须立即调用。
- **输入：** 话题描述（必需）；自动调用 Topics Pool / Performance Data / Cluster Map / Constitution + Risk Compliance
- **核心逻辑：** 6 维度各 0-10 分 —— ① 搜索意图清晰度 ② ASG 服务相关性 ③ 客户旅程位置 ④ Cluster 适配性 ⑤ ASG 独家数据支撑 ⑥ 重复风险。加总 ≥70 GO / 50-69 MODIFY / <50 KILL。同时输出 Pillar/Share/Response 推荐。
- **输出：** 固定结构 STRATEGIC FILTER REPORT（评分明细 + 决定 + 文章类型推荐 + Cluster 归属 + 优先级 + 风险标注）。MODIFY 输出调整建议，KILL 输出替代话题。
- **依赖：** constitution(Art 1,3) / risk-compliance(Sec 5,6) / Topics Pool / Performance Data / Cluster Map / Cases / Facts。输出→keyword-researcher 输入。
- **验收标准（4 个测试用例）：**
  - 用例 1（GO）："private agent dropshipping for jewelry" → GO + Pillar + Jewelry cluster
  - 用例 2（MODIFY）："dropshipping" → MODIFY + 建议聚焦（太宽泛）
  - 用例 3（KILL）："free dropshipping suppliers" → KILL + 替代建议（低意图）
  - 用例 4（重复检测）："uk supplier testing protocol" → KILL + 引用 #37 已覆盖

### 9.3 Skill #2：asg-keyword-researcher

- **身份：** v1.0 / 阶段 2 / `/skills/pre-production/asg-keyword-researcher.skill`
- **⚠️ 重要澄清：** 这个 Skill **不是** "AI 自动调研关键词"。真实关键词数据（KD/搜索量/CPC）必须来自外部工具（Ahrefs / SEMrush / DataForSEO / Keywords Everywhere）。本 Skill 真实作用是把 Janson 从外部工具拉来的原始数据**加工成 v1 熟悉格式的关键词规范文档**。
- **触发：** Filter 输出 GO 后，Janson 完成外部关键词调研后立即调用。
- **输入：** Janson 提供（外部工具拉取）：主关键词候选 1-3 个+数据 / 长尾 5-15 个+数据 / 语义共现词 6-10 个 / SERP 顶部 5-10 URL（可选）。自动调用 Topics Pool / Cluster Map / Filter 报告。
- **核心逻辑：** ① 关键词去重（对比 Topics Pool）② 主词选择 ③ 密度计划（按文章类型）④ SEO 放置规则 ⑤ GEO 放置规则 ⑥ Cluster 关系标注
- **输出：** 与 v1 熟悉的"关键词规范文档"完全一致格式 + 新增【Cluster 关系标注】段
- **依赖：** Topics Pool / Cluster Map / Filter 报告。输出→asg-seo-writer-v2 Step 1 输入。
- **验收标准（3 个测试用例）：**
  - 用例 1（Pillar）："uk dropshipping suppliers"+外部数据 → 格式与 v1 #42 规范文档一致
  - 用例 2（Share）："best dropshipping agents 2026"+外部数据 → 主词放置规则适合 Share
  - 用例 3（Cluster 识别）：新 UK 关键词 → 自动识别 UK Cluster，推荐 #37/#42/#43 内链

### 9.4 Skill #3：asg-seo-writer-v2

- **身份：** v2.0（v1 直接升级）/ 阶段 2 / `/skills/production/asg-seo-writer-v2.skill`
- **作用：** 执行 28 步流程中 Steps 1-19 + 21，保留 v1 验证有效 80% 逻辑，升级 20%。
- **v1 → v2 关键升级点（5 项）：**
  1. 三种文章类型显式分支（Pillar 完整 21 步 / Share 精简 18 步 / Response 精简 15 步，各有独立字数/H2/Library 密度/GEO 配置）
  2. 强制 Library 引用（每个 ASG 数据必须标注来源 ID，无 ID → Gate BLOCK）
  3. Performance Data 反馈接入（Step 12 标题 / Step 21 Meta 参考历史高 CTR 模式）
  4. Cluster 自动识别（Step 8 内链自动从 Cluster Map 取）
  5. 历史回溯前置（Step 4-5 从 Cases Library 主动调用，不能想象案例）
- **输入：** keyword-researcher 输出规范文档 / Filter 报告 / 4 Library / 3 规则文档 / Performance Data / Cluster Map
- **输出：** Steps 1-19+21 执行 + WordPress HTML + Rank Math Settings + 3 个 Meta 版本
- **依赖：** geo-optimizer 协同调用 + 所有 Library + 规则文档
- **验收标准：** 跑通第 44 篇，符合：三种类型分支正确 ✅ / ASG 数据有 Library ID ✅ / 内链来自 Cluster Map ✅ / 5 Title 含历史 CTR 参考 ✅ / HTML 过 Gate ✅ / Janson 4 个确认点正常 ✅

### 9.5 Skill #4：asg-editorial-gate

- **身份：** v1.0 / 阶段 2（v2 核心 Gate）/ `/skills/post-production/asg-editorial-gate.skill`
- **作用：** 强制审核 Gate，Step 20 触发。"软自检(v1)" 升级为 "硬阻断(v2)"。
- **触发：** asg-seo-writer-v2 完成 Step 19 后立即触发。
- **输入：** 完整 WordPress HTML / Rank Math Settings / 资产清单 / 文章类型。引用 publishing-gate.md（主依据）+ constitution + voice-bible + geo-standards。
- **核心逻辑 — 10 项硬检查：**
  1. 主词 SEO 位置完整性（Title 前置/H1/URL/Meta/前 100 字/≥2 H2/≥1 Alt）→ 缺则 MODIFY
  2. 主词密度（Pillar 1-1.5% / Share 1-2% / Response 1.5-2%）→ 超 ±0.2% MODIFY / ±0.5% BLOCK
  3. 语义共现词覆盖 100% → 缺 1 MODIFY / 缺 2+ BLOCK
  4. Schema 完整性（Article+FAQPage+BreadcrumbList 必须，Pillar 额外 HowTo/ItemList）→ 缺核心 BLOCK
  5. 内外链数量（Pillar 4+10 / Share 3+8 / Response 2+5）→ 差 1-2 MODIFY / ≥3 BLOCK
  6. ASG 数据 Library ID 标注 → 无 ID **BLOCK（硬伤）**
  7. 每个 H2 结构完整（GEO Block + KT 段 + 表格/列表/案例 + 外部权威源）→ 缺 MODIFY
  8. 段落规则（无 >5 句，平均 2-4 句）→ 超长 MODIFY 自动拆分
  9. 禁用词扫描 → 发现 **BLOCK（硬规则）**
  10. 重复内容核查（与 43 篇相似度 >30%）→ BLOCK
- **输出：** EDITORIAL GATE REPORT。PASS→Step 21 / MODIFY→列清单+自动修复+重过（二次不过→升 BLOCK）/ BLOCK→列原因+返回 Janson（修改/重写/弃稿）
- **验收标准（3 个测试用例）：**
  - 用例 1：第 44 篇开发中 Gate 至少 BLOCK 过一次（证明真在干活）
  - 用例 2：43 篇 TOP 3 重新过 Gate → 全 PASS
  - 用例 3：找一篇有明显问题的 → BLOCK 并指出问题

### 9.6 Skill #5：asg-voice-checker

- **身份：** 阶段 2 / 触发 Step 22（Gate PASS 后）
- **输入：** 完整 HTML + asg-voice-bible.md
- **5 项检查：** ① 第一人称密度 ≥ 阈值 ② 实战锚定语句至少 3 处 ③ 中性专家化警告 ④ AI 痕迹扫描 ⑤ en-GB/en-US 一致性
- **输出：** PASS→Step 23 / FLAG→问题段落+改写建议
- **验收：** 第 44 篇通过，且 43 篇 UK 系列重跑能正确 flag en-US 拼写错误

### 9.7 规则文档 + Library 开发规格模板

- **规则文档模板：** 每章节"声明+示例+反例"三段式 / 规则可独立检测 / 禁用强制项明确"如何检测" / 文档末尾版本历史 / 季度审查+月度临时修订
- **Library 模板：** .md（人工友好）+ .json（机器调用）/ 每条数据有 ID / 有"最后更新时间" / 有"已被引用次数" / Janson 在 Obsidian 草稿→commit→同步 Project Knowledge / Skill 引用必须指定 ID

### 9.8 短视频 / Facebook 等 Skills 暂不展开

阶段 3 才做的 Skills 详细规格等阶段 2 完成、第 44 篇验证通过后再写。现在全部规格化是过度设计。

---

## 第 10 章 | 测试与验收标准

### 10.1 三阶段验收清单

**阶段 1 验收（10 项）：** GitHub 仓库可访问 / 43 篇审计表（CSV+MD）/ 每篇标 KEEP·UPGRADE·REWRITE·KILL / Facts ≥30 数据点 / Cases 7 个标准化 / Authority ≥30 源 / Voices ≥20 条 / constitution v0.1 / voice-bible v0.1 / publishing-gate v0.1

**阶段 2 验收（9 项）：** filter 过 4 用例 / keyword-researcher 过 3 用例 / seo-writer-v2 完成 5 项升级 / editorial-gate 过 3 用例 / voice-checker 过基础测试 / 第 44 篇 v2 全流程跑通 / 第 44 篇 Gate 至少 BLOCK 一次 / 第 44 篇 ASG 数据有 Library ID / 第 44 篇 Janson 4 确认点正常

**阶段 3 验收（5 项）：** 月度审计 SOP 跑通 ≥1 次 / Performance Data ≥30 篇 / Topics Pool 有状态变化 / ≥1 次 Rulebook 因反馈修订 / 短视频 ≥10 个脚本

### 10.2 整体 v2 是否成功的最终判断（6 个月后看 3 个硬指标）

1. **内容质量：** v2 新文章 SEO 表现平均优于 43 篇中位数
2. **系统可持续：** 连续 3 个月每月跑通 Filter→写作→Gate→发布→月度反馈
3. **资产沉淀：** 4 个 Library 每月 ≥10 条新数据，Topics Pool 有状态升降

3 个都成立 = v2 真的活起来了。

### 10.3 早期警告信号（阶段 2 出现必须停下重新评估）

- ⚠️ Editorial Gate 永远 PASS（太宽松，橡皮图章）
- ⚠️ Editorial Gate 永远 BLOCK（太严苛或规则不合理）
- ⚠️ 第 44 篇用 v2 花了 ≥6 小时（流程过度复杂）
- ⚠️ Janson 在 4 确认点都觉得"为什么要确认这个？"（Skill 输出不够好）
- ⚠️ Library ID 经常"找不到对应数据"（Library 不全或没维护）

### 10.4 v2 不会做完美才上线

所有 Skills 和文档初版都是 **v0.1，不是 v1.0**。v0.1 = "能用，不完美"。第 44 篇会暴露所有问题，驱动 v0.2/v0.3 迭代。3-6 个月后才有稳定 v1.0。**否则阶段 2 会被完美主义拖到永远不能上线。**

---

## 第 11 章 | 旧 Skills 迁移 + Obsidian 知识库对接 + GEO 校准设计

### 11.1 旧 Skills 迁移到 Claude Code 项目

**核心判断：12 个旧 Skills 不能原封照搬，必须经过"改造"步骤。**

v1 Skills 设计前提（对话临时输入 / 凭记忆调用 / 对话友好输出）与 v2（文件输入 / 主动读 Library / 结构化文件输出）不同。

**迁移 4 步（每个旧 Skill 都走一遍）：**

1. **导出** — 从 Claude.ai 下载 .skill 源文件 → `/skills/_legacy_v1/`（保留原始备份）
2. **改造分析** — Claude Code 阅读 Skill，输出"改造清单"（哪些对话依赖→文件输入 / 哪些凭记忆→Library 引用 / 哪些对话格式→结构化文件）
3. **改造执行** — 重写为 v2 版本，写入 `/skills/[阶段]/[skill-name].skill`
4. **验证** — 用真实 v1 文章作为输入跑通新 v2 Skill，输出应相似或更好

【表格待补：12 个旧 Skills 具体迁移决策表（原飞书文档内容）】

**迁移工作量估算：** 🟢 小改 4 个 ×30 分=2h / 🟠 改造 2 个 ×4-6h=10h / 🆕 首封装+新开发 6 个 ×4-6h=30h。总计约 40-50 小时（Claude Code 并行可压缩到 1-2 周），是阶段 2 核心工作量。

### 11.2 Obsidian 知识库对接（关键章节）

**核心架构：**

```
Obsidian (Janson 唯一编辑入口)
  /00-企业DNA  /01-销售获客  /01-GEO市场分析
  /02-供应链与服务  /03-品牌与营销  /04-团队管理
  /05-战略复盘  /06-AI-Agent  /07-模板库
  /09-客户案例库-F&Q  /10-竞品情报库  /11-行业洞察
  /ASG_Content  /ip知识库
       ↓ Obsidian Git 插件自动同步 (Ctrl+S = git push)
GitHub Repo: asg-knowledge-vault
       ↓ Claude Code 实时读取
Claude Code Skills (执行时调用)
       ↓
内容产出 (写回 Obsidian /ASG_Content)
```

**决策 1：v2 项目改用 2 个 GitHub 仓库**

- 仓库 1 `asg-content-os`：工程仓库（skills/rulebooks/workflows/templates/data），Janson 几乎不直接编辑，月度几次 commit
- 仓库 2 `asg-knowledge-vault`：Obsidian 库的 GitHub 镜像，天天编辑，一天几十次 commit
- 两者生命周期/编辑者/提交频率不同，混在一起会乱

**决策 2：Obsidian 现有结构 = v2 Library 真实形态**

放弃"建 5 个新 Library"，改为为现有 Obsidian 结构定义"调用语义"。v2 不创造新数据，v2 是"为现有数据建立调用层"。

【表格待补：Obsidian 文件夹 → v2 Library 调用语义映射表（原飞书文档内容）】

**决策 3：新增第 6 份规则文档 `obsidian-knowledge-base-standards.md`**

放在 `asg-content-os/rulebooks/`，规范如何维护和调用 Obsidian 知识库。核心章节：

1. 文件夹角色与命名
2. 笔记命名规范（CASE-[国家]-[行业]-[规模]-[年] / FACT-[域]-[编号] / COMP-[竞品]-[主题]-[日期] / VOICE-[来源]-[日期]）
3. 笔记结构规范（YAML frontmatter + 固定结构）
4. 标签系统（#cluster/UK #type/case #status/active 等）
5. 收录标准（什么值得进库 / 什么不进库）
6. 收集 SOP（每天 5 分 / 每周 30 分 / 每月 2 小时）
7. Claude Code 调用接口（GitHub 仓库 + 标签/frontmatter 筛选 + 引用计数）
8. 同步机制（Obsidian Git 自动 commit 30 分 / push 每次保存）

**实施工作量：** 文档撰写 1 个会话 + Obsidian 结构清理分 3 周（第 1 周标签+命名 / 第 2 周 09 案例库 / 第 3 周 10 竞品库）。优先做 09/10/11 三个核心文件夹。

### 11.3 GEO 同行对标 Skill：asg-geo-benchmarker（核心新增）

- **作用：** 让 v2 "看见"什么样的文章被 AI 引用，反推校准 GEO 规则。**持续运行的校准 Skill，每周触发一次。**
- **触发：** 每周一次 Janson 手动触发"本周对标 5 篇文章"，或关键主词在 Perplexity/AI Overview 引用变化时触发。
- **输入：** Janson 提供 3-5 个目标关键词 + 5-10 个同行文章 URL。自动调用 Obsidian /10-竞品情报库 + ASG 已发文章库。
- **核心逻辑：** ① 对标文章拆解（GEO 结构 / AI 引用证据 / SEO 信号 / Voice 客户价值）② 模式提炼（≥4 篇被引用文章共有结构 = AI 喜欢；ASG 做了但没被引用 = 浪费；同行做了我们没做 = 机会）③ 校准建议（对 GEO 规则文档的修订建议，进入下次月度 Rulebook 修订）
- **输出：** 每周对标报告写入 Obsidian /10-竞品情报库（COMP-2026-W21.md）
- **对系统影响：** asg-geo-standards.md 不再"一次写定"，每月按 Benchmarker 报告修订。这让 v2 真正"活起来"——按 AI 偏好持续进化。
- **验收标准：** ① 连续 4 周输出报告 → 第一份"AI 偏好模式"总结 ② 按对标修订规则，下篇按新规则写，30 天后跟踪引用率提升 ③ /10-竞品情报库累积 ≥20 篇对标笔记

### 11.4 Skill 总数更新

```
阶段 2 必做 (6 个):
  1. asg-strategic-filter
  2. asg-keyword-researcher
  3. asg-seo-writer-v2
  4. asg-editorial-gate
  5. asg-voice-checker
  6. asg-geo-benchmarker  ← 新增

阶段 3 (5 个):
  7. facebook-page-adapter
  8. facebook-groups-adapter
  9. short-video-adapter
  10. (substack 批量启用)
  11. (其他平台精修)

延后 (3 个):
  12. youtube-longform-adapter
  13. asg-service-page-writer
  14. asg-stock-auditor (一次性)

迁移自 v1 (3 个，基本保留):
  15. linkedin-seo-adapter
  16. twitter-seo-adapter
  17. medium-seo-adapter
```

---

## 第 12 章 | Claude Code 项目搭建实操指南

### 12.1 项目搭建分 5 步

1. **本地建项目目录** — `~/Projects/asg-content-os/`（工程仓库）+ `~/Projects/asg-knowledge-vault/`（Obsidian 同步目标）
2. **迁移现有 Obsidian 库** — 已用 Obsidian Git：移动 vault 到 asg-knowledge-vault 并推送私有仓库；未用：安装 Obsidian Git 插件→初始化→推送
3. **建 asg-content-os 仓库** — `git init` + 建目录骨架 + README + commit + `gh repo create asg-content-os --private --source=. --push`
4. **安装 Claude Code 并初始化** — `npm install -g @anthropic-ai/claude-code` → `cd ~/Projects/asg-content-os` → `claude`
5. **把 v2 方案放进项目** — 保存为 `asg-content-os/workflows/v2-development-plan.md`（即本文档）

### 12.2 项目搭建后第一周（Week 1：阶段 1 启动周）

- Day 1：完成 12.1 五步 + 把方案放进项目
- Day 2-3：从 Claude.ai 导出所有 v1 Skills → `/skills/_legacy_v1/` → commit+push
- Day 4-5：建第 6 份规则文档 obsidian-knowledge-base-standards.md，开始为 09 案例库按规范命名（一周做 5-10 个最重要案例）
- Day 6-7：准备 43 篇 URL 清单 + 接入 GSC 拉性能数据 + 准备调用 stock-auditor

**Week 1 验收：** 两个 GitHub 仓库建好 / Obsidian Git 同步正常 / Claude Code 能读项目 / 第 6 份规则文档 v0.1 完成 / 43 篇 URL+性能数据准备好

### 12.3 Claude Code 使用要点

**必须养成的习惯：**

1. 每次干活前让 Claude Code 先读 README.md 和 v2-development-plan.md
2. 任何 Skill 开发都先做规格 → 后写代码
3. 每个 Skill 开发完必须跑 1 个测试用例再 commit
4. 大改动用 feature branch，不直接在 main 改

**避免的反模式：** ❌ "帮我重构整个系统" / ❌ "你看着办" / ❌ 一次改 5 个文件 / ❌ 不读 commit diff 就 push

---

## 第 13 章 | 风险与应对

### 13.1 5 大风险 + 应对

1. **Obsidian 知识库规范化拖延** — 分批做，优先 09/10/11，接受"不完美但够用"v0.1，边用边改
2. **43 篇审计发现大部分没 AI 引用** — 接受是大概率结果（v1 盲打不是你的错），把数据当作 v2 GEO 校准基线
3. **Claude Code 太复杂卡在工具上** — 工具次要架构主要，卡住先用 Claude.ai 把第 6 份规则文档写完
4. **Editorial Gate 太严第 44 篇反复被 BLOCK** — Gate v0.1 故意放宽 20%，前 3 篇先跑通再逐步收紧
5. **每周对标 Benchmarker 坚持不住** — 每周固定一天，一次只看 3 篇，当作"读行业文章"，漏了不补下周继续

### 13.2 v2 不会发生的事（明确边界）

- ❌ 不会让写文章更快（可能更慢，多了 Filter/Gate/Voice Check）
- ❌ 不会立刻让 SEO 大幅提升（SEO 滞后，至少 3 个月）
- ❌ 不会自动产生 AI 引用（Benchmarker 是校准工具）
- ❌ 不会让 Janson 工作量减少（更结构化但单篇时间相似）
- ❌ 不会一次性完成（3-6 个月渐进过程）

### 13.3 v2 会带来的真正改变

- ✅ 每篇文章都"看得见"（Filter 评分+Gate 报告+30 天追踪）
- ✅ 资产持续积累（Obsidian 越用越值钱）
- ✅ 规则持续校准（每月 Benchmarker 反哺）
- ✅ 质量不再"看心情"（Gate 强制阻断有底线）
- ✅ 三种文章类型有效区分
- ✅ Obsidian 知识库 + Claude 写作流真正打通

### 13.4 最终判断

**v2 不是软件项目，是工作方式改革。** 真正价值在"它强迫你每周做对标、每月做反馈、持续维护知识库"这套纪律。3 个月后跑稳定，你拥有的是：① 会自我进化的内容生产系统 ② 实时同步的高质量知识库 ③ 有反馈数据的运营节奏 ④ 别人很难抄走的内容护城河。

---

## 附录：本文档落盘说明

- 本文档由设计会话整理落盘，作为 Claude Code 实施 ASG Content OS v2 的工程依据。
- `【表格待补：...】` 标注处为原飞书文档中的对照表，未随文本迁移，需在对应阶段补全。
- 后续实施严格遵循：先输出 Skill 规格 → Janson 确认 → 才写代码；每个 Skill 开发完跑测试用例；大改动走 feature branch；所有 Skill 输入输出使用 JSON 结构化文件（为 v2.1 n8n 迁移做准备）。
