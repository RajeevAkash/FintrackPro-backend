from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from app.utils.bson_helpers import serialize_doc


async def create_goal(db, goal_data: dict) -> dict:
    now = datetime.utcnow()
    goal_data["current_amount"] = 0.0
    goal_data["progress_log"] = []
    goal_data["created_at"] = now
    goal_data["updated_at"] = now
    result = await db["goals"].insert_one(goal_data)
    doc = await db["goals"].find_one({"_id": result.inserted_id})
    return serialize_doc(doc)


async def get_goals(db, user_id: str) -> List[dict]:
    docs = await db["goals"].find({"user_id": user_id}).sort("created_at", -1).to_list(length=1000)
    return [serialize_doc(doc) for doc in docs]


async def get_goal_by_id(db, goal_id: str, user_id: str) -> Optional[dict]:
    try:
        doc = await db["goals"].find_one({"_id": ObjectId(goal_id), "user_id": user_id})
    except Exception:
        return None
    return serialize_doc(doc) if doc else None


async def update_goal_progress(db, goal_id: str, user_id: str, amount_added: float) -> Optional[dict]:
    now = datetime.utcnow()
    progress_entry = {"date": now, "amount_added": amount_added}
    result = await db["goals"].update_one(
        {"_id": ObjectId(goal_id), "user_id": user_id},
        {
            "$inc": {"current_amount": amount_added},
            "$push": {"progress_log": progress_entry},
            "$set": {"updated_at": now},
        },
    )
    if result.matched_count == 0:
        return None
    doc = await db["goals"].find_one({"_id": ObjectId(goal_id)})
    return serialize_doc(doc)
