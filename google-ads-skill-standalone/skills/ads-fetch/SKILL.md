---
name: ads-fetch
description: 从 Google Ads API 获取广告投放数据，支持关键词、广告系列、搜索词等多维度数据。
---

# 获取 Google Ads 数据

## 何时使用
- 用户想查看广告表现数据
- 需要指定日期范围的数据
- 获取关键词、广告系列或搜索词报告

## 可用脚本

### 1. 关键词表现
```bash
python3 .agents/skills/google-ads/scripts/fetch_keywords.py --date_range TODAY --limit 20
```

**支持的日期范围**：`TODAY`, `YESTERDAY`, `LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`, `LAST_90_DAYS`, `THIS_MONTH`, `LAST_MONTH`

**输出字段**：Campaign, Ad Group, Keyword, Impressions, Clicks, CTR, Conversions, Cost, CPC

### 2. 广告系列表现
```bash
python3 .agents/skills/google-ads/scripts/fetch_campaigns.py --date_range LAST_7_DAYS
```

**输出字段**：Campaign Name, Status, Impressions, Clicks, CTR, Conversions, Cost, CPC

### 3. 搜索词报告
```bash
python3 .agents/skills/google-ads/scripts/fetch_search_terms.py --date_range LAST_7_DAYS --limit 30
```

**输出字段**：Search Term, Campaign, Ad Group, Match Type, Impressions, Clicks, Conversions, Cost

## 注意事项
1. 所有脚本在**项目根目录**下运行
2. 数据有 2-3 小时延迟
3. 费用单位为账户设置的货币（通常 SGD 或 USD）
4. 如果遇到 `RefreshError`，执行 `ads-setup` 重新认证
