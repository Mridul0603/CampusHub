from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import (
    RegisterRequest,
    LoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
    MessageResponse,
)
from app.dependencies import get_current_user
from app.models.user import User
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user account."""
    service = AuthService(db)
    user = service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """
    Authenticate and receive a JWT set as an httpOnly cookie.
    The token is also returned in the body for API clients.
    """
    service = AuthService(db)
    token, user = service.login(data)

    # Set JWT as httpOnly cookie — inaccessible to JavaScript (XSS safe)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=not settings.DEBUG,   # HTTPS-only in production
        samesite="lax",              # CSRF protection
        max_age=60 * 60 * 24,        # 24 hours
    )

    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post("/logout", response_model=MessageResponse)
def logout(response: Response, _: User = Depends(get_current_user)):
    """Clear the auth cookie, effectively logging the user out."""
    response.delete_cookie("access_token")
    return MessageResponse(message="Logged out successfully")


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Send a password reset email.
    Always returns 200 — we don't reveal whether the email exists.
    """
    AuthService(db).forgot_password(data)
    return MessageResponse(
        message="If an account exists with this email, a reset link has been sent"
    )


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset the user's password using the token from the email."""
    AuthService(db).reset_password(data)
    return MessageResponse(message="Password reset successfully. Please log in.")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return current_user
