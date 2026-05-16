---
name: asg-strategic-filter
version: 0.1.0
stage: pre-production
status: v0.1
step: 0
human_gate: true
enforced_rulebooks: [asg-content-constitution, asg-publishing-gate, asg-risk-compliance]
reads_libraries: [topics, performance, cluster-map, cases, facts]
emits: data/runs/<article_id>/00-filter.json
io_schema: ./io-schema.json
---

# asg-strategic-filter

## 1. 作用
Janson 提议话题后立即评分,决定该话题进入完整流程(GO)/ 调整后再议(MODIFY)/
直接弃(KILL),并推荐文章类型(pillar/share/response)。终结"所有话题默认升级
Pillar 的盲打"。

## 2. 触发
Janson 说出新话题 / 上传候选清单 / 问"下一篇写什么"。**强制,不可跳过**——
不过 Filter 不能进 keyword-researcher。

## 3. 输入(见 io-schema.json#input)
- 必需:`topic`(一句话或名词短语)。可选:`candidates[]`、`target_market`。
- 自动读:Topics Pool、过去 90 天 Performance、Cluster Map、Cases/Facts(算数据支撑度)、Constitution Art.1/3、Risk-Compliance Sec.5/6。
- **无对话依赖**:给定 input JSON 必须能独立评分。

## 4. 核心逻辑 — 6 维度各 0–10 分

| # | 维度 | 10 分 | 5 分 | 0 分 |
|---|---|---|---|---|
| 1 | 搜索意图清晰度 | 商业意图明确+量≥100 | 信息意图+量50-100 | 模糊/无量 |
| 2 | ASG 服务相关性 | 直接对应核心服务 | 周边话题 | 无关 |
| 3 | 客户旅程位置 | 对应明确阶段 | 跨阶段有主轴 | 不知服务谁 |
| 4 | Cluster 适配性 | 扩展现有/开高潜 cluster | 单点有价值 | 完全孤立 |
| 5 | ASG 独家数据支撑 | ≥5 个 FACT/CASE 可引 | 3–4 个 | <2 个 |
| 6 | 重复风险(反向计分) | 与 43 篇无重叠 | 角度不同 | 已被覆盖 |

总分 = Σ(满分 60)。**decision**:`≥42(70%) → GO` / `30–41 → MODIFY` /
`<30 → KILL`(按 60 分制换算方案的 70/50 阈值)。

**文章类型推荐**(决策树):
- 综合分高 + 维度4 高 + 维度5≥8 + 信息纵深大 → **pillar**
- 比较型意图(best/top/vs,多对象)→ **share**
- 单一信息型问句(what is / how does)→ **response**

**风险标注**:命中 Risk-Compliance(法律/财务/健康/竞品)→ 在 output.risk_flags 列出,human_gate 强提示。

## 5. 输出(见 io-schema.json#output)
固定结构 STRATEGIC FILTER REPORT:scores(6 项)/ total / decision /
recommended_article_type + 理由 / cluster / priority(P0–P2)/ risk_flags /
modify_suggestion(MODIFY 时)/ alternative(KILL 时)。

写 `dossier.filter_report` + `dossier.article_type` + `dossier.cluster`。
status: GO→ok / MODIFY→modify / KILL→blocked。next_skill:
ok|modify → asg-keyword-researcher;blocked → null。human_gate=true。

## 6. 依赖与被依赖
读 Libraries+Rulebooks(上)。输出 → asg-keyword-researcher 输入。

## 7. 验收测试(tests/cases.json)
1. `"private agent dropshipping for jewelry"` → GO + pillar + jewelry cluster
2. `"dropshipping"` → MODIFY + 聚焦建议(太宽泛)
3. `"free dropshipping suppliers"` → KILL + 替代(低意图,Risk Sec 命中)
4. `"uk supplier testing protocol"` → KILL + 引用 #37 已覆盖(重复)

跑通 4 个用例 = 本 Skill v0.1 完成。
