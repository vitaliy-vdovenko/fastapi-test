import os
import motor.motor_asyncio
from typing import List
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from ..auth.models import UserModel, CreateUserModel, UpdateUserModel

router = APIRouter(prefix="/admin", tags=["admin"])
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.task_db


@router.post("/", response_description="Create new User", response_model=UserModel)
async def create_user(user: CreateUserModel = Body(...)):
    user_data = jsonable_encoder(user)
    password = user_data.pop('password')
    confirm_password = user_data.pop('confirm_password')
    user_data['hashed_pass'] = password
    new_user = await db["users"].insert_one(user_data)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.get("/", response_description="List all Users", response_model=List[UserModel])
async def list_users():
    students = await db["users"].find().to_list(1000)
    print(students)
    return students


@router.get("/{id}", response_description="Get a single User", response_model=UserModel)
async def show_user(user_id: str):
    if (user := await db["users"].find_one({"_id": user_id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.put("/{id}", response_description="Update a User", response_model=UserModel)
async def update_user(user_id: str, student: UpdateUserModel = Body(...)):
    user = {field: value for field, value in student.dict().items() if value is not None}

    if len(user) >= 1:
        update_result = await db["users"].update_one({"_id": user_id}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := await db["users"].find_one({"_id": user_id})
            ) is not None:
                return updated_user

    if (existing_user := await db["users"].users({"_id": user_id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@router.delete("/{id}", response_description="Delete a User")
async def delete_student(user_id: str):
    delete_result = await db["users"].delete_one({"_id": user_id})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

