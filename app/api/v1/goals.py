from typing import List

from fastapi import APIRouter, Depends, status

from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.goal import GoalCreate, GoalProgressUpdate, GoalResponse
from app.services import goal_service

router = APIRouter(prefix="/api/goals", tags=["goals"])


@router.get("", response_model=List[GoalResponse])
async def list_goals(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await goal_service.list_goals(db, user_id=current_user["id"])


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    data: GoalCreate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await goal_service.create_goal(db, user_id=current_user["id"], data=data)


@router.patch("/{goal_id}/progress", response_model=GoalResponse)
async def update_goal_progress(
    goal_id: str,
    data: GoalProgressUpdate,
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await goal_service.update_goal_progress(
        db, goal_id=goal_id, user_id=current_user["id"], data=data
    )
