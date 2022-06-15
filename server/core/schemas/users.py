from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from core.models.objects import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "email": "jdoe@example.com",
                "full_name": "John Doe",
                "disabled": False,
            }
        }


class UpdateUser(BaseModel):
    username: str | None
    email: EmailStr | None
    full_name: str | None
    disabled: bool | None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "jdoe@example.com",
                "email": "jdoe@example.com",
                "full_name": "John Doe",
                "disabled": False,
            }
        }


class UserInDB(User):
    hashed_password: str
