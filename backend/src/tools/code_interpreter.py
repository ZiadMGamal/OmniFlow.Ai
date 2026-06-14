import io
import sys
import traceback
from typing import Any
from pydantic import BaseModel, Field
from src.tools.base import BaseTool


class PythonExecutionInput(BaseModel):
    code: str = Field(description="The Python code to execute. Variables are NOT persisted across executions unless explicitly returned. Always use print() to output results.")


class PythonExecutorTool(BaseTool):
    name = "python_executor"
    description = "Executes arbitrary Python code in a sandboxed environment and returns the stdout and stderr."
    args_schema = PythonExecutionInput
    permission_level = "admin" # Highly privileged tool

    async def _run(self, code: str) -> str:
        # NOTE: This is a VERY simple local execution for MVP.
        # In production, this MUST use the Docker sandbox module built in Phase 4.
        
        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_error

        try:
            # Create a restricted globals dict
            exec_globals = {
                "__builtins__": __builtins__,
                "print": print,
            }
            exec(code, exec_globals)
            output = redirected_output.getvalue()
            return output if output else "Execution successful (no output)."
        except Exception:
            error_msg = traceback.format_exc()
            return f"Execution Error:\n{error_msg}"
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
