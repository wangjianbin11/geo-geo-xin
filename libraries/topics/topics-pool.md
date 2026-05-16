---
doc: topics-pool
title: 选题池库 (Topics Pool Library)
status: v0.1
verified: true
source: janson-keyword-corpus-2026-05-16
last_updated: 2026-05-16
note: 真实选题池,替换原结构占位。volume/KD/CPC/intent/competition 逐字取自 Janson 真实关键词语料(3,625 行,2026-05-16 导出),故 verified=true;选种/优先级(P0-P3)/聚类为基于该真实语料的 AI 派生判断,故 derived=true。pool_status/article_refs 已对真实 GSC pages+queries 交叉核验。真实选题的唯一编辑入口仍是 Janson 的 Obsidian /01-GEO市场分析。
---

# 选题池库 (Topics Pool Library)

> 每条选题是一个可被引用的话题资产,带 `TOPIC-` ID(envelope.schema.json
> `library_refs` 已预留 `TOPIC-` 前缀)。机器调用读 `topics-pool.json`。
> 本表为**真实数据**:42 条选题的 volume/KD/CPC/intent/competition 直接来自
> Janson 2026-05-16 提供的 3,625 行真实关键词语料(`data/keywords/keyword-corpus.csv`),
> 故 `verified:true`;选种、P0–P3 优先级与 cluster 归类是基于该真实语料的
> AI 派生判断,故 `derived:true`。`pool_status` / `article_refs` 已对真实 GSC
> 存量页(`data/gsc/gsc_pages.csv`)与真实查询(`data/gsc/gsc_queries.csv`)交叉核验。

`pool_status` 取值:`new`(候选,未投产)| `observed`(已在 GSC 查询出现,观察期)|
`active`(已有清晰覆盖该词的存量页)| `retired`(淘汰,ID 不回收)。
`priority` 取值:`P0`(volume≥1000 且 KD≤35 且 intent∈[C,T,N])|
`P1`(可观量级且 KD≤45)| `P2`(利基/长尾)| `P3`(信息型/低优先,含被降级的高量 KD>60 巨词)。

统计:共 **42** 条 | P0=3 P1=18 P2=19 P3=2 | cluster {'general': 29, 'sourcing': 6, 'agent': 3, 'jewelry': 4} | pool_status {'active': 9, 'new': 33}。

## 选题池(真实数据,按 P0→P3 排序)

| ID | term | priority | cluster | volume | KD | intent | pool_status | article_refs |
|---|---|---|---|---|---|---|---|---|
| TOPIC-best-dropshipping-products-2025 | best dropshipping products 2025 | P0 | general | 2400 | 27.0 | C | active | how-to-find-winning-products |
| TOPIC-best-dropshipping-products | best dropshipping products | P0 | general | 1900 | 31.0 | C | active | how-to-find-winning-products |
| TOPIC-ecommerce-platform-for-dropshipping | ecommerce platform for dropshipping | P0 | general | 1600 | 17.0 | C | active | where-to-best-ecommerce-platform-for-dropshipping |
| TOPIC-shopify-dropshipping-suppliers | shopify dropshipping suppliers | P1 | sourcing | 1300 | 43.0 | N | active | shopify-dropshipping-suppliers-top-7-compared-for-speed-quality-and-scale |
| TOPIC-cj-dropshipping-suitcasse-handles | cj dropshipping suitcasse handles | P1 | agent | 880 | 8.0 | N | new | (空) |
| TOPIC-ksa-dropshipping | ksa dropshipping | P1 | general | 880 | 17.0 | N | new | (空) |
| TOPIC-best-dropshipping-niches-2025 | best dropshipping niches 2025 | P1 | general | 880 | 27.0 | C | new | (空) |
| TOPIC-gpc-chris-dropshipping-reddit | gpc chris dropshipping reddit | P1 | general | 880 | 29.0 | N | new | (空) |
| TOPIC-is-depop-dropshipping-legit-reddit | is depop dropshipping legit reddit | P1 | general | 880 | 31.0 | N | new | (空) |
| TOPIC-arabia-dropshipping | arabia dropshipping | P1 | general | 880 | 36.0 | N | new | (空) |
| TOPIC-dropshipping-clothing-suppliers | dropshipping clothing suppliers | P1 | sourcing | 720 | 24.0 | C | new | (空) |
| TOPIC-bigcommerce-dropshipping | bigcommerce dropshipping | P1 | general | 720 | 27.0 | N | active | how-does-it-work-bigcommerce-dropshipping |
| TOPIC-dropshipping-jewelry | dropshipping jewelry | P1 | jewelry | 390 | 21.0 | C | new | (空) |
| TOPIC-intimate-dropshipping | intimate dropshipping | P1 | general | 390 | 18.0 | N | new | (空) |
| TOPIC-best-fashion-jewelry-dropshipping-suppliers-no-inventory | best fashion jewelry dropshipping suppliers no inventory | P1 | jewelry | 320 | 6.0 | C | new | (空) |
| TOPIC-jewelry-dropshipping | jewelry dropshipping | P1 | jewelry | 320 | 15.0 | C | new | (空) |
| TOPIC-best-dropshipping-apps-for-shopify | best dropshipping apps for shopify | P1 | general | 320 | 24.0 | C | new | (空) |
| TOPIC-top-dropshipping-suppliers | top dropshipping suppliers | P1 | sourcing | 320 | 30.0 | C | active | the-top-10-dropshipping-suppliers-and-platforms |
| TOPIC-dropshipping-website-builder | dropshipping website builder | P1 | general | 320 | 31.0 | C | active | can-i-free-dropshipping-website-builder |
| TOPIC-dropshipping-t-shirts | dropshipping t shirts | P1 | general | 320 | 35.0 | C | new | (空) |
| TOPIC-cj-dropshipping-usa | cj dropshipping usa | P1 | agent | 320 | 29.0 | N | active | 6-best-china-to-usa-shipping-lines-for-dropshipping-in-2026 |
| TOPIC-best-dropshipping-apps | best dropshipping apps | P2 | general | 260 | 13.0 | C | new | (空) |
| TOPIC-best-dropshipping-jewelry-suppliers-low-cost-bulk-orders | best dropshipping jewelry suppliers low cost bulk orders | P2 | jewelry | 260 | 13.0 | C | new | (空) |
| TOPIC-dropshipping-home-decor | dropshipping home decor | P2 | general | 170 | 4.0 | C | new | (空) |
| TOPIC-home-decor-dropshipping | home decor dropshipping | P2 | general | 140 | 2.0 | C | new | (空) |
| TOPIC-dropshipping-coasters | dropshipping coasters | P2 | general | 140 | 5.0 | C | new | (空) |
| TOPIC-best-shopify-themes-for-dropshipping | best shopify themes for dropshipping | P2 | general | 110 | 3.0 | C | new | (空) |
| TOPIC-home-decor-dropshipping-suppliers | home decor dropshipping suppliers | P2 | sourcing | 110 | 4.0 | C | new | (空) |
| TOPIC-dropshipping-shoes | dropshipping shoes | P2 | general | 110 | 5.0 | C | new | (空) |
| TOPIC-best-dropshipping-apps-2024 | best dropshipping apps 2024 | P2 | general | 70 | 0.0 | C | new | (空) |
| TOPIC-dropshipping-belgie | dropshipping belgie | P2 | general | 70 | 1.0 | C | new | (空) |
| TOPIC-dropshipping-bracelet-men-luxury | dropshipping bracelet men luxury | P2 | general | 50 | 0.0 | C | new | (空) |
| TOPIC-dropshipping-club-dresses | dropshipping club dresses | P2 | general | 50 | 0.0 | C | new | (空) |
| TOPIC-dropshipping-sunglasses | dropshipping sunglasses | P2 | general | 50 | 0.0 | C | new | (空) |
| TOPIC-sunglasses-dropshipping | sunglasses dropshipping | P2 | general | 50 | 1.0 | C | new | (空) |
| TOPIC-best-cbd-dropshipping-suppliers-usa | best cbd dropshipping suppliers usa | P2 | sourcing | 40 | 0.0 | C | new | (空) |
| TOPIC-dab-rig-dropshipping | dab rig dropshipping | P2 | general | 40 | 0.0 | C | new | (空) |
| TOPIC-dropshipping-work-safety-boots | dropshipping work safety boots | P2 | general | 40 | 0.0 | C | new | (空) |
| TOPIC-electric-scooter-dropshipping | electric scooter dropshipping | P2 | general | 40 | 0.0 | C | new | (空) |
| TOPIC-dropshipping-va | dropshipping va | P2 | general | 40 | 1.0 | C | new | (空) |
| TOPIC-dropshipping-suppliers | dropshipping suppliers | P3 | sourcing | 12100 | 64.0 | C | active | the-top-10-dropshipping-suppliers-and-platforms |
| TOPIC-cj-dropshipping | cj dropshipping | P3 | agent | 12100 | 58.0 | N | new | (空) |

> intent 编码:`C`=commercial,`T`=transactional,`N`=navigational,
> `I`=informational,空=未分类(本池选种时已优先非 I 意图)。`KD` 为关键词难度,
> `volume` 已剥离千分位为整数。每条均带 `cpc` / `competition` / `source` /
> `verified:true` / `derived:true`,完整字段见 `topics-pool.json`。

## 引用示例

> asg-strategic-filter 命中已存选题时,envelope `library_refs` 写
> `["TOPIC-ecommerce-platform-for-dropshipping"]`(本池最佳 P0:volume 1600 /
> KD 17 / 商业意图,全语料中 KD/volume 比最优);asg-monthly-auditor 复盘后可将
> `pool_status` 由 `new`→`observed`→`active`,或基于新一轮真实语料提案新 `TOPIC-` 候选。

## 维护 / 同步

真实选题的唯一编辑入口是 Janson 的 Obsidian `/01-GEO市场分析`(基于真实关键词
语料、竞品与市场分析),经 `rulebooks/asg-obsidian-knowledge-base-standards.md`
Section 2 目录映射(Obsidian `/01-GEO市场分析` → `(阶段2) topics`,前缀 `TOPIC-`)
与 Section 4 同步契约投影到本库。本库这一版已从真实语料派生填充,但仍以
Obsidian GEO 文件夹为人类真值;冲突时 `.json` 为机器真值、`.md` 为人类真值,
月度审计(asg-monthly-auditor)对齐并批量回写 `usage_count` 与 `pool_status`。
新增选题取下一个未用 `TOPIC-` ID(本池以词条 kebab-slug 命名),不复用;
淘汰置 `retired`,ID 不回收。下游引用计数变化由月度审计批量回写,非实时。
