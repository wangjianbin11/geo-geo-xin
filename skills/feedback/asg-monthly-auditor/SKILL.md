---
name: asg-monthly-auditor
version: 0.1.0
stage: feedback
status: v0.1
trigger: monthly-manual
human_gate: false
reads_libraries: [topics-pool, asg-published]
emits: data/runs/<task_id>/monthly-audit.json + data/articles-performance-<month>.csv + Obsidian /01-GEO市场分析/MONTH-<month>.md
io_schema: ./io-schema.json
---

# asg-monthly-auditor

## 1. 作用
月度反馈环审计器,对应 28 步流程 Steps 25–27 + 月度 Rulebook 校准。把"已发文章
的真实月度表现"反推为三类动作:逐篇处置、选题池更新、Rulebook 修订建议。
**持续运行的月度校准器**,直接服务北极星①(AI 引用)与②(询盘)。

## 2. 触发
每月 Janson 手动触发("复盘 2026-05")。**旁路 Skill,不在主链**
(`next_skill: null`,`human_gate: false`)。

## 3. 输入(io-schema.json#input)
Janson 提供:`month`(YYYY-MM)+ `articles[]`:每篇 {ref(#44),
primary_kw,topic_id(TOPIC-…)}+ 该月外部表现指标 `metrics`
(clicks / impressions / avg_position / featured_snippet / ai_cited /
inquiries)。这些是 **GSC 风格的外部输入,Skill 绝不编造**。
**指标缺失 → 降级 `basic` 模式**(仅凭 Google 排名 + 人工 AI 核查给方向性
处置),`output.mode="basic"`,envelope `status="flagged"`(可继续但需人看)。

## 4. 核心逻辑
1. **逐篇处置** — 综合该月 metrics 打 `action`:
   - 排名 ≤10 + 有 AI 引用/有询盘 → KEEP
   - 排名 11–30 + 主题仍有价值 → UPGRADE
   - 排名 >30 或主题过时但 cluster 重要 → REWRITE
   - 低意图 / 过时 / 无价值 → KILL
2. **选题池动作** — 对每篇的 `topic_id`:达标转 `active`、观察期保持
   `observed`、淘汰转 `retired`;发现新机会词 → 提案新 `TOPIC-` id
   (`topics_pool_actions[]`)。
3. **Rulebook 修订建议** — 聚合 `rulebook_revision_proposals[]`,字段同
   benchmarker:`{target_doc, section, change, evidence}`,
   `target_doc` ∈ {asg-publishing-gate, asg-geo-standards, asg-voice-bible,
   asg-content-constitution}。进 publishing-gate §C / geo-standards §8
   月度人工合入。
4. **usage_count 回写指令** — 输出 `library_writeback[]`,声明本月各
   `TOPIC-`/`FACT-` 应 +N(批量回写指令,Skill **不**实时改库)。

> **本 Skill 永不自动改 Rulebook,也不自动改 Library。** Rulebook 改动只产
> **提案**,改规则是月度人工动作(镜像 benchmarker §3 第 3 步);
> Library 回写是**指令**,由月度审计人工执行。绝不编造 ASG 编号、客户数据、
> GSC 指标或排名——Janson 提供的指标是输入,缺失即 basic 模式。

## 5. 输出(io-schema.json#output)
`mode`(full|basic)+ `audited[]`(逐篇 action+priority)+
`topics_pool_actions[]` + `rulebook_revision_proposals[]` +
`library_writeback[]` + `csv_path`(常量 `data/articles-performance-<month>.csv`,
镜像 stock-auditor 的 csv_path 常量做法)+ `report_path`。同时生成
`MONTH-<YYYY-MM>.md` 写回 Obsidian /01-GEO市场分析。
`article_id` 覆盖为 `^ASG-MA-[0-9]{4}-[0-9]{2}$`(如 ASG-MA-2026-05)。
status: ok(full)| flagged(basic)。next_skill: null。

## 6. 验收测试(tests/cases.json)
1. full 模式:覆盖全部输入文章,每篇有 action+priority,产出可执行
   rulebook_revision_proposals(指明 §、改成什么、证据)。
2. basic 模式(无 metrics)不报错,mode=basic,envelope status=flagged。
3. article_id 遵循 `^ASG-MA-2026-05$` 覆盖模式。
