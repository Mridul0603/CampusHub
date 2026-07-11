import uuid
import math
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.notice_repository import NoticeRepository
from app.schemas.notice import NoticeCreate, NoticeUpdate, PaginatedNotices
from app.models.notice import Notice, NoticeCategory
from app.models.user import User, UserRole
from app.utils.openai_service import summarize_notice


class NoticeService:
    def __init__(self, db: Session):
        self.repo = NoticeRepository(db)

    def get_all(
        self,
        page: int,
        limit: int,
        category: NoticeCategory | None,
        department: str | None,
        semester: int | None,
        search: str | None,
        sort: str,
        order: str,
    ) -> PaginatedNotices:
        items, total = self.repo.get_all(
            page=page, limit=limit, category=category,
            department=department, semester=semester,
            search=search, sort=sort, order=order,
        )
        return PaginatedNotices(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=math.ceil(total / limit) if total > 0 else 0,
        )

    def get_by_id(self, notice_id: uuid.UUID) -> Notice:
        notice = self.repo.get_by_id(notice_id)
        if not notice:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notice not found")
        return notice

    def create(self, data: NoticeCreate, current_user: User) -> Notice:
        return self.repo.create(
            author_id=current_user.id,
            title=data.title,
            content=data.content,
            category=data.category,
            department=data.department,
            semester=data.semester,
            expires_at=data.expires_at,
        )

    def update(self, notice_id: uuid.UUID, data: NoticeUpdate, current_user: User) -> Notice:
        notice = self.get_by_id(notice_id)
        self._check_ownership(notice, current_user)

        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(notice, **update_data)

    def delete(self, notice_id: uuid.UUID, current_user: User) -> None:
        notice = self.get_by_id(notice_id)
        self._check_ownership(notice, current_user)
        self.repo.delete(notice)

    def summarize(self, notice_id: uuid.UUID) -> str:
        notice = self.get_by_id(notice_id)
        try:
            return summarize_notice(notice.title, notice.content)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Summarization service is currently unavailable. Please try again later.",
            )

    def _check_ownership(self, notice: Notice, current_user: User) -> None:
        """Author or Admin can modify/delete. Anyone else gets 403."""
        if notice.author_id != current_user.id and current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to modify this notice",
            )
