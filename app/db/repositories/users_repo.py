from datetime import datetime
from typing import Optional

from bson import ObjectId

from app.utils.bson_helpers import serialize_doc


async def get_user_by_email(db, email: str) -> Optional[dict]:
    user = await db["users"].find_one({"email": email})
    return serialize_doc(user) if user else None


async def get_user_by_id(db, user_id: str) -> Optional[dict]:
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    return serialize_doc(user) if user else None


async def create_user(db, user_data: dict) -> dict:
    user_data["created_at"] = datetime.utcnow()
    result = await db["users"].insert_one(user_data)
    user = await db["users"].find_one({"_id": result.inserted_id})
    return serialize_doc(user)
