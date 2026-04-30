from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import create_user
from app.schemas.auth import LoginRequest
from app.core.security import create_access_token
from app.services.auth_service import authenticate_user
from app.api.deps import get_current_user
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/signup")
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        user = create_user(
            db,
            user_data
        )

        return {
            "message": "User created successfully",
            "user_id": user.id
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {"sub": user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
