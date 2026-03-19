---
name: local-context-bridge
description: Search local documents (PDF, Word, Excel, Markdown) using semantic search.
metadata: { "openclaw": { "emoji": "🌉", "requires": { "bins": ["curl"] } } }
---

# ContextBridge Knowledge Base

ContextBridge is a local AI agent's memory bridge. It provides instant access to your documents (PDF, Office, Markdown) for AI agents like OpenClaw, Claude Desktop, and Cursor.

## 📚 HOW IT WORKS

ContextBridge acts as a "Semantic Bridge" between your files and OpenClaw:

1. **Local Indexing**: Scans documents and splits them into text chunks.
2. **Vectorization**: Converts text into semantic vectors using a local AI embedding model.
3. **Semantic Search**: Finds the most relevant chunks from your knowledge base.
4. **100% Private**: All data stays on your local machine.

**Key Features:**
- 🔌 **MCP and API Ready**: Native support for Model Context Protocol
- 📄 **Multi-format Parsing**: PDF, Word, Excel, PPTX, Markdown
- 🔋 **Batteries Included**: Embedded vector database
- 👁️ **Auto Sync**: Automatic file monitoring and index rebuilding

---

## 🚀 INSTALLATION

### 1. Install ContextBridge
```bash
pip install cbridge-agent
```

### 2. Initialize Workspace
```bash
cbridge init
```
Creates workspace directories and generates config file (`~/.cbridge/config.yaml`).

### 3. Add Documents
```bash
cbridge watch add /path/to/your/documents
cbridge watch list    # View watched folders
```

### 4. Start Service
```bash
cbridge serve         # API only (http://127.0.0.1:9790)
```

### Configuration
Edit `~/.cbridge/config.yaml`:
```yaml
workspace_dir: ~/.cbridge/workspace
watch_dirs:
  - /path/to/documents
exclude_patterns:
  - "**/node_modules/**"
  - "**/.git/**"
language: en
mode: embedded
```

**Performance Optimization** (for low-end devices):
```bash
export CB_MAX_CONCURRENT_FILES=2
export CB_EMBEDDING_BATCH_SIZE=4
export CB_DISABLE_WATCHER=true
```

---

## 🔧 API USAGE

ContextBridge provides a REST API at `http://127.0.0.1:9790`.

### 1. Semantic Search
```json
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/search -d '{\"query\": \"project budget 2024\", \"top_k\": 5}'"
}
```

**Response:**
```json
{
  "results": [
    {
      "content": "The 2024 Q1 budget is $500,000...",
      "metadata": {"source": "budget.xlsx"},
      "score": 0.89
    }
  ]
}
```

### 2. Check Status
```json
{
  "command": "curl -s http://127.0.0.1:9790/api/v1/watch/status"
}
```

### 3. Add/Remove Watch Directory
```json
// Add
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/watch/directories -d '{\"path\": \"/path/to/folder\"}'"
}

// Remove
{
  "command": "curl -s -X DELETE http://127.0.0.1:9790/api/v1/watch/directories -d '{\"path\": \"/path/to/folder\"}'"
}
```

### 4. Manual Re-index
```json
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/index/sync"
}
```

### 5. Health Check
```json
{
  "command": "curl -s http://127.0.0.1:9790/api/v1/health"
}
```

---

## 🎯 WHEN TO USE THIS SKILL

**DIRECTIVE**: If the user's request involves information NOT in general public knowledge, MUST query ContextBridge before answering.

### 1. Deep Fact Retrieval (Private Knowledge)
Find specific numbers, names, or facts from local files.
- **Examples**: "What was the 2024 marketing budget?", "Who was the lead engineer for Project X?"
- **Query**: `"2024 marketing budget"` ✅

### 2. Policy-Based Auditing & Compliance
Review documents against standards.
- **Examples**: "Does this contract follow our procurement policy?", "Review this PR based on coding standards."
- **Strategy**: First search `"coding standards"`, then search document content.

### 3. Contextual Drafting (Style & Templates)
Write content matching previous style or templates.
- **Examples**: "Draft a project proposal using our template.", "Write a follow-up email in the same tone."
- **Query**: `"project proposal template"` or `"client communication style"`

### 4. Technical Support & Internal Processes
Answer "How-to" questions about internal tools or processes.
- **Examples**: "How do I set up the dev environment?", "What's the onboarding process?"
- **Query**: `"development environment setup"` or `"onboarding process steps"`

### 5. Codebase Understanding
Navigate and understand your own codebase.
- **Examples**: "Where is authentication implemented?", "How does payment processing work?"
- **Query**: `"authentication implementation"` or `"payment processing flow"`

---

## 💡 SEARCH BEST PRACTICES

### Keyword Extraction
- **DO**: Extract core entities
  - `"2024 marketing budget"` ✅
- **DON'T**: Use full sentences
  - `"What was the budget for 2024 marketing?"` ❌

### Iterative Searching
1. Start with specific keywords
2. If no results, broaden query
3. Try synonyms or related terms

### Multiple Queries
For complex tasks, execute multiple searches:
```json
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/search -d '{\"query\": \"coding standards python\", \"top_k\": 3}'"
}
```

### Citation Requirement
**Always cite sources**:
- "According to `budget.xlsx`..."
- "As documented in `employee_handbook.pdf`..."

---

## 📖 CLI COMMANDS

```bash
# Initialization
cbridge init                 # Setup workspace
cbridge lang en              # Switch language

# Document Management
cbridge watch add <path>     # Add folder
cbridge watch remove <path>  # Remove folder
cbridge watch list           # List folders
cbridge index                # Manual re-index

# Service Control
cbridge start                # Start service
cbridge serve                # API only
cbridge stop                 # Stop
cbridge status               # Check status
cbridge logs                 # View logs

# Search
cbridge search <query>       # Search documents
```

---

## 🔍 TROUBLESHOOTING

### API Connection Failed
```bash
cbridge status               # Check status
cbridge restart              # Restart service
curl -s http://127.0.0.1:9790/api/v1/health  # Health check
```

### Cannot Find Latest Content
```bash
cbridge watch list           # Check watched folders
cbridge index                # Force re-index
```

### Curl Command Fails
Ensure `curl` is installed:
```bash
curl --version               # Check version
brew install curl            # macOS
sudo apt install curl        # Linux
```

---

## 📝 WORKFLOW EXAMPLES

### Example 1: Find Project Budget
**User asks:** "What was the total budget for Project Alpha?"

**Agent actions:**
1. Extract keywords: `"Project Alpha budget"`
2. Execute search:
```json
{
  "command": "curl -s -X POST http://127.0.0.1:9790/api/v1/search -d '{\"query\": \"Project Alpha budget\", \"top_k\": 3}'"
}
```
3. Cite source: "According to `project_alpha_proposal.pdf`, the total budget was $150,000."

### Example 2: Code Review
**User asks:** "Review this Python function for compliance with our coding standards."

**Agent actions:**
1. Search for standards: `"Python coding standards"`
2. Search for examples: `"Python best practices"`
3. Compare and provide feedback with citations.

---

## 📚 RESOURCES

- **GitHub**: [whyischen/context-bridge](https://github.com/whyischen/context-bridge)
- **API Docs**: `http://127.0.0.1:9790/docs` (when running)
- **Config**: `~/.cbridge/config.yaml`
- **Workspace**: `~/.cbridge/workspace/`
