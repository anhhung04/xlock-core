from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from repository import Storage

from utils.log import logger


class DemoRepo:
    def __init__(self, session: Session = Depends(Storage.get_db)):
        self._sess = session

    def demo(self):
        logger.info("Demo repository")
        return self._sess.execute(text("SELECT 1"))
