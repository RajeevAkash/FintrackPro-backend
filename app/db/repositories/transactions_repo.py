from datetime import datetime
from typing import List, Optional

from bson import ObjectId

from app.utils.bson_helpers import serialize_doc


async def create_transaction(db, transaction_data: dict) -> dict:
    now = datetime.utcnow()
    transaction_data["created_at"] = now
    transaction_data["updated_at"] = now
    result = await db["transactions"].insert_one(transaction_data)
    doc = await db["transactions"].find_one({"_id": result.inserted_id})
    return serialize_doc(doc)


async def get_transactions(
    db,
    user_id: str,
    category: Optional[str] = None,
    transaction_type: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    page: int = 1,
    limit: int = 20,
) -> dict:
    query: dict = {"user_id": user_id}
    if category:
        query["category"] = category
    if transaction_type:
        query["type"] = transaction_type
    if from_date or to_date:
        query["date"] = {}
        if from_date:
            query["date"]["$gte"] = from_date
        if to_date:
            query["date"]["$lte"] = to_date

    total = await db["transactions"].count_documents(query)
    skip = (page - 1) * limit
    docs = await db["transactions"].find(query).sort("date", -1).skip(skip).to_list(length=limit)
    transactions = [serialize_doc(doc) for doc in docs]
    return {"transactions": transactions, "total": total, "page": page, "limit": limit}


async def get_transaction_by_id(db, transaction_id: str, user_id: str) -> Optional[dict]:
    try:
        doc = await db["transactions"].find_one(
            {"_id": ObjectId(transaction_id), "user_id": user_id}
        )
    except Exception:
        return None
    return serialize_doc(doc) if doc else None


async def update_transaction(db, transaction_id: str, user_id: str, update_data: dict) -> Optional[dict]:
    update_data["updated_at"] = datetime.utcnow()
    result = await db["transactions"].update_one(
        {"_id": ObjectId(transaction_id), "user_id": user_id},
        {"$set": update_data},
    )
    if result.matched_count == 0:
        return None
    doc = await db["transactions"].find_one({"_id": ObjectId(transaction_id)})
    return serialize_doc(doc)


async def delete_transaction(db, transaction_id: str, user_id: str) -> bool:
    result = await db["transactions"].delete_one(
        {"_id": ObjectId(transaction_id), "user_id": user_id}
    )
    return result.deleted_count > 0


async def get_transactions_by_query(db, query: dict) -> List[dict]:
    docs = await db["transactions"].find(query).to_list(length=10000)
    return [serialize_doc(doc) for doc in docs]
