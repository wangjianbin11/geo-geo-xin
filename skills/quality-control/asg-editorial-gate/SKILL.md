---
name: asg-editorial-gate
version: 0.1.0
stage: quality-control
status: v0.1
step: 20
human_gate: true
enforced_rulebooks: [asg-publishing-gate, asg-content-constitution, asg-voice-bible, asg-risk-compliance, asg-geo-standards]
reads_libraries: [facts, cases, sources, voices]
emits: data/runs/<article_id>/03-gate.json
io_schema: ./io-schema.json
---

# asg-editorial-gate

## 1. 作用
v2 核心 Gate。Step 20 强制审核,把 v1 "软自检" 升级为 "硬阻断"。决定文章
能否进入发布流程。**这是质量底线,不可绕过。**

## 2. 触发
asg-seo-writer-v2 完成 draft(Step 19)后立即触发。

## 3. 输入(io-schema.json#input)
`draft`(html/rank_math/asset_manifest/h2_blocks/schema_blocks)+ `article_type`
+ `keyword_spec`。引用 `asg-publishing-gate.md`(主依据,含 §A 类型参数表 + 10 Gate)。

## 4. 核心逻辑 — 执行 publishing-gate §B 的 10 项硬检查
逐项判 PASS/MODIFY/BLOCK,按 publishing-gate §C 决定逻辑汇总:

```
任一 BLOCK → BLOCK
否则 MODIFY≥3 → BLOCK
否则 1≤MODIFY≤2 → MODIFY
否则 → PASS
```

类型阈值**从 io-schema.json $defs.article_type_params 取**(该副本数值必须
与 publishing-gate §A 一致;CI/审阅核对,不一致以 §A 为准)。

**Gate 6(★硬伤)**:遍历 draft 所有 ASG 数据声明,每个必须有 Library ID 且
该 ID 能在 `libraries/*/*.json` 解析到;任一无 ID/解析失败 → 立即 BLOCK。

v0.1 放宽 20%:Gate 2 容差 ±0.3%/±0.7%、Gate 10 阈值 40%(见 publishing-gate §C)。

降级数据处理:keyword_spec.mode=="degraded" 时,密度类 Gate(2/3)改为 FLAG
而非 BLOCK,并在 audit.warnings 提示"基于估算数据,待补真实关键词"。

## 5. 输出(io-schema.json#output)
`checks[10]{id,name,result,detail}` + `decision` + `modify_list[]` + `block_reasons[]`。
status: PASS→ok / MODIFY→modify(自动修复重跑,二次不过升 blocked)/ BLOCK→blocked。
PASS → next=asg-seo-writer-v2(phase=meta);BLOCK → next=null,human_gate=true。
写 dossier.gate_report。audit.rulebook_refs 列触发的 Gate(如 asg-publishing-gate.md#gate-6)。

## 6. 验收测试(tests/cases.json,plan §9.5)
1. 第 44 篇开发中 Gate **至少 BLOCK 一次**(证明非橡皮图章)
2. 43 篇 TOP 3 重过 Gate → 全 PASS
3. 找一篇明显有问题的(缺 Schema / 密度超标 / 引用无 ID)→ BLOCK 并指出
