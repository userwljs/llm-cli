from pydantic_ai import Agent
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown


async def run_stream(msg: str, agent: Agent, markdown: bool = True, prefix=""):
    """
    Run a streaming message through an agent and display it using either Markdown or plaintext formatting.

    通过代理运行一个流式消息，并使用 Markdown 或纯文本格式进行显示。

    :param msg: The user prompt. 用户消息。
    :type msg: str
    :param agent: The agent to process the message. 处理消息的代理。
    :type agent: Agent
    :param markdown: Whether to format the output as Markdown. 是否使用 Markdown 格式化输出。
    :type markdown: bool
    :param prefix: A prefix to add to each assistant output. 添加到每个助手输出的前缀。
    :type prefix: str
    """
    if markdown:
        await run_stream_markdown(msg, agent, prefix=prefix)
    else:
        await run_stream_plaintext(msg, agent, prefix=prefix)


async def run_stream_markdown(msg: str, agent: Agent, prefix=""):
    console = Console()
    with Live("", console=console) as live:
        async with agent.run_stream(msg) as result:
            async for msg in result.stream():
                live.update(Markdown(prefix + "\n" + msg))
                # Add "\n" to prevent the heading from not being rendered if the first line is a Markdown heading and prefix is set.
                # 添加 "\n" 来防止：当第一行是 Markdown 标题且有前缀时，标题不渲染。


async def run_stream_plaintext(msg: str, agent: Agent, prefix=""):
    console = Console()
    with Live("", console=console) as live:
        async with agent.run_stream(msg) as result:
            async for msg in result.stream():
                live.update(prefix + msg)
