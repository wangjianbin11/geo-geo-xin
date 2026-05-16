# ASG Content OS v2

英文 SEO + GEO 双优化内容生产系统 — 面向 ASG Dropshipping 业务。

> 设计依据见 `workflows/v2-development-plan.md`(13 章完整方案)。
> 本仓库是方案第 2 章 / 第 11 章定义的**工程仓库 `asg-content-os`**。
> 知识库仓库 `asg-knowledge-vault`(Obsidian 镜像)是独立仓库,不在此处。

## 这是什么

让现有 43 篇验证过的内容体系从"盲打高质量内容"升级为"看见自己 + 持续进化"。

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
rulebooks/
  asg-content-constitution.md  内容宪法(最高约束)
  asg-voice-bible.md           Janson 声音规范
  asg-publishing-gate.md       发布门禁清单(Editorial Gate 执行依据)
libraries/
  README.md                    Library 通用规范(ID 方案 / frontmatter / 引用计数)
  facts/                       ASG 锚定数据库
  cases/                       真实案例库(7 个核心)
  sources/                     外部权威源池
  voices/                      客户声音库
skills/
  pre-production/              asg-strategic-filter / asg-keyword-researcher
  production/                  asg-seo-writer-v2
  quality-control/             asg-editorial-gate / asg-voice-checker
  feedback/                    asg-geo-benchmarker
  utility/                     asg-stock-auditor(一次性)
data/
  runs/                        每篇文章的流转 JSON(由 Skill 读写)
  templates/                   审计/追踪 CSV 模板
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

## 开发状态

- [x] 工程骨架 + JSON 流转契约
- [x] 3 份核心规则文档(v0.1)
- [x] 4 个 Library 结构(v0.1)
- [x] 6 个核心 Skill + stock-auditor(v0.1)
- [ ] 阶段 1 真实数据沉淀(需 Janson 接 GSC + 维护 Obsidian)
- [ ] 第 44 篇 v2 全流程验证

所有产物初版均为 **v0.1 = 能用,不完美**。详见方案第 10.4 节。
