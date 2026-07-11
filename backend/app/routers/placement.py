import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.placement import ApplicationStage
from app.services.placement_service import PlacementService
from app.schemas.placement import (
    ApplicationCreate, ApplicationUpdate,
    ApplicationResponse, PlacementStats,
)

router = APIRouter(prefix="/api/placement", tags=["Placement Hub"])


@router.get("/applications", response_model=list[ApplicationResponse])
def get_applications(
    stage: ApplicationStage | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all placement applications for the logged-in student."""
    return PlacementService(db).get_all(current_user, stage, search)


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PlacementService(db).create(data, current_user)


@router.put("/applications/{record_id}", response_model=ApplicationResponse)
def update_application(
    record_id: uuid.UUID,
    data: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PlacementService(db).update(record_id, data, current_user)


@router.delete("/applications/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    record_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    PlacementService(db).delete(record_id, current_user)


@router.get("/stats", response_model=PlacementStats)
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Dashboard stats — total, offers, rejections, in-progress, by stage."""
    return PlacementService(db).get_stats(current_user)
