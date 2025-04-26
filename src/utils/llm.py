import os

from pydantic_ai import Agent
from pydantic_ai.result import StreamedRunResult
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from .config import Config


async def run_stream(
    msg: str, agent: Agent, markdown: bool = True, prefix="", *args, **kwargs
) -> StreamedRunResult:
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
        return await run_stream_markdown(msg, agent, prefix=prefix, *args, **kwargs)
    else:
        return await run_stream_plaintext(msg, agent, prefix=prefix, *args, **kwargs)


async def run_stream_markdown(
    msg: str, agent: Agent, prefix="", *args, **kwargs
) -> StreamedRunResult:
    console = Console()
    with Live("", console=console) as live:
        async with agent.run_stream(msg, *args, **kwargs) as result:
            async for msg in result.stream():
                live.update(Markdown(prefix + "\n" + msg))
                # Add "\n" to prevent the heading from not being rendered if the first line is a Markdown heading and prefix is set.
                # 添加 "\n" 来防止：当第一行是 Markdown 标题且有前缀时，标题不渲染。
    return result


async def run_stream_plaintext(
    msg: str, agent: Agent, prefix="", *args, **kwargs
) -> StreamedRunResult:
    console = Console()
    with Live("", console=console) as live:
        async with agent.run_stream(msg, *args, **kwargs) as result:
            async for msg in result.stream():
                live.update(prefix + msg)
    return result


def create_agent(model_name: str, config: Config):
    # Get config. 获取配置。
    conf_model = config.models[model_name]
    conf_provider = config.providers[conf_model.provider]
    assert conf_provider.api_key_type in ["key", "env"]
    if conf_provider.api_key_type == "key":
        api_key = conf_provider.api_key
    elif conf_provider.api_key_type == "env":
        api_key = os.getenv(conf_provider.api_key)

    # Create Agent. 创建智能体。
    assert conf_provider.type in ["openai"]
    if conf_provider.type == "openai":
        from pydantic_ai import Agent
        from pydantic_ai.models.openai import OpenAIModel
        from pydantic_ai.providers.openai import OpenAIProvider

        provider = OpenAIProvider(base_url=conf_provider.base_url, api_key=api_key)
        model = OpenAIModel(model_name=conf_model.model_name, provider=provider)
        agent = Agent(model=model)
    return agent
