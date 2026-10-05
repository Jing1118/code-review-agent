# 代码审查 Agent

一个基于 LangChain 和 DeepSeek 的智能代码审查助手。它可以读取 Python 代码文件，自动分析代码质量、发现潜在 Bug、给出改进建议，并将审查报告保存为 Markdown 文件。

## 功能特性
- 📂 **自动文件读取**：支持读取本地指定路径的Python代码文件
- 🔍 **多维度审查**：覆盖代码Bug、代码风格、性能优化、安全隐患四个维度
- 📋 **结构化输出**：每条问题包含对应行号、严重程度、问题描述、具体修改建议
- 💬 **上下文记忆**：支持多轮对话，可针对审查结果继续追问
- 🛡️ **错误处理**：内置解析错误重试、文件不存在校验等异常处理机制
- 💾 **报告自动保存**：审查完成后自动生成Markdown格式的审查报告文件

## 环境要求
- Python 3.8 及以上版本
- DeepSeek API Key（兼容OpenAI接口格式的大模型均可替换）

## 安装步骤
1. 克隆或下载本项目到本地。

2. 创建虚拟环境并激活：
    ```bash
    python -m venv .venv
    # Windows系统激活命令:
    .venv\Scripts\activate
    # Mac/Linux系统激活命令:
    source .venv/bin/activate


3. 安装项目依赖（必须安装`langchain-classic`，新版LangChain将经典Agent模式拆分至此包）：
   ```bash
   pip install -U langchain langchain-openai langchain-classic python-dotenv
   ```

4. 配置API密钥：
   复制项目根目录下的 `.env.example` 文件，重命名为 `.env`，在文件中填入你的DeepSeek API Key：
   ```env
   DEEPSEEK_API_KEY=你的API Key
   ```

## 使用方法
1. 确保虚拟环境已激活，在项目根目录下运行启动命令：
   ```bash
   python agent.py
   ```

2. 看到欢迎提示后，输入审查指令即可，例如：
   ```
   审查 test_code.py 这个文件
   ```

3. Agent 会自动执行「读取文件→分析代码→生成报告」的完整 Agent 循环，审查结果会输出在终端，同时自动保存到项目根目录的 `review_report.md` 文件中。

4. 输入 `quit` 即可退出程序。

## 输出示例

审查完成后会生成结构化的 Markdown 报告，核心格式如下：

```
# 代码审查报告 - test_code.py

## 一、整体评价
代码实现了基础功能，但存在多处潜在Bug和规范问题。

## 二、详细问题
### 1. 边界条件缺失
- 行号：第3行
- 严重程度：高
- 问题描述：函数未对输入参数做类型校验，传入非数字会直接崩溃
- 修改建议：增加参数类型判断和异常捕获
```

## 项目结构

```
code-review-agent/
├── agent.py          # 主程序：Agent核心逻辑、工具定义、交互入口
├── test_code.py      # 测试代码：包含常见Bug，用于演示审查功能
├── .env              # API密钥配置文件（不提交到代码仓库）
├── .env.example      # API密钥配置示例文件
├── .gitignore        # Git忽略文件配置
├── README.md         # 项目说明文档
├── Design.md         # 详细设计文档（架构、流程、技术选型说明）
└── review_report.md  # 生成的审查报告（运行程序后自动生成）
```

## 技术栈

- **编程语言**：Python
- **Agent 框架**：LangChain（ReAct Agent 模式）
- **大语言模型**：DeepSeek（兼容 OpenAI 接口规范）
- **内置工具**：文件读取工具（read_file）、报告保存工具（save_review）

## 设计文档

详细的架构设计、Agent 工作流程、工具设计说明请查看 [Design.md](./Design.md)。

## 作者

- 学号：242010408
- 姓名：荆怡嘉