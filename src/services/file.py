from datetime import datetime
from typing import Any, Coroutine
import uuid
from pathlib import Path

import aiofiles
from aiofiles.os import makedirs
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import UploadFile

from auth.config import User
from services.base import RepositoryDB
from models.file import File as FileModel
from schemas.file import FileCreate

FILESTORE_ROOT = "/media"


class NotAuthError(Exception):
    pass


class RebositoryDBFile(RepositoryDB[FileModel, FileCreate]):

    async def __write_file(self, filepath: Path, data: UploadFile):
        dir = str(filepath.parent)
        await makedirs(dir, exist_ok=True)
        async with aiofiles.open(file=filepath, mode="wb") as f:
            await f.write(await data.read())

    async def create(
        self, db: AsyncSession, user: User, file: UploadFile, filename: str, directory: str
    ) -> Coroutine[Any, Any, FileModel]:

        if filename:
            file.filename = filename
        else:
            filename = file.filename

        if directory == "/":
            directory = ""

        path = Path(directory, filename)
        temp = FILESTORE_ROOT + "/" + str(user.id) + str(path)
        full_path = Path(temp)

        await self.__write_file(full_path, file)

        return await super().create(
            db=db,
            obj_in=FileCreate(
                name=file.filename,
                created_at=datetime.utcnow(),
                path=str(path),
                real_path=str(full_path),
                size=file.size,
                is_downloadable=True,
                creator_id=user.id
            )
        )

    async def read_user(self, db: AsyncSession, user: User, limit: int, offset: int):

        if not user:
            raise NotAuthError

        statement = (
            select(self._model)
            .where(self._model.creator_id == user.id, self._model.deleted == False)  # noqa
            .limit(limit=limit)
            .offset(offset=offset)
        )

        result = await db.execute(statement)
        return result.scalars().all()

    async def download_file_by_id(self, db: AsyncSession, user: User, file_id: uuid.UUID):
        statement = (
            select(self._model.real_path)
            .where(self._model.creator_id == user.id, self._model.deleted == False, self._model.id == file_id)  # noqa
        )

        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def download_file_by_path(self, db: AsyncSession, user: User, file_path: str):
        statement = (
            select(self._model.real_path)
            .where(self._model.creator_id == user.id, self._model.deleted == False, self._model.path == file_path)  # noqa
        )

        result = await db.execute(statement)
        return result.scalar_one_or_none()


file_repository = RebositoryDBFile(FileModel)
