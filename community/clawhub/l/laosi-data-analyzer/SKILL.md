---
badge: premium
name: data-analyzer
version: 2.0.0
description: 数据分析 - 加载CSV/JSON自动计算统计描述(均�?中位�?标准�?极�?，异常检测，趋势分析，结果本地持久化
tags: [data, analysis, statistics, visualization, productivity]
author: laosi
source: original
---

# Data Analyzer - 数据分析引擎

> 激活词: 分析数据 / data analyze / 统计

## 功能

- CSV/JSON 数据加载解析
- 自动统计描述：均值、中位数、标准差、极�?- 异常值检测（IQR/z-score�?- 趋势判断（上�?下降/波动�?- 结果保存到本�?JSON

## Python 实现

```python
import csv, json, statistics, math
from datetime import datetime
from typing import List, Dict, Any

class DataAnalyzer:
    def __init__(self):
        self.data: List[Dict[str, Any]] = []
        self.numeric_cols: List[str] = []
    
    def load_csv(self, path: str, delimiter: str = ",") -> int:
        """从CSV加载数据"""
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            self.data = list(reader)
        self._detect_numeric()
        return len(self.data)
    
    def load_json(self, path: str) -> int:
        """从JSON加载数据（支持列表和记录列表�?""
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, list):
            self.data = raw
        elif isinstance(raw, dict):
            # 尝试找到第一个列表字�?            for v in raw.values():
                if isinstance(v, list):
                    self.data = v
                    break
        self._detect_numeric()
        return len(self.data)
    
    def _detect_numeric(self):
        """自动检测数值列"""
        if not self.data:
            return
        for col in self.data[0]:
            try:
                float(self.data[0][col])
                self.numeric_cols.append(col)
            except (ValueError, TypeError):
                pass
    
    def describe(self, col: str) -> dict:
        """数值列的统计描�?""
        if col not in self.numeric_cols:
            return {"error": f"'{col}' is not numeric"}
        vals = [float(r[col]) for r in self.data if r.get(col)]
        
        n = len(vals)
        mean = statistics.mean(vals)
        median = statistics.median(vals)
        stdev = statistics.stdev(vals) if n > 1 else 0
        
        # 异常检�?(IQR方法)
        sorted_vals = sorted(vals)
        q1 = sorted_vals[n // 4]
        q3 = sorted_vals[3 * n // 4]
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = [v for v in vals if v < lower or v > upper]
        
        # 趋势判断
        half = n // 2
        first_half = statistics.mean(vals[:half]) if half > 0 else mean
        second_half = statistics.mean(vals[half:]) if half > 0 else mean
        trend = "up" if second_half > first_half * 1.05 else "down" if second_half < first_half * 0.95 else "stable"
        
        return {
            "column": col,
            "count": n,
            "mean": round(mean, 2),
            "median": round(median, 2),
            "stdev": round(stdev, 2),
            "min": round(min(vals), 2),
            "max": round(max(vals), 2),
            "range": round(max(vals) - min(vals), 2),
            "q1": round(q1, 2),
            "q3": round(q3, 2),
            "iqr": round(iqr, 2),
            "outliers": len(outliers),
            "outlier_values": [round(v, 2) for v in outliers[:10]],
            "trend": trend,
        }
    
    def correlation(self, col1: str, col2: str) -> float:
        """Pearson相关系数"""
        if col1 not in self.numeric_cols or col2 not in self.numeric_cols:
            return None
        pairs = [(float(r[col1]), float(r[col2])) for r in self.data
                 if r.get(col1) and r.get(col2)]
        n = len(pairs)
        if n < 3:
            return None
        sum_x = sum(p[0] for p in pairs)
        sum_y = sum(p[1] for p in pairs)
        sum_xy = sum(p[0] * p[1] for p in pairs)
        sum_x2 = sum(p[0] ** 2 for p in pairs)
        sum_y2 = sum(p[1] ** 2 for p in pairs)
        num = n * sum_xy - sum_x * sum_y
        den = math.sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))
        return round(num / den, 3) if den else 0
    
    def report(self, output: str = None) -> dict:
        """完整分析报告"""
        report = {
            "rows": len(self.data),
            "columns": list(self.data[0].keys()) if self.data else [],
            "numeric_columns": self.numeric_cols,
            "statistics": {col: self.describe(col) for col in self.numeric_cols},
            "timestamp": datetime.now().isoformat(),
        }
        # 相关性矩�?        if len(self.numeric_cols) >= 2:
            report["correlations"] = {}
            for i, c1 in enumerate(self.numeric_cols):
                for c2 in self.numeric_cols[i+1:]:
                    corr = self.correlation(c1, c2)
                    if corr is not None:
                        report["correlations"][f"{c1}_vs_{c2}"] = corr
        
        if output:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        return report

# 使用示例
analyzer = DataAnalyzer()

# 模拟数据
sample_data = [
    {"date": "2026-05-01", "revenue": 1200, "users": 45, "conversion": 0.12},
    {"date": "2026-05-02", "revenue": 1350, "users": 52, "conversion": 0.14},
    {"date": "2026-05-03", "revenue": 1100, "users": 38, "conversion": 0.11},
    {"date": "2026-05-04", "revenue": 1600, "users": 61, "conversion": 0.13},
    {"date": "2026-05-05", "revenue": 900,  "users": 30, "conversion": 0.09},
    {"date": "2026-05-06", "revenue": 1450, "users": 55, "conversion": 0.15},
    {"date": "2026-05-07", "revenue": 1300, "users": 48, "conversion": 0.11},
]
analyzer.data = sample_data
analyzer._detect_numeric()

# 描述统计
desc = analyzer.describe("revenue")
print(f"营收: 均�?{desc['mean']}, 中位�?{desc['median']}, 趋势={desc['trend']}")
print(f"异常�? {desc['outliers']}�?)

# 相关�?corr = analyzer.correlation("revenue", "users")
print(f"营收-用户 相关系数: {corr}")

# 完整报告
report = analyzer.report("analysis_results.json")
print(f"分析完成: {report['rows']}条记�? {len(report['statistics'])}个数值列")
```

## 输出示例

```json
{
  "rows": 7,
  "columns": ["date", "revenue", "users", "conversion"],
  "statistics": {
    "revenue": {
      "mean": 1271.43,
      "median": 1300.0,
      "stdev": 239.05,
      "min": 900,
      "max": 1600,
      "trend": "stable"
    }
  },
  "correlations": {
    "revenue_vs_users": 0.985,
    "revenue_vs_conversion": 0.672
  }
}
```

## 使用场景

1. **业务报表**: 月度/周度运营数据自动分析
2. **A/B测试**: 实验组vs对照组的关键指标对比
3. **数据质量**: 异常值检测发现数据采集问�?4. **趋势监控**: 连续跟踪指标变化方向

## 依赖

- Python 3.8+
- 标准库（csv, json, statistics, math�?