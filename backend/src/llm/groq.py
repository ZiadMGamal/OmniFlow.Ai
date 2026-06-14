import tiktoken
from typing import List, Dict, Any, Optional, AsyncGenerator
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from src.llm.provider import LLMProvider
from src.core.config import settings


class GroqProvider(LLMProvider):
    def __init__(self, model_name: str = "llama3-8b-8192", api_key: Optional[str] = None, **kwargs):
        self.model_name = model_name
        self.api_key = api_key or settings.GROQ_API_KEY
        if not self.api_key:
            raise ValueError("Groq API key is missing")

        # Groq uses OpenAI-compatible API
        self.client = ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1",
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
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
