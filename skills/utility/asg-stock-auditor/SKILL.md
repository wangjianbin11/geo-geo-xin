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

## 3. 输入(io-schema.json#input,两种模式 oneOf)
- **article-list 模式**:`articles[]` 每篇 {ref(#37),url,primary_kw};可选
  `gsc_data` / `ahrefs_data` / `ai_citation_manual[]` / `inquiry_attribution[]`。
- **gsc-source 模式(真实阶段 1 路径)**:`{gsc_source, pages_csv, queries_csv?,
  period}` —— 直接喂 GSC 导出,审计真实索引到的页面全集(不需手列文章)。
  实战见 `data/runs/ASG-AUDIT-001/`(98 页真实审计)。
**无 AI 引用维度也能跑**(GSC 无此维度):`ai_cited` 置 null,output.mode 标
`basic`,envelope.status 标 `flagged`,提示 KILL 前需人工核 AI 引用。

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
