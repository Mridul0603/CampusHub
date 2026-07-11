from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from jose import JWTError
import uuid

from app.database import get_db
from app.utils.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserRole


def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    """
    Core auth dependency. Validates JWT from httpOnly cookie.
    Inject this into any route that requires authentication.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not access_token:
        raise credentials_exception

    try:
        payload = decode_access_token(access_token)
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
    """
    Factory that returns a dependency enforcing one of the given roles.

    Usage:
        @router.post("/admin-only")
        def admin_route(user = Depends(require_roles(UserRole.admin))):
            ...

        @router.post("/faculty-or-admin")
        def faculty_route(user = Depends(require_roles(UserRole.faculty, UserRole.admin))):
            ...
    """
    def _check(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in roles]}",
            )
        return current_user
    return _check
