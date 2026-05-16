---
name: asg-seo-writer-v2
version: 0.1.0
stage: production
status: v0.1
steps: "1-19, 21"
human_gate: true
enforced_rulebooks: [asg-content-constitution, asg-voice-bible, asg-publishing-gate, asg-geo-standards]
reads_libraries: [facts, cases, sources, voices, cluster-map, performance]
emits: [data/runs/<article_id>/02-draft.json, data/runs/<article_id>/04-meta.json]
io_schema: ./io-schema.json
---

# asg-seo-writer-v2

## 1. 作用
v1 asg-seo-writer 直接升级。执行 28 步中 Steps 1-19(写作主体)+ Step 21(Meta)。
保留 v1 验证有效的 80% 逻辑(分段写作、每 H2 单独确认精神、GEO 元素),升级 20%。

## 2. v1 → v2 五项升级(必须全实现,验收点)
1. **三种类型显式分支** — 按 `dossier.article_type` 查 `asg-publishing-gate.md §A`
   取字数/H2/链接/密度。pillar 完整 / share 精简 / response 最精简。**不硬编码参数**。
2. **强制 Library 引用** — 每个 ASG 数据/案例必须带 Library ID 写进
   `output.draft.h2_blocks[].library_refs` 和 envelope.library_refs。无 ID 的
   ASG 数据声明禁止写入(否则 Gate 检查 6 硬 BLOCK)。
3. **Performance 反馈接入** — Step 12 五标题候选附历史高 CTR 模式参考;Step 21
   Meta 附历史高 CTR Meta 模式参考(读 performance,无数据则标 no-history)。
4. **Cluster 自动识别** — Step 8 内链从 `keyword_spec.cluster_relations` /
   Cluster Map 取,不 AI 临时挑。
5. **历史回溯前置** — Step 4-5 差异化从 Cases Library 主动调用真实案例,禁止
   "想象案例"。

## 3. 触发 / 输入
asg-keyword-researcher 之后(主体);asg-editorial-gate PASS 之后再触发一次(Step 21 Meta)。
输入(io-schema.json#input):`keyword_spec` + `filter_report` + Libraries +
Rulebooks + Performance + Cluster Map + `phase`("draft" | "meta")。

## 4. 核心流程(摘要,完整 21 步映射见 workflows/v2-development-plan.md 第 3 章)
- Step 1-3:意图确认 / SERP+PAA(对 Voices Library) / 受众
- Step 4-5:SERP 差距 + ASG 独家差异化(强制 Cases Library)
- Step 6-7:资产清单 / 大纲(每 H2 标注将引用的 Library ID)
- Step 8-10:内链(Cluster Map)/ 外链(Authority Pool)/ ASG 数据(Facts+Cases)
- Step 11-14:分段写作,每 H2 含 GEO Answer Block + Key Takeaway;**Step 14 大纲+标题锁定 → human_gate ②**
- Step 15-19:正文完成 / 4 Schema embed(Article+FAQ+Breadcrumb+类型附加)/ Rank Math / HTML 组装
- Step 21:Meta Description ×3(附 Performance CTR 参考)

## 5. 输出(io-schema.json#output)
`phase=draft`:`draft{ html, rank_math_settings, asset_manifest, h2_blocks[]{heading,library_refs,has_answer_block,has_key_takeaway}, schema_blocks[] }` → 写 dossier.draft,emit 02-draft.json,next=asg-editorial-gate,human_gate=true。
`phase=meta`:`meta_variants[3]` → 写 dossier.publish_package,emit 04-meta.json,next=asg-voice-checker。

## 6. 验收测试(tests/cases.json)
跑通第 44 篇,符合:类型分支正确 / ASG 数据全有 Library ID / 内链来自 Cluster Map /
5 标题含历史 CTR 参考(或 no-history)/ HTML 过 Gate / 4 个 human_gate 正常。
v0.1 用 mock keyword_spec 跑 pillar/response 两条最小路径(见 tests)。
