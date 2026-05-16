---
name: asg-keyword-researcher
version: 0.1.0
stage: pre-production
status: v0.1
step: 0.5
human_gate: false
reads_libraries: [topics, cluster-map]
emits: data/runs/<article_id>/01-keyword.json
io_schema: ./io-schema.json
---

# asg-keyword-researcher

## ⚠️ 真实形态澄清(必读)
本 Skill **不调研关键词**。真实数据(KD / 月搜索量 / CPC / 意图)**必须由
Janson 从外部工具**(Ahrefs / SEMrush / DataForSEO / Keywords Everywhere)
拉取后作为 input 提供。本 Skill 的作用是把原始数据**加工成 v1 熟悉的关键词
规范文档**,并接入 Cluster 关系。不造数据(宪法 Art.4)。

## 降级模式(degraded mode)— 解决单点脆弱
若 input 未提供外部数据(`external_data` 缺失或不完整):
- 不阻塞流程。生成规范文档,但所有缺失指标标 `"value": null, "estimated": true`。
- output.mode = `"degraded"`,envelope.status = `flagged`。
- 下游 editorial-gate 见 `estimated:true` 的密度类指标时放宽核查并 FLAG,提示
  Janson 补真实数据。
- 这样"没拉数据"不会卡死 Phase B(方案风险 ① 的工程对策)。

## 1. 触发
asg-strategic-filter 输出 GO/MODIFY 后。

## 2. 输入(io-schema.json#input)
- `filter_report`(来自 dossier)
- `external_data`(Janson 提供,可选;缺失则降级):primary_candidates[]
  {term,kd,volume,cpc,intent}、long_tail[]、cooccurrence[]、competitor_urls[]
- 自动读:Topics Pool(去重/状态)、Cluster Map(归属)

## 3. 核心逻辑(6 步)
1. **去重** — 对比 Topics Pool,每词标 already-active / already-retired / observed / new
2. **主词选择** — 从候选选 1 个,依据 KD÷volume 比、cluster 适配、商业意图、与 Filter 推荐类型匹配
3. **密度计划** — 按 `dossier.article_type` 查 `asg-publishing-gate.md §A`(不自行设值)
4. **SEO 放置规则** — Title 前置 / H1 完整 / URL slug / Meta 靠前 / 前 100 字 / ≥2 H2-H3 / 图 Alt / FAQ Schema
5. **GEO 放置规则** — Answer Capsule / FAQ Schema / 对比表 / 步骤列表(依 geo-standards)
6. **Cluster 关系标注** — 是否扩展现有 cluster;推荐 ≥2 已发文章双向内链;推荐 ≥1 未来扩展文章

## 4. 输出(io-schema.json#output)
延续 v1「关键词规范文档」格式 + 新增 cluster_relations 段。写 `dossier.keyword_spec`。
status: ok(有数据)/ flagged(降级)。next_skill: asg-seo-writer-v2。

## 5. 验收测试(tests/cases.json)
1. pillar:"uk dropshipping suppliers"+外部数据 → 规范文档完整,density 取自 §A pillar
2. share:"best dropshipping agents 2026"+外部数据 → 放置规则适配 share
3. cluster 识别:新 UK 关键词 → 归属 UK Cluster,推荐 #37/#42/#43 内链
4. 降级:无 external_data → mode=degraded,status=flagged,指标 estimated:true
