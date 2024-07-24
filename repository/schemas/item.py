from repository.schemas import Base
from repository.schemas.user import Status

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, Enum as DBEnum

from typing import Optional

from uuid import UUID

from datetime import datetime, timezone

from enum import Enum


class ItemType(Enum):
    PERSONAL = "Personal"
    SHARED = "Shared"


class ActionType(Enum):
    FILL = "Fill"
    SHARE = "Share"


class Item(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    logo: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    type = mapped_column(DBEnum(ItemType))
    credentials: Mapped[str] = mapped_column()
    added_time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    last_modified_time: Mapped[Optional[datetime]] = mapped_column()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    histories: Mapped["ItemHistory"] = relationship()


class PersonalItem(Base):
    __tablename__ = "personal_items"

    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"), primary_key=True)
    item_info: Mapped["Item"] = relationship(
        primaryjoin="Item.id==PersonalItem.item_id",
        uselist=False,
    )

    __table_args__ = (UniqueConstraint("item_id"),)


class SharedItem(Base):
    __tablename__ = "shared_items"

    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"), primary_key=True)
    private_key: Mapped[str] = mapped_column()
    shared_time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    item_info: Mapped["Item"] = relationship(
        primaryjoin="Item.id==SharedItem.item_id",
        uselist=False,
    )


class ItemHistory(Base):
    __tablename__ = "item_histories"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(DBEnum(ActionType))
    time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    location: Mapped[str] = mapped_column()
    ip: Mapped[str] = mapped_column()
    device_info: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(DBEnum(Status))
    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"))


class SharingHistory(Base):
    __tablename__ = "sharing_histories"

    history_id: Mapped[UUID] = mapped_column(
        ForeignKey("item_histories.id"), primary_key=True
    )
    recipient_name: Mapped[str] = mapped_column()
    recipient_email: Mapped[str] = mapped_column()
    detail: Mapped["ItemHistory"] = relationship(
        primaryjoin="ItemHistory.id==SharingHistory.history_id",
        uselist=False,
    )


class FillingHistory(Base):
    __tablename__ = "filling_histories"

    history_id: Mapped[UUID] = mapped_column(
        ForeignKey("item_histories.id"), primary_key=True
    )
    detail: Mapped["ItemHistory"] = relationship(
        primaryjoin="ItemHistory.id==FillingHistory.history_id",
        uselist=False,
    )
