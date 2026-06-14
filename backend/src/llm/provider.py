from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator
from langchain_core.messages import BaseMessage


class LLMProvider(ABC):
    @abstractmethod
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        pass

    @abstractmethod
    async def generate(
        self,
        messages: List[BaseMessage],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> BaseMessage:
        """Generate a complete response"""
        pass

    @abstractmethod
    async def stream_generate(
        self,
        messages: List[BaseMessage],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> AsyncGenerator[BaseMessage, None]:
        """Generate a response in a streaming fashion"""
        pass

    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """Calculate the number of tokens in the given text"""
        pass
