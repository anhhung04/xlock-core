from sqlalchemy.ext.declarative import declarative_base

from enum import Enum

Base = declarative_base()


class Status(Enum):
    SUCCESS = "seccessful"
    FAILED = "failed"
