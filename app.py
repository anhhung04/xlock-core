from fastapi import FastAPI, status, APIRouter
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from utils.http import APIResponse
from utils.log import logger

from config import config
from routes.v1 import * 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config["ALLOWED_HOSTS"],
    allow_credentials=True,
    allow_methods=config["ALLOWED_METHODS"],
)

api_router = APIRouter(prefix="/v1")

api_router.include_router(demo_router, tags=["Demo"], prefix="/demo")
api_router.include_router(authRouter, tags=["Auth"], prefix="/auth")
api_router.include_router(itemRouter, tags=["Item"], prefix="/items")

app.include_router(api_router, prefix="/api", tags=["App API v1"])


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return APIResponse.as_json(exc.status_code, exc.detail, {})


@app.exception_handler(RequestValidationError)
async def request_validate_handler(request, exc):
    return APIResponse.as_json(
        status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid request", exc.errors()
    )


app.add_event_handler(
    "startup",
    lambda: logger.info(
        "Application starting up", app_name="xlock", environment="production"
    ),
)
