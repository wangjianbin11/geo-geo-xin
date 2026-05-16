# ASG Content OS v2

英文 SEO + GEO 双优化内容生产系统 — 面向 ASG Dropshipping 业务。

> 设计依据见 `workflows/v2-development-plan.md`(13 章完整方案)。
> 本仓库是方案第 2 章 / 第 11 章定义的**工程仓库 `asg-content-os`**。
> 知识库仓库 `asg-knowledge-vault`(Obsidian 镜像)是独立仓库,不在此处。

## 这是什么

让现有存量内容体系从"盲打高质量内容"升级为"看见自己 + 持续进化"。

> 存量真实规模(来自 `data/runs/ASG-AUDIT-001/` 真实 GSC 审计,2026-05-16):
> **98 个已索引页面,其中 73 个内容文章页**(方案早期假设的"43 篇"已被真实
> 数据修正)。当前权威完成度状态见 `workflows/framework-review-2026-05-16.md`。

三个北极星:

1. **AI 引用(GEO)+ 关键词排名(SEO)双管齐下** — 每篇文章同时为被 AI 引擎引用和搜索排名优化。
2. **看见自己** — 写前 Filter 评分、写后 Gate 报告、30 天表现追踪。
3. **持续进化** — 月度审计 + 每周对标反哺规则。

## 目录结构

```
README.md                      本文件
AGENTS.md                      Skills 索引 + 调用关系图
CHANGELOG.md                   版本记录
workflows/
  v2-development-plan.md       完整设计方案(13 章)
schemas/
  envelope.schema.json         所有 Skill 共用的 I/O 信封(n8n 命脉)
  article-dossier.schema.json  随流程累积的文章主对象
  pipeline-contract.md         Skill 间 JSON 文件流转契约 + n8n 映射说明
rulebooks/                     6 份规则文档(v0.1/v0.2)
  asg-content-constitution.md  内容宪法(最高约束)
  asg-voice-bible.md           Janson 声音规范
  asg-publishing-gate.md       发布门禁清单 + §A 类型参数 SSoT
  asg-risk-compliance.md       风险与合规(落地宪法 5/6/7)
  asg-geo-standards.md          GEO 被引用元素标准
  asg-obsidian-knowledge-base-standards.md  双仓同步契约(已校真实文件夹)
libraries/                     5 个 Library
  README.md                    Library 通用规范(ID 方案 / frontmatter)
  facts/asg-verified-data-library.json  ★ 71 条 Janson 已核验真实数据(canonical SSoT)
  cases/                       客户案例 = facts 库内 ASG-CASE-*(旧种子已废弃)
  sources/ voices/             外部权威源 / 客户原话(种子,待 Janson)
  topics/                      42 条真实主题(取自真实关键词语料)
  obsidian-folder-map.json     真实 Obsidian 文件夹机器索引(路径 SSoT)
skills/                        12 个 Skill(各含 SKILL.md+io-schema.json+tests/)
  pre-production/              asg-strategic-filter / asg-keyword-researcher
  production/                  asg-seo-writer-v2
  quality-control/             asg-editorial-gate / asg-voice-checker
  distribution/                facebook-page / facebook-groups /
                               short-video-scripter / platform-polisher
  feedback/                    asg-geo-benchmarker / asg-monthly-auditor
  utility/                     asg-stock-auditor(一次性)
data/
  runs/                        ASG-044(主链样例)/ ASG-AUDIT-001(真实审计)/ ASG-KW-001
  sources/ gsc/ keywords/      Janson 真实数据 + 提取 CSV + 溯源
  migrations/id-crosswalk.md   种子→真实 ID 权威迁移表
  templates/                   审计/追踪 CSV 模板
tools/
  validate_pipeline.py         零依赖回归门(契约自洽,非质量门)
  xlsx_to_csv.py               GSC/语料提取器
workflows/
  framework-review-2026-05-16.md  ★ 当前权威完成度 + 缺陷清单 + 交接清单
  28-step-flow.md / integration-selfcheck.md(后者已 superseded)
```

## 核心设计原则

1. **单一真实源** — 规则和库的唯一真实源是本仓库 + Obsidian。Skill 不硬编码规则。
2. **执行与定义分离** — Skill 管 how,规则/库管 what。
3. **可追溯** — 所有改动走 Git commit。
4. **接口标准化(n8n 就绪)** — 每个 Skill 输入输出都是 JSON 文件,符合 `schemas/envelope.schema.json`,可独立调用、可被 n8n 编排。**禁止硬编码对话依赖。**

## 怎么用

每个 Skill 是一个目录,含:

- `SKILL.md` — 给 Claude Code / 未来 n8n 节点的执行说明
- `io-schema.json` — 该 Skill 的输入输出 JSON 契约
- `tests/` — 测试用例(输入 JSON + 期望输出断言)

一篇文章的生产 = 按 `AGENTS.md` 的调用关系图,依次用每个 Skill 处理 `data/runs/<article_id>/` 下的 JSON 文件,后一个 Skill 读前一个的输出。

## 开发状态(摘要;权威详情见 framework-review-2026-05-16.md §5)

- [x] 工程骨架 + JSON 流转契约 + 零依赖回归门(validator 393/393 全绿)
- [x] 6 份规则文档 + 12 个 Skill + 5 Library(v0.1/v0.2)
- [x] **真实数据集成**:71 条 Janson 已核验数据(canonical)、真实 GSC、
      3,625 关键词语料、真实 Obsidian 文件夹映射
- [x] 真实存量审计 ASG-AUDIT-001(98 页)+ 主链样例 ASG-044(已迁真实 ID)
- [ ] sources/voices 真实沉淀、Ahrefs 关键词指标、第 44 篇真实跑通(待 Janson)
- [ ] 「看见自己 + 进化」两个北极星:机制已落地,待真实表现数据兑现

裁决 **GO-WITH-FIXES**:框架结构健全、回归门会咬人;v0.1 = 能用,不完美。
交接前必修项与最高 ROI 下一步见 `workflows/framework-review-2026-05-16.md`。
