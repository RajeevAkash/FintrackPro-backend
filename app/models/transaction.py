from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    amount: float
    title: str
    type: str  # "income" | "expense"
    category: Optional[str] = None
    payment_method: str
    description: Optional[str] = None
    receipt: Optional[str] = None  # base64 encoded image
    date: datetime


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    title: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None
    receipt: Optional[str] = None
    date: Optional[datetime] = None


class TransactionResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    title: str
    type: str
    category: Optional[str] = None
    payment_method: str
    description: Optional[str] = None
    receipt: Optional[str] = None
    date: datetime
    created_at: datetime
    updated_at: datetime


class PaginatedTransactions(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    page: int
    limit: int
