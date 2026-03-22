from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_client: AsyncIOMotorClient = None
_db: AsyncIOMotorDatabase = None


async def connect_to_mongo() -> None:
    global _client, _db
    _client = AsyncIOMotorClient(settings.MONGO_URI)
    _db = _client[settings.DATABASE_NAME]


async def close_mongo_connection() -> None:
    global _client
    if _client is not None:
        _client.close()


@asynccontextmanager
async def lifespan(app):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


async def get_database() -> AsyncIOMotorDatabase:
    return _db
