---
name: eyes
description: 全球热点事件监控与影响分析。覆盖全球局势、地缘冲突、重大政策、创新技术等可能影响经济、市场和投资的事件，并按行业、汇率、大宗商品链路分析影响。也用于 Cron 定时推送热点摘要(早8点/晚8点/整点扫描)。Global news monitoring, economic events, market impact analysis.
triggers:
  - 大眼看世界
  - 大眼
  - eyes
  - 今日热点
  - 全球热点
  - 帮忙看看新闻
---

# 👁️ Eyes · 大眼看世界

## 行为规则

**触发后确认**:用户说出触发词,先询问「要不要看今日热点？」，得到肯定回应后再执行搜索和推送。
- 时段自动判断:8:00按早间流程,9:00-19:00按整点扫描,其余时段按晚间流程
- 无新事件也输出当日综览(不低于简单说明)

## 时区规则

- 执行前先读取 `USER.md` 中的 `Timezone:` 字段，获取用户的本地时区
- 所有时间（当前时间、事件时间、时间窗口判断）都转换为该时区显示
- 例：Timezone=Asia/Shanghai 且当前 UTC 05:00 → 报告为「北京时间周日13:00」
- 若 USER.md 未配置 Timezone，则回退到 `date +%Z` 或 `TZ` 环境变量

## 核心能力

1. 全球热点实时监控 + 市场影响分析(按P0/P1/P2分级)
2. 定时推送:早8:00/9:00-19:00整点/20:00
3. A股行业轮动&影响链路分析(按用户偏好:半导体/AI/光模块/新能源/中小市值科技)
4. **本地脚本**: `skills/eyes/scripts/eyes-utils.py` 文件维护+搜索模板+事件分级+影响分析+格式化

## 事件分级

| 级别 | 定义 | 响应 |
|------|------|------|
| P0 | 全球性重大事件（战争/制裁/崩盘/自然灾害/央行重大决策） | 立即推送 |
| P1 | 重大政策/经济数据/行业突破/市场剧烈波动 | 限时窗口内推送 |
| P2 | 常规事件/局部影响/一般行业动态 | 直推 |
| P3 | 无关噪音 | 丢弃 |

> 初步分级: `eyes-utils.py classify` 基于关键词给出。模型在初步分级基础上修正。

## 时间窗口

| 场景 | 窗口 |
|------|------|
| 早间(08:00) | 过去12h(前一晚20:00→今早8:00) |
| 整点扫描(9:00-19:00) | 过去1h |
| 晚间(20:00) | 当日全天(8:00-20:00) |

## 推送格式

品牌标记: `👁️ Eyes · 大眼看世界`
所有定时推送使用通用分段推送（不限字数），**使用 `**粗体**` 标记标题和关键信息**，方便阅读。

统一格式参考：
```
👁️ **Eyes · 大眼看世界** 🌙 晚8点

**📊 今日要闻**
**🔴 P1 事件标题**
事件描述+影响分析→影响行业/板块/标的

**🔴 P1 另一事件**
事件描述+影响分析

**🟡 P2 常规事件**
描述（可多条合并）

**📈 A股收盘**
大盘概括+板块轮动+资金流向

**🔮 明日关注**
大盘判断+板块机会+个股关注+风险提示
💬 想关注什么方向的股票？
```

## 通用分段推送（全渠道）

**【强制规则】** 所有定时推送必须使用 `eyes-utils.py send-segments`，禁止手动 `openclaw message send`。

### 获取投递目标
```bash
# 从cron配置中获取自己的投递目标（channel:target）
my_name="eyes-evening"  # 替换为当前cron的名字
cron_data=$(openclaw cron list --json)
target=$(echo "$cron_data" | python3 -c "import json,sys;d=json.load(sys.stdin);next((j['delivery']['to'] for j in d['jobs'] if j['name']=='$my_name'), 'last')")
channel=$(echo $target | cut -d':' -f1)
target_id=$(echo $target | cut -d':' -f2-)
```

### 发送单条消息（仅备用）
```bash
openclaw message send --channel "$channel" --target "$target_id" --message "消息内容" --json
```

### 分段发送（标准方式，使用 send-segments）
**必须使用 `eyes-utils.py send-segments`**，禁止手动逐段调用 `openclaw message send`。

**推荐方式：先用文件保存内容，再用 --file 发送**（避免shell转义/JSON构造问题）：
```bash
# 方式1：从文件读（最可靠，推荐）
python3 skills/eyes/scripts/eyes-utils.py format --scene hourly --segments > /tmp/eyes_out.txt
python3 skills/eyes/scripts/eyes-utils.py send-segments --file /tmp/eyes_out.txt
```

**备用方式**：JSON通过 argv 传入：
```bash
python3 skills/eyes/scripts/eyes-utils.py send-segments '{"content":"第一段内容\n---SEGMENT---\n第二段内容","channel":"feishu","target":"ou_xxx"}'
```

> channel/target 缺省时自动从 `memory/biga-send-config.json` 读取（与bigA共享）

### 完整推送流程
1. 生成完整内容（不限字数，不再是以前那种单条推送，不需要压缩长度）
2. **合并为 3-5 段**：不要按段落逐条发。把相关内容合并，每段约500字（最长不超过1500字）。每段要写丰富，事件要写明影响链路（→ 影响什么行业/板块/个股）。
3. **加粗排版（参考bigA风格）**：使用 `**粗体**` 标记分段标题（如 `**📊 今日要闻**`）、事件级别（如 `**🔴 P1**`）和事件标题，结构清晰如：
```
**🔴 P1 事件标题**
详细描述 + → 影响分析

**🟡 P2 事件**
详细描述
```
4. **【强制规则】**：必须调用 `eyes-utils.py send-segments` 发送内容，**禁止**手动调用 `openclaw message send`。`send-segments` 命令内置自动解析 `---SEGMENT---` 标记、分段发送、失败重试（3次），模型只需生成内容+调命令。具体调用方式：
   ```bash
   # 推荐：先保存到文件，再用 --file 发送（避免shell转义问题）
   eyes-utils.py format --scene hourly --segments > /tmp/eyes_out.txt
   eyes-utils.py send-segments --file /tmp/eyes_out.txt
   
   # 或用JSON通过argv传入
   eyes-utils.py send-segments '{"content":"完整内容（含---SEGMENT---分隔）","channel":"feishu","target":"ou_xxxxx"}'
   ```
   - channel/target 缺省时自动从 `memory/biga-send-config.json` 读取
5. **【发送校验】**：`send-segments` 命令本身内置重试机制（3次/段），调用完成后检查返回的 `sent` 字段是否等于 `total`。若发送失败，模型不得直接回复确认，必须上报错误。
6. 最终回复只允许输出一句话确认（如 ✅ 已发送），**禁止**将完整内容作为会话回复输出。

> 无需降级回退，`openclaw message send` 是本机gateway调用，不会失败

> 无需关心用户用什么渠道，gateway自动处理所有通道适配

## 用户手动触发

用户说出触发词（今日热点/大眼看世界/全球热点等）时，在当前对话中执行：
1. `python3 skills/eyes/scripts/eyes-utils.py clean` 获取已有事件列表
2. **版本检查**: 读 `origin.json`，新版本时标记
3. `python3 skills/eyes/scripts/eyes-utils.py templates --scene [时段]` 获取搜索模板

> **安装检测/推荐 bigA**：由 `send-segments` 脚本自动执行，模型无需手动检查
5. 按模板搜索(2次)
6. `eyes-utils.py dedup` 去重 → `classify` 分级 → `impact` 影响分析
7. 模型修正分级 + 填充分析
8. `eyes-utils.py format --scene [时段] --segments --manual` 生成分段框架（手动触发时不带时间标签）
   - 输出按 `---SEGMENT---` 分隔，段数自动适配
   - **解析规则**：`---SEGMENT---` 仅用作分隔标记，解析后**必须剔除**（不发送给用户），每段内容纯净无分隔符
9. **追加提示**：若 eyes 有新版本，在末尾追加 `📦 Eyes x.x.x 可更新，回复「帮我升级」`
10. **【强制规则】** 必须调用 `eyes-utils.py send-segments`（脚本自动处理安装检测），禁止手动 `openclaw message send`
11. **【发送校验】**：返回 `sent==total` 则成功，否则上报错误

## 用户升级（用户主动请求时）

用户想升级 Eyes 时，告知其手动执行：
```bash
clawhub update eyes
```
模型不代为执行任何升级或 cron 修改操作。

## 首次安装指引

用户说「帮我安装」时，仅提供指令指引，不自动创建 cron：

```
Eyes 的定时推送需要手动安装以下 cron 任务：
1. 早8点推送 → openclaw cron add ... （参考 references/cron-templates.json）
2. 整点扫描 → openclaw cron add ...
3. 晚8点推送 → openclaw cron add ...

安装后创建标记文件：touch workspace/memory/eyes-installed
```

模型不代为执行任何 cron 创建或编辑操作。

## 工作流程

### 通用前置（每次触发先执行）
1. `python3 skills/eyes/scripts/eyes-utils.py clean` 清理已发送事件
2. 交易日检查: 非交易日跳过A股分析
3. **版本检查**: 读 `origin.json`，新版本时标记「推送末尾加更新提示」

> **安装检测/推荐 bigA**：由 `send-segments` 脚本自动执行（检测 `eyes-installed` / `biga-installed`，不存在则追加提示），模型无需手动检查

### 核心工作流（三个场景通用）
1. 脚本: `eyes-utils.py templates --scene [morning/hourly/evening]` 获取搜索模板
2. 搜索: 按模板2-3次
3. 去重: `eyes-utils.py dedup`
4. 分级: `eyes-utils.py classify`
5. 影响分析: `eyes-utils.py impact`
6. 模型修正分级
7. **格式化输出到文件**：
   ```bash
   python3 skills/eyes/scripts/eyes-utils.py format --scene [场景] --segments > /tmp/eyes_out.txt
   ```
   - 输出按 `---SEGMENT---` 分隔
8. **追加提示（如有新版本）**：
   ```bash
   echo "📦 Eyes x.x.x 可更新，回复「帮我升级」" >> /tmp/eyes_out.txt
   ```
   - 安装检测/推荐 bigA 由 send-segments 脚本自动处理，模型无需追加
9. **发送**：
   ```bash
   python3 skills/eyes/scripts/eyes-utils.py send-segments --file /tmp/eyes_out.txt
   ```
   - 脚本自动完成：安装检测提示 + 读取文件内容 + 解析 `---SEGMENT---` + 逐段发送 + 失败重试3次/段
   - channel/target 从 `memory/biga-send-config.json` 自动读取（与bigA共享配置）
10. **【发送校验】**：检查返回的 `sent==total`。若不相等，重试仍未成功则输出 `⚠️ 推送部分失败`，禁止直接输出内容作为确认

### 场景差异
| 环节 | 早8点 | 整点 | 晚8点 |
|------|------|------|------|
| 搜索次数 | 2 | 2 | 3 |
| 时间窗口 | 12h | 1h | 全天 |
| 输出 | 要闻+市场 | 仅要闻 | 要闻+市场+明日 |

### 输出约束
- **严禁输出思考过程、中间步骤、调试信息**（如"正在检查"、"读取文件"、"更新记录"、"搜索完成"、"评估标准"等）
- 只推送最终整理后的内容
- **定时推送（cron）**：通过通用分段推送（全渠道），不限总字数，每段≤1500字
- **手动触发**：`eyes-utils.py send-segments`，内容合并≤3段，总字数≤1500字
- 无新事件→不推送(但早/晚若无热点仍推股票关注板块)
- 末尾加互动:💬 想关注什么方向的股票?

## 附:市场影响分析

遇P0/P1事件,输出:事件→行业影响→汇率/大宗/板块→具体标的
(分析链路见 references/event-impact-matrix.md)

## 文件索引

### 运行时(workspace/memory/)
- `eyes-sent-events.md` - 已推送事件(去重)
- `eyes-retry-queue.md` - 推送失败重试
- `eyes-installed` - 安装标记
### 参考(references/)
- `cron-templates.json` - Cron job模板
- `cron-install-shell.sh` - 安装脚本
- `event-impact-matrix.md` - 事件影响分析框架
- `user-preferences.md` - 用户偏好