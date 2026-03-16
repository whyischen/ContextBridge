[**🇨🇳 中文**](README_zh-CN.md) | [**🇬🇧 English**](README.md)

# 🧠 ContextBridge (cbridge-agent)

> **AI Agent 的一站式本地记忆桥梁。**  
> 为你的本地 AI Agent（如 OpenClaw, Claude Desktop, Cursor）即刻投喂真实世界的文档（PDF、Office、Markdown）。自带引擎，开箱即用，零配置。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/cbridge-agent.svg)](https://badge.fury.io/py/cbridge-agent)

## 💡 为什么开发 ContextBridge？

大多数本地 AI Agent 擅长阅读代码，但面对隐藏在 `.pdf`、`.docx` 和 `.xlsx` 文件里的真实业务数据时，它们却像“瞎子”一样。

在过去，如果你想为本地 Agent 搭建一个文档检索系统，你必须经历一场“配置地狱”：*装 Node -> 装向量数据库 -> 配置各种环境变量 -> 写个解析脚本 -> 把它们全连起来……*

**ContextBridge 终结了这一切。** 
我们将高保真解析神器（`MarkItDown`、`Docling`）和极速的内嵌向量数据库（`ChromaDB`）直接打包成了一个独立工具。没有外部依赖，告别繁琐配置。**只需 `pip install`，你的 Agent 瞬间就拥有了记忆。**

---

## ✨ 核心特性

- 🔋 **自带引擎 (Batteries Included)**：内置了 `ChromaDB` 向量数据库。不再需要手动安装环境或操心向量索引的初始化，我们在底层全替你搞定。
- 👁️ **无感同步 (Zero-Touch Sync)**：只需把文件丢进监听目录，ContextBridge 会通过带有防抖机制的 `Watchdog` 监听变更，在后台异步队列中自动解析，并瞬间重建本地向量索引，绝不阻塞你的工作流。
- 🧹 **幽灵数据清理 (Ghost Data Cleanup)**：在全量索引时，自动检测并清理“幽灵数据”（即在 ContextBridge 离线期间被删除的文件），确保 AI 的记忆与本地磁盘绝对同步。
- 📄 **多格式解析 (Multi-Format Parsing)**：完美提取 PDF（基于 `Docling`）、Word、Excel、PPTX 等文件中的文本（基于 `MarkItDown`）。
- 🔌 **原生支持 MCP 协议**：对外提供纯净的本地 API 与最新的 **MCP (Model Context Protocol)** 接口。只需一行配置，即可无缝接入 Claude Desktop、Cursor 或 OpenClaw。
- 🌐 **多语言支持 (i18n)**：全面支持中英文界面切换（`cbridge lang zh` / `cbridge lang en`）。
- 🔒 **100% 本地与绝对隐私**：不依赖任何云端大模型 API 进行存储。你的财务报表和核心业务文档永远只留在你的电脑硬盘里。

---

## 🚀 快速开始

忘掉那些繁琐的向量数据库和 CLI 工具安装教程吧，一切交给我们。

### 1. 安装 ContextBridge

直接通过 PyPI 安装（需要 Python 3.9+ 环境）：

```bash
pip install cbridge-agent
```

*(在首次运行时，ContextBridge 会在后台自动拉取并初始化内置的向量模型)*。

### 2. 初始化工作区

```bash
cbridge init
```
跟随交互式向导完成工作区配置（默认路径为 `~/ContextBridge_Workspace`）。

### 3. 添加监控目录

告诉 ContextBridge 你的文档存放在哪里：

```bash
cbridge watch add /你的/文档/路径
```

### 4. 启动引擎

```bash
cbridge start
```
**搞定了！** 监控后台和 API 服务已经在静默运行。你在监控目录中添加、修改或删除的任何文件，都会被瞬间同步到向量数据库中。

### 5. 手动索引与清理（可选）

如果你在 ContextBridge 离线期间修改了文件，可以强制进行一次全量同步并清理幽灵数据：

```bash
cbridge index
```

---

## 🤖 接入你的 AI Agent (基于 MCP)

ContextBridge 原生支持 **Model Context Protocol (MCP)** 协议，这让它成为了现代 AI Agent 即插即用的完美记忆模块。

**对于 Claude Desktop / Cursor / OpenClaw：**
你只需要在 Agent 的 MCP 配置文件中加入 ContextBridge 的服务路径即可：

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
连接成功后，每当你的 AI Agent 需要回想你的办公文档信息时，它就会自主调用 ContextBridge 进行精准的高级语义查询。

---

## 🛠️ CLI 命令速查

ContextBridge 提供了一个优雅的命令行工具来管理你的知识库：

- `cbridge init`: 交互式初始化配置。
- `cbridge watch add <dir>`: 添加一个新的监控目录。
- `cbridge watch list`: 列出所有正在监控的目录。
- `cbridge watch remove <dir>`: 移除指定的监控目录。
- `cbridge index`: 对所有监控目录进行一次性全量索引，并清理幽灵数据。
- `cbridge start`: 启动 ContextBridge 实时监控服务与 API 服务。
- `cbridge serve`: 仅启动 API 服务。
- `cbridge search "你的问题"`: 在终端中直接测试语义检索。
- `cbridge status`: 查看当前配置和运行状态。
- `cbridge lang <zh|en>`: 切换显示语言。

---

## 🤝 参与贡献

我们极其欢迎任何形式的贡献！如果你对本地化 AI、RAG 技术以及极致的开发者体验（DX）充满热情，请加入我们，一起构建最强的 AI 记忆桥梁。

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的代码 (`git commit -m 'Add some AmazingFeature'`)
4. 推送至远端分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📜 许可证

本项目采用 [MIT License](LICENSE) 协议开源。