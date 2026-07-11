import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from app.models.notice import NoticeCategory


# ── Request Schemas ──────────────────────────────────────────────────────────

class NoticeCreate(BaseModel):
    title: str
    content: str
    category: NoticeCategory = NoticeCategory.general
    department: str | None = None
    semester: int | None = None
    expires_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        if len(v) > 255:
            raise ValueError("Title must be under 255 characters")
        return v.strip()

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()

    @field_validator("semester")
    @classmethod
    def valid_semester(cls, v: int | None) -> int | None:
        if v is not None and not (1 <= v <= 8):
            raise ValueError("Semester must be between 1 and 8")
        return v


class NoticeUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category: NoticeCategory | None = None
    department: str | None = None
    semester: int | None = None
    expires_at: datetime | None = None
    is_active: bool | None = None


# ── Response Schemas ─────────────────────────────────────────────────────────

class AuthorInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    full_name: str
    role: str


class NoticeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    content: str
    category: NoticeCategory
    department: str | None
    semester: int | None
    is_active: bool
    expires_at: datetime | None
    created_at: datetime
    updated_at: datetime
    author: AuthorInfo


class PaginatedNotices(BaseModel):
    items: list[NoticeResponse]
    total: int
    page: int
    limit: int
    pages: int


class SummaryResponse(BaseModel):
    summary: str
