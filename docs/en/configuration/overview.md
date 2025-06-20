# Overview
## Location
The configuration file for LLM CLI is located at:<br>
Windows: `C:\Users\<YourUsername>\AppData\Local\llm-cli\config.toml`<br>
macOS: `/Users/<YourUsername>/Library/Application Support/llm-cli/config.toml`<br>
Linux: `/home/<YourUsername>/.config/llm-cli/config.toml`

## Syntax
LLM CLI uses **[TOML](https://toml.io/en/v1.0.0)** as the configuration file format.

## Configuration Items
There are three main categories of configuration items:

- `default`: Manages default and global settings  
    - Default model selection  
    - Whether to render output in Markdown by default  
    - Whether to enable multi-turn conversations by default  
    - ...  
- `providers`: Manages service providers (e.g., OpenAI, DeepSeek, etc.)  
- `models`: Manages specific models (e.g., gpt-4-mini, deepseek-chat, etc.)  