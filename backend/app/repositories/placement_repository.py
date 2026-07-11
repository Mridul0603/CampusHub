import uuid
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.placement import PlacementRecord, ApplicationStage


class PlacementRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_for_student(
        self,
        student_id: uuid.UUID,
        stage: ApplicationStage | None = None,
        search: str | None = None,
    ) -> list[PlacementRecord]:
        query = self.db.query(PlacementRecord).filter(
            PlacementRecord.student_id == student_id
        )
        if stage:
            query = query.filter(PlacementRecord.stage == stage)
        if search:
            pattern = f"%{search}%"
            query = query.filter(PlacementRecord.company_name.ilike(pattern))
        return query.order_by(PlacementRecord.created_at.desc()).all()

    def get_by_id(self, record_id: uuid.UUID) -> PlacementRecord | None:
        return self.db.query(PlacementRecord).filter(PlacementRecord.id == record_id).first()

    def get_stats(self, student_id: uuid.UUID) -> dict:
        """
        Single DB query to get counts grouped by stage.
        Push aggregation to PostgreSQL — don't load all rows into Python.
        """
        results = (
            self.db.query(PlacementRecord.stage, func.count(PlacementRecord.id))
            .filter(PlacementRecord.student_id == student_id)
            .group_by(PlacementRecord.stage)
            .all()
        )
        return {stage.value: count for stage, count in results}

    def create(self, student_id: uuid.UUID, **kwargs) -> PlacementRecord:
        record = PlacementRecord(student_id=student_id, **kwargs)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update(self, record: PlacementRecord, **kwargs) -> PlacementRecord:
        for key, value in kwargs.items():
            setattr(record, key, value)
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, record: PlacementRecord) -> None:
        self.db.delete(record)
        self.db.commit()
