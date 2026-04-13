from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import create_job, get_jobs
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("", response_model=JobResponse)
async def create_job_route(
    payload: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_job(
        db,
        payload.company,
        payload.role,
        current_user.id
    )


@router.get("", response_model=list[JobResponse])
async def get_jobs_route(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_jobs(db, current_user.id)