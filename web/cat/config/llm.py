import langchain
from pydantic import PyObject, BaseSettings


# Base class to manage LLM configuration.
class LLMSettings(BaseSettings):
    # class instantiating the model
    _pyclass: None

    # instantiate an LLM from configuration
    @classmethod
    def get_llm_from_config(cls, config):
        if cls._pyclass is None:
            raise Exception(
                "Language model configuration class has self._pyclass = None. Should be a valid LLM class"
            )
        return cls._pyclass(**config)


class LLMDefault(langchain.llms.base.LLM):
    @property
    def _llm_type(self):
        return ""

    def _call(self, prompt, stop=None):
        # TODO: if AI prefix in the agent changes, this will break
        return "AI: You did not configure a Language Model. Send a POST request to ... [TODO: instructions here]"


class LLMDefaultConfig(LLMSettings):
    _pyclass: PyObject = LLMDefault

    class Config:
        schema_extra = {
            "name_human_readable": "Default Language Model",
            "description": "A dumb LLM just telling that the Cat is not configured. There will be a nice LLM here once consumer hardware allows it.",
        }


class LLMOpenAIConfig(LLMSettings):
    openai_api_key: str
    _pyclass: PyObject = langchain.llms.OpenAI

    class Config:
        schema_extra = {
            "name_human_readable": "OpenAI GPT-3",
            "description": "OpenAI GPT-3. More expensive but also more flexible than ChatGPT.",
        }


class LLMOpenAIChatConfig(LLMSettings):
    openai_api_key: str
    _pyclass: PyObject = langchain.llms.OpenAIChat

    class Config:
        schema_extra = {
            "name_human_readable": "OpenAI ChatGPT",
            "description": "Chat model from OpenAI",
        }


class LLMCohereChatConfig(LLMSettings):
    cohere_api_key: str
    _pyclass: PyObject = langchain.llms.Cohere

    class Config:
        schema_extra = {
            "name_human_readable": "Cohere",
            "description": "Configuration for Cohere language model",
        }


class LLMHuggingFaceHubConfig(LLMSettings):
    repo_id: str
    huggingfacehub_api_token: str
    _pyclass: PyObject = langchain.llms.HuggingFaceHub

    class Config:
        schema_extra = {
            "name_human_readable": "HuggingFace Hub",
            "description": "Configuration for HuggingFace Hub language models",
        }


class LLMHuggingFaceEndpointConfig(LLMSettings):
    endpoint_url: str
    huggingfacehub_api_token: str
    _pyclass: PyObject = langchain.llms.HuggingFaceEndpoint

    class Config:
        schema_extra = {
            "name_human_readable": "HuggingFace Endpoint",
            "description": "Configuration for HuggingFace Endpoint language models",
        }


SUPPORTED_LANGUAGE_MODELS = [
    LLMDefaultConfig,
    LLMOpenAIConfig,
    LLMOpenAIChatConfig,
    LLMCohereChatConfig,
    LLMHuggingFaceHubConfig,
    LLMHuggingFaceEndpointConfig,
]

# LLM_SCHEMAS contains metadata to let any client know which fields are required to create the language model.
LLM_SCHEMAS = {}
for config_class in SUPPORTED_LANGUAGE_MODELS:
    schema = config_class.schema()
    schema["languageModelName"] = schema[
        "title"
    ]  # useful for clients in order to call the correct config endpoints
    LLM_SCHEMAS[schema["title"]] = schema
