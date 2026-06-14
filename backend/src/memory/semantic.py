import uuid
from typing import List, Dict, Any, Optional
from langchain_openai import OpenAIEmbeddings
from src.core.qdrant import QdrantManager
from src.core.config import settings


class SemanticMemory:
    """Manages vector-based semantic search in Qdrant"""
    
    def __init__(self):
        self.collection_name = "semantic_memory"
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )
        
    async def init_collection(self):
        await QdrantManager.create_collection(
            collection_name=self.collection_name,
            vector_size=1536 # text-embedding-3-small size
        )
        
    async def add_memory(self, user_id: str, content: str, metadata: Dict[str, Any] = None):
        if not metadata:
            metadata = {}
        metadata["user_id"] = user_id
        metadata["content"] = content
        
        vector = await self.embeddings.aembed_query(content)
        
        point = {
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": metadata
        }
        
        await QdrantManager.upsert_vectors(self.collection_name, [point])
        return point["id"]
        
    async def search(
        self, user_id: str, query: str, limit: int = 5, score_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        query_vector = await self.embeddings.aembed_query(query)
        
        filters = {"user_id": user_id}
        
        results = await QdrantManager.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            filters=filters
        )
        
        # Return formatted payloads
        return [r["payload"] for r in results]
