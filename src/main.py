import asyncio
import sys
from typing import Annotated

import prompt_toolkit
import typer

from utils.cli import AutoName
from utils.config import load_config

config = load_config()

app = typer.Typer()
model_name_enum = AutoName("model_name", list(config.models.keys()))


@app.command()
def chat(
    msg: Annotated[str, typer.Argument()] = "",
    model_name: Annotated[
        model_name_enum, typer.Option("--model", "-m")
    ] = config.default.model,
    markdown_output: Annotated[
        bool, typer.Option(is_flag=True)
    ] = config.default.markdown_output,
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
    from utils.llm import create_agent, run_stream

    agent = create_agent(model_name, config)
    asyncio.run(run_stream(msg, agent, markdown=markdown_output, prefix="Assistant: "))


if __name__ == "__main__":
    app()
