from fastapi import APIRouter, Depends
from services.auth import AuthService
from models.user import *
from models.auth import *

from utils.http import *

authRouter = APIRouter()


@authRouter.post("/register", tags=["Auth"], response_model=UserDetailResponse)
async def register_user(
    newUserInfo: CreateUserModel,
    service: AuthService = Depends(AuthService),
):
    new_user = await service.create(newUserInfo)
    return APIResponse.as_json(201, "User created successfully", new_user)


@authRouter.post("/login", tags=["Auth"], response_model=UserAuthResponse)
async def login_user(
    authInfo: UserAuth,
    service: AuthService = Depends(AuthService),
):
    result = await service.gen_token(authInfo)

    await service.log(authInfo.email)

    res = APIResponse.as_json(200, "User logged in successfully", result)
    res.set_cookie(
        "auth", result["access_token"], httponly=True, samesite="strict", path="/api"
    )
    return res


@authRouter.post("/verify", tags=["Auth"], response_model=VerifyTokenResponse)
async def verify_token(
    tokenInfo: VerifyTokenRequest,
    service: AuthService = Depends(AuthService),
):
    result = await service.verify(tokenInfo.access_token)

    return APIResponse.as_json(200, "Token verified", result)


@authRouter.get("/user", tags=["Auth"], response_model=UserDetailResponse)
async def get_user(
    service: AuthService = Depends(AuthService),
    session: UserSession = Depends(UserSession),
):
    user = await service.get(session._user_id)
    return APIResponse.as_json(200, "OK", user)

@authRouter.patch("/user", tags=["Auth"], response_model=UserDetailResponse)
async def update_user(
    userInfo: UpdateUserModel,
    service: AuthService = Depends(AuthService),
    session: UserSession = Depends(UserSession),
):
    user = await service.update(session._user_id, userInfo)
    return APIResponse.as_json(200, "User updated successfully", user)

@authRouter.delete("/user", tags=["Auth"], response_model=UserDetailResponse)
async def delete_user(
    service: AuthService = Depends(AuthService),
    session: UserSession = Depends(UserSession),
):
    await service.delete(session._user_id)
    return APIResponse.as_json(200, "User deleted successfully")