---
doc: customer-voices
title: 客户声音库
status: v0.1
verified: false
source: placeholder
last_updated: 2026-05-16
note: 此库无法用方案种子填充——必须由 Janson 从真实 WhatsApp/Email/Sales 记录脱敏录入。以下为结构 + 字段示例,非真实数据。
---

# 客户声音库 (Voices Library)

> 真实客户原话(脱敏)。用于 Step 3 PAA / Step 5 差异化 / Step 13 FAQ 设计。
> 机器调用读 `customer-voices.json`。**这是唯一无法 AI 代填的 Library——
> 价值全在"真实原话",必须 Janson 手动从对话捞。**

## 字段规范

每条 = 一个 `VOICE-` ID,含:type / quote(脱敏原话)/ frequency /
context(pre-sales|onboarding|post-sale)/ source(WhatsApp|Email|Sales)/
counter_framework / related_article / related_case。

不公开:客户姓名 / 公司 / 邮箱 / 电话 / 业务规模具体数(只留区间)。

## High-Frequency Questions(示例结构,非真实)

| ID | quote(脱敏) | frequency | context | source |
|---|---|---|---|---|
| VOICE-001 | "How long does shipping to the UK actually take?" | (待统计) | pre-sales | Email+WhatsApp |
| VOICE-002 | "Do you offer custom packaging?" | (待统计) | pre-sales | WhatsApp |

## Common Objections(示例结构,非真实)

| ID | objection | frequency | counter_framework | related |
|---|---|---|---|---|
| VOICE-010 | "AliExpress is cheaper" | (待统计) | margin math(总到手成本对比,见宪法 Art.6) | CASE-007 |
| VOICE-011 | "How do I trust you?" | (待统计) | 8-year track record(FACT-040/041/042) | CASE-001 |

## 收集 SOP(见 obsidian 规范,阶段2正式化)
每天 5 分钟:把当天客户对话片段脱敏记入对应 VOICE 文件。
