---
doc: authority-pool
title: 外部权威源池
status: v0.1
verified: false
source: v2-plan-seed
last_updated: 2026-05-16
note: 类目结构 + 少量种子源。43 篇文章用过的真实权威源须由 Janson 从 Obsidian /11-行业洞察 同步去重后补全。
---

# 外部权威源池 (Authority Pool)

> Step 9 强制从此池按主题匹配调用外链(数量见 publishing-gate §A)。
> 每源带 `SOURCE-` ID + Authority Score(0–10)+ `last_verified`(宪法 Article 7)。
> 机器调用读 `authority-pool.json`。

## 类目

government / industry-bodies / carriers / research / platforms

## 种子源(待 Janson 扩充)

| ID | 名称 | 类目 | URL | Score | 覆盖主题 | last_verified |
|---|---|---|---|---|---|---|
| SOURCE-001 | HMRC | government | https://www.gov.uk/ | 10 | UK VAT / 关税 / DDP | 待核 |
| SOURCE-002 | Companies House | government | https://www.gov.uk/government/organisations/companies-house | 10 | UK 公司合规 | 待核 |
| SOURCE-003 | FTC | government | https://www.ftc.gov/ | 10 | US 广告/消费者合规 | 待核 |
| SOURCE-010 | Royal Mail | carriers | https://www.royalmail.com/ | 8 | UK 末端配送 | 待核 |
| SOURCE-011 | DHL Express | carriers | https://www.dhl.com/ | 8 | 跨境快递时效 | 待核 |
| SOURCE-020 | Statista | research | https://www.statista.com/ | 7 | 行业统计 | 待核 |
| SOURCE-030 | Shopify | platforms | https://www.shopify.com/ | 7 | 平台机制/数据 | 待核 |

## 引用模板字段
每源含 `citation_template`,例:
> "Per HMRC guidance (verified {date}) [SOURCE-001], …"

## 维护
AI 每篇引用后 `usage_count += 1`(月度回写);Janson 季度核查 URL 有效性 +
更新 `last_verified`。过期源 score 降级或 retired。
