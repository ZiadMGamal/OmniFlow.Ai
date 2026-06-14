import tiktoken
from typing import List, Dict, Any, Optional, AsyncGenerator
from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from src.llm.provider import LLMProvider
from src.core.config import settings


class AnthropicProvider(LLMProvider):
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620", api_key: Optional[str] = None, **kwargs):
        self.model_name = model_name
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("Anthropic API key is missing")

        self.client = ChatAnthropic(
            model=self.model_name,
            api_key=self.api_key,
            **kwargs
        )

    async def generate(
        self,
        messages: List[BaseMessage],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> BaseMessage:
        client = self.client.bind(temperature=temperature, max_tokens=max_tokens)
        if tools:
            client = client.bind_tools(tools)
        
        response = await client.ainvoke(messages)
        return response

    async def stream_generate(
        self,
        messages: List[BaseMessage],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> AsyncGenerator[BaseMessage, None]:
        client = self.client.bind(temperature=temperature, max_tokens=max_tokens)
        if tools:
            client = client.bind_tools(tools)
        
        async for chunk in client.astream(messages):
            yield chunk

    def get_token_count(self, text: str) -> int:
        # Approximate using cl100k_base
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
