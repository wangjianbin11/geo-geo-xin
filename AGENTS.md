# AGENTS — Skills 索引与调用关系

> 给 Claude Code / 未来 n8n 编排器看的 Skill 目录与调用图。
> 每个 Skill 的契约见各自目录下 `io-schema.json`,共用信封见 `schemas/envelope.schema.json`。

## Skill 清单(阶段 1+2 核心,共 7 个)

| # | Skill | 阶段 | 状态 | 目录 |
|---|---|---|---|---|
| 1 | asg-strategic-filter | pre-production | 🆕 v0.1 | `skills/pre-production/asg-strategic-filter/` |
| 2 | asg-keyword-researcher | pre-production | 🆕 v0.1 | `skills/pre-production/asg-keyword-researcher/` |
| 3 | asg-seo-writer-v2 | production | 🟠 v0.1 | `skills/production/asg-seo-writer-v2/` |
| 4 | asg-editorial-gate | quality-control | 🆕 v0.1 | `skills/quality-control/asg-editorial-gate/` |
| 5 | asg-voice-checker | quality-control | 🆕 v0.1 | `skills/quality-control/asg-voice-checker/` |
| 6 | asg-geo-benchmarker | feedback | 🆕 v0.1 | `skills/feedback/asg-geo-benchmarker/` |
| 7 | asg-stock-auditor | utility | 🆕 v0.1 | `skills/utility/asg-stock-auditor/` |

阶段 3 Skill(facebook-page / facebook-groups / short-video / 平台精修)与延后
Skill(youtube / service-page)本波不做,见方案第 11.4 节。

## 主链调用图(单篇文章 28 步)

```
[新话题 topic]
   │
   ▼
① asg-strategic-filter ──blocked(KILL)──▶ [弃稿/替代建议]
   │ ok(GO) / modify(MODIFY)
   │ human_gate ① Filter GO
   ▼
② asg-keyword-researcher   (需 Janson 先从 Ahrefs/SEMrush 拉外部数据)
   │ ok / flagged(降级模式:数据不全标 estimated)
   ▼
③ asg-seo-writer-v2  Steps 1-19  (+ geo-optimizer 思维内嵌)
   │ human_gate ② 标题+大纲锁定 (Step 14)
   ▼
④ asg-editorial-gate  Step 20  ──blocked──▶ [返回 Janson: 改/重写/弃]
   │ ok(PASS) / modify(自动修复重跑)
   │ human_gate ③ Editorial Gate
   ▼
⑤ asg-seo-writer-v2  Step 21 (Meta 生成)
   │
   ▼
⑥ asg-voice-checker  Step 22  ──flagged──▶ [标问题段落+改写建议,可继续]
   │ ok(PASS)
   ▼
[Step 23 打包] ─▶ [Step 24 分发, human_gate ④] ─▶ [Step 25-27 反馈闭环]
```

旁路(独立触发):

```
asg-geo-benchmarker  ◀── 每周手动触发 ──  产出规则修订建议 ──▶ asg-geo-standards / publishing-gate
asg-stock-auditor    ◀── 一次性触发   ──  产出 43 篇审计表 ──▶ 阶段 1 验收
```

## 4 个强制人工确认点(human_gate)

1. **Filter GO 决定** — 没有则 AI 自己说写就写
2. **标题 + 大纲锁定**(Step 14)— 没有则 AI 凭直觉跑完全篇
3. **Editorial Gate 决定**(Step 20)— 没有则质量没底线
4. **平台分发逐个确认**(Step 24)— 没有则错误内容被批量扩散

## 三种文章类型分支(article_type)

由 ① Filter 决定,贯穿 ②③④ 全部下游 Skill。精确参数集中在
`rulebooks/asg-publishing-gate.md` 的「Article Type Parameter Table」,
所有 Skill 引用同一张表,禁止各自硬编码,避免漂移。

| 类型 | 字数 | H2 | 内+外链 | 主词密度 | 流程 |
|---|---|---|---|---|---|
| pillar | 3000-5000 | 6-7 | 4 + 10 | 1.0-1.5% | 完整 28 步 |
| share | 2000-3000 | 5-6 | 3 + 8 | 1.0-2.0% | 精简 25 步 |
| response | 1200-2000 | 3-4 | 2 + 5 | 1.5-2.0% | 精简 22 步 |

## 规则文档依赖

```
asg-content-constitution.md  (最高约束)
   ├── asg-voice-bible.md                       ← asg-seo-writer-v2 写作 + asg-voice-checker 核查
   ├── asg-publishing-gate.md                   ← asg-editorial-gate 执行依据(类型参数表 SSoT + 10 Gate)
   ├── asg-risk-compliance.md                   ← asg-editorial-gate Gate 9 + asg-strategic-filter 风险标注
   ├── asg-geo-standards.md                     ← writer/gate 据此 + asg-geo-benchmarker 每周校准
   └── asg-obsidian-knowledge-base-standards.md ← 双仓同步契约(asg-knowledge-vault)
```
6 份规则文档全部 v0.1 落盘。
