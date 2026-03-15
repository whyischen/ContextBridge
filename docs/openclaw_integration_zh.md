# OpenClaw 集成指南

ContextBridge 可以无缝集成到 OpenClaw 中作为 Skill，让你的 AI 智能体直接访问和理解本地文档。

## 什么是 Local ContextBridge Skill？

Local ContextBridge Skill 是一个强大的 OpenClaw 扩展，提供：

- **实时文档访问** - 即时搜索和检索本地 Word、Excel、PDF 和 Markdown 文件
- **向量搜索** - 跨文档集合的智能语义搜索
- **自动索引** - 自动解析和索引新增或修改的文档
- **零上传** - 所有文档保留在本地，确保隐私和安全
- **智能环境检测** - 自动检测系统环境并选择最佳配置
- **命名空间隔离** - 支持与其他应用共享 QMD 和 OpenViking 服务

## 前置要求

在 OpenClaw 中启用 Local ContextBridge Skill 前，请确保你已有：

- 已安装并配置 OpenClaw
- Python 3.8 或更高版本

## 安装和配置

### 在 OpenClaw 中启用 Skill

1. 打开 OpenClaw Skill 市场
2. 搜索 "local-context-bridge"
3. 点击 "安装"
4. Skill 将自动启动安装引导

### 自动安装引导

Skill 会自动为你完成以下操作：

✅ **环境检测**
- 检测你的系统环境
- 自动选择最佳配置模式

✅ **ContextBridge 安装**
- 自动安装 cbridge-agent（如需要）
- 初始化配置

✅ **模式选择**
- **内嵌模式**（默认）：使用内置 ChromaDB
- **外部模式**（自动检测）：连接到现有 QMD 和 OpenViking 服务

✅ **工作区初始化**
- 创建必要的目录
- 初始化向量数据库

安装完成后，Skill 即可使用。

## 在 OpenClaw 中使用 ContextBridge

安装后，你可以在 OpenClaw 工作流中使用 Local ContextBridge Skill：

### 支持的能力

Skill 提供以下 7 个能力：

1. **search_documents** - 搜索本地文档
   ```
   "在我的文档中搜索关于项目架构的信息"
   ```

2. **setup_environment** - 重新配置环境
   ```
   "重新初始化 ContextBridge 环境"
   ```

3. **detect_environment** - 检测当前环境
   ```
   "检测我的系统环境"
   ```

4. **add_watch_directory** - 添加监控目录
   ```
   "添加 ~/Documents 到监控目录"
   ```

5. **remove_watch_directory** - 移除监控目录
   ```
   "从监控目录中移除 ~/Downloads"
   ```

6. **get_watch_directories** - 获取监控目录列表
   ```
   "列出所有监控的目录"
   ```

7. **get_status** - 获取当前状态
   ```
   "获取 ContextBridge 的当前状态"
   ```

### 搜索文档

要求 AI 智能体搜索信息：

```
"在我的文档中搜索关于项目架构的信息"
```

智能体将：
1. 查询 ContextBridge 获取相关文档
2. 检索匹配的内容
3. 为你提供结果

### 读取特定文件

请求特定文档内容：

```
"从我的文档中读取 2024 年第四季度财务报告"
```

### 分析多个文档

合并来自多个来源的信息：

```
"比较 doc1.pdf 和 doc2.docx 中的需求"
```

### 管理监控目录

动态添加或移除监控目录：

```
"添加 ~/Projects 到监控目录"
"从监控目录中移除 ~/Downloads"
"列出所有监控的目录"
```

## 配置

### 支持的文件格式

- **文档**：Word (.docx)、Excel (.xlsx)、PDF (.pdf)
- **文本**：Markdown (.md)、纯文本 (.txt)

### 文件夹监控

通过 Skill 能力管理监控文件夹：

```
"添加 /path/to/folder 到监控目录"
"从监控目录中移除 /path/to/folder"
"列出所有监控的目录"
```

或使用命令行：

```bash
cbridge watch add /path/to/folder
cbridge watch remove /path/to/folder
cbridge watch list
```

### 搜索设置

在 Skill 设置中自定义搜索行为：

- **最大结果数**：返回的文档数量（默认：5）
- **相似度阈值**：最小相关性分数（默认：0.5）
- **搜索超时**：最大搜索时长（秒）（默认：30）

### 部署模式

Skill 自动检测并选择最佳部署模式：

**内嵌模式**（默认）
- 使用内置 ChromaDB
- 无需外部依赖
- 适合独立使用

**外部模式**（自动检测）
- 连接到现有 QMD 和 OpenViking 服务
- 使用命名空间隔离：
  - QMD Collection: `contextbridge_docs`
  - OpenViking Mount: `viking://contextbridge/`
- 支持与其他应用共享服务

## 故障排查

### Skill 无法连接

**问题**：OpenClaw 无法连接到 Local ContextBridge Skill

**解决方案**：
1. 检查 Skill 是否已正确安装
2. 查看 Skill 的安装日志
3. 重新启用 Skill

### 文档未被索引

**问题**：你的文档未出现在搜索结果中

**解决方案**：
1. 使用 `get_watch_directories` 能力验证文件夹是否被监控
2. 检查文件格式是否支持
3. 使用命令行重建索引：`cbridge index --force`

### 搜索性能缓慢

**问题**：搜索查询耗时过长

**解决方案**：
1. 减少监控的文件夹数量
2. 排除大型二进制文件
3. 在 Skill 设置中增加搜索超时时间

### 内存占用过高

**问题**：ContextBridge 占用内存过多

**解决方案**：
1. 减少索引的文档数量
2. 清理旧索引：`cbridge clean`
3. 监控文件夹大小并归档旧文档

### 需要重新配置

**问题**：需要改变部署模式或重新初始化

**解决方案**：
使用 `setup_environment` 能力重新配置：
```
"重新初始化 ContextBridge 环境"
```

## 高级配置

### 自定义嵌入模型

使用不同的嵌入模型：

```bash
cbridge config set embedding_model "model-name"
```

可用模型：
- `default` - 内置模型（推荐）
- `openai` - OpenAI 嵌入（需要 API 密钥）
- `local` - 本地模型（需要额外设置）

### 批量索引

对于大型文档集合：

```bash
cbridge index --batch-size 100 --workers 4
```

### 导出和备份

备份你的索引：

```bash
cbridge export /path/to/backup
```

从备份恢复：

```bash
cbridge import /path/to/backup
```

## 性能优化建议

1. **组织文档** - 使用清晰的文件夹结构以便更好地组织
2. **定期清理** - 归档旧文档以保持索引精简
3. **批量操作** - 在非高峰时段索引大型集合
4. **监控资源** - 定期检查内存和磁盘使用情况

## 常见问题

**Q：我可以在多个 OpenClaw 实例中使用 ContextBridge 吗？**

A：可以，你可以在不同端口上运行多个 ContextBridge 实例，并将每个 OpenClaw 实例连接到其自己的服务器。

**Q：我的文档是否被加密？**

A：文档存储在你的本地机器上。ContextBridge 不会上传或传输它们。加密取决于你的系统文件系统设置。

**Q：ContextBridge 运行时我可以更新文档吗？**

A：可以，ContextBridge 实时监控文件夹并自动索引新增或修改的文件。

**Q：我最多可以索引多少个文档？**

A：没有硬性限制，但性能取决于你的系统资源。大多数系统可以高效处理 10,000+ 个文档。

**Q：我可以离线使用 ContextBridge 吗？**

A：可以，ContextBridge 完全离线工作。所有处理都在你的本地机器上进行。

## 获取帮助

- **文档**：查看 [使用指南](./usage_zh.md)
- **问题报告**：在 [GitHub](https://github.com/whyischen/ContextBridge/issues) 上报告 bug
- **社区讨论**：加入我们的社区讨论

## 后续步骤

- 探索 [高级功能](./usage_zh.md#高级功能)
- 了解 [最佳实践](./usage_zh.md#最佳实践)
- 查看 [示例工作流](./usage_zh.md#示例工作流)
