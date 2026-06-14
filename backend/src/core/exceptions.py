from typing import Optional


class OmniFlowException(Exception):
    def __init__(self, message: str, status_code: int = 500, detail: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


class AuthenticationError(OmniFlowException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, status_code=401)


class AuthorizationError(OmniFlowException):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, status_code=403)


class NotFoundError(OmniFlowException):
    def __init__(self, resource: str, resource_id: str = ""):
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(message=message, status_code=404)


class ValidationError(OmniFlowException):
    def __init__(self, message: str = "Validation failed", detail: Optional[str] = None):
        super().__init__(message=message, status_code=422, detail=detail)


class RateLimitError(OmniFlowException):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message=message, status_code=429)


class AgentExecutionError(OmniFlowException):
    def __init__(self, message: str = "Agent execution failed", detail: Optional[str] = None):
        super().__init__(message=message, status_code=500, detail=detail)


class ToolExecutionError(OmniFlowException):
    def __init__(self, tool_name: str, message: str = "Tool execution failed"):
        super().__init__(message=f"Tool '{tool_name}': {message}", status_code=500)


class LLMProviderError(OmniFlowException):
    def __init__(self, provider: str, message: str = "LLM provider error"):
        super().__init__(message=f"LLM Provider '{provider}': {message}", status_code=502)


class StorageError(OmniFlowException):
    def __init__(self, message: str = "Storage operation failed"):
        super().__init__(message=message, status_code=500)


class WorkflowError(OmniFlowException):
    def __init__(self, message: str = "Workflow execution failed"):
        super().__init__(message=message, status_code=500)


class DocumentProcessingError(OmniFlowException):
    def __init__(self, message: str = "Document processing failed"):
        super().__init__(message=message, status_code=500)


class SandboxError(OmniFlowException):
    def __init__(self, message: str = "Sandbox execution failed"):
        super().__init__(message=message, status_code=500)


class QuotaExceededError(OmniFlowException):
    def __init__(self, message: str = "Usage quota exceeded"):
        super().__init__(message=message, status_code=429)
