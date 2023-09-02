from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_async_session
from services.ping import ping
from auth.config import User
from api.auth import current_user
from config.redis import redis

ping_router = APIRouter()


@ping_router.get('/')
async def get_ping(
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
):
    connect = await ping(db=db, redis=redis)

    email = None if not user else user.email

    return {
        "status": "OK",
        "data": {
            "services": connect,
            "user": email
        },
        "description": None
    }
