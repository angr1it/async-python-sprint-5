from fastapi import APIRouter

from api.ping import ping_router
from api.file import file_router

api_router = APIRouter()


api_router.include_router(router=ping_router, prefix="/ping")
api_router.include_router(router=file_router, prefix="/files")
