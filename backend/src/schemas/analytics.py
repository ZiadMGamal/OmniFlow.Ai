from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_conversations: int
    total_messages: int
    total_tokens: int
    total_cost: float
    total_agent_runs: int
    avg_latency_ms: float
    success_rate: float
    active_users: int


class TokenUsageData(BaseModel):
    date: str
    tokens_input: int
    tokens_output: int
    total_tokens: int
    cost: float


class AgentPerformanceData(BaseModel):
    agent_id: UUID
    agent_name: str
    total_runs: int
    success_rate: float
    avg_latency_ms: float
    total_tokens: int
    total_cost: float


class ProviderUsageData(BaseModel):
    provider: str
    model: str
    total_requests: int
    total_tokens: int
    total_cost: float
    avg_latency_ms: float


class AnalyticsDashboardResponse(BaseModel):
    overview: AnalyticsOverview
    token_usage: List[TokenUsageData]
    agent_performance: List[AgentPerformanceData]
    provider_usage: List[ProviderUsageData]
    recent_errors: List[Dict[str, Any]]


class AnalyticsDateRange(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    period: str = "7d"
