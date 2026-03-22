from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.core.security import get_current_user
from app.services import classifier_service, tips_service
from pydantic import BaseModel


class ClassifyRequest(BaseModel):
    title: str
    description: str = ""


router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/classify")
async def classify_transaction(
    data: ClassifyRequest,
    current_user: dict = Depends(get_current_user),
):
    predicted_category = classifier_service.predict_category(data.title, data.description)
    return {"predicted_category": predicted_category}


@router.get("/tips")
async def get_tips(
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    return await tips_service.generate_tips(db, user_id=current_user["id"])
