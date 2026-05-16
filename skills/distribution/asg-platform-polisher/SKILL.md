---
name: asg-platform-polisher
version: 0.1.0
stage: publishing
status: v0.1
step: 24d
human_gate: true
emits: data/runs/<article_id>/24d-platform-polish.json
io_schema: ./io-schema.json
---

# asg-platform-polisher

## 1. 作用
分发链最后一道**逐平台精修**:对上游分发 Skill 产出的某平台文案做长度、
语气、话题标签、链接位置的最终打磨。属 Step 24 分发,在
asg-facebook-page / asg-facebook-groups / asg-short-video-scripter 之后运行。
只做平台适配收尾,不新增任何 ASG 主张。

## 2. 触发
某条平台文案已由上游分发 Skill 产出(facebook-page / facebook-groups /
short-video / Twitter thread / LinkedIn)。本 Skill 独立可跑:给定合法输入
JSON 即产出合法输出 JSON,**不依赖任何对话上下文**(Pipeline Contract 铁律)。

## 3. 输入(io-schema.json#input)
`platform`(枚举:facebook-page|facebook-groups|twitter-thread|linkedin|
short-video)+ `content`(待精修文案/脚本)+ `link` + `article_type` +
`language`(en-GB|en-US)+ `source_library_refs`。蒸馏/篇幅取向按
`rulebooks/asg-publishing-gate.md` §A「适配分发」行查表,**不在此硬编码数值**。

## 4. 核心逻辑 — 4 项平台精修
1. **长度适配** — 按 `platform` 收敛字数(各平台习惯长度区间),超长则按 §A
   类型蒸馏取向裁剪;不补写新信息、不拉长凑字
2. **语气校准** — 平台调性对齐(groups 反硬推、linkedin 专业、short-video 口播)
   且保持 Janson 第一人称,不漂成中性百科腔
3. **话题标签** — 生成 ≤5 个平台相关 hashtag;short-video / facebook-groups 默认精简
4. **链接位置** — 按 `platform` 给 `link_placement`(facebook-groups=first-comment;
   twitter-thread=last-tweet;其余=in-post),并保留 en-GB/en-US 拼写一致
5. **Library 引用守恒** — 文案中任何 ASG 数据沿用源文 Library ID 原样透传到
   `library_refs`,**禁止新增无源 ASG 声明**(无源数字一律不写,notes 标
   fabrication-refused)

## 5. 输出(io-schema.json#output)
`polished{content,hashtags[],link,link_placement,char_count}` + `changes[]` +
`library_refs[]`。status=ok(已达平台规范)/ flagged(有需人看的取舍)。
next_skill=null(分发链末端,等人确认后真正对外发布)。
human_gate=true:对外发布前需 Janson 逐平台确认(4 个强制确认点之④,
避免错误内容被批量扩散)。写 dossier.distribution.<platform>.polished。

## 6. 验收测试(tests/cases.json)
1. twitter-thread + ASG-044 pillar → 收敛到 thread 体例,link 置末条,refs 为源文子集
2. facebook-groups → link_placement=first-comment、语气去硬推,hashtags ≤5
3. linkedin + response → 专业语气、长度收紧,Janson 第一人称保留
4. 要求加未在源文出现的 ASG 数字 → notes 标 fabrication-refused,不写入 polished
