import json
from typing import List, Dict, Any, Optional
from src.core.redis import RedisManager


class ShortTermMemory:
    """Manages conversational context in Redis"""
    
    def __init__(self, ttl_seconds: int = 86400): # 24 hours
        self.ttl = ttl_seconds
        
    def _get_key(self, conversation_id: str) -> str:
        return f"memory:short:{conversation_id}"
        
    async def add_message(self, conversation_id: str, role: str, content: str, **kwargs):
        message = {
            "role": role,
            "content": content,
            **kwargs
        }
        key = self._get_key(conversation_id)
        client = RedisManager.get_client()
        
        # Keep list bounded
        pipe = client.pipeline()
        await pipe.rpush(key, json.dumps(message))
        await pipe.ltrim(key, -50, -1) # Keep last 50 messages
        await pipe.expire(key, self.ttl)
        await pipe.execute()
        
    async def get_context(self, conversation_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        key = self._get_key(conversation_id)
        raw_messages = await RedisManager.lrange(key, -limit, -1)
        return [json.loads(m) for m in raw_messages]
        
    async def clear(self, conversation_id: str):
        key = self._get_key(conversation_id)
        await RedisManager.delete(key)
