import json
from fastapi.testclient import TestClient
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from repository.schemas import Base
from repository import Storage, RedisStorage
from app import app
import requests

USER_DB = json.loads(open("./tests/data.json", errors="replace").read())

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

redis_cache = {}


class RedisLocal:
    def set(self, key, value, ex):
        redis_cache[key] = value

    def delete(self, key):
        if key in redis_cache:
            redis_cache.pop(key)

    def get(self, key):
        return redis_cache.get(key, None)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_redis():
    try:
        yield RedisLocal()
    finally:
        pass


app.dependency_overrides[RedisStorage.get] = override_get_redis
app.dependency_overrides[Storage.get] = override_get_db

client = TestClient(app)
