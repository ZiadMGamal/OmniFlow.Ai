from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken


class DocumentChunker:
    """Intelligently chunks text documents based on tokens and structure"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoder = tiktoken.get_encoding("cl100k_base")
        
    def _length_function(self, text: str) -> int:
        return len(self.encoder.encode(text))
        
    def split_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=self._length_function,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        
        chunks = splitter.split_text(text)
        
        result = []
        for i, chunk in enumerate(chunks):
            chunk_meta = metadata.copy() if metadata else {}
            chunk_meta["chunk_index"] = i
            chunk_meta["token_count"] = self._length_function(chunk)
            
            result.append({
                "content": chunk,
                "metadata": chunk_meta
            })
            
        return result
