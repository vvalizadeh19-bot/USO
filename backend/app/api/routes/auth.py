"""Authentication routes (§7.3): password login, token refresh, current user."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.user import User
from app.schemas import RefreshRequest, Token, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


def _tokens_for(user: User) -> Token:
    roles = sorted(user.role_names)
    return Token(
        access_token=create_access_token(user.username, roles),
        refresh_token=create_refresh_token(user.username),
    )


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = db.query(User).filter(User.username == form.username).one_or_none()
    if not user or user.is_deleted or not user.is_active or not verify_password(
        form.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return _tokens_for(user)


@router.post("/refresh", response_model=Token)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)) -> Token:
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")
    user = db.query(User).filter(User.username == payload.get("sub")).one_or_none()
    if not user or user.is_deleted or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")
    return _tokens_for(user)


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        roles=sorted(user.role_names),
        region=user.region,
        contractor_id=user.contractor_id,
    )
