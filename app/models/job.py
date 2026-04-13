from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    company: Mapped[str] = mapped_column(String(255), index=True)
    role: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(100), default="APPLIED")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user = relationship("User", back_populates="jobs")