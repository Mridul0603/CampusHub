import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    """
    All DB queries related to users live here.
    No business logic — just data access.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_reset_token_hash(self, token_hash: str) -> User | None:
        return (
            self.db.query(User)
            .filter(
                User.reset_token_hash == token_hash,
                User.reset_token_expires_at > datetime.utcnow(),
            )
            .first()
        )

    def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
