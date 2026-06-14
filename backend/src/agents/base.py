import json
from typing import List, Dict, Any, Optional
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from src.llm.factory import llm_factory
from src.tools.registry import tool_registry
import logging

logger = logging.getLogger("omniflow.agent")


class BaseReActAgent:
    def __init__(
        self,
        name: str,
        system_prompt: str,
        provider: str = "openai",
        model: str = "gpt-4o",
        tools: Optional[List[str]] = None,
        temperature: float = 0.7,
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm_factory.get_provider(provider, model)
        self.temperature = temperature
        
        # Load tools from registry
        self.tools = []
        self.tool_schemas = []
        if tools:
            for t_name in tools:
                tool_instance = tool_registry.get_tool(t_name)
                if tool_instance:
                    self.tools.append(tool_instance)
                    self.tool_schemas.append(tool_instance.get_schema())

    async def _execute_tool(self, tool_call: Dict[str, Any]) -> str:
        """Execute a tool called by the LLM"""
        tool_name = tool_call.get("name")
        tool_args_str = tool_call.get("arguments", "{}")
        
        try:
            tool_args = json.loads(tool_args_str)
        except json.JSONDecodeError:
            return f"Error: Invalid JSON arguments for tool {tool_name}"

        tool_instance = tool_registry.get_tool(tool_name)
        if not tool_instance:
            return f"Error: Tool {tool_name} not found or not available to this agent"

        try:
            result = await tool_instance.run(**tool_args)
            return str(result)
        except Exception as e:
            return f"Error executing tool {tool_name}: {str(e)}"

    async def run(self, input_text: str, chat_history: Optional[List[Dict[str, Any]]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Main ReAct execution loop (Streamed)"""
        
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Add history
        if chat_history:
            for msg in chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
                    
        # Add current input
        messages.append(HumanMessage(content=input_text))

        max_iterations = 10
        iterations = 0
        
        while iterations < max_iterations:
            iterations += 1
            
            # 1. THOUGHT / REASONING (LLM Call)
            yield {"type": "status", "content": f"Thinking (Iteration {iterations})..."}
            
            response = await self.llm.generate(
                messages=messages,
                tools=self.tool_schemas if self.tool_schemas else None,
                temperature=self.temperature
            )
            
            messages.append(response)
            
            # Stream the actual text content if present
            if response.content:
                yield {"type": "content", "content": response.content}

            # 2. ACTION (Tool Calls)
            if not getattr(response, "tool_calls", None) and not getattr(response, "additional_kwargs", {}).get("tool_calls"):
                # No tools called -> FINAL ANSWER
                break

            # Handle LangChain v0.2 tool_calls abstraction
            tool_calls = getattr(response, "tool_calls", [])
            if not tool_calls:
                # Fallback to older format in additional_kwargs
                raw_calls = response.additional_kwargs.get("tool_calls", [])
                for rc in raw_calls:
                    if "function" in rc:
                        tool_calls.append({
                            "id": rc.get("id"),
                            "name": rc["function"]["name"],
                            "args": json.loads(rc["function"]["arguments"])
                        })

            for tc in tool_calls:
                tc_id = tc.get("id")
                tc_name = tc.get("name")
                tc_args = tc.get("args", {})
                
                yield {"type": "tool_call", "tool": tc_name, "args": tc_args}
                
                # Format for our executor
                exec_tc = {"name": tc_name, "arguments": json.dumps(tc_args)}
                
                # 3. OBSERVATION (Execute and get result)
                result = await self._execute_tool(exec_tc)
                
                yield {"type": "tool_result", "tool": tc_name, "result": result}
                
                # Add tool result to messages
                messages.append(ToolMessage(
                    content=result,
                    name=tc_name,
                    tool_call_id=tc_id
                ))
                
        if iterations >= max_iterations:
            yield {"type": "error", "content": "Agent reached maximum iteration limit."}
