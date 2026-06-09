---
badge: premium
name: email-helper
version: 2.0.0
description: 邮件助手 - 编写/发�?管理邮件，支持SMTP发信和IMAP收信，多模板草稿，自动归�?tags: [email, communication, smtp, imap, productivity]
author: laosi
source: original
---

# Email Helper - 邮件助手

> 激活词: 邮件 / 发邮�?/ email

## 功能

- 编写邮件草稿（支持模板）
- 通过SMTP发送邮�?- 通过IMAP读取收件�?- 邮件归档和搜�?- 草稿本地持久�?
## Python 实现

```python
import os, json, smtplib, imaplib, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Optional

DRAFT_FILE = os.path.join(os.path.dirname(__file__), "email_drafts.json")

class EmailHelper:
    def __init__(self):
        os.makedirs(os.path.dirname(DRAFT_FILE), exist_ok=True)
        self.drafts = self._load_drafts()
    
    def _load_drafts(self) -> list:
        if os.path.exists(DRAFT_FILE):
            with open(DRAFT_FILE, encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def _save_drafts(self):
        with open(DRAFT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.drafts, f, ensure_ascii=False, indent=2)
    
    def create_draft(self, to_addr: str, subject: str, body: str,
                     cc: str = "", bcc: str = "") -> dict:
        """创建邮件草稿"""
        draft = {
            "id": len(self.drafts) + 1,
            "to": to_addr,
            "cc": cc,
            "bcc": bcc,
            "subject": subject,
            "body": body,
            "status": "draft",
            "created": datetime.now().isoformat(),
        }
        self.drafts.append(draft)
        self._save_drafts()
        return draft
    
    def build_mime(self, draft_id: int) -> Optional[MIMEMultipart]:
        """将草稿构建为MIME消息"""
        draft = next((d for d in self.drafts if d["id"] == draft_id), None)
        if not draft:
            return None
        
        msg = MIMEMultipart()
        msg["From"] = draft.get("from_addr", "sender@example.com")
        msg["To"] = draft["to"]
        if draft.get("cc"):
            msg["Cc"] = draft["cc"]
        msg["Subject"] = draft["subject"]
        msg.attach(MIMEText(draft["body"], "plain", "utf-8"))
        return msg
    
    def send(self, draft_id: int, smtp_host: str, smtp_port: int,
             username: str, password: str, use_tls: bool = True) -> dict:
        """通过SMTP发送草�?""
        draft = next((d for d in self.drafts if d["id"] == draft_id), None)
        if not draft:
            return {"error": f"Draft #{draft_id} not found"}
        
        msg = self.build_mime(draft_id)
        if not msg:
            return {"error": "Failed to build MIME message"}
        
        try:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            if use_tls:
                server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            draft["status"] = "sent"
            draft["sent_at"] = datetime.now().isoformat()
            self._save_drafts()
            return {"success": True, "to": draft["to"], "subject": draft["subject"]}
        except Exception as e:
            return {"error": str(e)}
    
    def inbox(self, imap_host: str, username: str, password: str,
              limit: int = 10) -> List[dict]:
        """读取收件�?""
        try:
            conn = imaplib.IMAP4_SSL(imap_host)
            conn.login(username, password)
            conn.select("INBOX")
            
            _, data = conn.search(None, "ALL")
            ids = data[0].split()[-limit:]  # 最近的N�?            messages = []
            
            for mid in ids:
                _, msg_data = conn.fetch(mid, "(RFC822)")
                raw = email.message_from_bytes(msg_data[0][1])
                messages.append({
                    "from": raw["From"],
                    "subject": raw["Subject"],
                    "date": raw["Date"],
                    "body": self._get_text(raw)[:200],
                })
            
            conn.logout()
            return messages
        except Exception as e:
            return [{"error": str(e)}]
    
    def _get_text(self, msg) -> str:
        """从邮件对象提取正�?""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode("utf-8", errors="ignore")
        return msg.get_payload(decode=True).decode("utf-8", errors="ignore") if msg.get_payload(decode=True) else ""
    
    def list_drafts(self, status: str = None) -> list:
        """列出草稿"""
        if status:
            return [d for d in self.drafts if d["status"] == status]
        return self.drafts
    
    def delete_draft(self, draft_id: int) -> bool:
        """删除草稿"""
        before = len(self.drafts)
        self.drafts = [d for d in self.drafts if d["id"] != draft_id]
        if len(self.drafts) < before:
            self._save_drafts()
            return True
        return False

# 使用示例
eh = EmailHelper()

# 创建草稿
draft = eh.create_draft(
    to_addr="team@company.com",
    subject="Weekly Update - May 28",
    body="Hi team,\n\nThis week's update:\n1. Feature A completed\n2. Bug fixes deployed\n\nBest,\nLaosi"
)
print(f"Draft #{draft['id']}: {draft['subject']}")

# 列出所有草�?for d in eh.list_drafts():
    print(f"  [{d['status']}] #{d['id']}: {d['subject']} -> {d['to']}")

# 实际发送（需要配置SMTP�?# result = eh.send(1, "smtp.gmail.com", 587, "user@gmail.com", "app_password")
# print(f"Send result: {result}")
```

## 邮件模板

```python
TEMPLATES = {
    "weekly_report": {
        "subject": "Weekly Report - {date}",
        "body": "Hi {name},\n\n{content}\n\nBest,\n{sender}"
    },
    "meeting_invite": {
        "subject": "Meeting: {topic} - {date}",
        "body": "Hi {name},\n\nYou're invited to {topic} at {time}.\n\nAgenda:\n{agenda}\n\nRegards,\n{sender}"
    },
    "follow_up": {
        "subject": "Re: {topic}",
        "body": "Hi {name},\n\nFollowing up on {topic}. Any updates?\n\nBest,\n{sender}"
    }
}
```

## 使用场景

1. **周报自动发�?*: 集成数据分析结果，自动生成并发送周�?2. **告警通知**: 系统异常时自动发邮件给值班人员
3. **批量邀�?*: 会议邀�?活动通知批量发�?4. **邮件归档**: 按项�?关键词自动分类归档邮�?
## 配置

```yaml
smtp:
  host: smtp.gmail.com
  port: 587
  use_tls: true
imap:
  host: imap.gmail.com
sender:
  name: AI Assistant
  email: ai@example.com
```

## 依赖

- Python 3.8+
- 标准库（smtplib, imaplib, email�?