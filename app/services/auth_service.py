from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


async def register_user(db: AsyncSession, email: str, password: str):
    existing = await db.scalar(select(User).where(User.email == email))
    if existing:
        raise ValueError("User already exists")

    user = User(
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login_user(db: AsyncSession, email: str, password: str):
    user = await db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")

    token = create_access_token({"sub": user.email})
    return token