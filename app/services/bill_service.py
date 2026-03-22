from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException, status

from app.db.repositories import bills_repo
from app.models.bill import BillCreate
from app.utils.dates import date_to_datetime


async def list_bills(
    db,
    user_id: str,
    is_paid: Optional[bool] = None,
    due_before: Optional[date] = None,
) -> list:
    due_before_dt = date_to_datetime(due_before) if due_before else None
    return await bills_repo.get_bills(db, user_id=user_id, is_paid=is_paid, due_before=due_before_dt)


async def create_bill(db, user_id: str, data: BillCreate) -> dict:
    bill_doc = {
        "user_id": user_id,
        "name": data.name,
        "amount": data.amount,
        "due_date": data.due_date,
        "recurrence": data.recurrence,
    }
    return await bills_repo.create_bill(db, bill_doc)


async def pay_bill(db, bill_id: str, user_id: str) -> dict:
    result = await bills_repo.mark_bill_paid(db, bill_id, user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")
    return result
