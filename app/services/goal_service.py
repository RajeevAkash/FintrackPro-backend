from fastapi import HTTPException, status

from app.db.repositories import goals_repo
from app.models.goal import GoalCreate, GoalProgressUpdate


async def list_goals(db, user_id: str) -> list:
    return await goals_repo.get_goals(db, user_id)


async def create_goal(db, user_id: str, data: GoalCreate) -> dict:
    goal_doc = {
        "user_id": user_id,
        "name": data.name,
        "target_amount": data.target_amount,
        "deadline": data.deadline,
    }
    return await goals_repo.create_goal(db, goal_doc)


async def update_goal_progress(db, goal_id: str, user_id: str, data: GoalProgressUpdate) -> dict:
    if data.amount_added <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="amount_added must be positive",
        )
    result = await goals_repo.update_goal_progress(db, goal_id, user_id, data.amount_added)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return result
