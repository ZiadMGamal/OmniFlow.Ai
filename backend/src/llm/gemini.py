import tiktoken
from typing import List, Dict, Any, Optional, AsyncGenerator
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from src.llm.provider import LLMProvider
from src.core.config import settings


class GeminiProvider(LLMProvider):
    def __init__(self, model_name: str = "gemini-1.5-pro", api_key: Optional[str] = None, **kwargs):
        self.model_name = model_name
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key is missing")

        self.client = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
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
        client = self.client.bind(temperature=temperature, max_output_tokens=max_tokens)
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
        client = self.client.bind(temperature=temperature, max_output_tokens=max_tokens)
        if tools:
            client = client.bind_tools(tools)
        
        async for chunk in client.astream(messages):
            yield chunk

    def get_token_count(self, text: str) -> int:
        # Approximate
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
