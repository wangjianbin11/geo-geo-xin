# 集成自检 — 阶段 1+2 核心骨架 (v0.1)

> ⚠️ **SUPERSEDED 2026-05-16。** 本文件记录的是**骨架期**自检
> (7 Skill / 3 规则 / 4 库 / 20 JSON / 260 检查),已被后续多轮真实数据集成
> 大幅超越。**当前权威状态以 `workflows/framework-review-2026-05-16.md` 为准**
> (真实数:12 Skill / 6 规则 / 5 库 + 71 条 Verified Data / validator 393 全绿 /
> 真实 GSC + 关键词语料 + ASG-AUDIT-001 真实审计)。下方内容保留作历史快照,
> **不要据此判断当前完成度**——看 framework-review 的 §5 完成度清单。

> (历史)这份文档把骨架对照方案的阶段 1 / 阶段 2 验收清单逐条核对。给 Janson 总审用。

## 1. 阶段 1 验收清单(方案 §10.1)对照

| 验收项 | 状态 | 落点 |
|---|---|---|
| GitHub 仓库可访问,目录结构 | ✅ | 本仓库 + 已推送分支 |
| 43 篇审计表(CSV+MD/JSON) | ⚙️ 工具就绪 | asg-stock-auditor 输出 CSV+JSON;**需 Janson 提供 43 篇 URL + GSC 才能产出数据** |
| 每篇标 KEEP/UPGRADE/REWRITE/KILL | ⚙️ 工具就绪 | io-schema enum 已定 |
| Facts ≥30 数据点 | 🌱 13 个种子 | 方案明确陈述的全部已入;Janson 补到 ≥30 并核验 |
| Cases 7 个标准化 | ✅ 结构 / 🌱 数据 | 7 个 before/after 已入,细节待 Janson 补 |
| Authority ≥30 源 | 🌱 7 个种子 | 类目结构就绪;Janson 从 Obsidian 同步去重补全 |
| Voices ≥20 条 | 🌱 结构 | 无法 AI 代填,Janson 从真实对话录入 |
| constitution v0.1 | ✅ | rulebooks/asg-content-constitution.md |
| voice-bible v0.1 | ✅ | rulebooks/asg-voice-bible.md |
| publishing-gate v0.1 | ✅ | rulebooks/asg-publishing-gate.md |

✅ = 工程完成 / ⚙️ = 工具完成待真实输入 / 🌱 = 结构完成待 Janson 数据。
**纯工程部分 100% 完成;数据沉淀部分依赖 Janson 真实数据与 GSC(方案明确说这部分
压不进 2-3 天,需接 GSC + 维护 Obsidian)。**

## 2. 阶段 2 验收清单(方案 §10.1)对照

| 验收项 | 状态 | 落点 |
|---|---|---|
| strategic-filter 4 用例 | ✅ 用例已固化 | tests/cases.json,跑实需真实 Topics/Performance |
| keyword-researcher 3+1 用例 | ✅ | 含降级模式用例(风险①对策) |
| seo-writer-v2 五项升级 | ✅ 规格落地 | SKILL.md §2 五项 + io-schema 强制 library_refs |
| editorial-gate 3 用例 | ✅ | 含"必须 BLOCK 一次"用例 |
| voice-checker 基础测试 | ✅ | 4 用例 |
| 第 44 篇全流程跑通 | ⏳ 待执行 | 需 Janson 给话题 + 外部关键词数据 |
| Gate 至少 BLOCK 一次 | ✅ 已设计 | tests 含强制 BLOCK 用例 |
| ASG 数据有 Library ID | ✅ 已强制 | Gate 6 硬 BLOCK + io-schema pattern 约束 |
| Janson 4 确认点 | ✅ 已布线 | AGENTS.md + envelope.human_gate |

## 3. 跨文件一致性验证

### 3.1 类型参数表单一真实源
`asg-publishing-gate.md §A` ↔ `asg-editorial-gate/io-schema.json $defs.article_type_params`
逐值核对一致(pillar/share/response 的 word/h2/links/density/refs/schema)。
→ **消除了我之前指出的"类型参数跨 Skill 漂移"风险**:所有 Skill 引用 §A 这一处。

### 3.2 JSON 合法性
全部 20 个 JSON 文件通过 `json.load` 解析(见提交前校验)。

### 3.3 信封契约闭环
每个 skill 的 io-schema `allOf $ref` envelope.schema.json;`skill` 字段 `const`
锁定;`status` 五态语义在 pipeline-contract §4 统一定义;`next_skill` 串联与
AGENTS.md 调用图一致。

### 3.4 n8n 就绪自检
- ✅ 每 Skill 输入输出皆 JSON,无对话依赖(SKILL.md 明示"给定 input JSON 独立运行")
- ✅ status/next_skill 驱动编排(可直接映射 n8n Switch/连线)
- ✅ human_gate 标注(映射 n8n Wait/Approval)
- ✅ Library 引用走 ID 解析(映射 n8n 读 vault)
- ✅ pipeline-contract.md §6 给出 n8n 映射表

## 4. 已知缺口(需 Janson 决定/输入,非工程遗漏)

1. **真实 ASG 数据核验** — 所有 Library `verified:false`,种子取自方案陈述,Janson 须用真实运营数据逐条核验。
2. **外部关键词数据** — keyword-researcher 不造数;Janson 需接 Ahrefs/SEMrush。已建降级模式兜底。
3. **GSC 接入** — stock-auditor / 反馈环需要;无 GSC 走 basic 模式但效果差一档。
4. **Obsidian 双仓** — 第 11 章 `asg-knowledge-vault` 是独立仓库,本仓库是 `asg-content-os`。Obsidian 规范化(obsidian-knowledge-base-standards.md,第 6 份规则文档)与 risk-compliance/geo-standards 两份规则文档**未在本波**(方案定为阶段 2 中后段)。
5. **方案中 `【表格待补】`** — 28 步表、21 步映射表等原飞书表格仍待补;不阻塞骨架,但完整流程文档需补。

## 5. 一句话结论
**阶段 1+2 的纯工程骨架已全部交付且自洽:7 个 Skill(规格+JSON 契约+测试用例)
+ 3 规则文档 + 4 Library 结构 + n8n 就绪流转契约,跨文件一致,JSON 全合法。**
剩余的是"真实数据/外部工具/Janson 决策"四类输入——这些方案本身就定义为
依赖 Janson 的部分,不是 2-3 天工程能产出的。
