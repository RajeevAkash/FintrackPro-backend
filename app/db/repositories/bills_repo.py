from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from app.utils.bson_helpers import serialize_doc


async def create_bill(db, bill_data: dict) -> dict:
    bill_data["is_paid"] = False
    bill_data["paid_at"] = None
    bill_data["created_at"] = datetime.utcnow()
    result = await db["bills"].insert_one(bill_data)
    doc = await db["bills"].find_one({"_id": result.inserted_id})
    return serialize_doc(doc)


async def get_bills(
    db,
    user_id: str,
    is_paid: Optional[bool] = None,
    due_before: Optional[datetime] = None,
) -> List[dict]:
    query: dict = {"user_id": user_id}
    if is_paid is not None:
        query["is_paid"] = is_paid
    if due_before:
        query["due_date"] = {"$lte": due_before}
    docs = await db["bills"].find(query).sort("due_date", 1).to_list(length=1000)
    return [serialize_doc(doc) for doc in docs]


async def get_bill_by_id(db, bill_id: str, user_id: str) -> Optional[dict]:
    try:
        doc = await db["bills"].find_one({"_id": ObjectId(bill_id), "user_id": user_id})
    except Exception:
        return None
    return serialize_doc(doc) if doc else None


async def mark_bill_paid(db, bill_id: str, user_id: str) -> Optional[dict]:
    now = datetime.utcnow()
    result = await db["bills"].update_one(
        {"_id": ObjectId(bill_id), "user_id": user_id},
        {"$set": {"is_paid": True, "paid_at": now}},
    )
    if result.matched_count == 0:
        return None
    doc = await db["bills"].find_one({"_id": ObjectId(bill_id)})
    return serialize_doc(doc)
