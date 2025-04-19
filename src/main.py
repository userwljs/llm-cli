import os
import sys
import tomllib
from typing import Annotated

import platformdirs
import typer
from pydantic import ValidationError

from config import Config

dirs = platformdirs.PlatformDirs(appname="llm-cli", appauthor=False)
config_path = os.path.join(dirs.user_config_dir, "config.toml")

if not os.path.exists(config_path):
    print("No config file {fp}".format(fp=config_path))
    sys.exit(1)

if not os.access(config_path, os.R_OK):
    print("Cannot read config file {fp}".format(fp=config_path))
    sys.exit(1)

with open(config_path, "rb") as f:
    try:
        config = Config(**tomllib.load(f))
    except ValidationError as e:
        print("Invalid config file {fp}.\nError: {e}".format(fp=config_path, e=e))
        sys.exit(1)


app = typer.Typer()


@app.command()
def chat(
    msg: Annotated[str, typer.Argument()] = None,
    model_name: Annotated[
        str, typer.Argument(show_choices=config.models.keys())
    ] = config.default.model,
):
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
