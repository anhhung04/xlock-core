from fastapi import Depends
from sqlalchemy.sql import text
from repository import Storage
from sqlalchemy.orm import Session
from redis import Redis

from utils.log import logger

class DemoRepo:
    def __init__(self, init_storage: Storage = Depends(Storage)):
        self._db: Session = init_storage._db
        self._fstore: Redis = init_storage._fstore

    async def demo(self):
        logger.info("Demo repository")
        return self._db.execute(text("SELECT 1"))
