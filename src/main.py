import os
import sys
from typing import Annotated

import prompt_toolkit
import typer

from config import load_config
from utils import AutoName

config = load_config()

app = typer.Typer()
model_name_enum = AutoName("model_name", list(config.models.keys()))


@app.command()
def chat(
    msg: Annotated[str, typer.Argument()] = "",
    model_name: Annotated[
        model_name_enum, typer.Option("--model", "-m")
    ] = config.default.model,
):
    if model_name is None:
        print(
            "Model name is required. Use --model/-m to specific a model. Or edit the config to set the default model."
        )
        sys.exit(1)
    if not sys.stdin.isatty():
        msg += sys.stdin.read()
    if msg == "":
        msg = prompt_toolkit.prompt("Enter your message: ") + msg
        if not msg:
            raise typer.Abort()
    model_name = model_name.name
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.providers.openai import OpenAIProvider

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
        provider = OpenAIProvider(base_url=conf_provider.base_url, api_key=api_key)
        model = OpenAIModel(model_name=conf_model.model_name, provider=provider)
        agent = Agent(model=model)

    print(agent.run_sync(msg).data)


if __name__ == "__main__":
    app()
