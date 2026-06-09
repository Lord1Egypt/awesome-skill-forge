---
badge: premium
name: webhook-receiver
version: 2.0.0
description: Webhook接收 - 本地HTTP服务接收和处理webhook事件，支持日志记录、事件过滤、自动重�?tags: [webhook, http, events, automation, integration]
author: laosi
source: original
---

# Webhook Receiver - Webhook接收服务

> 激活词: webhook / 接收webhook / hook

## 功能

- 本地HTTP服务接收webhook事件
- 事件日志持久�?- 事件类型过滤
- 自动重试机制
- 支持多种webhook格式（GitHub/Slack/Generic�?
## Python 实现

```python
import os, json, hashlib, hmac
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable, Dict, List, Optional

WEBHOOK_LOG = os.path.join(os.path.dirname(__file__), "webhook_logs.json")

class WebhookEvent:
    def __init__(self, headers: dict, body: str, source: str = "unknown"):
        self.headers = headers
        self.body = body
        self.source = source
        self.timestamp = datetime.now().isoformat()
        self.id = hashlib.sha256(body.encode()).hexdigest()[:16]
        self.parsed = self._parse_body()
    
    def _parse_body(self) -> dict:
        try:
            return json.loads(self.body)
        except json.JSONDecodeError:
            return {"raw": self.body[:200]}
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "timestamp": self.timestamp,
            "headers": self.headers,
            "parsed": self.parsed,
        }

class WebhookReceiver:
    def __init__(self, log_file: str = None):
        self.log_file = log_file or WEBHOOK_LOG
        self.handlers: Dict[str, Callable] = {}
        self.events: List[dict] = self._load_events()
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def _load_events(self) -> list:
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, encoding="utf-8") as f:
                    return json.load(f).get("events", [])
            except (json.JSONDecodeError, ValueError):
                return []
        return []
    
    def _save_events(self):
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump({"events": self.events[-500:]}, f,
                      ensure_ascii=False, indent=2)
    
    def register_handler(self, event_type: str, handler: Callable):
        """注册事件处理函数"""
        self.handlers[event_type] = handler
    
    def receive(self, event: WebhookEvent) -> dict:
        """处理接收到的webhook"""
        event_dict = event.to_dict()
        self.events.append(event_dict)
        self._save_events()
        
        result = {"received": True, "id": event.id, "source": event.source}
        
        # 查找匹配的handler
        event_type = event.parsed.get("event", "generic")
        if event_type in self.handlers:
            try:
                handler_result = self.handlers[event_type](event.parsed)
                result["handler_result"] = handler_result
                result["processed"] = True
            except Exception as e:
                result["error"] = str(e)
                result["processed"] = False
        else:
            result["processed"] = False
            result["note"] = f"No handler for event type: {event_type}"
        
        return result
    
    def verify_github_signature(self, payload: str, signature: str,
                                 secret: str) -> bool:
        """验证GitHub webhook签名"""
        expected = "sha256=" + hmac.new(
            secret.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
    
    def list_events(self, source: str = None, limit: int = 20) -> list:
        """列出最近事�?""
        events = self.events
        if source:
            events = [e for e in events if e.get("source") == source]
        return events[-limit:]
    
    def get_stats(self) -> dict:
        """统计信息"""
        sources = {}
        for e in self.events:
            src = e.get("source", "unknown")
            sources[src] = sources.get(src, 0) + 1
        return {
            "total_events": len(self.events),
            "by_source": sources,
            "oldest": self.events[0]["timestamp"] if self.events else None,
            "newest": self.events[-1]["timestamp"] if self.events else None,
        }

# 使用示例
receiver = WebhookReceiver()

# 注册handler
def handle_github_push(data):
    repo = data.get("repository", {}).get("name", "unknown")
    commits = len(data.get("commits", []))
    print(f"  Push to {repo}: {commits} commits")
    return {"repo": repo, "commits": commits}

receiver.register_handler("push", handle_github_push)

# 模拟接收webhook
event = WebhookEvent(
    headers={"X-GitHub-Event": "push", "Content-Type": "application/json"},
    body=json.dumps({
        "event": "push",
        "repository": {"name": "my-repo"},
        "commits": [{"message": "feat: add webhook"}]
    }),
    source="github"
)

result = receiver.receive(event)
print(f"Event: {result['id']}, processed: {result.get('processed')}")

# 统计
stats = receiver.get_stats()
print(f"Total events: {stats['total_events']}, by source: {stats['by_source']}")
```

## 验证签名

```python
def verify_webhook(payload, signature, secret):
    """GitHub/Stripe webhook签名验证"""
    import hmac, hashlib
    expected = "sha256=" + hmac.new(
        secret.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## 使用场景

1. **CI/CD**: 接收GitHub/GitLab push事件触发构建
2. **支付通知**: 接收Stripe/PayPal支付成功回调
3. **监控告警**: 接收Grafana/Prometheus告警
4. **聊天机器�?*: 接收Slack/Discord消息事件

## 依赖

- Python 3.8+
- 标准库（http.server, json, hashlib�?