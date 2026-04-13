from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job


async def create_job(db: AsyncSession, company: str, role: str, user_id: int):
    job = Job(company=company, role=role, user_id=user_id)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_jobs(db: AsyncSession, user_id: int):
    result = await db.scalars(
        select(Job).where(Job.user_id == user_id)
    )
    return result.all()