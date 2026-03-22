from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException, status

from app.db.repositories import transactions_repo
from app.models.transaction import TransactionCreate, TransactionUpdate
from app.utils.dates import date_to_datetime


async def list_transactions(
    db,
    user_id: str,
    category: Optional[str] = None,
    transaction_type: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    page: int = 1,
    limit: int = 20,
) -> dict:
    from_dt = date_to_datetime(from_date) if from_date else None
    to_dt = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59) if to_date else None
    return await transactions_repo.get_transactions(
        db,
        user_id=user_id,
        category=category,
        transaction_type=transaction_type,
        from_date=from_dt,
        to_date=to_dt,
        page=page,
        limit=limit,
    )


async def create_transaction(db, user_id: str, data: TransactionCreate) -> dict:
    transaction_doc = {
        "user_id": user_id,
        "amount": data.amount,
        "title": data.title,
        "type": data.type,
        "category": data.category,
        "payment_method": data.payment_method,
        "description": data.description,
        "receipt": data.receipt,
        "date": data.date,
    }
    return await transactions_repo.create_transaction(db, transaction_doc)


async def update_transaction(db, transaction_id: str, user_id: str, data: TransactionUpdate) -> dict:
    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    result = await transactions_repo.update_transaction(db, transaction_id, user_id, update_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return result


async def delete_transaction(db, transaction_id: str, user_id: str) -> dict:
    deleted = await transactions_repo.delete_transaction(db, transaction_id, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}
