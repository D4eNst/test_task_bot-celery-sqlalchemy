from datetime import datetime

from sqlalchemy import String, DateTime, FetchedValue, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from repository.base import Base


class UserRequests(Base):  # type: ignore
    __tablename__ = "user_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=False)
    article: Mapped[int] = mapped_column(Integer, nullable=False, unique=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=now()
    )

    __mapper_args__ = {"eager_defaults": True}
