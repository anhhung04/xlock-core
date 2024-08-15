from fastapi import APIRouter, Depends
from services.auth import AuthService
from models.user import *
from models.auth import *

from utils.http import *
from utils.session import *

authRouter = APIRouter(tags=["Auth"])


@authRouter.post("/register", response_model=UserDetailResponse)
async def register_user(
    newUserInfo: CreateUserModel,
    service: AuthService = Depends(AuthService),
):
    new_user = await service.create(newUserInfo)
    return APIResponse.as_json(201, "User created successfully", new_user)


@authRouter.post("/login", response_model=UserAuthResponse)
async def login_user(
    authInfo: UserAuth,
    service: AuthService = Depends(AuthService),
):
    result = await service.gen_token(authInfo)

    res = APIResponse.as_json(200, "User logged in successfully", result)
    res.set_cookie(
        "auth", result["access_token"], httponly=True, samesite="strict", path="/"
    )
    return res


@authRouter.post("/verify", response_model=VerifyTokenResponse)
async def verify_token(
    tokenInfo: VerifyTokenRequest,
    service: AuthService = Depends(AuthService),
):
    result = await service.verify(tokenInfo.access_token)

    return APIResponse.as_json(200, "Token verified", result)


@authRouter.get("/me", response_model=UserDetailResponse)
async def get_user(
    service: AuthService = Depends(AuthService),
    session: UserSession = Depends(UserSession),
):
    user_id = session.get_authorized_user_id()
    if not user_id:
        return APIResponse.as_json(401, "Unauthorized", None)
    user = await service.get(user_id)
    return APIResponse.as_json(200, "OK", user)


@authRouter.patch("/user", response_model=UserDetailResponse)
async def update_user(
    userInfo: UpdateUserModel,
    service: AuthService = Depends(AuthService),
    session: UserSession = Depends(UserSession),
):
    user_id = session.get_authorized_user_id()
    if not user_id:
        return APIResponse.as_json(401, "Unauthorized", None)
    user = await service.update(user_id, userInfo)
    return APIResponse.as_json(200, "User updated successfully", user)

@authRouter.get("/keys/{subject}", response_model=CrytoKeyResponse)
async def get_keys(
    subject: str,
    service: AuthService = Depends(AuthService),
    user_session: UserSession = Depends(UserSession),
):
    caller_id = user_session.get_authorized_user_id()
    if not caller_id:
        return APIResponse.as_json(401, "Unauthorized", None)
    own_resource = subject == "me" or subject == caller_id
    keys = await service.get_keys(caller_id if own_resource else subject, own_resource)
    return APIResponse.as_json(200, "OK", keys)