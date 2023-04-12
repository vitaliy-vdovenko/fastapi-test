from bson import ObjectId
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, validator


class RoleEnum(str, Enum):
    admin = 'admin'
    dev = 'dev'
    simple_mortal = 'simple mortal'


class PyObjectId(ObjectId):
    """Handling ObjectIds before storing them as the _id."""
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
    """Base model, which includes common fields"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str = Field(...)
    last_name: str = Field(...)
    role: RoleEnum = RoleEnum.simple_mortal

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserModel(BaseUserModel):
    """User Model with all fields"""
    is_active: bool = Field(...)
    created_at: datetime = Field(...)
    last_login: datetime | None = Field(...)
    hashed_pass: str = Field(...)

    class Config(BaseUserModel.Config):
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "role": "simple mortal",
                "is_active": "false",
                "created_at": "2023-04-11T10:52:42.931253",
                "last_login": "2023-04-11T10:52:42.931253",
                "hashed_pass": "fakehashedsecret",
            }
        }


class CreateUserModel(BaseUserModel):
    """Created model with setting default value for created_at field"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    password: str = Field(...)
    confirm_password: str = Field(...)

    @validator('confirm_password')
    def passwords_match(cls, confirm_password, values, **kwargs):
        if 'password' in values and confirm_password != values['password']:
            raise ValidationError('Passwords do not match')
        return confirm_password

    class Config(BaseUserModel.Config):
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "role": "simple mortal",
                "password": "fakesecret",
                "confirm_password": "fakesecret",
            }
        }


class UpdateUserModel(BaseUserModel):
    """Update model"""
    first_name: str | None
    last_name: str | None
    role: str | None
    is_active: bool | None
    created_at: datetime | None
    last_login: datetime | None

    @validator('role')
    def name_must_contain_space(cls, role):
        available_roles = [member.value for member in RoleEnum]
        if role not in available_roles:
            raise ValidationError('Available options are admin, dev and simple simple mortal')
        return role

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "Jane",
                "last_name": "Doe",
                "role": "simple mortal",
                "is_active": True,
                "created_at": "2023-04-11T10:52:42.931253",
                "last_login": "2023-04-11T10:52:42.931253",
            }
        }


