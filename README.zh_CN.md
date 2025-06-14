# LLM CLI
一个 LLM 的命令行界面。
<p align="center"><a href="README.md">English</a> | 简体中文</p>

# 安装
**以下的绝大部分操作，对于中国大陆用户来说需要代理或镜像。**

**在安装 LLM CLI 前，需要安装 [Python](https://www.python.org/downloads/)。**

**你可能需要配置 PATH 环境变量。**

通过 `pip` 安装（通常在 MacOS 和 Linux 上不可用）：
```bash
pip install llm_ya_cli
```

通过 [`pipx`](https://pipx.pypa.io/) 安装：
```bash
pipx install llm_ya_cli
```

通过 [`uv`](https://docs.astral.sh/uv/getting-started/installation/) 安装
```bash
uv tool install llm_ya_cli
```

# 许可证
此项目包含以下第三方项目的代码：
- **[Rich](https://github.com/Textualize/rich)** 
([live_render.py](src/llm_cli/utils/live_render.py)) 
([许可证](licenses/LICENSE-Rich))
**Copyright (c) 2020 Will McGugan**
- **[Chatlas](https://github.com/posit-dev/chatlas)** 
([live_render.py](src/llm_cli/utils/live_render.py)，修改自 Rich 的代码) 
([许可证](licenses/LICENSE-Chatlas))
**Copyright (c) 2022-2025 Posit Software, PBC**
