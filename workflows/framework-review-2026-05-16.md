---
doc: framework-review
title: ASG Content OS v2 — 资深架构复盘
status: review
reviewer: senior-architecture-retrospective
date: 2026-05-16
scope: read-only audit; no other file modified; no commit
verdict: GO-WITH-FIXES
---

# ASG Content OS v2 — 框架结构复盘 (2026-05-16)

> 这是一次**审查**,不是修复。punch list 留给集成者(Janson 本地)分诊。
> 凡无法核实者标「未核实」。Validator 实测:`393 passed, 0 failed`(ALL GREEN)。

---

## 1. 结论先行 (Verdict)

**判定:GO-WITH-FIXES。** 这个框架在结构上是**站得住的**英文 SEO+GEO 内容生产系统:
分层清晰(Rulebooks=what / Skills=how / Libraries=assets / JSON 契约=n8n 命脉 /
feedback=进化),envelope+dossier 双对象是真骨架而非装饰——它被一个零依赖的
validator 实打实校验(393 项全绿,覆盖信封合规、Gate-6 库引用解析、链路 next_skill、
§A 参数表跨文件一致)。真实数据集成(Janson Verified Data Library 71 条 + 真实 GSC +
3,625 关键词语料 + 真实 Obsidian 映射)是这次最大的正确动作,且基本是**干净并入**而非
硬塞:旧种子被显式废弃、ID 故意不可解析、crosswalk 权威映射存在、ASG-044 已按真实 ID
迁移。**最重要的单一理由支持 GO**:系统的核心安全失败(无 Library ID 的 ASG 数字 = 硬
BLOCK)被技术化落点并实测验证,这是整个体系的承重墙,它真的在咬人。**但不是裸 GO**:
存在一批文档漂移(SKILL/pipeline-contract 的 `03-gate.json`/`06-publish.json` 文件名与真实
run 不符、integration-selfcheck 还停在「7 Skill/3 规则/4 库」的旧世界、README「43 篇」对
真实「73/98」),且 validator 有真实盲点(它只校验结构自洽,**不校验 Skill 的语义产物质量**,
也未覆盖去重 Gate10、禁用词 Gate9、密度 Gate2 这类真正决定内容质量的检查)。这些是交接
前必须清掉的「认知地雷」,不影响架构本身。

---

## 2. 架构复盘

### 分层是否成立:成立。

| 层 | 评价 |
|---|---|
| Rulebooks (what) | 6 份齐全,宪法→子法层级清楚,每条三段式+「如何检测」+ `enforced_by` frontmatter 反向声明 Skill 绑定。**连贯。** |
| Skills (how) | 12 个,frontmatter 统一(step/human_gate/enforced_rulebooks/emits/io_schema),SKILL.md 明示「给定 input JSON 独立运行」。**连贯,n8n 就绪意图贯彻到位。** |
| Libraries (assets) | facts 已升级为真实 Verified Data Library(71/15 类);sources(7)/voices(4)/topics(42)仍是种子或派生。**结构连贯,数据成熟度分层(见 §5)。** |
| JSON 契约 | envelope+dossier+pipeline-contract 三件套,status 五态语义统一,validator 强制。**这是最硬的一层。** |
| Feedback | monthly-auditor(月)+ geo-benchmarker(周)+ stock-auditor(一次)旁路设计,`next_skill:null`、不阻塞主链。**逻辑闭环成立,但闭环的「反哺」是月度人工合入,非自动——这是正确的克制。** |

### (a) envelope/dossier 契约是真骨架还是装饰?——**真骨架,实测有效。**

`tools/validate_pipeline.py` 把契约变成可执行回归门:每个 run 信封逐字段校验、每个
`library_refs` 必须在 `libraries/**` 解析(Gate-6 契约的技术落点)、next_skill 串链
(含 gate BLOCK→retry 回路)、§A 参数表与 editorial-gate io-schema `$defs` 逐值核对。
ASG-044 真实跑了 BLOCK→自动修复→PASS,证明 Gate 非橡皮图章。**这是本系统最可信的部分。**

### (b) SSoT 纪律是否真防漂移?——**关键三处防住了,但 SSoT 之外有文件名漂移。**

- ✅ 类型参数 SSoT:publishing-gate §A ↔ editorial-gate io-schema `$defs.article_type_params`
  validator 逐值核对(pillar/share/response 的 word/h2/links/density/refs)实测一致。
- ✅ 数据 SSoT:Verified Data Library 是唯一真值,旧种子 `asg-canonical-data.json` /
  `cases/index.json` 已清空 `data_points`/`cases`(`[]`),故旧 `FACT-*`/`CASE-*` **真的
  不可解析**——这不是说说,是验证过的「预期安全失败」。
- ✅ 路径 SSoT:obsidian-folder-map.json 为机器登记权威,obsidian-standards §2 校准至真实
  中文文件夹名,已知违规(`&`/前缀重复/空格)显式登记 `conforms:false`。
- ⚠️ **SSoT 不覆盖文件名契约**:pipeline-contract §2 与 editorial-gate SKILL.md 写
  `03-gate.json` / `06-publish.json`,但真实 ASG-044 是 `03-gate-attempt1/2.json`,且
  **不存在** `06-publish.json`(publish_package 实际由 04-meta 阶段写入 dossier)。
  validator 用 glob `[0-9]*.json` 自动发现,**绕过了这个矛盾**——所以它绿,但文档说谎。

### (c) 4 人工 gate + status 语义:**连贯。** Filter GO / Step14 大纲锁 / Gate20 / Step24
逐平台,在 AGENTS.md / 28-step-flow §3 / pipeline-contract §3 / envelope.human_gate 四处
一致。status 五态(ok/modify/flagged/blocked/error)→ 编排器动作映射明确。24c 短视频
human_gate=false 但其精修 24d 受 ④ 约束——这个细节是想清楚的。

### (d) 28 步是真的还是 PPT?——**半真。** 28-step-flow.md 把 plan 的 `【表格待补】`
解掉为可执行映射,且诚实地写了「一致性脚注」(Phase 边界、Filter 阈值百分制 vs 60 分制、
22/25/28 步语义)。但**只有 7 主链 Skill 的 ASG-044 路径被真实 run 验证过**;Step 23 打包、
Step 24a-d 分发、Step 25-27 月度,**没有任何真实 run**,只有 tests/cases.json mock。
28 步是「设计成立 + 关键链路验证 + 尾部待跑」,不是纯 PPT,但也别当它全跑通了。

### (e) v1→v2 五项升级是否兑现「看见自己+进化」北极星?——**机制兑现,数据未兑现。**
filter(写前评分)/ gate(写后强制阻断)/ library-ID 强制 / cluster / feedback 五件套
在**机制层全部落地且自洽**。但「看见自己」需要真实 Performance 数据(no-history)、
「进化」需要 benchmarker 连续 4 周真实跑——这两者依赖 Janson 真实输入,目前是
**架空的闭环**(契约都在,数据是空的)。这是设计本身就声明的依赖,不是缺陷;但要清醒:
现在系统能「强制约束 + 复用资产」,还不能「看见自己 + 进化」——后两个北极星是欠条。

---

## 3. 真实数据集成评估

**结论:干净并入(clean adoption),不是硬塞(bolt-on)。** 是这次多 agent pass 里
质量最高的一段工作。

- ✅ Verified Data Library 71 条、15 类、11 字段 schema、`verified` 恒 true、引用优先
  `claim_en`、区间值保区间——规范完整,README 人类索引齐全。
- ✅ 旧种子处理**正确**:`asg-canonical-data.{md,json}` / `cases/{cases.md,index.json}`
  打 `status:deprecated`、JSON 数组清空、ID「故意不可解析(intended)」、crosswalk 权威
  映射存在;宪法「只增不改」靠「历史无已发布文章引用过旧 ID」论证成立——这个论证是诚实的。
- ✅ 半迁移残留检查:ASG-044 dossier 有 `migration_note`,library_refs 全部是真实
  `ASG-*`(实测 13 个 asg_data_refs 全解析),旧 `FACT-011`(珠宝缺陷,真实库无对应)按
  crosswalk **删除**而非硬塞——处理正确。
- ✅ deprecation_and_conflicts_log 三条(客户数 5,000+ 非 6,000+;4.2M 单年 vs 5M+ 累计;
  Janson 非 Jason)在 README、libraries/README、各处反复重申。
- ⚠️ **但这三条「冲突日志」没有任何机器强制点**:validator 不扫文章正文是否写了
  「6,000+」「Jason」,Gate 9 禁用词库(voice-bible §5)也未纳入这三项。它是
  **纪律性约定,不是技术护栏**——ASG-044 narrative 是占位字符串,真实第 44 篇正文里
  写错没人拦。这是真实数据集成里**唯一的实质裂缝**(见 punch list P1)。
- 未核实:`gsc-2026-05-16.xlsx` 原始内容、71 条 claim 与 Janson 真实业务的逐条吻合度
  (审查不重做 Janson 的核验,只看集成纪律);topics 42 条的 P0-P3 派生判断质量(标
  `derived:true` 已诚实声明)。

**仍在编造或假 verified 的地方:无。** 凡 `verified:false`(sources/voices)都诚实标注,
契约规定它们可引用但 Gate 会 FLAG。没有发现「verified:false 伪装成真实」的情况。

---

## 4. 缺陷清单 (Punch List)

### [P0 — 交接前必修]

- **P0-1 文件名契约漂移(认知地雷)。** `schemas/pipeline-contract.md` §2 写
  `03-gate.json` + `06-publish.json`;`skills/quality-control/asg-editorial-gate/SKILL.md`
  frontmatter `emits: 03-gate.json`。**真实 ASG-044 是 `03-gate-attempt1.json` /
  `03-gate-attempt2.json`,且 `06-publish.json` 根本不存在**(publish_package 由 04-meta
  写入 dossier)。后果:Janson 本地按文档手搓 run 会产出与样例不一致的布局,n8n 映射也会
  错。validator 因 glob 自动发现而绿,**掩盖了这个矛盾**。必须三处对齐(契约 / SKILL / 真实
  布局取其一为准)。
- **P0-2 integration-selfcheck.md 整篇过期。** §1/§3.1/§5 仍写「7 个 Skill + 3 规则文档
  + 4 Library」「JSON 文件 20 个」「260/260」,与当前真实状态(12 Skill / 6 规则 / 5 库 /
  393 项)完全脱节。这是给 Janson「总审用」的文档,会直接误导他对完成度的判断。要么重写
  要么显式标 superseded。
- **P0-3 完成度声明漂移(README/CHANGELOG)。** README §9「让现有 **43 篇**…」、§开发状态
  「7 个核心」「第 44 篇验证」;但真实 stock audit(ASG-AUDIT-001)实测是 **98 页 / 73 篇
  文章页**(audit-summary.md 已诚实记录「README said 97, file has 98」「README estimated
  ~90」)。`data/sources/README.md` §1 仍写「~97 个 URL / 约 90 个文章页 / 方案曾假设 43」。
  README.md 顶层「43 篇」是给人看的第一句话,必须改为真实「73/98」,否则 Janson 一打开就
  被旧叙事锚定。

### [P1 — 应修]

- **P1-1 deprecation_and_conflicts_log 无机器强制。** §3 已述:5,000+/4.2M/Janson 三条
  仅口头约定,validator 与 Gate 9 都不扫。建议把 `6,000+` / `Jason` 作为禁用 token 纳入
  voice-bible §5 + Gate 9 扫描(这是 punch list 提示,不在本审查内做)。
- **P1-2 validator 语义盲点。** validator 只证「结构自洽」:它**不**校验 Gate 2(密度)/
  Gate 9(禁用词)/ Gate 10(43→73 篇去重相似度)这些真正决定内容质量的检查是否被 Skill
  执行,也不校验 Skill 输出的语义合理性(ASG-044 的 html 是 `"<article>...~3600 words..."`
  占位字符串,validator 照样绿)。它是「契约回归门」不是「质量门」——交接文档必须讲清这条
  边界,否则 Janson 会误以为「绿 = 内容没问题」。
- **P1-3 Gate 10 基线已失真。** publishing-gate §B Gate 10 写「与已发 43 篇(审计后保留集)
  对比相似度」,但真实保留集是 ASG-AUDIT-001 的 KEEP27+UPGRADE26 等,不是 43。规则文本未
  随真实审计更新。
- **P1-4 monthly-auditor 写回路径未在 obsidian-standards 登记。**
  `asg-monthly-auditor` SKILL.md `emits: Obsidian /01-GEO市场分析/MONTH-<month>.md`,但
  obsidian-standards §2.2「写回/产出物投影」表**只登记了 benchmarker**(`/10-竞品情报库`),
  没有 monthly-auditor 的 `/01-GEO市场分析` 写回项。而 `01-GEO市场分析` 本身又是
  `conforms:false`(前缀与 SALES 重复、拟并入 11)的待协调文件夹——双重隐患。
- **P1-5 28-step-flow §1 表与真实文件名不符。** Table 1 的「信封文件」列写
  `03-gate-attempt1.json → 03-gate-attempt2.json`(对)但同栏 Step 23 写
  `06-publish.json`(不存在,见 P0-1)。文档内部自相矛盾(它对了 gate、错了 publish)。

### [P2 — 锦上添花]

- **P2-1 CHANGELOG 数字过期。** 写「388/388 全绿」「260/260」「344/344」,实测现在 393。
  CHANGELOG 是历史记录可接受滚动,但「Unreleased」段的当前数字应是 393。
- **P2-2 plan 大量 `【表格待补】` 仍在。** v2-development-plan.md §0.3/§1.2/§3.2 等十余处
  占位。28-step-flow 已解掉流程相关的几张,但 plan 本体未回填,读者需自行跳转。
- **P2-3 README 目录树过期。** README §目录结构只画了 7 个 Skill 的旧分组,未含
  distribution/feedback 全量;`rulebooks/` 只列 3 份(实际 6 份)。
- **P2-4 keyword-researcher `pool_status` 枚举与 topics 状态语义不统一。** io-schema 枚举有
  `new/observed/candidate/active/retired/already-active`,但 plan §7.2 定义 Topics 5 态是
  `observed→candidate→trial→active→retired`,`trial` 在 io-schema **缺失**,`already-active`
  /`new` 是 Skill 自造态。topics-pool.json 的 42 条 `status` 字段实测全为 `null`(只有
  `pool_status` 字段)。不阻塞,但状态机定义散在三处不收口。

### [JANSON — 只有 Janson 能做]

- **J-1** Verified Library 71 条与真实业务的逐条复核(审查不替代 Janson 核验)。
- **J-2** sources(7→≥30)/ voices(4→≥20)/ Performance(0→真实 GSC)真实数据沉淀。
- **J-3** 外部关键词数据(Ahrefs/SEMrush)接入——keyword-researcher 不造数,降级模式兜底。
- **J-4** `asg-knowledge-vault` 双仓 + Obsidian Git;`09-客户案例库-F&Q` 等违规文件夹是否
  真重命名(决定 obsidian-standards §2.3 缺口能否关闭)。
- **J-5** 第 44 篇真实全流程跑通(目前只有 mock ASG-044 + 真实 ASG-AUDIT-001 + ASG-KW-001)。

---

## 5. 开发完成度清单 (State Inventory)

state 取值:**real** = 真实数据/已验证可用 / **v0.1** = 骨架可用待迭代 /
**placeholder** = 结构占位 / **Janson-pending** = 等 Janson 真实输入。

| 组件 | state | 一句话 |
|---|---|---|
| schemas/envelope | real | 12 Skill 枚举、五态、library_ref pattern;validator 强制,可靠 |
| schemas/article-dossier | real | 累积主对象,字段完整;但 ASG-044 的 draft.html 是占位串 |
| schemas/pipeline-contract | v0.1 | 契约逻辑对,但 §2 文件名(03-gate/06-publish)与真实 run 不符(P0-1) |
| tools/validate_pipeline.py | real | 393 全绿,结构回归门可靠;**不是质量门**(P1-2) |
| tools/xlsx_to_csv.py | real | 真实 GSC/语料提取已用,可重跑 |
| rulebook: constitution | v0.1 | 8 Article,三段式完整;verified:false(锚定数字待 Janson) |
| rulebook: voice-bible | v0.1 | 10 Section + 禁用词库;密度阈值待校准 |
| rulebook: publishing-gate | v0.1 | §A SSoT + 10 Gate;Gate 10 基线仍写 43(P1-3) |
| rulebook: risk-compliance | v0.1 | 6 Section,落地宪法 5/6/7;红线词待 Janson 补行业特定 |
| rulebook: geo-standards | v0.1 | 8 Section;设计为 benchmarker 每周校准(最快迭代,现未跑) |
| rulebook: obsidian-kb-standards | v0.2 | 已按真实文件夹校准;§2.2 漏登 monthly-auditor 写回(P1-4) |
| lib: facts (Verified Data Library) | real | 71 条/15 类,Janson 核验,canonical SSoT。整库最成熟资产 |
| lib: cases | real(并入) | 5 真实 ASG-CASE-*(并入 facts);旧种子已正确废弃 |
| lib: sources | placeholder | 7 条 SOURCE-*,verified:false,last_verified:null。待 Janson |
| lib: voices | placeholder | 4 条 VOICE-*,verified:false。AI 无法代填,Janson 从真实对话录入 |
| lib: topics | real(派生) | 42 条,指标取自真实语料(verified:true)+ AI 派生选种(derived:true) |
| skill: strategic-filter | v0.1 | 规格+io-schema+4 用例;真跑需真实 Topics/Performance |
| skill: keyword-researcher | v0.1 | 不造数+降级模式;ASG-KW-001 真实 fixture 已验证 |
| skill: seo-writer-v2 | v0.1 | 五项升级规格落地;无真实成稿(html 占位) |
| skill: editorial-gate | v0.1 | 10 Gate + §A 镜像;BLOCK→PASS 真实验证过(ASG-044) |
| skill: voice-checker | v0.1 | 5 检查;mock 验证 |
| skill: geo-benchmarker | v0.1 | 旁路周触发;无真实 run(依赖 Janson 竞品 URL+引用核查) |
| skill: monthly-auditor | v0.1 | 旁路月触发;无真实 run;写回路径未登记(P1-4) |
| skill: stock-auditor | real | **唯一跑过真实数据的主产 Skill**:ASG-AUDIT-001 真审 98 页 |
| skill: facebook-page/groups/short-video/platform-polisher | v0.1 | 阶段 3 分发;仅 mock tests,无真实 run |
| run: ASG-044 | v0.1 mock | 7 主链端到端干跑 + 真实 ID 迁移;html/数字是占位串 |
| run: ASG-AUDIT-001 | real | 真实 GSC 审计,98 页,basic 模式(诚实标 ai_cited:null) |
| run: ASG-KW-001 | real | 真实关键词语料 fixture,指标逐字真实 |
| data: gsc/keywords/sources | real | Janson 2026-05-16 真实导出,溯源 README 齐全 |
| data: id-crosswalk | real | 权威迁移映射,authoritative,论证诚实 |
| data: templates (CSV) | placeholder | 审计/追踪 CSV 模板,空表头 |

---

## 6. 本地交接清单 (Local Handoff Checklist)

**克隆即用的回归门(每次改动后必跑):**

```
git clone <repo> && cd asg-content-os
python3 tools/validate_pipeline.py           # 期望:RESULT: 393 passed, 0 failed / ALL GREEN
```

这一条命令就是 sanity check。**它绿 = 契约自洽(信封/库引用/链路/§A 一致),不等于内容
质量没问题**(见 P1-2)。任何 PR 合并前先跑它;新增 Skill / run / 库条目后它仍须全绿。

**SSoT 文件——禁止随手改(改了要连带改镜像 + 跑 validator):**

1. `rulebooks/asg-publishing-gate.md` §A 类型参数表 —— 改它必须同步
   `skills/quality-control/asg-editorial-gate/io-schema.json` `$defs.article_type_params`
   (validator 逐值核对,不一致直接 FAIL)。
2. `libraries/facts/asg-verified-data-library.json` —— 数据 SSoT,**只增不改**,淘汰置
   `status:retired`,ID 永不回收。
3. `libraries/obsidian-folder-map.json` —— 路径 SSoT,新增/改名文件夹先登记这里。
4. `schemas/envelope.schema.json` 的 skill 枚举 —— 新增 Skill 必须先进枚举,否则
   validator 报 orphan。

**安全扩展点(照 id 规则做,validator 会守门):**

- 加 Skill:建 `skills/<stage>/<name>/{SKILL.md,io-schema.json,tests/}` → io-schema
  `allOf $ref` envelope + `properties.skill.const == 目录名` → 加进 envelope 枚举 + validator
  `IO_SCHEMA` dict。跑 validator,绿即合规。
- 加 Topic:`libraries/topics/topics-pool.json` 追加,id 用 `TOPIC-<slug-kebab>`,指标来自
  真实语料则 `verified:true`,选种判断标 `derived:true`。
- 加 Verified 数据点:只能进 `asg-verified-data-library.json`,id 用 `ASG-{CATEGORY}-{NNN}`
  (15 类前缀见 README),`verified` 恒 true,引用走 `claim_en`,区间值保区间。**不要复活
  `FACT-*`/旧 `CASE-*`(故意不可解析)。**

**接下来必须 Janson 真实输入的:** J-1..J-5(见 §4),其中 GSC 已接(ASG-AUDIT-001 已是
真实),缺的是 Ahrefs/SEMrush 关键词指标 + sources/voices 真实沉淀 + 第 44 篇真实跑通。

**单一最高 ROI 下一步动作:** 不是写第 44 篇。是**先消化 ASG-AUDIT-001 的真实发现**——
audit-summary.md 已经用真实 GSC 指出:Top-10 高展现低点击页(如
`how-long-does-stockx-take-to-ship` 21,925 展现 / 13 点击 / 排名 9.1,UPGRADE/P0)的最快
赢面是**改 title/meta/snippet,不是写新文章**;26 篇 UPGRADE 全部是这类。对一个「内容
已 73 篇但盲打」的系统,先把 3 个 P0 UPGRADE 页用现有 editorial-gate+voice-checker 重做
meta,30 天看 CTR——这是用最小动作验证整套 v2「看见自己」是否真能转成结果的最便宜实验,
且立刻产生真实 Performance 数据反哺空闭环。第 44 篇可以并行,但 ROI 在存量 UPGRADE。

---

## 7. 一句话给 Janson

这套系统的「骨架」是真的、自洽的、有一个会咬人的回归门守着——它已经能强制你
「复用真实资产、不许凭记忆编 ASG 数字、不合格内容硬阻断」,这三件 v1 做不到的事现在
做得到了。还没兑现的是「看见自己 + 自动进化」,因为那要真实表现数据,而那只能你来喂。
**周一早上别急着写第 44 篇**:先打开 `data/runs/ASG-AUDIT-001/audit-summary.md`,挑那 3
个 P0 UPGRADE 页(高展现、几乎零点击、排名第 9-17 名),用现成的 gate+voice-checker 把
它们的 title/meta 重做一遍发出去——这是花一天就能让系统第一次「产生真实反馈数据」的
动作,比从零写新文章便宜十倍。同时让本地 Claude Code 先清掉 P0-1/P0-2/P0-3 三处文档
漂移(文件名、过期自检、43→73 篇),否则你和它都会被旧叙事带偏。框架可以走,带着这张
单子走。
