---
name: asg-geo-benchmarker
version: 0.1.0
stage: feedback
status: v0.1
trigger: weekly-manual
human_gate: false
reads_libraries: [competitor-intel, asg-published]
emits: data/runs/<task_id>/benchmark.json + Obsidian /10-竞品情报库/COMP-<week>.md
io_schema: ./io-schema.json
---

# asg-geo-benchmarker

## 1. 作用
让 v2 "看见"什么样的文章被 AI 引用,反推校准 GEO 规则。**持续运行的校准器**,
每周触发一次,产出对 `asg-geo-standards.md` / `asg-publishing-gate.md` 的修订建议。
直接服务于北极星①(AI 引用)。

## 2. 触发
每周 Janson 手动触发("本周对标 N 篇");或关键主词在 Perplexity/AI Overview
引用变化时触发。**旁路 Skill,不在主链。**

## 3. 输入(io-schema.json#input)
Janson 提供:`target_keywords[3-5]` + `competitor_urls[5-10]` +
`ai_citation_evidence[]`(人工核查截图/记录:该 URL 是否被 Perplexity/AI
Overview 引用、引哪段)。自动读 Obsidian /10-竞品情报库历史 + ASG 已发文章。

## 4. 核心逻辑(3 步)
1. **拆解** — 对每个 competitor_url 结构化拆:GEO 结构(Answer Capsule / KT / FAQ
   Schema / 表列频率 / 段长分布)、AI 引用证据、SEO 信号、Voice/客户价值。
2. **模式提炼** — 横向对比:出现在 ≥4 篇被引用文 = AI 偏好;ASG 做了但没被引
   = 浪费;同行做了我们没做 = 机会。
3. **校准建议** — 输出对 geo-standards / publishing-gate 的可执行修订条目,进入
   下次月度 Rulebook 修订(不自动改规则,只产建议;改规则是月度人工动作)。

## 5. 输出(io-schema.json#output)
`teardowns[]` + `patterns{ai_loved[], asg_wasted[], opportunities[]}` +
`rulebook_revision_proposals[]`。同时生成 `COMP-<YYYY-Www>.md` 写回 Obsidian
/10-竞品情报库(human-readable 周报)。status: ok。next_skill: null。

## 6. 验收测试(tests/cases.json,plan §11.3)
1. 连续 4 周输出周报 → 首份"AI 偏好模式"总结(累积性,标记 week 序号)
2. 产出 rulebook_revision_proposals 且字段可执行(指明改哪个 §、改成什么)
3. /10-竞品情报库 结构能累积 ≥20 篇 COMP 笔记(命名 COMP-YYYY-Www)
