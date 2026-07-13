from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    company: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    
    location: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    salary: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    
    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    
    url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )
    
    status: Mapped[str] = mapped_column(
        String(30),
        default="new",
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )