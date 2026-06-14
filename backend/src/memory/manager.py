from uuid import UUID
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.memory.short_term import ShortTermMemory
from src.memory.long_term import long_term_memory
from src.memory.semantic import SemanticMemory


class MemoryManager:
    """Orchestrates different memory types to provide unified context to agents"""
    
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.semantic = SemanticMemory()
        
    async def setup(self):
        await self.semantic.init_collection()
        
    async def save_interaction(
        self, session: AsyncSession, user_id: UUID, conversation_id: UUID, user_input: str, agent_response: str
    ):
        # 1. Save to fast short-term context
        await self.short_term.add_message(str(conversation_id), "user", user_input)
        await self.short_term.add_message(str(conversation_id), "assistant", agent_response)
        
        # 2. Save semantic meaning for future search
        # In a real system, we'd run an LLM task here to extract facts/summarize 
        # before saving to semantic memory to reduce noise.
        combined = f"User: {user_input}\nAssistant: {agent_response}"
        await self.semantic.add_memory(str(user_id), combined, {"conversation_id": str(conversation_id)})
        
    async def get_agent_context(
        self, session: AsyncSession, user_id: UUID, conversation_id: UUID, current_query: str
    ) -> str:
        """Assembles a rich context string for the agent's prompt"""
        
        # Fetch core persistent memories
        core_memories = await long_term_memory.get_core_memories(session, user_id)
        core_text = "\n".join([f"- {m.content}" for m in core_memories])
        
        # Fetch semantic matches for current query
        semantic_matches = await self.semantic.search(str(user_id), current_query, limit=3)
        semantic_text = "\n".join([f"- {m.get('content')}" for m in semantic_matches])
        
        # Fetch recent conversation history
        recent_history = await self.short_term.get_context(str(conversation_id), limit=10)
        history_text = ""
        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
            
        # Assemble
        context = "=== USER PROFILE & CORE MEMORIES ===\n"
        context += (core_text if core_text else "None") + "\n\n"
        
        context += "=== RELEVANT PAST CONTEXT ===\n"
        context += (semantic_text if semantic_text else "None") + "\n\n"
        
        context += "=== RECENT CONVERSATION ===\n"
        context += (history_text if history_text else "None")
        
        return context


memory_manager = MemoryManager()
