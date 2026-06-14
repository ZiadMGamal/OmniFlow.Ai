import tiktoken
from typing import List, Dict, Any, Optional, AsyncGenerator
from langchain_core.messages import BaseMessage
from langchain_community.chat_models import ChatOllama
from src.llm.provider import LLMProvider
from src.core.config import settings


class OllamaProvider(LLMProvider):
    def __init__(self, model_name: str = "llama3", **kwargs):
        self.model_name = model_name
        self.base_url = settings.OLLAMA_BASE_URL

        self.client = ChatOllama(
            model=self.model_name,
            base_url=self.base_url,
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
        client = self.client.bind(temperature=temperature)
        # Note: Ollama tool support varies by model
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
        client = self.client.bind(temperature=temperature)
        if tools:
            client = client.bind_tools(tools)
        
        async for chunk in client.astream(messages):
            yield chunk

    def get_token_count(self, text: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
