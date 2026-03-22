from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ProgressEntry(BaseModel):
    date: datetime
    amount_added: float


class GoalCreate(BaseModel):
    name: str
    target_amount: float
    deadline: datetime


class GoalProgressUpdate(BaseModel):
    amount_added: float


class GoalResponse(BaseModel):
    id: str
    user_id: str
    name: str
    target_amount: float
    current_amount: float
    deadline: datetime
    progress_log: List[ProgressEntry] = []
    created_at: datetime
    updated_at: datetime
