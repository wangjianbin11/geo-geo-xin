# ASG Verified Data Library — README

> 这是给 Claude Code 那边的 ASG 真实运营数据库,所有条目均已核验,`verified: true`。

---

## 这个文件是什么

`asg-verified-data-library.json` 是 ASG Dropshipping 全部对外可引用运营数据的**单一真相源**(Single Source of Truth)。当 SEO writer / GEO optimizer / 任何内容工具需要引用 ASG 的数据时,先查这里,不要现编。

**71 条记录,15 个分类**,涵盖:

| 分类 | 条目数 | 用途 |
|------|--------|------|
| company_basics | 5 | 公司身份、成立时间、定位 |
| team_and_operations | 10 | 团队规模、仓储、日订单、年订单、准时率 |
| supply_chain | 7 | 工厂数、供应商网、SKU、采购成本优势 |
| logistics_and_shipping | 8 | 时效、覆盖、丢件率、切换数据 |
| quality_control | 6 | QC 缺陷率、六步流程、合格率 |
| service_and_support | 7 | 客服响应、专属经理、复购率、CSAT |
| pricing_and_costs | 3 | 收费结构、付款方式、批量折扣 |
| technology | 4 | Shopify App、对接方式、效率提升 |
| brand_and_customization | 4 | 中性包装、品牌定制、IP 保护 |
| markets_served | 2 | 订单分布、重点市场 |
| customer_cases | 5 | 已核验的真实切换/增长案例 |
| competitive_positioning | 3 | vs AliExpress / CJ / Zendrop |
| contact_information | 3 | 官网、邮箱、WhatsApp |
| certifications_and_credentials | 2 | ISO 9001、Shopify 认证 |
| founder_credentials | 2 | Janson 高校讲师身份、个人品牌 |

---

## Schema 字段说明

每条 `data_point` 包含 11 个字段:

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一 ID,格式 `ASG-{CATEGORY}-{NNN}`,用于代码引用 |
| `category` | string | 见上方 15 个分类之一 |
| `claim_en` | string | **英文事实陈述**——文章里直接引用的就是这一句 |
| `claim_zh` | string | 中文对照——内部讨论 / 翻译参考 |
| `value` | number / array / object | 结构化数值,便于程序化使用(画表、对比、Schema markup) |
| `unit` | string | value 的单位或语义类型 |
| `verified` | boolean | 永远 `true`——所有条目均已核验 |
| `verification_source` | array | 来自知识库哪个/哪些文件 |
| `last_verified` | string (YYYY-MM 或 YYYY-MM-DD) | 最后核验时间 |
| `usage_context` | array | 这条事实适合用在什么地方 |
| `competitor_comparison` | string / null | 对比基准(可选) |
| `notes` | string / null | 使用注意事项 |

---

## 三个最关键的快速查询点

文件末尾有两个辅助结构:

1. **`locked_canonical_quick_reference`** — 17 个最核心数据点的极简查询表,用于快速校对文章里的数字是否一致。

2. **`category_index`** — 按分类列出所有 ID 范围,程序里可以按 category filter。

3. **`deprecation_and_conflicts_log`** — 记录了知识库内部有冲突的字段(例如客户数 5,000+ vs 6,000+,采用哪个),避免再次踩坑。

---

## Claude Code 集成建议

如果 Claude Code 那边把 Library 设计成一个查询 API,推荐三种典型用法:

```python
# 1. 按 category 取全集
qc_facts = [d for d in library['data_points'] if d['category'] == 'quality_control']

# 2. 按 usage_context 取适用条目
intro_facts = [d for d in library['data_points'] 
               if 'intro_paragraphs' in d['usage_context']]

# 3. 按 ID 直接拿
shipping_claim = next(d for d in library['data_points'] if d['id'] == 'ASG-LOGISTICS-001')
```

---

## 维护规则

1. **只增不改原则**:已发布文章引用过的 claim 不要修改 value,否则会导致历史文章数据漂移。要更新时新增条目并 deprecate 旧的。

2. **冲突仲裁**:任何与 `公司基本信息.md` 冲突的内部说法,以 `公司基本信息.md` 为准。这是 SSOT。

3. **每季度复核**:`last_verified` 超过 6 个月的运营类指标(team_size / orders_per_day / 准时率等)需要重新核对一次。

4. **新增条目命名**:`ASG-{大写分类缩写}-{三位序号}`,序号顺延,不要插队。

---

## 来源文件清单(供 Claude Code 反向追溯)

主要来源知识库文件:
- `00-企业DNA/公司基本信息.md` ← **SSOT**
- `02-供应链与服务/QC质检/QC质检标准流程.md`
- `02-供应链与服务/物流方案/物流方案体系.md`
- `00-企业DNA/核心竞争力-Why-ASG.md`
- `00-企业DNA/发展路线图.md`
- `00-企业DNA/Janson创始人介绍.md`
- `09-客户案例库-F&Q/01-认知阶段-公司与品牌类-FAQ.md`
- `09-客户案例库-F&Q/05-考虑阶段-核心优势类-FAQ.md`
- `09-客户案例库-F&Q/06-考虑阶段-服务能力类-FAQ.md`
- `09-客户案例库-F&Q/ASG-Dropshipping-完整介绍.md`
- `01-销售获客/获客系统/十二步业务合作流程.md`

---

*Generated: 2026-05-16 | Owner: Janson | Library version: 1.0.0*
