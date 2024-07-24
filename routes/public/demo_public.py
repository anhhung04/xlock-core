from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def demo():
    return {"message": "Hello, world!"}
