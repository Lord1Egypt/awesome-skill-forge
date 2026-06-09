---
badge: premium
name: scheduler
version: 2.0.0
description: 任务调度 - 定时任务/周期性任�?一次性提醒，cron语法支持，持久化存储，下次执行时间自动计�?tags: [scheduler, cron, task, reminder, automation, productivity]
author: laosi
source: original
---

# Scheduler - 任务调度�?
> 激活词: 调度 / 定时任务 / 提醒 / schedule

## 功能

- 创建定时任务（cron表达式）
- 一次性提醒（指定时间�?- 周期性任务（每天/每周/每月�?- 任务列表和状态管�?- 下次执行时间自动计算
- 持久化存�?
## Python 实现

```python
import os, json, re
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from dataclasses import dataclass, field, asdict

SCHEDULE_FILE = os.path.join(os.path.dirname(__file__), "scheduled_tasks.json")

@dataclass
class ScheduledTask:
    name: str
    schedule: str  # cron表达�? "minute hour day month weekday"
    description: str = ""
    enabled: bool = True
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    created: str = ""
    run_count: int = 0
    tags: List[str] = field(default_factory=list)

class Scheduler:
    def __init__(self):
        os.makedirs(os.path.dirname(SCHEDULE_FILE), exist_ok=True)
        self.tasks: List[ScheduledTask] = []
        self._load()
    
    def _load(self):
        if os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [ScheduledTask(**t) for t in data]
    
    def _save(self):
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.tasks], f,
                      ensure_ascii=False, indent=2)
    
    def add_task(self, name: str, schedule: str,
                 description: str = "", tags: list = None) -> ScheduledTask:
        """添加定时任务"""
        task = ScheduledTask(
            name=name,
            schedule=schedule,
            description=description,
            enabled=True,
            created=datetime.now().isoformat(),
            next_run=self._calc_next_run(schedule),
            tags=tags or []
        )
        self.tasks.append(task)
        self._save()
        return task
    
    def _calc_next_run(self, cron_expr: str) -> str:
        """计算下次执行时间（简化实现）"""
        parts = cron_expr.strip().split()
        if len(parts) != 5:
            return datetime.now().isoformat()
        
        minute, hour, day, month, weekday = parts
        now = datetime.now()
        
        # 简单解析：如果只有小时和分钟指�?        if minute == "*" and hour == "*":
            # 每分钟：下一分钟
            next_time = now + timedelta(minutes=1)
        elif minute != "*" and hour == "*":
            # 每小时的指定分钟
            m = int(minute)
            next_time = now.replace(minute=m, second=0, microsecond=0)
            if next_time <= now:
                next_time += timedelta(hours=1)
        elif minute != "*" and hour != "*":
            # 每天的指定时�?            h, m = int(hour), int(minute)
            next_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if next_time <= now:
                next_time += timedelta(days=1)
        else:
            # 默认�?小时�?            next_time = now + timedelta(hours=1)
        
        return next_time.isoformat()
    
    def remove_task(self, task_id: int) -> bool:
        """删除任务"""
        if 0 <= task_id < len(self.tasks):
            self.tasks.pop(task_id)
            self._save()
            return True
        return False
    
    def toggle(self, task_id: int) -> Optional[bool]:
        """启用/禁用任务"""
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id].enabled = not self.tasks[task_id].enabled
            self._save()
            return self.tasks[task_id].enabled
        return None
    
    def mark_run(self, task_id: int):
        """标记任务已执�?""
        if 0 <= task_id < len(self.tasks):
            task = self.tasks[task_id]
            task.last_run = datetime.now().isoformat()
            task.run_count += 1
            task.next_run = self._calc_next_run(task.schedule)
            self._save()
    
    def due_tasks(self) -> List[ScheduledTask]:
        """获取到期的任�?""
        now = datetime.now()
        return [
            t for t in self.tasks
            if t.enabled and t.next_run and datetime.fromisoformat(t.next_run) <= now
        ]
    
    def list_tasks(self, enabled_only: bool = False) -> List[Dict]:
        """列出所有任�?""
        tasks = [t for t in self.tasks if not enabled_only or t.enabled]
        return [
            {
                "id": i,
                "name": t.name,
                "schedule": t.schedule,
                "enabled": t.enabled,
                "next_run": t.next_run,
                "last_run": t.last_run or "never",
                "run_count": t.run_count,
                "tags": t.tags,
            }
            for i, t in enumerate(tasks)
        ]
    
    def summary(self) -> Dict:
        """调度器概�?""
        total = len(self.tasks)
        enabled = sum(1 for t in self.tasks if t.enabled)
        due_now = len(self.due_tasks())
        return {
            "total": total,
            "enabled": enabled,
            "disabled": total - enabled,
            "due_now": due_now,
            "file": SCHEDULE_FILE
        }

# 使用示例
sched = Scheduler()

# 添加定时任务
sched.add_task(
    name="daily backup",
    schedule="0 2 * * *",      # 每天凌晨2�?    description="Run daily database backup",
    tags=["system", "backup"]
)

sched.add_task(
    name="health check",
    schedule="*/5 * * * *",    # �?分钟
    description="Ping all services",
    tags=["monitoring"]
)

sched.add_task(
    name="weekly report",
    schedule="0 9 * * 1",      # 每周一9�?    description="Generate and email weekly report",
    tags=["report", "email"]
)

sched.add_task(
    name="standup reminder",
    schedule="0 10 * * 1-5",   # 工作�?0�?    description="Remind team for daily standup",
    tags=["team", "meeting"]
)

# 查看所有任�?print("任务列表:")
for t in sched.list_tasks():
    status = "🟢" if t["enabled"] else "🔴"
    print(f"  {status} [{t['id']}] {t['name']} ({t['schedule']})")
    print(f"      Next: {t['next_run']}")

# 调度器概�?stats = sched.summary()
print(f"\n调度�? {stats['enabled']}/{stats['total']} 启用, {stats['due_now']} 个待执行")

# 检查到期任�?due = sched.due_tasks()
if due:
    print(f"\n到期任务 ({len(due)}):")
    for t in due:
        print(f"  �?{t.name} - 应在 {t.next_run} 执行")
        # 执行并标�?        sched.mark_run(self.tasks.index(t))
```

## Cron语法速查

```
* * * * *
�?�?�?�?�?�?�?�?�?└── 星期 (0-7, 0�?=周日)
�?�?�?└──── 月份 (1-12)
�?�?└────── 日期 (1-31)
�?└──────── 小时 (0-23)
└────────── 分钟 (0-59)
```

| 示例 | 含义 |
|------|------|
| `0 2 * * *` | 每天凌晨2�?|
| `*/5 * * * *` | �?分钟 |
| `0 9 * * 1` | 每周一9�?|
| `0 9-17 * * 1-5` | 工作�?点到17点每小时 |
| `0 0 1 * *` | 每月1�?�?|
| `30 8 * * *` | 每天8:30 |

## 使用场景

1. **系统维护**: 定时备份、日志清理、缓存刷�?2. **监控告警**: 定期健康检查，异常自动告警
3. **报告生成**: 自动生成日报/周报并发�?4. **个人提醒**: 喝水/站立/休息的定时提�?5. **工作�?*: 定时触发数据同步/ETL任务

## 依赖

- Python 3.8+
- 无第三方依赖
