import React from 'react';
import { Plug, Sparkles, FolderSync, Shield, Zap, BookOpen, FileText, Cog } from 'lucide-react';

export const APP_CONTENT = {
  en: {
    title: "ContextBridge",
    badgeText: "Open Source · MIT License",
    heroTitle: "Give AI Agents",
    heroHighlight: "",
    heroSuffix: <>Effortless Access<br />to Your Local Documents</>,
    subtitle: "Local knowledge base for OpenClaw, Cursor and AI assistants. Read your documents instantly—Word, Excel, PDF. No uploads. Privacy first.",
    docsSection: "Documentation",
    docCards: [
      {
        icon: BookOpen,
        title: "User Guide",
        desc: "Complete setup and usage instructions for ContextBridge"
      },
      {
        icon: Zap,
        title: "OpenClaw Integration",
        desc: "Install and use ContextBridge as an OpenClaw Skill"
      }
    ],
    openclawCta: {
      badge: "OpenClaw Integration",
      title: "Use with OpenClaw in Seconds",
      desc: "ContextBridge is available as an OpenClaw Skill. Install it once and let your AI agent search your local documents instantly.",
      steps: [
        { label: "Install", cmd: "pip install cbridge-agent" },
        { label: "Init", cmd: "cbridge init && cbridge start" },
      ],
      cta: "View Integration Guide",
    },
    features: [
      {
        icon: Shield,
        title: "100% Local Privacy",
        desc: "100% local operation. All data stored on your hard drive. No cloud APIs, complete data sovereignty."
      },
      {
        icon: Zap,
        title: "Intelligent Text Chunking",
        desc: <>Three-tier progressive retrieval:<br /><span className="text-xs opacity-70 leading-tight block my-1">L0: Abstract · L1: Outline · L2: Semantic Chunks</span>Quickly locates documents with precise context.</>
      },
      {
        icon: Sparkles,
        title: "Hybrid Search Optimization",
        desc: "Combines semantic search, BM25, keyword matching, and more. Intelligently weighted ranking delivers more precise retrieval results."
      },
      {
        icon: FolderSync,
        title: "Smart Folder Watcher",
        desc: <>Effortlessly track project directories with <code className="text-indigo-300">cbridge watch</code>. Add or remove context sources instantly without restarts.</>
      },
      {
        icon: Plug,
        title: "Native MCP Protocol",
        desc: "Built-in Model Context Protocol support. One-click integration with Claude Desktop, Cursor, OpenClaw, and other mainstream AI tools."
      },
      {
        icon: FileText,
        title: "Multi-Format Support",
        desc: "Supports Word, Excel, PDF, and Markdown. Automatically parses documents into high-fidelity context for AI agents."
      }
    ],
    quickStart: "Quick Start",
    steps: [
      { comment: "# 1. Install ContextBridge globally", cmd: "pip install cbridge-agent" },
      { comment: "# 2. Interactive Initialization", cmd: "cbridge init" },
      { comment: "# 3. Add folders to monitor", cmd: "cbridge watch add ~/Documents/MyProjects" },
      { comment: "# 4. Build initial index with progress bar", cmd: "cbridge index" },
      { comment: "# 5. Start the real-time watcher & MCP Server", cmd: "cbridge start" },
      { comment: "# 6. Test with the demo document", cmd: 'cbridge search "ContextBridge"' }
    ]
  },
  zh: {
    title: "ContextBridge",
    badgeText: "开源 · MIT 协议",
    heroTitle: "让 AI 智能体",
    heroHighlight: "",
    heroSuffix: <>轻松读懂<br />你的本地文档</>,
    subtitle: "专为 Openclaw、Cursor 等智能体设计的知识库插件。让你的 AI 助手轻松读取、理解本地的 Word、Excel 和 PDF 文件，无需上传，隐私安全。",
    docsSection: "文档中心",
    docCards: [
      {
        icon: BookOpen,
        title: "使用指南",
        desc: "ContextBridge 的完整设置和使用说明"
      },
      {
        icon: Zap,
        title: "OpenClaw 集成",
        desc: "将 ContextBridge 作为 OpenClaw Skill 安装和使用"
      }
    ],
    openclawCta: {
      badge: "OpenClaw 集成",
      title: "秒级接入 OpenClaw",
      desc: "ContextBridge 已作为 OpenClaw Skill 发布。一次安装，即可让你的 AI 智能体即时检索本地文档。",
      steps: [
        { label: "安装", cmd: "pip install cbridge-agent" },
        { label: "启动", cmd: "cbridge init && cbridge start" },
      ],
      cta: "查看集成指南",
    },
    features: [
      {
        icon: Shield,
        title: "隐私保护",
        desc: "100% 本地运行，所有数据存储在本地硬盘。无需云端 API，完全掌控数据主权。"
      },
      {
        icon: Zap,
        title: "智能文本分块",
        desc: <>三层递进式检索：<br /><span className="text-xs opacity-70 leading-tight block my-1">L0: 文档摘要 · L1: 结构大纲 · L2: 语义分块</span>快速定位文档并获取精准上下文。</>
      },
      {
        icon: Sparkles,
        title: "混合搜索优化",
        desc: "结合语义搜索、BM25、关键词匹配等多种算法。智能加权排序，提供更精准的检索结果。"
      },
      {
        icon: FolderSync,
        title: "智能目录监控",
        desc: <>使用 <code className="text-indigo-300">cbridge watch</code> 命令轻松追踪项目目录。无需重启，即可实时动态增减上下文来源。</>
      },
      {
        icon: Plug,
        title: "原生 MCP 协议",
        desc: "内置 Model Context Protocol 支持。一键接入 Claude Desktop、Cursor、OpenClaw 等主流 AI 工具。"
      },
      {
        icon: FileText,
        title: "多格式支持",
        desc: "支持 Word、Excel、PDF 及 Markdown。自动解析文档为高保真上下文，供 AI 智能体使用。"
      }
    ],
    quickStart: "快速开始",
    steps: [
      { comment: "# 1. 全局安装 ContextBridge", cmd: "pip install cbridge-agent" },
      { comment: "# 2. 交互式初始化", cmd: "cbridge init" },
      { comment: "# 3. 添加监控目录", cmd: "cbridge watch add ~/Documents/MyProjects" },
      { comment: "# 4. 构建初始索引（带进度条）", cmd: "cbridge index" },
      { comment: "# 5. 启动实时监控与 MCP 服务", cmd: "cbridge start" },
      { comment: "# 6. 使用内置 Demo 文档进行测试", cmd: 'cbridge search "ContextBridge"' }
    ]
  }
};
