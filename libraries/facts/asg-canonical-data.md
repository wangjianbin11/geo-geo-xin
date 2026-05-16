---
doc: asg-canonical-data
title: ASG 锚定数据库
status: v0.1
verified: false
source: v2-plan-seed
last_updated: 2026-05-16
note: 种子数值取自 v2 开发方案明确陈述的 ASG canonical data,非编造;Janson 须用真实运营数据逐条核验后置 verified=true。
---

# ASG 锚定数据库 (Facts Library)

> 每个数据点是一个可被引用的事实,带 `FACT-` ID。文章引用必须带 ID
> (宪法 Article 4)。机器调用读 `asg-canonical-data.json`。

## Team & Operations

| ID | 数据点 | 值 | verified | not_public |
|---|---|---|---|---|
| FACT-001 | QC/运营团队规模 | 200 人 | false | false |
| FACT-002 | 仓库数量 | 4 个(东莞 + 深圳) | false | false |
| FACT-003 | 供应商网络 | 520,000+ 供应商 | false | false |
| FACT-004 | 合作工厂 | 2,300+ 工厂 | false | false |

## QC Standards

| ID | 数据点 | 值 | verified |
|---|---|---|---|
| FACT-010 | 整体缺陷率 | 0.3% | false |
| FACT-011 | 珠宝品类缺陷率 | < 1.8% | false |

## Service Capabilities

| ID | 数据点 | 值 | verified |
|---|---|---|---|
| FACT-020 | US 妥投时效 | 4–6 天 | false |
| FACT-021 | UK DDP 妥投时效 | 5–7 天 | false |

## Throughput / Reliability

| ID | 数据点 | 值 | verified |
|---|---|---|---|
| FACT-030 | Q4 旺季单量 | 23,000 单 | false |
| FACT-031 | 旺季准时率 | 97.3% on-time | false |

## Experience Anchors

| ID | 数据点 | 值 | verified |
|---|---|---|---|
| FACT-040 | 运营年限 | 8 年 | false |
| FACT-041 | 服务店铺数 | 5,000+ stores | false |
| FACT-042 | 累计订单 | 5M+ 订单 | false |

## 引用示例

> "ASG documented [FACT-001] [FACT-010]: a 200-person QC operation holding an
> overall 0.3% defect rate across [FACT-002] four warehouses."

## 不公开(not_public,禁止入正文)

- 单个供应商名单、单笔订单金额、单个客户详情、内部定价。
  (这类数据**不在本表**,此处仅声明边界。)

## 维护

Janson 数据变化时立即更新;月度审计回写 `usage_count`。新增数据点取下一个
未用 ID,不复用。
