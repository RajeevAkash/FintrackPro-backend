from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.bill import BillCreate, BillResponse
from app.services import bill_service

router = APIRouter(prefix="/api/bills", tags=["bills"])


@router.get("", response_model=List[BillResponse])
async def list_bills(
    is_paid: Optional[bool] = Query(None),
    due_before: Optional[date] = Query(None),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await bill_service.list_bills(
        db, user_id=current_user["id"], is_paid=is_paid, due_before=due_before
    )


@router.post("", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
async def create_bill(
    data: BillCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await bill_service.create_bill(db, user_id=current_user["id"], data=data)


@router.patch("/{bill_id}/pay", response_model=BillResponse)
async def pay_bill(
    bill_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await bill_service.pay_bill(db, bill_id=bill_id, user_id=current_user["id"])
