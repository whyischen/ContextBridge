# ContextBridge (cbridge-agent)

## 项目介绍

ContextBridge 是一个本地 AI 代理的全能内存桥接工具。它能够将真实世界的文档（PDF、Office 文件、Markdown）即时提供给本地 AI 代理（如 OpenClaw、Claude Desktop、Cursor）。

**核心特性：**
- 🔋 **开箱即用**：内置嵌入式 ChromaDB 向量数据库，无需手动安装或配置
- 👁️ **零接触同步**：使用 Watchdog 监控文件夹变化，自动解析并重建向量索引
- 🧹 **幽灵数据清理**：自动检测并清理离线期间删除的文件
- 📄 **多格式解析**：支持 PDF（Docling）、Word、Excel、PPTX 等格式
- 🔌 **MCP 和 API 就绪**：原生支持 Model Context Protocol，无缝集成 Claude Desktop、Cursor 和 OpenClaw
- 🌐 **国际化支持**：完全支持英文和中文界面
- 🔒 **100% 本地隐私**：所有数据存储在本地硬盘，不依赖云 LLM API

## 项目结构

```
context-bridge/
├── core/                         # 核心模块
│   ├── api_server.py             # FastAPI 服务器
│   ├── config.py                 # 配置管理
│   ├── factories.py              # 工厂类初始化
│   ├── i18n.py                   # 国际化支持
│   ├── mcp_server.py             # MCP 服务器实现
│   ├── parser.py                 # 文档解析器
│   ├── repo_manager.py           # 仓库管理
│   ├── watcher.py                # 文件监控和索引
│   ├── interfaces/               # 接口定义
│   │   ├── context_manager.py    # 上下文管理接口
│   │   ├── parser.py             # 解析器接口
│   │   └── search_runtime.py     # 搜索运行时接口
│   ├── managers/                 # 管理器实现
│   │   └── openviking_manager.py # OpenViking 管理器
│   ├── parsers/                  # 解析器实现
│   │   ├── composite_parser.py   # 组合解析器
│   │   ├── docling_parser.py     # Docling 解析器
│   │   └── markitdown_parser.py  # MarkItDown 解析器
│   ├── runtimes/                 # 运行时实现
│   │   └── qmd_runtime.py        # QMD 运行时
│   └── utils/                    # 工具函数
│       ├── logger.py             # 日志工具
│       └── model_downloader.py   # 模型下载工具
├── cbridge.py                    # CLI 入口点
├── src                           # 前端页面
├── main.py                       # 主程序入口
├── setup.py                      # 包配置
└── requirements.txt              # 依赖列表
```

## 编码规范

1. **跨平台兼容性**：考虑 Mac/Linux/Windows 多端操作
   - 使用 `pathlib.Path` 处理路径，避免硬编码路径分隔符
   - 使用 `os.path.join()` 或 `Path` 对象进行路径操作
   - 在 Windows 上使用 `subprocess.Popen` 的 `creationflags` 参数处理后台进程

2. **异步编程**：
   - 使用 `asyncio` 处理异步操作
   - 使用 `threading` 处理后台任务（如文件监控）
   - 确保线程安全的数据访问

3. **配置管理**：
   - 使用 YAML 格式存储配置
   - 支持环境变量覆盖
   - 提供合理的默认值

4. **国际化**：
   - 使用 `core.i18n.t()` 函数进行文本翻译
   - 支持中文（zh）和英文（en）

5. **日志记录**：
   - 使用 `core.utils.logger.setup_logger()` 创建日志记录器
   - 记录关键操作和错误信息

6. **错误处理**：
   - 捕获特定异常而不是通用异常
   - 提供有意义的错误消息
   - 优雅地处理资源清理

7. **官网设计**
   - 中英文官网设计，要同步适配
   - 使用克制的 Vercel 极简风