# ContextBridge 使用手册 📚

ContextBridge 是一款专为 AI 智能体（如 OpenClaw、Cursor、Claude Code）设计的极速知识库外挂。它能让你的 AI 助手直接读取、理解本地的 Word、Excel、PDF 等文件，并提供高保真的 Markdown 上下文，无需上传至云端，隐私绝对安全。

## 安装

```bash
pip install cbridge-agent
```

## 首次初始化

您可以运行引导式命令启动引擎与环境配置：

```bash
cbridge init
```

初始化过程中，你需要指定：
1. 终端显示语言（`en` 或 `zh`）。
2. 运行模式（`embedded` 内置或 `external` 外置）。对于个人用户，强烈推荐默认的 `embedded` 模式，因为它可以让你在本地零配置运行向量搜索。
3. 工作区目录（默认为 `~/ContextBridge_Workspace`）。

## 核心使用指南

### 1. 文件夹监控 (`watch`)

ContextBridge 支持智能目录监控功能，能自动感知所绑定文件夹内文档的变化，并自动生成、同步向量索引。

- **添加监控目录：**
  ```bash
  cbridge watch add /你的目录绝对路径
  ```

- **查看正在监控的目录列表：**
  ```bash
  cbridge watch list
  ```

- **取消对某目录的监控：**
  ```bash
  cbridge watch remove /你的目录绝对路径
  ```

### 2. 手动构建索引 (`index`)

希望对手动修改过的大量文档进行一次性批量构建，可以运行：

```bash
cbridge index
```

### 3. 启动检索引擎 (`start`)

启动后台监控程序与核心搜索服务引擎：

```bash
cbridge start
```

### 4. 万能检索与测试 (`search`)

你可以在不使用 AI 的情况下，在命令行测试本地知识库：

```bash
cbridge search "帮我找一下最近那个表格里的项目预算是多少"
```

### 5. 启动 MCP 服务 (`mcp`)

如果您通过 Claude Code / Cursor 等客户端接入，需要直接开启 MCP 协议的服务端功能：

```bash
cbridge mcp
```

### 6. 一键切换语言 (`lang`)

一键在命令行中英语言间进行无缝切换：

```bash
cbridge lang zh
# 或者
cbridge lang en
```

### 7. 查看运行状态与配置 (`status` / `config`)

- **查看当前程序详细运行状态：**
  ```bash
  cbridge status
  ```
- **展示配置文件的原始内容：**
  ```bash
  cbridge config
  ```

## 🔌 接入你的 AI 智能体 (MCP 协议)

对于支持 MCP (Model Context Protocol) 协议的本地 AI 工具（如 **Claude Code** 或 **Cursor**），将以下配置加入智能体配置文件即可：

```json
{
  "mcpServers": {
    "context-bridge": {
      "command": "cbridge",
      "args": ["mcp"]
    }
  }
}
```

绑定成功后，当你的 AI 需要搜索参考特定的文档上下文时，就会自动自主向 ContextBridge 提问检索！
