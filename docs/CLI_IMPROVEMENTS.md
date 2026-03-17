# ContextBridge CLI Improvements Changelog

## Search Command Enhancements

### Overview
Enhanced the `cbridge search` command with intelligent search capabilities including configurable result limits, similarity thresholds, and automatic keyword-based reranking.

### Features

#### 1. Top-K Results (`--top-k`)
- **Default**: 5 results
- **Usage**: `cbridge search "embedding model" --top-k 10`
- **Description**: Controls the number of search results returned. Higher values provide more comprehensive results but may include less relevant matches.

#### 2. Similarity Threshold (`--threshold`)
- **Default**: 0.5 (balanced filtering)
- **Range**: 0.0 - 1.0
- **Usage**: `cbridge search "embedding model" --threshold 0.7`
- **Description**: Filters out results below the specified similarity score. The default value of 0.5 provides a good balance between relevance and recall for most use cases.
- **Recommendation**: 
  - **0.7-0.9**: Strict matching, only highly relevant results
  - **0.5-0.7**: Balanced mode (default: 0.5, suitable for most scenarios)
  - **0.3-0.5**: Loose matching, exploratory search
  - **0.0-0.3**: Very permissive, may include irrelevant results

**中文说明：相似度阈值设置指南**

余弦相似度取值范围为 0.0 到 1.0（ChromaDB 归一化后）：
- **1.0**：完全相同
- **0.0**：完全不相关

**默认值 0.5** 在相关性和召回率之间取得良好平衡，适合大多数文档检索场景。

**推荐设置：**
- **0.7-0.9**：严格匹配，只返回高度相关的结果（适合精确问答）
- **0.5-0.7**：平衡模式（默认 0.5，适合大多数场景）
- **0.3-0.5**：宽松匹配，返回更多可能相关的结果（适合探索性搜索）
- **0.0-0.3**：最宽松，可能包含大量不相关结果

**实践建议：**
1. 默认值 0.5 适合大多数情况，可以直接使用
2. 如需更严格的结果，提高到 0.6-0.7
3. 如需更多候选结果，降低到 0.3-0.4
4. 完全不过滤可设置为 0.0

示例：
```bash
# 使用默认阈值 0.5（推荐）
cbridge search "embedding model"

# 更严格的匹配
cbridge search "embedding model" --threshold 0.7

# 更宽松的匹配
cbridge search "embedding model" --threshold 0.3

# 不过滤
cbridge search "embedding model" --threshold 0.0
```

#### 3. Keyword-Based Reranking (`--rerank`)
- **Default**: Enabled
- **Usage**: 
  - Enabled (default): `cbridge search "embedding model"`
  - Disabled: `cbridge search "embedding model" --no-rerank`
- **Description**: Automatically reranks results by combining semantic similarity (70%) with keyword matching (30%). This boosts results that contain exact query terms, improving relevance.
- **How it works**:
  1. Retrieves 2x the requested results initially
  2. Extracts keywords from the query
  3. Calculates keyword match scores for each result
  4. Combines semantic score (70%) + keyword match (30%)
  5. Returns top-k results sorted by combined score

### Example Usage

```bash
# Basic search with defaults (top-k=5, threshold=0.5, rerank=enabled)
cbridge search "embedding model"

# Get more results
cbridge search "embedding model" --top-k 10

# Filter for high-quality matches only
cbridge search "embedding model" --threshold 0.7

# More permissive filtering
cbridge search "embedding model" --threshold 0.3

# No filtering at all
cbridge search "embedding model" --threshold 0.0

# Combine all options
cbridge search "embedding model" --top-k 10 --threshold 0.7

# Disable reranking for pure semantic search
cbridge search "embedding model" --no-rerank

# Full example with all parameters
cbridge search "embedding model" --top-k 10 --threshold 0.6 --rerank
```

### Technical Details

#### Reranking Algorithm
The reranking process uses a weighted scoring approach:
- **Semantic Score (70%)**: Original vector similarity from the embedding model
- **Keyword Match (30%)**: Ratio of query keywords found in the result content/URI
- **Formula**: `final_score = semantic_score * 0.7 + keyword_ratio * 0.3`

This hybrid approach ensures that results are both semantically relevant and contain the actual terms users are searching for.

#### Performance Considerations
- When reranking is enabled, the system retrieves `top_k * 2` results initially to ensure sufficient candidates for reranking
- Threshold filtering is applied before reranking to eliminate low-quality matches early
- Results are sorted by the combined score in descending order

### Internationalization
All search-related messages support both English and Chinese:
- `search_desc`: Command description
- `search_empty`: No results found
- `search_filtered`: Threshold filtering message
- `search_reranked`: Reranking confirmation
- `search_empty_after_filter`: No results after filtering
- `search_results_title`: Results header
- `search_result_item_numbered`: Individual result format

### Migration Notes
- **Breaking Change**: `--rerank` is now enabled by default. Users who prefer pure semantic search must explicitly use `--no-rerank`.
- **Breaking Change**: `--threshold` default changed from 0.0 to 0.5. This provides better default filtering but may return fewer results. To restore previous behavior, use `--threshold 0.0`.
- All existing commands will continue to work, but will now benefit from automatic reranking and relevance filtering.
