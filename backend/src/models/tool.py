from sqlalchemy import Column, String, Boolean, JSON, Integer, Text
from src.models.base import BaseModel


class Tool(BaseModel):
    __tablename__ = "tools"

    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    input_schema = Column(JSON, default=dict)
    output_schema = Column(JSON, default=dict)
    permission_level = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    is_builtin = Column(Boolean, default=True)
    requires_api_key = Column(Boolean, default=False)
    api_key_name = Column(String(100), nullable=True)
    config = Column(JSON, default=dict)
    total_executions = Column(Integer, default=0)
    avg_latency_ms = Column(Integer, default=0)
    success_rate = Column(Integer, default=100)
    icon = Column(String(100), nullable=True)
    version = Column(String(20), default="1.0.0")
