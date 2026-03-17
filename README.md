[**🇨🇳 中文**](README_zh-CN.md) | [**🇬🇧 English**](README.md)

# 🧠 ContextBridge (cbridge-agent)

> **The All-in-One Local Memory Bridge for AI Agents.**  
> Instantly feed real-world documents (PDFs, Office files, Markdown) to your local AI Agents (like OpenClaw, Claude Desktop, Cursor). Batteries included, zero configuration required.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/cbridge-agent.svg)](https://badge.fury.io/py/cbridge-agent)

## 💡 Why ContextBridge?

Most local AI Agents are great at reading code, but they are completely blind to the real-world business data hidden in your `.pdf`, `.docx`, and `.xlsx` files.

In the past, building a document retrieval system for your local Agent meant entering "configuration hell": *Install Node -> Install a Vector DB -> Configure environment variables -> Write parsing scripts -> Connect them all together...*

**ContextBridge ends all of this.** 
We packaged high-fidelity parsers (`MarkItDown`, `Docling`) and a blazing-fast embedded vector database (`ChromaDB`) into a single, standalone tool. No external dependencies, no complex setup. **Just `pip install`, and your Agent instantly gets a memory.**

---

## ✨ Core Features

- 🔋 **Batteries Included**: Built-in embedded `ChromaDB` vector database. No need to manually install environments or worry about vector index initialization. We handle it all under the hood.
- 👁️ **Zero-Touch Sync**: Just drop a file into your watched folder. ContextBridge uses a debounced `Watchdog` to monitor changes, automatically parses them in an asynchronous background queue, and instantly rebuilds the local vector index without blocking your workflow.
- 🧹 **Ghost Data Cleanup**: Automatically detects and cleans up "ghost data" (files deleted while the bridge was offline) during full indexing, ensuring your AI's memory is always perfectly synchronized with your local disk.
- 📄 **Multi-Format Parsing**: Flawlessly extracts text from PDFs (via `Docling`), Word, Excel, PPTX, and more (via `MarkItDown`).
- 🔌 **MCP & API Ready**: Exposes a clean local API and natively supports the **Model Context Protocol (MCP)**. Seamlessly integrates with Claude Desktop, Cursor, and OpenClaw.
- 🌐 **i18n Support**: Fully supports both English and Chinese interfaces (`cbridge lang en` / `cbridge lang zh`).
- 🔒 **100% Local & Private**: Does not rely on any cloud LLM APIs for storage. Your financial reports and core business documents never leave your hard drive.

---

## 🚀 Quick Start

Forget about tedious vector database setups. Everything is handled for you.

### 1. Installation

Install ContextBridge directly from PyPI (requires Python 3.9+):

```bash
pip install cbridge-agent
```

*(On the first run, ContextBridge will automatically download and initialize the built-in embedding models in the background).*

### 2. Initialize Workspace

```bash
cbridge init
```
Follow the interactive prompts to set up your workspace (defaults to `~/ContextBridge_Workspace`).

### 3. Add Folders to Watch

Tell ContextBridge which folders contain your documents:

```bash
cbridge watch add /path/to/your/documents
```

### 4. Start the Bridge

```bash
cbridge start
```
**That's it!** The background watcher and API server are now running silently. Any files you add, modify, or delete in your watched folders will be instantly synced to the vector database.

### 5. Manual Indexing & Cleanup (Optional)

If you made changes while the bridge was offline, you can force a full sync and clean up ghost data:

```bash
cbridge index
```

---

## 🤖 Connect Your AI Agent (MCP)

ContextBridge natively supports the **Model Context Protocol (MCP)**, making it the perfect plug-and-play memory module for modern AI Agents.

**For Claude Desktop / Cursor / OpenClaw:**
Simply add the ContextBridge MCP server to your Agent's configuration file:

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
Once connected, whenever your AI Agent needs to recall information from your office documents, it will autonomously query ContextBridge for precise, semantic retrieval.

---

## 🛠️ CLI Command Reference

ContextBridge provides an elegant CLI for managing your knowledge base:

- `cbridge init`: Interactively initialize configuration.
- `cbridge watch add <dir>`: Add a directory to monitor.
- `cbridge watch list`: List all monitored directories.
- `cbridge watch remove <dir>`: Stop monitoring a directory.
- `cbridge index`: Run a full index and clean up ghost data.
- `cbridge start`: Start the real-time watcher and API server.
- `cbridge serve`: Start only the API server.
- `cbridge search "your query"`: Test semantic search directly from the terminal.
- `cbridge status`: View current configuration and running status.
- `cbridge lang <en|zh>`: Switch display language.

---

## 🤝 Contributing

We welcome contributions of all kinds! If you are passionate about local AI, RAG technologies, and ultimate Developer Experience (DX), join us in building the strongest AI memory bridge.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).