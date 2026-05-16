---
doc: asg-cases
title: 真实案例库
status: v0.1
verified: false
source: v2-plan-seed
last_updated: 2026-05-16
note: 7 个核心案例的 before/after 数值取自 v2 方案陈述,非编造;细节(行业/周期/ASG 介入点)为模板占位,Janson 须用真实案例补实并核验。阶段 2 可拆为独立文件。
---

# 真实案例库 (Cases Library)

> 叙述四拍(voice-bible §8):情境 → 问题 → ASG 做了什么 → 量化结果。
> 一律匿名化(宪法 Article 5)。机器调用读 `index.json`。

---

## CASE-001 — UK 品牌增长
- industry: UK ecommerce / brand
- scale: ~£5K/month → 规模化
- period: 待补(模板:~12 周)
- before: 月营收 ≈ £5,500
- after: 月营收 ≈ £42,000
- key_numbers: ≈ 7.6x 营收增长
- asg_role: 待 Janson 补(sourcing + 履约基础设施)
- adaptable_articles: UK cluster / brand scaling
- magnitude: { industry: "UK ecom", vertical: "brand", cluster: "UK" }
- verified: false

## CASE-002 — 珠宝品牌
- industry: US jewelry
- before: 月营收 ≈ $8,000
- after: 月营收 ≈ $42,000
- key_numbers: ≈ 5.25x;关联 FACT-011(珠宝缺陷率 <1.8%)
- asg_role: 待补(QC + 包装 + 履约)
- adaptable_articles: jewelry vertical cluster
- magnitude: { industry: "US jewelry", vertical: "jewelry", cluster: "jewelry" }
- verified: false

## CASE-003 — 服饰品牌
- industry: apparel
- before: 月营收 ≈ $15,000
- after: 月营收 ≈ $80,000
- key_numbers: ≈ 5.3x
- asg_role: 待补
- adaptable_articles: apparel scaling / sourcing
- verified: false

## CASE-004 — banking / 资金周转情境
- industry: 待 Janson 澄清情境(方案标 "banking $15K→$80K")
- before: $15,000 ; after: $80,000
- asg_role: 待补
- note: 此案例语义需 Janson 确认(资金/账期/现金流?)
- verified: false

## CASE-005 — 1688 sourcing 优化
- industry: cross-border sourcing
- before: 月营收/成本基线 ≈ $42,000
- after: ≈ $68,000
- key_numbers: ≈ 1.6x;sourcing 链路优化
- asg_role: 待补(1688 直采 + 质检)
- adaptable_articles: sourcing / cost optimization
- verified: false

## CASE-006 — Black Friday 旺季
- industry: peak-season scaling
- before: $80,000 ; after: $245,000
- key_numbers: ≈ 3x 旺季放量;关联 FACT-030/031(23,000 单 / 97.3% on-time)
- asg_role: 待补(旺季产能 + 履约保障)
- adaptable_articles: BFCM / peak readiness
- verified: false

## CASE-007 — UK 运费优化
- industry: UK ecommerce / logistics
- period: 12 周 (2024,模板)
- before: £1.85 / order shipping(独家 DHL Express)
- after: £0.92 / order shipping(hybrid routing)
- key_numbers: 50% 降幅;≈ £20,088/yr 利润保护;96% on-time 维持
- asg_role: 提供 hybrid routing 基础设施
- adaptable_articles: UK shipping cluster / logistics / margin protection
- magnitude: { industry: "UK ecom", vertical: "logistics", cluster: "UK" }
- verified: false

## 引用示例
> "In one case [CASE-007], a UK store cut shipping from £1.85 to £0.92 per
> order over twelve weeks — about £20,088/yr in protected margin — while
> holding 96% on-time."
