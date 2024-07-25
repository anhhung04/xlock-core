from repository.schemas import Base
from repository.schemas.item import Item

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, Enum as DBEnum

from typing import Optional, List

from uuid import UUID, uuid4

from datetime import datetime, timezone

from enum import Enum


class Status(Enum):
    SUCCESS = "seccessful"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    registered_time: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc)
    )
    updated_time: Mapped[Optional[datetime]] = mapped_column()
    key: Mapped["CryptoKey"] = relationship(back_populates="user")
    sessions: Mapped[List["SessionInfo"]] = relationship()
    items: Mapped[List["Item"]] = relationship()


class CryptoKey(Base):
    __tablename__ = "crypto_keys"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    private_key: Mapped[str] = mapped_column()
    public_key: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="key", single_parent=True)

    __table_args__ = (UniqueConstraint("user_id"),)


class SessionInfo(Base):
    __table__ = "session_infos"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    location: Mapped[str] = mapped_column()
    ip: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(DBEnum(Status))
    device_info: Mapped[str] = mapped_column()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
