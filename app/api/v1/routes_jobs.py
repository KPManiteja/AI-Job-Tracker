from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.job import JobCreate, JobUpdate, JobResponse
from app.services.job_service import (
    create_job,
    get_jobs,
    update_job,
    delete_job
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("", response_model=JobResponse)
async def create_job_route(
    payload: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_job(db, payload.company, payload.role, current_user.id)


@router.get("", response_model=list[JobResponse])
async def get_jobs_route(
    status: str | None = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await get_jobs(
        db,
        current_user.id,
        status,
        skip,
        limit
    )


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job_route(
    job_id: int,
    payload: JobUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        job = await update_job(
            db,
            job_id,
            current_user.id,
            payload.model_dump(exclude_unset=True)
        )
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{job_id}")
async def delete_job_route(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = await delete_job(db, job_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}