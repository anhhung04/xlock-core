import uvicorn

import os

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from config import config

from utils.http import APIResponse

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config["ALLOWED_HOSTS"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_imports():
    base_path = "./routes"
    subdirs = ["api", "public"]
    imports = []

    for subdir in subdirs:
        path = os.path.join(base_path, subdir)
        if not os.path.isdir(path):
            continue
        for route in os.listdir(path):
            if route.startswith("_") or not route.endswith(".py"):
                continue
            module_name = route.removesuffix(".py")
            import_statement = f"from routes.{subdir} import {module_name}"
            imports.append(import_statement)

    return imports


imports = generate_imports()
for imp in imports:
    print(imp)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return APIResponse.as_json(exc.status_code, exc.detail, {})


@app.exception_handler(RequestValidationError)
async def request_validate_handler(request, exc):
    return APIResponse.as_json(
        status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid request", exc.errors()
    )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=config["HOST"],
        port=config["PORT"],
        reload=True,
        workers=config["workers"] if config["PROD"] else 1,
    )
