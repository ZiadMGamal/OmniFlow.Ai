from src.tools.base import BaseTool
from src.tools.registry import tool_registry, ToolRegistry
from src.tools.web_search import WebSearchTool
from src.tools.code_interpreter import PythonExecutorTool

# Register core tools automatically
tool_registry.register(WebSearchTool())
tool_registry.register(PythonExecutorTool())

__all__ = ["BaseTool", "ToolRegistry", "tool_registry"]
