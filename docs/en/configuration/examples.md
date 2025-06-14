# Configuration Examples
**All the following examples require configuring an API key to be used.**
## DeepSeek
This example includes the DeepSeek provider and its two models. Note: LLM CLI does not yet support displaying the reasoning process of DeepSeek inference models.
```toml
[providers.deepseek]
type = "openai"
api_key_type = "key"
api_key = "ENTER YOUR API KEY HERE"
base_url = "https://api.deepseek.com"

[models.deepseek-chat]
model_name = "deepseek-chat"
provider = "deepseek"

[models.deepseek-reasoner]
model_name = "deepseek-reasoner"
provider = "deepseek"
```