---
doc: 28-step-flow
status: v0.1
last_updated: 2026-05-16
source: consolidates workflows/v2-development-plan.md + schemas/pipeline-contract.md
---

# 28-Step Content Flow — 流程总表（解 plan 中的【表格待补】)

## 0. 本文档定位（先读这段)

`workflows/v2-development-plan.md` 在多处用 `【表格待补：...】` 占位,把原飞书
文档里的对照表挪掉了。本文档把其中**与 28 步流程直接相关的表**补齐为可读文档。

**这是文档(documentation),不是新契约(contract)。** 权威契约仍然是,且只是:

- `schemas/envelope.schema.json` — 单次调用信封结构
- `schemas/pipeline-contract.md` — Skill 间 JSON 流转规则、status 语义、文件布局
- `rulebooks/asg-publishing-gate.md` §A — 三类型参数表(Single Source of Truth)

本文档与上述如有出入,**以契约为准**;本文遇到 plan 与契约不一致时,按
pipeline-contract.md 走并加脚注说明(见文末「一致性脚注」)。

本文解掉的 plan 占位:
§3.2「21-Step Workflow Upgrade Mapping 完整映射表」、§3.3「8 个新增步骤说明表」、
§4.2「28 步完整设计表」、§3.1「21 步升级 4 类动作总体策略表」(以流程视角覆盖)。

阶段划分(plan §4.1):Phase A 写前 / Phase B 核心写作 / Phase C 质控 /
Phase D 发布分发 / Phase E 反馈循环。三类型流程长度:**pillar 28 步 / share 25 步 /
response 22 步**(数值与归属见 publishing-gate §A,本文不另定义)。

主链 7 个 Skill + 2 个旁路 Skill(geo-benchmarker 周触发 / monthly-auditor 月触发);
status 枚举固定为 `[ok, blocked, flagged, modify, error]`(pipeline-contract §4);
4 个 human_gate:① Filter GO / ② Step 14 标题+大纲锁定 / ③ Step 20 Editorial Gate /
④ Step 24 逐平台分发确认(AGENTS.md)。

---

## 1. Table 1 — 完整 28 步流程

列说明:**status 取值**列只列该步可能出现的 envelope status;**next** 指
status=ok(或可继续)时的下一步;**三类型差异**列标注 share(25)/response(22)
相对 pillar(28)精简或减负的步骤。**信封文件**列把行绑定到
`data/runs/<id>/NN-*.json`(worked example = 真实 run `data/runs/ASG-044/`)。

| Step# | 阶段 | 名称 | 负责 Skill | 输入 | 输出/产物 | status 取值 | next | human_gate | 三类型差异 | 信封文件(ASG-044) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | pre-production | Strategic Filter 战略筛选 | asg-strategic-filter | `{topic}` + Topics Pool + 90d Performance + Cluster Map | filter_report(6 维评分/decision/类型推荐/cluster/priority/risk) | ok(GO) / modify(MODIFY) / blocked(KILL) / error | asg-keyword-researcher（blocked→null) | **① Filter GO 决定** | 三类型共有(类型在此决定) | `00-filter.json` |
| 0.5 | pre-production | Keyword 规范化 | asg-keyword-researcher | filter_report + Janson 外部关键词数据(Ahrefs/SEMrush) | keyword_spec(主词/密度计划/SEO+GEO 放置/共现/cluster 关系) | ok / flagged(degraded:外部数据缺失,标 estimated) | asg-seo-writer-v2(draft) | — | 三类型共有(密度计划按类型查 §A) | `01-keyword.json` |
| 1 | production | 搜索意图确认 | asg-seo-writer-v2 | keyword_spec + filter_report | 意图判定 | (并入 02-draft 的 ok/error) | Step 2 | — | 共有 | (并入 `02-draft.json`) |
| 2 | production | SERP + PAA 抓取 | asg-seo-writer-v2 | SERP/PAA + Voices Library | PAA 清单 | 同上 | Step 3 | — | 共有 | 同上 |
| 3 | production | 受众与旅程定位 | asg-seo-writer-v2 | filter_report 旅程位置 | 受众画像 | 同上 | Step 4 | — | 共有 | 同上 |
| 4 | production | SERP 差距分析 | asg-seo-writer-v2 | SERP + Cases Library(强制) | 差距清单 | 同上 | Step 5 | — | 共有 | 同上 |
| 5 | production | ASG 独家差异化 | asg-seo-writer-v2 | Cases/Facts Library(强制真实案例,禁想象) | 差异化主张 | 同上 | Step 6 | — | 共有 | 同上 |
| 6 | production | 资产清单 | asg-seo-writer-v2 | Facts/Cases/Authority/Voices | asset_manifest 初稿 | 同上 | Step 7 | — | 共有 | 同上 |
| 7 | production | 大纲构建(每 H2 标 Library ID) | asg-seo-writer-v2 | 资产清单 + §A H2 数 | 带 Library 标注的大纲 | 同上 | Step 8 | — | share/response H2 数较少(§A: pillar 6–7 / share 5–6 / response 3–4) | 同上 |
| 8 | production | 内链(Cluster Map) | asg-seo-writer-v2 | keyword_spec.cluster_relations / Cluster Map | 内链清单 | 同上 | Step 9 | — | 内链下限按 §A(pillar≥4 / share≥3 / response≥2) | 同上 |
| 9 | production | 外链(Authority Pool) | asg-seo-writer-v2 | Authority Pool(SOURCE-) | 外链清单 | 同上 | Step 10 | — | 外链下限按 §A(pillar≥10 / share≥8 / response≥5) | 同上 |
| 10 | production | ASG 一手数据嵌入 | asg-seo-writer-v2 | Facts+Cases(必带 ID) | asg_data_refs(FACT-/CASE-) | 同上 | Step 11 | — | 数据/案例下限按 §A(pillar≥9/≥2 等) | 同上 |
| 11 | production | 分段写作(每 H2 + Answer Block) | asg-seo-writer-v2 | 大纲 + Library + voice-bible | H2 正文(GEO Answer Block) | 同上 | Step 12 | — | 共有(篇幅按 §A 字数) | 同上 |
| 12 | production | 每 H2 Key Takeaway | asg-seo-writer-v2 | H2 正文 | KT 段 | 同上 | Step 13 | — | 共有 | 同上 |
| 13 | production | 5 标题候选(附历史 CTR) | asg-seo-writer-v2 | Performance(无则 no-history) | title_options[5] | 同上 | Step 14 | — | 共有 | 同上 |
| 14 | production | **标题 + 大纲锁定** | asg-seo-writer-v2 | title_options + 大纲 | 锁定的标题+大纲 | 同上 | Step 15 | **② 标题+大纲锁定** | 共有(三类型都必须锁) | 同上 |
| 15 | production | 正文完成 | asg-seo-writer-v2 | 锁定大纲 | 全文 HTML 主体 | 同上 | Step 16 | — | 共有 | 同上 |
| 16 | production | 4 Schema embed | asg-seo-writer-v2 | §A Schema 组合 | schema_blocks | 同上 | Step 17 | — | Schema 组合按 §A(response 仅 Article+FAQ+Breadcrumb) | 同上 |
| 17 | production | Rank Math 设置 | asg-seo-writer-v2 | focus keyword | rank_math_settings | 同上 | Step 18 | — | 共有 | 同上 |
| 18 | production | HTML 组装 | asg-seo-writer-v2 | 全文 + Schema + 设置 | 完整 WordPress HTML | 同上 | Step 19 | — | 共有 | 同上 |
| 19 | production | draft 信封产出 | asg-seo-writer-v2 | draft 全量 | `draft{html,rank_math,asset_manifest,h2_blocks,schema_blocks}` | ok / error | asg-editorial-gate | (承接 ② 已在 Step 14) | 共有 | `02-draft.json` |
| 20 | quality-control | **Editorial Gate 强制审核** | asg-editorial-gate | draft + publishing-gate §A/§B + Libraries | gate_report(10 项 checks/decision) | ok(PASS) / modify(1–2 轻微,自动修复重跑) / blocked(任一 BLOCK 或 MODIFY≥3) / error | asg-seo-writer-v2(meta)（blocked→null) | **③ Editorial Gate 决定** | 阈值按 §A 类型(密度/链接/数据下限不同) | `03-gate-attempt1.json` → `03-gate-attempt2.json` |
| 21 | production | Meta Description ×3 | asg-seo-writer-v2 | 成稿 + Performance(无则 no-history) | meta_variants[3] | ok / error | asg-voice-checker | — | 共有 | `04-meta.json` |
| 22 | quality-control | Voice Checker 声音核查 | asg-voice-checker | 成稿 HTML + voice-bible | voice_report(5 项 checks) | ok(PASS) / flagged(FLAG,可继续) | Step 23 打包 | — | 共有(密度阈值按 voice-bible §2 类型) | `05-voice.json` |
| 23 | publishing | Publish 工程化打包 | (打包步,无独立 Skill) | dossier.draft + publish_package | 发布包(HTML+Meta+canonical) | ok / error | Step 24 | — | 共有 | `06-publish.json`(layout 见 contract §2) |
| 24 | publishing | 平台分发(逐平台确认) | 分发 Skills(见下) | 发布包 + article_type + language | 各平台文案/脚本 | ok / error | Step 25 | **④ 逐平台分发确认** | pillar 长视频+5 平台 / share 短视频+Twitter thread / response 短视频+FAQ 拆解(§A「适配分发」) | `24a/24b/24c/24d-*.json` |
| 24a | publishing | Facebook Page 改写 | asg-facebook-page | 发布包 | FB Page 帖 | ok | asg-platform-polisher | ④(对外发布前确认) | 共有 | `24a-facebook-page.json` |
| 24b | publishing | Facebook Groups 改写(反 spam) | asg-facebook-groups | 发布包 | 社群友好帖(链接进评论区) | ok | asg-platform-polisher | ④ | 共有 | `24b-facebook-groups.json` |
| 24c | publishing | 短视频脚本 | asg-short-video-scripter | 发布包 | 脚本 + shot list | ok | asg-platform-polisher | 否(内部生产物,不直接对外) | 三类型都要短视频 | `24c-short-video.json` |
| 24d | publishing | 逐平台精修(收尾) | asg-platform-polisher | 上游某平台文案 | 精修后文案 | ok | Step 25 | ④(对外发布前确认) | 长度/蒸馏按 §A 类型 | `24d-platform-polish.json` |
| 25 | feedback | Performance 写入 | asg-monthly-auditor | 该篇 ref+topic_id + 月度 metrics(GSC 风格) | 逐篇 action | ok(full) / flagged(basic:无 metrics) | Step 26 | — | 共有(月度集中,非单篇阻塞) | `data/runs/ASG-MA-<YYYY-MM>/monthly-audit.json` |
| 26 | feedback | 30 天后表现检查 + 选题池动作 | asg-monthly-auditor | 同上累积 | topics_pool_actions / KEEP·UPGRADE·REWRITE·KILL | ok / flagged | Step 27 | — | 共有 | 同上 |
| 27 | feedback | 月度数据回流 + 规则修订建议 | asg-monthly-auditor | 全月聚合 | rulebook_revision_proposals / library_writeback / CSV / Obsidian 月报 | ok / flagged | 反哺 Step 0(闭环) | — | 共有 | 同上 + `data/articles-performance-<month>.csv` |

> 旁路(不在主链,不计入 22/25/28 步):`asg-geo-benchmarker`(每周手动,
> 产 geo-standards/publishing-gate 修订建议,`data/runs/ASG-BM-<week>/benchmark.json`);
> `asg-stock-auditor`(一次性,43 篇审计,`data/runs/ASG-AUDIT-001/audit.json`)。
> 二者 `next_skill: null`、`human_gate: false`,见 pipeline-contract §3 旁路段。

**关于「步数 22/25/28」的解读:** §A 规定 pillar=28(完整)/ share=25 / response=22。
精简不是删上表的行,而是按 §A 在 Phase B 减负(更少 H2 / 更低链接与数据下限 /
Schema 组合更短:response 无 HowTo/ItemList)并在 Phase D 走更轻的分发组合
(share=短视频+Twitter thread;response=短视频+FAQ 拆解)。**4 个 human_gate
对三类型都强制保留**——精简的是工作量,不是确认点。精确步数差异以 §A 为准。

---

## 2. Table 2 — asg-seo-writer-v2 内部 21 步映射

把 `skills/production/asg-seo-writer-v2/SKILL.md` 第 4 节展开为 Steps 1–19 + 21
(Step 20 = Editorial Gate,不属 writer;Step 22 = Voice Checker,不属 writer)。
「锁定点」列只在 Step 14 标 human_gate ②。

| WriterStep# | 名称 | 做什么 | 引用的 Rulebook/Library | 对应 28-step | 锁定点 |
|---|---|---|---|---|---|
| 1 | 搜索意图确认 | 据 keyword_spec.intent 定文章意图 | keyword_spec | Step 1 | — |
| 2 | SERP + PAA | 抓 PAA,比对客户真实问题 | Voices Library | Step 2 | — |
| 3 | 受众与旅程 | 定位读者在客户旅程的位置 | filter_report | Step 3 | — |
| 4 | SERP 差距分析 | 找现有结果没覆盖的角度 | Cases Library(强制) | Step 4 | — |
| 5 | ASG 独家差异化 | 用真实案例建立差异主张(禁想象) | Cases + Facts Library | Step 5 | — |
| 6 | 资产清单 | 列将引用的 FACT/CASE/SOURCE/VOICE | Facts/Cases/Authority/Voices | Step 6 | — |
| 7 | 大纲构建 | 按 §A H2 数搭大纲,每 H2 标 Library ID | asg-publishing-gate §A | Step 7 | — |
| 8 | 内部链接 | 从 Cluster Map / cluster_relations 取内链 | Cluster Map | Step 8 | — |
| 9 | 外部权威链接 | 从 Authority Pool 按主题取(SOURCE-) | sources(Authority Pool) | Step 9 | — |
| 10 | ASG 一手数据 | 嵌 FACT-/CASE-,每条带可解析 ID | Facts + Cases Library | Step 10 | — |
| 11 | 分段写作 | 逐 H2 写,每 H2 含 GEO Answer Block | asg-geo-standards / asg-voice-bible | Step 11 | — |
| 12 | Key Takeaway | 每 H2 补 KT 段 | asg-geo-standards | Step 12 | — |
| 13 | 5 标题候选 | 给 5 个,附历史 CTR 参考(无则 no-history) | performance | Step 13 | — |
| 14 | **标题 + 大纲锁定** | 选定标题、冻结大纲,等 Janson 确认 | — | Step 14 | **② human_gate** |
| 15 | 正文完成 | 锁定后写完全文 | asg-voice-bible | Step 15 | — |
| 16 | Schema embed | 按 §A 组合 embed 4 类 Schema | asg-geo-standards / §A | Step 16 | — |
| 17 | Rank Math 设置 | 设 focus keyword 等 | asg-publishing-gate | Step 17 | — |
| 18 | HTML 组装 | 拼完整 WordPress HTML | — | Step 18 | — |
| 19 | draft 信封产出 | 写 dossier.draft,emit 02-draft.json | pipeline-contract §3 | Step 19 | — |
| 21 | Meta Description ×3 | Gate PASS 后生成 3 版 Meta(附 CTR 参考) | performance / asg-voice-bible §9 | Step 21 | — |

> writer SKILL.md §4 把 1–19 概括为 6 个分组(1–3 / 4–5 / 6–7 / 8–10 / 11–14 /
> 15–19)外加 Step 21;上表是其逐步展开,行数与 SKILL.md 分组等价,无新增动作。
> writer 的 5 项 v1→v2 升级落在:Step 7/8(Cluster)、Step 5/4(真实案例)、
> Step 10(强制 Library ID)、Step 13/21(Performance CTR 参考)、全程类型分支查 §A。

---

## 3. 4 个 human_gate 确认点(跳过即失效)

与 AGENTS.md「4 个强制人工确认点」逐条一致:

1. **① Filter GO 决定(Step 0)** — 跳过则 AI 自己说写就写,低价值话题直接进
   28 步流程,plan §0.2 弱项 2 复发(没有写前判断层)。envelope:`00-filter.json`
   `human_gate:true`,blocked(KILL)时 `next_skill:null`。
2. **② 标题 + 大纲锁定(Step 14 / Writer Step 14)** — 跳过则 AI 凭直觉跑完
   全篇,大纲方向无人确认即落地。envelope:`02-draft.json` `human_gate:true`。
3. **③ Editorial Gate 决定(Step 20)** — 跳过则质量没底线,不合格内容进入
   发布。envelope:`03-gate-*.json` `human_gate:true`;BLOCK→返回 Janson
   决定(改/重写/弃稿)。ASG-044 第 1 次 BLOCK(Gate 1+Gate 5)、自动修复后
   第 2 次 PASS,证明 Gate 真在咬人(非橡皮图章)。
4. **④ 平台分发逐个确认(Step 24)** — 跳过则错误内容被批量扩散到多平台。
   24a/24b/24d `human_gate:true`(对外发布前逐平台确认);24c 短视频脚本是
   内部生产物 `human_gate:false`,但其精修产物经 24d 仍受 ④ 约束。

---

## 4. 未覆盖 / 待 Janson(依赖真实外部输入,本文不杜撰)

以下流程节点的真实数据**必须由 Janson 从外部提供**,系统不编造(宪法 Art.4,
pipeline-contract §5,各 Skill「真实形态澄清/降级模式」段):

- **Step 0.5 外部关键词数据** — KD / 月搜索量 / CPC / 意图,来自
  Ahrefs / SEMrush / DataForSEO / Keywords Everywhere。缺失 → keyword-researcher
  降级 `degraded` 模式(status=flagged,指标标 `estimated:true`),不阻塞流程。
- **Step 13 / Step 21 历史 CTR 数据** — Performance 库无历史时 writer 标
  `ctr_reference:"no-history"`(ASG-044 即如此),非凭空给数字。
- **Step 25–27 月度 metrics** — clicks / impressions / avg_position /
  featured_snippet / ai_cited / inquiries,GSC 风格外部输入;缺失 →
  monthly-auditor 降 `basic` 模式(status=flagged,仅凭排名+人工 AI 核查)。
- **旁路 Benchmarker 输入** — target_keywords + competitor_urls +
  `ai_citation_evidence`(人工核查 Perplexity/AI Overview 是否引用、引哪段)。
- **旁路 Stock-Auditor 输入** — 43 篇 URL + 可选 GSC/Ahrefs 导出 +
  人工 AI 引用核查 + 询盘归因(Janson 标注);无 GSC 走 basic 模式。
- **真实 Obsidian 文件夹** — `/10-竞品情报库`(benchmarker 写回)、
  `/01-GEO市场分析`(monthly-auditor 月报)、Library 解析依赖
  `asg-knowledge-vault` 镜像。这些目录的真实内容与同步由 Janson 维护
  (plan 第 11 章双仓 + Obsidian Git),本文不假设其具体条目。

> 上述均为「依赖真实输入」而非「设计缺口」:每处都有契约层的降级路径,
> 流程不会因数据缺失而硬停。

---

## 5. 一致性脚注(plan ↔ 契约 的处理)

实施中本文以契约为准,记录如下调和点:

1. **Phase 边界差异。** plan §4.1 写 Phase B = Steps 1–17、Phase C = Steps 18–22。
   但 pipeline-contract §3 + writer/gate/voice-checker frontmatter 明确:
   writer 产 draft 含 Step 19、Step 20 = Editorial Gate、Step 22 = Voice Checker。
   本文 Table 1 的阶段列按**契约 + 各 Skill frontmatter 的 `step` 字段**归位
   (writer=1–19+21、gate=20、voice=22),plan §4.1 的 17/18 边界视为概述性
   描述,不作流程依据。
2. **Filter 阈值表述差异。** plan §0.3/§3.5 用 70/50/百分制;strategic-filter
   SKILL.md 用 60 分制(≥42 GO / 30–41 MODIFY / <30 KILL,等价 70%/50%)。
   本文 Table 1 只写 decision 语义(GO/MODIFY/KILL → ok/modify/blocked),
   不复述分数线,以 Skill io-schema 为准。ASG-044 total=50 → GO,与 Skill 制一致。
3. **「步数 22/25/28」语义。** plan 多处把 share/response 说成「精简 N 步」。
   契约侧(§A + 各 Skill)并不删流程行,而是减 Phase B 工作量 + 走更轻分发。
   本文按契约解释(见 Table 1 末段),步数权威值以 publishing-gate §A 为准。
4. **分发子步 24a–d 编号。** plan §5.3 只画「7 个平台 Skill 并行」,未给子步号;
   本文 24a–d 直接采用各分发 Skill frontmatter 的 `step` 字段(24a/24b/24c/24d),
   不自造编号。Twitter/LinkedIn 适配为阶段 3/迁移项,本波 7 主链 Skill 不含,
   故 Table 1 不展开其行(plan §11.4 / AGENTS.md「阶段 3」说明)。
5. **Step 25–27 归属。** plan §4.1 列为 Phase E 三步,无独立 Skill 名;契约侧由
   旁路 `asg-monthly-auditor`(月度手动、`next_skill:null`、article_id 模式
   `ASG-MA-<YYYY-MM>`)承担。本文据此把 25–27 映射到 monthly-auditor,并注明
   它是月度批处理而非单篇阻塞,因此「反哺 Step 0」是逻辑闭环、非同步调用。

— 完 —
