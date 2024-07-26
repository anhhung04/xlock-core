from repository.schemas import Base, Status

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, Enum as DBEnum

from typing import Optional, List

from uuid import UUID, uuid4

from datetime import datetime, timezone
from .user import *


class Item(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    site: Mapped[str] = mapped_column()
    logo_url: Mapped[Optional[str]] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()
    type: Mapped[str] = mapped_column()
    credentials: Mapped[str] = mapped_column()
    added_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=datetime.now(timezone.utc)
    )
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="items")
    histories: Mapped[List["ItemHistory"]] = relationship()

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "base_item",
    }


class PersonalItem(Item):
    __tablename__ = "personal_items"

    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "personal_item",
    }


class SharedItem(Item):
    __tablename__ = "shared_items"

    item_id: Mapped[UUID] = mapped_column(
        ForeignKey("items.id"), primary_key=True, default=UUID
    )
    private_key: Mapped[str] = mapped_column()
    shared_time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    __mapper_args__ = {
        "polymorphic_identity": "shared_item",
    }


class ItemHistory(Base):
    __tablename__ = "item_histories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    type: Mapped[str] = mapped_column()
    time: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    location: Mapped[str] = mapped_column()
    ip: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(DBEnum(Status))
    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"))

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "base_history",
    }


class SharingHistory(ItemHistory):
    __tablename__ = "sharing_histories"

    history_id: Mapped[UUID] = mapped_column(
        ForeignKey("item_histories.id"), primary_key=True
    )
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    recipient_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    __mapper_args__ = {
        "polymorphic_identity": "sharing_history",
    }


class FillingHistory(ItemHistory):
    __tablename__ = "filling_histories"

    history_id: Mapped[UUID] = mapped_column(
        ForeignKey("item_histories.id"), primary_key=True
    )

    __mapper_args__ = {
        "polymorphic_identity": "filling_history",
    }
