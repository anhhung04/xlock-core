import redis
from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

engine = create_engine(config["POSTGRES_SQL_URL"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

redis_pool: redis.ConnectionPool = redis.ConnectionPool(
    host=config["REDIS_HOST"],
    port=int(config["REDIS_PORT"]),
    max_connections=config["MAX_CONNECTIONS_REDIS"],
    db=0,
)


class BaseRepository:
    def __init__(self):
        self.db = None
        self.redis = None

    def get_db(self):
        if self.db is None:
            self.db = SessionLocal()
        return self.db

    def get_redis(self):
        if self.redis is None:
            self.redis = redis.Redis(connection_pool=redis_pool)
        return self.redis

    def close_db(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def close_redis(self):
        if self.redis is not None:
            self.redis.close()
            self.redis = None

    def __enter__(self):
        self.db = self.get_db()
        self.redis = self.get_redis()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_db()
        self.close_redis()
        if exc_type is not None:
            raise HTTPException(status_code=500, detail=str(exc_val))
