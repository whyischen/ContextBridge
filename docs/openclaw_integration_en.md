# OpenClaw Integration Guide

Integrate your local knowledge base seamlessly with [OpenClaw](https://openclaw.com/) (or related AI platforms) using the `local-context-bridge` Skill natively provided by ContextBridge.
With just a simple `SKILL.md` file, you can empower OpenClaw agents to instantly read, retrieve, and understand your local documents.

---

## 📦 Installing the Skill

ContextBridge's native skill is published on [clawhub.ai](https://clawhub.ai/). We provide two installation methods:

### ✨ Method 1: Conversational Installation (Easiest)

If you already have OpenClaw running, you can simply ask the AI to complete the installation using natural language:

> **💬 Example Conversation:**
> _"Install the local-context-bridge skill for me"_

OpenClaw will automatically parse your intent and guide you through the installation process.

### 💻 Method 2: Command Line Installation (Recommended for Developers)

🛠 Prerequisites

Before you begin integration, ensure that:

1. **ContextBridge is running locally** (refer to [Getting Started](#) to launch your local service).
2. [Node.js](https://nodejs.org/) is installed on your machine (required for npm commands).

Use the ClawHub CLI tool for global installation:

```bash
# 1. Install ClawHub CLI globally
npm install -g clawhub@latest

# 2. Install the local-context-bridge skill
clawhub install local-context-bridge
```

---

## 🚀 Getting Started

Configuration complete! Your OpenClaw now has the ability to "see" your local files. You can ask the AI anytime:

- 🔍 _"Using local-context-bridge, search my local documents for API authentication configuration details."_
- 📖 _"Read my local `README.md` and summarize the quick start steps for the project."_
- 💡 _"Based on the error code documentation in my local repository, what causes `Error 5003`?"_

---

## ❓ Frequently Asked Questions (FAQ)

**Q: OpenClaw says it cannot connect to the local service. What should I do?**

A: Please verify that your ContextBridge service is running properly in the background, and confirm that the port number in `SKILL.md` is correct.
