from fastapi import APIRouter, Depends, status

from app.api.deps import get_db
from app.core.security import get_current_user
from app.models.user import UserLogin, UserRegister, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db=Depends(get_db)):
    return await auth_service.register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db=Depends(get_db)):
    return await auth_service.login_user(db, login_data)
