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
    multi_turn: Annotated[bool, typer.Option(is_flag=True)] = config.default.multi_turn,
):
    from utils.llm import create_agent, run_stream

    if model_name is None:
        print(
            "Model name is required. Use --model/-m to specific a model. Or edit the config to set the default model."
        )
        sys.exit(1)
    model_name = model_name.name
    agent = create_agent(model_name, config)
    if not sys.stdin.isatty():
        msg += sys.stdin.read()
    if multi_turn:
        chat_multi_turn(agent, first_msg=msg, markdown_output=markdown_output)
        return
    if msg == "":
        msg = prompt_toolkit.prompt("Enter your message: ") + msg
        if not msg:
            raise typer.Abort()

    asyncio.run(run_stream(msg, agent, markdown=markdown_output, prefix="Assistant: "))


def chat_multi_turn(
    agent,
    first_msg: str = "",
    markdown_output: bool = config.default.markdown_output,
    prefix: str = "Assistant: ",
):
    from utils.llm import run_stream

    messages = []  # The message history. 消息记录。
    if first_msg:
        result = asyncio.run(
            run_stream(first_msg, agent, markdown=markdown_output, prefix=prefix)
        )
        messages.extend(result.new_messages())
    prompt_session = prompt_toolkit.PromptSession()
    try:
        while True:
            msg = prompt_session.prompt("User: ")
            if not msg:
                raise typer.Abort()
            result = asyncio.run(
                run_stream(
                    msg,
                    agent,
                    markdown=markdown_output,
                    prefix=prefix,
                    message_history=messages,
                )
            )
            messages.extend(result.new_messages())
    except KeyboardInterrupt:
        raise typer.Abort()


if __name__ == "__main__":
    app()
