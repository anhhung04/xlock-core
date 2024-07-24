from fastapi import APIRouter, Depends
from services.demo import DemoService

from utils.http import APIResponse

router = APIRouter()


@router.get("/")
async def demo(
    demo_service: DemoService = Depends(DemoService),
):
    print("DemoRoute")
    demo_service.demo()
    return APIResponse.as_json(200, "OK!", "Hello, world!")
