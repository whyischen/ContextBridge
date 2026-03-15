# OpenClaw Integration Guide

ContextBridge can be seamlessly integrated into OpenClaw as a Skill, enabling your AI agents to directly access and understand your local documents.

## What is Local ContextBridge Skill?

Local ContextBridge Skill is a powerful OpenClaw extension that provides:

- **Real-time Document Access** - Search and retrieve your local Word, Excel, PDF, and Markdown files instantly
- **Vector Search** - Intelligent semantic search across your document collection
- **Auto-Indexing** - Automatic parsing and indexing of new or modified documents
- **Zero Upload** - All documents stay on your machine, ensuring privacy and security
- **Smart Environment Detection** - Automatically detects system environment and selects best configuration
- **Namespace Isolation** - Supports sharing QMD and OpenViking services with other applications

## Prerequisites

Before enabling Local ContextBridge Skill in OpenClaw, ensure you have:

- OpenClaw installed and configured
- Python 3.8 or higher

## Installation and Configuration

### Enable Skill in OpenClaw

1. Open OpenClaw Skill marketplace
2. Search for "local-context-bridge"
3. Click "Install"
4. Skill will automatically start the installation guide

### Automatic Installation Guide

The Skill will automatically complete the following for you:

✅ **Environment Detection**
- Detects your system environment
- Automatically selects the best configuration mode

✅ **ContextBridge Installation**
- Automatically installs cbridge-agent (if needed)
- Initializes configuration

✅ **Mode Selection**
- **Embedded Mode** (default): Uses built-in ChromaDB
- **External Mode** (auto-detected): Connects to existing QMD and OpenViking services

✅ **Workspace Initialization**
- Creates necessary directories
- Initializes vector database

After installation, the Skill is ready to use.

## Using ContextBridge in OpenClaw

Once installed, you can use Local ContextBridge Skill in your OpenClaw workflows:

### Supported Capabilities

The Skill provides the following 7 capabilities:

1. **search_documents** - Search local documents
   ```
   "Search my documents for information about project architecture"
   ```

2. **setup_environment** - Reconfigure environment
   ```
   "Reinitialize ContextBridge environment"
   ```

3. **detect_environment** - Detect current environment
   ```
   "Detect my system environment"
   ```

4. **add_watch_directory** - Add directory to monitor
   ```
   "Add ~/Documents to watch directories"
   ```

5. **remove_watch_directory** - Remove directory from monitor
   ```
   "Remove ~/Downloads from watch directories"
   ```

6. **get_watch_directories** - Get list of monitored directories
   ```
   "List all monitored directories"
   ```

7. **get_status** - Get current status
   ```
   "Get ContextBridge current status"
   ```

### Search Documents

Ask your AI agent to search for information:

```
"Search my documents for information about project architecture"
```

The agent will:
1. Query ContextBridge for relevant documents
2. Retrieve matching content
3. Provide you with the results

### Read Specific Files

Request specific document content:

```
"Read the Q4 2024 financial report from my documents"
```

### Analyze Multiple Documents

Combine information from multiple sources:

```
"Compare the requirements from doc1.pdf and doc2.docx"
```

### Manage Watch Directories

Dynamically add or remove monitored directories:

```
"Add ~/Projects to watch directories"
"Remove ~/Downloads from watch directories"
"List all monitored directories"
```

## Configuration

### Supported File Formats

- **Documents**: Word (.docx), Excel (.xlsx), PDF (.pdf)
- **Text**: Markdown (.md), Plain text (.txt)

### Folder Monitoring

Manage monitored folders through Skill capabilities:

```
"Add /path/to/folder to watch directories"
"Remove /path/to/folder from watch directories"
"List all monitored directories"
```

Or use command line:

```bash
cbridge watch add /path/to/folder
cbridge watch remove /path/to/folder
cbridge watch list
```

### Search Settings

Customize search behavior in the Skill settings:

- **Max Results**: Number of documents to return (default: 5)
- **Similarity Threshold**: Minimum relevance score (default: 0.5)
- **Search Timeout**: Maximum search duration in seconds (default: 30)

### Deployment Mode

The Skill automatically detects and selects the best deployment mode:

**Embedded Mode** (Default)
- Uses built-in ChromaDB
- No external dependencies
- Best for standalone use

**External Mode** (Auto-detected)
- Connects to existing QMD and OpenViking services
- Uses namespace isolation:
  - QMD Collection: `contextbridge_docs`
  - OpenViking Mount: `viking://contextbridge/`
- Supports sharing services with other applications

## Troubleshooting

### Skill Not Connecting

**Problem**: OpenClaw can't connect to Local ContextBridge Skill

**Solution**:
1. Check if Skill is properly installed
2. Review Skill installation logs
3. Re-enable the Skill

### Documents Not Indexed

**Problem**: Your documents don't appear in search results

**Solution**:
1. Use `get_watch_directories` capability to verify folders are monitored
2. Check file formats are supported
3. Rebuild index using command line: `cbridge index --force`

### Slow Search Performance

**Problem**: Search queries are taking too long

**Solution**:
1. Reduce the number of monitored folders
2. Exclude large binary files
3. Increase the search timeout in Skill settings

### Memory Usage

**Problem**: ContextBridge is using too much memory

**Solution**:
1. Reduce the number of indexed documents
2. Clear old indexes: `cbridge clean`
3. Monitor folder size and archive old documents

### Need to Reconfigure

**Problem**: Need to change deployment mode or reinitialize

**Solution**:
Use `setup_environment` capability to reconfigure:
```
"Reinitialize ContextBridge environment"
```

## Advanced Configuration

### Custom Embedding Model

To use a different embedding model:

```bash
cbridge config set embedding_model "model-name"
```

Available models:
- `default` - Built-in model (recommended)
- `openai` - OpenAI embeddings (requires API key)
- `local` - Local model (requires additional setup)

### Batch Indexing

For large document collections:

```bash
cbridge index --batch-size 100 --workers 4
```

### Export and Backup

Backup your indexes:

```bash
cbridge export /path/to/backup
```

Restore from backup:

```bash
cbridge import /path/to/backup
```

## Performance Tips

1. **Organize Documents** - Use clear folder structures for better organization
2. **Regular Cleanup** - Archive old documents to keep indexes lean
3. **Batch Operations** - Index large collections during off-peak hours
4. **Monitor Resources** - Check memory and disk usage regularly

## FAQ

**Q: Can I use ContextBridge with multiple OpenClaw instances?**

A: Yes, you can run multiple ContextBridge instances on different ports and connect each OpenClaw instance to its own server.

**Q: Are my documents encrypted?**

A: Documents are stored locally on your machine. ContextBridge doesn't upload or transmit them. Encryption depends on your system's file system settings.

**Q: Can I update documents while ContextBridge is running?**

A: Yes, ContextBridge monitors folders in real-time and automatically indexes new or modified files.

**Q: What's the maximum number of documents I can index?**

A: There's no hard limit, but performance depends on your system resources. Most systems handle 10,000+ documents efficiently.

**Q: Can I use ContextBridge offline?**

A: Yes, ContextBridge works entirely offline. All processing happens locally on your machine.

## Getting Help

- **Documentation**: Check the [User Guide](./usage_en.md)
- **Issues**: Report bugs on [GitHub](https://github.com/whyischen/ContextBridge/issues)
- **Community**: Join our community discussions

## Next Steps

- Explore [advanced features](./usage_en.md#advanced-features)
- Learn about [best practices](./usage_en.md#best-practices)
- Check out [example workflows](./usage_en.md#example-workflows)
