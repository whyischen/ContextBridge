# Search Configuration Guide

## Overview

ContextBridge now supports centralized search configuration, allowing you to set default similarity thresholds and result counts across all search interfaces (CLI and MCP).

## Configuration Location

Search settings are stored in `~/.cbridge/config.yaml` under the `search` section:

```yaml
search:
  min_similarity: 0.5      # Minimum similarity threshold (0.0-1.0)
  default_top_k: 5         # Default number of results to return
```

## Understanding Similarity Scores

After the recent fix, similarity scores now correctly represent relevance:

- **0.7-1.0**: Highly relevant (strong match)
- **0.5-0.7**: Moderately relevant (good match)
- **0.3-0.5**: Weakly relevant (loose match)
- **< 0.3**: Not relevant (filtered out by default)

## Managing Configuration

### View Current Settings

```bash
cbridge search-config show
```

Output:
```
Current Search Configuration:
  Min Similarity Threshold: 0.5 (0.0-1.0)
  Default Top K Results: 5
```

### Update Settings

Update minimum similarity threshold:
```bash
cbridge search-config set --min-similarity 0.6
```

Update default number of results:
```bash
cbridge search-config set --default-top-k 10
```

Update both at once:
```bash
cbridge search-config set --min-similarity 0.5 --default-top-k 5
```

## Using in Different Interfaces

### CLI Search

Use default settings from config:
```bash
cbridge search "your query"
```

Override threshold for a specific search:
```bash
cbridge search "your query" --threshold 0.7
```

Override number of results:
```bash
cbridge search "your query" --top-k 10
```

### MCP Server

The MCP server automatically uses the configured defaults. No additional configuration needed.

## Recommended Settings

### For High Precision (fewer but more relevant results)
```bash
cbridge search-config set --min-similarity 0.7 --default-top-k 3
```

### For Balanced Results (default)
```bash
cbridge search-config set --min-similarity 0.5 --default-top-k 5
```

### For High Recall (more results, some may be less relevant)
```bash
cbridge search-config set --min-similarity 0.3 --default-top-k 10
```

## Troubleshooting

### Getting too many irrelevant results?
Increase the similarity threshold:
```bash
cbridge search-config set --min-similarity 0.6
```

### Not getting enough results?
Lower the similarity threshold:
```bash
cbridge search-config set --min-similarity 0.4
```

### Want to see more options?
Increase the default top-k:
```bash
cbridge search-config set --default-top-k 10
```

## Technical Details

The similarity score is calculated using the formula:
```
similarity = 1 / (1 + distance)
```

Where `distance` is the L2 distance from ChromaDB's vector search. This ensures:
- Distance 0 (perfect match) → Similarity 1.0
- Distance ∞ (no match) → Similarity 0.0
