from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.analytics import MonthlySummary, CategoriesResponse, BudgetStatus, ForecastResponse
from app.services import analytics_service
from app.services import forecast_service

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary", response_model=MonthlySummary)
async def get_summary(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await analytics_service.get_monthly_summary(db, user_id=current_user["id"])


@router.get("/categories", response_model=CategoriesResponse)
async def get_categories(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await analytics_service.get_category_breakdown(db, user_id=current_user["id"])


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await forecast_service.get_forecast(db, user_id=current_user["id"])


@router.get("/status", response_model=BudgetStatus)
async def get_status(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await analytics_service.get_budget_status(db, user_id=current_user["id"])
