# data/sources — 真实数据溯源 (provenance)

> Janson 于 2026-05-16 提供的真实运营数据。**这是真实数据,使用它不是杜撰**——
> 是方案阶段 1 应做的数据沉淀。所有下游产物标 `source` + `verified` 以可追溯。

## 原始档(只读,勿手改)

| 文件 | 来源 | 说明 |
|---|---|---|
| `gsc-2026-05-16.xlsx` | Google Search Console 导出 | asgdropshipping.com,搜索类型=网络,过去 3 个月(2026-02-15 ~ 2026-05-16) |
| `keyword-corpus-2026-05-16.xlsx` | Janson 整理的谷歌下拉框关键词 + 指标 | 3,625 关键词,含意图/搜索量/KD/CPC/竞争度 |

## 提取产物(由 `tools/xlsx_to_csv.py` 生成,可重跑)

重新生成:
```
python3 tools/xlsx_to_csv.py data/sources/gsc-2026-05-16.xlsx data/gsc --prefix gsc_
python3 tools/xlsx_to_csv.py data/sources/keyword-corpus-2026-05-16.xlsx data/keywords --prefix kw_
# 然后按语义重命名(见下表)
```

| CSV | 行数(不含表头) | 列 |
|---|---|---|
| `data/gsc/gsc_daily.csv` | 89 | 日期, 点击次数, 展示, 点击率, 排名 |
| `data/gsc/gsc_queries.csv` | 952 | 热门查询, 点击次数, 展示, 点击率, 排名 |
| `data/gsc/gsc_pages.csv` | 97 | 网页, 点击次数, 展示, 点击率, 排名 |
| `data/gsc/gsc_countries.csv` | 196 | 国家/地区, 点击次数, 展示, 点击率, 排名 |
| `data/gsc/gsc_devices.csv` | 3 | 设备, 点击次数, 展示, 点击率, 排名 |
| `data/gsc/gsc_appearance.csv` | 0 | (空) |
| `data/gsc/gsc_filters.csv` | 2 | 过滤器, 值 |
| `data/keywords/keyword-corpus.csv` | 3,625 | 关键词, 意图, 搜索量, KD值, CPC, 竞争激烈程度, 结果, 更新时间 |

## 数据口径与注意事项(下游必须遵守)

1. **页面是真实存量**:GSC `gsc_pages.csv` 有 ~97 个 URL,其中约 90 个是内容文章页
   (非 `/products/`、`/product-category/`、首页等)。方案曾假设"43 篇",**以真实
   数据为准**:审计真实索引到的内容页集合,产物注明真实总数。
2. **GSC 无 AI 引用维度**:GSC 只有点击/展示/CTR/排名。AI 引用情况(Perplexity/
   AI Overview)GSC **没有**,仍需人工核查。stock-auditor 用真实 GSC 跑,但
   `ai_cited` 字段保持 null,mode 标 `basic`(诚实标注,不臆造)。
3. **关键词意图编码**:`I`=informational,`C`=commercial,`N`=navigational,
   `T`=transactional,**空=未分类**(语料里约 1985 条空意图,多为长尾,可用但
   选种子时优先非空意图)。
4. **数字含千分位**:搜索量等以字符串存(如 `74,000`),已被 CSV 正确加引号。
   **下游解析必须用 Python `csv` 模块,不要用 `awk -F,`**(会被字段内逗号截断)。
5. **provenance 标注**:GSC 衍生产物 `source: gsc-export-2026-05-16`;关键词衍生
   产物 `source: janson-keyword-corpus-2026-05-16`;两者 `verified: true`
   (Janson 提供的真实数据),但派生的"推荐/评级"是 AI 判断,标 `derived: true`。
