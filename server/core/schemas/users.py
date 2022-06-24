from bson import ObjectId
from pydantic import BaseModel, Field

from core.objects import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    first_name: str | None = None
    last_name: str | None = None
    workspaces: list[str] | None = None
    disabled: bool | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "workspaces": ["ACME Inc.", "Boring Co."],
                "disabled": False,
            }
        }


class UpdateUser(BaseModel):
    username: str | None
    first_name: str | None
    last_name: str | None
    workspaces: list[str] | None
    disabled: bool | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "workspaces": ["ACME Inc.", "Boring Co."],
                "disabled": False,
            }
        }


class RegisterUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    workspaces: str
    password: str

    class Config(User.Config):
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "workspaces": "ACME Inc.",
                "password": "secret",
            }
        }


class UserInDB(User):
    hashed_password: str
    otp_secret: str | None
    otp_validated: bool = False
