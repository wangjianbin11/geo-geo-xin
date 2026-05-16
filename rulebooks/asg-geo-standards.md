---
doc: asg-geo-standards
title: GEO 优化标准
status: v0.1
authority: sub-law
parent: asg-content-constitution
last_updated: 2026-05-16
verified: false
review_cycle: monthly
enforced_by: [asg-keyword-researcher, asg-seo-writer-v2, asg-editorial-gate]
calibrated_by: [asg-geo-benchmarker]
---

# GEO 优化标准 (Generative Engine Optimization Standards)

> 定义"被 AI 引擎(Perplexity / Google AI Overview / ChatGPT search)引用"
> 所需的结构元素。asg-seo-writer-v2 据此写;asg-editorial-gate Gate 4/7 据此查;
> **asg-geo-benchmarker 每周用真实引用证据校准本文档**(本文档预期高频迭代)。

---

## Section 1 | GEO 与 SEO 的关系

**声明.** SEO 让页面被检索到;GEO 让段落被 AI 抽出来当答案引用。两者并行,**不
互斥**。同一篇文章必须同时满足 publishing-gate §A 的 SEO 项与本文档的 GEO 项。

**北极星映射.** 北极星① = AI 引用率;本文档是其唯一规则载体。

---

## Section 2 | Answer Capsule(答案胶囊)— 核心元素

**声明.** 每个 H2 开头必须有一个"可被独立摘走"的答案块:**40–60 词、自足、
无需上文即可读懂、含主词或其同义、给出直接结论**。

**正例.**
> **Short answer:** UK dropshipping suppliers typically add £0.9–£1.9 per order
> in shipping alone. The lever that moves it most is parcel routing, not unit
> price — we cut one store from £1.85 to £0.92 [ASG-CASE-XXX].

**反例.** H2 后直接进入背景铺垫,200 词后才给结论。AI 抽不到可引用句。

**如何检测.** asg-editorial-gate Gate 7(每 H2 必须有 answer block);
voice/structure 联检。

---

## Section 3 | FAQ Schema + 自然问答块

**声明.** 每篇含 FAQPage Schema,问题取自真实客户语言(Voices Library
`VOICE-*`),答案 30–80 词、自足。pillar ≥6 问,share ≥4,response ≥3。

**如何检测.** Gate 4(FAQPage Schema 必需)+ 数量按类型;问题尽量挂 VOICE 引用。

---

## Section 4 | 结构化抽取友好元素

**声明.** AI 偏好可结构化抽取的内容。每篇按类型至少含:
- 对比表(选项/before-after)≥1(pillar ≥2)
- 有序步骤列表 ≥1(适用题材)
- 关键数字以"数值 + 单位 + 来源 ID"形式呈现
- 每 H2 一个 **Key Takeaway** 单句结论(可被直接引用)

**反例.** 把对比信息写成一长段散文 → AI 难抽取,竞品的表格被引走。

**如何检测.** Gate 7(每 H2 表/列表/案例 ≥1 + Key Takeaway)。

---

## Section 5 | 段落与可读性(与 voice-bible §4 一致)

**声明.** 段落 2–4 句,**绝不 >5 句**(硬规则)。一段一个论点。结论前置。

**如何检测.** asg-editorial-gate Gate 8。

---

## Section 6 | 实体与权威信号

**声明.** 明确实体(ASG、地名、法规机构、载体)+ 第一人称经验锚 + 外部权威源
(SOURCE-*)。AI 更倾向引用"有主体、有出处、有具体数字"的段落。ASG 运营数据/
案例锚用 canonical `ASG-{CATEGORY}-{NNN}`(在
`libraries/facts/asg-verified-data-library.json` 可解析,含 `ASG-CASE-*`);外部
权威源仍用 `SOURCE-*`。ID 方案见 `data/migrations/id-crosswalk.md`。

**如何检测.** Gate 6(ASG 数据 ID,`ASG-*` 解析至 verified data library)+
Gate 5(外链)+ voice-checker 检查 2(经验锚)。

---

## Section 7 | 反 AI 痕迹(与 voice-bible §5/§7 协同)

**声明.** 被 AI 引用 ≠ 读起来像 AI 写的。禁用词、模板化同构段落、中性百科腔会
同时损害 voice 与被引用价值(AI 倾向引"有信息密度+有立场"的内容)。

**如何检测.** asg-voice-checker 检查 3/4;Gate 9 禁用词。

---

## Section 8 | 校准接口(给 asg-geo-benchmarker)

benchmarker 每周输出 `rulebook_revision_proposals[].target_doc ==
"asg-geo-standards"` 时,提案须指明:改哪个 Section、改成什么、证据(哪些被引
用竞品文具备该特征 / ASG 做了却没被引)。月度审计人工合入,版本号 +0.1,
CHANGELOG 记录证据来源。

---

## 版本历史
| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-05-16 | 初版 8 Section。Answer Capsule/FAQ/结构元素为种子标准,预期被 benchmarker 每周校准,迭代最快的规则文档。 |
