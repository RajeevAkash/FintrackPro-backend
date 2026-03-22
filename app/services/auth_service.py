from datetime import timedelta
from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password, create_access_token
from app.db.repositories import users_repo
from app.models.user import UserRegister, UserLogin, UserResponse, TokenResponse


async def register_user(db, user_data: UserRegister) -> TokenResponse:
    existing = await users_repo.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed = hash_password(user_data.password)
    user_doc = {
        "email": user_data.email,
        "full_name": user_data.full_name,
        "age": user_data.age,
        "occupation": user_data.occupation,
        "password_hash": hashed,
    }
    created_user = await users_repo.create_user(db, user_doc)
    token = create_access_token({"sub": created_user["id"]})
    user_response = UserResponse(
        id=created_user["id"],
        email=created_user["email"],
        full_name=created_user["full_name"],
        age=created_user["age"],
        occupation=created_user["occupation"],
        created_at=created_user["created_at"],
    )
    return TokenResponse(access_token=token, token_type="bearer", user=user_response)


async def login_user(db, login_data: UserLogin) -> TokenResponse:
    user = await users_repo.get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    token = create_access_token({"sub": user["id"]})
    user_response = UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        age=user["age"],
        occupation=user["occupation"],
        created_at=user["created_at"],
    )
    return TokenResponse(access_token=token, token_type="bearer", user=user_response)
