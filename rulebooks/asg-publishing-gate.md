---
doc: asg-publishing-gate
title: 发布门禁清单
status: v0.1
authority: sub-law
parent: asg-content-constitution
last_updated: 2026-05-16
verified: false
review_cycle: monthly
enforced_by: [asg-editorial-gate]
also_referenced_by: [asg-strategic-filter, asg-keyword-researcher, asg-seo-writer-v2]
---

# 发布门禁清单 (ASG Publishing Gate)

> Step 20 asg-editorial-gate 的执行依据。同时是**文章类型参数的唯一真实源**——
> Filter / Keyword / Writer / Gate 全部引用本文「§A 类型参数表」,禁止各自硬编码。
> 这条设计是为了消除"类型参数在多个 Skill 间漂移"的架构风险。

---

## §A 文章类型参数表(Single Source of Truth)

所有下游 Skill 按 `dossier.article_type` 查此表取参数。改参数只改这里。

| 参数 | pillar | share | response |
|---|---|---|---|
| 字数 word_count | 3000–5000 | 2000–3000 | 1200–2000 |
| H2 数 h2_count | 6–7 | 5–6 | 3–4 |
| 内链 internal_links | ≥ 4 | ≥ 3 | ≥ 2 |
| 外链 external_links | ≥ 10 | ≥ 8 | ≥ 5 |
| 主词密度 primary_kw_density | 1.0–1.5% | 1.0–2.0% | 1.5–2.0% |
| 共现词密度 cooccur_density | 0.5–1.0% | 0.5% | 0.3% |
| ASG 数据引用 asg_data_refs | ≥ 9 | ≥ 5 | ≥ 3 |
| 案例引用 case_refs | ≥ 2 | ≥ 1 | ≥ 1 |
| Schema | Article+FAQ+Breadcrumb+HowTo/ItemList | Article+FAQ+Breadcrumb+ItemList | Article+FAQ+Breadcrumb |
| 流程步数 | 28(完整) | 25 | 22 |
| 适配分发 | 长视频+5 平台 | 短视频+Twitter thread | 短视频+FAQ 拆解 |

机器可读副本见 `skills/quality-control/asg-editorial-gate/io-schema.json`
的 `$defs.article_type_params`(必须与本表数值一致;不一致以本表为准并修 schema)。

---

## §B 10 项 Gate 硬检查

每项独立判 PASS / MODIFY / BLOCK。决定规则见 §C。

### Gate 1 — 主词 SEO 位置完整性
主词必须出现在:Title(前置)/ H1 / URL slug / Meta Description(靠前)/
正文前 100 字 / ≥ 2 个 H2-H3 / ≥ 1 个图片 Alt。
- 缺任意 1 项 → MODIFY(自动建议补位)。全缺/缺 ≥3 项 → BLOCK。

### Gate 2 — 主词密度
按 §A 类型对应区间核查。
- 偏离区间 ≤ ±0.2% → MODIFY;> ±0.5% → BLOCK。

### Gate 3 — 语义共现词覆盖
keyword_spec 要求的 6–10 个共现词须 100% 出现。
- 缺 1 → MODIFY;缺 ≥ 2 → BLOCK。

### Gate 4 — Schema 完整性
按 §A 类型对应组合。Article + FAQPage + BreadcrumbList 为所有类型必需。
- 缺必需三件套任一 → BLOCK;缺类型附加(HowTo/ItemList)→ MODIFY。

### Gate 5 — 内/外链数量
按 §A 类型对应下限。
- 差 1–2 → MODIFY;差 ≥ 3 → BLOCK。

### Gate 6 — ASG 数据 Library ID 标注 ★硬伤
每个 "ASG documented…/案例引用" 必须带 Library ID,且 ID 在 `libraries/` 可解析。
- **任一引用无 ID 或 ID 解析失败 → 直接 BLOCK(不容讨论)。**
- 数量同时按 §A `asg_data_refs` / `case_refs` 下限核查;不足 → BLOCK。

### Gate 7 — 每个 H2 结构完整性
每个 H2 必须含:GEO Answer Block + Key Takeaway 段 + ≥1 个表格/列表/案例 +
≥1 个外部权威源。
- 任一 H2 缺任一项 → MODIFY。

### Gate 8 — 段落规则
扫描所有段落:无 > 5 句的段落(硬规则);平均 2–4 句。
- 发现超长段落 → MODIFY(自动拆分建议)。

### Gate 9 — 禁用词 / 合规扫描
扫 voice-bible §5 禁用词库 + risk-compliance(竞品诋毁 / 客户身份暴露 / 恐吓营销)。
- 命中禁用词或合规红线 → BLOCK(硬规则)。

### Gate 10 — 重复内容核查
与已发 43 篇(审计后保留集)对比内容相似度。
- 相似度 > 30% → BLOCK;15–30% → MODIFY(差异化建议)。

---

## §C 决定规则(decision logic)

```
若 任一 Gate 触发 BLOCK            → 决定 = BLOCK
否则 若 MODIFY 项 ≥ 3              → 决定 = BLOCK(质量整体不达标)
否则 若 1 ≤ MODIFY 项 ≤ 2          → 决定 = MODIFY
否则                               → 决定 = PASS
```

- **PASS** → status=ok,进 Step 21。
- **MODIFY** → status=modify,输出修改清单 + 自动修复;同一篇二次仍未过 → 升 BLOCK。
- **BLOCK** → status=blocked,human_gate,列阻断原因,返回 Janson(修改/重写/弃稿)。

v0.1 校准说明(方案 13.1 #4):初版**故意放宽约 20%**——Gate 2 容差按
±0.3%/±0.7% 执行,Gate 10 阈值按 40% 执行,前 3 篇 v2 文章跑通后再逐步收紧到
上表正式值。收紧动作在月度审计记录于 CHANGELOG。

---

## §D 失败修复模板(供 MODIFY 自动修复引用)

| Gate | 修复模板 |
|---|---|
| 1 | "主词缺失位置:{list}。建议:Title 改为 '{kw} …';H2#{n} 注入主词。" |
| 3 | "缺共现词:{list}。建议在 H2#{n} 段 {k} 自然嵌入。" |
| 6 | "引用 '{quote}' 无 Library ID。匹配候选:{FACT/CASE ids}。请绑定或删除该数据声明。" |
| 7 | "H2#{n} 缺 {Key Takeaway / 权威源 / 结构块}。已生成占位模板,需填实。" |
| 8 | "段落 P{n} 共 {x} 句(>5)。建议在第 {k} 句后拆段。" |

---

## 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-05-16 | 初版,类型参数表(SSoT)+ 10 Gate + 决定逻辑 + v0.1 放宽 20% 校准。 |
