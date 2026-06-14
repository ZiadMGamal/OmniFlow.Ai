from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class Organization(BaseModel):
    __tablename__ = "organizations"

    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    logo_url = Column(String(500), nullable=True)
    plan = Column(String(50), default="free", nullable=False)
    max_members = Column(Integer, default=5)
    max_agents = Column(Integer, default=10)
    max_workflows = Column(Integer, default=20)
    max_documents = Column(Integer, default=100)
    monthly_token_limit = Column(Integer, default=100000)
    monthly_tokens_used = Column(Integer, default=0)
    settings = Column(JSON, default=dict)

    members = relationship("User", back_populates="organization")
