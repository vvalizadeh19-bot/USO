"""FastAPI dependencies: authentication and RBAC authorization (§7.1–7.6)."""
from __future__ import annotations

from collections.abc import Iterable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")

_CREDENTIALS_EXC = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise _CREDENTIALS_EXC
    username = payload.get("sub")
    if not username:
        raise _CREDENTIALS_EXC
    user = db.query(User).filter(User.username == username, User.is_active.is_(True)).one_or_none()
    if user is None or user.is_deleted:
        raise _CREDENTIALS_EXC
    return user


def require_roles(*allowed: str):
    """Dependency factory: allow only users holding one of ``allowed`` roles."""

    def _checker(user: User = Depends(get_current_user)) -> User:
        if not (set(allowed) & user.role_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this operation",
            )
        return user

    return _checker


def has_any_role(user: User, roles: Iterable[str]) -> bool:
    return bool(set(roles) & user.role_names)
