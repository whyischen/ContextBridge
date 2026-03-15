# ContextBridge User Manual 📚

ContextBridge is a lightweight Knowledge Base plugin for AI Agents (like OpenClaw, Cursor, Claude Code). It gives your local AI assistants instant access to read and understand your local Office documents (Word, Excel, PDF, etc.) directly into high-fidelity Markdown context without cloud uploads.

## Installation

```bash
pip install cbridge-agent
```

## First Time Initialization

Run the initialization wizard to start the engine and set up your environment:

```bash
cbridge init
```

During initialization, you will be prompted to:
1. Choose the interface language (`en` or `zh`).
2. Choose the running mode (`embedded` or `external`). The default `embedded` mode is highly recommended for individual users as it does not require external database setups.
3. Configure your workspace directory. The default is `~/ContextBridge_Workspace`.

## Commands Guide

### 1. Monitor Folders (`watch`)

ContextBridge watches specific folders for any changes to your files to automatically build and update its vector index.

- **Add a folder to monitor:**
  ```bash
  cbridge watch add /path/to/your/folder
  ```

- **List monitored folders:**
  ```bash
  cbridge watch list
  ```

- **Stop monitoring a folder:**
  ```bash
  cbridge watch remove /path/to/your/folder
  ```

### 2. Manual Indexing (`index`)

If you want to manually trigger an indexing process for all your monitored folders:

```bash
cbridge index
```

### 3. Start Search Engine (`start`)

Start the background engine to watch directories in real-time and provide search capabilities:

```bash
cbridge start
```

### 4. Search (`search`)

You can test natural language queries via the CLI without using your agent:

```bash
cbridge search "Summarize Q3 revenue"
```

### 5. Start MCP Server (`mcp`)

If you are using ContextBridge as a Model Context Protocol (MCP) server for Claude Code or Cursor:

```bash
cbridge mcp
```

### 6. Switch Language (`lang`)

To change the interactive language displayed in the terminal:

```bash
cbridge lang en
# OR
cbridge lang zh
```

### 7. View Status and Config (`status` / `config`)

- **Check current running status:**
  ```bash
  cbridge status
  ```
- **View raw config file content:**
  ```bash
  cbridge config
  ```

## Integrating with AI Agents (MCP)

For clients fully supporting the Model Context Protocol (MCP) like **Cursor** or **Claude Code**, simply set the following configuration in your agent's MCP setup:

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

Once connected, your AI agents can autonomously query your local file contexts!
