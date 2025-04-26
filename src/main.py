# This file is part of the LLM CLI.
# The LLM CLI is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# The LLM CLI is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with the LLM CLI. If not, see <https://www.gnu.org/licenses/>.
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
        msg = prompt_toolkit.prompt(config.default.user_prompt_prefix) + msg
        if not msg:
            raise typer.Abort()

    asyncio.run(
        run_stream(
            msg,
            agent,
            markdown=markdown_output,
            prefix=config.default.assistant_output_prefix,
        )
    )


def chat_multi_turn(
    agent,
    first_msg: str = "",
    markdown_output: bool = config.default.markdown_output,
    prefix: str = config.default.assistant_output_prefix,
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
            msg = prompt_session.prompt(config.default.user_prompt_prefix)
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
