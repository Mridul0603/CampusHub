import uuid
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, field_validator
from app.models.placement import ApplicationStage


# ── Request Schemas ──────────────────────────────────────────────────────────

class ApplicationCreate(BaseModel):
    company_name: str
    role: str
    stage: ApplicationStage = ApplicationStage.applied
    notes: str | None = None
    applied_on: date | None = None

    @field_validator("company_name", "role")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("This field cannot be empty")
        return v.strip()


class ApplicationUpdate(BaseModel):
    company_name: str | None = None
    role: str | None = None
    stage: ApplicationStage | None = None
    notes: str | None = None
    applied_on: date | None = None


# ── Response Schemas ─────────────────────────────────────────────────────────

class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_name: str
    role: str
    stage: ApplicationStage
    notes: str | None
    applied_on: date | None
    created_at: datetime
    updated_at: datetime


class StageStats(BaseModel):
    stage: str
    count: int


class PlacementStats(BaseModel):
    total: int
    offers: int
    rejections: int
    in_progress: int
    by_stage: list[StageStats]
