from fastapi import APIRouter, HTTPException, status
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    if body.password != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    token = create_access_token({"sub": "admin"})
    return TokenResponse(access_token=token)


@router.get("/me")
def me(credentials=None):
    return {"role": "admin"}
