# 代码审查 Agent

一个基于 LangChain 和 DeepSeek 的智能代码审查助手。它可以读取 Python 代码文件，自动分析代码质量、发现潜在 Bug、给出改进建议，并将审查报告保存为 Markdown 文件。

## 功能特性
- 自动读取指定代码文件
- 多维度审查：Bug、代码风格、性能、安全
- 结构化输出：包含行号、严重程度、问题描述、修改建议
- 上下文记忆：支持多轮对话
- 错误处理与重试机制
- 审查报告自动保存

## 环境要求
- Python 3.8+
- DeepSeek API Key（或兼容 OpenAI 接口的大模型）

## 安装步骤
1. 克隆或下载本项目。
2. 创建虚拟环境并激活：
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
3. 安装依赖（注意：必须安装 langchain-classic）：
   pip install -U langchain langchain-openai langchain-classic python-dotenv
4. 复制 .env.example 文件为 .env，填入你的 API Key：
   DEEPSEEK_API_KEY=你的API Key

# 使用方法
1. 在项目根目录下，确保虚拟环境已激活，运行：
   python agent.py
2. 看到欢迎提示后，输入指令，例如：
   审查 test_code.py 这个文件
3. Agent 会自动读取文件、分析代码并生成审查报告，同时保存到 review_report.md 中。
4. 输入 quit 退出程序。

# 项目结构
代码审查Agent/
├── agent.py            # 主程序：Agent 逻辑与工具定义
├── test_code.py        # 测试代码：包含常见Bug，用于演示Agent审查功能
├── .env                # API Key 配置（不提交到仓库）
├── .env.example        # API Key 示例文件
├── .gitignore          # Git 忽略文件
├── README.md           # 项目说明
├── Design.md           # 设计文档
└── review_report.md    # 生成的审查报告（运行后产生）
# 技术栈
语言：Python
Agent框架：LangChain
LLM服务商：DeepSeek（兼容 OpenAI 接口）
工具：文件读取（read_file）、报告保存（save_review）
# GitHub 仓库
https://github.com/Jing1118/code-review-agent
# 作者
学号：242010408
姓名：荆怡嘉