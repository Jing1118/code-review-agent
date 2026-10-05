import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

# 加载环境变量
load_dotenv()

# 初始化大模型（DeepSeek 兼容 OpenAI 接口）
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0,
    max_retries=2,  # 错误重试机制
)

# 工具1：读取文件
@tool
def read_file(file_path: str) -> str:
    """根据文件路径读取并返回文件内容。当需要审查用户指定的代码文件时使用此工具。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"错误：找不到文件 '{file_path}'"
    except Exception as e:
        return f"读取文件时出错：{str(e)}"

# 工具2：保存审查报告
@tool
def save_review(content: str, output_path: str = "review_report.md") -> str:
    """将审查报告内容保存到指定文件中。在完成代码审查后，使用此工具将结果保存下来。"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"审查报告已成功保存到 '{output_path}'"
    except Exception as e:
        return f"保存报告时出错：{str(e)}"

tools = [read_file, save_review]

# 系统提示词：定义 Agent 的角色和输出格式
system_prompt = """
你是一个资深的 Python 代码审查专家。你的任务是仔细审查用户提供的代码，并给出专业、具体、可操作的反馈。

请遵循以下规则进行审查：
1. **Bug 与逻辑错误**：指出代码中潜在的错误、边界条件处理不当、异常处理缺失等问题。
2. **代码风格与规范**：检查是否符合 PEP 8 规范（如命名、缩进、行长度），以及是否有更 Pythonic 的写法。
3. **性能与安全**：指出可能的性能瓶颈（如低效循环）或安全隐患（如硬编码敏感信息）。
4. **改进建议**：对于每个发现的问题，提供具体的修改建议和示例代码。

**输出格式要求**：
请以 Markdown 格式输出你的审查结果，对于每个问题，请明确标出：
- **行号**：指出问题所在的行号（如果适用）。
- **严重程度**：High / Medium / Low。
- **问题描述**：清晰说明问题是什么。
- **修改建议**：提供改进后的代码片段或具体修改方案。

如果代码没有问题，也请明确说明“代码审查通过，未发现明显问题”。

完成审查后，请调用 save_review 工具将报告保存到 review_report.md 文件中。
"""

# 创建提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 创建 Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    print("🤖 欢迎使用代码审查助手！")
    print("你可以输入指令，例如：审查 ./test_code.py 这个文件")
    print("输入 'quit' 退出程序。\n")

    chat_history = []

    while True:
        user_input = input("你：")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("再见！")
            break

        try:
            response = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            print(f"\n助手：{response['output']}\n")
            chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=response['output'])
            ])
        except Exception as e:
            print(f"\n抱歉，处理时出现错误：{e}\n")

if __name__ == "__main__":
    main()