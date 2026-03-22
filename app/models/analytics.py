from typing import List, Optional

from pydantic import BaseModel


class MonthlySummary(BaseModel):
    current_month_income: float
    current_month_expense: float
    balance: float


class CategoryBreakdown(BaseModel):
    category: str
    amount: float
    percentage: float


class CategoriesResponse(BaseModel):
    categories: List[CategoryBreakdown]
    total_expense: float


class BudgetStatus(BaseModel):
    budget_status: str
    risk_level: str
    predicted_month_end_spending: float
    current_spending: float
    current_income: float
    days_elapsed: int
    days_remaining: int
    average_daily_spending: float


class ForecastResponse(BaseModel):
    labels: List[str]
    actual: List[Optional[float]]
    forecast: List[Optional[float]]
    message: Optional[str] = None
