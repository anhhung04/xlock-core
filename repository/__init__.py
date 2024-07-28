import redis
from fastapi import Depends, HTTPException
from redis import ConnectionPool, Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import config

engine = create_engine(config["POSTGRES_SQL_URL"])
redis_pool: ConnectionPool = ConnectionPool(
    host=config["REDIS_HOST"],
    port=int(config["REDIS_PORT"]),
    max_connections=config["MAX_CONNECTIONS_REDIS"],
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_store():
    redis = Redis(connection_pool=redis_pool)
    try:
        yield redis
    finally:
        redis.close()


class Storage:

    def __init__(
        self, db: Session = Depends(get_db), redis: Redis = Depends(get_store)
    ):
        self._fstore: Redis = redis
        self._db: Session = db

    def get(self):
        return self._db, self._fstore


class RedisStorage:
    @staticmethod
    def get():
        r = redis.Redis(connection_pool=redis_pool)
        try:
            yield r
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            pass
