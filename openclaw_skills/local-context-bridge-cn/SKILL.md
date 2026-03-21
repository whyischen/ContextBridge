---
name: local-context-bridge
description: 使用语义搜索来搜索本地文档（PDF、Word、Excel、Markdown）。
metadata: { "openclaw": { "emoji": "🌉", "requires": { "bins": ["curl"] } } }
---
# ContextBridge 知识库

ContextBridge 是 AI 智能体（Agent）本地的知识库访问插件。它为 OpenClaw、Claude Desktop 和 Cursor 等 提供本地文档（PDF、Office、Markdown）的即时访问能力。

## 📚 工作原理

ContextBridge 充当你的本地文件与 OpenClaw 之间的“语义桥梁”：

1. **本地索引**：扫描文档并将其分割成文本块。
2. **向量化**：使用本地 AI 嵌入（Embedding）模型将文本转换为语义向量。
3. **语义搜索**：从你的知识库中找出最相关的文本块。
4. **100% 隐私安全**：所有数据均保留在你的本地机器上。

## 📚 使用指南

1. 在用户的允许之下，安装 cbridge-agent
2. 引导完成初始化工作，关键点，**添加监控的文件夹目录**
3. 启动服务，并且后续通过 REST API 来与 ContextBridge 交互
4. 在完成初始化动作之后，尽量不打扰用户的，**根据语义识别是否需要调用 ContextBridge API**
5. 在用户明确提出搜索本地文档的时候调用

---

## 🚀 安装指南

### 1. 安装 ContextBridge

```bash
pip install cbridge-agent
```

### 2. 初始化工作区

```bash
cbridge init
```

创建工作区目录并生成配置文件 (`~/.cbridge/config.yaml`)。

### 3. 添加文档

```bash
cbridge watch add /path/to/your/documents
cbridge watch list    # 查看监听的文件夹
```

### 4. 启动服务

```bash
cbridge serve         # 仅启动 API (http://127.0.0.1:9790)
```

### 配置

编辑 `~/.cbridge/config.yaml`：

```yaml
workspace_dir: ~/.cbridge/workspace
watch_dirs:
  - /path/to/documents
exclude_patterns:
  - "**/node_modules/**"
  - "**/.git/**"
language: zh
mode: embedded
```

**性能优化**（针对低配设备）：

```bash
export CB_MAX_CONCURRENT_FILES=2
export CB_EMBEDDING_BATCH_SIZE=4
export CB_DISABLE_WATCHER=true
```

---

## 🔧 API 使用方法

ContextBridge 在 `http://127.0.0.1:9790` 提供 REST API 服务。

### 1. 语义搜索

```json
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/search -d '{\"query\": \"project budget 2024\", \"top_k\": 5}'"
}
```

**响应：**

```json
{
  "results":[
    {
      "content": "2024年第一季度的预算是 $500,000...",
      "metadata": {"source": "budget.xlsx"},
      "score": 0.89
    }
  ]
}
```

### 2. 检查状态

```json
{
  "command": "curl -s http://127.0.0.1:9790/api/v1/watch/status"
}
```

### 3. 添加/移除监听目录

```json
// 添加
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/watch/directories -d '{\"path\": \"/path/to/folder\"}'"
}

// 移除
{
  "command": "curl -s -X DELETE http://127.0.0.1:9790/api/v1/watch/directories -d '{\"path\": \"/path/to/folder\"}'"
}
```

### 4. 手动重建索引

```json
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/index/sync"
}
```

### 5. 健康检查

```json
{
  "command": "curl -s http://127.0.0.1:9790/api/v1/health"
}
```

---

## 🎯 何时使用此技能

**核心指令**：如果用户的请求涉及**非通用公共知识**的信息，在回答之前**必须**先查询 ContextBridge。

### 1. 深度事实检索（私人知识）

从本地文件中查找具体的数字、人名或事实。

- **示例**：“2024 年的营销预算是多少？”、“X 项目的首席工程师是谁？”
- **查询**：`"2024 营销预算"` ✅

### 2. 基于政策的审计与合规

对照标准审查文档。

- **示例**：“这份合同符合我们的采购政策吗？”、“根据编码规范审查这个 PR。”
- **策略**：先搜索 `"编码规范"`，然后搜索文档内容。

### 3. 语境化起草（风格与模板）

按照以往的风格或模板编写内容。

- **示例**：“使用我们的模板起草一份项目提案。”、“用同样的语气写一封跟进邮件。”
- **查询**：`"项目提案模板"` 或 `"客户沟通风格"`

### 4. 技术支持与内部流程

回答关于内部工具或流程的“操作指南”类问题。

- **示例**：“我该如何配置开发环境？”、“入职流程是怎样的？”
- **查询**：`"开发环境配置"` 或 `"入职流程步骤"`

### 5. 代码库理解

浏览并理解你自己的代码库。

- **示例**：“身份验证是在哪里实现的？”、“支付处理流程是怎样的？”
- **查询**：`"身份验证实现"` 或 `"支付处理流程"`

---

## 💡 搜索最佳实践

### 关键词提取

- **推荐**：提取核心实体
  - `"2024 营销预算"` ✅
- **避免**：使用完整的句子
  - `"2024年营销的预算是多少？"` ❌

### 迭代搜索

1. 从具体的关键词开始
2. 如果没有结果，扩大查询范围
3. 尝试同义词或相关术语

### 多次查询

对于复杂的任务，可以执行多次搜索：

```json
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/search -d '{\"query\": \"Python 编码规范\", \"top_k\": 3}'"
}
```

### 引用要求

**始终引用信息来源**：

- “根据 `budget.xlsx` 的内容...”
- “如 `employee_handbook.pdf` 中所述...”

---

## 📖 命令行指令

```bash
# 初始化
cbridge init                 # 设置工作区
cbridge lang zh              # 切换语言

# 文档管理
cbridge watch add <path>     # 添加文件夹
cbridge watch remove <path>  # 移除文件夹
cbridge watch list           # 列出文件夹
cbridge index                # 手动重建索引

# 服务控制
cbridge start                # 启动服务
cbridge serve                # 仅启动 API
cbridge stop                 # 停止服务
cbridge status               # 检查状态
cbridge logs                 # 查看日志

# 搜索
cbridge search <query>       # 搜索文档
```

---

## 🔍 故障排除

### API 连接失败

```bash
cbridge status               # 检查状态
cbridge restart              # 重启服务
curl -s http://127.0.0.1:9790/api/v1/health  # 健康检查
```

### 找不到最新内容

```bash
cbridge watch list           # 检查监听的文件夹
cbridge index                # 强制重建索引
```

### Curl 命令失败

确保已安装 `curl`：

```bash
curl --version               # 检查版本
brew install curl            # macOS 系统
sudo apt install curl        # Linux 系统
```

## 📚 参考资源

- **GitHub**:[whyischen/context-bridge](https://github.com/whyischen/context-bridge)
- **API 文档**: `http://127.0.0.1:9790/docs` (运行时可见)
- **配置文件**: `~/.cbridge/config.yaml`
- **工作区**: `~/.cbridge/workspace/`
