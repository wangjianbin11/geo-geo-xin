---
name: asg-facebook-page
version: 0.1.0
stage: publishing
status: v0.1
step: 24a
human_gate: true
emits: data/runs/<article_id>/24a-facebook-page.json
io_schema: ./io-schema.json
---

# asg-facebook-page

## 1. 作用
把已发布文章改写为一条 Facebook Page 帖子(hook + value + 软 CTA + 文章链接)。
属 Step 24 分发,在 asg-voice-checker(Step 22)+ Step 23 打包之后运行。
只做"渠道适配",不新增任何 ASG 主张。

## 2. 触发
asg-voice-checker status=ok 且 dossier.publish_package 已生成(文章已可发布)。
本 Skill 独立可跑:给定一个合法输入 JSON 即可产出输出 JSON,
**不依赖任何对话上下文**(Pipeline Contract 铁律)。

## 3. 输入(io-schema.json#input)
`draft`(成稿 html,来自 dossier.draft.html)+ `publish_package`(meta_variants /
canonical_url)+ `article_type`(pillar|share|response)+ `language`(en-GB|en-US)。
分发蒸馏程度按 `rulebooks/asg-publishing-gate.md` §A「适配分发」行查表,
**不在此硬编码数值**:pillar 蒸馏度低(展开多)、response 蒸馏度高(收紧)。

## 4. 核心逻辑 — 4 步改写
1. **Hook(1-2 句)** — 用文章中已有的 Janson 第一人称实战锚句作钩子,不造新数据
2. **Value 段** — 提炼文章 1 个核心 takeaway,按 §A「适配分发」对应类型控制展开篇幅
3. **软 CTA** — "full breakdown in the post" 类软引导,不硬推销、不承诺收益
4. **Library 引用守恒** — 帖中若带任何 ASG 数据/案例,必须沿用源文 Library ID
   (FACT-/CASE-/SOURCE-/VOICE-),原样透传到 `library_refs`,**禁止新增无源 ASG 声明**

## 5. 输出(io-schema.json#output)
`post{hook,body,soft_cta,link,hashtags[]}` + `library_refs[]` + `notes`。
status=ok,next_skill=asg-platform-polisher(Step 24d 做最终平台精修)。
human_gate=true:Step 24 分发逐平台需 Janson 确认后才真正对外发布
(4 个强制确认点之④,避免错误内容被批量扩散)。写 dossier.distribution.facebook_page。

## 6. 验收测试(tests/cases.json)
1. ASG-044 UK pillar → 产出 hook(沿用 8-year 锚句)+ value + 软 CTA,library_refs 为源文子集
2. response 类型 → body 明显更短(高蒸馏度),仍只软 CTA
3. 输入帖若被要求加未在源文出现的 ASG 数字 → notes 标 fabrication-refused,不写入 post
