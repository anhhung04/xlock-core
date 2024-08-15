from user_agents import parse
from user_agents.parsers import UserAgent
from fastapi import Cookie, Header, Request
from repository.schemas.user import User, SessionInfo, Device
from repository.schemas import SessionType
from fastapi import Depends, Cookie, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from repository import Storage
from typing import Annotated
from utils.http import JWTHandler


class DetectDevice:

    def __init__(
        self,
        device_id: str = Header(
            None,
            pattern="^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
            alias="X-Device-ID",
        ),
        agent: str = Header(None, alias="User-Agent"),
    ):
        self._device_id: str = device_id
        if not self._device_id:
            raise HTTPException(status_code=400, detail="Device ID not found")
        self._agent: UserAgent = parse(agent if agent else "Unknown")

    def device(self):
        device_info = {
            "device_id": self._device_id,
        }
        if self._agent:
            if self._agent.browser:
                device_info["browser"] = self._agent.browser.family
            if self._agent.os:
                device_info["os"] = (
                    self._agent.os.family + " " + self._agent.os.version_string
                )
            if self._agent.device:
                device_info["device_type"] = self._agent.device.family
        return device_info


class UserSession:

    def __init__(
        self,
        storage: Storage = Depends(Storage),
        device_detector: DetectDevice = Depends(DetectDevice),
        auth_header: Annotated[
            HTTPAuthorizationCredentials, "Authorization header"
        ] = Depends(
            HTTPBearer(
                auto_error=False,
                scheme_name="Bearer",
            )
        ),
        auth_cookie: Annotated[str | None, Cookie(..., alias="auth")] = None,
        req: Request = None,
    ):
        self._db = storage._db
        self._jwt = JWTHandler(storage._fstore)
        self._req = req
        self._device = device_detector.device()
        self._user = None
        self._token = None
        try:
            self._token = auth_cookie or auth_header.credentials
            user_id = self._jwt.verify(self._token)["id"]
            self._user = self._db.query(User).filter(User.id == user_id).first()
        except Exception:
            pass
        self._authorized = self._user is not None
        if self._authorized:
            self.log()

    def log(self, type: SessionType = SessionType.ACTIVE):
        exist_device = (
            self._db.query(Device)
            .filter(Device.device_id == self._device["device_id"])
            .first()
        )
        if not exist_device:
            exist_device = Device(**self._device)
            self._db.add(exist_device)
            self._db.commit()
            self._db.refresh(exist_device)
        session = SessionInfo(
            user_id=self._user.id,
            location="Unknown",
            ip=self._req.client.host,
            user_agent=self._req.headers["User-Agent"] or "Unknown",
            device_fk=exist_device.id,
            type=type,
            token=self._token,
        )
        self._db.add(session)
        self._db.commit()
        self._db.refresh(session)
        return session

    def attach(self, user: User, token: str):
        self._user = user
        self._token = token
        self._authorized = True

    def get_authorized_user_id(self):
        return str(self._user.id) if self._authorized else None
