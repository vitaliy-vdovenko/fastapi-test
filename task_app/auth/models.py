from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid object ID")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str = Field(...)
    last_name: str = Field(...)
    role: str = Field(...)
    is_active: str = Field(...)
    created_at: str = Field(...)
    last_login: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserModel(BaseUserModel):
    hashed_pass: str = Field(...)

    class Config(BaseUserModel.Config):
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "role": "simple mortal",
                "is_active": "false",
                "created_at": "datetime",
                "last_login": "datetime",
                "hashed_pass": "fakehashedsecret",
            }
        }


class CreateUserModel(BaseUserModel):
    password: str = Field(...)
    confirm_password: str = Field(...)

    class Config(BaseUserModel.Config):
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "role": "simple mortal",
                "is_active": "false",
                "created_at": "datetime",
                "last_login": "datetime",
                "password": "fakesecret",
                "confirm_password": "fakesecret",
            }
        }


class UpdateUserModel(BaseUserModel):
    pass

