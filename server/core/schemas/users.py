from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from core.models.objects import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    workspace: str | None = None
    disabled: bool | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "email": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "workspace": "ACME Inc.",
                "disabled": False,
            }
        }


class UpdateUser(BaseModel):
    username: str | None
    email: EmailStr | None
    first_name: str | None
    last_name: str | None
    workspace: str | None
    disabled: bool | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "email": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "workspace": "ACME Inc.",
                "disabled": False,
            }
        }


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    workspace: str
    password: str

    class Config(User.Config):
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "email": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "workspace": "ACME Inc.",
                "password": "secret"
            }
        }


class UserInDB(User):
    hashed_password: str
