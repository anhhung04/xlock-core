from enum import Enum

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SessionType(Enum):
    NEW = "new"
    ACTIVE = "active"
    LEAVE = "leave"


class Status(Enum):
    SUCCESS = "success"
    FAILED = "failed"
