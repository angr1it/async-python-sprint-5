from typing import Optional
import os

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import FilePath, DirectoryPath
from fastapi.responses import FileResponse

from auth.config import User
from api.auth import current_user
from services.file import file_repository, NotAuthError
from config.db import get_async_session as get_db_async
from schemas.file import FileRead


file_router = APIRouter()


@file_router.get("/")
async def show_files(
    limit: Optional[int] = None,
    offset: Optional[int] = 0,
    db: AsyncSession = Depends(get_db_async),
    user: User = Depends(current_user)
):
    try:
        return await file_repository.read_user(
            db=db,
            user=user,
            limit=limit,
            offset=offset
        )
    except NotAuthError:
        raise HTTPException(401)


@file_router.post("/upload", response_model=FileRead)
async def upload_file(
    file: UploadFile,
    file_path: Optional[FilePath] = None,
    directory_path: Optional[DirectoryPath] = None,
    db: AsyncSession = Depends(get_db_async),
    user: User = Depends(current_user)
):

    if file_path:
        directory, filename = os.path.split(file_path)
    else:
        filename = None
        directory = "/" if not directory_path else str(directory_path)

    if not user:
        raise HTTPException(401)

    return await file_repository.create(
        db=db,
        user=user,
        file=file,
        directory=directory,
        filename=filename
    )


@file_router.get("/download")
async def download_file(
    file_id: Optional[str] = None,
    file_path: Optional[str] = None,
    db: AsyncSession = Depends(get_db_async),
    user: User = Depends(current_user)
):
    if not user:
        raise HTTPException(401)

    if not file_id and not file_path:
        raise HTTPException(422, "Either parameter file_id or parameter file_path must be specified.")

    if file_id:
        path = await file_repository.download_file_by_id(db=db, user=user, file_id=file_id)
    else:
        path = await file_repository.download_file_by_path(db=db, user=user, file_path=file_path)

    return FileResponse(path=path)
