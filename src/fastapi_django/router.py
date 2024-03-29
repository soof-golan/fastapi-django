import uuid

from fastapi import APIRouter

from fastapi_django.models import User

router = APIRouter()


@router.get("/")
async def hello_world() -> dict[str, str]:
    return {"message": "Hello World"}


@router.get("/user/{user_id}")
async def user_get(user_id: uuid.UUID) -> dict:
    u = await User.objects.aget(id=user_id)
    return await User.objects.aget(id=user_id)


@router.post("/user/")
async def user_create() -> dict:
    return await User.objects.acreate(firebase_id=str(uuid.uuid4()))
