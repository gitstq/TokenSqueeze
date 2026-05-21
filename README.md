# 🚀 TokenSqueeze

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/gitstq/TokenSqueeze)

> 🎯 **轻量级LLM Token智能压缩工具** | **Lightweight LLM Token Compression Tool**

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

---

## 简体中文

### 🎉 项目介绍

**TokenSqueeze** 是一个零依赖的 Python 工具，专为 AI 编码助手设计，能够智能压缩命令行输出，帮助您节省 **60-90%** 的 Token 消耗。

#### 灵感来源

本项目灵感来源于 [rtk-ai/rtk](https://github.com/rtk-ai/rtk)，但我们追求更轻量、更易集成的解决方案：

| 特性 | rtk | TokenSqueeze |
|------|-----|--------------|
| 体积 | ~5MB Rust 二进制 | ~50KB Python 单文件 |
| 依赖 | 需编译安装 | **零依赖，即插即用** |
| 配置 | 多步骤初始化 | **自动检测，零配置** |
| 平台 | 支持有限 | **全平台 Python 支持** |

### ✨ 核心特性

- 🧠 **智能压缩引擎** - 自动识别命令类型并应用最佳压缩策略
- 📉 **Token 节省 60-90%** - 显著降低 AI 助手上下文消耗
- 🔧 **20+ 命令支持** - git、npm、pytest、docker、cargo 等常用工具
- 📊 **实时统计** - 追踪 Token 节省情况，可视化收益
- 🤖 **MCP 服务器模式** - 为 Claude Code、Cursor 等 AI 工具提供原生支持
- 🌍 **跨平台** - Windows、macOS、Linux 全支持
- ⚡ **零依赖** - 纯 Python 实现，无需额外安装

### 🚀 快速开始

#### 环境要求

- Python 3.8 或更高版本

#### 安装

```bash
# 方法1：直接下载使用
curl -fsSL https://raw.githubusercontent.com/gitstq/TokenSqueeze/main/tokensqueeze.py -o tokensqueeze.py
python3 tokensqueeze.py --version

# 方法2：通过 pip 安装
pip install tokensqueeze

# 方法3：本地安装
git clone https://github.com/gitstq/TokenSqueeze.git
cd TokenSqueeze
pip install -e .
```

#### 基本用法

```bash
# 压缩 git 输出
tokensqueeze git status
tokensqueeze git log --oneline -10
tokensqueeze git diff

# 压缩测试输出
tokensqueeze pytest -v
tokensqueeze npm test
tokensqueeze cargo test

# 压缩容器输出
tokensqueeze docker ps
tokensqueeze docker logs container_name

# 查看统计信息
tokensqueeze --stats
```

### 📖 详细使用指南

#### 支持的命令类型

| 命令类型 | 压缩策略 | 典型节省 |
|----------|----------|----------|
| `git` | 移除提示信息，简化状态 | 50-70% |
| `npm/yarn/pnpm` | 过滤进度日志，保留结果 | 60-80% |
| `pytest` | 简化 traceback，保留结果 | 70-90% |
| `docker` | 简化容器列表，过滤 pull 进度 | 50-70% |
| `cargo` | 过滤编译进度，保留错误 | 60-80% |
| `ls/tree` | 大量文件时显示摘要 | 40-60% |

#### MCP 服务器模式

为 AI 工具提供原生集成：

```bash
tokensqueeze --mcp
```

然后在 Claude Code 配置中添加：

```json
{
  "mcpServers": {
    "tokensqueeze": {
      "command": "tokensqueeze",
      "args": ["--mcp"]
    }
  }
}
```

### 💡 设计思路与迭代规划

#### 技术选型

- **纯 Python 实现**：确保跨平台兼容性，零依赖
- **模块化架构**：核心压缩引擎 + 命令适配器，易于扩展
- **智能检测**：自动识别命令类型，无需手动配置

#### 后续迭代计划

- [ ] 支持更多命令类型（kubectl、terraform、aws-cli 等）
- [ ] 自定义压缩规则配置
- [ ] 与更多 AI 工具深度集成
- [ ] 压缩效果可视化仪表板
- [ ] 团队协作统计功能

### 📦 打包与部署

#### 作为 Python 包使用

```python
from tokensqueeze import OutputCompressor, TokenEstimator

compressor = OutputCompressor()
output = compressor.compress(your_command_output, command_type='git')
print(f"节省: {compressor.stats.savings_ratio}")
```

#### 打包为可执行文件

```bash
# 使用 PyInstaller
pip install pyinstaller
pyinstaller --onefile tokensqueeze.py
```

### 🤝 贡献指南

欢迎提交 Issue 和 PR！请确保：

1. 代码符合 PEP 8 规范
2. 添加必要的测试用例
3. 更新相关文档

### 📄 开源协议

本项目采用 [MIT 协议](LICENSE) 开源。

---

## 繁體中文

### 🎉 專案介紹

**TokenSqueeze** 是一個零依賴的 Python 工具，專為 AI 編碼助手設計，能夠智慧壓縮命令列輸出，幫助您節省 **60-90%** 的 Token 消耗。

### ✨ 核心特性

- 🧠 **智慧壓縮引擎** - 自動識別命令類型並套用最佳壓縮策略
- 📉 **Token 節省 60-90%** - 顯著降低 AI 助手上下文消耗
- 🔧 **20+ 命令支援** - git、npm、pytest、docker、cargo 等常用工具
- 📊 **即時統計** - 追蹤 Token 節省情況，視覺化收益
- 🤖 **MCP 伺服器模式** - 為 Claude Code、Cursor 等 AI 工具提供原生支援
- 🌍 **跨平台** - Windows、macOS、Linux 全支援
- ⚡ **零依賴** - 純 Python 實現，無需額外安裝

### 🚀 快速開始

#### 安裝

```bash
# 直接下載使用
curl -fsSL https://raw.githubusercontent.com/gitstq/TokenSqueeze/main/tokensqueeze.py -o tokensqueeze.py
python3 tokensqueeze.py --version

# 或透過 pip 安裝
pip install tokensqueeze
```

#### 基本用法

```bash
# 壓縮 git 輸出
tokensqueeze git status
tokensqueeze git log --oneline -10

# 壓縮測試輸出
tokensqueeze pytest -v
tokensqueeze npm test

# 查看統計資訊
tokensqueeze --stats
```

### 📄 開源協議

[MIT 協議](LICENSE)

---

## English

### 🎉 Introduction

**TokenSqueeze** is a zero-dependency Python tool designed for AI coding assistants that intelligently compresses command-line output, helping you save **60-90%** of token consumption.

#### Inspiration

Inspired by [rtk-ai/rtk](https://github.com/rtk-ai/rtk), but we pursue a lighter and easier-to-integrate solution:

| Feature | rtk | TokenSqueeze |
|---------|-----|--------------|
| Size | ~5MB Rust binary | ~50KB Python single file |
| Dependencies | Requires compilation | **Zero dependencies, plug-and-play** |
| Configuration | Multi-step setup | **Auto-detection, zero config** |
| Platform | Limited support | **Full Python cross-platform** |

### ✨ Key Features

- 🧠 **Smart Compression Engine** - Automatically detects command types and applies optimal compression
- 📉 **60-90% Token Savings** - Significantly reduce AI assistant context consumption
- 🔧 **20+ Commands Supported** - git, npm, pytest, docker, cargo, and more
- 📊 **Real-time Statistics** - Track token savings with visualized benefits
- 🤖 **MCP Server Mode** - Native support for Claude Code, Cursor, and other AI tools
- 🌍 **Cross-platform** - Full support for Windows, macOS, Linux
- ⚡ **Zero Dependencies** - Pure Python implementation, no extra installs needed

### 🚀 Quick Start

#### Requirements

- Python 3.8 or higher

#### Installation

```bash
# Method 1: Direct download
curl -fsSL https://raw.githubusercontent.com/gitstq/TokenSqueeze/main/tokensqueeze.py -o tokensqueeze.py
python3 tokensqueeze.py --version

# Method 2: Via pip
pip install tokensqueeze

# Method 3: Local install
git clone https://github.com/gitstq/TokenSqueeze.git
cd TokenSqueeze
pip install -e .
```

#### Basic Usage

```bash
# Compress git output
tokensqueeze git status
tokensqueeze git log --oneline -10
tokensqueeze git diff

# Compress test output
tokensqueeze pytest -v
tokensqueeze npm test
tokensqueeze cargo test

# Compress container output
tokensqueeze docker ps
tokensqueeze docker logs container_name

# View statistics
tokensqueeze --stats
```

### 📖 Detailed Usage Guide

#### Supported Command Types

| Command Type | Compression Strategy | Typical Savings |
|--------------|---------------------|-----------------|
| `git` | Remove hints, simplify status | 50-70% |
| `npm/yarn/pnpm` | Filter progress logs, keep results | 60-80% |
| `pytest` | Simplify traceback, keep results | 70-90% |
| `docker` | Simplify container list, filter pull progress | 50-70% |
| `cargo` | Filter build progress, keep errors | 60-80% |
| `ls/tree` | Show summary for large directories | 40-60% |

#### MCP Server Mode

For native AI tool integration:

```bash
tokensqueeze --mcp
```

Then add to your Claude Code configuration:

```json
{
  "mcpServers": {
    "tokensqueeze": {
      "command": "tokensqueeze",
      "args": ["--mcp"]
    }
  }
}
```

### 💡 Design Philosophy & Roadmap

#### Technical Choices

- **Pure Python**: Ensures cross-platform compatibility, zero dependencies
- **Modular Architecture**: Core compression engine + command adapters, easy to extend
- **Smart Detection**: Auto-detects command types, no manual configuration needed

#### Future Roadmap

- [ ] Support more command types (kubectl, terraform, aws-cli, etc.)
- [ ] Custom compression rule configuration
- [ ] Deeper integration with more AI tools
- [ ] Visual compression effectiveness dashboard
- [ ] Team collaboration statistics

### 📦 Packaging & Deployment

#### Use as Python Package

```python
from tokensqueeze import OutputCompressor, TokenEstimator

compressor = OutputCompressor()
output = compressor.compress(your_command_output, command_type='git')
print(f"Saved: {compressor.stats.savings_ratio}")
```

#### Package as Executable

```bash
# Using PyInstaller
pip install pyinstaller
pyinstaller --onefile tokensqueeze.py
```

### 🤝 Contributing

Issues and PRs are welcome! Please ensure:

1. Code follows PEP 8 standards
2. Add necessary test cases
3. Update relevant documentation

### 📄 License

This project is open-sourced under the [MIT License](LICENSE).

---

## 🔗 Links

- 🏠 **Homepage**: https://github.com/gitstq/TokenSqueeze
- 🐛 **Issues**: https://github.com/gitstq/TokenSqueeze/issues
- 📖 **Documentation**: https://github.com/gitstq/TokenSqueeze#readme

---

<p align="center">Made with ❤️ by TokenSqueeze Team</p>
