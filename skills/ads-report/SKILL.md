---
name: ads-report
description: 生成 Google Ads 投放报告，支持 Markdown 和 CSV 格式输出。
---

# 生成 Google Ads 报告

## 何时使用
- 用户需要周报/月报
- 需要导出数据为 CSV
- 需要格式化的汇总报告

## 报告模板

### 周报模板

```markdown
# Google Ads 周报 [日期范围]

## 总览
| 指标 | 本周 | 上周 | 变化 |
|---|---|---|---|
| 总花费 | $XX | $XX | +/-XX% |
| 总点击 | XX | XX | +/-XX% |
| 总转化 | XX | XX | +/-XX% |
| 平均 CPC | $XX | $XX | +/-XX% |
| 平均 CTR | XX% | XX% | +/-XX% |

## Top 关键词
[按转化排序的前 10 个关键词表格]

## 搜索词洞察
[搜索词报告中的新发现]

## 优化建议
1. [具体建议 1]
2. [具体建议 2]
3. [具体建议 3]
```

## 执行步骤

### 1. 获取数据
运行以下脚本获取本周和上周的数据进行对比：
```bash
# 本周数据
python3 .agents/skills/google-ads/scripts/fetch_keywords.py --date_range LAST_7_DAYS --limit 50
python3 .agents/skills/google-ads/scripts/fetch_campaigns.py --date_range LAST_7_DAYS
python3 .agents/skills/google-ads/scripts/fetch_search_terms.py --date_range LAST_7_DAYS --limit 50
```

### 2. 生成报告
根据获取的数据填充报告模板，计算环比变化率。

### 3. 输出
- Markdown 格式：直接输出给用户
- CSV 格式：保存到 `google ads/google_ads_data/` 目录
- 如果用户需要，可保存为文件供后续使用
