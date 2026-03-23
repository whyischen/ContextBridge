# ContextBridge User Manual 📚

**ContextBridge** is your local AI knowledge base assistant. It enables Claude Code, Cursor, and other AI tools to read and understand Word, PDF, Excel, and other documents on your computer—no cloud uploads needed, all data processed locally with absolute privacy.

---

## Core Features

| Feature | Description |
|---------|-------------|
| 🔒 **Local Privacy** | 100% local execution, documents never leave your machine |
| 📄 **Multi-format Support** | One-click parsing for PDF, Word, Excel, PPTX, Markdown |
| 🧠 **Smart Parsing** | MarkItDown by default (lightweight), optional Docling for high precision |
| ⚡ **Real-time Sync** | Auto-detect folder changes, instant index updates |
| 🔋 **Ready to Use** | Built-in ChromaDB vector database, zero configuration |

---

## Quick Start (3 Minutes)

### Step 1: Installation

```bash
pip install cbridge-agent
```

### Step 2: Initialize and Start

```bash
cbridge init
```

Follow the prompts to choose:
1. **Interface Language**: `en` (English) or `zh` (Chinese)
2. **Workspace Directory**: Default is `~/ContextBridge_Workspace`
3. **Start Service**: Default is "Yes"—starts background monitoring immediately

After initialization, the service is already running in the background.

### Step 3: Add a Folder to Watch

```bash
cbridge watch add /Users/yourname/Documents/work-docs
```

ContextBridge will automatically index all documents in this folder.

---

## Common Commands

### Start/Stop Services

If you didn't start the service during initialization, or need manual control:

```bash
cbridge start        # Start background monitoring (Watcher + Vector DB)
cbridge serve        # Start API server (for external tool access)
cbridge stop         # Stop all background services
```

> **Note**: `start` launches file monitoring and search engine; `serve` starts the REST API server. For daily use, `start` is sufficient—only use `serve` for API access.

### Manage Watched Directories

```bash
# Add a directory to watch (supports multiple)
cbridge watch add /path/to/new-folder

# List watched directories
cbridge watch list

# Remove from watching
cbridge watch remove /path/to/folder
```

### 🔍 Test Search via CLI

Test search without opening your AI tool:

```bash
# Natural language query
cbridge search "What was the Q3 revenue figure"

# Fuzzy matching also works
cbridge search "Find the payment terms in that contract"
```

### 🌐 Connect to AI Tools (MCP)

For **Claude Code** or **Cursor** users, add this to your MCP settings:

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

After configuration, simply ask your AI:
> "Summarize the key projects from the budget spreadsheet"

The AI will automatically query ContextBridge to retrieve context from your local documents.

---

## Advanced Configuration

### Switch Parsing Strategy

ContextBridge supports two document parsing strategies:

| Strategy | Characteristics | Best For |
|----------|-----------------|----------|
| **MarkItDown** (Default) | Lightweight and fast, low resource usage | Daily document processing |
| **Docling** | High precision, preserves complex layouts | Academic papers, complex tables |

Modify the parsing strategy in your config file:

```yaml
parser:
  pdf_strategy: "docling"  # or "markitdown"
```

### Rebuild Index

Force a full vector index rebuild when needed:

```bash
cbridge index
```

> **Tip**: `cbridge start` includes automatic indexing, so manual rebuild is rarely needed.

### Switch Language

```bash
cbridge lang en    # Switch to English
cbridge lang zh    # Switch to Chinese
```

### Check Status

```bash
cbridge status     # View service status
cbridge config     # View configuration file
```

---

## Supported File Formats

| Format | Extensions | Notes |
|--------|------------|-------|
| PDF | `.pdf` | Supports both scanned (OCR) and text-based |
| Word | `.docx`, `.doc` | Preserves heading hierarchy |
| Excel | `.xlsx`, `.xls` | Parses tables as Markdown tables |
| PowerPoint | `.pptx`, `.ppt` | Extracts content from each slide |
| Markdown | `.md` | Native support |
| Text Files | `.txt`, `.csv` | Direct reading |

---

## FAQ

**Q: Are my documents sent to the cloud?**
A: No. All parsing, indexing, and retrieval happens locally—no internet connection or API key required.

**Q: How large can my documents be?**
A: Depends on your local memory; generally handles 100+ page PDFs without issues.

**Q: How quickly are new files indexed?**
A: Files are automatically synced to the index within 1-2 seconds of saving.

---

## Need Help?

- Project Home: https://github.com/whyischen/context-bridge
- Report Issues: Submit a GitHub Issue
