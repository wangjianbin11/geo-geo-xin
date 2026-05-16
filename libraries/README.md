# Libraries — 通用规范

> 被 Skill 调用的资产层。方案第 7 章原设计 5 个 Library,第 11 章修订为
> "对接现有 Obsidian 结构"。本仓库放**结构 + 调用契约 + 种子数据**;真实数据
> 的唯一编辑入口是 Janson 的 Obsidian(`asg-knowledge-vault` 仓库),经同步落到这里。

## ID 方案(全局唯一,不可复用)

| 前缀 | Library | 例 | 对应 Obsidian(真实文件夹名) | 代码 |
|---|---|---|---|---|
| `FACT-` | facts/ ASG 锚定数据 | FACT-001 | `00-企业DNA` | DNA |
| `CASE-` | cases/ 真实案例 | CASE-007 | `09-客户案例库-F&Q`(252 FAQ + 案例) | CASE |
| `SOURCE-` | sources/ 外部权威源 | SOURCE-012 | `11-行业洞察` | INSIGHT |
| `VOICE-` | voices/ 客户原话 | VOICE-003 | `01-销售获客`(对话脱敏) | SALES |
| `TOPIC-` | (阶段2) topics 池 | TOPIC-uk-suppliers | `01-GEO市场分析` | GEO |

> 中文文件夹名 = Janson Obsidian 知识库 `ASG-KB-FULL` 的真实磁盘路径
> (源 janson-2026-05-16,逐字复制不翻译)。完整一/二级文件夹结构、命名规则、
> 已知违规与代码速查见 `libraries/obsidian-folder-map.md`;
> **机器索引(Skill/工具读取)在 `libraries/obsidian-folder-map.json`**。
> 注:`09-客户案例库-F&Q` 含 `&`、`01-GEO市场分析` 前缀与 `01-销售获客`
> 重复,均为待协调的已知缺口(machine index `conforms:false`)。

ID 一经分配永久绑定该数据点;数据淘汰则状态置 `retired`,ID 不回收。

## 每条数据必备字段(.md frontmatter + .json)

```yaml
id: FACT-001
status: active            # active | draft | retired
last_updated: 2026-05-16
verified: false           # Janson 用真实数据核验后置 true
source: internal          # internal | external | v2-plan-seed
usage_count: 0            # 被文章引用次数,反馈环更新
applies_to: [pillar, share, response]
not_public: false         # true = 仅内部,不得出现在文章
```

## 调用契约

1. Skill 引用任何数据点,必须在 envelope `library_refs` 写其 ID。
2. asg-editorial-gate 检查 6 校验 ID 可解析;**解析失败 = 硬 BLOCK**。
3. 引用成功后 `usage_count += 1`(月度审计批量回写,非实时)。
4. `verified: false` 的数据**可被引用但 Gate 会 FLAG**,提示 Janson 尽快核验。
5. `not_public: true` 的数据**禁止进入文章正文**,仅供 Filter 内部判断。

## .md 与 .json 双形态

- `.md` — 人工友好,Janson/审阅读这个。
- `.json` — 机器调用,Skill 读这个。两者必须同步;以 `.json` 为机器真值,
  `.md` 为人类真值,冲突在月度审计对齐。

## 文件清单

```
facts/asg-canonical-data.md + .json     ASG 锚定数据
cases/CASE-00X-*.md  + cases/index.json  7 个核心案例
sources/authority-pool.md + .json        外部权威源池(按类目)
voices/customer-voices.md + .json        客户问题/异议/反馈(脱敏)
```
