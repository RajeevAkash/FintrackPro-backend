from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BillCreate(BaseModel):
    name: str
    amount: float
    due_date: datetime
    recurrence: str  # "monthly" | "one-time"


class BillResponse(BaseModel):
    id: str
    user_id: str
    name: str
    amount: float
    due_date: datetime
    recurrence: str
    is_paid: bool
    paid_at: Optional[datetime] = None
    created_at: datetime
