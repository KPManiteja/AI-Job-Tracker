from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job
from app.core.constants import VALID_JOB_STATUSES


async def create_job(db: AsyncSession, company: str, role: str, user_id: int):
    job = Job(company=company, role=role, user_id=user_id)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_jobs(
    db: AsyncSession,
    user_id: int,
    status: str | None = None,
    skip: int = 0,
    limit: int = 10
):
    query = select(Job).where(Job.user_id == user_id)

    if status:
        query = query.where(Job.status == status)

    query = query.offset(skip).limit(limit)

    result = await db.scalars(query)
    return result.all()


async def update_job(
    db: AsyncSession,
    job_id: int,
    user_id: int,
    updates: dict
):
    job = await db.scalar(
        select(Job).where(
            Job.id == job_id,
            Job.user_id == user_id
        )
    )

    if not job:
        return None

    if "status" in updates:
        if updates["status"] not in VALID_JOB_STATUSES:
            raise ValueError("Invalid status")

    for key, value in updates.items():
        if value is not None:
            setattr(job, key, value)

    await db.commit()
    await db.refresh(job)
    return job


async def delete_job(db: AsyncSession, job_id: int, user_id: int):
    job = await db.scalar(
        select(Job).where(
            Job.id == job_id,
            Job.user_id == user_id
        )
    )

    if not job:
        return False

    await db.delete(job)
    await db.commit()
    return True