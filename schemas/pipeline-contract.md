# Pipeline Contract — Skill 间 JSON 流转契约

> 这份文档定义所有 Skill 如何通过 JSON 文件串联。它是 v2.1 n8n 化的前置设计。
> **铁律:Skill 之间只通过 JSON 文件通信,不通过对话。** 任何 Skill 给定一个
> 合法输入 JSON,必须能独立运行出合法输出 JSON,无需会话上下文。

## 1. 两类 JSON 对象

| 对象 | Schema | 作用 |
|---|---|---|
| **Envelope** | `schemas/envelope.schema.json` | 单个 Skill 的一次调用包装。带元数据(skill/version/status/next_skill/library_refs/audit)。Skill 读 `input`,写 `output`。 |
| **Dossier** | `schemas/article-dossier.schema.json` | 一篇文章随流程累积的主对象。每个 Skill 写自己那一节,后续 Skill 读前面节。 |

Envelope 是"一次调用",Dossier 是"一篇文章的全程档案"。Skill 既更新 Dossier
对应节,也产出一个独立 Envelope(便于独立调用 / n8n 单节点测试)。

## 2. 文件布局

每篇文章一个目录:

```
data/runs/<article_id>/
  dossier.json              主档案(随流程累积)
  00-filter.json              asg-strategic-filter 的 envelope
  01-keyword.json             asg-keyword-researcher 的 envelope
  02-draft.json               asg-seo-writer-v2 (Steps 1-19) 的 envelope
  03-gate-attempt{N}.json     asg-editorial-gate 的 envelope(每次评审一份;
                              modify/blocked→重试产生 attempt2…,见 §4)
  04-meta.json                asg-seo-writer-v2 (Step 21 Meta) 的 envelope;
                              publish_package(meta variants)写入 dossier
  05-voice.json               asg-voice-checker 的 envelope
  ...
```

> **文件名契约(权威,以真实 run 为准)。** Editorial Gate 是带重试回路的检查,
> 故按 `03-gate-attempt1.json` / `03-gate-attempt2.json` … 编号(N=评审轮次),
> **不存在单一 `03-gate.json`**。Step 23「打包」在 v0.1 **不单独产 envelope**:
> publish_package 由 04-meta 阶段直接写入 `dossier.publish_package`。若未来需要
> 独立打包信封,约定文件名 `06-publish.json`(当前 worked example 不产出)。

非文章类 Skill 用自己的 task id 目录:

```
data/runs/ASG-BM-2026W21/    asg-geo-benchmarker 周报
data/runs/ASG-AUDIT-001/     asg-stock-auditor 一次性审计
```

## 3. 标准调用流程(28 步映射)

```
[新话题]
  → asg-strategic-filter
      读: {topic} + Topics Pool + Performance + Cluster Map
      写: 00-filter.json, dossier.filter_report, dossier.article_type
      status: ok(GO) | modify(MODIFY) | blocked(KILL)
      human_gate: true   ← 确认点 ① Filter GO 决定
  → asg-keyword-researcher
      读: dossier.filter_report + Janson 提供的外部关键词数据
      写: 01-keyword.json, dossier.keyword_spec
      status: ok | flagged(外部数据缺失,降级模式)
  → asg-seo-writer-v2 (Steps 1-19)
      读: dossier.keyword_spec + filter_report + Libraries + Rulebooks
      写: 02-draft.json, dossier.draft (html + rank_math + asset_manifest + h2_blocks)
      human_gate: true   ← 确认点 ② 标题 + 大纲锁定 (Step 14)
  → asg-editorial-gate (Step 20)
      读: dossier.draft + asg-publishing-gate.md + Libraries
      写: 03-gate-attempt{N}.json, dossier.gate_report
      status: ok(PASS) | modify(1-2 轻微) | blocked(≥3 或硬伤)
      human_gate: true   ← 确认点 ③ Editorial Gate 决定
  → asg-seo-writer-v2 (Step 21 Meta)
      写: 04-meta.json, dossier.publish_package(meta variants)
  → asg-voice-checker (Step 22)
      读: dossier.draft + asg-voice-bible.md
      写: 05-voice.json, dossier.voice_report
      status: ok(PASS) | flagged(FLAG)
  → [Step 23 打包] → [Step 24 分发, human_gate ④] → [Step 25-27 反馈]
```

旁路 Skill(独立触发,不在主链):

- `asg-geo-benchmarker` — 每周触发,读竞品 URL + Obsidian /10-竞品情报库,写周报,产出规则修订建议。
- `asg-stock-auditor` — 一次性,读 43 篇 URL + GSC 数据,写审计表。

## 4. status 语义(编排器据此决定下一步)

| status | 含义 | 编排器动作 |
|---|---|---|
| `ok` | 通过 | 运行 `next_skill`(若 `human_gate` 则先等人确认) |
| `modify` | 轻微未达标 | 同一 Skill 自动修复后重跑;二次仍不过 → 升 `blocked` |
| `flagged` | 可继续但需人看 | 继续 `next_skill`,但标记待人审 |
| `blocked` | 硬停 | 停,`next_skill=null`,返回 Janson 决定(修改/重写/弃稿) |
| `error` | Skill 运行失败 | 停,记录 `audit.errors`,人工介入 |

## 5. Library 引用契约

- 任何 Skill 引用 ASG 数据/案例/权威源,必须在 `library_refs` 列出其 ID(`FACT-001`/`CASE-007`/`SOURCE-012`/`VOICE-003`/`TOPIC-...`)。
- `asg-editorial-gate` 检查 6 会校验每个 `library_refs` 项能在 `libraries/` 里解析到;解析不到 → **硬 BLOCK**。
- 这条契约是"强制复用资产、杜绝凭记忆编数据"的技术落点。

## 6. n8n 映射说明(v2.1,当前不实现)

| v2 概念 | n8n 对应 |
|---|---|
| 一个 Skill | 一个 n8n 节点(Code / HTTP / Claude 节点) |
| Envelope JSON | 节点的 input/output item |
| Dossier JSON | 在节点间流动的合并 item(或挂到 workflow static data) |
| `next_skill` | n8n 的连线 / Switch 节点按 `status` 分支 |
| `human_gate` | n8n Wait / Approval 节点 |
| `data/runs/<id>/` | n8n 的执行存储 / 外部对象存储(S3/GitHub) |
| Library 解析 | n8n 读 `asg-knowledge-vault` 仓库或 Obsidian webhook |
| Benchmarker 周触发 | n8n Cron 节点 |

设计要求:**每个 Skill 的逻辑不得依赖"前面对话说过什么",只能依赖输入 JSON。**
这样迁移 n8n 时,Skill 逻辑可整段搬进 Code 节点,无需重写。
