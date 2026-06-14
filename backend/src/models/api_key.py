from sqlalchemy import Column, String, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.models.base import BaseModel


class UserApiKey(BaseModel):
    __tablename__ = "user_api_keys"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    provider = Column(String(100), nullable=False)
    encrypted_key = Column(String(1000), nullable=False)
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    permissions = Column(JSON, default=list)

    from sqlalchemy.orm import relationship
    user = relationship("User", back_populates="api_keys")
