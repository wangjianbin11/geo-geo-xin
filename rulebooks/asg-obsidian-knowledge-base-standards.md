---
doc: asg-obsidian-knowledge-base-standards
title: Obsidian 知识库规范
status: v0.2
authority: sub-law
parent: asg-content-constitution
last_updated: 2026-05-16
verified: false
review_cycle: quarterly
applies_to_repo: asg-knowledge-vault
referenced_by: [asg-geo-benchmarker, asg-strategic-filter, asg-keyword-researcher]
---

# Obsidian 知识库规范 (Knowledge Vault Standards)

> 第 6 份规则文档。约束**独立仓库 `asg-knowledge-vault`**(Janson 维护的
> Obsidian 镜像)的结构与同步契约。本工程仓 `asg-content-os` 的 `libraries/`
> 是其机器可读投影;两者经此规范对齐。

---

## Section 1 | 双仓职责边界

**声明.**
- `asg-knowledge-vault`(Obsidian)= Janson 的**人类编辑入口**,真实数据唯一录入处。
- `asg-content-os`(本仓)= **机器执行层**,`libraries/*.json` 是供 Skill 调用的投影。

**铁律.** Skill **不写** Obsidian 真实数据;只读投影。Janson 改 Obsidian →
同步到 `libraries/`(同步机制见 Section 4)。`asg-geo-benchmarker` 是唯一例外:
它把 `COMP-*.md` 周报**写回** Obsidian /10-竞品情报库(产出物,非真实源数据)。

---

## Section 2 | 目录映射(Obsidian → libraries/)

> 本表已按 Janson 提供的真实 Obsidian 知识库 `ASG-KB-FULL` 文件夹名校准
> (源:janson-2026-05-16)。中文文件夹名 = 真实磁盘路径,逐字复制,不翻译、
> 不臆造。**机器索引见 `libraries/obsidian-folder-map.json`**(对应人类索引
> `libraries/obsidian-folder-map.md`),新增/重命名文件夹以该机器索引为准。

### 2.1 核心投影(Skill 只读)

| Obsidian 真实文件夹 | 代码 | libraries/ 投影 | ID 前缀 |
|---|---|---|---|
| `00-企业DNA` | DNA | `libraries/facts/` | `FACT-` |
| `09-客户案例库-F&Q` | CASE | `libraries/cases/`(252 FAQ + 客户案例) | `CASE-` |
| `11-行业洞察` | INSIGHT | `libraries/sources/` | `SOURCE-` |
| `01-销售获客`(对话脱敏) | SALES | `libraries/voices/` | `VOICE-` |
| `01-GEO市场分析` | GEO | `libraries/topics/`(阶段2 主题池) | `TOPIC-` |

### 2.2 写回 / 产出物投影(非真实源数据)

| Obsidian 真实文件夹 | 代码 | 谁写 | 命名 |
|---|---|---|---|
| `10-竞品情报库` | COMPETE | `asg-geo-benchmarker` 写回 | `COMP-YYYY-Www` |

`distribution` 类 Skill 的成稿按平台分发回 `内容输出库`(代码 CONTENT,无前缀):

| Obsidian 子文件夹 | 代码 | 产出 Skill |
|---|---|---|
| `内容输出库/Facebook` | CONTENT.FACEBOOK | `asg-facebook-page` / `asg-facebook-groups` |
| `内容输出库/领英` | CONTENT.LINKEDIN | linkedin 分发 |
| `内容输出库/推特` | CONTENT.TWITTER | twitter 分发 |
| `内容输出库/YouTube` | CONTENT.YOUTUBE | `asg-short-video-scripter`(youtube 暂缓) |
| `内容输出库/seo 谷歌文章` | CONTENT.SEO | `asg-seo-writer-v2` 成稿 |

新增 Obsidian 文件夹须先登记到 `libraries/obsidian-folder-map.*` 并在此表
反映后,才允许被 Skill 引用。

### 2.3 待协调的已知缺口(known gaps to reconcile)

下列文件夹**不符合命名规则**,机器索引中 `conforms:false`,Skill 引用前
须人工确认目标路径稳定(详见 `obsidian-folder-map.md` §2.4):

- `09-客户案例库-F&Q` 含 `&` → 应为 `09-客户案例库-FAQ`(投影源,优先重命名)。
- `01-GEO市场分析` 与 `01-销售获客` 前缀重复,拟并入 `11-行业洞察`。
- `内容输出库` 无数字前缀(建议 `12-内容输出库` 或保留);`内容输出库/seo 谷歌文章` 含空格。
- `ip知识库` 刻意保持独立(例外保留);`asg 的销售教程` 含空格 + 无前缀;
  `西哥有绝招_副本` 含 `副本`;`ASG_Content` 英文 + 无前缀(空目录)。

文件夹一旦重命名为合规名,须**同步更新** `obsidian-folder-map.*` 与本表的
`real_name`,且保持投影 `id` 稳定(同步契约见 Section 4)。

---

## Section 3 | 笔记 frontmatter 规范

每条可被引用的 Obsidian 笔记必须含与 `libraries/README.md` 一致的 frontmatter:

```yaml
id: FACT-001            # 全局唯一,永不复用
status: active          # active | draft | retired
verified: true|false    # Janson 核验真实运营数据后 true
source: internal|external
last_updated: YYYY-MM-DD
not_public: false       # true=仅内部,禁入文章
usage_count: 0          # 月度审计回写
```

**声明.** 无合法 `id` 的笔记 = 不可被 Skill 引用(Gate 6 解析必失败 → BLOCK)。

---

## Section 4 | 同步契约(Obsidian ⇄ libraries/)

**声明.** 以 `.json` 投影为机器真值,Obsidian 为人类真值;冲突在**月度审计**对齐。

1. Janson 在 Obsidian 增改数据 → 月度(或临时)同步:更新对应 `libraries/*.json`
   + `.md`,commit 注明同步来源与日期。
2. 同步必须保 `id` 稳定;数据淘汰 → `status: retired`,**ID 不回收**。
3. `usage_count` 由月度审计从 `data/runs/**` 统计回写两侧。
4. 同步缺口(Obsidian 有、投影无)会导致 Skill 引用 BLOCK —— 这是**预期的安全
   失败**,提示该同步,不是 bug。

---

## Section 5 | benchmarker 写回规范

`asg-geo-benchmarker` 写 `/10-竞品情报库/COMP-<YYYY-Www>.md`:
- 命名固定 `COMP-YYYY-Www`(周序),便于累积与检索。
- frontmatter 含 `id: COMP-2026-W21` / `week` / `target_keywords` / `ai_cited`。
- 仅追加,不改历史周报;规则修订提案另存,人工合入规则文档。

---

## Section 6 | 命名与链接卫生

- 文件名英文 + 短横线;ID 在 frontmatter 不在文件名(文件名可改,ID 不可变)。
- Obsidian 双链 `[[...]]` 仅供人类导航,**不作为 Skill 解析依据**(Skill 只认
  frontmatter `id`)。
- 客户脱敏在录入 Obsidian 时即完成(risk-compliance §2),投影不做二次脱敏。

## 版本历史
| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-05-16 | 初版 6 Section。确立双仓边界 + 目录映射 + 同步契约 + benchmarker 写回。待 Janson 按真实 Obsidian 文件夹名校准 Section 2 映射表。 |
| v0.2 | 2026-05-16 | Section 2 按 janson-2026-05-16 真实文件夹名校准(中文名为真实磁盘路径);新增 distribution 产出物投影与「待协调的已知缺口」;引入机器索引 `libraries/obsidian-folder-map.{md,json}` 为登记权威。 |
