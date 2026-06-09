---
badge: premium
name: crypto-encoder
version: 2.0.0
description: 编码工具�?- Base64编码/解码、URL编码/解码、SHA256/MD5哈希计算、UUID生成、JWT解析
tags: [crypto, encoding, base64, hash, uuid, security]
author: laosi
source: original
---

# Crypto Encoder - 编码工具�?
> 激活词: 编码 / base64 / 哈希 / hash / uuid

## 功能

- Base64 编码/解码
- URL 编码/解码
- SHA256/SHA512/MD5 哈希
- HMAC 签名
- UUID v4 生成
- JWT Token 解析
- 密码强度检�?
## Python 实现

```python
import base64, hashlib, hmac, uuid, json, re
from datetime import datetime
from typing import Dict, Optional

class CryptoEncoder:
    def __init__(self):
        self.history: list = []
    
    def base64_encode(self, text: str) -> str:
        """Base64编码"""
        result = base64.b64encode(text.encode("utf-8")).decode("ascii")
        self._log("base64_encode", text, result)
        return result
    
    def base64_decode(self, encoded: str) -> str:
        """Base64解码"""
        result = base64.b64decode(encoded.encode("ascii")).decode("utf-8")
        self._log("base64_decode", encoded, result)
        return result
    
    def url_encode(self, text: str) -> str:
        """URL编码"""
        from urllib.parse import quote
        result = quote(text, safe="")
        self._log("url_encode", text, result)
        return result
    
    def url_decode(self, encoded: str) -> str:
        """URL解码"""
        from urllib.parse import unquote
        result = unquote(encoded)
        self._log("url_decode", encoded, result)
        return result
    
    def sha256(self, text: str) -> str:
        """SHA256哈希"""
        result = hashlib.sha256(text.encode("utf-8")).hexdigest()
        self._log("sha256", text, result)
        return result
    
    def sha512(self, text: str) -> str:
        """SHA512哈希"""
        return hashlib.sha512(text.encode("utf-8")).hexdigest()
    
    def md5(self, text: str) -> str:
        """MD5哈希"""
        return hashlib.md5(text.encode("utf-8")).hexdigest()
    
    def hmac_sha256(self, message: str, key: str) -> str:
        """HMAC-SHA256签名"""
        return hmac.new(
            key.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
    
    def generate_uuid(self) -> str:
        """生成UUID v4"""
        return str(uuid.uuid4())
    
    def parse_jwt(self, token: str) -> dict:
        """解析JWT Token（不验证签名�?""
        parts = token.split(".")
        if len(parts) != 3:
            return {"error": "Invalid JWT format"}
        
        try:
            header = json.loads(base64.urlsafe_b64decode(parts[0] + "=="))
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
            return {
                "header": header,
                "payload": payload,
                "signature": parts[2][:20] + "...",
            }
        except Exception as e:
            return {"error": str(e)}
    
    def password_strength(self, password: str) -> dict:
        """密码强度检�?""
        score = 0
        checks = {
            "length": len(password) >= 8,
            "uppercase": bool(re.search(r"[A-Z]", password)),
            "lowercase": bool(re.search(r"[a-z]", password)),
            "digits": bool(re.search(r"\d", password)),
            "special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
        }
        score = sum(checks.values())
        
        if score <= 2:
            strength = "weak"
        elif score <= 3:
            strength = "fair"
        elif score <= 4:
            strength = "good"
        else:
            strength = "strong"
        
        return {
            "score": score,
            "max_score": 5,
            "strength": strength,
            "checks": checks,
        }
    
    def _log(self, operation: str, input_val: str, output_val: str):
        self.history.append({
            "operation": operation,
            "input": input_val[:50],
            "output": output_val[:50],
            "timestamp": datetime.now().isoformat()
        })
    
    def batch_encode(self, text: str) -> Dict[str, str]:
        """批量编码"""
        return {
            "original": text,
            "base64": self.base64_encode(text),
            "url": self.url_encode(text),
            "sha256": self.sha256(text),
            "md5": self.md5(text),
            "uuid": self.generate_uuid(),
        }

# 使用示例
crypto = CryptoEncoder()

# Base64
encoded = crypto.base64_encode("Hello, 世界!")
decoded = crypto.base64_decode(encoded)
print(f"Base64: {encoded}")
print(f"解码: {decoded}")

# URL编码
url_enc = crypto.url_encode("https://example.com/path?q=你好&lang=�?)
print(f"URL编码: {url_enc}")

# 哈希
print(f"SHA256: {crypto.sha256('password123')}")
print(f"MD5: {crypto.md5('Hello')}")

# HMAC
print(f"HMAC: {crypto.hmac_sha256('message', 'secret-key')}")

# UUID
print(f"UUID: {crypto.generate_uuid()}")

# JWT解析
jwt_token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWxpY2UiLCJleHAiOjE3MDkxMjM0NTZ9.signature"
parsed = crypto.parse_jwt(jwt_token)
print(f"JWT Header: {parsed.get('header')}")
print(f"JWT Payload: {parsed.get('payload')}")

# 密码强度
strength = crypto.password_strength("MyP@ssw0rd!")
print(f"密码强度: {strength['strength']} ({strength['score']}/{strength['max_score']})")

# 批量编码
batch = crypto.batch_encode("OpenCode 2026")
print(f"\n批量编码:")
for k, v in batch.items():
    print(f"  {k}: {v[:40]}")
```

## 编码对照

| 输入 | Base64 | SHA256 (�?�? | MD5 |
|------|--------|---------------|-----|
| `hello` | `aGVsbG8=` | `2cf24dba` | `5d41402a` |
| `12345` | `MTIzNDU=` | `8d969eef` | `827ccb0e` |

## 使用场景

1. **API认证**: Base64编码Basic Auth、Bearer Token
2. **数据完整�?*: SHA256校验文件哈希
3. **密码存储**: MD5/SHA256哈希（加盐）
4. **Token处理**: 解析JWT、生成API密钥
5. **Web开�?*: URL编码参数、CSRF Token生成

## 依赖

- Python 3.8+
- 标准库（base64, hashlib, hmac, uuid, json�?