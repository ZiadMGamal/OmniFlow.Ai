from typing import Optional
from src.llm.provider import LLMProvider
from src.llm.openai import OpenAIProvider
from src.llm.anthropic import AnthropicProvider
from src.llm.gemini import GeminiProvider
from src.llm.groq import GroqProvider
from src.llm.ollama import OllamaProvider


class LLMFactory:
    @staticmethod
    def get_provider(
        provider_name: str,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ) -> LLMProvider:
        provider_name = provider_name.lower()
        
        if provider_name == "openai":
            return OpenAIProvider(model_name=model_name or "gpt-4o", api_key=api_key, **kwargs)
        elif provider_name == "anthropic":
            return AnthropicProvider(model_name=model_name or "claude-3-5-sonnet-20240620", api_key=api_key, **kwargs)
        elif provider_name == "gemini":
            return GeminiProvider(model_name=model_name or "gemini-1.5-pro", api_key=api_key, **kwargs)
        elif provider_name == "groq":
            return GroqProvider(model_name=model_name or "llama3-8b-8192", api_key=api_key, **kwargs)
        elif provider_name == "ollama":
            return OllamaProvider(model_name=model_name or "llama3", **kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_name}")


llm_factory = LLMFactory()
