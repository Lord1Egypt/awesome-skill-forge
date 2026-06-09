---
name: finbot-stock
description: "A股市场数据工具 — 实时行情、板块扫描、收盘简报、多因子选股。数据源：新浪财经（零成本，无需API Key）。不构成投资建议。"
tags:
  - finance
  - china-stocks
  - a-shares
  - market-data
  - stock-screening
version: 1.0.0
---

# finbot-stock — A股市场数据工具

一键获取A股实时行情、板块扫描、收盘简报和多因子选股评分。

## 数据源

新浪财经免费行情接口。零成本，无需 API Key。

## 用法

### 实时行情（单只）
```bash
python3 {baseDir}/scripts/fetcher.py
```
默认测试平安银行(000001)，修改 `__main__` 中的 code 参数即可。

### 批量行情
在 Python 中调用：
```python
from scripts.fetcher import fetch_batch
results = fetch_batch(["000001","000002","600519","300750"])
```

### 市场扫描
```bash
python3 {baseDir}/scripts/analyzer.py --scan
```
输出：各板块涨跌排名、异动提醒、成交额TOP。

### 收盘简报
```bash
python3 {baseDir}/scripts/analyzer.py --report
```
生成 Markdown 格式的每日市场简报，包含板块表现、异动监控。

## 输出示例

```
📊 阿不 市场扫描 | 2026-06-02
============================================================
📍 科技 (10只)
   🔴 寒武纪(688256): 1300.0 +5.01%
   🔴 立讯精密(002475): 74.0 +4.65%

💰 成交额TOP
   立讯精密: ¥167.48亿  4.65%
   宁德时代: ¥167.19亿  3.28%
```

## 合规声明

本工具仅提供市场数据整理与展示，**不构成任何投资建议**。所有数据来源于公开免费接口，使用时请自行核实。投资有风险，决策需自主。

## 依赖

- Python 3.8+
- 无需第三方包（仅使用标准库 urllib、json、csv、re）

## 授权

MIT
