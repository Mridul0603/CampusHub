import uuid
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.notice import Notice, NoticeCategory


class NoticeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, notice_id: uuid.UUID) -> Notice | None:
        return (
            self.db.query(Notice)
            .filter(Notice.id == notice_id, Notice.is_active == True)
            .first()
        )

    def get_all(
        self,
        page: int = 1,
        limit: int = 20,
        category: NoticeCategory | None = None,
        department: str | None = None,
        semester: int | None = None,
        search: str | None = None,
        sort: str = "created_at",
        order: str = "desc",
    ) -> tuple[list[Notice], int]:
        query = self.db.query(Notice).filter(Notice.is_active == True)

        # Filtering
        if category:
            query = query.filter(Notice.category == category)
        if department:
            query = query.filter(
                or_(Notice.department == department, Notice.department == None)
            )
        if semester:
            query = query.filter(
                or_(Notice.semester == semester, Notice.semester == None)
            )

        # Search — ILIKE is case-insensitive LIKE in PostgreSQL
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Notice.title.ilike(pattern),
                    Notice.content.ilike(pattern),
                )
            )

        # Sorting
        sort_col = getattr(Notice, sort, Notice.created_at)
        if order == "asc":
            query = query.order_by(sort_col.asc())
        else:
            query = query.order_by(sort_col.desc())

        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return items, total

    def create(self, author_id: uuid.UUID, **kwargs) -> Notice:
        notice = Notice(author_id=author_id, **kwargs)
        self.db.add(notice)
        self.db.commit()
        self.db.refresh(notice)
        return notice

    def update(self, notice: Notice, **kwargs) -> Notice:
        for key, value in kwargs.items():
            setattr(notice, key, value)
        self.db.commit()
        self.db.refresh(notice)
        return notice

    def delete(self, notice: Notice) -> None:
        # Soft delete — set is_active to False
        notice.is_active = False
        self.db.commit()
