# Configuration Reference
**Before starting configuration, ensure you're familiar with using [TOML](https://toml.io/en/v1.0.0).**

**In both the `default` and `models` tables, you'll encounter both `Model ID` and `Model Name` - these are distinct concepts requiring careful attention.**
## `default`
|Key|Type|Default Value|Description|Required|
|---|---|---|---|---|
|`model`|String (must be a **Model ID** defined in `models`)|None|Default model to use|If unset, users must explicitly specify models via `-m/--model`|
|`markdown_output`|Boolean|`true`|Whether to render LLM output in MarkDown by default|No|
|`multi_turn`|Boolean|`true`|Whether to enable multi-turn conversations by default|No|
|`user_prompt_prefix`|String|`User: `|Prefix displayed when prompting for user input|No|
|`assistant_output_prefix`|String|`Assistant: `|Prefix displayed before LLM output|No|

## `providers`
**LLM CLI defines providers through subtables in the `providers` table (declared as `[providers.<provider_id>]`).**

Provider subtable reference:

|Key|Type|Default Value|Description|Required|
|---|---|---|---|---|
|`type`|String (only `openai`)|`openai`|API request format to use|No|
|`base_url`|String|None|API endpoint URL|Yes|
|`api_key_type`|String (`key` or `env`)|`key`|`key`: Use `api_key` value directly<br>`env`: Read environment variable named in `api_key`|No|
|`api_key`|String|None|API key or environment variable name storing the key|Yes|

## `models`
**LLM CLI defines models through subtables in the `models` table (declared as `[models.<model_id>]`).**

**The subtable name becomes the Model ID** used to identify models within LLM CLI.<br>
**Model Name** refers to the identifier used in actual API requests.

Example: A model with name `deepseek-chat` and ID `ds`.<br>
Use Model ID (`ds`) in LLM CLI (e.g., `default.model`, `-m/--model` options).<br>
Model Name (`deepseek-chat`) is sent to providers during API requests.

Configuration example (illustrative only, non-functional):
```toml
[models.ds] # "ds" is the Model ID
model_name = "deepseek-chat" # Model Name used in API requests
provider = "deepseek" # Provider reference (assumes existence)
```

Model subtable reference:

|Key|Type|Default Value|Description|Required|
|---|---|---|---|---|
|`provider`|String (must reference a defined provider)|None|Service provider for the model|Yes|
|`model_name`|String|None|Model identifier used in API requests|Yes|
