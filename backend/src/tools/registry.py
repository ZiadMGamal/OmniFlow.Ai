from typing import Dict, List, Type, Optional
from src.tools.base import BaseTool
import logging

logger = logging.getLogger("omniflow.tools.registry")


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        if tool.name in self._tools:
            logger.warning(f"Overwriting existing tool: {tool.name}")
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def get_all_tools(self) -> List[BaseTool]:
        return list(self._tools.values())

    def get_schemas(self, tool_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        tools = self.get_all_tools()
        if tool_names:
            tools = [t for t in tools if t.name in tool_names]
        return [t.get_schema() for t in tools]


tool_registry = ToolRegistry()
