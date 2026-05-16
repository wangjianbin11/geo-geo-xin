# CHANGELOG

所有版本变更记录于此。版本语义见方案第 10.4 节:初版均为 v0.1(能用,不完美)。

## [Unreleased] — 阶段 1+2 核心骨架 (2026-05-16)

### Added

- `workflows/v2-development-plan.md` — 13 章完整设计方案落盘,含 0.5 节 n8n 演进预告。
- `schemas/` — n8n 就绪的 JSON 流转契约:envelope / article-dossier / pipeline-contract。
- `rulebooks/` — 3 份核心规则文档 v0.1:content-constitution / voice-bible / publishing-gate。
- `libraries/` — 4 个 Library 结构 v0.1:facts / cases / sources / voices(ID 方案 + frontmatter + 引用计数 + .json 索引)。
- `skills/` — 7 个 Skill v0.1(各含 SKILL.md + io-schema.json + tests/):
  strategic-filter / keyword-researcher / seo-writer-v2 / editorial-gate /
  voice-checker / geo-benchmarker / stock-auditor。
- `README.md` / `AGENTS.md` — 项目说明与 Skill 调用图。

### Notes

- 所有 Library 种子数据标 `verified: false`,需 Janson 用真实运营数据核验。
- 关键词真实数据(KD/搜索量/CPC)必须由 Janson 从外部工具提供;keyword-researcher 不造数据。
- 阶段 1 真实资产沉淀与第 44 篇验证待 Janson 接 GSC + 维护 Obsidian 后进行。
