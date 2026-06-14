import json
from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from src.agents.state import AgentState, add_messages
from src.agents.base import BaseReActAgent
from src.core.config import settings


# Pre-defined system prompts for specialized agents
SUPERVISOR_PROMPT = """You are a supervisor tasked with managing a conversation between the following workers: {members}.
Given the following user request, respond with the worker to act next.
Each worker will perform a task and respond with their results and status.
When finished, respond with FINISH."""

RESEARCHER_PROMPT = """You are a world-class Research Agent.
You have access to internet search tools. Your job is to gather accurate, up-to-date facts.
Always cite your sources."""

CODER_PROMPT = """You are an expert Software Engineer.
You can write, review, and execute Python code.
Ensure your code is efficient, well-documented, and bug-free."""


class AgentGraph:
    def __init__(self):
        self.members = ["researcher", "coder"]
        self.agents = self._init_agents()
        self.graph = self._build_graph()

    def _init_agents(self):
        return {
            "researcher": BaseReActAgent(
                name="researcher",
                system_prompt=RESEARCHER_PROMPT,
                tools=["web_search"]
            ),
            "coder": BaseReActAgent(
                name="coder",
                system_prompt=CODER_PROMPT,
                tools=["python_executor"]
            )
        }

    async def _supervisor_node(self, state: AgentState) -> dict:
        # Simplified supervisor logic for MVP
        # In a full implementation, this calls an LLM to decide the next route
        messages = state["messages"]
        last_message = messages[-1].content.lower()
        
        if "search" in last_message or "find" in last_message:
            return {"next_node": "researcher"}
        elif "code" in last_message or "python" in last_message or "script" in last_message:
            return {"next_node": "coder"}
        else:
            return {"next_node": "FINISH", "final_response": "I'm not sure which agent should handle this request."}

    async def _researcher_node(self, state: AgentState) -> dict:
        agent = self.agents["researcher"]
        # Simplified execution - gathering final output from generator
        last_human_msg = next((m.content for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), "")
        
        final_content = ""
        async for chunk in agent.run(last_human_msg):
            if chunk["type"] == "content":
                final_content += chunk["content"]
                
        return {"messages": [AIMessage(content=f"[Researcher]: {final_content}")], "sender": "researcher"}

    async def _coder_node(self, state: AgentState) -> dict:
        agent = self.agents["coder"]
        last_human_msg = next((m.content for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), "")
        
        final_content = ""
        async for chunk in agent.run(last_human_msg):
            if chunk["type"] == "content":
                final_content += chunk["content"]
                
        return {"messages": [AIMessage(content=f"[Coder]: {final_content}")], "sender": "coder"}

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("coder", self._coder_node)

        # Add edges
        for member in self.members:
            workflow.add_edge(member, "supervisor")

        # Conditional edges from supervisor
        def router(state: AgentState) -> str:
            next_node = state.get("next_node")
            if next_node == "FINISH":
                return END
            return next_node

        workflow.add_conditional_edges(
            "supervisor",
            router,
            {"researcher": "researcher", "coder": "coder", END: END}
        )

        workflow.add_edge(START, "supervisor")
        
        return workflow.compile()

    async def invoke(self, input_text: str):
        app = self.graph
        initial_state = {
            "messages": [HumanMessage(content=input_text)],
            "sender": "user"
        }
        
        async for event in app.astream(initial_state):
            yield event
