---
name: asg-voice-checker
version: 0.1.0
stage: quality-control
status: v0.1
step: 22
human_gate: false
enforced_rulebooks: [asg-voice-bible, asg-content-constitution]
emits: data/runs/<article_id>/05-voice.json
io_schema: ./io-schema.json
---

# asg-voice-checker

## 1. 作用
Janson 第一人称声音一致性强制检查。Editorial Gate PASS 之后(Step 22)运行。
Gate 管"结构合规",voice-checker 管"还是不是 Janson 在说话"。

## 2. 触发
asg-editorial-gate PASS 且 asg-seo-writer-v2 完成 Step 21 Meta 之后。

## 3. 输入(io-schema.json#input)
`html`(成稿)+ `article_type` + `language`(en-GB|en-US,来自 dossier)。
依据 `asg-voice-bible.md`(Section 2 密度表、Section 5 禁用词、Section 7 中性漂移、Section 9 拼写集)。

## 4. 核心逻辑 — 5 项检查(voice-bible 驱动)
1. **第一人称密度** — 按 voice-bible §2 类型阈值核查 "I/my/we/our" 频率
2. **实战锚定语句** — 按 §2/§3 计数 "After N years/Across 5000+ stores" 类锚,达类型下限
3. **中性专家化警告** — §7:扫"被动语态+中性结论+无第一人称"段落,命中 2 项特征 → FLAG
4. **AI 痕迹扫描** — §5 禁用词库 + 模板化结构(每段同构、过渡套话)
5. **en-GB/en-US 一致性** — §9:按 `language` 扫错拼写集(UK 文章出现 jewelry/optimize/color/fulfillment → FLAG)

## 5. 输出(io-schema.json#output)
`checks[5]{name,result,offending[]}`。任一 FAIL/FLAG → status=flagged(不硬阻断,
但标问题段落 + 改写建议);全 PASS → status=ok,next=Step 23 打包。写 dossier.voice_report。
注:禁用词命中虽然在 Editorial Gate 检查 9 已是 BLOCK,这里作为冗余防线再扫一次。

## 6. 验收测试(tests/cases.json,plan §9.6)
1. 干净 Janson 文风样本 → 全 PASS
2. 中性百科口吻样本 → 检查1/3 FLAG + 指出段落
3. UK 文章含 "jewelry"/"optimize" → 检查5 FLAG 出拼写错误
4. 含 "Let's dive in"/"In conclusion," → 检查4 FLAG
