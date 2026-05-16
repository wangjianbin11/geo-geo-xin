# Libraries — 通用规范

> 被 Skill 调用的资产层。方案第 7 章原设计 5 个 Library,第 11 章修订为
> "对接现有 Obsidian 结构"。本仓库放**结构 + 调用契约 + 种子数据**;真实数据
> 的唯一编辑入口是 Janson 的 Obsidian(`asg-knowledge-vault` 仓库),经同步落到这里。

## ID 方案(全局唯一,不可复用)

| 前缀 | Library | 例 | 对应 Obsidian(真实文件夹名) | 代码 |
|---|---|---|---|---|
| `ASG-{CAT}-{NNN}` | facts/ Verified Data Library(13 事实类:CORP/TEAM/SUPPLY/LOGISTICS/QC/SERVICE/PRICING/TECH/BRAND/MARKET/COMPARE/CONTACT/CERT/FOUNDER) | ASG-TEAM-001 | `00-企业DNA` | DNA |
| `ASG-CASE-*` | cases/ → 真实客户案例并入 verified library `customer_cases`(`ASG-CASE-001..005`) | ASG-CASE-002 | `09-客户案例库-F&Q`(252 FAQ + 案例) | CASE |
| `SOURCE-` | sources/ 外部权威源 | SOURCE-012 | `11-行业洞察` | INSIGHT |
| `VOICE-` | voices/ 客户原话 | VOICE-003 | `01-销售获客`(对话脱敏) | SALES |
| `TOPIC-` | (阶段2) topics 池 | TOPIC-uk-suppliers | `01-GEO市场分析` | GEO |

> **ID 方案权威决策(2026-05-16)**:Janson 提供 71 条已核验真实数据,
> canonical 方案 = `ASG-{CATEGORY}-{NNN}`(SSOT,只增不改),取代旧
> `verified:false` 种子 `FACT-*` / `CASE-*`(已废弃,见各目录 README)。
> `SOURCE-*` / `VOICE-*` / `TOPIC-*` 不在 Verified Data Library 范围,**维持不变**。
> 权威映射与迁移见 `data/migrations/id-crosswalk.md`。

> 中文文件夹名 = Janson Obsidian 知识库 `ASG-KB-FULL` 的真实磁盘路径
> (源 janson-2026-05-16,逐字复制不翻译)。完整一/二级文件夹结构、命名规则、
> 已知违规与代码速查见 `libraries/obsidian-folder-map.md`;
> **机器索引(Skill/工具读取)在 `libraries/obsidian-folder-map.json`**。
> 注:`09-客户案例库-F&Q` 含 `&`、`01-GEO市场分析` 前缀与 `01-销售获客`
> 重复,均为待协调的已知缺口(machine index `conforms:false`)。

ID 一经分配永久绑定该数据点;数据淘汰则状态置 `retired`,ID 不回收。

## 每条数据必备字段

**facts/ Verified Data Library**(`asg-verified-data-library.json`,canonical)每条
`data_point` 的 11 字段见 `libraries/facts/asg-verified-data-library-README.md`:
`id` / `category` / `claim_en` / `claim_zh` / `value` / `unit` / `verified`(恒 `true`)/
`verification_source` / `last_verified` / `usage_context` / `competitor_comparison` / `notes`。
引用时**优先 `claim_en`**,区间值保持区间。

**sources/ voices/ topics(SOURCE-/VOICE-/TOPIC-)** 仍用种子 frontmatter 形态:

```yaml
id: SOURCE-001
status: active            # active | draft | retired
last_updated: 2026-05-16
verified: false           # 核验后置 true
source: external          # internal | external | v2-plan-seed
usage_count: 0            # 被文章引用次数,反馈环更新
applies_to: [pillar, share, response]
not_public: false         # true = 仅内部,不得出现在文章
```

## 调用契约

1. Skill 引用任何数据点,必须在 envelope `library_refs` 写其 ID。ASG 运营数据/
   案例用 canonical `ASG-{CATEGORY}-{NNN}`(对 `asg-verified-data-library.json` 解析)。
2. asg-editorial-gate 检查 6 校验 ID 可解析;**解析失败 = 硬 BLOCK**。
3. 引用成功后 `usage_count += 1`(月度审计批量回写,非实时;仅 SOURCE-/VOICE-/TOPIC- 种子有此字段)。
4. verified data library 全部 `verified:true`,可直接引用;`SOURCE-*` 等
   `verified: false` 的数据**可被引用但 Gate 会 FLAG**,提示尽快核验。
5. `not_public: true` 的数据**禁止进入文章正文**,仅供 Filter 内部判断。

## .md 与 .json 双形态

- facts/ Verified Data Library:**机器真值 = `asg-verified-data-library.json`**;
  人类索引 = `asg-verified-data-library-README.md`(只读说明,非逐条镜像)。
- sources/ voices/ topics 种子:`.md` 人类真值 + `.json` 机器真值,两者必须同步,
  冲突在月度审计对齐。

## 文件清单

```
facts/asg-verified-data-library.json          ★ canonical SSOT(71 条,ASG-{CAT}-{NNN})
facts/asg-verified-data-library-README.md     人类索引
facts/asg-canonical-data.{md,json}            ⚠ DEPRECATED 种子(FACT-*,已废弃,见文件内)
cases/README.md                               真实案例索引(指向 verified library customer_cases)
cases/{cases.md,index.json}                   ⚠ DEPRECATED 种子(CASE-*,已废弃,见文件内)
sources/authority-pool.md + .json             外部权威源池(SOURCE-*,按类目)
voices/customer-voices.md + .json             客户问题/异议/反馈(VOICE-*,脱敏)
```

> ⚠ `facts/asg-canonical-data.*` 与 `cases/{cases.md,index.json}` 是 `verified:false`
> 旧种子,已于 2026-05-16 废弃,ID 故意不再可解析;真实数据在 verified data library。
> 迁移对照见 `data/migrations/id-crosswalk.md`。
