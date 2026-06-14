from typing import Annotated, Sequence, TypedDict, Dict, Any, List
import operator
from langchain_core.messages import BaseMessage


def add_messages(left: Sequence[BaseMessage], right: Sequence[BaseMessage]) -> Sequence[BaseMessage]:
    """Custom reducer for messages that ensures no duplicates by ID"""
    left_dict = {m.id: m for m in left if m.id}
    for m in right:
        if m.id:
            left_dict[m.id] = m
    return list(left_dict.values())


class AgentState(TypedDict):
    """The state of the agent execution graph."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    sender: str
    next_node: str
    intermediate_steps: Annotated[List[tuple[Any, Any]], operator.add]
    task: str
    plan: List[str]
    context: str
    final_response: str
