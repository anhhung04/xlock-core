from repository.schemas import Base
from repository.schemas.user import User

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from typing import Optional, List

from uuid import UUID

from datetime import datetime, timezone


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    created_time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_time: Mapped[Optional[datetime]] = mapped_column()
    member_counts: Mapped[int] = mapped_column()
    members: Mapped[List["UserInGroup"]] = relationship()


class UserInGroup(Base):
    __tablename__ = "users_in_groups"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[UUID] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    role: Mapped[str] = mapped_column()
    joined_time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    left_time: Mapped[Optional[datetime]] = mapped_column()
    user: Mapped["User"] = relationship()
