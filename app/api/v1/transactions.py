from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.transaction import TransactionCreate, TransactionResponse, TransactionUpdate, PaginatedTransactions
from app.services import transaction_service

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=PaginatedTransactions)
async def list_transactions(
    category: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await transaction_service.list_transactions(
        db,
        user_id=current_user["id"],
        category=category,
        transaction_type=type,
        from_date=from_date,
        to_date=to_date,
        page=page,
        limit=limit,
    )


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await transaction_service.create_transaction(db, user_id=current_user["id"], data=data)


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    data: TransactionUpdate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await transaction_service.update_transaction(
        db, transaction_id=transaction_id, user_id=current_user["id"], data=data
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
async def delete_transaction(
    transaction_id: str,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await transaction_service.delete_transaction(
        db, transaction_id=transaction_id, user_id=current_user["id"]
    )
