from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.repositories.user_repository import UserRepository
from app.schemas.user import RegisterRequest, LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_reset_token,
    hash_reset_token,
    reset_token_expiry,
)
from app.utils.email import send_password_reset_email
from app.models.user import User


class AuthService:
    """
    Business logic for authentication.
    The repository handles DB. This layer handles decisions.
    """

    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: RegisterRequest) -> User:
        # 1. Check email not already taken
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

        # 2. Hash password and create user
        user = self.repo.create(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
            department=data.department,
            semester=data.semester,
            phone=data.phone,
        )
        return user

    def login(self, data: LoginRequest) -> tuple[str, User]:
        # 1. Find user
        user = self.repo.get_by_email(data.email)

        # 2. Verify credentials — same error for wrong email OR wrong password
        #    (prevents user enumeration attacks)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # 3. Check account is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been deactivated. Contact admin.",
            )

        # 4. Generate JWT with user ID and role in payload
        token = create_access_token({"sub": str(user.id), "role": user.role})
        return token, user

    def forgot_password(self, data: ForgotPasswordRequest) -> None:
        user = self.repo.get_by_email(data.email)

        # Always return success — don't leak whether the email exists
        if not user:
            return

        raw_token, token_hash = generate_reset_token()
        self.repo.update(
            user,
            reset_token_hash=token_hash,
            reset_token_expires_at=reset_token_expiry(),
        )
        send_password_reset_email(user.email, raw_token, user.full_name)

    def reset_password(self, data: ResetPasswordRequest) -> None:
        token_hash = hash_reset_token(data.token)
        user = self.repo.get_by_reset_token_hash(token_hash)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        self.repo.update(
            user,
            password_hash=hash_password(data.new_password),
            reset_token_hash=None,
            reset_token_expires_at=None,
        )
