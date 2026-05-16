# CHANGELOG

所有版本变更记录于此。版本语义见方案第 10.4 节:初版均为 v0.1(能用,不完美)。

## [Unreleased] — Verified Data Library + 框架复盘加固 (2026-05-16)

### Added
- `libraries/facts/asg-verified-data-library.json` —— Janson 71 条已核验真实
  数据(15 类),采纳 `ASG-{CATEGORY}-{NNN}` 为 canonical ID 方案(SSoT)。
- `data/migrations/id-crosswalk.md` —— 种子 FACT-/CASE- → 真实 ASG-* 权威映射。
- `workflows/framework-review-2026-05-16.md` —— 资深架构复盘,裁决
  **GO-WITH-FIXES**,含缺陷清单 + 完成度清单 + 本地交接清单。

### Changed (框架加固,据复盘缺陷清单)
- envelope/dossier/validator library_ref 模式扩展接受 ASG-{CAT}-{NNN};
  旧种子库废弃为空 stub,ID 故意不可解析;6 规则文档传播至 canonical 方案;
  ASG-044 样例迁移到真实 ID。validator ID universe 124,**393/393 全绿**。
- P0 修复:pipeline-contract §2 / editorial-gate SKILL / 28-step-flow 文件名
  对齐真实(`03-gate-attempt{N}.json`,无 `06-publish.json`);
  integration-selfcheck 标 superseded;README 修正 43→真实 73/98 + 12 Skill +
  6 规则 + 目录树 + 开发状态。
- P1 修复:publishing-gate Gate 10 基线改真实保留集;Gate 9 + voice-bible §5.1
  把冲突日志(6,000+/Jason/4.2M-5M)变成机器强制扫描点;obsidian §2.2 登记
  monthly-auditor 写回;validator docstring 标注"契约门非质量门"。

## [Unreleased] — 真实数据集成 (2026-05-16, Janson 数据)

> 里程碑:从"骨架 + 种子"进入"真实数据驱动"。Janson 提供 GSC 导出 +
> 3,625 关键词语料 + 真实 Obsidian 文件夹映射。多 agent team 并行处理,中心化集成。

### Added (real data)

- `tools/xlsx_to_csv.py` + `data/sources/`(原始 xlsx + 溯源 README)+
  `data/gsc/`(97 页/952 查询/日/国家/设备)+ `data/keywords/`(3,625 关键词)。
- `data/runs/ASG-AUDIT-001/`(真实存量审计:98 页 KEEP27/UPGRADE26/REWRITE31/
  KILL14)+ `data/articles-stock-audit.csv` —— **阶段 1 验收交付物**。
- `libraries/topics/topics-pool.{json,md}` —— 占位替换为 **42 个真实 Topic**
  (从语料筛选,verified:true / derived:true,P0=3/P1=18/P2=19/P3=2)。
- `data/runs/ASG-KW-001/keyword.json` —— 真实 keyword-researcher 输入 fixture。
- `libraries/obsidian-folder-map.{md,json}` —— 真实 Obsidian 文件夹机器索引;
  `asg-obsidian-knowledge-base-standards.md` 校准至 v0.2(真实文件夹名)。

### Changed (real data)

- `skills/utility/asg-stock-auditor/io-schema.json` —— input 改 `oneOf`:
  article-list 模式 | **gsc-source 模式**(真实阶段 1 路径);audited item
  扩充真实 GSC 字段。修复 Agent 反馈的契约缺口。
- `tools/validate_pipeline.py` —— 自动发现所有 run;新增 standalone 旁路产物
  校验;**388/388 全绿**(覆盖 ASG-044 链 + ASG-AUDIT-001 + ASG-KW-001)。
- `.gitignore` 新增(__pycache__ / tmp_*)。

## [Unreleased] — 阶段 1+2 核心骨架 (2026-05-16)

### Added

- `workflows/v2-development-plan.md` — 13 章完整设计方案落盘,含 0.5 节 n8n 演进预告。
- `schemas/` — n8n 就绪的 JSON 流转契约:envelope / article-dossier / pipeline-contract。
- `rulebooks/` — 6 份规则文档 v0.1:content-constitution / voice-bible /
  publishing-gate / risk-compliance / geo-standards / obsidian-knowledge-base-standards。
- `data/runs/ASG-044/` — 主链端到端 mock 干跑(filter→keyword→draft→gate(BLOCK→fix→PASS)→meta→voice)。
- `tools/validate_pipeline.py` — 零依赖 CI 式校验器:信封合规 + library_ref 解析 +
  next_skill 链路 + 参数表跨文件一致性。260/260 全绿。
- `libraries/` — 5 个 Library 结构 v0.1:facts / cases / sources / voices / topics
  (ID 方案 + frontmatter + 引用计数 + .json 索引)。
- `skills/` — 12 个 Skill v0.1(各含 SKILL.md + io-schema.json + tests/):
  - 主链:strategic-filter / keyword-researcher / seo-writer-v2 / editorial-gate / voice-checker
  - 分发(阶段 3):facebook-page / facebook-groups / short-video-scripter / platform-polisher
  - 旁路反馈:geo-benchmarker(周)/ monthly-auditor(月)/ stock-auditor(一次)
- `workflows/28-step-flow.md` — 解决方案中 `【表格待补】`:28 步全表 + writer 21 步映射。
- `README.md` / `AGENTS.md` — 项目说明与 Skill 调用图。

### Changed

- `schemas/envelope.schema.json` — `skill` 枚举中心化扩展至 12(纳入分发/月审/新增)。
- `tools/validate_pipeline.py` — 扩展:全 12 Skill io-schema lint + enum-todo 已解决
  校验 + Topics 库 ID 解析 + 孤儿 Skill 检测。**344/344 全绿**。

### Notes

- 所有 Library 种子数据标 `verified: false`,需 Janson 用真实运营数据核验。
- 关键词真实数据(KD/搜索量/CPC)必须由 Janson 从外部工具提供;keyword-researcher 不造数据。
- 阶段 1 真实资产沉淀与第 44 篇验证待 Janson 接 GSC + 维护 Obsidian 后进行。
