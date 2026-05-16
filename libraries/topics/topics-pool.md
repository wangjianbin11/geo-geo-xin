---
doc: topics-pool
title: 选题池库 (Topics Pool Library)
status: v0.1
verified: false
source: placeholder
last_updated: 2026-05-16
note: 本表为结构占位,无真实搜索量/排名。真实选题必须由 Janson 基于真实关键词调研与市场分析在 Obsidian /01-GEO市场分析 录入后同步至此;此处所有示例行均为结构演示,严禁当真实选题使用。
---

# 选题池库 (Topics Pool Library)

> 每条选题是一个可被引用的话题资产,带 `TOPIC-` ID(envelope.schema.json
> `library_refs` 已预留 `TOPIC-` 前缀)。机器调用读 `topics-pool.json`。
> 选题池贯穿反馈环:asg-strategic-filter 读它判去重/优先级,
> asg-monthly-auditor 写回 `pool_status` / `usage_count` / 新 `TOPIC-` 提案。

`pool_status` 取值:`new`(候选,未投产)| `observed`(已投产,观察期)|
`active`(已投产且表现达标)| `retired`(淘汰,ID 不回收)。
`priority` 取值:`P0`–`P3`。**搜索量/排名等字段在真实数据录入前一律 `null`,
`verified:false`。**

## 选题池(结构占位,非真实数据)

| ID | term | pool_status | priority | cluster | article_refs | last_article_date | next_action | verified |
|---|---|---|---|---|---|---|---|---|
| TOPIC-uk-suppliers | uk dropshipping suppliers | active | P0 | uk-suppliers | #44 | null | KEEP,季度复盘是否升级 pillar | false |
| TOPIC-dropshipping-agent | dropshipping agent | observed | P1 | agent-service | #44 | null | 观察首月 GSC,达标转 active | false |
| TOPIC-uk-shipping-cost | uk dropshipping shipping cost | new | P2 | uk-suppliers | (空) | null | 待 Filter 评估是否投产 | false |
| TOPIC-private-label | private label dropshipping | new | P3 | brand-build | (空) | null | 候选,优先级低,暂不排期 | false |
| TOPIC-aliexpress-2024 | aliexpress dropshipping 2024 | retired | P3 | legacy | #5 | null | 已淘汰(年份过时,低意图),ID 留痕不回收 | false |

> 占位说明:`article_refs` 形如 `["#44"]`;`last_article_date` /
> `performance_note` 等依赖真实 GSC/运营数据的字段在核验前留 `null`。
> `TOPIC-aliexpress-2024` 为年份过时淘汰示例,演示 `retired` 状态留痕。

## 引用示例

> asg-strategic-filter 命中已存选题时,envelope `library_refs` 写
> `["TOPIC-uk-suppliers"]`;asg-monthly-auditor 复盘后可将其
> `pool_status` 由 `observed` 升 `active`,或提案新 `TOPIC-` 候选。

## 维护 / 同步

真实选题的唯一编辑入口是 Janson 的 Obsidian `/01-GEO市场分析`(基于真实关键词
调研、竞品与市场分析),经 `asg-obsidian-knowledge-base-standards.md` 约定的同步
流程投影到本库。本仓库只持有结构 + 调用契约 + 占位行;冲突时以 `.json` 为机器
真值、`.md` 为人类真值,月度审计(asg-monthly-auditor)对齐并批量回写
`usage_count` 与 `pool_status`。新增选题取下一个未用 `TOPIC-` ID,不复用;
淘汰置 `retired`,ID 不回收。
