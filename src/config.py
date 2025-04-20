from typing import Dict, Literal, Optional, Self

from pydantic import BaseModel, model_validator


class DefaultConfig(BaseModel):
    model: Optional[str] = None


class Provider(BaseModel):
    type: Literal["openai"]
    base_url: str
    api_key_type: Literal["key", "env"] = "key"
    api_key: str


class Model(BaseModel):
    provider: str
    model_name: str


class Config(BaseModel):
    default: DefaultConfig = DefaultConfig()
    providers: Dict[str, Provider]
    models: Dict[str, Model]

    @model_validator(mode="after")
    def check_default_model_exists(self) -> Self:
        if self.default.model is None:
            return self
        if self.default.model not in self.models.keys():
            raise ValueError(
                "default model {model} is not defined".format(model=self.default.model)
            )
        return self

    @model_validator(mode="after")
    def check_models_providers_exists(self) -> Self:
        providers = self.providers.keys()
        for model, conf in self.models.items():
            if conf.provider not in providers:
                raise ValueError(
                    "the provider {provider} of model {model} is not defined".format(
                        provider=conf.provider, model=model
                    )
                )
        return self
