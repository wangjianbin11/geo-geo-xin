---
doc: id-crosswalk
title: Library ID 迁移对照表(种子 → 真实)
status: authoritative
source: janson-verified-data-library-2026-05-16
last_updated: 2026-05-16
---

# Library ID 迁移对照表

> 背景:Janson 提供 71 条已核验真实数据(`libraries/facts/asg-verified-data-library.json`),
> 命名 `ASG-{类别}-{NNN}`,取代此前 `verified:false` 的种子 `FACT-*` / `CASE-*`。
> 本表是**权威映射**,ASG-044 样例与任何引用旧种子 ID 的产物按此迁移。

## 决策

- **权威 ID 方案 = `ASG-{CATEGORY}-{NNN}`**(Janson SSOT,只增不改)。
- `libraries/facts/` 承载 13 个事实类(CORP/TEAM/SUPPLY/LOGISTICS/QC/SERVICE/
  PRICING/TECH/BRAND/MARKET/COMPARE/CONTACT/CERT/FOUNDER)。
- `libraries/cases/` 承载 `customer_cases`(ASG-CASE-001..005)。
- `SOURCE-*`(外部权威源)、`VOICE-*`(客户原话)、`TOPIC-*`(主题池)**维持不变**
  —— 它们不在 Verified Data Library 范围内,是不同关注点。
- 旧 `FACT-*` / 种子 `CASE-*` **废弃**,仅经本表追溯。无已发布文章引用过它们,
  故安全替换(符合宪法"只增不改"——历史无引用)。

## FACT-* 种子 → 真实 ASG-*(用于迁移 ASG-044)

| 种子 ID(废弃) | 含义(种子) | 真实 ID | 真实 claim(权威值) | 备注 |
|---|---|---|---|---|
| FACT-001 | QC/团队 200 人 | `ASG-TEAM-001` | team ≈ 200 | 值一致 |
| FACT-002 | 4 仓库 | `ASG-TEAM-003` | 4 warehouses (Dongguan/Shenzhen) | 值一致 |
| FACT-003 | 520,000+ 供应商 | `ASG-SUPPLY-002` | 520,000+ suppliers | 值一致 |
| FACT-004 | 2,300+ 工厂 | `ASG-SUPPLY-001` | 2,300+ vetted factories | 值一致 |
| FACT-010 | 缺陷率 0.3% | `ASG-QC-001` | 0.3% vs 行业 8% | 真实值更完整(带行业基线) |
| FACT-011 | 珠宝缺陷 <1.8% | —(无真实对应) | — | **真实库无此项 → 删除该引用** |
| FACT-020 | US 4-6 天 | `ASG-LOGISTICS-002` | US 5-8 天 | ⚠ 种子值错;以真实 5-8 为准 |
| FACT-021 | UK 5-7 天 | `ASG-LOGISTICS-002` | UK 4-7 天 | ⚠ 种子值错;以真实 4-7 为准 |
| FACT-030 | Q4 峰值 23,000 单 | `ASG-TEAM-006` | 23,000 单(2024 双十一) | 值一致 |
| FACT-031 | 旺季 97.3% 准时 | `ASG-TEAM-009` | 全年 96.8%;峰值窗 97.3% | 用 009(注 006 备注含 97.3) |
| FACT-040 | 8 年经验 | `ASG-CORP-002` | 8+ years | 值一致 |
| FACT-041 | 5,000+ 店铺 | `ASG-SERVICE-001` | 5,000+ sellers served | 值一致 |
| FACT-042 | 5M+ 累计订单 | `ASG-TEAM-008` | 5M+ cumulative | 值一致 |

## 种子 CASE-* → 真实 ASG-CASE-*

种子 `CASE-001..007` 为**虚构占位**(verified:false),真实 `customer_cases`
仅 5 条且情境不同。**不做 1:1 映射**;ASG-044 样例的案例引用按真实库重建:

| 种子(废弃) | 处理 |
|---|---|
| CASE-001 (UK 品牌增长占位) | → 用 `ASG-CASE-002`(英国曼彻斯特切换案,真实) |
| CASE-007 (UK 运费 £1.85→£0.92 占位) | 真实库无运费案;改引 `ASG-LOGISTICS-002`+`ASG-CASE-002` 支撑 UK suppliers 论点;删除虚构运费数字 |
| CASE-002..006 | 无真实对应 → 删除,改引真实 ASG-CASE-001..005 中契合者 |

## ASG-044 样例迁移目标(供 Agent B 执行)

ASG-044 是「UK dropshipping suppliers」pillar 样例。迁移后 library_refs 用真实 ID,
建议集合(全部真实可解析):

```
ASG-CORP-002  (8+ yrs)        ASG-TEAM-001 (~200 team)   ASG-TEAM-003 (4 WH)
ASG-TEAM-008  (5M+ orders)    ASG-SERVICE-001 (5,000+)   ASG-QC-001 (0.3% vs 8%)
ASG-LOGISTICS-002 (UK 4-7d)   ASG-LOGISTICS-001 (5-8d)   ASG-CASE-002 (UK switch)
ASG-SUPPLY-001 (2,300+ fac)   ASG-SUPPLY-007 (1-pc MOQ)  ASG-COMPARE-001 (vs AliExpress)
```
`SOURCE-*` 外链与 `TOPIC-*` 不变。任何原 `FACT-011`/虚构 `CASE-*` 引用**移除**。

## 校验

迁移后 `python3 tools/validate_pipeline.py` 必须仍 ALL GREEN
(Gate-6 契约:每个 library_ref 在 `libraries/**` 可解析;真实 ASG-* 已纳入 ID universe)。
