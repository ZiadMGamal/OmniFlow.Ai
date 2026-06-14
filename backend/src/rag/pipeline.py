from uuid import UUID
from typing import List, Dict, Any
from src.rag.chunker import DocumentChunker
from src.rag.processor import FileProcessor
from src.rag.retriever import VectorRetriever


class RAGPipeline:
    """End-to-end pipeline for document ingestion and semantic retrieval"""
    
    def __init__(self):
        self.chunker = DocumentChunker()
        self.retriever = VectorRetriever()
        
    async def ingest_document(self, file_content: bytes, filename: str, collection_name: str, document_id: str) -> Dict[str, Any]:
        """Process file, chunk text, embed, and store in vector DB"""
        
        # 1. Extract Text
        extracted = FileProcessor.process(file_content, filename)
        text = extracted["text"]
        
        base_metadata = {
            "document_id": document_id,
            "filename": filename,
            "source": "upload",
            **extracted["metadata"]
        }
        
        # 2. Chunk Text
        chunks = self.chunker.split_text(text, metadata=base_metadata)
        
        # 3. Create Vector Collection if needed
        await self.retriever.create_collection(collection_name)
        
        # 4. Embed and Store
        # Process in batches if large
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            await self.retriever.embed_and_store(collection_name, batch)
            
        return {
            "status": "success",
            "total_chunks": len(chunks),
            "total_tokens": sum(c["metadata"]["token_count"] for c in chunks)
        }
        
    async def retrieve_context(self, query: str, collection_name: str, limit: int = 5) -> str:
        """Search for relevant chunks and format as context string"""
        
        results = await self.retriever.search(
            collection_name=collection_name,
            query=query,
            limit=limit
        )
        
        if not results:
            return ""
            
        context_parts = []
        for i, result in enumerate(results):
            payload = result["payload"]
            score = result["score"]
            filename = payload.get("filename", "Unknown Source")
            content = payload.get("content", "")
            
            context_parts.append(f"--- Source {i+1}: {filename} (Relevance: {score:.2f}) ---\n{content}\n")
            
        return "\n".join(context_parts)


rag_pipeline = RAGPipeline()
