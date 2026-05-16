---
name: asg-short-video-scripter
version: 0.1.0
stage: publishing
status: v0.1
step: 24c
human_gate: false
emits: data/runs/<article_id>/24c-short-video.json
io_schema: ./io-schema.json
---

# asg-short-video-scripter

## 1. 作用
把已发布文章转成一条短视频脚本(hook 3s / body / CTA,约 150-250 词)
并附镜头清单(shot list)。属 Step 24 分发,在 asg-voice-checker(Step 22)+
Step 23 打包之后运行。只做渠道适配,不新增任何 ASG 主张。

## 2. 触发
asg-voice-checker status=ok 且 dossier.publish_package 已生成。
本 Skill 独立可跑:给定合法输入 JSON 即产出合法输出 JSON,
**不依赖任何对话上下文**(Pipeline Contract 铁律)。

## 3. 输入(io-schema.json#input)
`draft` + `publish_package` + `article_type` + `language`。
所有类型都要短视频(§A「适配分发」:pillar=长视频+5 平台;share=短视频+
Twitter thread;response=短视频+FAQ 拆解)。蒸馏程度按 §A 行查表,**不硬编码数值**。

## 4. 核心逻辑 — 脚本三段 + 镜头表
1. **Hook(前 3 秒)** — 1 句强钩,用源文已有的 Janson 第一人称实战锚句,不造数据
2. **Body** — 1 个核心 takeaway 口播,按 §A「适配分发」类型控制信息密度;总词数 150-250
3. **CTA** — 软引导看完整文章(口播 + 文案位),不承诺收益、不硬推销
4. **Shot list** — 每段对应镜头(画面/字幕/时长秒),`total_seconds` 与词数自洽(≈2.5 词/秒)
5. **Library 引用守恒** — 口播若引 ASG 数据,沿用源文 Library ID 原样透传到 `library_refs`,
   **禁止新增无源 ASG 声明**(无源数字不写,notes 标 fabrication-refused)

## 5. 输出(io-schema.json#output)
`script{hook,body,cta,word_count}` + `shot_list[]{scene,visual,caption,seconds}` +
`library_refs[]`。status=ok,next_skill=asg-platform-polisher。
human_gate=false:短视频脚本是内部生产物,不直接对外发布,无需逐平台确认
(对外发布前由 platform-polisher / 真正发帖 Skill 承接确认点④)。
写 dossier.distribution.short_video。

## 6. 验收测试(tests/cases.json)
1. ASG-044 UK pillar → script 词数在 150-250,hook 沿用 8-year 锚句,shot_list 时长自洽
2. response 类型 → 信息密度更高、body 更紧,仍 150-250 词
3. 要求加未在源文出现的 ASG 数字 → notes 标 fabrication-refused,不写入脚本
