from enum import Enum

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Status(Enum):
    SUCCESS = "successful"
    FAILED = "failed"
