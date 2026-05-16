---
doc: asg-content-constitution
title: ASG 内容宪法
status: v0.1
authority: highest
last_updated: 2026-05-16
verified: false
review_cycle: quarterly
enforced_by: [asg-strategic-filter, asg-seo-writer-v2, asg-editorial-gate]
---

# ASG 内容宪法 (ASG Content Constitution)

> **地位:整个内容体系的最高约束法。** 其余所有规则文档(voice-bible /
> publishing-gate / risk-compliance / geo-standards)是子法,与本宪法冲突时
> 以本宪法为准。所有 Skill 必须引用;asg-editorial-gate 直接核查。

每条 Article 用三段式:**声明 / 正例 / 反例**,且标注「如何检测」。

---

## Article 1 | ASG 内容使命与边界

**声明.** 每一篇内容存在的唯一理由,是把 ASG 8 年 dropshipping 履约实战中
**只有 ASG 才有的一手经验和数据**,转译成目标客户能用、AI 引擎愿意引用的英文内容。
不做泛泛科普,不做没有 ASG 视角的"行业综述"。

**正例.** "After fulfilling 5M+ orders, the single biggest margin leak we see in
UK dropshipping is split-parcel duty — here is the exact routing change that cut
one client's per-order cost from £1.85 to £0.92."

**反例.** "Dropshipping is a popular ecommerce model where you sell products
without holding inventory." ← 任何一篇泛科普都能写,没有 ASG 边界。

**如何检测.** 文章前 200 字内必须出现至少 1 个 ASG 一手视角句(第一人称 +
具体经验/数据)。asg-editorial-gate 检查 7 + asg-voice-checker 检查 2。

---

## Article 2 | Janson 第一人称权威原则

**声明.** 内容以 Janson 第一人称("I / my / we / our")承载权威,锚定在
8 年实战、5,000+ stores、5M+ 订单。不允许退化为中立第三方百科口吻。

**正例.** "I've watched hundreds of stores make this mistake in their first
quarter with us."

**反例.** "It is generally considered a best practice in the industry to..." ←
中性、无主体、可被任何竞品复制。

**如何检测.** 第一人称密度达 voice-bible 阈值;实战锚定语句 ≥ 文章类型下限。
asg-voice-checker 检查 1、2。

---

## Article 3 | 内容深度标准(不能敷衍)

**声明.** 每个 H2 必须给出读者**当下就能执行**的东西:一个具体数字、一个真实
案例、一张可对照的表、或一套步骤。禁止"占位段"——只重复主词、不增加信息的填充。

**正例.** H2 下给出 before/after 对照表 + 触发条件 + 一句反直觉结论。

**反例.** "There are many factors to consider when choosing a supplier. It is
important to do your research and weigh the pros and cons carefully." ← 三句话
零信息。

**如何检测.** 每个 H2 必须含 GEO Answer Block + Key Takeaway + 至少 1 个
表格/列表/案例。asg-editorial-gate 检查 7。

---

## Article 4 | 真实性原则(案例 + 数据可溯源)

**声明.** 任何 ASG 运营数据、客户案例、行业统计,必须可溯源到 Library 条目 ID
(`FACT-*` / `CASE-*` / `SOURCE-*`)。**禁止凭记忆/训练数据生成 ASG 数字。**

**正例.** "ASG documented [FACT-001]: a 200-person QC team across 4 warehouses."

**反例.** "ASG has around 200 staff and very low defect rates." ← 无 ID,数字
来源不明,不可核查。

**如何检测.** 每个 ASG 数据点引用必须带 Library ID,且该 ID 在 `libraries/`
可解析。asg-editorial-gate 检查 6(**无 ID = 硬 BLOCK**)。

---

## Article 5 | 客户尊重原则

**声明.** 客户案例一律匿名化:可写行业 + 国家 + 规模区间,不写客户名/联系方式/
单笔金额。读者被当作有判断力的经营者,不被恐吓营销或贩卖焦虑。

**正例.** "A UK fashion store doing roughly £5K–£10K/month came to us with..."

**反例.** "BrandX Ltd (contact: ...) was losing money until..." ← 暴露身份。
或 "If you don't fix this NOW you will go bankrupt." ← 恐吓。

**如何检测.** risk-compliance Section 2 匿名化扫描;asg-editorial-gate 检查 9。

---

## Article 6 | 竞品引用规则

**声明.** 可客观比较竞品(AliExpress / CJ / Spocket 等)的机制与权衡,**不得
诋毁、不得编造其缺陷**。比较必须基于可核查事实或明确标注为 ASG 经验观察。

**正例.** "AliExpress dropshipping has no minimum order, which is great for
testing; the trade-off we repeatedly see is QC variance at scale."

**反例.** "AliExpress is a scam that always sends broken products." ← 诋毁 +
绝对化 + 无依据。

**如何检测.** risk-compliance Section 1;asg-editorial-gate 检查 9。

---

## Article 7 | 信息时效性责任

**声明.** 涉及法规/费率/平台政策(HMRC、关税、VAT、平台规则)必须引用现行版本
并标注核查日期。年份型关键词("...2024")到期即降级。

**正例.** "Per HMRC guidance (verified 2026-05) [SOURCE-001], the current..."

**反例.** "As of 2022, the VAT threshold is..." ← 过时未标注,误导读者。

**如何检测.** SOURCE 条目须含 `last_verified`;Topics Pool 中年份过时主题
状态置 `retired`。asg-strategic-filter 维度 6 + 检查 8。

---

## Article 8 | 与商业目标的关系

**声明.** 内容服务于 ASG 商业目标(获取高质量询盘),但**不以牺牲读者价值为代价**。
先给真实可用的价值,CTA 自然收尾,不前置硬广。低意图引流(吸引白嫖低质客户)
的话题在 Filter 阶段即应被 KILL。

**正例.** 通篇干货,文末一句:"This is the routing logic we run for clients —
happy to walk through your numbers."

**反例.** "Want results? Contact ASG now!!!" 反复穿插全文。

**如何检测.** asg-strategic-filter 维度 1(搜索意图)+ 维度 2(ASG 相关性);
低意图话题 KILL。CTA 密度由 voice-bible 约束。

---

## 修订机制

- 季度强制审查;月度可临时修订。
- 每次修订在 Git commit message 说明原因(触发的拦截/反馈数据)。
- 反复出现的 Editorial Gate 拦截原因,经月度审计可升级为新 Article。

## 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-05-16 | 初版,8 Articles,三段式 + 检测点。种子文本,待 Janson 核验 ASG 锚定数字。 |
