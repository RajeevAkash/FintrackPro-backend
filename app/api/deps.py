from fastapi import Depends

from app.core.database import get_database
from app.core.security import get_current_user


async def get_db():
    return await get_database()
