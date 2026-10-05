# 代码审查 Agent 设计文档

## 1. 系统架构
本 Agent 采用经典的 ReAct（推理+行动）循环模式，整体流程如下：
用户输入 → LLM 推理 → 决定调用工具 → 执行工具 → 返回结果给 LLM → 生成最终输出 → 保存报告

具体组件：
- LLM：DeepSeek-Chat，temperature=0 保证输出稳定。
- Prompt：系统提示词定义了审查专家的角色和结构化输出要求。
- 工具：
  - read_file：读取用户指定的代码文件。
  - save_review：将审查报告保存到 Markdown 文件。
- 记忆：通过 chat_history 列表保存对话历史，实现多轮上下文记忆。
- 错误处理：工具内部使用 try-except 捕获异常；LLM 调用设置 max_retries=2 自动重试。

## 2. 核心组件说明
### 2.1 LLM 调用
使用 langchain_openai.ChatOpenAI，指向 DeepSeek 的 API 地址。

### 2.2 Prompt 设计
系统提示词明确了 Agent 的角色、审查维度、输出格式，并要求最后调用 save_review 工具。

### 2.3 工具集成
- read_file：接收文件路径，返回文件内容。包含 FileNotFoundError 处理。
- save_review：接收报告内容和输出路径，写入文件。包含通用异常处理。

### 2.4 上下文记忆
在 main() 函数中维护 chat_history 列表，每次对话后将用户输入和 Agent 回复追加进去。

### 2.5 错误处理与重试
- 工具函数内部捕获异常并返回友好错误信息。
- LLM 调用通过 max_retries=2 实现自动重试。
- 主循环用 try-except 包裹，防止程序崩溃。

## 3. 工作流程
1. 用户输入“审查 test_code.py”。
2. Agent 调用 read_file 读取文件内容。
3. LLM 分析代码，生成结构化审查报告。
4. Agent 调用 save_review 保存报告。
5. 最终回复用户，并保留对话历史。

## 4. 可扩展性
- 可增加更多工具，如 write_file（自动修复）、list_directory（列出文件）。
- 可接入其他 LLM，只需修改 ChatOpenAI 的 base_url 和 model。
- 可扩展为 Web 界面，使用 FastAPI 或 Streamlit。