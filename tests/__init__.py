import random
import string
from datetime import datetime, timezone
from unittest import TestCase
from uuid import uuid4

import requests
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import app
from repository import Storage
from repository.schemas import Base
from repository.schemas.item import Item
from repository.schemas.user import User

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.create_all(bind=engine)

redis_cache = {}


class RedisLocal:
    def set(self, key, value):
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


def override_get_store():
    try:
        yield RedisLocal()
    finally:
        pass


app.dependency_overrides[Storage.get_db] = override_get_db
app.dependency_overrides[Storage.get_store] = override_get_store


client = TestClient(app)


class TestIntegration(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._s = requests.session()
        self._base = "http://localhost:8000/api"
        self._route = None
        self._access_token = self._s.post(
            self._base + "/auth/login",
            json={"username": "mhung", "password": "hung"},
        ).json()["data"]["access_token"]
        self._s.headers = {"Authorization": f"Bearer {self._access_token}"}

    def path(self, path):
        return self._base + self._route + path


class CredentialGenerator:
    def __init__(self, length=10):
        self.length = length

    def gen_username(self):
        return "".join(random.choices(string.ascii_lowercase, k=self.length))

    def gen_password(self):
        return "".join(random.choices(string.ascii_lowercase, k=self.length))


def create_user(name=None, email=None, password=None):
    u = name or CredentialGenerator.gen_username()
    p = password or CredentialGenerator.gen_password()
    id = uuid4()
    user = User(
        id=id,
        name=u,
        email=email or f"{u}@example.com",
        password=p,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
    )
    return user


def insert_user(db, name=None, email=None, password=None):
    user = create_user(name, email, password)
    db.add(user)
    db.commit()
    return user


def insert_items(
    db, owner_id, name, site, credentials, logo_url=None, description=None
):
    item = Item(
        id=uuid4(),
        name=name,
        site=site,
        logo_url=logo_url,
        description=description,
        credentials=credentials,
        added_at=datetime.now(),
        updated_at=None,
        owner_id=owner_id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
