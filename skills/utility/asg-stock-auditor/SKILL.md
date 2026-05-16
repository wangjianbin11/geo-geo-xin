---
name: asg-stock-auditor
version: 0.1.0
stage: utility
status: v0.1
trigger: one-time
human_gate: false
emits: data/runs/<task_id>/audit.json + data/articles-stock-audit.csv
io_schema: ./io-schema.json
---

# asg-stock-auditor

## 1. 作用
**一次性** Skill。审计 43 篇存量文章状态,输出 KEEP/UPGRADE/REWRITE/KILL 决策表。
方案规定:这一步必须在写第 44 篇之前做完——没有它,不知道 v2 在解决什么真实问题。

## 2. 触发
v2 骨架建成后、阶段 1 收尾时,一次性运行。

## 3. 输入(io-schema.json#input)
`articles[]`:每篇 {ref(#37),url,primary_kw}。可选 `gsc_data`(Janson 接 GSC
导出:每篇 clicks/impressions/position)、`ahrefs_data`、`ai_citation_manual[]`
(人工核查:Perplexity/AI Overview 是否引用)、`inquiry_attribution[]`(Janson
标注:哪几篇带来过询盘)。
**无 GSC 也能跑**(基础模式:仅 Google 排名 + 人工 AI 核查),但 output.mode 标 basic。

## 4. 核心逻辑
对每篇综合:当前主词排名、Featured Snippet 状态、AI 引用情况、询盘归因 →
打 `recommendation`(KEEP/UPGRADE/REWRITE/KILL)+ `priority`(P0–P3)+
`cluster`(现有/新建)。整体洞察:TOP5 共性 / BOTTOM5 共性 / 主题分布缺口。

决策启发(v0.1):
- 排名 ≤10 + 有 AI 引用 / 有询盘 → KEEP
- 排名 11–30 + 主题仍有价值 → UPGRADE
- 排名 >30 或主题过时但 cluster 重要 → REWRITE
- 低意图 / 过时年份 / 无价值 → KILL

## 5. 输出(io-schema.json#output)
`mode`(full|basic)+ `audited[]`(逐篇决策)+ `insights{top5_traits,
bottom5_traits, topic_gaps}`。同时写 `data/articles-stock-audit.csv`(CSV)+
本 JSON(MD/CSV 双格式,满足阶段 1 验收)。status: ok。next_skill: null。

## 6. 验收
- 输出覆盖全部输入文章,每篇有 recommendation + priority。
- CSV + JSON 两份齐全(阶段 1 验收要求 CSV+MD/JSON)。
- 无 GSC 时降级 basic 模式不报错。
- 测试样例见 tests/cases.json(3 篇 mock,覆盖 KEEP/UPGRADE/KILL)。
