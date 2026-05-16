---
name: asg-facebook-groups
version: 0.1.0
stage: publishing
status: v0.1
step: 24b
human_gate: true
emits: data/runs/<article_id>/24b-facebook-groups.json
io_schema: ./io-schema.json
---

# asg-facebook-groups

## 1. 作用
把已发布文章改写为一条**社群友好**的 Facebook Groups 帖子:价值优先、
零硬推销、反 spam 框架(像群成员分享经验,不像品牌投放)。属 Step 24 分发,
在 asg-voice-checker(Step 22)+ Step 23 打包之后运行。只做渠道适配。

## 2. 触发
asg-voice-checker status=ok 且 dossier.publish_package 已生成。
本 Skill 独立可跑:给定合法输入 JSON 即产出合法输出 JSON,
**不依赖任何对话上下文**(Pipeline Contract 铁律)。

## 3. 输入(io-schema.json#input)
`draft` + `publish_package` + `article_type` + `language`。
蒸馏程度按 `rulebooks/asg-publishing-gate.md` §A「适配分发」行查表,**不硬编码数值**。
群规风险:link 默认放评论区(`link_placement="first-comment"`),正文不放硬链接。

## 4. 核心逻辑 — 反 spam 改写
1. **经验开场** — 第一人称分享一个文章中已有的实战观察,口语化,不喊口号
2. **纯价值主体** — 给 1-2 个可操作要点(源文已有),不提产品/服务/报价
3. **反硬推** — 禁止 "DM me / link in bio / 我们提供" 类;CTA 仅"完整拆解我放评论里"
4. **链接降权** — `link_placement` 默认 first-comment,降低群规误判与限流
5. **Library 引用守恒** — 任何 ASG 数据沿用源文 Library ID 原样透传到 `library_refs`,
   **禁止新增无源 ASG 声明**(无源数字一律不写,notes 标 fabrication-refused)

## 5. 输出(io-schema.json#output)
`post{opener,value_points[],link,link_placement}` + `anti_spam_flags[]` +
`library_refs[]`。status=ok,next_skill=asg-platform-polisher。
human_gate=true:对外发布前需 Janson 逐平台确认(4 个强制确认点之④)。
写 dossier.distribution.facebook_groups。

## 6. 验收测试(tests/cases.json)
1. ASG-044 UK pillar → 经验开场 + 价值点,link_placement=first-comment
2. 含硬推销措辞输入 → anti_spam_flags 命中并改写为软表达
3. 要求加未在源文出现的 ASG 数字 → notes 标 fabrication-refused,不写入 post
