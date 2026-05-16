---
doc: asg-verified-data-library-readme
title: ASG Verified Data Library — 人类索引
status: v1.0
verified: true
source: janson-verified-data-library-2026-05-16
last_updated: 2026-05-16
---

# ASG Verified Data Library — README

> 本仓库内 ASG 全部对外可引用运营数据的**唯一真相源**(Single Source of Truth)的人类索引。
> 机器调用读 `libraries/facts/asg-verified-data-library.json`。

---

## 这个文件是什么

`asg-verified-data-library.json` 是 ASG Dropshipping 全部对外可引用运营数据的 SSoT。
当 SEO writer / GEO optimizer / 任何 Skill 需要引用 ASG 数据时,先查这里,**不要现编**。
全部 71 条均由 Janson 核验,`verified: true`。命名 `ASG-{CATEGORY}-{NNN}`,**只增不改**。

ID 方案权威决策与旧种子映射见 `data/migrations/id-crosswalk.md`。

---

## 71 条记录,15 个分类

| 分类 | 代码前缀 | 条目数 | 用途 |
|------|----------|--------|------|
| company_basics | ASG-CORP-* | 5 | 公司身份、成立时间、定位 |
| team_and_operations | ASG-TEAM-* | 10 | 团队规模、仓储、日订单、年订单、准时率 |
| supply_chain | ASG-SUPPLY-* | 7 | 工厂数、供应商网、SKU、采购成本优势 |
| logistics_and_shipping | ASG-LOGISTICS-* | 8 | 时效、覆盖、丢件率、切换数据 |
| quality_control | ASG-QC-* | 6 | QC 缺陷率、六步流程、合格率 |
| service_and_support | ASG-SERVICE-* | 7 | 客服响应、专属经理、复购率、CSAT |
| pricing_and_costs | ASG-PRICING-* | 3 | 收费结构、付款方式、批量折扣 |
| technology | ASG-TECH-* | 4 | Shopify App、对接方式、效率提升 |
| brand_and_customization | ASG-BRAND-* | 4 | 中性包装、品牌定制、IP 保护 |
| markets_served | ASG-MARKET-* | 2 | 订单分布、重点市场 |
| customer_cases | ASG-CASE-* | 5 | 已核验的真实切换/增长案例 |
| competitive_positioning | ASG-COMPARE-* | 3 | vs AliExpress / CJ / Zendrop |
| contact_information | ASG-CONTACT-* | 3 | 官网、邮箱、WhatsApp |
| certifications_and_credentials | ASG-CERT-* | 2 | ISO 9001、Shopify 认证 |
| founder_credentials | ASG-FOUNDER-* | 2 | Janson 高校讲师身份、个人品牌 |

> 前 13 个事实类承载于 `libraries/facts/`;`customer_cases`(`ASG-CASE-001..005`)
> 同时由 `libraries/cases/README.md` 索引。

---

## Schema 字段说明(每条 11 个字段)

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一 ID,格式 `ASG-{CATEGORY}-{NNN}`,代码引用 |
| `category` | string | 上方 15 个分类之一 |
| `claim_en` | string | **英文事实陈述——文章里直接引用的就是这一句(canonical 英文措辞)** |
| `claim_zh` | string | 中文对照——内部讨论 / 翻译参考 |
| `value` | number / array / object | 结构化数值,便于程序化使用(画表、对比、Schema markup) |
| `unit` | string | value 的单位或语义类型 |
| `verified` | boolean | 永远 `true`——所有条目均已核验 |
| `verification_source` | array | 来自知识库哪个/哪些文件 |
| `last_verified` | string (YYYY-MM 或 YYYY-MM-DD) | 最后核验时间 |
| `usage_context` | array | 这条事实适合用在什么地方 |
| `competitor_comparison` | string / null | 对比基准(可选) |
| `notes` | string / null | 使用注意事项 |

---

## Skill 如何引用

1. **优先引用 `claim_en`**——它就是文章里要落地的 canonical 英文措辞,不要自行改写。
2. **范围值保持范围**:`value` 为 `[10000, 20000]` 一类,引用为区间(如 "10,000–20,000"),
   不取中点、不四舍五入成单值。
3. envelope `library_refs` 写其 `ASG-{CAT}-{NNN}` ID;Gate 6 据此对
   `libraries/facts/asg-verified-data-library.json` 解析,**解析失败 = 硬 BLOCK**。
4. 按 `category` / `usage_context` / `id` 三种典型查询方式取条目。

辅助结构:`category_index`(按类列 ID 范围)、`locked_canonical_quick_reference`、
`deprecation_and_conflicts_log`(见下)。

---

## locked_canonical_quick_reference 重点

最核心数据的极简校对表,文章数字必须与之一致:

- 团队 **200** 人;仓库 **4 个**(东莞 & 深圳);工厂 **2,300+**;SKU **1.4M+**;
  供应商网络 **520,000+**。
- 日订单 **10,000–20,000**(范围,不取单值);累计订单 **5M+**。
- 物流:全球 **5–8 天**;US **5–8 天**;**UK 4–7 天**;DE 5–8 天;AU 5–10 天;TR 9–12 天。
- QC 缺陷率 **0.3%**(行业 **8%**);客服响应 **20 分钟**(行业 **24 小时**)。
- 累计服务卖家 **5,000+**;覆盖 **200+** 国家;2024 准时率 **96.8%**;成立 **2019**;经验 **8+** 年。

---

## deprecation_and_conflicts_log 重点(避免踩坑)

- **客户数**:canonical = **5,000+**(保守值,SSoT = 公司基本信息.md)。
  **不要写 6,000+**。
- **年订单 vs 累计**:**4.2M = 2024 单年**;**5M+ = 累计**。不要在同一句混用两个数字。
- **Janson 拼写**:canonical = **Janson**。**不要写 "Jason"**。

---

*Owner: Janson | Library version: 1.0.0 | 源:janson-verified-data-library-2026-05-16*
