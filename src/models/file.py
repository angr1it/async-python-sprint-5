from uuid import UUID
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, UUID, Integer, ForeignKey

from models import Base
from models.settings import MAX_USERNAME_LENGTH, MAX_PATH_LENGTH


class File(Base):
    __tablename__ = "file"
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: str = Column(String(MAX_USERNAME_LENGTH), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    path: str = Column(String(MAX_PATH_LENGTH), nullable=False)
    real_path: str = Column(String(MAX_PATH_LENGTH), nullable=False)
    size: int = Column(Integer)
    is_downloadable: bool = Column(Boolean, default=True, nullable=False)
    creator_id = Column(UUID, ForeignKey("user.id"), nullable=True)
    deleted = Column("deleted", Boolean, default=False)
