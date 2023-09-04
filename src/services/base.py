from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base


class Repository(ABC):

    @abstractmethod
    def create(self, *args, **kwargs):
        pass


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType]):

    def __init__(self, model: type[ModelType]) -> None:
        self._model = model

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType):
        obj = self._model(**obj_in.model_dump())

        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
