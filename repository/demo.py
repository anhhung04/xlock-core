from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from repository import Storage


class DemoRepo:
    def __init__(self, session: Session = Depends(Storage.get)):
        self._sess = session

    def demo(self):
        print("DemoRepo")
        return self._sess.execute(text("SELECT 1"))
