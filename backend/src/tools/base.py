from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger("omniflow.tools")


class BaseTool(ABC):
    name: str
    description: str
    args_schema: Type[BaseModel]
    permission_level: str = "user"
    requires_api_key: bool = False

    @abstractmethod
    async def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Execute the core logic of the tool"""
        pass

    async def run(self, **kwargs: Any) -> Any:
        """Wrapper method that handles validation, logging, and execution"""
        try:
            # Validate input against schema
            validated_args = self.args_schema(**kwargs)
            
            logger.info(f"Executing tool {self.name} with args {kwargs}")
            
            # Execute tool
            result = await self._run(**validated_args.model_dump())
            
            logger.info(f"Tool {self.name} execution successful")
            return result
            
        except Exception as e:
            logger.error(f"Tool {self.name} execution failed: {str(e)}")
            raise e

    def get_schema(self) -> Dict[str, Any]:
        """Return the OpenAI-compatible function schema"""
        schema = self.args_schema.model_json_schema()
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": schema.get("properties", {}),
                    "required": schema.get("required", []),
                },
            }
        }
