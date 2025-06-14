# 配置参考
**在开始配置前，请确保你了解 [TOML](https://toml.io/cn/v1.0.0) 的使用**

**在 `default` 和 `models` 表中，会同时存在 `模型 ID` 和 `模型名称` 两种说法。它们是不同的概念，请注意。**
## `default`
|键|类型|默认值|说明|是否必需|
|---|---|---|---|---|
|`model`|字符串，必须为在 `models` 里定义的**模型 ID**|无|默认使用的模型|如果未设置，程序会强制要求用户使用 `-m/--model` 指定模型|
|`markdown_output`|布尔|是|默认是否使用 MarkDown 格式化 LLM 输出|否|
|`multi_turn`|布尔|是|默认是否进行多轮对话|否|
|`user_prompt_prefix`|字符串|`User: `|询问用户输入时，显示的问题|否|
|`assistant_output_prefix`|字符串|`Assistant: `|LLM 输出时，显示的前缀|否|

## `providers`
**LLM CLI 通过在 `providers` 表中定义子表（即通过 `[providers.在此处填写提供商 ID]` 定义的表）来定义提供商。**

子表参考：

|键|类型|默认值|说明|是否必需|
|---|---|---|---|---|
|`type`|字符串，只能是 `openai`|`openai`|使用哪种格式的 API 请求|否|
|`base_url`|字符串|无|API 请求的网址|是|
|`api_key_type`|字符串，只能是 `key`、`env` 中的一个|`key`|如果为 `key`，则会将 `api_key` 的值直接作为 API 密钥；<br>如果为 `env`，则会读取以 `api_key` 的值为名字的环境变量作为 API 密钥|否|
|`api_key`|字符串|无|API 密钥或存储 API 密钥的环境变量的名字|是|

## `models`
**LLM CLI 通过在 `models` 表中定义子表（即通过 `[models.在此处填写模型 ID]` 定义的表）来定义模型。**

其中，**子表的表名将作为模型 ID**。
**模型 ID** 用来在 LLM CLI 中区分模型；
而**模型名称**是会在 API 请求中使用的名字。

举个例子：有一个模型，它的模型名称是 `deepseek-chat`，它的模型 ID 是 `ds`。<br>
在 LLM CLI 中（如：`default.model`、`-m/--model` 选项中）应该使用模型 ID（`ds`）。<br>
而模型名称（`deepseek-chat`）则是在服务提供商那边的名字，它会在 API 请求中被使用。

示例配置（此配置不可用，仅用于说明）：
```toml
[models.ds] # ds 就是它的模型 ID
model_name = "deepseek-chat" # 模型名称，在 API 请求中使用
provider = "deepseek" # 提供商，假设存在
```

子表参考：

|键|类型|默认值|说明|是否必需|
|---|---|---|---|---|
|`provider`|字符串，必须为在 `providers` 里定义的提供商|无|由哪家提供商提供模型|是|
|`model_name`|字符串|无|在 API 请求中使用的模型名称|是|
