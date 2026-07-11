import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.placement_repository import PlacementRepository
from app.schemas.placement import ApplicationCreate, ApplicationUpdate, PlacementStats, StageStats
from app.models.placement import PlacementRecord, ApplicationStage
from app.models.user import User


class PlacementService:
    def __init__(self, db: Session):
        self.repo = PlacementRepository(db)

    def get_all(
        self,
        current_user: User,
        stage: ApplicationStage | None = None,
        search: str | None = None,
    ) -> list[PlacementRecord]:
        # Students only see their own data — enforced here
        return self.repo.get_all_for_student(current_user.id, stage, search)

    def get_by_id(self, record_id: uuid.UUID, current_user: User) -> PlacementRecord:
        record = self.repo.get_by_id(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Application not found")
        self._check_ownership(record, current_user)
        return record

    def create(self, data: ApplicationCreate, current_user: User) -> PlacementRecord:
        return self.repo.create(
            student_id=current_user.id,
            company_name=data.company_name,
            role=data.role,
            stage=data.stage,
            notes=data.notes,
            applied_on=data.applied_on,
        )

    def update(self, record_id: uuid.UUID, data: ApplicationUpdate, current_user: User) -> PlacementRecord:
        record = self.get_by_id(record_id, current_user)
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(record, **update_data)

    def delete(self, record_id: uuid.UUID, current_user: User) -> None:
        record = self.get_by_id(record_id, current_user)
        self.repo.delete(record)

    def get_stats(self, current_user: User) -> PlacementStats:
        stage_counts = self.repo.get_stats(current_user.id)

        total = sum(stage_counts.values())
        offers = stage_counts.get("offer", 0)
        rejections = stage_counts.get("rejected", 0)
        in_progress = total - offers - rejections

        by_stage = [
            StageStats(stage=stage, count=count)
            for stage, count in stage_counts.items()
        ]

        return PlacementStats(
            total=total,
            offers=offers,
            rejections=rejections,
            in_progress=in_progress,
            by_stage=by_stage,
        )

    def _check_ownership(self, record: PlacementRecord, current_user: User) -> None:
        if record.student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this record",
            )
