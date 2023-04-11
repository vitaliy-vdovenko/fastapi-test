import os
import motor.motor_asyncio
from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .models import UserModel

router = APIRouter(prefix="/auth", tags=["auth"])
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.task_db


@router.post("/", response_description="Add new student", response_model=UserModel, summary="Test")
async def create_student(student: UserModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await db["students"].insert_one(student)
    created_student = await db["students"].find_one({"_id": new_student.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
