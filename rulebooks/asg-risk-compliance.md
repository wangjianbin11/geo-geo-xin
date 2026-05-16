---
doc: asg-risk-compliance
title: 风险与合规规则
status: v0.1
authority: sub-law
parent: asg-content-constitution
last_updated: 2026-05-16
verified: false
review_cycle: monthly
enforced_by: [asg-strategic-filter, asg-editorial-gate]
implements: [asg-content-constitution#article-5, asg-content-constitution#article-6, asg-content-constitution#article-7]
---

# 风险与合规规则 (Risk & Compliance)

> 宪法 Article 5/6/7 的执行细则。asg-strategic-filter 用于话题风险标注;
> asg-editorial-gate 检查 9 据此扫描并 **BLOCK**。三段式 + 检测点。

---

## Section 1 | 竞品引用红线(实现宪法 Art.6)

**声明.** 可客观比较竞品机制与权衡;不得诋毁、不得编造缺陷、不得用绝对化贬损词。

**红线词/句式(命中即 BLOCK):**
- 绝对贬损:"scam / fraud / always breaks / never works / garbage / rip-off"
- 无依据指控:未带可核查来源的"X 偷数据 / X 是骗局 / X 必然如何"
- 影射:"unlike certain shady agents…"(指向性贬低)

**正例.** "AliExpress has no MOQ — great for testing; the trade-off we see at
scale is QC variance."
**反例.** "AliExpress is a scam that always ships broken goods."

**如何检测.** Gate 9 扫红线词表 + "竞品名 + 绝对负面词" 邻近模式 → BLOCK。

---

## Section 2 | 客户隐私与匿名化(实现宪法 Art.5)

**声明.** 客户案例只允许:行业 + 国家/地区 + 规模区间 + 脱敏指标。禁止可定位身份信息。

**禁止出现:**
- 客户公司名 / 人名 / 邮箱 / 电话 / 店铺 URL / 社媒账号
- 精确到个位的单笔金额且与可定位主体绑定
- 截图含未打码的后台/聊天

**正例.** "A UK fashion store doing roughly £5K–£10K/month…"
**反例.** "BrandX Ltd (owner John, john@brandx.com) was…"

**如何检测.** Gate 9 PII 正则扫(email/phone/URL/@handle)+ CASE 引用须来自
Cases Library(已脱敏)。命中 → BLOCK。

---

## Section 3 | 法规/费率时效合规(实现宪法 Art.7)

**声明.** 涉 HMRC/关税/VAT/FTC/平台政策的陈述必须引用 SOURCE-* 并带核查日期;
不得给确定性法律/税务"建议",只陈述现行规则 + 指向官方源。

**禁止:** "you must legally do X"(无源)/ 过时年份费率未标注 / 把"经验做法"
表述成"法律要求"。

**正例.** "Per HMRC guidance (verified 2026-05) [SOURCE-001], the current
position is … — confirm your specifics with HMRC."
**反例.** "UK law requires you to register for VAT once you hit £85k."(无源、
无日期、绝对化)

**如何检测.** Gate 9:法规类语句必须邻接一个 `SOURCE-*` 且该 SOURCE 有
`last_verified`;否则 BLOCK。Filter 维度 6 对过时年份主题降级。

---

## Section 4 | 营销诚信(实现宪法 Art.5/8)

**声明.** 不恐吓营销、不虚假承诺、不保证收益。

**禁止句式(命中即 BLOCK):**
- 恐吓:"you WILL go bankrupt / lose everything if you don't…"
- 收益保证:"guaranteed 10x / you will make $X / 100% success"
- 虚假稀缺:"only 2 spots left"(非真实)

**正例.** "This won't fix a broken product. It does protect margin — here's the
math."
**反例.** "Fail to act now and your store is dead."

**如何检测.** Gate 9 句式扫描 → BLOCK。

---

## Section 5 | 健康/财务/法律高风险主题处理

**声明.** 命中高风险类目(医疗/财税申报/法律资质/金融投资)的主题,Filter 必须
在 `risk_flags` 标注;成稿须含一句非建议声明,且仅引官方源。

**如何检测.** asg-strategic-filter 维度评分时打 `risk_flags`;Gate 9 校验高风险
稿件存在 disclaimer + 官方 SOURCE,否则 BLOCK。

---

## Section 6 | 数据真实性(实现宪法 Art.4,与 Gate 6 协同)

**声明.** 任何 ASG 运营数字必须 Library ID 可溯源。无 ID 的 ASG 数字 = 合规事故。

**如何检测.** 由 asg-editorial-gate **Gate 6**(硬 BLOCK)主检;本节为合规口径声明。

---

## 升级机制
反复命中同一红线 → 月度审计可把该模式升级为新红线条目,commit 注明来源稿件。

## 版本历史
| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-05-16 | 初版 6 Section,落地宪法 Art.5/6/7,与 Gate 9/6 对接。待 Janson 补行业特定红线词。 |
