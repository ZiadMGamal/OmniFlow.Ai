from typing import Optional, List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    SearchParams,
)
from src.core.config import settings


class QdrantManager:
    _client: Optional[QdrantClient] = None

    @classmethod
    def initialize(cls):
        cls._client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            timeout=30,
        )

    @classmethod
    def get_client(cls) -> QdrantClient:
        if not cls._client:
            raise RuntimeError("Qdrant not initialized")
        return cls._client

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()

    @classmethod
    async def create_collection(
        cls,
        collection_name: str,
        vector_size: int = 1536,
        distance: Distance = Distance.COSINE,
    ):
        collections = cls._client.get_collections().collections
        existing = [c.name for c in collections]
        if collection_name not in existing:
            cls._client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=distance,
                ),
            )

    @classmethod
    async def upsert_vectors(
        cls,
        collection_name: str,
        points: List[Dict[str, Any]],
    ):
        point_structs = [
            PointStruct(
                id=p["id"],
                vector=p["vector"],
                payload=p.get("payload", {}),
            )
            for p in points
        ]
        cls._client.upsert(
            collection_name=collection_name,
            points=point_structs,
        )

    @classmethod
    async def search(
        cls,
        collection_name: str,
        query_vector: List[float],
        limit: int = 10,
        score_threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        query_filter = None
        if filters:
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filters.items()
            ]
            query_filter = Filter(must=conditions)

        results = cls._client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter,
        )

        return [
            {
                "id": r.id,
                "score": r.score,
                "payload": r.payload,
            }
            for r in results
        ]

    @classmethod
    async def delete_vectors(
        cls,
        collection_name: str,
        ids: List[str],
    ):
        cls._client.delete(
            collection_name=collection_name,
            points_selector=ids,
        )

    @classmethod
    async def delete_collection(cls, collection_name: str):
        cls._client.delete_collection(collection_name=collection_name)
