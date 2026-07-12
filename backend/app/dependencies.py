from fastapi import Depends, HTTPException, status, Cookie, Request
from sqlalchemy.orm import Session
from jose import JWTError
import uuid

from app.database import get_db
from app.utils.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserRole


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    """
    Auth dependency. Reads JWT from:
    1. httpOnly cookie (preferred)
    2. Authorization: Bearer header (fallback for cross-origin)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )

    # Try cookie first
    token = request.cookies.get("access_token")

    # Fallback to Authorization header
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise credentials_exception

    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = UserRepository(db).get_by_id(uuid.UUID(user_id))
    if not user or not user.is_active:
        raise credentials_exception

    return user


def require_roles(*roles: UserRole):
    def _check(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in roles]}",
            )
        return current_user
    return _check
