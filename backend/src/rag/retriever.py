from typing import List, Dict, Any, Optional
from langchain_openai import OpenAIEmbeddings
from src.core.qdrant import QdrantManager
from src.core.config import settings


class VectorRetriever:
    """Handles embedding generation and vector search"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY
        )
        self.vector_size = 1536

    async def create_collection(self, collection_name: str):
        await QdrantManager.create_collection(
            collection_name=collection_name,
            vector_size=self.vector_size
        )

    async def embed_and_store(
        self, collection_name: str, chunks: List[Dict[str, Any]]
    ):
        # Extract texts for embedding
        texts = [chunk["content"] for chunk in chunks]
        
        # Batch generate embeddings
        vectors = await self.embeddings.aembed_documents(texts)
        
        # Prepare points for Qdrant
        points = []
        for i, chunk in enumerate(chunks):
            import uuid
            chunk_id = str(uuid.uuid4())
            chunk["metadata"]["chunk_id"] = chunk_id
            
            payload = {
                "content": chunk["content"],
                **chunk["metadata"]
            }
            
            points.append({
                "id": chunk_id,
                "vector": vectors[i],
                "payload": payload
            })
            
        await QdrantManager.upsert_vectors(collection_name, points)

    async def search(
        self, collection_name: str, query: str, limit: int = 5, score_threshold: float = 0.7, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        query_vector = await self.embeddings.aembed_query(query)
        
        results = await QdrantManager.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            filters=filters
        )
        
        return results
