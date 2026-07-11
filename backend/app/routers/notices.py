import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.notice import NoticeCategory
from app.services.notice_service import NoticeService
from app.schemas.notice import (
    NoticeCreate, NoticeUpdate, NoticeResponse, PaginatedNotices, SummaryResponse
)

router = APIRouter(prefix="/api/notices", tags=["Notices"])


@router.get("", response_model=PaginatedNotices)
def get_notices(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: NoticeCategory | None = Query(None),
    department: str | None = Query(None),
    semester: int | None = Query(None, ge=1, le=8),
    search: str | None = Query(None, min_length=1),
    sort: str = Query("created_at", pattern="^(created_at|title)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all notices with search, filter, sort, and pagination."""
    return NoticeService(db).get_all(
        page=page, limit=limit, category=category,
        department=department, semester=semester,
        search=search, sort=sort, order=order,
    )


@router.get("/{notice_id}", response_model=NoticeResponse)
def get_notice(
    notice_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NoticeService(db).get_by_id(notice_id)


@router.post("", response_model=NoticeResponse, status_code=status.HTTP_201_CREATED)
def create_notice(
    data: NoticeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.faculty, UserRole.admin)),
):
    """Only Faculty and Admin can create notices."""
    return NoticeService(db).create(data, current_user)


@router.put("/{notice_id}", response_model=NoticeResponse)
def update_notice(
    notice_id: uuid.UUID,
    data: NoticeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return NoticeService(db).update(notice_id, data, current_user)


@router.delete("/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notice(
    notice_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    NoticeService(db).delete(notice_id, current_user)


@router.post("/{notice_id}/summarize", response_model=SummaryResponse)
def summarize_notice(
    notice_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Summarize a notice using OpenAI. Available to all authenticated users."""
    summary = NoticeService(db).summarize(notice_id)
    return SummaryResponse(summary=summary)
