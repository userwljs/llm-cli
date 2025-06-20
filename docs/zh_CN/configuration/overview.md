# 总览
## 位置
LLM CLI 的配置文件位于：<br>
Windows：`C:\Users\<你的用户名>\AppData\Local\llm-cli\config.toml`<br>
MacOS：`/Users/<你的用户名>/Library/Application Support/llm-cli/config.toml`<br>
Linux：`/home/<你的用户名>/.config/llm-cli/config.toml`

## 语法
LLM CLI 使用 **[TOML](https://toml.io/cn/v1.0.0)** 作为配置文件的格式。

## 配置项
有三大类配置项：

- default：管理默认和总体的设置
    - 默认使用什么模型
    - 是否默认使用 MarkDown 渲染输出
    - 是否默认使用多轮对话
    - ……
- providers：管理服务提供商（如 OpenAI、DeepSeek 等）
- models：管理具体模型（如 o4-mini、deepseek-chat 等）