# 搜索配置指南

## 概述

ContextBridge 现在支持集中式搜索配置，允许你在所有搜索接口（CLI 和 MCP）中设置默认的相似度阈值和结果数量。

## 配置位置

搜索设置存储在 `~/.cbridge/config.yaml` 的 `search` 部分：

```yaml
search:
  min_similarity: 0.5      # 最小相似度阈值 (0.0-1.0)
  default_top_k: 5         # 默认返回结果数量
```

## 理解相似度分数

在最近的修复后，相似度分数现在正确地表示相关性：

- **0.7-1.0**：高度相关（强匹配）
- **0.5-0.7**：中等相关（良好匹配）
- **0.3-0.5**：弱相关（松散匹配）
- **< 0.3**：不相关（默认被过滤）

## 管理配置

### 查看当前设置

```bash
cbridge search-config show
```

输出：
```
Current Search Configuration:
  Min Similarity Threshold: 0.5 (0.0-1.0)
  Default Top K Results: 5
```

### 更新设置

更新最小相似度阈值：
```bash
cbridge search-config set --min-similarity 0.6
```

更新默认结果数量：
```bash
cbridge search-config set --default-top-k 10
```

同时更新两者：
```bash
cbridge search-config set --min-similarity 0.5 --default-top-k 5
```

## 在不同接口中使用

### CLI 搜索

使用配置中的默认设置：
```bash
cbridge search "你的查询"
```

为特定搜索覆盖阈值：
```bash
cbridge search "你的查询" --threshold 0.7
```

覆盖结果数量：
```bash
cbridge search "你的查询" --top-k 10
```

### MCP 服务器

MCP 服务器自动使用配置的默认值，无需额外配置。

## 推荐设置

### 高精度（更少但更相关的结果）
```bash
cbridge search-config set --min-similarity 0.7 --default-top-k 3
```

### 平衡结果（默认）
```bash
cbridge search-config set --min-similarity 0.5 --default-top-k 5
```

### 高召回率（更多结果，部分可能不太相关）
```bash
cbridge search-config set --min-similarity 0.3 --default-top-k 10
```

## 故障排除

### 获得太多不相关的结果？
提高相似度阈值：
```bash
cbridge search-config set --min-similarity 0.6
```

### 获得的结果不够？
降低相似度阈值：
```bash
cbridge search-config set --min-similarity 0.4
```

### 想看到更多选项？
增加默认 top-k：
```bash
cbridge search-config set --default-top-k 10
```

## 技术细节

相似度分数使用以下公式计算：
```
similarity = 1 / (1 + distance)
```

其中 `distance` 是 ChromaDB 向量搜索的 L2 距离。这确保了：
- 距离 0（完美匹配）→ 相似度 1.0
- 距离 ∞（无匹配）→ 相似度 0.0
