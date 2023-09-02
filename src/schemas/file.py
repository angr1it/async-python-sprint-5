from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    creator_id: uuid.UUID
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool


class FileRead(FileBase):
    id: uuid.UUID


class FileCreate(FileBase):
    real_path: str


class FileInDBBase(FileRead):
    model_config = ConfigDict(from_attributes=True)

    deleted: bool
