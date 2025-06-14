# 配置示例
**以下所有示例均需要配置 API 密钥才能使用。**
## 深度求索
本示例包含了深度求索提供商和它的两个模型。注意：LLM CLI 尚未支持显示 DeepSeek 推理模型的思考过程。
```toml
[providers.deepseek]
type = "openai"
api_key_type = "key"
api_key = "在此处输入 API 密钥"
base_url = "https://api.deepseek.com"

[models.deepseek-chat]
model_name = "deepseek-chat"
provider = "deepseek"

[models.deepseek-reasoner]
model_name = "deepseek-reasoner"
provider = "deepseek"
```